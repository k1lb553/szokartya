from flask import Flask,Blueprint
from flask_pymongo import PyMongo
import pymongo
from flask_login import LoginManager


main_bp = Blueprint('main', __name__)
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cgpt_coll'
app.secret_key = '#'
mongo = PyMongo(app)
login_manager = LoginManager(app)
