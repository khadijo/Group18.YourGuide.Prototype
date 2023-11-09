from flask import Flask, render_template, request, flash
from sqlite3 import IntegrityError

class tourController():
    def __init__(self, tour_repository):
        self.tour_repository = tour_repository

    def filter_app(self):
        if request.method == 'POST':
            destination = request.form['destination']
            max_price = request.form['max_price']
            min_price = request.form['min_price']
            language = request.form['language']
            try:
                filter_tours = self.tour_repository.filter_combinations(destination, min_price, max_price, language)
                return render_template("homepage.html", tours=filter_tours)
            except IntegrityError:
                flash('there was a mistake', 'danger')
            return render_template("homepage.html")
