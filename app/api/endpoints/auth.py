from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.models import User
from app.core.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):

    if db.query(User).filter_by(email=user_data.email).first():
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")
    
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"token": token}

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います。")
    
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います。")

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "ログアウトしました。"}