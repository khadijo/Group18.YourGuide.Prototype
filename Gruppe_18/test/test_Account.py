import pytest
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids
from Gruppe_18.test.database.database_handler import get_session
from Gruppe_18.src.main.model.models import Account
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository


approval_options = Options().with_scrubber(scrub_all_guids)


@pytest.fixture()
def session():
    return get_session()


@pytest.fixture
def account():
    return Account(
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )


@pytest.fixture
def account_rep(session):
    account = AccountRepository(session)
    return account


@pytest.mark.parametrize("input_account, expected_result", [
    (Account("username1", "password1", "12345678", "user1@gmail.com"), True),
    (Account("username2", "password2", "87654321", "user2@gmail.com"), True),
    (Account("username3", "password3", "11112222", "user3@gmail.com"), True),
])
def test_account_can_be_created_and_saved(input_account, expected_result, account_rep):
    created_account = account_rep.create_account(input_account)
    saved_account = account_rep.get_account_by_id(created_account.account_id)
    assert saved_account is not None
    assert account_rep.successful_registration(input_account, saved_account) == expected_result


def test_user_can_delete_their_account(account, account_rep):
    created_account = account_rep.create_account(account)
    assert account_rep.delete_account(created_account.account_id) == True

