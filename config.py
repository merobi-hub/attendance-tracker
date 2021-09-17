import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = os.environ.get('SECRET KEY') or 'You will never guess...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DATABASE_URL = os.environ.get('DATABASE_URL')
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')