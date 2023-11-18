from flask_login import LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from Gruppe_18.src.main.controller.TourController import TourController
from Gruppe_18.src.main.model.models import Account, Tour
from Gruppe_18.src.main.database.app_config import app
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask import render_template, redirect, url_for
from Gruppe_18.src.main.database.create_data_db import get_session
from Gruppe_18.src.main.controller.AccountController import AccountController
from Gruppe_18.src.main.repository.TourRepository import TourRepository

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
    return tour_controller.homepage_based_on_usertype()


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
    return tour_controller.make_new_tour()


@app.route('/guide_tours')
def guide_tours():
    return tour_controller.show_guide_tour()


@app.route('/delete_tour', methods=['POST'])
def delete_tour():
    return tour_controller.deleting_tour()


@app.route('/show_all_tours', methods=['GET'])
def show_tours():
    tours = session.query(Tour).all()
    return render_template('homepage_admin.html', tours=tours, show_all_tours=True)


@app.route('/hide_tours', methods=['GET'])
def hide_tours():
    return render_template('homepage_admin.html', show_all_tours=False)


@app.route('/show_all_users', methods=['GET'])
def show_all_users():
    users = session.query(Account).all()
    return render_template('homepage_admin.html', users=users, show_all_users=True)


@app.route('/hide_all_users', methods=['GET'])
def hide_all_users():
    return render_template('homepage_admin.html', show_all_users=False)


@app.route('/delete_account', methods=['POST'])
def delete_account():
    return account_controller.deleting_account()


@app.route('/show_dashboard', methods=['GET'])
def show_dashboard():
    data = tour_rep.admin_dashboard()
    return render_template('homepage_admin.html', **data, show_dashboard=True)


@app.route('/hide_dashboard', methods=['GET'])
def hide_dashboard():
    return render_template('homepage_admin.html', show_dashboard=False)


@app.route('/profile')
@login_required
def profile():
    user_data = load_user(current_user.get_id())
    return render_template('profile.html', user_data=user_data)


@app.route('/home/filter', methods=['GET', 'POST'])
def filter_tour():
    return tour_controller.filter_app()


@app.route('/delete_user', methods=['POST'])
def delete_user():
    return account_controller.delete_my_account()


# Update user info
@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    return account_controller.update_user_information()


@app.route('/upgrade_usertype', methods=['POST'])
def upgrade_usertype():
    return account_controller.update_usertype()


if __name__ == '__main__':
    app.run(debug=True)
