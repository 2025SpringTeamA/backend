from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(string(255), nullable=False)
    pin_code = Column(String(6), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="admin")