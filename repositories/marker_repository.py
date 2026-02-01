from typing import List
from sqlalchemy.orm import Session
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
            MarkerSchema.model_validate(marker, from_atributes = True)
            for marker in markers
        ]