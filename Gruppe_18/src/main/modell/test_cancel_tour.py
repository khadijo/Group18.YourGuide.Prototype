from pytest import *
import datetime
from Gruppe_18.src.main.modell.cancel_tour import TourAdmin


def test_cancel_tour_function():
    tour_admin = TourAdmin()
    assert  tour_admin.add_tour("Tour", "Anne", "DMGF18") == True
    assert tour_admin.cancel_tour("Tour_1", "Nicole", "DORMMB_18") == True
    #assert tour_admin.cancel_tour("Tour_1", "Nicole", "DORMMB_18") == False

def test_cancel_tour_within_24_hours():
    tour_admin = TourAdmin()
    tour_admin.add_tour("Tour 1", "Nicole", "DORMMB_18")
    result = tour_admin.cancel_tour("Tour 1", "Nicole", "DORMMB_18")
    assert result == True

def test_cancel_tour_after_24_hours():
    tour_admin = TourAdmin()
    tour_admin.add_tour("Tour 1", "Nicole", "DORMMB_18")
    # Simulate waiting for more than 24 hours
    tour_admin.tours[0].sign_up_time -= datetime.timedelta(days=2)
    result = tour_admin.cancel_tour("Tour 1", "Nicole", "DORMMB_18")
    assert result == False

def test_cancel_tour_not_found():
    tour_admin = TourAdmin()
    result = tour_admin.cancel_tour("Tour 1", "Nicole", "DORMMB_18")
    assert result == True  # The tour is not found, so it's considered successful
