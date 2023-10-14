import json


class Tour:
    # duration in hours
    # cost in dollars
    def __init__(self, destination, duration, cost, pictureURL, language="English", max_travelers=15):
        self.pictureURL = pictureURL
        self.language = language
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.max_travelers = max_travelers
        self.booked = 0

    def book_tour(self):
        if not self.booked >= self.max_travelers:
            self.booked += 1
            return True
        else:
            return False


    def get_tour_description(self):
        return f"This tour will take you to {self.destination} for {self.duration}, and is " \
               f"offered in {self.language}"

    def save_to_json(self, filename):

        tour_data = {
            "destination": self.destination,
            "cost": self.cost,
            "duration": self.duration,
            "pictureURL": self.pictureURL,
            "language": self.language,
            "max_travelers": self.max_travelers
        }
        with open(filename, "w") as json_file:
            json.dump(tour_data, json_file, indent=4)


