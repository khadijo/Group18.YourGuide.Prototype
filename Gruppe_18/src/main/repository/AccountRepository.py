from sqlalchemy.exc import IntegrityError

from Gruppe_18.src.main.repository.JSONRepository import JSONRepository
from Gruppe_18.src.main.model.models import Account, Tour, tour_account_association, guide_tour_association
from Gruppe_18.src.main.repository.TourRepository import TourRepository


class AccountRepository(JSONRepository):
    def __init__(self, session):
        self.session = session
        self.tour_repo = TourRepository(session)

    def get_user_by_username(self, username):
        user = self.session.query(Account).filter_by(username=username).first()
        return user

    def get_one_specific_account(self, user_id):
        user = self.session.query(Account).filter_by(id=user_id).first()
        if user:
            return user
        else:
            print("The user was not found.")
            return False

    def get_all_users(self):
        all_users = self.session.query(Account).all()
        if all_users:
            return all_users
        else:
            print("There is no users registered")
            return False

    def delete_account(self, user_id):
        account_to_delete = self.get_one_specific_account(user_id)

        if account_to_delete:
            self.session.delete(account_to_delete)
            self.session.commit()
            return True
        else:
            print("Account to delete was not found")
            return False

    def upgrade_usertype_to_guide(self, user_id):
        user = self.get_one_specific_account(user_id)
        user.usertype = "guide"
        self.session.add(user)
        self.session.commit()
        return True

    def create_account(self, user):
        try:
            if any(value is None for value in
                   [user.username, user.password, user.phoneNumber, user.emailAddress]):
                return False
            else:
                account = Account(id=user.id,
                                  usertype=user.usertype,
                                  username=user.username,
                                  password=user.password,
                                  phoneNumber=user.phoneNumber,
                                  emailAddress=user.emailAddress)

                self.session.add(account)
                self.session.commit()
                return True
        except IntegrityError as e:
            self.session.rollback()
            raise e

    def update_account(self, user_id, new_username, new_telephone_number, new_email):
        user = self.get_one_specific_account(user_id)
        user.username = new_username
        user.phoneNumber = new_telephone_number
        user.emailAddress = new_email
        self.session.add(user)
        self.session.commit()
        return True

    def is_account_registered_to_tour(self, tour_id, user_id):
        existing_registration = self.session.query(tour_account_association).filter_by(
            tour_id=tour_id,
            account_id=user_id
        ).first()
        if existing_registration:
            return True
        else:
            return False

    def account_register_to_tour(self, tour_id, user_id):
        if self.is_account_registered_to_tour(tour_id, user_id):
            print("You are already registered for that tour.")
            return False
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
                print("Tour or user were not found.")
                return False

    def account_cancel_tour(self, tour_id, user_id):
        tour = self.tour_repo.get_specific_tour(tour_id)

        existing_registration = self.session.query(tour_account_association).filter_by(
            tour_id=tour_id,
            account_id=user_id
        ).first()

        if existing_registration is not None:
            stmt = tour_account_association.delete().where(
                tour_account_association.c.tour_id == tour_id,
                tour_account_association.c.account_id == user_id
            )
            self.tour_repo.cancel_booked_tour(tour)
            self.session.execute(stmt)
            self.session.commit()
            return True
        else:
            print("Tour or user is not found.")
            return False
