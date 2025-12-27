from services import UserService
from flask import request, jsonify
from models import UserSchema


class UserController:

    def __init__(self, user_service : UserService):
        self.user_service = user_service
    
    def sign_up(self):
        if request.is_json:
            body = request.get_json()
            user_data = UserSchema(**body)
            self.user_service.sign_up(user_data)
            return jsonify({"Message" : "Пользователь успешно зарегистрирован"}), 201
        return jsonify({"Message" : "Не хватает данных!"}), 400