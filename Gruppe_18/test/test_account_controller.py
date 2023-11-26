import datetime
import flask
from Gruppe_18.src.main.controller.AccountController import AccountController
import os
from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db
from Gruppe_18.src.main.model.models import Account, Tour
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask_login import login_user, LoginManager, logout_user
import pytest
from Gruppe_18.src.main.repository.TourRepository import TourRepository


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
def user():
    return Account("2", "user", "user", "user", "12345678", "user@gmial.com")


@pytest.fixture()
def guide():
    return Account("3", "guide", "guide", "guide", "12345678", "user@gmial.com")


@pytest.fixture()
def admin():
    return Account("1", "admin", "admin", "admin", "12345678", "user@gmial.com")


@pytest.fixture()
def account_repository(sqlalchemy_session):
    return AccountRepository(sqlalchemy_session)


@pytest.fixture()
def tour_repository(sqlalchemy_session):
    return TourRepository(sqlalchemy_session)


@pytest.fixture()
def account_controller(sqlalchemy_session, account_repository):
    return AccountController(account_repository, sqlalchemy_session)


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

    @app.route('/account_reg', methods=['POST', 'GET'])
    def account_reg():
        return None

    @app.route('/home', methods=['POST', 'GET'])
    def home():
        return None

    @app.route('/user_tours')
    def user_tours():
        return None

    @app.route('/cancel_tour', methods=['POST'])
    def cancel_tour():
        return None

    return app


