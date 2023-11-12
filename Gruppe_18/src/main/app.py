from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Gruppe_18.src.main.model.models import Account, Tour, tour_account_association
from Gruppe_18.src.main.database.sql_alchemy import app
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask import render_template, request, flash, redirect, url_for
from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.database.sql_alchemy import get_session
from Gruppe_18.src.main.controller.AccountController import AccountController

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

session = get_session()
account_rep = AccountRepository(session)
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
    if current_user.usertype == "user":
        tours = session.query(Tour).all()
        return render_template('homepage.html', tours=tours)
    elif current_user.usertype == "guide":
        tours = session.query(Tour).all()
        return render_template('homepage_guide.html', tours=tours)



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

@app.route('/home/filter', methods=['GET','POST'])
def filter_tour():
    try:
        return tourC.filter_app()
    except sqlalchemy.exc.InvalidRequestError as e:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
