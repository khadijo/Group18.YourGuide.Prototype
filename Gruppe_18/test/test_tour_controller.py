import datetime
import os
import uuid

import pytest
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db

from Gruppe_18.src.main.app import load_user
from Gruppe_18.src.main.controller.TourController import TourController
from Gruppe_18.src.main.model.models import Account, Tour
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
def tour_rep(get_session):
    return TourRepository(get_session)


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
def tour():
    return Tour('1', "Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


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
        assert tour_c.homepage_based_on_usertype() == render_template('homepage.html', tours=[])


def test_if_guide_gets_the_right_homepage(tour_c, guide, sqlalchemy_session, app):
    with app.test_request_context():
        login_user(guide, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage_guide.html', tours=[])


def test_if_admin_gets_the_right_homepage(tour_c, admin, sqlalchemy_session, app):
    with app.test_request_context():
        login_user(admin, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage_admin.html', tours=[])


def test_if_homepages_contains_all_available_tours(tour_c, user, sqlalchemy_session, app, tour_rep, tour):
    tour_rep.create_tour(tour)
    tours = [tour_rep.get_spesific_tour('1')]
    with app.test_request_context():
        login_user(user, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage.html', tours=tours)


def test_if_homepage_can_contain_spesific_tours(sqlalchemy_session, app, tour, user, tour_c, tour_rep):
    tour_rep.create_tour(tour)
    tours = [tour_rep.get_spesific_tour('1')]
    with app.test_request_context():
        login_user(user, remember=True)
        assert tour_c.homepage_based_on_usertype() == render_template('homepage.html', tours=tours)


def test_if_logget_in_user_can_see_booked_tours(sqlalchemy_session, app, tour_c, tour, user, tour_rep, acc_rep):
    tour_rep.create_tour(tour)
    acc_rep.create_account(user)
    acc_rep.account_register_to_tour(tour.id, user.id)
    user_tours = [tour_rep.get_spesific_tour('1')]
    user_comparison = sqlalchemy_session.query(Account).filter_by(id=user.id).first()
    with app.test_request_context():
        login_user(user, remember=True)
        assert tour_c.get_user_tours() == render_template('user_tours.html', user_tours=user_tours, user=user_comparison)


def test_if_not_logged_in_user_gets_returned_to_login_page_when_trying_to_see_booked_tours(app, sqlalchemy_session, tour_c):
    with app.test_request_context():
        assert tour_c.get_user_tours() == redirect(url_for('login'))


def test_if_guid_gets_sent_to_right_page_after_making_new_tour():
    pass

def test_if_guid_gets_sent_to_the_right_page_after_not_filling_out_all_tour_info():
    pass

