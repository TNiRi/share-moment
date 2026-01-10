from flask import Flask, request
from models import get_db, Base, engine, User
from repositories import UserRepository
from services import UserService
from controllers import UserController
from routers import UserRouter
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(override=True)
Base.metadata.create_all(bind=engine)
with get_db() as db:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    user_controller = UserController(user_service)
    user_router = UserRouter(user_controller)
    app.register_blueprint(user_router._router, url_prefix="/users")

app.run()