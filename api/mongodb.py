from pymongo import MongoClient


def get_database():
    MONGO_URI = "mongodb+srv://brebeufhx:brebeufhx@brebeufhx.pdpnnja.mongodb.net/"
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    
    return client["brebeufhx"]


def get_mails(collection, filters):
    return collection.find(filters)


def push_mail(collection, mail):
    collection.insert_one(mail)

"""
dbname = get_database()
collection = dbname["tracks"]

mail_1 = {
    "name": "John Smith",
    "address": "johnsmith@gmail.com",
    "sent_to": "abc@gmail.com",
    "status": "Not read",
    "desc": "Not read"
}
collection.insert_one(mail_1)


# Query and search the database
mails = get_mails(collection, {})
for mail in mails:
    print(f"From {mail['name'] }: {mail['status']} ({mail['desc']})")

# Only search the database for mails sent to def@gmail.com
print("Sent to def@gmail.com:")
mails = get_mails(collection, {"sent_to": "def@gmail.com"})
for mail in mails:
    print(f"From {mail['name'] }: {mail['status']} ({mail['desc']})")
"""