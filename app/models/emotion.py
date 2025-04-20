from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, TimestampMixin

class Emotion(Base,  TimestampMixin):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    emotion = Column(String(255), nullable=False)

    generated_images = relationship("GeneratedImage", back_populates="emotion")
    generated_bgms = relationship("GeneratedBGM", back_populates="emotion")
