import json

import pytest
from Gruppe_18_src.Tour import Tour
from Gruppe_18_src.Filter_tour import *


def test_all_tours_from_file_append_to_list():
    tours = read_tours_from_file_add_to_list("tour.json")
    with open("tour.json") as file:
        data1 = json.load(file)
    assert data1 == tours


def test_filter_tours_by_location_as_expected():
    test = []
    filter = filter_tour_by_location(read_tours_from_file_add_to_list("tour.json"), "Paris")
    with open("tour.json") as file:
        data1 = json.load(file)
        for data in data1:
            if data['destination'] == 'Paris':
                test.append(data)
    assert filter == test


def test_filter_tours_by_price_as_expected():
    test = []
    filter = filter_tour_by_price(read_tours_from_file_add_to_list("tour.json"), 100, 0)
    with open("tour.json") as file:
        data1 = json.load(file)
        for data in data1:
            if 0 <= data['cost'] <= 100:
                test.append(data)
    assert filter == test