from Gruppe_18.src.main.model.models import Tour
from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


class TourRepository(JSONRepository):
    def __init__(self, session):
        self.session = session

    def book_tour(self, entity):
        tour = self.session.query(Tour).filter_by(tour_id=entity.tour_id).first()
        if tour is not None:
            booked = int(tour.booked)
            max_travelers = int(tour.max_travelers)
            if not booked >= max_travelers:
                tour.booked = booked + 1
                self.session.commit()
                return True
            return False

    def get_tour_description(self, tour_id):
        tour = self.session.query(Tour).filter_by(tour_id=tour_id).first()

        if tour:
            description = f"This tour will take you to {tour.destination} for {tour.duration} hours, and is offered in {tour.language}"
            return description
        else:
            return "Tour not found"

    def get_spesific_tour(self, id):
        return self.session.query(Tour).filter_by(tour_id=id).first()
    def get_all_tours(self):
        return self.session.query(Tour).all()

    def filter_tour_by_location(self, destination):
        return self.session.query(Tour).filter_by(destination=destination).all()

    def filter_tour_by_price(self, max_price, min_price):
        return self.session.query(Tour).filter(Tour.cost.between(min_price, max_price)).all()

    def create_tour(self, entity):
        tour = Tour(title=entity.title,
                    date=entity.date,
                    destination=entity.destination,
                    duration=entity.duration,
                    cost=entity.cost,
                    max_travelers=entity.max_travelers,
                    language=entity.language,
                    pictureURL=entity.pictureURL)

        self.session.add(tour)
        self.session.commit()
        return tour

    def delete_tour(self, tour_id):
        tour = self.session.query(Tour).filter_by(tour_id=tour_id).first()

        if tour is not None:
            self.session.delete(tour)
            self.session.commit()
            return True
        else:
            return False

