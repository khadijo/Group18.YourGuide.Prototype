import datetime

class personTour:
    def __init__(self, tour_name, user_name, reference_number):
        self.tour_name = tour_name
        self.user_name = user_name
        self.reference_number = reference_number
        self.sign_up_time = datetime.datetime.now()
        self.is_cancelled = False

class TourAdmin:
    def __init__(self):
        self.tours = []


    def add_tour(self, tour_name, user_name, reference_number):
        tour = personTour(tour_name, user_name, reference_number)  # Use personTour instead of Tour
        self.tours.append(tour)
        print(f"User '{user_name}' signed up for '{tour_name}' tour with the reference number '{reference_number}'.")
        return True

    def cancel_tour(self, tour_name, user_name, reference_number):
        current_time = datetime.datetime.now()
        for tour in self.tours:
            if tour.tour_name == tour_name and tour.user_name == user_name and not tour.is_cancelled:
                time_difference = current_time - tour.sign_up_time
                if time_difference.total_seconds() <= 24 * 3600:  # 24 hours in seconds
                    return True
                    print(f"User '{user_name}' has canceled the '{tour_name}' tour with the reference number '{reference_number}' within 24 hours. No penalty.")
                else:
                    print(f"User '{user_name}' has canceled the '{tour_name}' tour with the reference number '{reference_number}' after 24 hours. Penalty may apply.")
                    return False
                tour.is_cancelled = True
                self.notify_guide_and_admin(tour)
                self.remove_tour_from_user(tour)
                self.send_cancellation_email(tour)
                return
        print(f"User '{user_name}' is not signed up for '{tour_name}' tour with the reference number '{reference_number}' or has already canceled.")
        return True

    def notify_guide_and_admin(self, tour):
        # Implement notification to tour guide and admin here
        print(f"Notifying guide and admin about the cancellation of '{tour.tour_name}' by '{tour.user_name}' with the reference number '{tour.reference_number}'.")

    def remove_tour_from_user(self, tour):
        # Implement removing the tour from the user's list here
        print(f"Removing '{tour.tour_name}' from '{tour.user_name}' 's tour list with the reference number '{tour.reference_number}'.")

    def send_cancellation_email(self, tour):
        # Implement sending an email about the cancellation here
        print(f"Sending cancellation email to '{tour.user_name}' for '{tour.tour_name}'.")

# Example usage:
tour_admin = TourAdmin()

# User signs up for a tour
tour_admin.add_tour("Tour 1", "Nicole", "DORMMB_18")

# User cancels a tour within 24 hours
tour_admin.cancel_tour("Tour 1", "Nicole", "DORMMB_18")

# User cancels a tour after 24 hours
# tour_admin.cancel_tour("Tour 1", "Nicole", "DORMMB_18")

