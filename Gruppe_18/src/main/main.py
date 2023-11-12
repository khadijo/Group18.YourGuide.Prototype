import datetime

from Gruppe_18.src.main.model.models import Tour, Account
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository

session = get_session()

account_rep = AccountRepository(session)
tour_repository = TourRepository(session)
a = Account(
        "user",
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )
b = Account(
        "guide",
        "username",
        "password",
        12345678,
        "user_@gmail.com"
    )
g = Account(
        "guide",
        "ole",
        "ole123",
        12345678,
        "user_@gmail.com"
    )

Dubai = Tour("Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")

Lofoten = Tour("Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norway",
        3,
        3674,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")

Hawaii = Tour("Discover the Maui beach",
              datetime.date(2024, 7, 27),
              "Hawaii, Maui",
              8,
              5000,
              15,
              "English",
              "https://th.bing.com/th/id/OIP.Cr0sJQe1p8z1Kp5MmhyVgQHaFj?pid=ImgDet&rs=1")
Oslo = Tour(
    "Discover Oslo's Charm",
    datetime.date(2024, 8, 5),
    "Oslo, Norway",
    2,
    2500,
    10,
    "Norwegian",
    "https://th.bing.com/th/id/R.204fc958e56b888bc534eaeeb0d20e56?rik=%2fW47vQ1hMRsekA&pid=ImgRaw&r=0"
)

'''
tour_repository.create_tour(Dubai)
tour_repository.create_tour(Lofoten)
tour_repository.create_tour(Hawaii)
tour_repository.create_tour(Oslo)
'''


#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)


'''
tour_repository.delete_tour("50856c60-208a-4316-8025-1c8ba5ff47e4")
tour_repository.delete_tour("3bc8b319-400a-4b72-ba08-f82bdda82a24")

tour_repository.delete_tour("e7e9a7d6-21d4-4506-bf3c-fb88cedb8456")
tour_repository.delete_tour("39d9b3a0-18bf-44d0-b203-d66f58877d34")
tour_repository.delete_tour("be56083c-4c4a-4064-a55a-b9a8f50409da")
print(tour_repository.get_tour_description("67eed256-fef7-4314-8900-b543cf5a3ecd"))
account_rep.account_register_to_tour("3bc8b319-400a-4b72-ba08-f82bdda82a24", "2258e3d1-edc2-4740-9757-b5ee64721904")
account_rep.account_register_to_tour("50856c60-208a-4316-8025-1c8ba5ff47e4", "2258e3d1-edc2-4740-9757-b5ee64721904")
session.commit()

'''




