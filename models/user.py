from .base import Base
from sqlalchemy import Column, Integer, String, Text
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    nickname = Column(String(100), unique=True)
    password = Column(Text)


class UserSchema(BaseModel):
    id: int | None = None
    email: str
    nickname: str
    password: str

class UserInfoSchema(BaseModel):
    id: int
    nickname: str


class SigninSchema(BaseModel):
    nickname: str
    password: str