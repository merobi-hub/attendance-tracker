# from oauth_var.oauth_var import GOOGLE_CLIENT_ID
from flask import Flask
from config import Config 
from .site.routes import site
from .authentication.routes import auth
from flask_migrate import Migrate
from attendance import models
from attendance.models import db as root_db, login_manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(Config)

# Passes in site to register_blueprint
app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
migrate = Migrate(app, root_db)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'





