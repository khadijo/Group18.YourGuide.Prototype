from Gruppe_18.test.stream_for_testing import *
from approvaltests import verify
from Gruppe_18.src.main.modell.Filter_tour import *


def test_if_reading_from_stream_is_as_expected():
    tours = read_tours_from_stream(stream)
    verify(tours)


def test_if_filter_tours_by_location_is_as_expected():
    filtered = filter_tour_by_location(read_tours_from_stream(stream), "London")
    verify(filtered)


def test_if_filter_tours_by_price_is_as_expected():
    filtered = filter_tour_by_price(read_tours_from_stream(stream), 150, 0)
    verify(filtered)
