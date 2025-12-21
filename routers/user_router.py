from flask import Blueprint
from controllers import UserController


class UserRouter:
    """ Роутер для работы с пользователями"""
    def __init__(self, user_controller: UserController):
        self.user_controller = user_controller
        self._router = Blueprint("users", __name__)
        self._router.add_url_rule("/signup/",
                                  view_func=self.user_controller.sign_up,
                                  methods=["POST"],
                                  endpoint="sign_up")
