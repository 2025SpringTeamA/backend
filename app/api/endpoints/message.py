from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.message import create_message, get_message, update_message, delete_message
from schemas.message import MessageCreate, MessageResponse
from db.session import get_db
from typing import List

router = APIRouter()

@router.post("/messages/", response_model=MessageResponse)
def create_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db=db, message=message)

@router.get("/messages/{session_id}", response_model=List[MessageResponse])
def get_message_endpoint(session_id: int, db: Session = Depends(get_db)):
    return get_message(db=db, session_id=session_id)

@router.put("/messages/{message_id}", response_model=MessageResponse)
def update_message_endpoint(message_id: int, content: str, db: Session = Depends(get_db)):
    return update_message(db=db, message_id=message_id, content=content)

@router.delete("/messages/{message_id}", status_code=204)
def delete_message_endpoint(message_id: int, db: Session = Depends(get_db)):
    delete_message(db=db, message_id=message_id)
    return {"detail": "Message deleted"}
