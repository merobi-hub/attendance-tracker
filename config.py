import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    # SECRET_KEY = os.environ['SECRET KEY'] or 'You will never guess...'
    # SQLALCHEMY_DATABASE_URI = os.environ['DEPLOY_DATABASE_URL'] or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_REDIRECT_URI = os.environ['GOOGLE_REDIRECT_URI']    

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')