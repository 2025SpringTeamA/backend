from pydantic import BaseModel
from datetime import datetime

class EmotionBase(BaseModel):
    emotion: str

class EmotionCreate(EmotionBase):
    pass

class EmotionResponse(EmotionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True