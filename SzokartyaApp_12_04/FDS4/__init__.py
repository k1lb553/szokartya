from flask_login import UserMixin
from flask_pymongo import PyMongo


class User(UserMixin):  # Create a User class for managing user sessions
    def __init__(self, user_id):  # every time the User() is called, the __init__ method runs
        self.id = user_id  # this makes sure the user_id is fresh


mongo = PyMongo()
