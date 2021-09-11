from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email

class CreateEvent(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    host = TextAreaField('Host', validators=[DataRequired()])
    day_time = DateTimeField('Day (yyyy-mm-dd hh:mm:ss)', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    duration = TextAreaField('Duration (minutes)', validators=[DataRequired()])
    other = TextAreaField('Other')
    submit_button = SubmitField()

class CheckIn(FlaskForm):
    first_name = TextAreaField('First Name', validators=[DataRequired()])
    last_name = TextAreaField('Last Name', validators=[DataRequired()])
    submit_button = SubmitField()

class HostLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

