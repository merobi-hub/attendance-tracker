from flask import Blueprint, request, render_template, flash, redirect
from flask.helpers import url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from attendance.forms import HostLogin
from attendance.models import User, db
import requests
from oauthlib.oauth2 import WebApplicationClient
from config import Config

auth = Blueprint('auth', __name__, template_folder='auth_templates') 

# OAuth 2 client setup
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = HostLogin()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data 
            password = form.password.data 
            
            user = User(email, password=password)
            db.session.add(user)
            db.session.commit()

            flash(f'A user account for {email} has been created', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('An error occurred. Please try again.')

    return render_template('signup.html', form=form) 

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = HostLogin() 
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)

                flash('You were successfully logged in.', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Email or password is incorrect. Please try again.', 'auth-failed')
                return redirect(url_for('auth.login'))

    except:
        raise Exception('An error occurred. Please try again.')

    return render_template('login.html', form=form)

@auth.route('/google', methods = ['GET', 'POST'])
def google():
    def get_google_provider_cfg():
        return requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = request.base_url + "/callback",
        scope = ["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))