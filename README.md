# 📧 Gmail to Google Sheets Automation using Python

## 👩‍💻 Author
**Name:** Riya Garg

---

## 📖 Project Overview
This project is a Python-based automation system that connects to the Gmail API and Google Sheets API using OAuth 2.0 authentication. The system reads real unread emails from the user’s Gmail Inbox and logs each email into a Google Sheet automatically. After processing, emails are marked as read and duplicate entries are prevented.

---

## 🎯 Objective
Each qualifying email is appended as a new row in a Google Sheet with the following fields:

| Column Name | Description |
|------------|-------------|
| From | Sender email address |
| Subject | Email subject |
| Date | Date & time received |
| Content | Email body (plain text) |

---

## 🛠️ Technical Requirements

### Mandatory
- Language: Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0 authentication (Installed App Flow)
- Append only new emails
- No duplicate rows

### Email Scope
- Inbox
- Unread emails only
- Emails marked as read after processing

---

## 📂 Project Structure
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py       # Gmail API authentication & email fetching
│   ├── sheets_service.py      # Google Sheets API interaction
│   ├── email_parser.py        # Email content parsing logic
│   └── main.py                # Application entry point
│
├── credentials/
│   └── credentials.json       # OAuth credentials (DO NOT COMMIT)
│
├── proof/
│   ├── gmail_unread.png       # Screenshot of unread Gmail emails
│   ├── sheets_data.png        # Google Sheet populated with email data
│   └── oauth_consent.png      # OAuth consent screen
│
├── .gitignore
├── requirements.txt
├── README.md
└── config.py

##  High-Level Architecture
Gmail Inbox (Unread Emails)
        ↓
   Gmail API (OAuth 2.0)
        ↓
 Email Parser
 (From, Subject, Date, Body)
        ↓
 Duplicate Check + State Validation
        ↓
 Google Sheets API
        ↓
 Google Sheet (Append Rows)


---

## ⚙️ Functional Flow
1. Authenticate using Gmail OAuth 2.0
2. Fetch unread emails from Inbox
3. Parse sender, subject, date, and body
4. Append data to Google Sheets
5. Store last processed state
6. Mark emails as read
7. Prevent duplicate entries on re-run

---

## 🔁 State Management & Duplicate Prevention
State is stored in a local file.
