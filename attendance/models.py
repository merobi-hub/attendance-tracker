from flask_sqlalchemy import SQLAlchemy
import uuid 
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager 

db = SQLAlchemy() 
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    print('loading User')
    return User.query.get(id)


class User(db.Model, UserMixin):
    name = db.Column(db.String)
    email = db.Column(db.String(80), nullable=False, unique=True)
    profile_pic = db.Column(db.String)
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, default='')
    

    def __init__(self, name, email, profile_pic, id='', password=''):
        self.name = name 
        self.email = email 
        self.profile_pic = profile_pic
        self.id = self.set_id()
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
    passkey = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(
        self,
        title,
        host,
        day,
        time,
        duration,
        other,
        passkey,
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
        self.passkey = passkey
        self.user_id = user_id  

    def __repr__(self):
        return f'{self.title}\n{self.host}\n{self.day}\n{self.time}\n{self.duration}\n{self.other}'

    def set_id(self):
        return str(uuid.uuid4())

class Participant(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(80), unique=True)
    event_id = db.Column(db.String, db.ForeignKey('event.id'), nullable=False)

    def __init__(self, first_name, last_name, email, event_id, id=''): 
        self.first_name = first_name 
        self.last_name = last_name
        self.email = email 
        self.event_id = event_id
        self.id = self.set_id() 

    def __repr__(self):
        return f'Thank you for checking in.'

    def set_id(self):
        return str(uuid.uuid4())
