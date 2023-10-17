from Gruppe_18.src.Model.Account import Account
from Gruppe_18.src.Model.Tour import Tour
from Gruppe_18.src.Repository.AccountRepository import AccountRepository

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
