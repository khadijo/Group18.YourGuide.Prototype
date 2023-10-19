import sqlite3
import sys

connection = sqlite3.connect("YourGuide")
cursor = connection.cursor()

cursor.execute("CREATE TABLE tour ()")

self.pictureURL = pictureURL
        self.language = language
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.max_travelers = max_travelers
        self.booked = 0
        self.tour_Id = str(uuid.uuid4())