# MongoDB for FREE and get $25 in free credit using the code MKT-TIM: https://bit.ly/TechwTim1
#from dotenv import load_env, find_dotenv
#load_env(find_dotenv())
#pw = os.environ.get("MONGODB_PWD")
import os
import pprint
from pymongo import MongoClient

##############################################password leak
connect_string = f"mongodb+srv://k1lb553cs:FsRgfiE4nNZ2yz6B@mongo-cluster1.rdhoq3g.mongodb.net/"
client = MongoClient(connect_string)
printer = pprint.PrettyPrinter()
dbs = client.list_database_names()

test_db = client.test
collections = test_db.coll


def insert_test_doc():
    collection = test_db.coll
    test_doc = {
        "name": "csaba",
        "type": "testdoc"}
    ins_id = collection.insert_one(test_doc).inserted_id
    print(ins_id)
#insert_test_doc()


production = client.production #mongodb automatikusan csinál egy production nevű databaset
person_coll = production.person_coll#mongodb automatikusan csinál egy person_coll nevű collectiont a production db alatt
def create_documents():#insertelni kell hogy valóban létrejöjjön a db, és a coll
    first_names = ["fneév1", "Pista","Csaba","János","fneév5"]
    last_names = ["lneév1", "Kis","Szekely","Nagy","lneév5"]
    kor = [12,33,33,45,56]
    docs = []
    for first_names, last_names, kor in zip(first_names, last_names, kor):
        doc = {"first_name": first_names,
               "last_name": last_names,
               "age": kor}
        docs.append(doc)
    person_coll.insert_many(docs)
#create_documents()


def find_all_people():
    people = person_coll.find()
    for person in people:
        printer.pprint(person)
#find_all_people()


def find_me():
    me = person_coll.find_one({"first_name": "Csaba", "last_name": "Szekely"})
    printer.pprint(me)
#find_me()


def count_documents_with_filter():
    count = person_coll.count_documents({"age": 33})
    print(count)
#count_documents_with_filter()


def get_person_by_id(str_person_id):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá
    person = person_coll.find_one({"_id":OI_person_id})
    printer.pprint(person)
#get_person_by_id("6563114bc6089f2cfd8d0ddd")


def show_specific_columns():
    columns = {"_id":0, "first_name":1, "age":1}
    people = person_coll.find({}, columns)
    for person in people:
        printer.pprint(person)
#show_specific_columns()


#__________________________________________________________

def update_person_by_id(str_person_id):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá
    """
    all_updates = {
        "$set": {"retardalt": True}, #set a (new or existing) field into a value we want
        "$inc": {"age": 1}, #növeli a számot eggyel (i++)
        "$rename": {"first_name" : "keresztnev", "last_name": "vezeteknev"} #a címeket átnevezi
        }
    person_coll.update_one({"_id":OI_person_id}, all_updates)"""
    person_coll.update_one({"_id": OI_person_id}, {"$unset":{"retardalt": ""}}) #törölje ki a retartdált mezőt
#update_person_by_id("65630f293363c18d21d4e1d7")



def replace_one(str_person_id):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá

    new_doc = {
        "first_name" : "új fname",
        "last_name" : "új lname",
        "kor": 333}
    person_coll.replace_one({"_id": OI_person_id}, new_doc)
#replace_one("65630f293363c18d21d4e1d7")


def delete_doc_by_id(str_person_id):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá
    person_coll.delete_many({"_id": OI_person_id})
#delete_doc_by_id("65630f293363c18d21d4e1d7")


#________________________________________________________________________________


address = {
    "_id":"65631113d0958600099ac928",
    "utca": "Betlehen Gábor utca",
    "város": "Budapest",
    "kód": 1871,
    "tud": True
} 


def add_address_embed(str_person_id, embed_data):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá
    person_coll.update_one({"_id": OI_person_id}, {"$addToSet": {"addresses": embed_data}})
#add_address_embed("65630f293363c18d21d4e1d9", address)


def add_address_relationship(str_person_id, embed_data):
    from bson.objectid import ObjectId
    OI_person_id = ObjectId(str_person_id) #a person_id-t konvertálja speciális formátummá (ObjectId)-vá

    #létehoz egy új "owner_id"-mezőt az embed dokumentumban,
    #amit egyenlővé tesz a str_person_id-vel
    embed_data["owner_id"] = str_person_id

    address_coll = production.address #új address nevű collection létrehozása a producion adatbázisban
    address_coll.insert_one(embed_data) 

#add_address_relationship("65631113d0958600099ac928", address)