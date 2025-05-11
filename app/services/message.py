from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from typing import List
from models.message import Message, ResponseTypeEnum
from models.session import Session as SessionModel, CharacterModeEnum
from schemas.message import MessageResponse
from services.ai.generator import generate_ai_response, generate_ai_response_via_bedrock


# テスト用-日記を保存
def create_message(
    db: Session,
    session_id: int,
    content: str,
) -> MessageResponse:
    # ユーザーの日記を保存
    user_message = Message(
        session_id=session_id,
        content=content,
        is_user=True
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # セッションを取得してモードを確認
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
    character_mode = session.character_mode

    return MessageResponse.from_orm(user_message), character_mode




# 日記を保存してキャラクターの返答を生成
async def create_message_with_ai(
    db: Session,
    session_id: int,
    content: str,
) -> MessageResponse:
    # ユーザーの日記を保存
    user_message = Message(
        session_id=session_id,
        content=content,
        is_user=True
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    print("ユーザーの日記を保存")
    
    # セッションを取得してモードを確認
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="チャットが見つかりません")
    character_mode = session.character_mode
    
    # AI返答を生成
    ai_reply, response_type = await run_in_threadpool(
        # generate_ai_response, # Open API用
        # generate_ai_response_via_bedrock, # Amazon Bedrock用
        character_mode=character_mode,
        user_input=content
    )
    
    # AI返答を保存
    ai_message = Message(
        session_id=session_id,
        content=ai_reply,
        is_user=False,
        response_type=response_type
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    # AI返答を返す
    return MessageResponse.from_orm(ai_message)


# チャット内の全メッセージを取得
def get_messages_by_session(db: Session, session_id: int) -> List[MessageResponse]:
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    return [MessageResponse.from_orm(m) for m in messages]


# メッセージを更新
def update_user_message(db: Session, message_id: int, new_content: str) -> MessageResponse:
    db_message = db.query(Message).filter(Message.id == message_id, Message.is_user == True).first()
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
    
