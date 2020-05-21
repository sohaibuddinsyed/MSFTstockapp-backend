# Next, we have to initialize our app with all our configurations. 
# This is done in the app/__init__.py file. Note that if we set instance_relative_config to True, 
# we can use app.config.from_object('config') to load the config.py file.

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')