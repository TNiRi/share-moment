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