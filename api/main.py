from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from mongodb import get_database, get_mails, push_mail, update_mail, get_template, push_update_template, update_template
from openai_api import get_openai_client, get_feedback
from gmail.gmail import get_google_api_connection, search_messages_from, read_message, send_message
import re
import time
from counter import LAST_REFRESH

app = Flask(__name__)
CORS(app)

database = get_database()
openai_client = get_openai_client()
googleapi_client = get_google_api_connection()

LAST_REFRESH = 0

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

    # TODO add first_name and last_name special placeholders

    return result


def refresh_emails():
    global LAST_REFRESH
    if current_time < LAST_REFRESH + 5:
        return
    LAST_REFRESH = current_time


    tracked_emails = get_mails(database, {})
    for track in tracked_emails:
        messages = search_messages_from(googleapi_client, track["email"])
        if len(messages) == 0:
            continue
        recent_message = messages[0]
        message_contents = read_message(googleapi_client, recent_message)
        if message_contents["read"]:
            continue
        
        gpt_feedback = get_feedback(openai_client, message_contents["text"])

        modify_post_data = {
            "removeLabelIds": [
                "UNREAD"
            ]
        }
        googleapi_client.users().messages().modify(userId="me", id=recent_message["id"], body=modify_post_data).execute()

        update_query = {"_id": track["_id"]}
        new_values = {
            "status": ("RP" if gpt_feedback["positive"] == True else "RN"),
            "desc": gpt_feedback["analysis"]
        }

        update_mail(database, update_query, new_values)


@app.route("/send", methods=["POST"])
def send_email():
    post_data = request.get_json()
    if not ("recipients" in post_data and "own_email" in post_data and "type" in post_data):
        return {"status": "ER"}, 403

    template = get_template(database, {"type": post_data["type"]})
    if template == None:
        return {"status": "ER"}, 403
    template = template["template"]

    for recipient in post_data["recipients"]:
        text = fill_template(template, recipient["placeholders"], recipient["first_name"], recipient["last_name"])
        # TODO handle object of email
        send_message(googleapi_client, recipient["email"], "Test", text)
    
    return {"status": "SC"}


@app.route("/track", methods=["POST"])
def track_email():
    post_data = request.get_json()
    if not ("email" in post_data and "first_name" in post_data and "last_name" in post_data and "sent_to" in post_data):
        return {"status": "ER"}, 403

    push_mail(database, {
        "first_name": post_data["first_name"],
        "last_name": post_data["last_name"],
        "email": post_data["email"],
        "sent_to": post_data["sent_to"],
        "status": "NR",
        "desc": "No Reply"
    })

    update_emails()

    return {"status": "SC"}


@app.route("/template", methods=["POST", "GET"])
def template():
    if request.method == "POST":
        post_data = request.get_json()
        if not ("template" in post_data and "type" in post_data):
            return {"status": "ER"}, 403

        push_update_template(database, {
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
 
    refresh_emails()

    own_email = request.args.get("own_email")
    recipients = get_mails(database, {"sent_to": own_email})

    recipients = [r.get("email") for r in recipients] # TODO there is a better way with error handling

    return {"recipients": recipients}


@app.route("/getRecipient", methods=["GET"])
def get_recipient():
    if not ("recipient" in request.args):
        return {"status": "ER"}, 403
 
    refresh_emails()

    recipient = request.args.get("recipient")
    recipient = list(get_mails(database, {"email": recipient}))

    if len(recipient) == 0:
        return {"status": "ER"}, 403

    recipient = recipient[0]

    return {
        "first_name": recipient.get("first_name"),
        "last_name": recipient.get("last_name"),
        "status": recipient.get("status"),
        "desc": recipient.get("desc")
    }