import pytest
from Gruppe_18_src.create_tour import Tour


def test_if_tour_is_created():
    tour = Tour("italia")
    assert tour.destination == "italia"