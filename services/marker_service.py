from typing import List
from models.marker import MarkerCreateDto, MarkerSchema, MarkerWithPhotosSchema
from models.marker_photo import MarkerPhotoCreateDto, MarkerPhotoUploadDto
from repositories.marker_photo_repository import MarkerPhotoRepository
from repositories.marker_repository import MarkerRepository
from storages.marker_photo_file_storage import MarkerPhotoFileStorage


class MarkerService:
    def __init__(
            self, 
            marker_repository: MarkerRepository,
            marker_photo_repository: MarkerPhotoRepository,
            marker_photo_file_storage: MarkerPhotoFileStorage
        ):
        self.marker_repository = marker_repository
        self.marker_photo_repository = marker_photo_repository
        self.marker_photo_file_storage = marker_photo_file_storage
    
    def create(self, marker: MarkerCreateDto):
        marker_schema = MarkerSchema(**marker.model_dump(exclude=["photos"]))
        marker_id = self.marker_repository.create(marker_schema)
        for photo in marker.photos:
            fpath = self.marker_photo_file_storage.upload_file(MarkerPhotoUploadDto(marker_id=marker_id, file=photo))
            self.marker_photo_repository.create(MarkerPhotoCreateDto(marker_id=marker_id, file_path=fpath))
        return marker_id

    def get_near_markers(self, latitude : float, longitude : float) -> List[MarkerWithPhotosSchema]:
        markers = self.marker_repository.get_nearest_by_radius(latitude, longitude)
        return [
            MarkerWithPhotosSchema(
                **marker.model_dump(), 
                photos=self.marker_photo_repository.get_by_marker_id(marker.id)
            )
            for marker in markers
        ]

    def get_by_user_id(self, user_id: int) -> List[MarkerWithPhotosSchema]:
        markers = self.marker_repository.get_by_user_id(user_id)
        return [
            MarkerWithPhotosSchema(
                **marker.model_dump(),
                photos=self.marker_photo_repository.get_by_marker_id(marker.id)
            )
            for marker in markers
        ]

    def get_by_id(self, marker_id: int) -> MarkerWithPhotosSchema:
        marker = self.marker_repository.get_by_id(marker_id)
        if marker is None:
            raise ValueError("Отметка не найдена")
        return MarkerWithPhotosSchema(
            **marker.model_dump(),
            photos=self.marker_photo_repository.get_by_marker_id(marker.id)
        )