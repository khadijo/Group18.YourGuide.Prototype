import json
import uuid


class Tour:
    # duration in hours
    # cost in dollars

    def __init__(self, title, destination, duration, cost, pictureURL, language="English", max_travelers=15):
        self.pictureURL = pictureURL
        self.language = language
        self.destination = destination
        self.title = title
        self.duration = duration
        self.cost = cost
        self.max_travelers = max_travelers
        self.booked = 0
        self.tour_Id = str(uuid.uuid4())


