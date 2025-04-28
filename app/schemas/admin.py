from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    email: EmailStr
    password: str
    user_name: str
    pin_code: int

class AdminLogin(BaseModel):
    email: EmailStr
    password: str
    pin_code: int

class AdminResponse(BaseModel):
    id: int
    email: EmailStr
    user_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
