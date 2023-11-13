import uuid
from datetime import datetime

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Gruppe_18.src.main.model.models import Account, Tour, tour_account_association, guide_tour_association
from Gruppe_18.src.main.database.sql_alchemy import app
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from flask import render_template, request, flash, redirect, url_for
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.controller.AccountController import AccountController

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

session = get_session()
account_rep = AccountRepository(session)
tour_rep = TourRepository(session)
account_controller = AccountController(account_rep)
app.secret_key = 'gruppe_18'
@login_manager.user_loader
def load_user(user_id):
    return session.query(Account).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = session.query(Account).filter_by(username=username).first()

        if user and user.password == password:
            login_user(user, remember=True)
            return redirect(url_for('home'))

        flash('Wrong username or password', 'danger')

    return render_template('index.html')

@app.route('/home')
def home():
    if current_user.usertype == "admin":
        tours = session.query(Tour).all()
        return render_template('homepage_admin.html')
    elif current_user.usertype == "guide":
        tours = session.query(Tour).all()
        return render_template('homepage_guide.html', tours=tours)
    else:
        tours = session.query(Tour).all()
        return render_template('homepage.html', tours=tours)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account_reg', methods=['GET', 'POST'])
def account_reg():
    if request.method == 'POST':
        usertype = request.form.get('usertype')
        username = request.form.get('username')
        password = request.form.get('password')
        phoneNumber = request.form.get('phoneNumber')
        emailAddress = request.form.get('emailAddress')

        if username and password:
            user = Account(usertype=usertype, username=username, password=password, phoneNumber=phoneNumber, emailAddress=emailAddress)
            account_rep.create_account(user)
            return render_template('index.html')

    return render_template('User_register.html')


@app.route('/search', methods=['GET'])
def search():
    q = request.args.get("q")
    # q is short for query
    print(str(q))
    qs = str(q)
    if q:
        results = session.query(Tour).filter(Tour.title.ilike(f"%{q}%")).order_by(Tour.title)
        # on the above code, please order the result
        print(str(q))
        print(results)
    else:
        results = []
    return render_template("homepage.html", tours=results)

# Run this code to open the application


@app.route('/register_for_tour', methods=['POST'])
def register_for_tour():
    if current_user.is_authenticated:
        tour_id = request.form.get('tour_id')
        user_id = current_user.id

        account_rep.account_register_to_tour(tour_id, user_id)
        return redirect(url_for('user_tours'))
    else:
        flash('You must be logged in to register for a tour', 'danger')
        return redirect(url_for('home'))



@app.route('/user_tours')
def user_tours():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_tours = session.query(Tour).join(
            tour_account_association, Tour.id == tour_account_association.c.tour_id
        ).filter(tour_account_association.c.account_id == user_id).all()

        user = session.query(Account).filter_by(id=user_id).first()

        return render_template('user_tours.html', user_tours=user_tours, user=user)
    else:
        flash('You must be logged in to see your registered tours.', 'danger')
        return redirect(url_for('login'))


@app.route('/cancel_tour', methods=['POST'])
def cancel_tour():
    if current_user.is_authenticated:
        tour_id = request.form.get('tour_id')
        user_id = current_user.id
        tour = session.query(Tour).filter_by(id=tour_id).first()
        if tour:
            account_rep.account_cancel_tour(tour_id, user_id)
            session.commit()
        return render_template('canceled_tour.html', tour=tour)
    else:
        flash('You must be logged in to cancel a tour.', 'danger')
        return redirect(url_for('login'))


@app.route('/New_Tour', methods=['POST', 'GET'])
def New_Tour():
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

        tour = Tour(id=str(uuid.uuid4()), title=title, date=date_obj, destination=destination, duration=duration, cost=cost,
                    max_travelers=max_travelers, language=language, pictureURL=pictureURL)
        tour_rep.create_tour(tour)
        guide_id = current_user.id
        tour_rep.guide_register_to_tour(tour.id, guide_id)

        tours = session.query(Tour).all()
        return render_template('homepage_guide.html', tours=tours)

    return render_template('new_tour.html')

@app.route('/guide_tours')
def guide_tours():
    if current_user.is_authenticated:
        guide_id = current_user.id
        guide_tours = session.query(Tour).join(
            guide_tour_association, Tour.id == guide_tour_association.c.tour_id
        ).filter(guide_tour_association.c.guide_id == guide_id).all()

        user = session.query(Account).filter_by(id=guide_id).first()

        return render_template('guide_tours.html', guide_tours=guide_tours, user=user)
    else:
        flash('You must be logged in to see your registered tours.', 'danger')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
