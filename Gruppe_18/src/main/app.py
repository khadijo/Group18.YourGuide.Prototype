import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "YourGuide.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'

db = SQLAlchemy(app)

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


@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('homepage.html', tours=tours)


if __name__ == '__main__':
    app.run(debug=True)
