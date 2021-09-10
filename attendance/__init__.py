from flask import Flask
from config import Config
from .site.routes import site

app = Flask(__name__)

app.config.from_object(Config)

# Passes in site to register_blueprint
app.register_blueprint(site)

