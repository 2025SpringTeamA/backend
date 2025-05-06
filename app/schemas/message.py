from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResponseType(str, Enum):
    PRAISE = "praise"
    INSULT = "insult"

class MessageBase(BaseModel):
    session_id: int
    is_user: bool
    response_type: Optional[ResponseType] = None
    content: str

class MessageCreate(MessageBase):
    content: str
    character_mode: Optional[str] = None

class MessageUpdate(BaseModel):
    content: str

class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True