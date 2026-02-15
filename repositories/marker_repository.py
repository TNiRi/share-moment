from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.marker import Marker, MarkerSchema


class MarkerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, marker: MarkerSchema):
        marker_model = Marker(**marker.model_dump())
        self.db.add(marker_model)
        self.db.commit()
    
    def get_by_user_id(self, user_id: int) -> List[MarkerSchema]:
        markers = self.db.query(Marker).filter(Marker.user_id == user_id).all()
        return [
            MarkerSchema.model_validate(marker, from_attributes = True)
            for marker in markers
        ]
    
    def get_all(self) -> List[MarkerSchema]:
        markers = self.db.query(Marker).all()
        return [
            MarkerSchema.model_validate(marker, from_attributes = True)
            for marker in markers
        ]
    
    def get_nearest_by_radius(self, latitude : float, longitude : float) -> List[MarkerSchema]:
        markers = self.db.query(Marker).filter(
            func.abs(Marker.latitude - latitude) < (Marker.radius_km / 111),
            func.abs(Marker.longitude - longitude) < (Marker.radius_km / 111)
        ).all()
        return [
            MarkerSchema.model_validate(marker, from_attributes = True)
            for marker in markers
        ]