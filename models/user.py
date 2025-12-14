from .base import Base
from sqlalchemy import Column, Integer, String, Text


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    nickname = Column(String(100), unique=True)
    password = Column(Text)
    