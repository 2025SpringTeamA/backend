from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Message, Session as ChatSession
from schemas.message import MessageCreate
from core.database import get_db

router = APIRouter()

@router.post("/sessions/{session_id}/messages")
async def create_message(session_id: int, message_data: MessageCreate, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="メッセージが見つかりません。")
    message = Message(content=message_data.content, session_id=session_id)
    db.add(message)
    db.commit()
    return message

# @router.put("/sessions/{session_id}/messages/{message_id}")
# async def update_message(session_id: int, message_id: int, message_data: MessageUpdate, db: Session = Depends(get_db)):
#     message = db.query(Message).filter(Message.id == message_id).first()
#     if not message:
#         raise HTTPException(status_code=404, detail="メッセージが見つかりません。")
#     message.content = message_data.content
#     db.commit()
#     return message
