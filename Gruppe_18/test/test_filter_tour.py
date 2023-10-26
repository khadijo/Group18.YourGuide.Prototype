import pytest
from approvaltests import verify
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.test.database.database_handler import get_session


@pytest.fixture
def tour_re():
    return TourRepository(get_session())


def test_if_reading_all_tours_from_database_is_as_expected(tour_re):
    all_tours = tour_re.get_all_tours()
    verify(all_tours)


def test_if_a_spesific_tour_can_be_returned_from_database(tour_re):
    tour = tour_re.get_spesific_tour("id")
    assert tour == ""


def test_if_filter_tours_by_location_is_as_expected(tour_re):
    filtered_tours = tour_re.filter_tour_by_location("London")
    verify(filtered_tours)


def test_if_filter_tours_by_price_is_as_expected(tour_re):
    filtered_tours = tour_re.filter_tour_by_price(0, 150)
    verify(filtered_tours)