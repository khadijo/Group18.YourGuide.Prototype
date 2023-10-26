import pytest
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids
from Gruppe_18.src.main.modell.models import Account
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from io import StringIO


approval_options = Options().with_scrubber(scrub_all_guids)


@pytest.fixture
def account():
    return Account(
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )


@pytest.fixture
def account_rep():
    account = AccountRepository()
    return account


def test_account_can_be_created_and_saved(account_rep, account):
    io_stream = StringIO()
    account_rep.save_to_stream(account, io_stream)
    saved_data = io_stream.getvalue()
    io_stream.seek(0)

    verify(saved_data, options=approval_options)


def test_account_had_an_successful_registration(account, account_rep):
    io_stream = StringIO()
    account_rep.save_to_stream(account, io_stream)
    assert account_rep.successful_registration(account, io_stream) == True


def test_user_can_delete_their_account(account, account_rep):
    io_stream = StringIO()
    account_rep.save_to_stream(account, io_stream)
    assert account_rep.delete_account(account, io_stream) == True


