
# ──────────────────────────────────────────────────────────────────────
# Importing necessary modules and classes
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database import get_db
from database.models.user import User
from database.models.device_token import DeviceToken
from utils.auth_utils import create_access_token, decode_token
from datetime import datetime, timedelta, timezone
import secrets
import logging

TIER_LIMITS = {
    "free": 10,
    "pro": 50,
    "business": None
}

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto" )


# User Registration

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")
    tier: str = Field(default="free", description="User tier, default is 'free'")
    device_name: str = Field(description="Name of the device")
    ip_address: str = Field(description="IP address of the device")

# ──────────────────────────────────────────────────────────────────────
# User Registration Endpoint
# This endpoint allows a new user to register by providing their email, password, and device information.
# The password is hashed before storing it in the database.


@router.post("/register", response_model=dict)
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    logging.info(f"Registering user: {data.email}")
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # ──────────────────────────────────────────────────────────────────────
    #Hash password
    hashed_password = pwd_context.hash(data.password)
    tier=data.tier.lower()
    new_user = User(
        name= data.name,
        email=data.email, 
        hashed_password=hashed_password,
       tier=tier
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
# ──────────────────────────────────────────────────────────────────────
#set tier limits

    max_devices = TIER_LIMITS.get(tier, 10)

    device_count = db.query(DeviceToken).filter(DeviceToken.user_id == new_user.id).count()
    if max_devices is not None and device_count >= max_devices:
        raise HTTPException(
            status_code=400, 
            detail=f"{data.tier.capitalize()} tier allows {max_devices} device(s)"
            )
    
    device_token = DeviceToken(
         user_id=new_user.id,
        token=secrets.token_hex(32),
        device_name=data.device_name,
        ip_address=data.ip_address,
        created_at=datetime.now(timezone.utc),
        last_used_at=datetime.now(timezone.utc)
    )
    db.add(device_token)
    db.commit()
    
    return{
        "message": "User registered successfully",
        "user_id": new_user.id,
        "device_token": device_token.token
    }