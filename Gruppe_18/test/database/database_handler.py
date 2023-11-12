import os
from sqlalchemy.orm import relationship
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db
from sqlalchemy.ext.declarative import declarative_base


module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "../Test.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)

db.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)


def get_session():
    engine = create_engine("sqlite:///Test.db", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()




