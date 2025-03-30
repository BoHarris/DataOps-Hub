from fastapi import FastAPI, File, UploadFile, Form
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
from utils.redaction import scan_and_redact_column
app = FastAPI(title="PII Sentinel", description="Real-Time PII Detection and Refaction API")

feature_columns = ["length", "num_underscores", "has_at", 
                   "has_email_keyword"]
#load trained model
MODEL_PATH = "models/pii_classifier.pkl"
model = joblib.load(MODEL_PATH)

#Set up logging
logging.basicConfig(filename="logs/api.log", level=logging.INFO,
format='%(asctime)s - %(message)s')

#Output folder
os.makedirs("uploads", exist_ok=True)
os.makedirs("redacted", exist_ok=True)

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

