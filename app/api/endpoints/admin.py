from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from models import User, Message
from schemas.user import UserRegister, UserLogin, UserUpdate, UserResponse, TokenResponse
from core.config import settings
from core.database import get_db
from utils.auth import hash_password, verify_password, create_access_token, get_current_admin_user
from utils.timestamp import now_jst

router = APIRouter()


# 管理者アカウント登録
@router.post("/admin/register/", response_model=TokenResponse)
async def register_admin(
    admin_data: UserRegister,
    db: Session = Depends(get_db)
):
    if db.query(User).filter_by(email=admin_data.email).first():
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")
    
    new_admin = User(
        email=admin_data.email,
        password_hash=hash_password(admin_data.password),
        user_name=admin_data.user_name,
        is_admin=True
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    token = create_access_token({"sub": str(new_admin.id)})
    return {"token": token }


# 管理者ログイン
@router.post("/admin/login", response_model=TokenResponse)
async def login_admin(
    admin_data: UserLogin,
    db: Session = Depends(get_db)
):
    admin = db.query(User).filter_by(email=admin_data.email, is_admin=True).first()
    if not admin:
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います")
    
    if not verify_password(admin_data.password, admin.password_hash):
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います")
    
    # PINコードは.envファイルから取得
    if str(admin_data.pin_code) != settings.ADMIN_PIN_CODE:
        raise HTTPException(status_code=400, detail="PINコードが正しくありません")
    
    token = create_access_token({"sub": str(admin_data.id)})
    return {"token": token, "is_admin": admin_data.is_admin}


# 管理者アカウント情報取得
@router.get("/admin_info", response_model=UserResponse)
async def get_admin_info(
    current_admin: User = Depends(get_current_admin_user)
):
    return current_admin


# 一般ユーザ情報一覧取得
@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    users = db.query(User).filter(User.is_admin==False).all()
    now = now_jst()
    return [
        UserResponse(
            user_id=user.id,
            email=user.email,
            user_name=user.user_name,
            is_active=user.is_active,
            can_be_delete=(
                not user.is_active
                and user.deleted_at
                and (now - user.deleted_at >= timedelta(days=30))
            )
        )for user in users
    ]


# ユーザーアカウントを削除する処理
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    if user.is_active or not user.deleted_at:
        raise HTTPException(status_code=400, detail="無効化されたアカウントのみ削除可能です")
    
    now = now_jst()
    if user.deleted_at + timedelta(days=30) > now:
        raise HTTPException(status_code=400, detail=f"{now - user.deleted_at}日後に削除可能です")
    
    db.delete(user)
    db.commit()
    return {"message": "ユーザーが削除されました"}


# ユーザーアカウントを凍結する処理
@router.patch("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    user.is_active = False
    user.deleted_at = now_jst()
    db.commit()
    return {"message": "ユーザーが無効化されました"}


# ユーザーアカウントを有効化する処理
@router.patch("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    user.is_active = True
    user.deleted_at = None # 論理削除日時をリセット
    db.commit()
    return {"message": "ユーザーが有効化されました"}


# ユーザー情報更新
@router.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    if user_data.user_name is None and user_data.email is None:
        raise HTTPException(status_code=400, detail="更新内容がありません")
    
    if user_data.user_name is not None:
        user.user_name = user_data.user_name
    if user_data.email is not None:
        user.email = user_data.email

    db.commit()
    return {"message": "ユーザー情報が更新されました"}


# TODO:削除？:投稿一覧
# @router.get("/messages")
# async def get_messages(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     messages = db.query(Message).all()
#     return messages

# TODO:設定変更
# @router.patch("/settings")
# async def update_settings(
#     new_message: str,
#     db: Session = Depends(get_db),
#     current_admin: User = Depends(get_current_admin_user)):
#     settings = db.query().first()
#     settings.support_message = new_message
#     db.commit()
#     return {"message": "設定が更新されました。"}