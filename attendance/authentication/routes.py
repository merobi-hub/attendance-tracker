from flask import Blueprint, request, render_template, flash, redirect
from flask.helpers import url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from attendance.forms import HostLogin
from attendance.models import User, db, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates') 

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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.html'))