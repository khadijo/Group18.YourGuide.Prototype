import uuid
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from sqlite3 import IntegrityError

from flask_login import current_user

from Gruppe_18.src.main.model.models import Tour, tour_account_association, Account


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

    # def make_new_tour(self):

