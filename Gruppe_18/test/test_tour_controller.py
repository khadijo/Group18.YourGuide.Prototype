import os

import pytest
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db

from Gruppe_18.src.main.app import load_user
from Gruppe_18.src.main.controller.TourController import TourController
from Gruppe_18.src.main.model.models import Account
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask_login import login_user, LoginManager


@pytest.fixture()
def user():
    return Account("2", "user", "user", "user", "12345678", "user@gmial.com")


@pytest.fixture()
def guide():
    return Account("3", "guide", "guide", "guide", "12345678", "user@gmial.com")


@pytest.fixture()
def admin():
    return Account("3", "admin", "admin", "admin", "12345678", "user@gmial.com")


@pytest.fixture()
def get_session():
    engine = create_engine("sqlite:///Test.db", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()


@pytest.fixture()
def acc_rep(get_session):
    return AccountRepository(get_session)


@pytest.fixture()
def sqlalchemy_session():
    module_path = os.path.dirname(os.path.abspath(__file__))
    database_name = os.path.join(module_path, "Test.db")
    engine = create_engine(f"sqlite:///{database_name}", echo=True)

    session = sessionmaker(bind=engine)()

    db.metadata.create_all(bind=engine)
    yield session

    session.close()
    db.metadata.drop_all(engine)


@pytest.fixture()
def tour_c(get_session):
    return TourController(TourRepository(get_session), get_session)


@pytest.fixture()
def app():
    app = Flask(__name__, template_folder='../src/main/templates')

    app.config['SECRET_KEY'] = 'testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager = LoginManager(app)

    return app


def test_if_user_gets_the_right_homepage(tour_c, user, sqlalchemy_session, app):
    with app.test_request_context():
        login_user(user, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage.html')


def test_if_guide_gets_the_right_homepage(tour_c, guide, sqlalchemy_session, app):
    with app.test_request_context():
        login_user(guide, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage_guide.html')


def test_if_admin_gets_the_right_homepage(tour_c, admin, sqlalchemy_session, app):
    with app.test_request_context():
        login_user(admin, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage_admin.html')
