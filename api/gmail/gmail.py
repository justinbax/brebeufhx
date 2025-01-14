import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText

SCOPES = ["https://mail.google.com/"]
our_email = "lucasoliver3141@gmail.com"

def get_google_api_connection():
  creds = None

  if os.path.exists("api/gmail/token.json"):
    creds = Credentials.from_authorized_user_file("api/gmail/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "api/gmail/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    
    # Save credentials
    with open("api/gmail/token.json", "w") as token:
      token.write(creds.to_json())

  service = None
  try:
    service = build("gmail", "v1", credentials=creds)
  except HttpError as error:
    print(f"An error occurred: {error}")

  return service


def get_email_address(service):
    return ""


def search_messages_from(service, email):
    result = service.users().messages().list(userId='me',q=f"from:{email}").execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=f"from:{email}", pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def parse_parts(service, parts, folder_name, message):
    message_text = ""
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")

            if part.get("parts"):
                parse_parts(service, part.get("parts"), folder_name, message)

            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    message_text += text
            elif mimeType == "text/html":
                # TODO handle this
                print("email has HTML part")
            else:
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")

    return message_text


def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    
    labelIds = msg["labelIds"]
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            #if name.lower() == 'from':
                # we print the From address
                #print("From:", value)
            #if name.lower() == "to":
                # we print the To address
                #print("To:", value)
            #if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                #has_subject = True
    message_text = parse_parts(service, parts, folder_name, message)
    return {"text": message_text, "read": not ("UNREAD" in labelIds)}


def build_message(destination, obj, body):
    message = MIMEText(body)
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = obj
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, destination, obj, body):
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, obj, body)
    ).execute()