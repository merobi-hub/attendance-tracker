from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user
from attendance.forms import CreateEvent, CheckIn
from attendance.models import db, Event, Participant
import datetime, timedelta

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    """Displays current and upcoming events"""
    events = Event.query.all()
    live_events = []
    for event in events:
        # Merge day/time form inputs
        dt_str = event.day + ' ' + event.time
        # Convert day/time str to datetime object
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        # Convert duration from mins to seconds
        dur = int(event.duration) * 60
        # Convert dur from int to datetime object
        dur = datetime.timedelta(seconds=int(dur))
        # Calculate event end time
        event_end = dt + dur
        # Compare current time to event end time
        now = str(datetime.datetime.now())[:-7]
        now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        if event_end >= now:
            live_events.append(event)
    return render_template('index.html', events = live_events)

@site.route('/newevent', methods = ['GET', 'POST'])
@login_required
def newevent():
    """Displays CreateEvent form and processes new event submission"""
    form = CreateEvent()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            title = form.title.data
            host = form.host.data
            day = form.day.data
            time = form.time.data
            duration = form.duration.data
            other = form.other.data 
            user_id = current_user.id

            event = Event(title, host, day, time, duration, other, user_id)
            db.session.add(event)
            db.session.commit()

            flash(f'Your new event was created successfully.', 'user-created')
            return redirect(url_for('site.home'))
    except:
        flash(f'An error occurred. Please try again.')
        return redirect(url_for('site.home'))

    return render_template('newevent.html', form=form)

@site.route('/checkin', methods = ['GET', 'POST']) 
def checkin():
    """Displays checkin form and checks in participant if event has begun"""
    form = CheckIn()
    event_id = request.args.get('event_id', None)
    print('event_id: ', event_id)
    event = Event.query.filter_by(id=event_id).first()
    # Combine day/time form inputs
    dt_str = event.day + ' ' + event.time
    # Convert day/time str to datetime object
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    # Using dt, determine if event has begun and prevent early check-in
    start_time = dt
    if datetime.datetime.now() < start_time:
        flash(f'Please wait for the event to begin.', 'auth-failed')
        return redirect(url_for('site.home'))
    else:
        try:
            if request.method == 'POST' and form.validate_on_submit(): 
                first_name = form.first_name.data 
                last_name = form.last_name.data

                checkin = Participant(first_name, last_name, event_id)
                db.session.add(checkin)
                db.session.commit() 

                flash(f'You have been checked in.', 'user-created')

                return redirect(url_for('site.home')) 
        except: 
            raise Exception('An error occurred. Please try again.') 

        return render_template('checkin.html', form=form)

@site.route('/profile')
@login_required
def profile():
    """Displays all events hosted by the current user"""
    host_events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', host_events=host_events)

@site.route('/deleteevent', methods = ['GET', 'POST'])
@login_required
def deleteevent():
    """Permits host to delete an event"""
    id = request.args.get('id', None)
    Event.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'The event has been deleted.', 'user-created')
    return redirect(url_for('site.profile'))

@site.route('/removeparticipant', methods = ['GET', 'POST'])
@login_required 
def removeParticipant():
    """Removes selected participant from an event"""
    id = request.args.get('id', None)
    first_name = request.args.get('first_name', None)
    last_name = request.args.get('last_name', None)
    Participant.query.filter_by(first_name=first_name, last_name=last_name, event_id=id).delete()
    db.session.commit()
    flash('The participant has been removed.', 'user-created')
    return redirect(url_for('site.profile'))

@site.route('/event')
@login_required
def event():
    """Displays all participants checked into an event"""
    event_id = request.args.get('id', None)
    event = Event.query.filter_by(id=event_id).first()
    participants = Participant.query.filter_by(event_id=event_id).all()
    return render_template('event.html', participants=participants, event=event)

# new route: form takes event name and outputs all attendees and each attendee's
# percentage of attended events with same name
@site.route('/calculate')
@login_required 
def calculate():
    
    first_name = request.args.get('first_name', None)
    last_name = request.args.get('last_name', None)
    title = request.args.get('title', None)
    events = Event.query.filter_by(title=title).all()
    # Get total number of events with title
    total_events = 0
    for event in events:
        total_events += 1
    # Get number of events with title attended by participant
    participant_events = 0
    for p, e in db.session.query(Participant, Event).filter(Participant.event_id == Event.id).all():
        if p.first_name == first_name and p.last_name == last_name:
            participant_events += 1
    participant_attendance = (participant_events * 100) / total_events
    name = first_name + ' ' + last_name
    return render_template('calculate.html', title=title, name=name, attendance=participant_attendance)

