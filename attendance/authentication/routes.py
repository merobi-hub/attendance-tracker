from flask import Blueprint, request, render_template, flash, redirect
from flask_login import login_user, logout_user, login_required
from attendance.forms import UserLogin


auth = Blueprint('auth', __name__, template_folder='auth_templates') 

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLogin()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data 
            password = form.password.data 
            user = User(email, password = password) 

