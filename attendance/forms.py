from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email
import flask_login

class CreateEvent(FlaskForm, flask_login.UserMixin):
    title = TextAreaField('Title', validators=[DataRequired()])
    host = TextAreaField('Host', validators=[DataRequired()])
    day = TextAreaField('Day (yyyy-mm-dd)', validators=[DataRequired()])
    time = TextAreaField('Time (use 24-hour clock in format hh:mm:ss)', validators=[DataRequired()])
    duration = TextAreaField('Duration (minutes)', validators=[DataRequired()])
    other = TextAreaField('Other')
    passkey = TextAreaField('Optional Passkey (provide to attendees)')
    submit_button = SubmitField()

class CheckIn(FlaskForm):
    first_name = TextAreaField('First Name', validators=[DataRequired()])
    last_name = TextAreaField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    passkey = TextAreaField('Passkey (if provided)')
    submit_button = SubmitField()

class AddParticipant(FlaskForm):
    first_name = TextAreaField('First Name', validators=[DataRequired()])
    last_name = TextAreaField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_button = SubmitField()

class HostLogin(FlaskForm, flask_login.UserMixin):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()
