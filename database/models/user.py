from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True) #TODO: make it not nullable
    device_token = relationship("DeviceToken", back_populates="user")