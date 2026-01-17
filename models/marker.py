from sqlalchemy import Column, Float, Integer, String, ForeignKey
from .base import Base


class Marker(Base):
    __tablename__ = "markers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))