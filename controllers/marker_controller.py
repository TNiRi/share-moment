from flask import jsonify, request
from models.marker import MarkerSchema
from services.marker_service import MarkerService
from utils.auth import authorized


class MarkerController:
    def __init__(self, marker_service: MarkerService):
        self.marker_service = marker_service
    
    @authorized
    def create(self, user_id: int):
        try:
            if request.is_json:
                body = request.get_json()
                marker_data = MarkerSchema(**body, user_id=user_id)
                self.marker_service.create(marker_data)
                return jsonify({"Message" : "Метка успешно создана"}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except Exception as e:
            return jsonify({"Message" : str(e)}), 500
    
    @authorized
    def get_nearest_markers(self, user_id: int):
        try:
            if request.is_json:
                body = request.get_json()
                latitude = body.get("latitude")
                longitude = body.get("longitude")
                markers = self.marker_service.get_near_markers(latitude, longitude)
                return jsonify([
                    marker.model_dump()
                    for marker in markers
                ]), 200
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except Exception as e:
            return jsonify({"Message" : str(e)}), 500