from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form) >>> "ImmutableMultiDict([('email', 'dagbs@gmail.com'), ('password', 'advb')])"
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #find the user with the maching email address

        if user:                #ha a bejövő emailcím matchel egyik adatbázisban lévővel, akkor létezik
            #print(user) >>> "<User 1>"

            if check_password_hash(user.password, password):    #ha a bejövő hash matchel a database-ban lévővel
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)                 #SESSION ID megjegyezése
                return redirect(url_for('views.home'))          #ha megvan a login, küldje a home page-re
            else:               #ha a bejövő hash NEM matchel a database-ban lévővel ==>incorrect password
                flash('Incorrect password, try again.', category='error')

        else:                   #ha a bejövő email NEM matchel egyikel sem, ami a database-ban van ==>incorrect password
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required #csak akkor logoutolhassunk, ha be vagyunk jelentkezve
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:                    #ha már foglalt az email cím, NE adhasson rá még egyet
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email       = email,
                            first_name  = first_name,
                            password    = generate_password_hash(password1, method='sha256'))
                            #amúgy nem a POST request küldése előtt kéne encryptolni??

            print(new_user)
            db.session.add(new_user)
            db.session.commit()                     #update database (new user created)
            login_user(new_user, remember=True)     # jelentkeztesse be a friss regisztráció adataiva

            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #a views fájlon belül a home funkcióhoz redirektál

    return render_template("sign_up.html", user=current_user)