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
tour = Tour("noe",
        datetime.date(2020, 10, 15),
        "test",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")


#new_tour = tour_repository.create_tour(tour)


#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)

tour_repository.delete_tour("25129e5f-3599-40be-be6a-07b87ba7762e")



session.commit()





