import os
import random
import subprocess
import uuid

from locust import HttpUser, task, between

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db
from Gruppe_18.src.main.model.models import Account, tour_account_association
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository
# testing nonfunctional feature 1.32, but with less users since this is only a prototype
# with the api's that we expect would get the most requests at once.


guide = Account(str(uuid.uuid4()), "guide", "guide", "guide", "12345678", "guide@gmial.com")
admin = Account(str(uuid.uuid4()), "admin", "admin", "admin", "12345678", "guide@gmial.com")
user = Account(str(uuid.uuid4()), "user", "user", "user", "12345678", "guide@gmial.com")

module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "Test.db")
engine = create_engine(f"sqlite:///{database_name}",
                       echo=True, connect_args={'check_same_thread': False}, pool_pre_ping=True)

session = sessionmaker(bind=engine)()

Acc_Rep = AccountRepository(session)
tour_rep = TourRepository(session)


class MyUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:5000"

    @task
    def access_start(self):
        self.client.get("/")

    @task
    def access_user_registration(self):
        self.client.post("/account_reg", data={'username': str(uuid.uuid4()),
                                               'password': str(uuid.uuid4()),
                                               'phoneNumber': str(uuid.uuid4()),
                                               'emailAddress': str(uuid.uuid4())})

    @task
    def access_user_login(self):
        response_login = self.client.post("/login", data={'username': 'user', 'password': 'user'})

        if response_login.status_code == 200:
            self.client.get("/home")

            self.client.post("/home/filter", data={'destination': 'some_destination',
                                                   'max_price': 'some_max_price',
                                                   'min_price': 'some_min_price',
                                                   'language': 'some_language'})

            self.client.get("/search?q=dubai")

            self.client.get("/profile")

    @task
    def access_guider(self):
        response_login = self.client.post("/login", data={'username': 'guide', 'password': 'guide'})
        if response_login.status_code == 200:
            self.client.post('/new_tour', data={
                'title': "Welcome to tour!",
                'date': "2023, 11, 17",
                'destination': "country, city",
                'duration': 5,
                'cost': 1600,
                'max_travelers': 5,
                'language': "English",
                'pictureURL': "http://example.com/image.jpg"})
            self.client.get("/guide_tours")

    @task
    def access_tours_registeret(self):
        self.client.get("/user_tours")

    @task
    def access_register_to_tour(self):
        all_accounts = session.query(Account).all()
        account = random.choice(all_accounts)
        if account.usertype != 'admin':
            response_login = self.client.post("/login", data={'username': account.username,
                                                              'password': account.password})
            if response_login.status_code == 200:
                tours = tour_rep.get_all_tours()
                if tours:
                    tour = random.choice(tours)
                    tour_id = tour.id
                    request_data = {
                        'tour_id': tour_id
                    }
                    self.client.post('/register_for_tour', data=request_data)

    @task
    def access_cancel_tour(self):
        registrations = session.query(tour_account_association).all()
        if registrations:
            registration = random.choice(registrations)
            registerd_account = session.query(Account).filter_by(id=registration.account_id).first()
            response_login = self.client.post("/login",
                                              data={'username': registerd_account.username,
                                                    'password': registerd_account.password})
            if response_login.status_code == 200:
                tour = tour_rep.get_specific_tour(registration.tour_id)
                tour_id = tour.id
                request_data = {
                    'tour_id': tour_id
                }
                self.client.post('/cancel_tour', data=request_data)


if __name__ == "__main__":

    db.metadata.create_all(bind=engine)
    Acc_Rep.create_account(user)
    Acc_Rep.create_account(guide)
    Acc_Rep.create_account(admin)
    try:
        os.environ["locust_test"] = "True"
        app_script_path = os.path.abspath("../src/main/app.py")
        cwd_path = os.path.abspath("../src/main/")

        subprocess.Popen(["python", app_script_path], cwd=cwd_path)
        # det betyr at det blir introdusert 10 brukere hvert sekund
        # til det blir 100 brukere
        subprocess.call(
            "locust -f locust_test.py --host http://127.0.0.1:5000 "
            "--web-host 127.0.0.1 --web-port 8888 --users 50 --spawn-rate 10",
            shell=True)

    finally:
        os.environ["locust_test"] = "False"

        session.close()
        db.metadata.drop_all(engine)

        powershell_command = (
            "Get-Process -Id (Get-NetTCPConnection -LocalPort 8888).OwningProcess | Stop-Process -Force"
        )
        subprocess.run(["powershell.exe", "-Command", powershell_command], shell=True)
