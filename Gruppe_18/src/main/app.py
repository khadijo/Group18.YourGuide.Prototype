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
from Gruppe_18.src.main.controller.TourController import TourController

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

session = get_session()
account_rep = AccountRepository(session)
tour_rep = TourRepository(session)
account_controller = AccountController(account_rep, session)
tour_controller = TourController(tour_rep, session)
app.secret_key = 'gruppe_18'


@login_manager.user_loader
def load_user(user_id):
    return session.query(Account).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return account_controller.account_login()


@app.route('/home')
def home():
    tours = session.query(Tour).all()
    if current_user.usertype == "admin":
        return render_template('homepage_admin.html')
    elif current_user.usertype == "guide":
        return render_template('homepage_guide.html', tours=tours)
    else:
        return render_template('homepage.html', tours=tours)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account_reg', methods=['GET', 'POST'])
def account_reg():
    return account_controller.account_registration()


@app.route('/search', methods=['GET'])
def search():
    return tour_controller.search_tour()


@app.route('/register_for_tour', methods=['POST'])
def register_for_tour():
    return account_controller.tour_registration()


@app.route('/user_tours')
def user_tours():
    return tour_controller.get_user_tours()


@app.route('/cancel_tour', methods=['POST'])
def cancel_tour():
    return account_controller.account_cancel_tour()


@app.route('/new_tour', methods=['POST', 'GET'])
def new_tour():
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


@app.route('/delete_tour', methods=['POST'])
def delete_tour():
    if current_user.is_authenticated:
        tour_id = request.form.get('tour_id')
        user_id = current_user.id
        tour = session.query(Tour).filter_by(id=tour_id).first()
        if tour:
            tour_rep.guide_delete_tour(tour_id, user_id)
            session.commit()
        return render_template('deleted_tour.html', tour=tour)
    else:
        flash('You must be logged in to cancel a tour.', 'danger')
        return redirect(url_for('login'))


@app.route('/show_tours', methods=['GET'])
def show_tours():
    tours = session.query(Tour).all()
    return render_template('homepage_admin.html', tours=tours, show_tours=True)


@app.route('/hide_tours', methods=['GET'])
def hide_tours():
    return render_template('homepage_admin.html', show_tours=False)


@app.route('/show_all_users', methods=['GET'])
def show_all_users():
    users = session.query(Account).all()
    return render_template('homepage_admin.html', users=users, show_all_users=True)


@app.route('/hide_all_users', methods=['GET'])
def hide_all_users():
    return render_template('homepage_admin.html', show_all_users=False)


if __name__ == '__main__':
    app.run(debug=True)
