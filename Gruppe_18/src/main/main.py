import datetime

from Gruppe_18.src.main.model.models import Tour, Account
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository


session = get_session()

tour_repository = TourRepository(session)
account_rep = AccountRepository(session)
a = Account(
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )
tour = Tour("Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norwat",
        3,
        3674,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")



new_tour = tour_repository.create_tour(tour)

account_rep.create_account(a)



# Create new tours
# new_tour = tour_repository.create_tour(tour)


session.commit()





