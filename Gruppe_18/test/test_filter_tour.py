import pytest
from approvaltests import verify
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.database.sql_alchemy import get_session

@pytest.fixture
def tour_re():
    return TourRepository(get_session)


def test_if_reading_from_stream_is_as_expected():
    pass


def test_if_filter_tours_by_location_is_as_expected():
    pass


def test_if_filter_tours_by_price_is_as_expected():
    pass