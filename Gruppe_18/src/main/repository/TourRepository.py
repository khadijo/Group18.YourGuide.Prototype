from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


class TourRepository (JSONRepository):
    def save_to_json(self, tour):
        filename = "tour.json"
        super().save_to_json(tour, filename)

