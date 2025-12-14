from flask import Flask, request
from models import get_db, Base, engine, User


app = Flask(__name__)
Base.metadata.create_all(bind=engine)
with get_db() as db:
    user = User(
        nickname = "guest",
        email = "exampe@mail.ru",
        password = "1234"
    )
    db.add(user)
    db.commit()

app.run()