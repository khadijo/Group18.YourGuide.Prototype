from Gruppe_18.src.main.model.models import Tour
from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


class TourRepository(JSONRepository):
    def __init__(self, session):
        self.session = session

    def book_tour(self, entity):
        tour = self.session.query(Tour).filter_by(id=entity.id).first()
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
        return self.session.query(Tour).filter_by(id=id).first()
    
    def get_all_tours(self):
        return self.session.query(Tour).all()

    def filter_combinations(self, destination, min_price, max_price, language):
        session = self.session
        query = session.query(Tour)
        if destination:
            query = query.filter_by(destination=destination)
        if min_price or max_price:
            if not max_price:
                max_price = 90000
            if not min_price:
                min_price = 0
            query = query.filter(Tour.cost.between(min_price, max_price))
        if language:
            query = query.filter_by(language=language)
        return query.all()

    def create_tour(self, tour):
        tour = Tour(title=tour.title,
                    date=tour.date,
                    destination=tour.destination,
                    duration=tour.duration,
                    cost=tour.cost,
                    max_travelers=tour.max_travelers,
                    language=tour.language,
                    pictureURL=tour.pictureURL)

        self.session.add(tour)
        self.session.commit()
        return tour

    def delete_tour(self, tour_id):
        tour = self.session.query(Tour).filter_by(id=tour_id).first()

        if tour is not None:
            self.session.delete(tour)
            self.session.commit()
            return True
        else:
            return False

