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
    assert True


def test_filter_tours_by_price_to_new_lis():
    assert True