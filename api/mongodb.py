from pymongo import MongoClient
import os


def get_database():
    db_username = os.environ.get("MONGODB_ATLAS_USERNAME")
    db_passwd = os.environ.get("MONGODB_ATLAS_PASSWD")
    MONGO_URI = f"mongodb+srv://{db_username}:{db_passwd}@brebeufhx.pdpnnja.mongodb.net/"
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        return None
    
    return client["brebeufhx"]


def get_mails(database, filters):
    return database["tracks"].find(filters)


def push_mail(database, mail):
    database["tracks"].insert_one(mail)


def update_mail(database, filters, new_values):
    database["tracks"].update_one(filters, {"$set": new_values})


def get_template(database, filters):
    return database["templates"].find_one(filters)


def push_update_template(database, template):
    if get_template(database, {"type": template["type"]}) == None:
        database["templates"].insert_one(template)
    else:
        update_query = {"type": template["type"]}
        new_values = {"template": template["template"]}
        update_template(database, update_query, new_values)


def update_template(database, filters, new_values):
    database["templates"].update_one(filters, {"$set": new_values})