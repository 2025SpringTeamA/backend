from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    message_id: int
    user_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True