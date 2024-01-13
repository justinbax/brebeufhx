from pymongo import MongoClient

def get_database():

    MONGO_URI = "mongodb+srv://brebeufhx:brebeufhx@brebeufhx.pdpnnja.mongodb.net/"
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    
    return client["brebeufhx"]


dbname = get_database()
collection_name = dbname["tracks"]

# Insert into database

mail_1 = {
    "name": "John Smith",
    "address": "johnsmith@gmail.com",
    "sent_to": "abc@gmail.com",
    "status": "Not read",
    "desc": "Not read"
}
collection_name.insert_one(mail_1)


# Query and search the database
mails = collection_name.find()
for mail in mails:
    print(f"From {mail['name'] }: {mail['status']} ({mail['desc']})")