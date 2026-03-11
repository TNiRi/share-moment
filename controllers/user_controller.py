from models.contact_group import ContactGroupCreateSchema
from services import UserService
from flask import request, jsonify
from models import UserSchema, SigninSchema
from sqlalchemy.exc import IntegrityError

from utils.auth import authorized


class UserController:

    def __init__(self, user_service : UserService):
        self.user_service = user_service
    
    def sign_up(self):
        try:
            if request.is_json:
                body = request.get_json()
                user_data = UserSchema(**body)
                self.user_service.sign_up(user_data)
                return jsonify({"Message" : "Пользователь успешно зарегистрирован"}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except IntegrityError:
            return jsonify({"Message" : "Такой пользователь уже существует!"}), 409
    
    def sign_in(self):
        try:
            if request.is_json:
                body = request.get_json()
                user_data = SigninSchema(**body)
                token = self.user_service.sign_in(user_data)
                return jsonify({"token" : token}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except ValueError as e:
            return jsonify({"Message" : str(e)}), 403
    
    @authorized
    def me(self, user_id : int):
        user = self.user_service.get_user_by_id(user_id)
        return jsonify(user.model_dump()), 200
    
    @authorized
    def find_users(self, user_id: int, nickname: str):
        users = self.user_service.find_users(nickname)
        return jsonify([user.model_dump() for user in users]), 200
    
    @authorized
    def add_friend(self, user_id: int):
        try:
            if request.is_json:
                body = request.get_json()
                contact_id = body.get("contact_id")
                self.user_service.add_friend(user_id, contact_id)
                return jsonify({"Message" : "друг успешно добавлен"}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except ValueError as e:
            return jsonify({"Message" : str(e)}), 403
    
    @authorized
    def delete_friend(self, user_id: int):
        try:
            if request.is_json:
                body = request.get_json()
                contact_id = body.get("contact_id")
                self.user_service.delete_friend(user_id, contact_id)
                return jsonify({"Message" : "друг успешно удален"}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except ValueError as e:
            return jsonify({"Message" : str(e)}), 403
        
    @authorized
    def create_contact_group(self, user_id: int):
        try:
            if request.is_json:
                body = request.get_json()
                contact_group = ContactGroupCreateSchema(**body, user_id = user_id)
                self.user_service.create_contact_group(contact_group)
                return jsonify({"Message" : "Группа контактов успешно создана"}), 201
            return jsonify({"Message" : "Не хватает данных!"}), 400
        except ValueError as e:
            return jsonify({"Message" : str(e)}), 400