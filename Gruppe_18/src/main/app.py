import os
from sqlite3 import IntegrityError

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.model.models import Account

app = Flask(__name__, template_folder='templates')
module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "YourGuide.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'

db = SQLAlchemy(app)
session = get_session()
account_rep = AccountRepository(session)


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

@app.route('/home', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = User.query.filter_by(username=username).first()

            if user and user.password == password:
                tours = Tour.query.all()
                return render_template('homepage.html', tours=tours)
            else:
                flash('Feil brukernavn eller passord', 'danger')

        except IntegrityError:
            flash('Det oppestod en feil ved innlogging', 'danger')

        return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)
