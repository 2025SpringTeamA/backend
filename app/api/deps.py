from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends

# データベースセッションを依存関係として注入する
def get_db_dependency(db: Session = Depends(get_db)):
    return db
