from flask import Flask
import joblib
# For persistent storage 
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os

app = Flask(__name__)

# if "Testing" in os.environ:
#     app.config.from_envvar('TESTING')
#     print("Using configuration for TESTING.")
# elif "DEVELOPMENT" in os.environ:
#     app.config.from_envvar('DEVELOPMENT')
#     print("Using configuration for DEVELOPMENT.")
# else:
#     app.config.from_pyfile('config_test.cfg')
#     #app.config.from_pyfile('config_dply.cfg')

# Calling out heroku on app
#heroku = Heroku(app)

# Instantiate SQLAlchemy to handle db process
# joblib_file = "./application/static/Fetus_Predictus.pkl"
# ai_model = joblib.load(joblib_file)

# Importing routes.py as the final step
from application import routes