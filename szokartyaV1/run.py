from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cgpt_coll'
app.secret_key = '#'
mongo = PyMongo(app)
login_manager = LoginManager(app)

from app.main import main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
