from repositories import UserRepository
from models import UserSchema, SigninSchema
from jwt import encode
import os


class UserService:

    def __init__(self, user_repo : UserRepository):
        self.user_repo = user_repo

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