from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from Gruppe_18.src.main.model.models import Account


class AccountRepository(JSONRepository):
    def __init__(self, session):
        self.session = session

    def create_account(self, entity):
        account = Account(username=entity.username,
                          password=entity.password,
                          phoneNumber=entity.phoneNumber,
                          emailAddress=entity.emailAddress)

        self.session.add(account)
        self.session.commit()
        return account

    def delete_account(self, account_id):
        account = self.session.query(Account).filter_by(account_id=account_id).first()

        if account is not None:
            self.session.delete(account)
            self.session.commit()
            return True
        else:
            return False

    def successful_registration(self, input_account, saved_account):
        if (input_account.username == saved_account.username and
                input_account.password == saved_account.password and
                input_account.phoneNumber == saved_account.phoneNumber and
                input_account.emailAddress == saved_account.emailAddress):
            return True

        else:
            return False


'''
    def successful_registration(self, entity):
        self.create_account(entity)
        return True'''
