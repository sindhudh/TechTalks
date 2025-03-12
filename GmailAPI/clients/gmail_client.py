import os
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from clients.base_client import BaseEmailClient

from config import config

class GmailClient(BaseEmailClient):
    def __init__(self, token_file=os.getcwd() + "/config/token.json"):
        self.token_file = token_file
        self.service = self.authenticate()

    def authenticate(self):
        try:
            """Authenticate and return Gmail service."""
            print("Starting Authentication process with Gmail")
            SCOPES = config.get("scopes")
            creds = None
            current_directory = os.getcwd()
            if os.path.exists(current_directory + "/configs/token.json"):
                """If the token file exists, it will get access token from file and process the request"""
                creds = Credentials.from_authorized_user_file(current_directory + "/configs/token.json", SCOPES)

            if not creds or not creds.valid:
                """If the credentials are invalid or the token is expired, it will create new tokens and store them in token.json file"""
                flow = InstalledAppFlow.from_client_secrets_file(current_directory + "/configs/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                with open(current_directory + "/configs/token.json", "w") as token:
                    token.write(creds.to_json())
            print("Authentication Successful")
            return build("gmail", "v1", credentials=creds)
        except Exception as error:
            print(f"Exception in email authentication process\n Exception Message : {str(error)}")

    def fetch_emails(self, max_results=1):
        print("Started fetching emails")
        try:
            results = self.service.users().messages().list(userId="me", maxResults=config.get("max_results_email")).execute()
            messages = results.get("messages", [])
            email_data = []
            for msg in messages:
                outputs = {}
                msg_detail = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                headers = msg_detail["payload"]["headers"]
                outputs = {h["name"]: h["value"] for h in headers if h.get("name", "NA") in config.get("extract_from_headers")}
                outputs["id"] = msg["id"]
                outputs["message"] = msg_detail["snippet"]
                labels = ",".join(msg_detail["labelIds"])
                outputs["labels"] = labels
                email_data.append(outputs)
            return email_data
        except Exception as error:
            print(f"Exception in fetching emails from Gmail\n Exception Message:{str(error)}")

    def mark_as_read(self, email_ids):
        try:
            def callback(request_id, response, exception):
                if exception:
                    print(f"Error processing email {request_id}: {exception}")

            batch = self.service.new_batch_http_request(callback=callback)

            for email_id in email_ids:
                batch.add(self.service.users().messages().modify(
                    userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}
                ))

            batch.execute()
            print("Mark as read successful")
        except Exception as error:
            print(f"Exception in marking email as read\n Exception Message :{str(error)}")

    def move_email(self, email_folder_map):
        """
        Moves multiple emails to different folders efficiently using batch processing.

        :param email_folder_map: Dictionary {email_id: folder_name}
        """
        try:
            print("Moving emails to different folders")
            def callback(request_id, response, exception):
                if exception:
                    print(f"Error moving email {request_id}: {exception}")

            batch = self.service.new_batch_http_request(callback=callback)

            for email_id, folder_name in email_folder_map.items():
                batch.add(self.service.users().messages().modify(
                    userId="me", id=email_id, body={"addLabelIds": [folder_name]}
                ))
            batch.execute()
        except Exception as error:
            print(f"Exception in moving email\n Exception Message :{str(error)}")
