import os
from sqlalchemy import Table, Column, String, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
import uuid
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = sqlalchemy.orm.declarative_base()

module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "../YourGuide.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    engine = create_engine("sqlite:///YourGuide.db", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()

