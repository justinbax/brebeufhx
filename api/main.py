from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/send", methods=["POST"])
def send_email():
    return

@app.route("/track", methods=["POST"])
def track_email():
    return

@app.route("/template", methods=["POST", "GET"])
def template():
    if flask.request.method == "POST":
        return
    elif flask.request.method == "GET":
        return

@app.route("/getListOfRecipients", methods=["GET"])
def get_list_of_recipients():
    return

@app.route("/getRecipient", methods=["GET"])
def get_recipient():
    return