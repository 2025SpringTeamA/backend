from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Favorite, Session as DBSession
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.core.database import get_db

@router.post("/favorites")
async def create_favorite(favorite_data: FavoriteCreate, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == favorite_data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="お気に入り登録が見つかりません。")
    favorite = Favorite(session_id=favorite_data.session_id, user_id=favorite_data.user_id)
    db.add(favorite)
    db.commit()
    return favorite

@router.get("/favorites")
async def get_favorites(user_id: int, db: Session = Depends(get_db)):
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    return favorites