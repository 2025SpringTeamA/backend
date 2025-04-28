# db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from dotenv import load_dotenv
from models import Base


DATABASE_URL = os.getenv("DATABASE_URL")


# MySQL用：connect_argsなしでエンジン作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースの接続を管理する関数
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
