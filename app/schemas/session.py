from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CharacterMode(str, Enum):
    SABURO = "saburo"
    BIJYO = "bijyo"
    ANGER_MOM = "anger_mom"

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