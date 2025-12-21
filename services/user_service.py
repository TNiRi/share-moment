from repositories import UserRepository
from models import UserSchema


class UserService:

    def __init__(self, user_repo : UserRepository):
        self.user_repo = user_repo

    def sign_up(self, user_data : UserSchema):
        self.user_repo.create(user_data)