from datetime import datetime

from flask import Flask, request, redirect, flash, render_template, url_for
from flask_pymongo import PyMongo
from flask_login import (
    logout_user,
    LoginManager,
    login_required,
    current_user,
    login_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

from  import User, mongo

login_manager = LoginManager(app)


############################################### DATABASE ############################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/cgpt_coll"
app.secret_key = (
    "hpAVBF572FOe6HLBsoZTxnapSNhO3L8T"  # Change this to a secure secret key
)
mongo.init_app(app)
users_coll = mongo.db.Users_coll
cards_coll = mongo.db.Cards_coll
############################################### VIEWS ############################################


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        print("AUTHED")
        return redirect(url_for("my_cards"))
    else:
        print("NOT AUTHED")
        return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main_page"))


@app.route("/add_card")
@login_required
def addcard():
    return render_template("add_card.html")


############################################### AUTH ############################################


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        inc_password = request.form["password"]

        existing_user = users_coll.find_one({"username": username})

        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("signup_page"))
        else:
            hashed_password = generate_password_hash(
                inc_password, method="pbkdf2:sha256"
            )
            user_id = users_coll.insert_one(
                {"username": username, "password": hashed_password}
            ).inserted_id
            user = User(user_id)  # Create a User object
            login_user(user, remember=True)
            flash("Account created successfully. You are logged in!", "success")
            return redirect(url_for("my_cards"))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        inc_password = request.form["password"]

        existing_user = users_coll.find_one({"username": username})

        if existing_user:
            if check_password_hash(existing_user["password"], inc_password):
                user = User(existing_user["_id"])  # create a User (session ember cucc)
                login_user(user, remember=True)
                return redirect(url_for("my_cards"))
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


############################################### CARD_MGM ############################################


@app.route("/add_card", methods=["POST"])
@login_required
def add_card():
    if request.method == "POST":
        field1 = request.form["field1"]
        field2 = request.form["field2"]
        user_id = current_user.get_id()
        add_date_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        cards_coll.insert_one(
            {
                "user_id": user_id,
                "field1": field1,
                "field2": field2,
                "add_date": add_date_utc,
            }
        )

        flash("Card added successfully!", "success")
        return redirect(url_for("my_cards"))
    return render_template("add_card.html")


@app.route("/my_cards")
@login_required
def my_cards():
    user_cards = mongo.db.Cards_coll.find({"user_id": current_user.get_id()})
    return render_template("my_cards.html", user_cards=user_cards)


######################################## OTHER STUFF ####################################################


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


if __name__ == "__main__":
    app.run(debug=True)
