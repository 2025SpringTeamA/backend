from fastapi import APIRouter
from app.api.endpoints import auth, admin, user, session, message, emotion, favorite, generated_media

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(user.router, tags=["User"])
api_router.include_router(session.router, tags=["Session"])
api_router.include_router(message.router, tags=["Message"])
api_router.include_router(emotion.router, tags=["Emotion"])
api_router.include_router(favorite.router, tags=["Favorite"])
api_router.include_router(generated_media.router, tags=["GeneratedMedia"])