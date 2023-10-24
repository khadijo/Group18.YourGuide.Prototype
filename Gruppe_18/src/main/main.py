import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Gruppe_18.src.main.modell.models import Tour, Account
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
        15,
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg",
        "English")


new_tour = tour_repository.create_tour(tour)


result = tour_repository.book_tour(new_tour)


session.commit()


print(f"Opprettet ny tur: {new_tour.title} ({new_tour.tour_id})")


