import json

from Gruppe_18.src.main.repository.JSONRepository import JSONRepository


# list_with_tours =

class TourRepository(JSONRepository):

    def book_tour(self, entity):
        if not entity.booked >= entity.max_travelers:
            entity.booked += 1
            return True
        else:
            return False

    def get_tour_description(self, entity):
        return f"This tour will take you to {entity.destination} for {entity.duration} hours, and is " \
               f"offered in {entity.language}"

    def filter_tour_by_location(self, tour_list, destination):
        filtered_tours = []
        for tour in tour_list:
            if tour['destination'] == destination:
                filtered_tours.append(tour)
        return filtered_tours

    def filter_tour_by_price(self, tour_list, max_price, min_price):
        filtered_tours = []
        for tour in tour_list:
            if min_price <= tour['cost'] <= max_price:
                filtered_tours.append(tour)
        return filtered_tours
