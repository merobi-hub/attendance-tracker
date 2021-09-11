from attendance.forms import CreateEvent
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from attendance.forms import CreateEvent, CheckIn
from attendance.models import db, Event, User, Participant

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    # revise: return only future/current events here
    events = Event.query.all()
    return render_template('index.html', events = events)

@site.route('/newevent')
@login_required
def newevent():
    form = CreateEvent()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            # must add precise day/time of event w/ form and db
            title = form.title.data
            host = form.host.data
            day_time = form.day_time.data
            duration = form.duration.data
            other = form.other.data 
            user_id = current_user.id

            event = Event(title, host, day_time, duration, other, user_id)
            db.session.add(event)
            db.session.commit()

            flash(f'Your new event was created successfully', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('An error occurred. Please try again.')

    return render_template('newevent.html', form=form)

@site.route('/checkin', methods = ['GET', 'POST']) 
def checkin():
    form = CheckIn()
    event_id = request.args.get('id', None)
    try:
        if request.method == 'POST' and form.validate_on_submit(): 
            first_name = form.first_name.data 
            last_name = form.last_name.data

            checkin = Participant(first_name, last_name, event_id)
            db.session.add(checkin)
            db.session.commit() 

            flash(f'You have been checked in', 'user-created')

            return redirect(url_for('site.home')) 
    except: 
        raise Exception('An error occurred. Please try again.') 

    return render_template('checkin.html', form=form)

@site.route('/profile')
@login_required
def profile():
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user_events=user_events)

            