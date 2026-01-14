import os

SPREADSHEET_ID = '1q2YvfT3cfDA8YVziVPLHY40auq7_T16XOqpyGP7AFxs' 
RANGE_NAME = 'Email log'      
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'token.pickle'

LAST_PROCESSED_FILE = 'last_processed.txt'