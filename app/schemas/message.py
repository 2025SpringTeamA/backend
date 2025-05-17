from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
from schemas.user import UserResponse


class ResponseType(str, Enum):
    PRAISE = "praise"
    INSULT = "insult"

class MessageBase(BaseModel):
    session_id: int
    is_user: bool
    response_type: Optional[ResponseType] = None
    content: str
    
    class Config:
        from_attributes = True

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str

class MessageResponse(MessageBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True
        
        
# 履歴の詳細表示用
class MessageDetail(BaseModel):
    message_id: int
    message_text: str
    sender_type: Literal["user", "ai"]



# 管理者投稿一覧表示
class AdminMessageResponse(BaseModel):
    user_name: str
    content: str
    created_at: Optional[datetime]


    class Config:
        from_attributes = True