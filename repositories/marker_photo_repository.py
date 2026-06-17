from typing import List

from models.marker_photo import MarkerPhoto, MarkerPhotoCreateDto, MarkerPhotoSchema
from repositories.abstract_repository import AbstractRepository


class MarkerPhotoRepository(AbstractRepository):
    def create(self, marker_photo: MarkerPhotoCreateDto) -> None:
        marker_photo_model = MarkerPhoto(**marker_photo.model_dump())
        self.db.add(marker_photo_model)
        self.db.commit()

    def get_by_marker_id(self, marker_id: int) -> List[MarkerPhotoSchema]:
        return [
            MarkerPhotoSchema.model_validate(photo, from_attributes=True)
            for photo in self.db.query(MarkerPhoto)
            .filter(MarkerPhoto.marker_id == marker_id).all()
        ]

    def delete_by_id(self, photo_id: int) -> None:
        photo = self.db.query(MarkerPhoto).filter(MarkerPhoto.id == photo_id).first()
        if photo is not None:
            self.db.delete(photo)
            self.db.commit()

    def delete_by_marker_id(self, marker_id: int) -> None:
        photos = self.db.query(MarkerPhoto).filter(MarkerPhoto.marker_id == marker_id).all()
        for photo in photos:
            self.db.delete(photo)
        self.db.commit()
