from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MediaType(str, Enum):
    IMG = "img"
    BGM = "bgm"

class GeneratedMediaBase(BaseModel):
    message_id: int
    emotion_id: int
    media_type: MediaType
    image_prompt: Optional[str] = None
    bgm_prompt: Optional[str] = None
    bgm_duration: Optional[str] = None

class GeneratedMediaCreate(GeneratedMediaBase):
    pass

class GeneratedMediaResponse(GeneratedMediaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    clsss Config:
    from_attributes = True