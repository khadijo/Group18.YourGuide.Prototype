from Gruppe_18_src.Account import Account

account = Account("kari_768", "kjwhd73eh", 48282234, "kariMarie@gmail.com")

account.save_to_json()
account.delete_account("kari_768")
