from flask import Blueprint, render_template 
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    print('site route loading')
    return render_template('index.html')

