import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


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
    # Save the credentials for the next run
    with open("api/gmail/token.json", "w") as token:
      token.write(creds.to_json())

  service = None
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
  except HttpError as error:
    print(f"An error occurred: {error}")

  return service


def print_labels():
  try:
    service = get_google_api_connection()
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    print(f"An error occurred: {error}")