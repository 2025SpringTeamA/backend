from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Session as ChatSession, Message
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.core.database import get_db
from app.utils.auth import get_current_user

@router.post("/sessions")
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_session = ChatSession(chat_title=session_data.chat_title, user_id=current_user.id)
    db.add(new_session)
    db.commit()
    return new_session

@router.get("/sessions")
async def get_session(id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    retuen session

@router.patch("/sessions")
async def update_session(id: int, session_data: SessionUpdate, db:Session = Depends(get_db) ):
    session = db.query(ChatSession).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    session.chat_title = session_data.chat_title
    db.commit()
    return session

@router.delete("/sessions")
async def delete_session(id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    db.delete(session)
    db.commit()
    raise {"message": "セッションを削除しました。"}
