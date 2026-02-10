from datetime import datetime
from flask import Flask, request, redirect, flash, render_template, url_for
from flask_login import logout_user,LoginManager,login_required,current_user,login_user
from werkzeug.security import generate_password_hash, check_password_hash

from __init__ import *


############################################### DATABASE ############################################
app = Flask(__name__)
login_manager = LoginManager(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/SzokartyaApp12_04"
app.secret_key = "#"  # Change this to a secure secret key
mongo.init_app(app)
users_coll = mongo.db.Users_coll
cards_coll = mongo.db.Cards_coll
knowledges = ["0_unassigned","1_1day","2_2day","3_3day","4_1week","5_1month","6_3month","7_6month","8_done"]

############################################### CARD_MGM ############################################

@app.route("/query_me_daily", methods=["POST", "GET"]) #have to get query_me(weekly)  done, only POST will be required
@login_required
#IF USER CARDS == None: redirect to add cards
#user should be able to set the amount of cards they want to learn in a day
def query_me_daily():  
    user_id = current_user.get_id()
    columns = {"side1":1, "side2":1}
                    #only show current_user's cards     only show certein columns
    new_cards= cards_coll.find({"owner_id": user_id,"known_times": 0}, columns).limit(3)

    return render_template("query_me_daily.html", user_cards=new_cards)



@app.route("/query_me_custom", methods=["POST", "GET"]) #and GET??
@login_required
def query_me_custom():
    #if request.method == "POST":
    print("query_me_custom()")


@app.route("/add_card", methods=["POST", "GET"]) #and GET??
@login_required
def add_card():
    if request.method == "POST":
        user_id = current_user.get_id()
        side1 = request.form["side1"]
        side2 = request.form["side2"]
        decklabel = request.form["decklabel"]

        word_to_card(user_id,side1,side2,decklabel)
        flash("Card added successfully!", "success")

        return redirect(url_for("my_decks"))
    else:
        return render_template("add_card.html")
    

@app.route("/my_decks")
@login_required
def my_decks():
    user_id = current_user.get_id()
    user_decks = cards_coll.find({"owner_id": user_id})
    print(user_decks) #IF USER CARDS == None: redirect to add cards
    return render_template("my_decks.html", user_decks=user_decks)



############################################### AUTH ############################################
@app.route("/signup", methods=["POST", "GET"])
def signup():
    # only let non-logged-in users sign up 
    # MIGHT HAVE TO USE User CLASS INSEAD
    if not current_user.is_authenticated : 
        if request.method == "POST":
            username = request.form["username"]
            inc_password = request.form["password"]
            acc_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") #date of account creation
            acc_pic = "image123321.jpg"

            existing_user = users_coll.find_one({"username": username})

            if existing_user:
                flash("Username already exists. Please choose a different one.", "error")
                return redirect(url_for("signup_page"))
            else:
                hashed_password = generate_password_hash(inc_password, method="pbkdf2:sha256")
                user_id = users_coll.insert_one({"username": username,
                                                "password": hashed_password,
                                                "acc_date": acc_date,
                                                "acc_pic": acc_pic,
                                                "0_unknown": [],
                                                "1_1day":[],
                                                "2_2day":[],
                                                "3_3day":[],
                                                "4_1week":[],
                                                "5_1month":[],
                                                "6_3month":[],
                                                "7_6month":[],
                                                "8_done":[]
                                                }).inserted_id

                user = User(user_id)  # Create a User object
                login_user(user, remember=True)
                flash("Account created successfully. You are logged in!", "success")
                return redirect(url_for("my_decks"))
        else:
            return render_template("signup.html")
    else:
        return redirect(url_for("my_decks"))
    


@app.route("/login", methods=["POST", "GET"])
def login():
    if not current_user.is_authenticated : #only let non-logged-in users log in
        if request.method == "POST":
            username = request.form["username"]
            inc_password = request.form["password"]
            existing_user = users_coll.find_one({"username": username})

            if existing_user:
                flash("Username does not exist.", "error")

                if check_password_hash(existing_user["password"], inc_password):
                    flash("Incorrect password", "error")
                    user = User(existing_user["_id"])  # create a User (session ember)
                    login_user(user, remember=True)
                    return redirect(url_for("my_decks"))
                else:
                    return redirect(url_for("login"))
                
            else:
                return redirect(url_for("login"))
        else:
            return render_template("login.html")
    else:
        return redirect(url_for("my_decks"))


############################################### VIEWS ############################################
@app.route("/")
def main_page():
    if current_user.is_authenticated:
        print("AUTHED")
        return redirect(url_for("my_decks"))
    else:
        print("NOT AUTHED")
        return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main_page"))


######################################## STATIC FUNCTIONS ####################################################


def word_to_card(user_id, side1, side2, decklabel,
                 knowledge_lvl = 0,
                 # lvl_1_2=0, lvl_2_1=0,
                 known_date="", known_times=0,
                 not_known_date="", not_known_times=0,
                 creat_date_utc=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")):
    
    cards_coll.insert_one({
            "owner_id": user_id,
            "side1": side1,
            "side2": side2,
            "decklabel": decklabel,
            "knowledge_lvl": knowledge_lvl,
            # "lvl_1_2":lvl_1_2,
            # "lvl_2_1":lvl_2_1,
            "known_date":known_date,
            "known_times":known_times,
            "not_known_date":not_known_date,
            "not_known_times":not_known_times,
            "creat_date": creat_date_utc
        })
    update_user_decks(user_id,knowledge_lvl)


def csv_to_words(user_id, file_loc):
    with open(file_loc, encoding="UTF-8") as f:
        for sor in f:
            szo1, szo2 = sor.strip().split("-")
            decklabel = file_loc
            word_to_card(user_id,szo1,szo2,decklabel)
#csv_to_words("656e364f22fbe9f72336dc4b","tricks_gegen_kalt_szavak.txt")



from bson import ObjectId

def user_card_ids(user_id, lvl):
    #                          show cards from user       only cards with matching lvl
    user_cards = cards_coll.find({ "owner_id":user_id, "knowledge_lvl":lvl })
    card_ids = [card["_id"] for card in user_cards]
    return card_ids
    

def update_user_decks(user_id, lvl):
    #the function has to be called first, before transforming from ObjectId("asd123") to "asd123"
    card_ids = user_card_ids(user_id, lvl) 
    user_id = ObjectId(user_id)

    #                   update user's coll    add if doesnt exist already
    users_coll.update_one({"_id":user_id}, {"$set": {knowledges[lvl]: card_ids}})
    # here we have to remove the cards that are still in the deck they were before

update_user_decks("65735b278ba931a5d59cffc3", lvl=0)










######################################## OTHER STUFF ####################################################

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

if __name__ == "__main__":
    app.run(debug=True)
