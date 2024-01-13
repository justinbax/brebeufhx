import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText

SCOPES = ["https://mail.google.com/"]
our_email = "cai.lucia04@gmail.com"

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


def search_messages_from(service, email):
    result = service.users().messages().list(userId='me',q=f"from:{email}").execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
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
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    message_text += text
            elif mimeType == "text/html":
                #print("This email has an HTML part")
                """
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
                """
            else:
                # attachment other than a plain text or HTML
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            #print("This email has an attachment")
                            """
                            # we get the attachment ID 
                            # and make another request to get the attachment itself
                            print("Saving the file:", filename, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                        .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))
                            """
    return message_text


def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            #if name.lower() == 'from':
                # we print the From address
                #print("From:", value)
            #if name.lower() == "to":
                # we print the To address
                #print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                #folder_name = clean(value)
                # we will also handle emails with the same subject name
                folder_counter = 0
                """
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    # we have the same folder name, add a number next to it
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject:", value)
                """
            #if name.lower() == "date":
                # we print the date when the message was sent
                #print("Date:", value)
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    message_text = parse_parts(service, parts, folder_name, message)
    return message_text


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




if __name__ == "__main__":
    # get emails that match the query you specify
    service = get_google_api_connection()
    results = search_messages_from(service, "justin.bax@icloud.com")
    # for each email matched, read it (output plain/text to console & save HTML and attachments)
    for msg in results:
        print(read_message(service, msg))
    
    # test send email
    send_message(service, "justin.bax@icloud.com", "This is a subject", 
        "This is the body of the email")