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
    password: Optional[str] = None
    

# パスワード変更・リクエスト
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


# アカウント登録・ログイン　レスポンス
class TokenResponse(BaseModel):
    token: str
    
    class Config:
        from_attributes = True


# アカウント情報取得・レスポンス
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    user_name: str
    is_active: bool
    can_be_deleted:  Optional[bool] = False # 管理画面の「削除可能」表示用

    class Config:
        from_attributes = True