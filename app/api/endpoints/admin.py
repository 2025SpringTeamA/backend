# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from models import User, Session as ChatSession, Message
# from core.database import get_db
# from utils.auth import hash_password, verify_password, create_access_token

# router = APIRouter()

# @router.post("/admin/register/")
# async def register_admin(admin_data: User, db: Session = Depends(get_db)):
#     if db.query(User).filter_by(email=admin_data.email).first():
#         raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")
    
#     new_admin = User(
#         email=admin_data.email,
#         password_hash=hash_password(admin_data.password),
#         user_name=admin_data.user_name,
#         pin_code=str(admin_data.pin_code)
#     )
#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     token = create_access_token({"sub": str(new_admin.id)})
#     return {"token": token}

# @router.post("/admin/login")
# async def login_admin(admin_data: AdminLogin, db: Session = Depends(get_db)):
#     admin = db.query(Admin).filter_by(email=admin_data.email).first()
#     if not admin:
#         raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います。")
    
#     if not verify_password(admin_data.password, admin.password_hash):
#         raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが違います。")
    
#     if admin_data.pin_code != admin.pin_code:
#         raise HTTPException(status_code=400, detail="PINコードが正しくありません。")
    
#     token = create_access_token({"sub": str(new_admin.id)})
#     return {"token": token}


# @router.get("/admin_info")
# async def get_admin_info(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     return current_admin


# @router.get("/users")
# async def get_users(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     users = db.query(User).filter_by(is_active=True).all()
#     return users


# @router.delete("/users/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません。")
    
#     db.delete(user)
#     db.commit()
#     return {"message": "ユーザーが削除されました。"}

# # ユーザーアカウントを凍結する処理
# @router.patch("/users/{user_id}/deactivate")
# async def deactivate_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません。")
    
#     user.is_active = False
#     db.commit()
#     return {"message": "ユーザーが無効化されました。"}


# # ユーザーアカウントを有効化する処理
# @router.patch("/users/{user_id}/activate")
# async def activate_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません。")
    
#     user.is_active = True
#     db.commit()
#     return {"message": "ユーザーが有効化されました。"}


# @router.patch("/users/{user_id}")
# async def update_user(user_id: int, user_data: UserBase, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません。")
    
#     user.user_name = user_data.user_name
#     user.email = user_data.email

#     db.commit()
#     return {"message": "ユーザー情報が更新されました。"}

# @router.get("/messages")
# async def get_messages(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     messages = db.query(Message).all()
#     return messages

# @router.patch("/settings")
# async def update_settings(new_message: str, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
#     settings = db.query(Settings).first()
#     settings.support_message = new_message
#     db.commit()
#     return {"message": "設定が更新されました。"}