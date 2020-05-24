from flask import Flask
# change Config to TestConfig for tests 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from models import User
from flask_login import LoginManager
import os



app = Flask(__name__)
<<<<<<< HEAD
# change Config to TestConfig for tests 
=======
app._static_folder = os.getcwd() + '/app/static'
>>>>>>> 02cafe9adbee589f55def7dca7ef13661087cb8f
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view='login'
from app import routes, models
