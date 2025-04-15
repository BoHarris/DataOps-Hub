from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import os
import shutil
import uuid
import re
import numpy as np
import logging
import joblib

from utils.redaction import scan_and_redact_column

router = APIRouter(prefix="/predict", tags=["Prediction"])

xgb_model = joblib.load("models/xgboost_model.pkl")

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_RE = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
SSN_RE = re.compile(r"\d{3}-\d{2}-\d{4}")
IP_RE = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")

class PredictionResult(BaseModel):
    filename: str
    pii_columns: list[str]
    redacted_file: str
    risk_score: float

@router.post("/", response_model=PredictionResult)
async def predict(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    file_path = f"uploads/{file_id}{ext}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        df = pd.read_csv(file_path)
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid CSV file"})

    features = df.columns.tolist()
    X = pd.DataFrame(features, columns=["column"])
    X["length"] = X["column"].apply(len)
    X["num_underscores"] = X["column"].apply(lambda x: x.count("_"))
    X["num_digits"] = X["column"].apply(lambda x: sum(c.isdigit() for c in x))
    X["has_at"] = X["column"].apply(lambda x: int("@" in x))
    X["has_email_keyword"] = X["column"].apply(lambda x: int("email" in x.lower()))

    value_samples = [df[col].dropna().astype(str).head(3).tolist() for col in df.columns]
    X["parsed_values"] = value_samples

    def pct_match(regex, values):
        return np.mean([bool(regex.search(str(v))) for v in values]) if values else 0

    X["pct_email_like"] = X["parsed_values"].apply(lambda v: pct_match(EMAIL_RE, v))
    X["pct_phone_like"] = X["parsed_values"].apply(lambda v: pct_match(PHONE_RE, v))
    X["pct_ssn_like"] = X["parsed_values"].apply(lambda v: pct_match(SSN_RE, v))
    X["pct_ip_like"] = X["parsed_values"].apply(lambda v: pct_match(IP_RE, v))
    X["avg_digits_per_val"] = X["parsed_values"].apply(lambda v: np.mean([sum(c.isdigit() for c in str(i)) for i in v]) if v else 0)
    X["avg_val_len"] = X["parsed_values"].apply(lambda v: np.mean([len(str(i)) for i in v]) if v else 0)

    def contains_dob_pattern(values):
        dob_re = re.compile(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}[/-]\d{1,2}[/-]\d{1,2})")
        return any(bool(dob_re.search(str(v))) for v in values)

    def contains_gender_term(values):
        gender_terms = {"male", "female", "nonbinary", "trans", "woman", "man"}
        return any(str(v).strip().lower() in gender_terms for v in values)

    def contains_street_suffix(values):
        street_suffixes = {"st", "street", "ave", "road", "rd", "blvd", "ln", "lane"}
        return any(str(v).strip().lower().split()[-1] in street_suffixes for v in values)

    def contains_city_name(values):
        cities = {"new york", "los angeles", "miami"}
        return any(str(v).lower() in cities for v in values)

    def contains_known_name(values):
        names = {"alice", "bob", "charlie", "john", "jane"}
        return any(any(word.lower() in names for word in str(v).split()) for v in values)

    def contains_zip_code_pattern(values):
        zip_code_re = re.compile(r"\b\d{5}(?:-\d{4})?\b")
        return any(bool(zip_code_re.search(str(v))) for v in values)

    def contains_phone_pattern(values):
        phone_patterns = [
            re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"),
            re.compile(r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
        ]
        return any(any(p.search(str(v)) for p in phone_patterns) for v in values)

    X["has_dob_pattern"] = X["parsed_values"].apply(contains_dob_pattern)
    X["has_gender_term"] = X["parsed_values"].apply(contains_gender_term)
    X["has_street_suffix"] = X["parsed_values"].apply(contains_street_suffix)
    X["has_city_name"] = X["parsed_values"].apply(contains_city_name)
    X["has_known_name"] = X["parsed_values"].apply(contains_known_name)
    X["has_zip_pattern"] = X["parsed_values"].apply(contains_zip_code_pattern)
    X["has_phone_pattern"] = X["parsed_values"].apply(contains_phone_pattern)

    feature_columns = [
        "length", "num_underscores", "num_digits", "has_at",
        "has_email_keyword", "pct_email_like", "pct_phone_like",
        "pct_ssn_like", "pct_ip_like", "avg_digits_per_val", "avg_val_len",
        "has_dob_pattern", "has_gender_term", "has_street_suffix",
        "has_city_name", "has_known_name", "has_zip_pattern", "has_phone_pattern"
    ]

    predictions = xgb_model.predict(X[feature_columns])
    pii_columns = [col for col, is_pii in zip(features, predictions) if is_pii == 0]

    redacted_df = df.copy()
    for col in pii_columns:
        redacted_df[col] = scan_and_redact_column(redacted_df[col])

    redacted_path = f"redacted/redacted_{file_id}{ext}"
    redacted_df.to_csv(redacted_path, index=False)

    logging.info(f"Processed file: {file.filename} | PII Columns: {pii_columns}")

    return PredictionResult(
        filename=file.filename,
        pii_columns=pii_columns,
        redacted_file=redacted_path,
        risk_score=round(len(pii_columns) / len(df.columns), 2)
    )
