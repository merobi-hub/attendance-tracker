from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_login import UserMixin

class CreateEvent(FlaskForm, UserMixin):
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
    passkey = TextAreaField('Passkey (if provided)')
    submit_button = SubmitField()

class AddParticipant(FlaskForm):
    first_name = TextAreaField('First Name', validators=[DataRequired()])
    last_name = TextAreaField('Last Name', validators=[DataRequired()])
    submit_button = SubmitField()

class HostLogin(FlaskForm, UserMixin):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()


