from dotenv import load_dotenv
from flask import Flask, g
from sqlalchemy.orm import Session
from flask_cors import CORS
from models import *
from models.base import SessionLocal
from repositories import *
from services import *
from controllers import *
from routers import *


app = Flask(__name__)
CORS(app)
load_dotenv(override=True)
Base.metadata.create_all(bind=engine)

@app.before_request
def before_request_db():
    # Создаем сессию для текущего запроса и сохраняем ее в g
    g.db = SessionLocal()


@app.teardown_appcontext
def teardown_request_db(exception=None):
    db: Session = g.pop('db', None)
    if db is not None:
        db.close()

user_repo = UserRepository()
marker_repo = MarkerRepository()
contact_repo = ContactRepository()
contact_group_repo = ContactGroupRepository()
user_service = UserService(user_repo, contact_repo, contact_group_repo)
marker_service = MarkerService(marker_repo)
user_controller = UserController(user_service)
marker_controller = MarkerController(marker_service)
user_router = UserRouter(user_controller)
marker_router = MarkerRouter(marker_controller)
app.register_blueprint(user_router._router, url_prefix="/users")
app.register_blueprint(marker_router._router, url_prefix="/markers")

app.run(host="0.0.0.0")