from __future__ import print_function
import pickle
import base64
import json
import yaml
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


class MailSender():
    def __init__(self, my_mail_file):
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.mail_list = []
        with open(my_mail_file, "r") as f:
            self.my_mail = json.load(f)["myMail"]
        self.subject = "Among Us bonus"

    
    def return_message(self, to, message_text):
        message = MIMEText(message_text, "html")
        message['to'] = to
        message['from'] = self.my_mail
        message['subject'] = self.subject
        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    def return_text(self, name):
        text = f"""\
            <html>
            <body>
                <h2>Hello {name}</h2>
                <p> Send me your card number and CVC code to unlock new Among Us map</p>
                Best Regards,
                <br>
                Prince Of Kongo
            </body>
            </html>
        """
        return text

    def return_list_from_json(self, file_name):
        with open(file_name, "r") as f:
            self.mail_list = json.load(f)["data"]

    def return_list_from_yaml(self, file_name):
        with open(file_name, "r") as f:
            self.mail_list = yaml.load(f, Loader=yaml.FullLoader)["data"]

    def send_mail(self, to, message_text):
        message = self.return_message(to, message_text)
        response = (self.service.users().messages().send(userId='me', body=message).execute())
        return response
    
    def send_from_file(self, file_name):
        extension = file_name.split('.')[1].upper()
        if extension == "JSON":
            self.return_list_from_json(file_name)
        elif extension == "YAML":
            self.return_list_from_yaml(file_name)
        else:
            print("Extension not supported")
            return

        for m in self.mail_list:
            mail_text = self.return_text(m["name"])
            self.send_mail(m["email"], mail_text)


if __name__ == '__main__':
    try:
        ms = MailSender("mymail.json")
        #ms.send_from_file("mails.yaml")
    except:
        print("Something went wrong")