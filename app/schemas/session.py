from fastapi import Query
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CharacterMode(str, Enum):
    SABURO = "saburo"
    BIJYO = "bijyo"
    ANGER_MOM = "anger_mom"

class SessionQueryParams(BaseModel):
    skip: int = 0
    limit: int = 20
    favorite_only: bool = False
    keyword: Optional[str] = None

class SessionBase(BaseModel):
    user_id: int
    character_mode: CharacterMode

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SessionSummaryResponse(BaseModel):
    session_id: int
    character_mode: CharacterMode
    first_message: Optional[str] = ""
    created_at: datetime

    class Config:
        from_attributes = True