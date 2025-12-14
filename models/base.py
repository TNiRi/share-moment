from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

# Подключение к базе данных SQLite
#DATABASE_URL = os.getenv("DATABASE_URL", "")
DATABASE_URL = f"mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PWD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"

# engine = create_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        # db.execute(text("PRAGMA foreign_keys=ON"))
        yield db
    finally:
        db.close()
