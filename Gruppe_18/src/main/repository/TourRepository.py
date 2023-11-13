from Gruppe_18.src.main.model.models import Tour, guide_tour_association, Account
from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


class TourRepository(JSONRepository):
    def __init__(self, session):
        self.session = session

    def book_tour(self, tour):
        tour = self.session.query(Tour).filter_by(id=tour.id).first()
        if tour is not None:
            booked = int(tour.booked)
            max_travelers = int(tour.max_travelers)
            if not booked >= max_travelers:
                tour.booked = booked + 1
                self.session.commit()
                return True
            return False

    def cancel_booked_tour(self, tour):
        tour = self.session.query(Tour).filter_by(id=tour.id).first()
        if tour is not None:
            booked = int(tour.booked)
            max_travelers = int(tour.max_travelers)
            if not booked >= max_travelers:
                tour.booked = booked - 1
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

    def filter_tour_by_destination(self, destination):
        return self.session.query(Tour).filter_by(destination=destination).all()

    def filter_tour_by_price(self, min_price, max_price):
        return self.session.query(Tour).filter(Tour.cost.between(min_price, max_price)).all()

    def filter_tour_by_language(self, language):
        return self.session.query(Tour).filter_by(language=language).all()

    def filter_tour_by_price_and_destination(self, destination, min_price, max_price):
        return self.session.query(Tour).filter(Tour.cost.between(min_price, max_price))\
            .filter_by(destination=destination).all()

    def filter_tour_by_destination_and_language(self, destination, language):
        return self.session.query(Tour).filter_by(destination=destination).filter_by(language=language).all()

    def filter_tour_by_price_and_language(self, min_price, max_price, language):
        return self.session.query(Tour).filter(Tour.cost.between(min_price, max_price))\
            .filter_by(language=language).all()

    def filter_tour_by_destination_price_language(self, destination, min_price, max_price, language):
        return self.session.query(Tour).filter_by(destination=destination).filter_by(language=language)\
            .filter(Tour.cost.between(min_price, max_price)).all()

    def filter_combinations(self, destination, min_price, max_price, language):
        if destination and min_price and max_price and language:
            return self.filter_tour_by_destination_price_language(destination, min_price, max_price, language)
        elif destination and language:
            return self.filter_tour_by_destination_and_language(destination, language)
        elif destination and min_price and max_price:
            return self.filter_tour_by_price_and_destination(destination, min_price, max_price)
        elif min_price and max_price and language:
            return self.filter_tour_by_price_and_language(min_price, max_price, language)
        elif destination:
            return self.filter_tour_by_destination(destination)
        elif language:
            return self.filter_tour_by_language(language)
        elif min_price and max_price:
            return self.filter_tour_by_price(min_price, max_price)

    def create_tour(self, tour):
        tour = Tour(id=tour.id,
                    title=tour.title,
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

    def guide_register_to_tour(self, tour_id, user_id):
        existing_registration = self.session.query(guide_tour_association).filter_by(
            tour_id=tour_id,
            guide_id=user_id
        ).first()

        if existing_registration:
            print("You have already posted that tour.")
        else:
            tour = self.session.query(Tour).filter_by(id=tour_id).first()
            guide = self.session.query(Account).filter_by(id=user_id).first()

            if tour is not None and guide is not None:
                tour_guide_assoc_obj = guide_tour_association.insert().values(
                    tour_id=tour_id,
                    guide_id=user_id
                )
                self.session.execute(tour_guide_assoc_obj)
                self.session.commit()
                return True
            else:
                print("Tour or guide were not found.")

    def delete_tour(self, tour_id):
        tour = self.session.query(Tour).filter_by(id=tour_id).first()

        if tour is not None:
            self.session.delete(tour)
            self.session.commit()
            return True
        else:
            return False

    def guide_delete_tour(self, tour_id, user_id):
        tour = self.session.query(Tour).filter_by(id=tour_id).first()
        user = self.session.query(Account).filter_by(id=user_id).first()

        if tour is not None and user is not None:
            stmt = guide_tour_association.delete().where(
                guide_tour_association.c.tour_id == tour_id,
                guide_tour_association.c.guide_id == user_id
            )
            self.delete_tour(tour.id)
            self.session.execute(stmt)
            self.session.commit()
        else:
            print("Tour or user is not found.")