from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Session as SessionModel
from models import User
from schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionWithMessagesResponse, SessionSummaryResponse
from core.database import get_db
from utils.auth import get_current_user
from utils.timestamp import now_jst
from services.session import get_sessions_with_first_message, toggle_favorite_session, delete_session


router = APIRouter()

# -----------------
# チャットの開始
# -----------------
@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    user_id=current_user.id
    today = now_jst().date()
    
    # 当日のセッションを確認
    existing_session = db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.created_at >= datetime.combine(today, datetime.min.time()),
        SessionModel.created_at <= datetime.combine(today, datetime.max.time())
    ).first()
    
    # if existing_session:
    #     # 1日１回制限：エラーメッセージで伝える
    #     raise HTTPException(
    #         status_code=403,
    #         detail="今日はすでにチャットを開始しています。明日またご利用ください。"
    #     )
    
    
    new_session = SessionModel(
        character_mode=session_data.character_mode,
        user_id=user_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# ----------------
# チャット一覧取得
# ----------------
@router.get("/sessions", response_model=list[SessionSummaryResponse])
async def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    favorite_only: bool =False,
    keyword: Optional[str] = None
    ):
    return get_sessions_with_first_message(
        db = db,
        user_id = current_user.id, 
        favorite_only = favorite_only,
        keyword = keyword
    )


# -------------------
# 特定のチャットを取得
# -------------------
@router.get("/sessions/{session_id}", response_model=SessionWithMessagesResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="セッションが見つかりません。")
    
    messages =[{
        "message_id": m.id,
        "message_text": m.content,
        "sender_type": "user" if m.is_user else "ai"
    } for m in session.messages
    ]
    
    return {
        "session_id" : session.id,
        "messages" : messages,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


# -------------------
# 特定のチャットを変更
# -------------------
@router.patch("/sessions/{session_id}", response_model= SessionResponse)
async def update_session(
    id: int, 
    session_data: SessionUpdate, 
    db: Session = Depends(get_db),
    current_user : User= Depends(get_current_user)
    ):

    session = db.query(SessionModel).filter(
        SessionModel.id == id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
    
    # 更新
    if session_data.character_mode:
        session.character_mode = session_data.character_mode
        
    db.commit()
    db.refresh(session)
    return session


# ------------------
# 特定のチャットを削除
# ------------------
@router.delete("/sessions/{session_id}")
async def delete_session_route(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_session(db, session_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="チャットが見つかりません。")
    return {"message": "チャットを削除しました。"}


# ----------------
# お気に入りのトグル
# ----------------
@router.post("/sessions/{session_id}/favorite")
def toggle_favorite(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return toggle_favorite_session(db, session_id, current_user.id)
