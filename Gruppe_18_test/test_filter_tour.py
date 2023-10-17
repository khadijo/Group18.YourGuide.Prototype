import pytest
from stream_for_testing import *
from approvaltests import verify
from Gruppe_18_src.Filter_tour import *


def test_all_tours_from_file_append_to_list():
    tours = read_tours_from_json(stream)
    verify(tours)


def test_filter_tours_by_location_as_expected():
    filtered = filter_tour_by_location(read_tours_from_json(stream), "London")
    verify(filtered)


def test_filter_tours_by_price_as_expected():
    filtered = filter_tour_by_price(read_tours_from_json(stream), 150, 0)
    verify(filtered)
