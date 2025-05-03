from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from core.config import settings
from schemas.user import UserRegister, UserLogin, TokenResponse
from models import User
from core.database import get_db
from utils.auth import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter()

# アカウント登録
@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):

    if db.query(User).filter_by(email=user_data.email).first():
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")
    
    new_user = User(
        email=user_data.email,
        user_name=user_data.user_name,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"token": token}


# ログイン
@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います。")
    
    if user.is_admin:
        if user_data.pin_code is None:
            raise HTTPException(status_code=400, detail="PINコードが必要です。")
        if user_data.pin_code != settings.admin_pin_code:
            raise HTTPException(status_code=400, detail="PINコードが違います。")
        
    token = create_access_token({"sub": str(user.id)})
    return {"token": token}
        

# ログアウト
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "ログアウトしました。"}