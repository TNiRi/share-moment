from sqlalchemy.orm import Session

from models.user import UserSchema, User


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