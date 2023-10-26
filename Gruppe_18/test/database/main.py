from Gruppe_18.test.database.database_handler import get_session
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository

session = get_session()

tour_rep = TourRepository(session)
account_rep = AccountRepository(session)

account_rep.delete_account("632f8390-29d4-49f2-8940-0e4599c4e44e")
tour_rep.delete_tour("68c09512-e670-4fbc-b40b-bb4b0e8816e0")