import datetime
import os
import uuid

import flask
import pytest
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db

from Gruppe_18.src.main.app import load_user
from Gruppe_18.src.main.controller.TourController import TourController
from Gruppe_18.src.main.model.models import Account, Tour
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask_login import login_user, LoginManager, logout_user


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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return None

    @app.route('/new_tour', methods=['POST', 'GET'])
    def new_tour():
        return None

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


def test_if_not_logged_in_user_gets_returned_to_login_page_when_trying_to_see_booked_tours(app, sqlalchemy_session, tour_c, user):
    with app.test_request_context():
        login_user(user)
        logout_user()
        result = tour_c.get_user_tours()
        assert result.status_code == 302
        assert result.headers['location'] == '/login'
        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to see your registered tours.' in messages


def test_if_guide_gets_sent_to_right_template_when_wanting_to_create_tour(sqlalchemy_session, app, tour_c, guide):
    with app.test_request_context():
        login_user(guide)
        assert tour_c.make_new_tour() == render_template('new_tour.html')


def test_if_guide_gets_sent_to_right_template_after_filling_out_tour_creating_form_correctly(sqlalchemy_session, app, tour_c, guide, tour, tour_rep):
    with app.test_request_context(method='POST', data={
        'title': 'Welcome to Dubai',
        'date': '2020, 10, 15',
        'destination': 'Dubai',
        'duration': '4',
        'cost': 255,
        'max_travelers': 15,
        'language': 'English',
        'pictureURL': 'https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg',
    }):
        login_user(guide)
        assert tour_c.make_new_tour() == render_template('homepage_guide.html', tours=tour_rep.get_all_tours())


def test_if_guide_can_see_posted_tours_in_the_right_template(sqlalchemy_session, tour_c, app, guide, tour_rep):
    with app.test_request_context(method='POST', data={
        'title': 'Welcome to Dubai',
        'date': '2020, 10, 15',
        'destination': 'Dubai',
        'duration': '4',
        'cost': 255,
        'max_travelers': 15,
        'language': 'English',
        'pictureURL': 'https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg',
    }):
        login_user(guide)
        assert tour_c.make_new_tour() == render_template('homepage_guide.html', tours=tour_rep.get_all_tours())


def test_if_not_logged_in_user_gets_sent_to_login_when_wanting_too_see_posted_tours(app, sqlalchemy_session, tour_c, guide):
    with app.test_request_context():
        login_user(guide)
        logout_user()
        result = tour_c.show_guide_tour()
        assert result.status_code == 302
        assert result.headers['location'] == '/login'
        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to see your registered tours.' in messages


def test_if_guide_gets_sent_to_right_template_after_deleting_posted_tour(sqlalchemy_session, tour_c, app, guide, tour_rep):
    with app.test_request_context(method='POST', data={
        'title': 'Welcome to Dubai',
        'date': '2020, 10, 15',
        'destination': 'Dubai',
        'duration': '4',
        'cost': 255,
        'max_travelers': 15,
        'language': 'English',
        'pictureURL': 'https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg',
    }):
        login_user(guide)
        tour_c.make_new_tour()
        tour_id = tour_rep.get_all_tours()[0].id

        request_data = {
            'tour_id': tour_id
        }

        request_data.update(request.form)
        # Make the request with the updated data
        with app.test_client():
            assert tour_c.deleting_tour() == render_template('deleted_tour.html', tour=[])


def test_if_not_logged_in_user_gets_sent_to_login_after_wanting_to_deleted_tour(app, sqlalchemy_session, tour_c, guide):
    with app.test_request_context():
        login_user(guide)
        logout_user()
        result = tour_c.deleting_tour()
        assert result.status_code == 302
        assert result.headers['location'] == '/login'
        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to delete a tour.' in messages


def test_if_admin_gets_sent_to_the_right_page_with_right_info_when_wanting_to_see_all_tours(app, sqlalchemy_session, tour_c, tour, tour_rep, admin):
    tour_rep.create_tour(tour)
    tour = tour_rep.get_all_tours()
    with app.test_request_context():
        login_user(admin)
        assert tour_c.show_all_tours() == render_template('homepage_admin.html', tours=tour, show_all_tours=True)


def test_if_admin_gets_sent_to_the_right_page_when_wanting_to_see_hide_all_tours(app, sqlalchemy_session, tour_c, admin):
    with app.test_request_context():
        login_user(admin)
        assert tour_c.hide_all_tours() == render_template('homepage_admin.html', show_all_tours=False)


def test_if_admin_gets_sent_to_right_page_with_right_info_when_opening_dashboard(app, sqlalchemy_session, tour_c, admin):
    dictionary = {
            'num_users': 0,
            'num_tours': 0,
            'num_booked_tours': None,
            'num_guides': 0,
            'num_admin': 0,
            'num_regular_users': 0
        }
    with app.test_request_context():
        login_user(admin)
        assert tour_c.show_dashboard() == render_template('homepage_admin.html', **dictionary, show_dashboard=True)


def test_if_admin_gets_sent_to_right_page_wen_hiding_dashboard(app, sqlalchemy_session, tour_c, admin):
    with app.test_request_context():
        login_user(admin)
        assert tour_c.hide_dashboard() == render_template('homepage_admin.html', show_dashboard=False)
