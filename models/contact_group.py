from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String

from models.base import Base


class ContactGroup(Base):
    __tablename__ = "contact_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))


class ContactGroupContact(Base):
    __tablename__ = "contact_group_contacts"
    contact_group_id = Column(Integer, ForeignKey("contact_groups.id"), primary_key=True)
    contact_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


class ContactGroupSchema(BaseModel):
    id: int
    title: str
    user_id: int


class ContactGroupContactSchema(BaseModel):
    contact_group_id: int
    contact_id: int


class ContactGroupCreateSchema(BaseModel):
    title: str
    user_id: int
    contact_ids: List[int]