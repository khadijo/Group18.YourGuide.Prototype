from flask import request, redirect, render_template, flash, url_for
from flask_login import login_user

from Gruppe_18.src.main.model.models import Account


class AccountController:
    def __init__(self, account_repository):
        self.account_repository = account_repository

