import os

from approvaltests.scrubbers import scrub_all_guids
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db

import pytest
from approvaltests import verify, Options

from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.test.database.database_handler import get_session
import datetime
from Gruppe_18.src.main.model.models import Tour


@pytest.fixture
def tour_re():
    return TourRepository(get_session())


@pytest.fixture()
def tour():
    return Tour("Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


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
    "Norwegian",
    "https://www.example.com/oslo-city.jpg"
)

@pytest.fixture()
def tour_4():
    return Tour(
    "Discover Oslo's Charm",
    datetime.date(2024, 8, 5),
    "Oslo, Norway",
    2,
    2500,
    0,
    "Norwegian",
    "https://www.example.com/oslo-city.jpg"
)


@pytest.fixture()
def sqlalchemy_session(tour_re, tour, tour_2, tour_3):
    module_path = os.path.dirname(os.path.abspath(__file__))
    database_name = os.path.join(module_path, "Test.db")
    engine = create_engine(f"sqlite:///{database_name}", echo=True)

    session = sessionmaker(bind=engine)()

    db.metadata.create_all(bind=engine)

    tour_re.create_tour(tour)
    tour_re.create_tour(tour_2)
    tour_re.create_tour(tour_3)
    yield session

    session.close()
    db.metadata.drop_all(engine)


approval_options = Options().with_scrubber(scrub_all_guids)


def test_if_tour_is_created_saved_and_retrived(tour_re, sqlalchemy_session):
    saved_data = tour_re.get_all_tours()
    verify(saved_data, options=approval_options)


def test_if_booked_goes_up_by_one_after_registration_to_a_not_fully_booked_tour(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    tour = data[0]
    tour_re.book_tour(tour)
    assert tour.booked == 1


def test_if_booking_to_fully_booked_tour_is_not_possible(tour_re, sqlalchemy_session, tour_4):
    tour_re.create_tour(tour_4)
    data = tour_re.get_all_tours()
    tour = data[len(data)-1]
    assert tour_re.book_tour(tour) == False


def test_if_booked_goes_down_by_one_after_tour_cancelletion(tour_re, sqlalchemy_session):
    tours = tour_re.get_all_tours()
    tour = tours[0]
    tour_re.cancel_booked_tour(tour)
    assert tour.booked == -1


def test_if_description_for_a_tour_is_correctly_returnet(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    tour = data[0]
    assert tour_re.get_tour_description(tour.id) == "This tour will take you to Dubai for 4 " \
                                                    "hours, and is offered in English"


def test_if_tour_can_be_deleted_from_database(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    assert len(data) == 3
    tour_re.delete_tour(data[0].id)
    saved_data = tour_re.get_all_tours()
    assert len(saved_data) == 2


def test_if_filtering_based_on_nothing_returns_all_tours(sqlalchemy_session, tour_re):
    filter_tour = tour_re.filter_combinations('', '', '', '')

    verify(filter_tour, options=approval_options)


def test_if_filtering_based_on_only_destination_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("Dubai", "", "", "")
    verify(filter_tour, options=approval_options)


def test_if_filtering_based_on_only_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "500", "3000", "")
    verify(filter_tour, options=approval_options)


def test_if_filtering_only_on_max_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "", "3000", "")
    verify(filter_tour, options=approval_options)


def test_if_filtering_only_on_min_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "500", "", "")
    verify(filter_tour, options=approval_options)


def test_if_filtering_based_on_only_language_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "", "", "English")
    verify(filter_tour, options=approval_options)


def test_if_filtering_based_on_destination_price_and_language_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("Dubai", "0", "600", "English")
    verify(filter_tour, options=approval_options)


def test_if_searching_tours_by_title_gives_is_as_expected(tour_re, sqlalchemy_session):
    searched_tour = tour_re.search_tour("dubai")
    verify(searched_tour, options=approval_options)
