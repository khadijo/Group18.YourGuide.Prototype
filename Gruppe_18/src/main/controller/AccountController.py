from flask import request, redirect, render_template, flash, url_for
from flask_login import login_user

from Gruppe_18.src.main.main import session
from Gruppe_18.src.main.model.models import Account


class AccountController:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def handle_registration(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            phoneNumber = request.form.get('phoneNumber')
            emailAddress = request.form.get('emailAddress')

            if username and password:
                self.account_repository.create_account(username, password, phoneNumber, emailAddress)
                return render_template('index.html')

        return render_template('User_register.html')
