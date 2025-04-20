# models/base.py
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime
from utils.time import now_jst

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=now_jst)
    updated_at = Column(DateTime(timezone=True), default=now_jst, onupdate=now_jst)
