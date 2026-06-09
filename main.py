from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from models import *
from repositories import *
from services import *
from controllers import *
from routers import *


app = Flask(__name__)
CORS(app)
load_dotenv(override=True)
Base.metadata.create_all(bind=engine)
with get_db() as db:
    user_repo = UserRepository(db)
    marker_repo = MarkerRepository(db)
    contact_repo = ContactRepository(db)
    contact_group_repo = ContactGroupRepository(db)
    user_service = UserService(user_repo, contact_repo, contact_group_repo)
    marker_service = MarkerService(marker_repo)
    user_controller = UserController(user_service)
    marker_controller = MarkerController(marker_service)
    user_router = UserRouter(user_controller)
    marker_router = MarkerRouter(marker_controller)
    app.register_blueprint(user_router._router, url_prefix="/users")
    app.register_blueprint(marker_router._router, url_prefix="/markers")

app.run(host="0.0.0.0")