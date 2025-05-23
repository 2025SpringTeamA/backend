from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, TimestampMixin

class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    session = relationship("Session", back_populates="favorites")
    user = relationship("User", back_populates="favorites")
