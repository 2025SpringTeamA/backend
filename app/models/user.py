from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo
from .base import Base, TimestampMixin

JST = ZoneInfo("Asia/Tokyo")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    user_name = Column(String, nullable=False)
    poem_id = Column(Integer, ForeignKey("poems.id"))
    is_admin = Column(Boolean, default=False)

    sessions = relationship("Session", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
