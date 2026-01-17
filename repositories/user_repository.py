from sqlalchemy.orm import Session
from models.user import UserSchema, User, SigninSchema


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
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

    def get_by_id(self, user_id : int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        return UserSchema.model_validate(user, from_attributes=True) 