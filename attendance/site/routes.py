from flask.json import tojson_filter
from attendance.forms import CreateEvent
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from attendance.forms import CreateEvent, CheckIn
from attendance.models import db, Event, User, Participant

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    # list future/current events here as buttons that lead to checkin
    return render_template('index.html')

@site.route('/newevent')
@login_required
def newevent():
    form = CreateEvent()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            title = form.title.data
            host = form.host.data
            day = form.day.data
            duration = form.duration.data
            other = form.other.data 
            user_id = current_user.id

            event = Event(title, host, day, duration, other, user_id)
            db.session.add(event)
            db.session.commit()

            flash(f'Your new event was created successfully', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('An error occurred. Please try again.')

    return render_template('newevent.html', form=form)

@site.route('/checkin') 
def checkin():
    form = CheckIn()
    try:
        if request.method == 'POST' and form.validate_on_submit(): 
            first_name = form.first_name.data 
            last_name = form.last_name.data
            event_id = # get from button on index.html

            checkin = Participant(first_name, last_name, event_id)
            db.session.add(checkin)
            db.session.commit() 

            flash(f'You have been checked in', 'user-created')

            return redirect(url_for('site.home')) 
    except: 
        raise Exception('An error occurred. Please try again.') 

    return render_template('checkin.html', form=form)

            

            