import uuid
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from sqlite3 import IntegrityError

from flask_login import current_user

from Gruppe_18.src.main.model.models import Tour, tour_account_association, Account, guide_tour_association


class TourController():
    def __init__(self, tour_repository, session):
        self.tour_repository = tour_repository
        self.session = session

    def filter_app(self):
        if request.method == 'POST':
            destination = request.form['destination']
            max_price = request.form['max_price']
            min_price = request.form['min_price']
            language = request.form['language']
            try:
                if destination or max_price or min_price or language:
                    filter_tours = self.tour_repository.filter_combinations(destination, min_price, max_price, language)
                else:
                    filter_tours = self.tour_repository.get_all_tours()
                return render_template("homepage.html", tours=filter_tours)
            except IntegrityError:
                flash('there was a mistake', 'danger')
            return render_template("homepage.html")

    def search_tour(self):
        q = request.args.get("q")
        # q is short for query
        print(str(q))
        qs = str(q)
        if q:
            results = self.session.query(Tour).filter(Tour.title.ilike(f"%{q}%")).order_by(Tour.title)
            # on the above code, please order the result
            print(str(q))
            print(results)
        else:
            results = []
        return render_template("homepage.html", tours=results)

    def get_user_tours(self):
        if current_user.is_authenticated:
            user_id = current_user.id
            user_tours = self.session.query(Tour).join(
                tour_account_association, Tour.id == tour_account_association.c.tour_id
            ).filter(tour_account_association.c.account_id == user_id).all()

            user = self.session.query(Account).filter_by(id=user_id).first()

            return render_template('user_tours.html', user_tours=user_tours, user=user)
        else:
            flash('You must be logged in to see your registered tours.', 'danger')
            return redirect(url_for('login'))

    def make_new_tour(self):
        if request.method == 'POST':
            title = request.form.get('title')
            date = request.form.get('date')
            date_obj = datetime.strptime(date, '%Y, %m, %d')
            destination = request.form.get('destination')
            duration = request.form.get('duration')
            cost = request.form.get('cost')
            max_travelers = request.form.get('max_travelers')
            language = request.form.get('language')
            pictureURL = request.form.get('pictureURL')
            tour = Tour(id=str(uuid.uuid4()), title=title, date=date_obj, destination=destination, duration=duration,
                        cost=cost,
                        max_travelers=max_travelers, language=language, pictureURL=pictureURL)
            self.tour_repository.create_tour(tour)
            guide_id = current_user.id
            self.tour_repository.guide_register_to_tour(tour.id, guide_id)
            tours = self.session.query(Tour).all()
            return render_template('homepage_guide.html', tours=tours)

        return render_template('new_tour.html')

    def show_guide_tour(self):
        if current_user.is_authenticated:
            guide_id = current_user.id
            guide_tours = self.session.query(Tour).join(
                guide_tour_association, Tour.id == guide_tour_association.c.tour_id
            ).filter(guide_tour_association.c.guide_id == guide_id).all()

            user = self.session.query(Account).filter_by(id=guide_id).first()

            return render_template('guide_tours.html', guide_tours=guide_tours, user=user)
        else:
            flash('You must be logged in to see your registered tours.', 'danger')
            return redirect(url_for('login'))

    def deleting_tour(self):
        if current_user.is_authenticated:
            tour_id = request.form.get('tour_id')
            user_id = current_user.id
            tour = self.session.query(Tour).filter_by(id=tour_id).first()
            if tour:
                self.tour_repository.guide_delete_tour(tour_id, user_id)
                self.session.commit()
            return render_template('deleted_tour.html', tour=tour)
        else:
            flash('You must be logged in to delete a tour.', 'danger')
            return redirect(url_for('login'))

