import json


class Account:

    def __init__(self, username, password, phoneNumber, emailAddress):
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress

    def successful_registration(self):
        self.save_to_json()
        return True

    def delete_account(self, username):
        with open("account.json", "r") as json_file:
            data = json.load(json_file)
            if username in data:
                del data[username]

                with open("account.json_2", "w") as json_file:
                    json.dump(data, json_file, indent=4)
                return True
            else:
                return False

    def save_to_json(self):
        account_data = {
            "username": self.username,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "emailAddress": self.emailAddress

        }

        with open("account.json", "w") as json_file:
            json.dump(account_data, json_file, indent=4)
