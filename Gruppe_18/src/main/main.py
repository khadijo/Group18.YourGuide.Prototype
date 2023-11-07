import datetime

from Gruppe_18.src.main.model.models import Tour, Account
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
session = get_session()

account_rep = AccountRepository(session)
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


#new_tour = tour_repository.create_tour(tour)


#result = tour_repository.book_tour(new_tour)
#result1 = tour_repository.book_tour(new_tour)
#account_rep.create_account(a)
tour_repository.delete_tour("0ddff35a-e91f-4dae-8555-8a1a256e8f22")
tour_repository.delete_tour("b7ec9785-78e0-4bbd-af2c-181f1d9463af")
tour_repository.delete_tour("f84ea9e9-df02-465d-9814-a95cb8a22cfb")
tour_repository.delete_tour("39d9b3a0-18bf-44d0-b203-d66f58877d34")
tour_repository.delete_tour("be56083c-4c4a-4064-a55a-b9a8f50409da")
print(tour_repository.get_tour_description("67eed256-fef7-4314-8900-b543cf5a3ecd"))
account_rep.account_register_to_tour("3bc8b319-400a-4b72-ba08-f82bdda82a24", "2258e3d1-edc2-4740-9757-b5ee64721904")
account_rep.account_register_to_tour("50856c60-208a-4316-8025-1c8ba5ff47e4", "2258e3d1-edc2-4740-9757-b5ee64721904")
session.commit()





