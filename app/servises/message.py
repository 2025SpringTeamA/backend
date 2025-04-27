from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate


def create_message(db: Session, message: MessageCreate) -> Message:
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, session_id: int) -> list[Message]:
    return db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()


def update_message(db: Session, message_id: int, content: str) -> Message:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="該当するメッセージが見つかりません") #　もしくはreturn None
    db_message.content = content
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int) -> None:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
