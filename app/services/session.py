from sqlalchemy.orm import Session
from models.session import Session as SessionModel
from models.message import Message
from models.favorite import Favorite
from schemas.session import SessionSummaryResponse


def get_sessions_with_first_message(
    db: Session, 
    user_id: int,
    favorite_only: bool = False,
    keyword: str | None = None,
    ):
    """
    指定したユーザーIDに紐づくセッション一覧を取得します。
    セッションごとに、最初のメッセージの内容と作成日時をまとめて返します。

    Args:
        db (Session): データベースセッション
        user_id (int): ユーザーID
        favorite_only (bool, optional): お気に入りメッセージが存在するセッションのみ取得する場合True（デフォルトFalse）
        keyword (str | None, optional): メッセージ本文に含まれるキーワードでフィルタリングする場合に指定（デフォルトNone）

    Returns:
        セッション情報（session_id、character_mode、first_message、created_at）をまとめたリスト
    """
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    
    if favorite_only or keyword:
        query = query.join(SessionModel.messages)
    
    if favorite_only:
        query = query.join(SessionModel.favorites)
        
    if keyword:
        query = query.filter(Message.content.ilike(f"%{keyword}%"))
    
    sessions = query.distinct().all()
    result = []
    for session in sessions:
        first_message = (
            db.query(Message)
            .filter(Message.session_id == session.id)
            .order_by(Message.created_at.asc())
            .first()
        )
        
        is_fav = db.query(Favorite).filter(
            session_id = session.id,
            user_id = user_id
        ).first() is not None
        
        result.append(SessionSummaryResponse(
            session_id=session.id,
            character_mode=session.character_mode,
            first_message=first_message.content[:20] if first_message else "",
            created_at=session.created_at,
            is_favorite=is_fav
        ))
    return result


def delete_session(db: Session, session_id: int, user_id: int):
    """指定したセッションとそのメッセージを削除します。

    Args:
        db (Session): データベースセッション
        session_id (int): 削除対象のセッションID
        user_id (int): ユーザーID（本人確認用）
    """
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user_id
    ).first()
    
    if  not session:
        return False
    
    db.query(Message).filter(Message.session_id == session_id).delete()
    
    db.delete(session)
    db.commit()
    
    return True