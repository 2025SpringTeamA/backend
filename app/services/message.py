from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.message import Message
from schemas.message import MessageCreate, MessageResponse


# メッセージ（日記またはキャラクターの返答）を作成
def create_message(
    db: Session,
    session_id: int,
    content: str,
    is_users: bool = True
) -> MessageResponse:
    db_message = Message(session_id=session_id, content=content, is_users=is_users)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return MessageResponse.from_orm(db_message)


# チャット内の全メッセージを取得
def get_messages_by_session(db: Session, session_id: int) -> List[MessageResponse]:
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    return [MessageResponse.from_orm(m) for m in messages]


# メッセージを更新
def update_user_message(db: Session, message_id: int, new_content: str) -> MessageResponse:
    db_message = db.query(Message).filter(Message.id == message_id, Message.is_users == True).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="該当するメッセージが見つかりません") #　もしくはreturn None
    db_message.content = new_content
    db.commit()
    db.refresh(db_message)
    return MessageResponse.from_orm(db_message)


# メッセージ削除
def delete_message(db: Session, message_id: int) -> None:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="該当するメッセージが見つかりません")
    db.delete(db_message)
    db.commit()
