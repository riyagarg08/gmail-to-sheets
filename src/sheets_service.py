import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import config


class SheetsService:
    def __init__(self):
        self.service = None
        self.authenticate()

    # def authenticate(self):
    #     """Authenticate with Google Sheets API using existing OAuth token"""
    #     creds = None
        
    #     # Load existing token (should be created by GmailService)
    #     if os.path.exists(config.TOKEN_FILE):
    #         with open(config.TOKEN_FILE, 'rb') as token:
    #             creds = pickle.load(token)
        
    #     if not creds or not creds.valid:
    #         if creds and creds.expired and creds.refresh_token:
    #             creds.refresh(Request())
    #             # Save refreshed token
    #             with open(config.TOKEN_FILE, 'wb') as token:
    #                 pickle.dump(creds, token)
        
    #     self.service = build('sheets', 'v4', credentials=creds)
    #     print("✓ Google Sheets API authenticated successfully")
    def authenticate(self):
        creds = None

        if os.path.exists(config.TOKEN_FILE):
            with open(config.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    config.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(config.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
        print("✓ Google Sheets API authenticated successfully")
      

    def get_existing_emails(self):
        """Retrieve all existing email IDs from the sheet to prevent duplicates"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=config.SPREADSHEET_ID,
                range=config.RANGE_NAME
            ).execute()
            
            values = result.get('values', [])
            
            # Skip header row and extract 'From' column (used as unique identifier)
            if len(values) > 1:
                existing_emails = set()
                for row in values[1:]:  # Skip header
                    if row:  # Check if row has data
                        # Store combination of sender and subject as unique key
                        if len(row) >= 2:
                            unique_key = f"{row[0]}||{row[1]}"  # From||Subject
                            existing_emails.add(unique_key)
                return existing_emails
            
            return set()
        
        except HttpError as error:
            print(f'An error occurred while reading sheet: {error}')
            return set()

    def append_email(self, email_data):
        """Append a single email to the Google Sheet"""
        try:
            body = {
                'values': [email_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range=config.RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
        
        except HttpError as error:
            print(f'An error occurred while appending to sheet: {error}')
            return False

    def append_emails_batch(self, email_list):
        """Append multiple emails to the Google Sheet in one request"""
        if not email_list:
            print("No emails to append")
            return True
        
        try:
            body = {
                'values': email_list
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range=config.RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✓ Added {len(email_list)} email(s) to Google Sheet")
            return True
        
        except HttpError as error:
            print(f'An error occurred while batch appending: {error}')
            return False