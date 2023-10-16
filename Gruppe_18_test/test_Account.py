import pytest
from Gruppe_18_src.Account import Account


@pytest.fixture
def account():
    return Account(
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )


def test_account_can_be_created(account):
    assert account.username == "username"
    assert account.password == "password"
    assert account.phoneNumber == 12345678
    assert account.emailAddress == "user_@gmail.com"


def test_account_had_an_successful_registration(account):
    assert account.successful_registration() == True


def test_user_can_delete_their_account(account):
    assert account.delete_account() == True