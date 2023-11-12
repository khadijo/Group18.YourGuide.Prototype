from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from Gruppe_18.src.main.model.models import Account, Tour, tour_account_association
from Gruppe_18.src.main.repository.TourRepository import TourRepository


class AccountRepository(JSONRepository):
    def __init__(self, session):
        self.session = session
        self.tour_repo = TourRepository(session)

    def delete_account(self, user):
        account_to_delete = self.session.query(Account).filter_by(username=user.username).first()

        if account_to_delete:
            self.session.delete(account_to_delete)
            self.session.commit()
            return True

        return False

    def create_account(self, user):
        account = Account(usertype=user.usertype,
                          username=user.username,
                          password=user.password,
                          phoneNumber=user.phoneNumber,
                          emailAddress=user.emailAddress)

        self.session.add(account)
        self.session.commit()
        return account

    def account_register_to_tour(self, tour_id, user_id):
        existing_registration = self.session.query(tour_account_association).filter_by(
            tour_id=tour_id,
            account_id=user_id
        ).first()

        if existing_registration:
            print("Du er allerede registrert for denne turen.")
        else:
            tour = self.session.query(Tour).filter_by(id=tour_id).first()
            user = self.session.query(Account).filter_by(id=user_id).first()

            if tour is not None and user is not None:
                tour_account_assoc_obj = tour_account_association.insert().values(
                    tour_id=tour_id,
                    account_id=user_id
                )
                self.tour_repo.book_tour(tour)
                self.session.execute(tour_account_assoc_obj)
                self.session.commit()
                return True
            else:
                print("Tur eller bruker ble ikke funnet.")

    def account_cancel_tour(self, tour_id, user_id):
        tour = self.session.query(Tour).filter_by(id=tour_id).first()
        user = self.session.query(Account).filter_by(id=user_id).first()

        if tour is not None and user is not None:
            stmt = tour_account_association.delete().where(
                tour_account_association.c.tour_id == tour_id,
                tour_account_association.c.account_id == user_id
            )
            self.tour_repo.cancel_booked_tour(tour)
            self.session.execute(stmt)
            self.session.commit()
        else:
            print("Tur eller bruker ble ikke funnet.")

    def account_logged_in(self, status=False):
        logged_in = status
        return logged_in
