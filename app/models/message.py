from sqlalchemy import Column, Integer, Boolean, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base, TimestampMixin

class ResponseTypeEnum(str, enum.Enum):
    praise = "praise"
    insult = "insult"

class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"))
    is_user = Column(Boolean, default=True)
    response_type = Column(Enum(ResponseTypeEnum))
    content = Column(Text, nullable=False)

    session = relationship("Session", back_populates="messages")