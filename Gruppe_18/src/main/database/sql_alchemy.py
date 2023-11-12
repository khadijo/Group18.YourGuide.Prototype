import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__, template_folder='../templates')
module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "../YourGuide.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'
db = SQLAlchemy(app)

Session = sessionmaker(bind=engine)


db.metadata.create_all(bind=engine)


def get_session():
    engine = create_engine("sqlite:///YourGuide.db", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()

