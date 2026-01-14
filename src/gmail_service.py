import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config


class GmailService:
    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        creds = None
        
        # Load existing token if available
        if os.path.exists(config.TOKEN_FILE):
            with open(config.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, 
                    config.GMAIL_SCOPES + config.SHEETS_SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future runs
            with open(config.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✓ Gmail API authenticated successfully")

    def get_unread_emails(self, max_results=100):
        """Fetch unread emails from inbox"""
        try:
            # Query for unread emails in inbox
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread in:inbox',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("No unread emails found.")
                return []
            
            print(f"Found {len(messages)} unread email(s)")
            return messages
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_email_details(self, msg_id):
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            return message
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def mark_as_read(self, msg_id):
        """Mark an email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            return True
        
        except HttpError as error:
            print(f'Error marking email as read: {error}')
            return False