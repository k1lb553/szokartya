import pprint
from pymongo import MongoClient

##############################################password leak
connect_string = f"mongodb+srv://k1lb553cs:FsRgfiE4nNZ2yz6B@mongo-cluster1.rdhoq3g.mongodb.net/"
client = MongoClient(connect_string)
printer = pprint.PrettyPrinter()
db_szokartya = client.szokartya             #database
coll_deckek = db_szokartya.deckek           #collection a production db alatt


def parse_data(): #def parse_data(incoming_raw)
    incoming_data = {
	"sess_id": "qwx123",
	"button": "add_to_deck",
	"deck_id": "deck01",
	"lang_1_2": ["hu","ge"],
	"card_side_1_2": ["alma", "apple"],
	"knowledge_lvl": 2 }
    return incoming_data


def decide_def():
    inc_dict = parse_data()
    if inc_dict["button"] == "add_to_deck":
        
        print("ok")

decide_def()

 
def newcard(sess_id, ):
    coll_deckek.insert_one(incoming_data)
newcard()