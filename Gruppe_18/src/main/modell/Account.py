import json
import uuid


class Account:

    def __init__(self, username, password, phoneNumber, emailAddress):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress



    def get_id(self):
        return self.id
