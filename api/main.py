from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from mongodb import get_database, get_mails, push_mail, get_template, push_template
from openai_api import get_openai_client, get_feedback
from gmail.gmail import get_google_api_connection, search_messages_from, read_message
import re

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

database = get_database()
openai_client = get_openai_client()
googleapi_client = get_google_api_connection()


class Recipient:
    def __init__(self, first_name, last_name, email, placeholders):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.placeholders = placeholders
    
    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'placeholders': self.placeholders
        }


def fill_template(template, placeholders, first_name, last_name):
    result = template
    iters = re.finditer(r"<<(.*?)>>", template)
    iters_list = []
    for i in iters:
        iters_list.insert(0, i)

    for i in iters_list:
        key = template[i.start() + 2 : i.end() - 2]
        if not key in placeholders:
            continue
        result = result[0 : i.start()] + placeholders[key] + result[i.end() : len(result)]

    return result

print(fill_template("Hello <<Abcdef>> i am <<good>> bye", {
    "Abcdef": "my dear",
    "good": "bad"
}, "a", "b"))


@app.route("/send", methods=["POST"])
def send_email():
    post_data = request.get_json()
    if not ("recipients" in post_data and "own_email" in post_data and "template" in post_data):
        return {"status": "ER"}, 403



    # TODO send email
    return


@app.route("/track", methods=["POST"])
def track_email():
    post_data = request.get_json()
    if not ("email" in post_data and "first_name" in post_data and "last_name" in post_data and "sent_to" in post_data):
        return {"status": "ER"}, 403

    push_mail(database, {
        "first_name": post_data["first_name"],
        "last_name": post_data["last_name"],
        "email": post_data["email"],
        "sent_to": post_data["send_to"],
        "status": "NR",
        "desc": "No Reply"
    })

    # TODO maybe check immediately if there's an answer and analyze it & change status/desc
    return {"status": "SC"}


@app.route("/template", methods=["POST", "GET"])
def template():
    if request.method == "POST":
        if not ("template" in post_data and "type" in post_data):
            return {"status": "ER"}, 403
        # TODO this adds a new template, it doesn't modify it
        push_template(database, {
            "template": post_data["template"],
            "type": post_data["type"]
        })
        
        return {"status": "SC"}
    
    elif request.method == "GET":
        if not ("type" in request.args):
            return {"status": "ER"}, 403
 
        template_type = request.args.get("type")
        matches = get_template(database, {"type": template_type})
        if matches == None:
            return {"status": "ER"}, 403

        match_template = matches.get("template")

        return {"template": match_template}


@app.route("/getListOfRecipients", methods=["GET"])
def get_list_of_recipients():
    if not ("own_email" in request.args):
        return {"status": "ER"}, 403
 
    own_email = request.args.get("own_email")
    recipients = get_mails(database, {"sent_to": own_email})
    if len(recipients) == 0:
        return {"status": "ER"}, 403

    recipients = [r.get("email") for r in recipients] # TODO there is a better way with error handling

    return {"recipients": recipients}


@app.route("/getRecipient", methods=["GET"])
def get_recipient():
    if not ("recipient" in request.args):
        return {"status": "ER"}, 403
 
    recipient = request.args.get("recipient")
    recipient = get_mails(database, {"email": recipient})

    if len(recipient) == 0:
        return {"status": "ER"}, 403
    elif len(recipient) > 1:
        print("More than one recipient match found. Deal with that.")

    recipient = recipient[0]
    return {
        "first_name": recipient.get("first_name"),
        "last_name": recipient.get("last_name"),
        "status": recipient.get("status"),
        "desc": recipient.get("desc")
    }