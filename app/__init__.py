from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth

from config import app_config

db = SQLAlchemy()
from app.routes import (api as api_blueprint, UserRoute, CompanyRoute, WaitingLineRoute, CustomerRoute, LineUpRoute)

# IMPORTING YOUR MODELS
from app.models import (User, Company, Customer, WaitingLine, LineUp, Config, CompanyConfig)

auth = HTTPBasicAuth()

def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True)
    app.register_blueprint(api_blueprint)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    return app