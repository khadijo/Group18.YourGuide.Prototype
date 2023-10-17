from Gruppe_18_src.Account import Account
from Gruppe_18_src.Tour import Tour

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


tour.save_to_json("tour.json")
tour2.save_to_json("tour.json")
print(tour.check_if_tour_is_saved(2))