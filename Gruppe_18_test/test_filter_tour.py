import json

import pytest
from Gruppe_18_src.Tour import Tour
from Gruppe_18_src.Filter_tour import *


def test_all_tours_from_file_append_to_list():
    tours = read_tours_from_file_add_to_list("tour.json")
    with open("tour.json") as file:
        data1 = json.load(file)
    assert data1 == tours

def test_filter_tours_by_location_to_new_list():
    filter = filter_tour_by_location(read_tours_from_file_add_to_list("tour.json"), "Paris")
    assert filter == [{'destination': 'Paris', 'duration': 3, 'cost': 150, 'pictureURL': 'https://example.com/paris.jpg', 'language': 'French', 'max_travelers': 20, 'booked': 5}]

def test_filter_tours_by_price_to_new_lis():
    filer = filter_tour_by_price(read_tours_from_file_add_to_list("tour.json"), 100, 0)
    assert filer == [{'destination': 'Rome', 'duration': 2, 'cost': 100, 'pictureURL': 'https://example.com/rome.jpg', 'language': 'Italian', 'max_travelers': 15, 'booked': 3}]