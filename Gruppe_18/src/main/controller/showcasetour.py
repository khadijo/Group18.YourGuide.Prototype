from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/khad1/OneDrive - Østfold University College/B3/host/S/Gruppe_18/Gruppe_18/src/main/YourGuide.db'
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
    pictureURL = db.Column(db.String)  # Endret fra picture til pictureURL
    booked = db.Column(db.Integer)

@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('homepage.html', tours=tours)

if __name__ == '__main__':
    app.run(debug=True)
