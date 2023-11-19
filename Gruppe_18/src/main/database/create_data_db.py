import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Gruppe_18.src.main.database.app_config import db

module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "../YourGuide.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)

Session = sessionmaker(bind=engine)
db.metadata.create_all(bind=engine)

def get_session(path):
    engine = create_engine(f"sqlite:///{path}", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()
