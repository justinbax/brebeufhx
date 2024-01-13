from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from mongodb import get_database, get_mails, push_mail
from openai_api import get_openai_client, get_feedback
from gmail.gmail import get_google_api_connection, search_messages_from, read_message

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


@app.route("/send", methods=["POST"])
def send_email():
    post_data = request.get_json()
    if not ("recipients" in post_data and "own_email" in post_data and "template" in post_data):
        return Response(jsonify({"status": "ER"}), status=403)

    # TODO send email
    return

@app.route("/track", methods=["POST"])
def track_email():
    post_data = request.get_json()
    if not ("email" in post_data and "first_name" in post_data and "last_name" in post_data and "sent_to" in post_data):
        return Response(jsonify({"status": "ER"}), status=403)

    database["tracks"].insert_one({
        "first_name": post_data["first_name"],
        "last_name": post_data["last_name"],
        "email": post_data["email"],
        "sent_to": 
    })

    return

@app.route("/template", methods=["POST", "GET"])
def template():
    if flask.request.method == "POST":
        if not ("template" in post_data and "type" in post_data):
            return Response(jsonify({"status": "ER"}), status=403)
        return
    elif flask.request.method == "GET":
        if not ("type" in request.args):
            return Response(jsonify({"status": "ER"}), status=403)
 
        template_type = request.args.get("type")

        # TODO do stuff
        return

@app.route("/getListOfRecipients", methods=["GET"])
def get_list_of_recipients():
    if not ("recipients" in request.args):
        return Response(jsonify({"status": "ER"}), status=403)
 
    recipients = request.args.get("recipients")

    # TODO do stuff
    return

@app.route("/getRecipient", methods=["GET"])
def get_recipient():
    if not ("recipient" in request.args):
        return Response(jsonify({"status": "ER"}), status=403)
 
    recipients = request.args.get("recipient")

    # TODO do stuff
    return