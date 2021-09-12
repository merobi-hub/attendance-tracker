from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_login import UserMixin

class CreateEvent(FlaskForm, UserMixin):
    title = TextAreaField('Title', validators=[DataRequired()])
    host = TextAreaField('Host', validators=[DataRequired()])
    day_time = TextAreaField('Day (yyyy-mm-dd hh:mm:ss)', validators=[DataRequired()])
    duration = TextAreaField('Duration (seconds)', validators=[DataRequired()])
    other = TextAreaField('Other')
    submit_button = SubmitField()

class CheckIn(FlaskForm):
    first_name = TextAreaField('First Name', validators=[DataRequired()])
    last_name = TextAreaField('Last Name', validators=[DataRequired()])
    submit_button = SubmitField()

class HostLogin(FlaskForm, UserMixin):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

