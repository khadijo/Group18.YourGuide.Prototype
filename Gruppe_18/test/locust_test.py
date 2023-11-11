import os
import subprocess

from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5)  # Brukerene venter 1-5 sekunder før de sender neste request
    host = "http://127.0.0.1:5000" #applikasjonen vår
    #sender brukere til disse sidene, og utfører requests:
    @task
    def access_start(self):
        response = self.client.get("/")


    @task
    def access_account_reg(self):
        response = self.client.get("/account_reg")

    @task
    def access_home(self):
        response = self.client.get("/home")

    @task
    def access_filter(self):
        response = self.client.post("/home/filter",
                                    data={'destination': 'some_destination', 'max_price': 'some_max_price',
                                          'min_price': 'some_min_price', 'language': 'some_language'})

    @task
    def access_tours_registeret(self):
        response = self.client.get("/user_tours")

    @task
    def access_cancel_tour(self):
        response = self.client.post("/cancel_tour")

    @task
    def access_search(self):
        response = self.client.get("/search?q=dubai")


# app.py må kjøre for at den skal kunne sende brukere

if __name__ == "__main__":
    try:
        # 100 brukere med en hastighet på 10 brukere per sekund
        # det betyr at det blir introdusert 10 brukere hvert sekund
        # til det blir 100 brukere
        subprocess.call(
            "locust -f locust_test.py --host http://127.0.0.1:5000 --web-host 127.0.0.1 --web-port 8888 --users 100 --spawn-rate 10",
            shell=True)
    finally:
        # Legg til en kommando for å drepe Locust-prosessen når testen er fullført
        os.system("taskkill /F /IM locust")

# skrive dette i terminalen hvis processene ikke blir terminert på en port fordi den ikke har
# blitt avsluttet ordentlig:
# Get-Process -Id (Get-NetTCPConnection -LocalPort 8888).OwningProcess | Stop-Process -Force


