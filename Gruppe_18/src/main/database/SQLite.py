import sqlite3

connection = sqlite3.connect("YourGuide.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE tour (title TEXT, destination TEXT, duration REAL, cost REAL, "
               "pictureURL TEXT, language TEXT, MAX_travelers INTEGER, Booked INTEGER, Tour_ID TEXT)")

cursor.execute("CREATE TABLE Account (username TEXT, password TEXT, phonen TEXT, emailAdress TEXT, account_id Integer)")

cursor.execute("INSERT INTO tour (title, destination, duration, cost, pictureURL, "
               "language, MAX_travelers, Booked, Tour_ID) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               ("Tour Title", "Destination", 7.5, 500.0, "example.jpg", "English", 20, 5, "12345"))


connection.commit()

# Now, let's retrieve the inserted row as a dictionary
cursor.execute("SELECT * FROM tour WHERE Tour_ID = ?", ("12345",))
row = cursor.fetchone()

print(row)

# Close the cursor and the connection
cursor.close()
connection.close()




