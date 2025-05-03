from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import User
from schemas.user import UserUpdate, PasswordUpdate, UserResponse
from core.database import get_db
from utils.auth import hash_password, verify_password, get_current_user
from utils.timestamp import now_jst


router = APIRouter()

# アカウント情報取得
@router.get("/api/user", response_model=UserResponse)
async def get_my_account(current_user: User = Depends(get_current_user)):
    return current_user


# アカウント情報の更新
@router.patch("/api/user", response_model=UserResponse)
async def update_my_account(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # メールアドレスの更新
    if user_update.email and user_update.email != current_user.email:
        # 他のユーザと重複していないかチェック
        if db.query(User).filter_by(email=user_update.email).first():
            raise HTTPException(status_code=400, detail="このメールアドレスはすでに使われています")
        current_user.email = user_update.email
    
    if user_update.user_name:
        current_user.user_name = user_update.user_name
    
    db.commit()
    db.refresh(current_user)
    return current_user


# パスワード変更 
@router.put("/api/password")
async def change_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="現在のパスワードが間違っています")
    
    current_user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "パスワードを変更しました"}


# アカウント凍結
@router.delete("/api/user")
async def deactivate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="管理者アカウントは削除できません")
    
    current_user.is_active =False
    current_user.deleted_at = now_jst()
    db.commit()
    return {"message": "アカウントを削除しました"}


# アカウント削除
@router.delete("/api/user/delete")
async def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="管理者アカウントは削除できません")
    
    db.delete(current_user)
    db.commit()
    return {"message": "アカウントを完全に削除しました"}