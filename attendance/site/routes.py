from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user
from attendance.forms import AddParticipant, CreateEvent, CheckIn
from attendance.models import db, Event, Participant
import datetime, timedelta
from sqlalchemy import desc

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    """Displays current and upcoming events."""
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
    """Displays CreateEvent form and processes new event submission."""
    form = CreateEvent()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            title = form.title.data.strip().title()
            host = form.host.data.strip().title()
            day = form.day.data.strip()
            time = form.time.data.strip()
            duration = form.duration.data.strip()
            other = form.other.data.strip().title()
            passkey = form.passkey.data.strip() 
            user_id = current_user.id

            event = Event(title, host, day, time, duration, other, passkey, user_id)
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
    """Displays checkin form and checks in participant if event has begun."""
    form = CheckIn()
    event_id = request.args.get('event_id', None)
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
    # Look for passkey in db and, if needed, request from attendee before checking in
        try:
            if request.method == 'POST' and form.validate_on_submit():
                if event.passkey != None:
                    if form.passkey.data is not None:
                        passkey = form.passkey.data
                        if event.passkey == passkey:
                            first_name = form.first_name.data.strip().title() 
                            last_name = form.last_name.data.strip().title()
                            checkin = Participant(first_name, last_name, event_id)
                            db.session.add(checkin)
                            db.session.commit() 

                            flash(f'You have been checked in.', 'user-created')

                            return redirect(url_for('site.home'))

                        elif event.passkey != passkey:

                            flash(f'Incorrect passkey. Please try again.', 'auth-failed')

                            return redirect(url_for('site.home'))
                else:

                    first_name = form.first_name.data.strip().title() 
                    last_name = form.last_name.data.strip().title()
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
    """Displays all events hosted by the current user, ordered by event date."""
    host_events = Event.query.filter_by(user_id=current_user.id).order_by(Event.day.desc()).all()
    return render_template('profile.html', host_events=host_events)

@site.route('/deleteevent', methods = ['GET', 'POST'])
@login_required
def deleteevent():
    """
    Deletes an event. Rows in the Participant and Event tables with matching 
    'event_id' (Participant) and 'id' (Event) values are deleted.
    """
    id = request.args.get('id', None)
    Participant.query.filter_by(event_id=id).delete()
    Event.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'The event has been deleted.', 'user-created')
    return redirect(url_for('site.profile'))

@site.route('/removeparticipant', methods = ['GET', 'POST'])
@login_required 
def removeParticipant():
    """Removes selected participant from an event."""
    id = request.args.get('id', None)
    first_name = request.args.get('first_name', None)
    last_name = request.args.get('last_name', None)
    Participant.query.filter_by(
        first_name=first_name, 
        last_name=last_name, 
        event_id=id
        ).delete()
    db.session.commit()
    flash('The participant has been removed.', 'user-created')
    return redirect(url_for('site.profile'))

@site.route('/event')
@login_required
def event():
    """Displays all participants checked into an event."""
    event_id = request.args.get('id', None)
    event = Event.query.filter_by(id=event_id).first()
    participants = Participant.query.filter_by(event_id=event_id).all()
    return render_template('event.html', participants=participants, event=event)

@site.route('/calculate')
@login_required 
def calculate():
    """
    Displays an attendee's percentage of attended events with the same 'title' 
    and 'other' data.
    """
    first_name = request.args.get('first_name', None)
    last_name = request.args.get('last_name', None)
    title = request.args.get('title', None)
    other = request.args.get('other', None)
    events = Event.query.filter_by(title=title, other=other).all()
    # Get total number of events with title and other data
    total_events = 0
    for event in events:
        total_events += 1
    # Get number of events with title attended by participant
    participant_events = 0
    for p, e in db.session.query(Participant, Event).filter(
        Participant.event_id == Event.id, 
        Event.title == title, 
        Event.other == other
        ).all():
        if p.first_name == first_name and p.last_name == last_name:
            participant_events += 1
    participant_attendance = (participant_events * 100) / total_events
    name = first_name + ' ' + last_name
    return render_template(
        'calculate.html', 
        title=title, 
        other=other, 
        name=name, 
        attendance=participant_attendance,
        total_events=total_events
        )

@site.route('/calculateall')
@login_required
def calculateAll():
    """"""
    title = request.args.get('title', None)
    other = request.args.get('other', None)
    events = Event.query.filter_by(title=title, other=other).all()
    total_events = 0 
    for event in events:
        total_events += 1 
    participants = db.session.query(Participant, Event).filter(
        Participant.event_id == Event.id, 
        Event.title == title,
        Event.other == other
        ).all()
    # for p, e in participants:
    #     print(p.first_name)
    #     print(p.last_name)
    total_attendance = {}
    for p, e in participants:
        if p.first_name.strip() + ' ' + p.last_name.strip() in total_attendance.keys():
            total_attendance[p.first_name.strip() + ' ' + p.last_name.strip()] += 1
        else:
            total_attendance[p.first_name.strip() + ' ' + p.last_name.strip()] = 1
    # print(total_attendance)
    return render_template(
        'calculateall.html', 
        title=title, 
        other=other, 
        total_attendance=total_attendance
        )

@site.route('/addparticipant', methods = ['GET', 'POST'])
@login_required 
def addParticipant():
    """
    Allows a host to add a participant to an event from the profile route. 
    Simplified by exclusion of passkey and day/time checking.
    """
    form = AddParticipant()
    event_id = request.args.get('id', None)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            
            first_name = form.first_name.data.strip().title() 
            last_name = form.last_name.data.strip().title()
            checkin = Participant(first_name, last_name, event_id)
            db.session.add(checkin)
            db.session.commit() 

            flash(f'Participant has been added.', 'user-created')

            return redirect(url_for('site.profile'))
    except: 
        raise Exception('An error occurred. Please try again.') 

    return render_template('addparticipant.html', form=form)

@site.route('/editevent', methods = ['GET', 'POST'])
@login_required 
def editevent():
    """
    Allows a host to edit an event. Populates the form with existing data from 
    the db for reference.
    """
    form = CreateEvent()
    event_id = request.args.get('id', None)
    title = request.args.get('title', None)
    host = request.args.get('host', None)
    day = request.args.get('day', None)
    time = request.args.get('time', None)
    duration = request.args.get('duration', None)
    other = request.args.get('other', None)
    passkey = request.args.get('passkey', None)

    try:
        if request.method == 'POST' and form.validate_on_submit():
            Event.query.filter_by(id=event_id).update({
                "title": (form.title.data.strip().title()),
                "host": (form.host.data.strip().title()),
                "day": (form.day.data.strip()),
                "time": (form.time.data.strip()),
                "duration": (form.duration.data.strip()),
                "other": (form.other.data.strip()),
                "passkey": (form.passkey.data.strip()),
                "user_id": (current_user.id)
            })
            db.session.commit() 

            flash(f'The {form.title.data} event has been updated.', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('An error occurred. Please try again.')

    return render_template(
        'editevent.html', 
        form=form, 
        title=title,
        host=host,
        day=day,
        time=time,
        duration=duration,
        other=other,
        passkey=passkey
        )