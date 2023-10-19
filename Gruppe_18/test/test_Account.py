import pytest
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids
from Gruppe_18.src.main.modell.Account import Account
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

def test_account_can_be_created_and_saved(account):
    io_stream = StringIO()
    account.save_to_stream(io_stream)
    saved_data = io_stream.getvalue()
    io_stream.seek(0)

    verify(saved_data, options=approval_options)

def test_account_had_an_successful_registration(account):
    assert account.successful_registration() == True

def test_user_can_delete_their_account(account):
    assert account.delete_account() == True
