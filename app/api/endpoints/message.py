from fastapi import Request, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from models import Message, Session as SessionModel
from models import User
from schemas.message import MessageCreate, MessageResponse, MessageUpdate
from core.database import get_db
from utils.auth import get_current_user
from services.message import create_message_with_ai, create_message as create_user_message, get_messages_by_session, update_user_message ,delete_message


router = APIRouter()
# レートリミッター
limiter = Limiter(key_func=get_remote_address)


# 日記の投稿またはキャラクターの返答を作成
@router.post("/sessions/{session_id}/messages")
@limiter.limit("2/minute")  # IPごとに2回/分
async def create_message(
    request: Request,
    session_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
        # SessionModel.user_id == 1 # テスト
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
        
    # return create_user_message(db, session_id, content=message_data.content) #テスト

    try:
        return await create_message_with_ai(db, session_id, message_data.content)
    except HTTPException as e:
        print(f"HTTPエラー: {e.detail}") 
        raise e
    except Exception as e:
        print(f"未処理エラー:{e}")
        raise HTTPException(status_code=500, detail="サーバ内部エラー")


# 特定のチャットの全メッセージを取得
@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_messages_endpoint(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
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
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
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
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません。")

    delete_message(db, message_id)
    return {"message": "メッセージを削除しました。"}