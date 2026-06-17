from typing import Union

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, String
from werkzeug.datastructures import FileStorage

from models.base import Base


class MarkerPhoto(Base):
    __tablename__ = "marker_photos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    marker_id = Column(Integer, ForeignKey("markers.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255), nullable=False)


class MarkerPhotoSchema(BaseModel):
    id: int
    marker_id: int
    file_path: str


class MarkerPhotoCreateDto(BaseModel):
    marker_id: int
    file_path: str


class MarkerPhotoUploadDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    file: Union[FileStorage, None] = None
    marker_id: int
