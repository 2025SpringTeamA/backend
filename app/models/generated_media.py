from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .base import Base, TimestampMixin

class MessageTypeEnum(str, enum.Enum)
    IMAGE = "image"
    BGM - "bgm"

class GeneratedMedia(Base, TimestampMixin):
    __tablename__ = "generated_media"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    emotion_id = Column(Integer, ForeignKey("emotion.id"))
    media_type = Column(Enum(MediaTypeEnum), nullable=False)
    media_url = Column(String(255), nullable=False)

    image_prompt = Column(Text, nullable=True)

    bgm_prompt = Column(Text, nullable=True)
    bgm_duration = Column(Integer, nullable=True)

    message = relationship("Message", back_populates="generated_media")
    emotion = relationship("Emotion", back_populates="generated_media")
    