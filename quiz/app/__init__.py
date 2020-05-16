from flask import Flask
from config import Config
#from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from flask_migrate import Migrate
#from models import User, Question, QuestionAnswer, Answer


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
#db = SQLAlchemy(app)
#migrate = Migrate(app,db)
from app import routes
