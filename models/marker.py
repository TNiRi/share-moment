from pydantic import BaseModel
from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, Text
from .base import Base


class Marker(Base):
    __tablename__ = "markers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    latitude = Column(Numeric(precision=9, scale=6), nullable=False)
    longitude = Column(Numeric(precision=10, scale=6), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

class MarkerSchema(BaseModel):
    id: int | None = None
    label: str
    description: str
    latitude: float
    longitude: float
    user_id: int