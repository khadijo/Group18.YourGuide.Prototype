from io import StringIO

import pytest
from Gruppe_18.src.main.modell.Tour import Tour
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids


approval_options = Options().with_scrubber(scrub_all_guids)

@pytest.fixture
def tour():
    return Tour(
        "Italy",
        4,
        255,
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg",
        "English",
        20,
    )

# kan man forenkle assertene her med noen pytest-funksjoner?
def test_if_tour_is_created_and_saved(tour):
    io_stream = StringIO()
    tour.save_to_stream(io_stream)
    saved_data = io_stream.getvalue()
    io_stream.seek(0)
    verify(saved_data, options=approval_options)

def test_book_tour_with_available_space(tour):
    assert tour.book_tour() == True


def test_book_tour_when_fully_booked(tour):
    tour.max_travelers = 1
    tour.booked = 1
    # assert tour.book_tour() == True
    assert tour.book_tour() == False


def test_book_multiple_tours_with_available_space(tour):
    tour.max_travelers = 2
    assert tour.book_tour() == True
    assert tour.book_tour() == True


def test_book_more_tours_than_available_space(tour):
    tour.max_travelers = 2
    tour.booked = 2
    assert tour.book_tour() == False

#approvaltest


def test_tour_description_generation_is_as_expected(tour):
    given_description = tour.get_tour_description()
    expected_description = "This tour will take you to Italy for 4 hours, and is " \
               "offered in English"
    assert given_description == expected_description


def test_tour_description_generation_is_not_as_expected(tour):
    given_description = tour.get_tour_description()
    tour.destination = "Montenegro"
    expected_description = "This tour will take you to Montenegro for 4 hours, and is " \
               "offered in English"
    assert given_description != expected_description


def test_tour_information_is_saved_to_json(tour):
    tour.save_to_json("tour.json")
    assert tour.check_if_tour_is_saved() == True
