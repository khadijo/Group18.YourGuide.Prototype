from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


class AccountRepository (JSONRepository):
    def save_to_json(self, account):
        filename = "account.json"
        super().save_to_json(account, filename)

