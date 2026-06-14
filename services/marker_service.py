from typing import List
from models.marker import MarkerSchema
from repositories.marker_repository import MarkerRepository


class MarkerService:
    def __init__(self, marker_repository: MarkerRepository):
        self.marker_repository = marker_repository
    
    def create(self, marker: MarkerSchema):
        self.marker_repository.create(marker)

    def get_near_markers(self, latitude : float, longitude : float) -> List[MarkerSchema]:
        return self.marker_repository.get_nearest_by_radius(latitude, longitude)

    def get_by_user_id(self, user_id: int) -> List[MarkerSchema]:
        return self.marker_repository.get_by_user_id(user_id)

    def get_by_id(self, marker_id: int) -> MarkerSchema:
        marker = self.marker_repository.get_by_id(marker_id)
        if marker is None:
            raise ValueError("Отметка не найдена")
        return marker