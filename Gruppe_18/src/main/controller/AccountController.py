import uuid
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_user, current_user
from Gruppe_18.src.main.model.models import Account, Tour, guide_tour_association


class AccountController:
    def __init__(self, account_repository, session):
        self.account_repository = account_repository
        self.session = session

    def account_login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = self.account_repository.get_user_by_username(username)

            if user and user.password == password:
                login_user(user, remember=True)
                return redirect(url_for('home'))

            flash('Wrong username or password', 'danger')

        return render_template('index.html')

    def account_registration(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            phoneNumber = request.form.get('phoneNumber')
            emailAddress = request.form.get('emailAddress')
            if username and password:
                user = Account(id=str(uuid.uuid4()), usertype="user", username=username, password=password,
                               phoneNumber=phoneNumber,
                               emailAddress=emailAddress)
                self.account_repository.create_account(user)
                return render_template('index.html')

        return render_template('User_register.html')

    def tour_registration(self):
        if current_user.is_authenticated:
            tour_id = request.form.get('tour_id')
            user_id = current_user.id

            self.account_repository.account_register_to_tour(tour_id, user_id)
            return redirect(url_for('user_tours'))
        else:
            flash('You must be logged in to register for a tour', 'danger')
            return redirect(url_for('login'))

    def account_cancel_tour(self):
        if current_user.is_authenticated:
            tour_id = request.form.get('tour_id')
            user_id = current_user.id
            tour = self.session.query(Tour).filter_by(id=tour_id).first()
            if tour:
                self.account_repository.account_cancel_tour(tour_id, user_id)
                self.session.commit()
            return render_template('canceled_tour.html', tour=tour)
        else:
            flash('You must be logged in to cancel a tour.', 'danger')
            return redirect(url_for('login'))

    def deleting_account(self):
        if current_user.is_authenticated:
            user_id = request.form.get('user_id')
            user = self.session.query(Account).filter_by(id=user_id).first()
            if user:
                self.account_repository.delete_account(user_id)
                self.session.commit()
            return render_template('deleted_account.html', user=user)
        else:
            flash('You must be logged in to delete the account.', 'danger')
            return redirect(url_for('login'))

    def delete_my_account(self):
        if current_user.is_authenticated:
            account_id = current_user.id
            account = self.session.query(Account).filter_by(id=account_id).first()
            if account:
                self.account_repository.delete_account(account_id)
                self.session.commit()
            return render_template('User_register.html')

    def update_user_information(self):
        if current_user.is_authenticated:
            new_username = request.form.get("username")
            new_telephone_number = request.form.get("phoneNumber")
            new_email = request.form.get("email")

            current_user_id = current_user.id
            self.account_repository.update_account(current_user_id, new_username, new_telephone_number, new_email)

            self.session.commit()
            return redirect(url_for('home'))

    def update_usertype(self):
        if current_user.is_authenticated:
            user_to_upgrade = request.form.get("user_id")
            self.account_repository.upgrade_usertype_to_guide(user_to_upgrade)
            self.session.commit()
            return redirect(url_for('home'))

    def admin_get_all_users(self):
        users = self.account_repository.get_all_users()
        return render_template('homepage_admin.html', users=users, show_all_users=True)

    def admin_hide_all_user(self):
        return render_template('homepage_admin.html', show_all_users=False)

    def show_profile(self):
        user_data = self.account_repository.get_one_specific_account(current_user.get_id())
        return render_template('profile.html', user_data=user_data)
