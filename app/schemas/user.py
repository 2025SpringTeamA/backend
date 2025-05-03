from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# アカウント登録・リクエスト
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    user_name: str
    is_admin: Optional[bool] = False


# ログイン・リクエスト 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    pin_code: Optional[int] = None  # 管理者ログイン時のみ使用


# アカウント情報更新・リクエスト
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    

# パスワード変更・リクエスト
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


# アカウント登録・ログイン　レスポンス
class TokenResponse(BaseModel):
    token: str


# アカウント情報取得・レスポンス
class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    user_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True