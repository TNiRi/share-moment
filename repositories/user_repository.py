from typing import List

from sqlalchemy.orm import Session
from models.user import UserInfoSchema, UserSchema, User, SigninSchema
from repositories.abstract_repository import AbstractRepository


class UserRepository(AbstractRepository):
    def create(self, user: UserSchema):
        user_model = User(
            nickname = user.nickname,
            email = user.email,
            password = user.password
        )
        self.db.add(user_model)
        self.db.commit()
    
    def get_by_nickname_and_password(self, sign_in : SigninSchema):
        user = self.db.query(User).filter(User.nickname == sign_in.nickname,
                                          User.password == sign_in.password).first()
        if user is None:
            return None
        return UserSchema.model_validate(user, from_attributes=True)

    def get_by_email_and_password(self, sign_in : SigninSchema):
        user = self.db.query(User).filter(User.email == sign_in.email,
                                          User.password == sign_in.password).first()
        if user is None:
            return None
        return UserSchema.model_validate(user, from_attributes=True)

    def get_by_id(self, user_id : int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        return UserSchema.model_validate(user, from_attributes=True)
    
    def find_by_nickname(self, nickname: str) -> List[UserInfoSchema]:
        results = self.db.query(User).filter(User.nickname.startswith(nickname)).all()
        if results is None:
            return None
        return [
            UserInfoSchema.model_validate(result, from_attributes=True)
            for result in results
        ]