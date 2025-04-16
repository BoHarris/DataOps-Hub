from fastapi import FastAPI, File, UploadFile, Request
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
from database.database import Base, engine
from routers import register,login, protected
from routers.predict_router import router as predict_router


app = FastAPI(title="PII Sentinel", description="Real-Time PII Detection and Refaction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(protected.router)
app.include_router(predict_router)

Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"details": str(exc)})

logging.basicConfig(filename="logs/api.log", level=logging.INFO, format='%(asctime)s - %(message)s')
os.makedirs("uploads", exist_ok=True)
os.makedirs("redacted", exist_ok=True)



@app.get("/")
def root():
    return {"message": "Welcome to PII Sentinel API. Upload a CSV to detect and redact PII."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
