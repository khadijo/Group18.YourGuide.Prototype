from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from Gruppe_18.src.main.model.models import Account


class AccountRepository(JSONRepository):

    def __init__(self, session):
        self.session = session

    def delete_account(self, session, entity):
        account_to_delete = session.query(Account).filter_by(username=entity.username).first()

        if account_to_delete:
            session.delete(account_to_delete)
            session.commit()
            return True

        return False

    '''

    def delete_account(self, entity, io_stream):
        try:
                io_stream.seek(0)
                filedata = json.load(io_stream)
        except json.JSONDecodeError:
            filedata = []

        index_to_delete = None
        for i, item in enumerate(filedata):
            if item["username"] == entity.username:
                index_to_delete = i
                break

        if index_to_delete is not None:
            del filedata[index_to_delete]

            io_stream.seek(0)
            io_stream.truncate()
            json.dump(filedata, io_stream, indent=4)
            return True

        return False
'''

    # needs to be updated after database is implemented

    def successful_registration(self, entity, io_stream):
        self.save_to_stream(entity, io_stream)
        return True

    def create_account(self, entity):
        account = Account(username=entity.username,
                          password=entity.password,
                          phoneNumber=entity.phoneNumber,
                          emailAddress=entity.emailAddress)

        self.session.add(account)
        self.session.commit()
        return account
