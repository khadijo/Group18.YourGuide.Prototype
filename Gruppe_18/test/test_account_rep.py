import os
import datetime
import uuid
from sqlite3 import IntegrityError

import pytest
from approvaltests import Options
from approvaltests.scrubbers import scrub_all_guids
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import Account, db, Tour
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository

approval_options = Options().with_scrubber(scrub_all_guids)


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


@pytest.fixture
def account():
    return Account(
        str(uuid.uuid4()),
        "user",
        "username",
        "password",
        "12345678",
        "user_@gmail.com"
    )


@pytest.fixture
def tour_1():
    return Tour(
        uuid.uuid4(),
        "Discover Oslo's Charm",
        datetime.date(2024, 8, 5),
        "Oslo, Norway",
        2,
        2500,
        10,
        "Norwegian",
        "https://www.example.com/oslo-city.jpg"
    )


@pytest.fixture
def account_rep(sqlalchemy_session):
    account = AccountRepository(sqlalchemy_session)
    return account


@pytest.fixture
def tour_rep(sqlalchemy_session):
    tour = TourRepository(sqlalchemy_session)
    return tour


@pytest.mark.parametrize("attribute", ["id", "usertype", "username", "password", "phoneNumber", "emailAddress"])
def test_account_creation_and_saving(account_rep, account, sqlalchemy_session, attribute):
    account_rep.create_account(account)
    saved_account_from_db = sqlalchemy_session.query(Account).filter_by(id=account.id).first()

    assert getattr(saved_account_from_db, attribute) == getattr(account, attribute)


def test_account_missing_id_raises_integrity_error(account, account_rep, sqlalchemy_session):
    account.id = None
    assert account_rep.create_account(account) is False


def test_account_missing_id_gives_failed_registration(account, account_rep, sqlalchemy_session):
    account.id = None
    with pytest.raises(IntegrityError):
        account_rep.create_account(account)
        saved_account_from_db = sqlalchemy_session.query(Account).filter_by(id=account.id).first()

        assert saved_account_from_db.id is None


@pytest.mark.parametrize("missing_column", ["usertype", "username", "password", "phoneNumber", "emailAddress"])
def test_account_missing_information_returns_false(account, account_rep, sqlalchemy_session, missing_column):
    setattr(account, missing_column, None)

    assert account_rep.create_account(account) is False


'''
def test_account_can_register_a_tour(account_rep, account, sqlalchemy_session, tour_1, tour_rep):
    account_rep.create_account(account)
    tour_rep.create_tour(tour_1)
    saved_account_from_db = sqlalchemy_session.query(Account).filter_by(username=account.username).first()
    saved_tour_from_db = sqlalchemy_session.query(Tour).filter_by(id=tour_1.id).first()
    assert account_rep.account_register_to_tour(saved_tour_from_db.id, saved_account_from_db.id) is True
'''

'''
def test_account_had_an_successful_registration(account, account_rep):
    io_stream = StringIO()
    account_rep.save_to_stream(account, io_stream)
    assert account_rep.successful_registration(account, io_stream) == True
'''

'''
def test_user_can_delete_their_account(account, account_rep, sqlalchemy_session):
    account_rep.create_account(account)
    saved_account_from_db = sqlalchemy_session.query(Account).filter_by(username=account.username).first()
    assert account_rep.delete_account(saved_account_from_db) == True
'''
