from typing import List

from repositories import UserRepository, ContactRepository
from models import UserSchema, SigninSchema
from jwt import encode
import os


class UserService:

    def __init__(self, user_repo: UserRepository, contact_repo: ContactRepository):
        self.user_repo = user_repo
        self.contact_repo = contact_repo


    def sign_up(self, user_data : UserSchema):
        self.user_repo.create(user_data)
    
    def sign_in(self, user_data : SigninSchema):
        user = self.user_repo.get_by_nickname_and_password(user_data)
        if user is None:
            raise ValueError("Неверный логин или пароль!")
        return self._generate_token(user.id, user.nickname)
    
    def _generate_token(self, user_id : int, nickname : str):
        payload = {
            "user_id" : str(user_id),
            "nickname" : nickname
        }
        return encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
    
    def get_user_by_id(self, user_id : int) -> UserSchema:
        return self.user_repo.get_by_id(user_id)
    
    def find_users(self, nickname: str) -> List [UserSchema]:
        return self.user_repo.find_by_nickname(nickname)
    
    def add_friend(self, user_id: int, contact_id: int):
        if user_id == contact_id:
            raise ValueError("Нельзя добавить в друзья самого себя!")
        self.contact_repo.create(user_id, contact_id)
    
    def delete_friend(self, user_id: int, contact_id: int):
        self.contact_repo.delete(user_id, contact_id)