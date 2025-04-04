# ──────────────────────────────────────────────────────────────────────
# © 2025 PII Sentinel™
# Proprietary & Confidential – All Rights Reserved
#
# This software is the confidential and proprietary information of
# PII Sentinel™ ("Confidential Information"). You shall not disclose
# such Confidential Information and shall use it only in accordance
# with the terms of a binding agreement or license.
#
# Unauthorized reproduction, modification, or distribution of this
# software or its components, in whole or in part, is strictly prohibited.
#
# For licensing, partnership, or commercial use, contact:
# Bo.k.harris@gmail.com
# ──────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import joblib
from pydantic import BaseModel
import pandas as pd
from typing import List
import logging
import os
import shutil
import uuid
import re
import numpy as np
from utils.redaction import scan_and_redact_column

#RIP THIS OUT
from database.database import Base, engine
from database.models.user import User

#Create the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PII Sentinel", description="Real-Time PII Detection and Refaction API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
feature_columns = [ "length", "num_underscores", "num_digits", "has_at",
    "has_email_keyword", "pct_email_like", "pct_phone_like", 
    "pct_ssn_like", "pct_ip_like", "avg_digits_per_val", "avg_val_len"]
#load trained model
MODEL_PATH = "models/pii_classifier.pkl"
model = joblib.load(MODEL_PATH)

#Set up logging
logging.basicConfig(filename="logs/api.log", level=logging.INFO,
format='%(asctime)s - %(message)s')

#Output folder
os.makedirs("uploads", exist_ok=True)
os.makedirs("redacted", exist_ok=True)

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_RE = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
SSN_RE = re.compile(r"\d{3}-\d{2}-\d{4}")
IP_RE = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")



class PredictionResult(BaseModel):
    filename: str
    pii_columns: List[str]
    redacted_file: str
    risk_score: float
    
@app.post("/predict", response_model=PredictionResult)
async def predict(file: UploadFile = File(...)):
    #Save the upload file
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Invalid CSV file"})
    
    #Predict PII columns using model
    features = df.columns.tolist()
    X = pd.DataFrame(features, columns=["column"])
    X["length"] = X["column"].apply(len)
    X["num_underscores"] = X["column"].apply(lambda x: x.count("_"))
    X["num_digits"] = X["column"].apply(lambda x: sum(c.isdigit() for c in x))
    X["has_at"] = X["column"].apply(lambda x: int("@" in x))
    X["has_email_keyword"] = X["column"].apply(lambda x: int("email" in x.lower()))
    
    # Pull sample values from the uploaded data
    value_samples = [df[col].dropna().astype(str).head(3).tolist() for col in df.columns]
    X["parsed_values"] = value_samples

    # Value-based features
    def pct_match(regex, values):
        return np.mean([bool(regex.search(str(v))) for v in values]) if values else 0

    X["pct_email_like"] = X["parsed_values"].apply(lambda v: pct_match(EMAIL_RE, v))
    X["pct_phone_like"] = X["parsed_values"].apply(lambda v: pct_match(PHONE_RE, v))
    X["pct_ssn_like"] = X["parsed_values"].apply(lambda v: pct_match(SSN_RE, v))
    X["pct_ip_like"] = X["parsed_values"].apply(lambda v: pct_match(IP_RE, v))
    X["avg_digits_per_val"] = X["parsed_values"].apply(lambda v: np.mean([sum(c.isdigit() for c in str(i)) for i in v]) if v else 0)
    X["avg_val_len"] = X["parsed_values"].apply(lambda v: np.mean([len(str(i)) for i in v]) if v else 0)
    
    #match the training time features
    predictions = model.predict(X[feature_columns])

    print(predictions)
    for name, pred in zip(features, predictions):
        print(f"{name}: {'PII' if pred == 0 else 'Non-PII'}")

    pii_columns = [col for col, is_pii in zip(features, predictions) if is_pii == 0]
    
    #Redact PII 
    redacted_df = df.copy()
    for col in pii_columns:
        redacted_df[col] = scan_and_redact_column(redacted_df[col])
        
    redacted_path = f"redacted/redacted_{file_id}_{file.filename}"
    redacted_df.to_csv(redacted_path, index=False)

    #Log the request
    logging.info(f"Processed file: {file.filename} | PII Columns: {pii_columns}")
    return PredictionResult(
        filename=file.filename,
        pii_columns=pii_columns,
        redacted_file=redacted_path,
        risk_score=round(len(pii_columns)/ len(df.columns), 2)
    )
    
@app.get("/")
def root():
    return {"message": "Welcome to PII Sentinel API. Upload a CSV to detect and redact PII."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pii_app:app", host="127.0.0.1", port=8000, reload=True)

