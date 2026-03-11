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
    
        self._router.add_url_rule("/signin/",
                                  view_func=self.user_controller.sign_in,
                                  methods=["POST"],
                                  endpoint="sign_in")
        
        self._router.add_url_rule("/me/",
                                  view_func=self.user_controller.me,
                                  methods=["GET"],
                                  endpoint="me")
        
        self._router.add_url_rule("/search/<string:nickname>/",
                                  view_func=self.user_controller.find_users,
                                  methods=["GET"],
                                  endpoint="search")
        
        self._router.add_url_rule("/friends/",
                                  view_func=self.user_controller.add_friend,
                                  methods=["POST"],
                                  endpoint="add_friend")

        self._router.add_url_rule("/friends/",
                                  view_func=self.user_controller.delete_friend,
                                  methods=["DELETE"],
                                  endpoint="delete_friend")
        
        self._router.add_url_rule("/contact_groups/",
                                  view_func=self.user_controller.create_contact_group,
                                  methods=["POST"],
                                  endpoint="create_contact_group")