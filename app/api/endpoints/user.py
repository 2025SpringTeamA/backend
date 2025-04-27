from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.database import get_db
from app.utils.auth import create_access_token, verify_password

@router.get("/user")
async def get_user_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/user")
async def updated_user_info(user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.email = user_data.email
    current_user.user_name = user_data.user_name
    db.commit()
    return current_user

@router.delete("/user")
async def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db:delete(current_user)
    db.commit()
    return {"message": "アカウントを削除しました。"}