@pytest.fixture()
def tour():
    return Tour('1', "Welcome to Dubai",
                datetime.datetime(2020, 10, 15),
                "Dubai",
                4,
                255,
                15, "English",
                "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


# Testing feature 1.1.1, 1.1.2, 1.1.3 and nonfunctional feature 1.31
def test_if_user_can_register_if_all_required_fields_is_filled(app, user, account_controller, account_repository):
    with app.test_request_context(method='POST', data={
        'username': 'valid_username',
        'password': 'valid_password',
        'phoneNumber': '12345678',
        'emailAddress': 'user@gmail.com'
    }):
        login_user(user, remember=True)
        result = account_controller.account_registration()
        assert result == render_template('index.html')
        assert account_repository.get_user_by_username('valid_username') is not None


# Testing feature 1.1.2
def test_user_cannot_register_if_one_field_is_missing_data(app, user, account_controller, account_repository):
    with app.test_request_context(method='POST', data={
        'username': '',
        'password': 'valid_password',
        'phoneNumber': '12345678',
        'emailAddress': 'user@gmail.com'
    }):
        login_user(user, remember=True)
        result = account_controller.account_registration()
        assert result == render_template('User_register.html')
        assert account_repository.get_user_by_username('') is None


# Testing feature 1.1.6
def test_if_user_can_login_with_saved_account_after_registration(app, user, account_controller, account_repository):
    account_repository.create_account(user)
    with app.test_request_context(method='POST', data={
        'username': f'{user.username}',
        'password': f'{user.password}',
    }):
        login_user(user, remember=True)
        result = account_controller.account_login()
        assert result.status_code == 302
        assert result.headers['location'] == '/home'


# Testing feature 1.1.5 and nonfunctional feature 1.31
def test_if_user_cannot_login_without_completed_registration_or_saved_account(app, user, account_controller,
                                                                              account_repository):
    with app.test_request_context(method='POST', data={
        'username': 'nonexistent_user',
        'password': 'some_password',
    }):
        login_user(user, remember=True)
        result = account_controller.account_login()
        assert result == render_template('index.html')

        messages = list(flask.get_flashed_messages())
        assert 'Wrong username or password' in messages


# Testing feature 1.9.1.
def test_if_user_can_register_a_tour(app, user, tour, account_controller, account_repository, tour_repository):
    account_repository.create_account(user)
    tour_repository.create_tour(tour)

    with app.test_request_context(method='POST', data={
        'tour_id': f'{tour.id}',
        'user_id': f'{user.id}'
    }):
        login_user(user, remember=True)
        result = account_controller.tour_registration()
        assert result.status_code == 302
        assert result.headers['location'] == '/user_tours'
        assert account_repository.is_account_registered_to_tour(tour.id, user.id) is True


# Testing nonfunctional feature 1.26.1
def test_tour_registration_with_unauthenticated_user_sends_user_to_login_with_flash_message(app, user,
                                                                                             account_controller
                                                                                             , tour):
    with app.test_request_context(method='POST', data={'tour_id': f'{tour.id}'}):
        login_user(user)
        logout_user()
        result = account_controller.tour_registration()

        assert result.status_code == 302
        assert result.headers['location'] == '/login'

        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to register for a tour' in messages


# Testing feature 1.12.1, 1.12.2 and 1.12.2.1
def test_user_can_cancel_a_tour_registration(app, user, tour, account_controller, account_repository
                                             , tour_repository):
    account_repository.create_account(user)
    tour_repository.create_tour(tour)
    user_from_db = account_repository.get_one_specific_account(user.id)
    tour_from_db = tour_repository.get_specific_tour(tour.id)
    with app.test_request_context(method='POST', data={
        'tour_id': f'{tour_from_db.id}',
        'user_id': f'{user_from_db.id}'
    }):
        login_user(user, remember=True)
        result = account_controller.account_cancel_tour()
        assert result == render_template('canceled_tour.html', tour=tour)
        assert account_repository.is_account_registered_to_tour(tour.id, user.id) is False


# Testing nonfunctional feature 1.26.1
def test_unauthenticated_user_try_to_cancel_a_tour_gets_sent_to_login_with_flash_message(app, user, tour,                                                                                    account_controller):
    with app.test_request_context(method='POST', data={'tour_id': f'{tour.id}',
                                                       'user_id': f'{user.id}'}):
        login_user(user)
        logout_user()
        result = account_controller.account_cancel_tour()

        assert result.status_code == 302
        assert result.headers['location'] == '/login'

        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to cancel a tour.' in messages


# Testing feature 1.2.1, 1.2.1.4
def test_authenticated_user_can_delete_their_own_account(app, user, account_controller, account_repository):
    account_repository.create_account(user)
    with app.test_request_context(method='POST', data={'account_id': f'{user.id}'}):
        login_user(user, remember=True)
        result = account_controller.delete_my_account()
        assert result == render_template('User_register.html')
        assert account_repository.get_one_specific_account(user.id) is False


# Testing feature 1.3.2
def test_authenticated_admin_can_delete_users(app, user, admin, account_controller, account_repository):
    account_repository.create_account(user)
    account_repository.create_account(admin)
    with app.test_request_context(method='POST', data={'user_id': f'{user.id}'}):
        login_user(admin, remember=True)
        result = account_controller.deleting_account()
        assert result == render_template('deleted_account.html', user=user)
        assert account_repository.get_one_specific_account(user.id) is False


# Testing nonfunctional 1.26.1
def test_unauthenticated_admin_cannot_delete_users_and_gets_sent_to_login_and_gets_flashed_message(app, user, admin,
                                                                                               account_controller):
    with app.test_request_context(method='POST', data={'user_id': f'{user.id}'}):
        login_user(admin)
        logout_user()
        result = account_controller.deleting_account()
        assert result.status_code == 302
        assert result.headers['location'] == '/login'

        messages = list(flask.get_flashed_messages())
        assert 'You must be logged in to delete the account.' in messages


# Testing feature 1.2.1, 1.2.1.1, 1.2.1.1.1, 1.2.1.1.3, 1.2.1.1.4
def test_authenticated_user_can_update_their_profile_information(app, user, account_controller, account_repository):
    account_repository.create_account(user)
    with app.test_request_context(method='POST', data={'username': f'{user.username}',
                                                       'phoneNumber': f'{user.phoneNumber}',
                                                       'email': f'{user.emailAddress}'}):
        login_user(user, remember=True)
        result = account_controller.update_user_information()
        assert result.status_code == 302
        assert result.headers['location'] == '/home'
        assert account_repository.get_user_by_username(user.username) is not None


# Testing feature 1.3.1, 1.3.1.1
def test_authenticated_admin_can_update_user_usertype_to_guide(app, admin, user, account_controller,
                                                               account_repository):
    account_repository.create_account(admin)
    account_repository.create_account(user)
    user_from_db = account_repository.get_one_specific_account(user.id)
    with app.test_request_context(method='POST', data={'user_id': f'{user.id}'}):
        login_user(admin, remember=True)
        result = account_controller.update_usertype()
        assert result.status_code == 302
        assert result.headers['location'] == '/home'
        assert user_from_db.usertype == 'guide'


# Testing feature 1.3.5
def test_authenticated_admin_can_view_all_users(app, admin, user, guide, account_controller, account_repository):
    account_repository.create_account(admin)
    account_repository.create_account(user)
    account_repository.create_account(guide)
    with app.test_request_context():
        login_user(admin, remember=True)
        result = account_controller.admin_get_all_users()
        users = account_repository.get_all_users()
        assert result == render_template('homepage_admin.html', users=users, show_all_users=True)
        assert users is not None


# Testing feature 1.3.7
def test_authenticated_admin_can_hide_all_users(app, admin, account_controller, account_repository):
    with app.test_request_context():
        login_user(admin, remember=True)
        result = account_controller.admin_hide_all_user()
        assert result == render_template('homepage_admin.html', show_all_users=False)


# Testing feature 1.2 and nonfunctional feature 1.31
def test_authenticated_user_can_view_their_profile_with_their_correct_user_information(app, user,
                                                                                       account_controller,
                                                                                       account_repository):
    account_repository.create_account(user)
    with app.test_request_context():
        login_user(user, remember=True)
        result = account_controller.show_profile()
        user_data = account_repository.get_one_specific_account(user.id)
        assert result == render_template('profile.html', user_data=user_data)
        assert user_data is not None
