from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from .base import Base


class Contact(Base):
    __tablename__ = "contacts"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    contact_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

class ContactSchema(BaseModel):
    user_id: int
    contact_id: int