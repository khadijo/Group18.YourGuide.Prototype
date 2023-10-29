import pytest
from approvaltests import verify
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.test.database.database_handler import get_session
import datetime
from Gruppe_18.src.main.model.models import Tour


@pytest.fixture
def tour_re():
    return TourRepository(get_session())


@pytest.fixture
def tour():
    return Tour("Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norway",
        3,
        3674,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")


@pytest.fixture
def tour_2():
    return Tour(
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
def tour_3():
    return Tour(
    "Discover Oslo's Charm",
    datetime.date(2024, 8, 5),
    "Oslo, Norway",
    2,
    2500,
    10,
    "English",
    "https://www.example.com/oslo-city.jpg"
)


@pytest.fixture
def tour_4():
    return Tour(
    "Arctic Wonders in Tromsø",
    datetime.date(2024, 9, 15),
    "Tromsø, Norway",
    5,
    4899,
    12,
    "English",
    "https://www.example.com/tromso-arctic.jpg"
)


@pytest.fixture
def tour_5():
    return Tour("Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norway",
        3,
        200,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")


def test_if_reading_all_tours_from_database_is_as_expected(tour_re):
    all_tours = tour_re.get_all_tours()
    verify(all_tours)


def test_if_a_spesific_tour_can_be_returned_from_database(tour_re):
    spesific_tour = f"{tour_re.get_spesific_tour('5194d52d-3a5e-46d1-82fa-a56cf1360866')}"
    assert spesific_tour == ('(5194d52d-3a5e-46d1-82fa-a56cf1360866) Welcome to Lofoten Lofoten, Norway 3 3674 English 20'
                             ' https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg 0')


def test_if_filter_tours_by_destination_is_as_expected(tour_re):
    filtered_tours = tour_re.filter_tour_by_location("Lofoten, Norway")
    verify(filtered_tours)


def test_if_filter_tours_by_price_is_as_expected(tour_re):
    filtered_tours = tour_re.filter_tour_by_price(4000, 6000)
    verify(filtered_tours)


def test_if_filter_tours_by_price_and_destination_is_as_expected(tour_re):
    filtered_tours = tour_re.filter_tour_by_price_and_location("Lofoten, Norway", 500, 4000)
    verify(filtered_tours)
