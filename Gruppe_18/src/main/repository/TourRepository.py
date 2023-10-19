from Gruppe_18.src.main.repository.JSONRepository import JSONRepository

list_with_tours =

class TourRepository (JSONRepository):

    def filter_tour_by_location(tour_list, destination):
        filtered_tours = []
        for tour in tour_list:
            if tour['destination'] == destination:
                filtered_tours.append(tour)
        return filtered_tours

    def filter_tour_by_price(tour_list, max_price, min_price):
        filtered_tours = []
        for tour in tour_list:
            if min_price <= tour['cost'] <= max_price:
                filtered_tours.append(tour)
        return filtered_tours