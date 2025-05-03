from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base, TimestampMixin

class CharacterModeEnum(str, enum.Enum):
    saburo = "saburo"
    bijyo = "bijyo"
    anger_mom = "anger_mom"

class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    character_mode = Column(Enum(CharacterModeEnum), nullable=False)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="session", cascade="all, delete-orphan")
