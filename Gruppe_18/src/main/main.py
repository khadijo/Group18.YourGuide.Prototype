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
tour = Tour("Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norwat",
        3,
        3674,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")



# new_tour = tour_repository.create_tour(tour)


#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)

tour_repository.delete_tour("25129e5f-3599-40be-be6a-07b87ba7762e")
tour_repository.delete_tour("009ea0dc-5fae-4538-8c6c-e439fa876e7c")
tour_repository.delete_tour("e9e2fa19-09c7-4fcb-8b86-bfbaefdf236b")
tour_repository.delete_tour("0c784c92-9e5b-42d3-91d2-21c21eafb6f6")
tour_repository.delete_tour("42018dd6-5b95-4852-9016-7f63e9856136")

# Create new tours
#new_tour = tour_repository.create_tour(tour)


session.commit()





