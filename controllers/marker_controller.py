from typing import List

from flask import Request, jsonify, request
from werkzeug.datastructures import FileStorage
from models.marker import MarkerCreateDto, MarkerSchema
from services.marker_service import MarkerService
from utils.auth import authorized


class MarkerController:
    def __init__(self, marker_service: MarkerService):
        self.marker_service = marker_service
    
    @staticmethod
    def _get_files_from_form_data(
            r: Request
    ) -> List[FileStorage]:
        files = []
        i = 0
        while True:
            file = r.files.get(f"photo[{i}]", None)
            if file is None:
                break

            files.append(file)
            i += 1
        return files

    @authorized
    def create(self, user_id: int):
        try:
            if request.form:
                body = request.form
                marker_data = MarkerCreateDto(
                    label=body.get("label"),
                    description=body.get("description"),
                    latitude=float(body.get("latitude")),
                    longitude=float(body.get("longitude")),
                    radius_km=float(body.get("radius_km", 1)),
                    user_id=user_id,
                    photos=self._get_files_from_form_data(request)
                )
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
                    if marker.user_id != user_id
                ]), 200
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except Exception as e:
            return jsonify({"Message" : str(e)}), 500

    @authorized
    def get_by_user_id(self, user_id: int):
        try:
            markers = self.marker_service.get_by_user_id(user_id)
            return jsonify([
                marker.model_dump()
                for marker in markers
            ]), 200
        except Exception as e:
            return jsonify({"Message" : str(e)}), 500

    @authorized
    def get_by_id(self, user_id: int, marker_id: int):
        try:
            marker = self.marker_service.get_by_id(marker_id)
            return jsonify(marker.model_dump()), 200
        except ValueError as e:
            return jsonify({"Message": str(e)}), 404
        except Exception as e:
            return jsonify({"Message" : str(e)}), 500
