from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "oashd345ois4nfvk45lja45533snf34"
app.config["MONGO_URI"] = "mongodb+srv://k1lb553cs:FsRgfiE4nNZ2yz6B@mongo-cluster1.rdhoq3g.mongodb.net/"


mongodb_client = PyMongo(app)
db = mongodb_client.db


from application import routes


"""
from flask import Flask, request
from flask_mongoalchemy import MongoAlchemy
# MongoDB for FREE and get $25 in free credit using the code MKT-TIM: https://bit.ly/TechwTim1
import pprint
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGOALCHEMY_DATABASE"] = "mongo_flask_db"
app.config["MONGOALCHEMY_CONNECTION_STRING"] = "mongodb+srv://k1lb553cs:FsRgfiE4nNZ2yz6B@mongo-cluster1.rdhoq3g.mongodb.net/"
printer = pprint.PrettyPrinter()

db = MongoAlchemy(app)


class User(db.Document):
    name = db.StringField()
    passwd = db.StringField()


csaba = User(name="csbva", passwd="secret")
"""
