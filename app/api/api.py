from fastapi import APIRouter
from api.endpoints import auth, admin, user, session, message


router = APIRouter()


# 認証用エンドポイント
router.include_router(auth.router, tags=["Auth"])
# 管理者用エンドポイント
router.include_router(admin.router, tags=["Admin"])
# アカウント情報用エンドポイント
router.include_router(user.router, tags=["User"])
# チャット用エンドポイント
router.include_router(session.router, tags=["Session"])
# メッセージ用エンドポイント
router.include_router(message.router, tags=["Message"])