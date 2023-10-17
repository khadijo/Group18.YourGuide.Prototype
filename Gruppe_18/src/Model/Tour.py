import json


class Tour:
    # duration in hours
    # cost in dollars
    # tour_counter:
    tour_counter = 1

    def __init__(self, destination, duration, cost, pictureURL, language="English", max_travelers=15):
        self.pictureURL = pictureURL
        self.language = language
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.max_travelers = max_travelers
        self.booked = 0
        self.tour_Id = Tour.tour_counter
        Tour.tour_counter += 1

    def book_tour(self):
        if not self.booked >= self.max_travelers:
            self.booked += 1
            return True
        else:
            return False

    def get_tour_description(self):
        return f"This tour will take you to {self.destination} for {self.duration} hours, and is " \
               f"offered in {self.language}"

    def to_dict(self):
        return {"tour_Id": self.tour_Id,
                "destination": self.destination,
                "cost": self.cost,
                "duration": self.duration,
                "pictureURL": self.pictureURL,
                "language": self.language,
                "max_travelers": self.max_travelers}

    def save_to_stream(self, io_stream):
        try:
            filedata = json.load(io_stream)
        except json.JSONDecodeError:
            filedata = []

        duplicate_found = False
        for item in filedata:
            if item == self.to_dict():
                duplicate_found = True
                break

        if not duplicate_found:
            data = self.to_dict()
            filedata.append(data)

        io_stream.truncate(0)
        io_stream.seek(0)
        json.dump(filedata, io_stream, indent=4)

    # er det riktig måte å overføre klasser på til JSON-format?
    def check_if_tour_is_saved(self):
        try:
            with open("../tour.json", "r") as json_file:
                filedata = json.load(json_file)
        except FileNotFoundError:
            filedata = []

        index_is_saved = None
        for i, item in enumerate(filedata):
            if item["tour_Id"] == self.tour_Id:
                index_is_saved = i
                break

        if index_is_saved is not None:
            return True

        else:
            return False

    '''
        def save_to_json(self, filename):
            try:
                with open(filename, "r") as json_file:
                    filedata = json.load(json_file)
            except FileNotFoundError:
                filedata = []
    
            duplicate_found = False
            for item in filedata:
                if item == self.to_dict():
                    duplicate_found = True
                    break
    
            if not duplicate_found:
                data = self.to_dict()
                filedata.append(data)
    
                with open(filename, "w") as json_file:
                    json.dump(filedata, json_file, indent=4)
        '''
