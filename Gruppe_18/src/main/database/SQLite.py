import sqlite3
import sys

connection = sqlite3.connect("YourGuide.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE tour (title String, destination String, duration Float, cost Float,"
               "pictureURL String, language String, MAX_travelers Integer, Booked Integer, Tour_ID String)")

cursor.execute("CREATE TABLE Account (username String, password String, phonen, emailAdress String, account_id Integer)")


