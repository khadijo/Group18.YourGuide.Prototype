import os
import uuid

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
    return Tour(str(uuid.uuid4()), "Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


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
def tour_3():
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

@pytest.fixture()
def another_tour():
    return Tour("Exploring Parisian Charm",
                datetime.date(2021, 5, 20),
                "Paris",
                3,
                200,
                1,
                "French",
                "https://www.example.com/paris.jpg")

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


def test_book_tour_with_available_space(sqlalchemy_session, tour_re, another_tour):
    tour = another_tour
    tour_re.create_tour(tour)
    assert tour_re.book_tour(tour) == True


def test_book_tour_when_fully_booked(sqlalchemy_session, tour, tour_re, another_tour):
    tour_re.create_tour(another_tour)
    tour_re.book_tour(another_tour)
    assert tour_re.book_tour(another_tour) == False
'''
def test_book_multiple_tours_with_available_space(tour, tour_rep):
    tour.max_travelers = 2
    assert tour_rep.book_tour(tour) == True
    assert tour_rep.book_tour(tour) == True

def test_book_more_tours_than_available_space(tour, tour_rep):
    tour.max_travelers = 2
    tour.booked = 2
    assert tour_rep.book_tour(tour) == False
'''
def test_tour_description_generation_is_as_expected(tour, tour_rep):
    given_description = tour_rep.get_tour_description(tour)
    expected_description = "This tour will take you to Italy for 4 hours, and is " \
               "offered in English"
    assert given_description == expected_description


def test_tour_description_generation_is_not_as_expected(tour, tour_rep):
    given_description = tour_rep.get_tour_description(tour)
    tour.destination = "Montenegro"
    expected_description = "This tour will take you to Montenegro for 4 hours, and is " \
               "offered in English"
    assert given_description != expected_description


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
