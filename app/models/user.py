from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    user_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True) # 論理削除日時
    is_admin = Column(Boolean, default=False)
    
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
