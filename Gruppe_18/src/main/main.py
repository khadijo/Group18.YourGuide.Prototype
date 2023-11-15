import datetime
import uuid

from Gruppe_18.src.main.model.models import Tour, Account
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository

session = get_session()

account_rep = AccountRepository(session)
tour_repository = TourRepository(session)
a = Account(str(uuid.uuid4()),
        "user",
        "user",
        "user",
        12345678,
        "user_@gmail.com"
    )
b = Account(
        str(uuid.uuid4()),
        "admin",
        "admin",
        "admin",
        12345678,
        "admin_@gmail.com"
    )
g = Account(
        str(uuid.uuid4()),
        "guide",
        "guide",
        "guide",
        12345678,
        "guide_@gmail.com"
    )

Dubai = Tour(
        str(uuid.uuid4()),
        "Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")

Lofoten = Tour(str(uuid.uuid4()),"Welcome to Lofoten",
        datetime.date(2024, 6, 25),
        "Lofoten, Norway",
        3,
        3674,
        20,"English",
        "https://www.thonhotels.no/siteassets/artikler/lofoten/nordlys-lofoten-1.jpg")

Hawaii = Tour(str(uuid.uuid4()), "Discover the Maui beach",
              datetime.date(2024, 7, 27),
              "Hawaii, Maui",
              8,
              5000,
              15,
              "English",
              "https://th.bing.com/th/id/OIP.Cr0sJQe1p8z1Kp5MmhyVgQHaFj?pid=ImgDet&rs=1")
Oslo = Tour(str(uuid.uuid4()),
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



account_rep.create_account(a)
account_rep.create_account(b)
account_rep.create_account(g)
''''''

#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)
'''

account_rep.create_account(a)
'''
tour_repository.delete_tour("b2ad50e1-ac86-4ecf-bf51-feeda5a910a3")
tour_repository.delete_tour("c1f09a81-118b-4ca1-8f47-b387125f853f")
tour_repository.delete_tour("7dcd6e7f-2ffe-4f23-855e-2990f23d4c3f")
tour_repository.delete_tour("d75eac3f-6651-4148-a862-90b2f0e964aa")
tour_repository.delete_tour("532341d5-450b-40c5-9d94-7070541278bb")
tour_repository.delete_tour("2df5b17e-1cae-4eb0-ab1e-b06254ecda0f")

print(tour_repository.get_tour_description("67eed256-fef7-4314-8900-b543cf5a3ecd"))
account_rep.account_register_to_tour("3bc8b319-400a-4b72-ba08-f82bdda82a24", "2258e3d1-edc2-4740-9757-b5ee64721904")
account_rep.account_register_to_tour("50856c60-208a-4316-8025-1c8ba5ff47e4", "2258e3d1-edc2-4740-9757-b5ee64721904")
session.commit()

'''




