# db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from models import Base

# ローカル開発環境のみ .env を読み込む
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

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
