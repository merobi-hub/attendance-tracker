from flask_sqlalchemy import SQLAlchemy
# from datetime import date, time 
import uuid 
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager 

db = SQLAlchemy() 
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id) 

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, default='')

    def __init__(self, email, id='', password=''):
        self.id = self.set_id() 
        self.email = email 
        self.password = self.set_password(password)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 

    def __repr__(self):
        return f'An account for {self.email} has been created.'

class Event(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(300))
    host = db.Column(db.String(150))
    day = db.Column(db.String(10))
    time = db.Column(db.String(8))
    duration = db.Column(db.String(5))
    other = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(
        self,
        title,
        host,
        day,
        time,
        duration,
        other,
        user_id,
        id = ''
        ):
        self.id = self.set_id()
        self.title = title 
        self.host = host 
        self.day = day
        self.time = time 
        self.duration = duration 
        self.other = other
        self.user_id = user_id  

    def __repr__(self):
        return f'{self.title} has been created.'

    def set_id(self):
        return str(uuid.uuid4())

class Participant(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    event_id = db.Column(db.String, db.ForeignKey('event.id'), nullable=False)

    def __init__(self, first_name, last_name, event_id, id=''): 
        self.first_name = first_name 
        self.last_name = last_name 
        self.event_id = event_id
        self.id = self.set_id() 

    def __repr__(self):
        return f'Thank you for checking in.'

    def set_id(self):
        return str(uuid.uuid4())
