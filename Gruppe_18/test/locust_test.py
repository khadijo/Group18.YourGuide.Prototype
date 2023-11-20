import os
import subprocess
import uuid

from locust import HttpUser, task, between

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db
from Gruppe_18.src.main.model.models import Account
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.test.database.database_handler import get_session
Acc_Rep = AccountRepository(get_session())

# NB app.py skal ikke kjøre samtidi som locust_test. den kjører app her med test_database tilknyttet
guide = Account(str(uuid.uuid4()), "guide", "guide", "guide", "12345678","guide@gmial.com")
admin = Account(str(uuid.uuid4()), "admin", "admin", "admin", "12345678","guide@gmial.com")
user = Account(str(uuid.uuid4()), "user", "user", "user", "12345678","guide@gmial.com")

module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "Test.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)

session = sessionmaker(bind=engine)()

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Brukerene venter 1-5 sekunder før de sender neste request
    host = "http://127.0.0.1:5000" #applikasjonen vår
    #sender brukere til disse sidene, og utfører requests:

    @task
    def access_start(self):
        response = self.client.get("/")
    @task
    def access_user_registration(self):
            register = self.client.post("/account_reg",
                                        data={'username': str(uuid.uuid4()),
                                              'password': str(uuid.uuid4()),
                                              'phoneNumber': str(uuid.uuid4()),
                                              'emailAddress': str(uuid.uuid4())})
    @task
    def access_user_login(self):
        response_login = self.client.post("/login", data={'username': 'user', 'password': 'user'})

        if response_login.status_code == 200:
            respons_home = self.client.get("/home")

            response_filter = self.client.post("/home/filter",
                                               data={'destination': 'some_destination',
                                                     'max_price': 'some_max_price',
                                                     'min_price': 'some_min_price',
                                                     'language': 'some_language'})

            response_search = self.client.get("/search?q=dubai")

    @task
    def access_guider(self):
        response_login = self.client.post("/login", data={'username': 'guide', 'password': 'guide'})
        if response_login.status_code == 200:
            with session.begin():
                create_tour = self.client.post('/new_tour', data={
                    'title': "Welcome to tour!",
                    'date': "2023, 11, 17",
                    'destination': "country, city",
                    'duration': 5,
                    'cost': 1600,
                    'max_travelers': 5,
                    'language': "English",
                    'pictureURL': "http://example.com/image.jpg"})
            check_published_tours = self.client.get("/guide_tours")
    @task
    def access_tours_registeret(self):
        response = self.client.get("/user_tours")

    @task
    def access_tour_registration(self):
        respons = self.client.get()




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
            "--web-host 127.0.0.1 --web-port 8888 --users 100 --spawn-rate 10",
            shell=True)


    finally:
        os.system("taskkill /F /IM locust")
        os.environ["locust_test"] = "False"

        # tømmer database
        session.close()
        db.metadata.drop_all(engine)


# skrive dette i terminalen hvis processene ikke blir terminert på en port fordi den ikke har
# blitt avsluttet ordentlig:
# Get-Process -Id (Get-NetTCPConnection -LocalPort 8888).OwningProcess | Stop-Process -Force


