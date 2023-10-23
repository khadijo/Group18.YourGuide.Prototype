import sqlite3

connection = sqlite3.connect("YourGuide.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("CREATE TABLE tour (title TEXT, destination TEXT, duration REAL, cost REAL, "
               "pictureURL TEXT, language TEXT, MAX_travelers INTEGER, Booked INTEGER, Tour_ID TEXT PRIMARY KEY)")

cursor.execute("CREATE TABLE Account (username TEXT, password TEXT, phonen TEXT, "
               "emailAdress TEXT, account_id Integer PRIMARY KEY)")
