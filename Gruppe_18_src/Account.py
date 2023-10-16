import json


class Account:

    def __init__(self, username, password, phoneNumber, emailAddress):
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress

    def delete_account(self):
        try:
            with open("account.json", "r") as json_file:
                filedata = json.load(json_file)
        except FileNotFoundError:
            filedata = []

        index_to_delete = None
        for i, item in enumerate(filedata):
            if item["username"] == self.username:
                index_to_delete = i
                break

        if index_to_delete is not None:
            del filedata[index_to_delete]

            with open("account.json", "w") as json_file:
                json.dump(filedata, json_file, indent=4)
                return True

        return False

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "emailAddress": self.emailAddress

        }

    def save_to_json(self):
        try:
            with open("account.json", "r") as json_file:
                filedata = json.load(json_file)
        except FileNotFoundError:
            filedata = []

        for item in filedata:
            if item["username"] == self.username:
                return

        data = self.to_dict()
        filedata.append(data)

        with open("account.json", "w") as json_file:
            json.dump(filedata, json_file, indent=4)

    def successful_registration(self):
        self.save_to_json()
        return True

