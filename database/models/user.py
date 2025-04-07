from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    
    created_at = Column(String, default=func.now())
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True) #TODO: make it not nullable
    role = Column(String, default="free") #represents the role of the user, e.g. free, pro, admin
    stripe_customer_id = Column(String, nullable=True)
    scans_this_month = Column(Integer, default=0) #number of scans the user has done this month