from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.message import Message
from app.schemas.session import SessionSummaryResponse


def get_sessions_with_first_message(
    db: Session, 
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    favorite_only: bool = False,
    keyword: str | None = None,
    ):
    """
    指定したユーザーIDに紐づくセッション一覧を取得します。
    セッションごとに、最初のメッセージの内容と作成日時をまとめて返します。

    Args:
        db (Session): データベースセッション
        user_id (int): ユーザーID
        skip (int, optional): 取得開始位置（デフォルト0）
        limit (int, optional): 取得件数（デフォルト100）
        favorite_only (bool, optional): お気に入りメッセージが存在するセッションのみ取得する場合True（デフォルトFalse）
        keyword (str | None, optional): メッセージ本文に含まれるキーワードでフィルタリングする場合に指定（デフォルトNone）

    Returns:
        セッション情報（session_id、character_mode、first_message、created_at）をまとめたリスト
    """
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    
    if favorite_only:
        query = query.join(SessionModel.messages).join(Message.favorites).distinct()
        
    if keyword:
        query = query.join(SessionModel.messages).filter(Message.content.ilike(f"%{keyword}%")).distinct()
    
    sessions = query.offset(skip).limit(limit).all()
    result = []
    for session in sessions:
        first_message = (
            db.query(Message)
            .filter(Message.session_id == session.id)
            .order_by(Message.created_at.asc())
            .first()
        )
        result.append(SessionSummaryResponse(
            session_id=session.id,
            character_mode=session.character_mode,
            first_message=first_message.content[:20] if first_message else "",
            created_at=session.created_at,
        ))
    return result