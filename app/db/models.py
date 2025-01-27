from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    kakao_user_id = Column(String, primary_key=True)
    encrypted_korail_id = Column(String)
    encrypted_korail_pw = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    macros = relationship("MacroJob", back_populates="user")

class MacroJob(Base):
    __tablename__ = "macro_jobs"
    
    id = Column(Integer, primary_key=True)
    kakao_user_id = Column(String, ForeignKey("users.kakao_user_id"))
    departure_station = Column(String)
    arrival_station = Column(String)
    target_date = Column(String)  # YYYYMMDD format
    target_time = Column(String)  # HHMMSS format
    train_type = Column(String)
    seat_type = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="macros")
