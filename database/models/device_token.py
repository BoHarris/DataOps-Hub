from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import secrets

class DeviceToken(Base):
    __tablename__ = 'device_tokens'
    
    id = Column(Integer, primary_key=True, index =True)
    user_id = Column(Integer< ForeignKey('user.id'))
    token = Column(String, unique=True, default=lambda: secrets.token_hex(32))
    device_name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utc)
    last_used_at = Column(DateTime, default=datetime.utc)
    user = relationship("User", back_populates="device_tokens")