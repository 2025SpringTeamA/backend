from fastapi import Query
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from schemas.message import MessageDetail


class CharacterMode(str, Enum):
    SABURO = "saburo"
    BIJYO = "bijyo"
    ANGER_MOM = "anger_mom"

class SessionQueryParams(BaseModel):
    favorite_only: bool = False
    keyword: Optional[str] = None

class SessionBase(BaseModel):
    character_mode: CharacterMode

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    character_mode: Optional[CharacterMode] = None
    token: str
    
    class Config:
        from_attributes = True

class SessionResponse(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SessionSummaryResponse(BaseModel):
    session_id: int
    character_mode: CharacterMode
    first_message: Optional[str] = ""
    created_at: datetime
    is_favorite: bool = False

    class Config:
        from_attributes = True
        

class MessageSummary(BaseModel):
    message_id :int
    message_text: str
    sender_type : str # "user" or "ai"
    
    
class SessionWithMessagesResponse(BaseModel):
    session_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageDetail]