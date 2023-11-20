import os
import datetime
import uuid

import pytest
from approvaltests import Options, verify
from approvaltests.scrubbers import scrub_all_guids
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import Account, db, Tour, tour_account_association
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
        str(uuid.uuid4()),
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


# Testing feature 1.1:
@pytest.mark.parametrize("attribute", ["id", "usertype", "username", "password", "phoneNumber", "emailAddress"])
def test_account_creation_and_saving(account_rep, account, sqlalchemy_session, attribute):
    account_rep.create_account(account)
    saved_account_from_db = account_rep.get_one_specific_account(account.id)

    assert getattr(saved_account_from_db, attribute) == getattr(account, attribute)


# Testing feature 1.1.2:
@pytest.mark.parametrize("missing_column", ["username", "password", "phoneNumber", "emailAddress"])
def test_account_missing_information_returns_false(account, account_rep, sqlalchemy_session, missing_column):
    setattr(account, missing_column, None)

    assert account_rep.create_account(account) is False


# Testing feature 1.3.2 and 1.2.1.4:
def test_account_can_be_deleted(account, account_rep):
    account_rep.create_account(account)
    assert account_rep.delete_account(account.id) is True


# Testing feature 1.2.1.1.1, 1.2.1.1.3 and 1.2.1.1.4
def test_account_can_update_their_information(account, account_rep):
    account_rep.create_account(account)
    new_username = "NewName"
    new_phoneNumber = "NewNumber"
    new_emailAddress = "New@gmail.com"
    account_rep.update_account(account.id, new_username, new_phoneNumber, new_emailAddress)
    updated_account = account_rep.get_one_specific_account(account.id)

    verify(repr(updated_account), options=approval_options)


# Testing feature 1.3.1.1:
def test_account_usertype_can_be_upgraded_to_guide(account, account_rep):
    account_rep.create_account(account)
    account_from_db = account_rep.get_one_specific_account(account.id)
    usertype_before_upgrade = account_from_db.usertype

    assert account_rep.upgrade_usertype_to_guide(account_from_db.id) is True

    account_from_db = account_rep.get_one_specific_account(account.id)

    usertype_after_upgrade = account_from_db.usertype
    assert usertype_before_upgrade == "user" and usertype_after_upgrade == "guide"


# Testing Feature 1.8:
def test_account_can_register_a_tour(account_rep, account, sqlalchemy_session, tour_1, tour_rep):
    account_rep.create_account(account)
    tour_rep.create_tour(tour_1)
    account_from_db = account_rep.get_one_specific_account(account.id)
    tour_from_db = tour_rep.get_specific_tour(tour_1.id)
    assert account_rep.account_register_to_tour(tour_from_db.id, account_from_db.id) is True
    registration_row = sqlalchemy_session.query(tour_account_association).filter_by(
        tour_id=tour_from_db.id,
        account_id=account_from_db.id
    ).first()
    assert registration_row is not None
