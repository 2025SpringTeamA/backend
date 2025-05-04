from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Message, Session as ChatSession
from models import User
from schemas.message import MessageCreate, MessageResponse, MessageUpdate
from core.database import get_db
from utils.auth import get_current_user
from services.message import create_message_with_ai, get_messages_by_session, update_user_message ,delete_message


router = APIRouter()


# 日記の投稿またはキャラクターの返答を作成
@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def create_message(
    session_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
    
    return create_message_with_ai(db, session_id, content=message_data.content)


# 特定のチャットの全メッセージを取得
@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_messages_endpoint(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")

    return get_messages_by_session(db, session_id)


# ユーザのメッセージを更新
@router.put("/sessions/{session_id}/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    session_id: int,
    message_id: int,
    message_data: MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")

    return update_user_message(db, message_id, message_data.content)


# 特定のメッセージを削除
@router.delete("/sessions/{session_id}/messages/{message_id}")
async def delete_message_endpoint(
    session_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません。")

    delete_message(db, message_id)
    return {"message": "メッセージを削除しました。"}