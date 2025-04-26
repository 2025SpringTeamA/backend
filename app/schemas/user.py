from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    user_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    user_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True