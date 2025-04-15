from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from database.models.user import User
from database.models.device_token import DeviceToken
from utils.auth_utils import create_access_token
from datetime import timedelta
from passlib.context import CryptContext
import logging

router = APIRouter(prefix="/auth", tags=["Login"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token
@router.post("/token", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username.strip().toLower()
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    logging.warning(f"Failed login attempt for user: {form_data.username}")   
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")

    # Grab most recent device (later: match by IP/device)
    device_token = db.query(DeviceToken).filter(DeviceToken.user_id == user.id).order_by(DeviceToken.created_at.desc()).first()
    if not device_token:
        raise HTTPException(status_code=400, detail="Device token not found")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "device_token": device_token.token},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }