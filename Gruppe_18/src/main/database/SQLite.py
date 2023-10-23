import sqlite3

connection = sqlite3.connect("YourGuide.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


cursor.execute("INSERT INTO tour (title, destination, duration, cost, pictureURL, "
               "language, MAX_travelers, Booked, Tour_ID) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               ("Tour Title", "Destination", 7.5, 500.0, "example.jpg", "English", 20, 5, "12345"))


connection.commit()

cursor.execute("SELECT * FROM tour WHERE Tour_ID = ?", ("12345",))
row = cursor.fetchone()

print(row['title'], row['destination'])

# Close the cursor and the connection
cursor.close()
connection.close()




