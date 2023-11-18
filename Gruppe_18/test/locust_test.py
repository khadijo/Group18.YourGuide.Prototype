import os
import subprocess
import uuid

from locust import HttpUser, task, between

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db

# NB app.py skal ikke kjøre samtidi som locust_test. den kjører app her med test_database tilknyttet


module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "Test.db")
engine = create_engine(f"sqlite:///{database_name}", echo=True)

session = sessionmaker(bind=engine)()

db.metadata.create_all(bind=engine)




class MyUser(HttpUser):
    wait_time = between(1, 5)  # Brukerene venter 1-5 sekunder før de sender neste request
    host = "http://127.0.0.1:5000" #applikasjonen vår
    #sender brukere til disse sidene, og utfører requests:

    @task
    def access_start(self):
        response = self.client.get("/")

    @task
    def access_user(self):
        with session.begin():
            username = str(uuid.uuid4())
            password = str(uuid.uuid4())
            register = self.client.post("/account_reg",
                                        data={'usertype': 'user',
                                              'username': username,
                                              'password': password,
                                              'phoneNumber': '123456789',
                                              'emailAddress': 'testuser@example.com'})

        if register.status_code == 200:
            response_login = self.client.post("/login", data={'username': username, 'password': password})

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
        with session.begin():
            username = str(uuid.uuid4())
            password = str(uuid.uuid4())
            register = self.client.post("/account_reg",
                                        data={
                                            'usertype': 'guide',
                                            'username': username,
                                            'password': password,
                                            'phoneNumber': '123456789',
                                            'emailAddress': 'testuser@example.com'})
            session.commit()
        if register.status_code == 200:
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
                session.commit()

        check_published_tours = self.client.get("/guide_tours")
    @task
    def access_tours_registeret(self):
        response = self.client.get("/user_tours")

    def access_tour_registration(self):
        respons = self.client.get()




if __name__ == "__main__":
    try:
        # setter applikasjonen til å bruke test databasen
        os.environ["locust_test"] = "True"
        # kjører applikasjonen
        app_script_path = os.path.abspath("../src/main/app.py")
        cwd_path = os.path.abspath("../src/main/")

        subprocess.Popen(["python", app_script_path], cwd=cwd_path)
        # kjører selve locust test
        # 100 brukere med en hastighet på 10 brukere per sekund
        # det betyr at det blir introdusert 10 brukere hvert sekund
        # til det blir 100 brukere
        subprocess.call(
            "locust -f locust_test.py --host http://127.0.0.1:5000 "
            "--web-host 127.0.0.1 --web-port 8888 --users 100 --spawn-rate 10",
            shell=True)


    finally:
        # Legg til en kommando for å drepe Locust-prosessen når testen er fullført
        os.system("taskkill /F /IM locust")
        # setter applikasjonen tilbake til vanlig database
        os.environ["locust_test"] = "False"

        # tømmer database

        session.close()
        db.metadata.drop_all(engine)


# skrive dette i terminalen hvis processene ikke blir terminert på en port fordi den ikke har
# blitt avsluttet ordentlig:
# Get-Process -Id (Get-NetTCPConnection -LocalPort 8888).OwningProcess | Stop-Process -Force


