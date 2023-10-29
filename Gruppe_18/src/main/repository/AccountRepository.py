from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from Gruppe_18.src.main.model.models import Account, Tour, tour_account_association


class AccountRepository (JSONRepository):
    def __init__(self, session):
        self.session = session

    def delete_account(self, session, entity):
        # Søk etter kontoen som skal slettes
        account_to_delete = session.query(Account).filter_by(username=entity.username).first()

        if account_to_delete:
            # Hvis kontoen ble funnet, slett den fra databasen
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


    def account_register_to_tour(self, tour_id, user_id):
        tour = self.session.query(Tour).filter_by(tour_id=tour_id).first()
        user = self.session.query(Account).filter_by(account_id=user_id).first()

        if tour is not None and user is not None:
            tour_account_assoc_obj = tour_account_association.insert().values(
                    tour_id=tour_id,
                    account_id=user_id
                )
            self.session.execute(tour_account_assoc_obj)
            self.session.commit()

        else:
            print("Tur eller bruker ble ikke funnet.")


