from flask import Flask
# change Config to TestConfig for tests 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from models import User
from flask_login import LoginManager


app = Flask(__name__)
# change Config to TestConfig for tests 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view='login'
from app import routes, models
