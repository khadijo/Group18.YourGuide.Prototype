import os
from sqlite3 import IntegrityError

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.model.models import Account
from Gruppe_18.src.main.controller.tourController import tourController

from Gruppe_18.src.main.model.models import Account, tour_account_association
app = Flask(__name__, template_folder='templates')
module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "YourGuide.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'
app.secret_key = 'gruppe18'

db = SQLAlchemy(app)
session = get_session()
account_rep = AccountRepository(session)
tour_rep = TourRepository(session)
tourC = tourController(tour_rep)


class Tour(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.String)
    destination = db.Column(db.String)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    max_travelers = db.Column(db.Integer)
    language = db.Column(db.String)
    pictureURL = db.Column(db.String)
    booked = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    phoneNumber = db.Column(db.String)
    emailAddress = db.Column(db.String)
@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('index.html')


authenticated_user = None


@app.route('/home', methods=['GET', 'POST'])
def login():
    global authenticated_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = User.query.filter_by(username=username).first()

            if user and user.password == password:
                authenticated_user = user
                tours = Tour.query.all()
                return render_template('homepage.html', tours=tours)
            else:
                flash('Wrong username or password', 'danger')

        except IntegrityError:
            flash('An error occurred during login.', 'danger')

        return render_template('index.html')


@app.route('/home/filter', methods=['GET','POST'])
def filter_tour():
    return tourC.filter_app()


@app.route('/Account_reg', methods=['GET', 'POST'])
def account_reg():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phoneNumber = request.form.get('phoneNumber')
        emailAddress = request.form.get('emailAddress')
        if username and password:
            user = Account(username=username, password=password, phoneNumber=phoneNumber, emailAddress=emailAddress)
            account_rep.create_account(user)
            return render_template('index.html')

    return render_template('User_register.html')

@app.route('/register_for_tour', methods=['POST'])
def register_for_tour():
    global authenticated_user
    if authenticated_user is not None:
        tour_id = request.form.get('tour_id')
        user_id = authenticated_user.id
        account_rep.account_register_to_tour(tour_id, user_id)
        return 'You are now registered for the tour.'
    else:
        return 'You must be logged in to register for a tour', 401

@app.route('/user_tours')
def user_tours():
    global authenticated_user
    if authenticated_user is not None:
        user_id = authenticated_user.id
        user_tours = session.query(Tour).join(
            tour_account_association, Tour.id == tour_account_association.c.tour_id
        ).filter(tour_account_association.c.account_id == user_id).all()

        user = session.query(Account).filter_by(account_id=user_id).first()

        return render_template('user_tours.html', user_tours=user_tours, user=user)
    else:
        flash('You must be logged in to see your registered tours.', 'danger')
        return redirect(url_for('login'))


@app.route('/cancel_tour', methods=['POST'])
def cancel_tour():
    global authenticated_user
    if authenticated_user is not None:
        tour_id = request.form.get('tour_id')
        user_id = authenticated_user.id
        account_rep.account_cancel_tour(tour_id, user_id)
        flash('Your tour was canceled', 'success')
        return render_template('canceled_tour.html')
    else:
        flash('You must be logged in to cancel a tour.', 'danger')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
