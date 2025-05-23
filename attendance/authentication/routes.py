from flask import Blueprint, request, render_template, flash, redirect
from flask_login import login_required, login_user, logout_user
from flask.helpers import url_for
from werkzeug.security import check_password_hash
from attendance.forms import HostLogin
from attendance.models import User, db
import requests
from oauthlib.oauth2 import WebApplicationClient
from config import Config
import json


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
            
            user = User(name='', email=email, profile_pic='', password=password)
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

    return render_template('login.html', form=form, client_id=Config.GOOGLE_CLIENT_ID)

@auth.route('/google', methods = ['GET', 'POST'])
def google():
    try:
        def get_google_provider_cfg():
            return requests.get(Config.GOOGLE_DISCOVERY_URL).json()
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            # redirect_uri = request.base_url + "/callback",
            redirect_uri = Config.GOOGLE_REDIRECT_URI,
            scope = ["openid", "email", "profile"],
            )
        return redirect(request_uri)
    except:
        raise Exception('An error occurred. Please try again.')

@auth.route('/oauth2callback', methods = ['GET', 'POST'])
def callback():
    code = request.args.get('code')
    def get_google_provider_cfg():
        return requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        # redirect_url=request.base_url,
        redirect_uri=Config.GOOGLE_REDIRECT_URI,
        code=code
        )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
        )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['given_name']

        google_user = User.query.filter(User.email == users_email).first()

        if not google_user:
            user = User(name=users_name, email=users_email, profile_pic=picture)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            flash('You were successfully logged in.', 'auth-success')
            return redirect(url_for('site.home'))
        
        else:
            login_user(google_user)

            flash('You were successfully logged in.', 'auth-success')
            return redirect(url_for('site.home'))
    else:
        flash('An error occurred. Please try again.', 'auth-failed')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    flash('You were successfully logged out.', 'auth-success')
    return redirect(url_for('site.home'))