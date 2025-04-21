from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, TimestampMixin

class Poem(Base,TimestampMixin):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    poem = Column(Text, nullable=False)
    
    users = relationship("User", backref="poem")
