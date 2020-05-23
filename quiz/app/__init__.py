from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from models import User
from flask_login import LoginManager
import os



app = Flask(__name__)
app._static_folder = os.getcwd() + '/app/static'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view='login'
from app import routes, models
