import datetime

from Gruppe_18.src.main.model.models import Tour, Account
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.TourRepository import TourRepository

session = get_session()

tour_repository = TourRepository(session)
a = Account(
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )
tour = Tour("Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


new_tour = tour_repository.create_tour(tour)


#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)

# tour_repository.delete_tour("25129e5f-3599-40be-be6a-07b87ba7762e")
print(tour_repository.get_tour_description("67eed256-fef7-4314-8900-b543cf5a3ecd"))


session.commit()





