from Gruppe_18.src.main.modell.Account import Account
from Gruppe_18.src.main.modell.Tour import Tour
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from io import StringIO

account = Account("k", "kjwhd73eh", 48282234, "kariMarie@gmail.com")
account2 = Account("m", "89283447", 4839759793, "koiejewjre@gmail.com")

account.save_to_json()
account2.save_to_json()
# account.delete_account()

tour = Tour("Italy",
        4,
        255,
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg",
        "English",
        20)
tour2 = Tour("Italy",
        4,
        255,
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg",
        "English",
        20)


account_repository = AccountRepository()
account = Account("username", "password", 12345678, "user_@gmail.com")
account_repository.save_to_json(account)
io_stream = StringIO()

# Lagre tour-instansen til io_stream ved hjelp av save_to_stream
tour.save_to_stream(io_stream)

# Les innholdet i io_stream (kan være tomt hvis det er første gang)
saved_data = io_stream.getvalue()
print("Saved data:")
print(saved_data)
'''
tour_repo = TourRepository()
tour_repo.save_to_json(tour2)
'''
JSON_repo = JSONRepository()
print(JSON_repo.to_dict(account))




