from models.marker import MarkerSchema
from repositories.marker_repository import MarkerRepository


class MarkerService:
    def __init__(self, marker_repository: MarkerRepository):
        self.marker_repository = marker_repository
    
    def create(self, marker: MarkerSchema):
        self.marker_repository.create(marker)