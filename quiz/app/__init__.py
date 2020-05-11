from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask_migrate import Migrate
from models import #add model names
=======
#from flask_migrate import Migrate
#from models import #add table names
>>>>>>> 62e37b597fcca98deba971da8f83c86392aefb0f

app = Flask(__name__)
app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app,db)
from app import routes
