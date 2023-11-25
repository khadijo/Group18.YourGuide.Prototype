import os
import datetime
import uuid
from sqlalchemy.exc import IntegrityError
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
def account_1():
    return Account(
        str(uuid.uuid4()),
        "user",
        "MartinB",
        "kunmartin55",
        "12345678",
        "MartinB_@gmail.com"
    )


@pytest.fixture
def account_2():
    return Account(
        str(uuid.uuid4()),
        "guide",
        "Ole1999",
        "Ole345",
        "87654321",
        "Ole1999_@yahoo.com"
    )


@pytest.fixture
def account_3():
    return Account(
        str(uuid.uuid4()),
        "Admin",
        "KariMarie",
        "Kari987",
        "8763548",
        "KariM_@hotmail.com"
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
def tour_2():
    return Tour(
        str(uuid.uuid4()),
        "Bergen Fjord Exploration",
        datetime.date(2024, 7, 10),
        "Bergen, Norway",
        4,
        4199,
        15,
        "English",
        "https://www.example.com/bergen-fjords.jpg"
    )


@pytest.fixture
def account_rep(sqlalchemy_session):
    account = AccountRepository(sqlalchemy_session)
    return account


@pytest.fixture
def tour_rep(sqlalchemy_session):
    tour = TourRepository(sqlalchemy_session)
    return tour


# Testing feature 1.15
def test_can_get_one_specific_user_based_on_id(account_1, account_rep):
    account_rep.create_account(account_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    verify(account_from_db, options=approval_options)


# Testing feature 1.15
def test_can_not_get_one_specific_user_that_does_not_exist_based_on_id(account_1, account_rep):
    account_rep.create_account(account_1)
    account_id_does_not_exist = str(uuid.uuid4())
    account_1.id = account_id_does_not_exist
    assert account_rep.get_one_specific_account(account_1.id) is False


def test_if_get_all_users_returns_all_existing_accounts(account_1, account_2, account_3, account_rep):
    account_rep.create_account(account_1)
    account_rep.create_account(account_2)
    account_rep.create_account(account_3)
    all_users = account_rep.get_all_users()
    verify(all_users, options=approval_options)


def test_if_there_is_none_users_get_all_users_returns_false(account_rep):
    assert account_rep.get_all_users() is False


# Testing feature 1.1:
@pytest.mark.parametrize("attribute", ["id", "usertype", "username", "password", "phoneNumber", "emailAddress"])
def test_account_creation_and_saving(account_rep, account_1, sqlalchemy_session, attribute):
    account_rep.create_account(account_1)
    saved_account_from_db = account_rep.get_one_specific_account(account_1.id)

    assert getattr(saved_account_from_db, attribute) == getattr(account_1, attribute)


# Testing feature 1.1.2:
@pytest.mark.parametrize("missing_column", ["username", "password", "phoneNumber", "emailAddress"])
def test_account_missing_information_returns_false(account_1, account_rep, sqlalchemy_session, missing_column):
    setattr(account_1, missing_column, None)

    assert account_rep.create_account(account_1) is False


def test_creating_two_accounts_with_the_same_id_returns_integrity_error(account_1, account_rep):
    account_rep.create_account(account_1)

    with pytest.raises(IntegrityError):
        account_rep.create_account(account_1)


# Testing feature 1.3.2 and 1.2.1.4:
def test_user_can_be_deleted(account_1, account_rep):
    account_rep.create_account(account_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    assert account_rep.delete_account(account_from_db.id) is True


def test_user_cannot_be_deleted_if_user_does_not_exist(account_1, account_rep):
    account_rep.create_account(account_1)
    account_id_does_not_exist = str(uuid.uuid4())
    account_1.id = account_id_does_not_exist
    assert account_rep.delete_account(account_1.id) is False


# Testing feature 1.2.1.1.1, 1.2.1.1.3 and 1.2.1.1.4
def test_user_can_update_their_information(account_1, account_rep):
    account_rep.create_account(account_1)
    new_username = "NewName"
    new_phoneNumber = "NewNumber"
    new_emailAddress = "New@gmail.com"
    account_rep.update_account(account_1.id, new_username, new_phoneNumber, new_emailAddress)
    updated_account = account_rep.get_one_specific_account(account_1.id)

    verify(updated_account, options=approval_options)


# Testing feature 1.3.1.1:
def test_user_usertype_can_be_upgraded_to_guide(account_1, account_rep):
    account_rep.create_account(account_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    usertype_before_upgrade = account_from_db.usertype

    assert account_rep.upgrade_usertype_to_guide(account_from_db.id) is True

    account_from_db = account_rep.get_one_specific_account(account_1.id)

    usertype_after_upgrade = account_from_db.usertype
    assert usertype_before_upgrade == "user" and usertype_after_upgrade == "guide"


# Testing feature 1.8:
def test_user_can_register_to_a_tour(account_rep, account_1, sqlalchemy_session, tour_1, tour_rep):
    account_rep.create_account(account_1)
    tour_rep.create_tour(tour_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    tour_from_db = tour_rep.get_specific_tour(tour_1.id)
    assert account_rep.account_register_to_tour(tour_from_db.id, account_from_db.id) is True
    registration_row = sqlalchemy_session.query(tour_account_association).filter_by(
        tour_id=tour_from_db.id,
        account_id=account_from_db.id
    ).first()
    assert registration_row is not None


def test_user_cannot_register_to_already_registered_tour(account_1, account_rep, sqlalchemy_session, tour_1, tour_rep):
    account_rep.create_account(account_1)
    tour_rep.create_tour(tour_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    tour_from_db = tour_rep.get_specific_tour(tour_1.id)
    account_rep.account_register_to_tour(tour_from_db.id, account_from_db.id)
    assert account_rep.account_register_to_tour(tour_from_db.id, account_from_db.id) is False


def test_user_cannot_register_to_tour_if_tourId_or_userId_does_not_exist(account_1, account_rep, tour_1, tour_rep,
                                                                         sqlalchemy_session):
    account_rep.create_account(account_1)
    tour_rep.create_tour(tour_1)
    none_existing_user_id = str(uuid.uuid4())
    none_existing_tour_id = str(uuid.uuid4())
    account_1.id = none_existing_user_id
    assert account_rep.account_register_to_tour(tour_1.id, account_1.id) is False
    tour_1.id = none_existing_tour_id
    assert account_rep.account_register_to_tour(tour_1.id, account_1.id) is False


# Testing feature 1.11.1, 1.11.2, 1.11.2.1
def test_user_can_cancel_a_tour_after_registration(account_rep, account_1, sqlalchemy_session, tour_1, tour_rep):
    account_rep.create_account(account_1)
    tour_rep.create_tour(tour_1)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    tour_from_db = tour_rep.get_specific_tour(tour_1.id)
    account_rep.account_register_to_tour(tour_from_db.id, account_from_db.id)
    assert account_rep.account_cancel_tour(tour_from_db.id, account_from_db.id) is True


def test_user_cannot_cancel_unregistered_tour(account_1, account_rep, sqlalchemy_session, tour_1, tour_2, tour_rep):
    account_rep.create_account(account_1)
    tour_rep.create_tour(tour_1)
    tour_rep.create_tour(tour_2)
    account_from_db = account_rep.get_one_specific_account(account_1.id)
    tour_1_from_db = tour_rep.get_specific_tour(tour_1.id)
    tour_2_from_db = tour_rep.get_specific_tour(tour_2.id)
    account_rep.account_register_to_tour(tour_1_from_db.id, account_from_db.id)
    assert account_rep.account_cancel_tour(tour_2_from_db.id, account_from_db.id) is False
