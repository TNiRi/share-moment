from flask import Blueprint

from controllers.marker_controller import MarkerController


class MarkerRouter:
    def __init__(self, controller: MarkerController):
        self.controller = controller
        self._router = Blueprint("markers", __name__)
        self._router.add_url_rule("/",
                                    view_func=self.controller.create,
                                    methods=["POST"],
                                    endpoint="create_marker")
        self._router.add_url_rule("/near/",
                                    view_func=self.controller.get_nearest_markers,
                                    methods=["POST"],
                                    endpoint="get_nearest_markers")
        self._router.add_url_rule("/",
                                    view_func=self.controller.get_by_user_id,
                                    methods=["GET"],
                                    endpoint="get_my_markers")
        self._router.add_url_rule("/<int:marker_id>/",
                                    view_func=self.controller.get_by_id,
                                    methods=["GET"],
                                    endpoint="get_marker_by_id")
        self._router.add_url_rule("/image/",
                                    view_func=self.controller.get_image_by_path,
                                    methods=["GET"],
                                    endpoint="get_image_by_path")