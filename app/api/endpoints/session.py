from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Session as ChatSession
from app.models import Favorite, User
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionWithMessagesResponse, SessionSummaryResponse
from app.core.database import get_db
from app.utils.auth import get_current_user
from service.session import get_sessions_with_first_message
from typing import Optional


# TODO::チャットの開始
@router.post("/sessions")
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_session = ChatSession(chat_title=session_data.chat_title, user_id=current_user.id)
    db.add(new_session)
    db.commit()
    return new_session


# チャット一覧取得
@router.get("/api/sessions", response_model=list[SessionSummaryResponse])
async def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    favorite_only: bool =False,
    keyword: Optional[str] = None
    ):
    return get_sessions_with_first_message(
        db = db,
        user_id = current_user.user_id, 
        favorite_only = favorite_only,
        keyword = keyword
    )


# 特定のチャットを取得
@router.get("/api/sessions/{id}", response_model=SessionWithMessagesResponse)
async def get_session(id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    return {
        "chat_id" : session.id,
        "messages" : [
            {
                "message_id": m.id,
                "message_text": m.content,
                "sender_type": "user" if m.is_users else "ai"
            }for m in session.messages
        ],
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


# 特定のチャットを変更
@router.patch("/api/sessions/{id}", response_model= SessionResponse)
async def update_session(
    id: int, 
    session_data: SessionUpdate, 
    db:Session = Depends(get_db)
    ):
    # TODO::tokenからuser_idを取得
    
    session = db.query(Session).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
    
    # 更新
    if session_data.character_mode:
        session.character_mode = session_data.character_mode
        
    db.commit()
    db.refresh(session)
    return session


# 特定のチャットを削除
@router.delete("/api/sessions/{id}")
async def delete_session(id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    db.delete(session)
    db.commit()
    raise {"message": "チャットを削除しました。"}


# お気に入りのトグル
@router.post("/api/favorites")
def toggle_favorite(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    # セッションの存在を確認
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        if not session:
            raise HTTPException(status_code=404, detail= "")
        
    # お気に入りの状態チェック
    favorite = db.query(Favorite).filter_by(
            session_id = session_id,
            user_id = current_user.id
        ).first()
    
    if favorite:
        db.delete(favorite)
        db.commit()
        return{"message": "お気に入りを解除しました", "is_favorite": False}
    else:
        new_fav = Favorite(
            session_id = session_id,
            user_id = current_user.id
        )
        db.add(new_fav)
        db.commit()
        return {"message": "お気に入りを追加しました", "is_favorite": True}
    
