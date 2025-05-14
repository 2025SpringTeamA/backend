from sqlalchemy.orm import Session
from sqlalchemy import cast, String, or_
from models.session import Session as SessionModel
from models.message import Message
from models.favorite import Favorite
from schemas.session import SessionSummaryResponse
from fastapi import HTTPException


# チャット履歴取得
def get_sessions_with_first_message(
    db: Session, 
    user_id: int,
    favorite_only: bool = False,
    keyword: str | None = None,
    )->list[SessionSummaryResponse]:
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    
    if favorite_only or keyword:
        query = query.join(SessionModel.messages)
        
    if favorite_only:
        query = query.join(SessionModel.favorites)
        
    # 　キーワード検索
    if keyword:
        query = query.join(SessionModel.messages).filter(
            or_(
                Message.content.ilike(f"%{keyword}%"),
                cast(SessionModel.created_at, String).ilike(f"%{keyword}%")
            )
        )
        
    sessions =  query.distinct().all()

    result = []
    for session in sessions:
        first_message = (
            db.query(Message)
            .filter(Message.session_id == session.id)
            .order_by(Message.created_at.asc())
            .first()
        )
        
        is_fav = db.query(Favorite).filter(
            Favorite.session_id == session.id,
            Favorite.user_id == user_id
        ).first() is not None
        
        result.append(SessionSummaryResponse(
            session_id=session.id,
            character_mode=session.character_mode,
            first_message=first_message.content[:20] if first_message else "",
            created_at=session.created_at,
            is_favorite=is_fav
        ))
    return result


# 管理者用投稿内容一覧
def get_all_sessions_with_first_message(
    db:Session,
)-> list[dict]:
    sessions = db.query(SessionModel).join(SessionModel.user).all()
    result = []
    for session in sessions:
        first_user_message = (
            db.query(Message)
            .filter(
                Message.session_id == session.id,
                Message.is_user == True
            )
            .order_by(Message.created_at.asc())
            .first()
        )
        
        if first_user_message:
            result.append({
                "user_name": session.user.user_name,
                "content": first_user_message.content,
                "created_at": first_user_message.created_at or session.created_at,
            })
    return result



# 履歴削除
def delete_session(
    db: Session,
    session_id: int,
    user_id: int
)-> bool:
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if not session:
        return False
    
    db.delete(session) # cascade設定によりメッセージも削除される
    db.commit()
    return True


# お気に入りのトグル
def toggle_favorite_session(
    db: Session,
    session_id: int,
    user_id: int
)->dict:
    # セッションの存在を確認
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail= "チャットが見つかりません")
        
    # お気に入りの状態チェック
    favorite = db.query(Favorite).filter_by(
            session_id = session_id,
            user_id = user_id
        ).first()
    
    if favorite:
        db.delete(favorite)
        db.commit()
        return{"message": "お気に入りを解除しました", "is_favorite": False}
    else:
        new_fav = Favorite(
            session_id = session_id,
            user_id = user_id
        )
        db.add(new_fav)
        db.commit()
        return {"message": "お気に入りを追加しました", "is_favorite": True}
    