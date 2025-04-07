from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database.database import sessionmaker
from database.models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto" )

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
@router.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(sessionmaker)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already redistered")
    
    hashed_password = pwd_context.hash(data.password)
    new_user = User(email=data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message": "User registered successfully", "user_id": new_user.id}