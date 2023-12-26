from flask import render_template, request, redirect, url_for, flash, Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from . import main_bp

from . import login_manager
from flask import Blueprint

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@main_bp.route('/')
def main_page():
    return render_template('index.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main_page'))

@main_bp.route('/login')
def login_page():
    return render_template('login.html')

@main_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    inc_password = request.form['password']

    users_coll = mongo.db.Users_coll

    existing_user = users_coll.find_one({'username': username})

    if existing_user:
        if check_password_hash(existing_user['password'], inc_password):
            user = User(existing_user['_id'])  #create a User (session ember cucc)
            login_user(user, remember=True)
            return redirect(url_for('my_cards'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@main_bp.route('/add_card')
@login_required
def addcard():
    return render_template("add_card.html")

@main_bp.route('/add_card', methods=['POST'])
@login_required
def add_card():
    if request.method == 'POST':
        field1 = request.form['field1']
        field2 = request.form['field2']

        user_id = current_user.get_id()
        print(user_id)

        cards_coll = mongo.db.Cards_coll
        cards_coll.insert_one({'user_id': user_id, 'field1': field1, 'field2': field2})

        flash('Card added successfully!', 'success')
        return redirect(url_for('my_cards'))

    return render_template('add_card.html')


@main_bp.route('/signup')
def signup_page():
    return render_template('signup.html')

@main_bp.route('/signup', methods=['POST'])
def signup():
    print("SIGNUP")
    username = request.form['username']
    inc_password = request.form['password']

    users_coll = mongo.db.Users_coll

    existing_user = users_coll.find_one({'username': username})

    if existing_user:
        print("EXISTING USER")
        flash('Username already exists. Please choose a different one.', 'error')
        return redirect(url_for('signup_page'))
    else:
        hashed_password = generate_password_hash(inc_password, method='pbkdf2:sha256')
        user_id = users_coll.insert_one({'username': username, 'password': hashed_password}).inserted_id
        user = User(user_id)  # Create a User object
        login_user(user, remember=True)
        flash('Account created successfully. You are logged in!', 'success')
        return redirect(url_for('my_cards'))


@main_bp.route('/my_cards')
@login_required
def my_cards():
    cards_coll = mongo.db.Cards_coll
    user_cards = mongo.db.Cards_coll.find({'user_id': current_user.get_id()})

    #print("User's Cards:")
    #for card in user_cards:
    #    print(f"Card ID: {card['_id']},Field 1: {card['field1']}, Field 2: {card['field2']}")

    return render_template('my_cards.html', user_cards=user_cards)

