from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from database.database import get_db
from database.models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto" )

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")
    
@router.post("/register", response_model=dict)
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    print("Registering user with email: ", data.email)
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(data.password)
    new_user = User(email=data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}