import base64
from datetime import datetime
from email.mime.text import MIMEText
import re


class EmailParser:
    @staticmethod
    def parse_email(message):
        """Parse email message and extract relevant fields"""
        headers = message['payload']['headers']
        
        # Extract headers
        sender = EmailParser._get_header(headers, 'From')
        subject = EmailParser._get_header(headers, 'Subject')
        date = EmailParser._get_header(headers, 'Date')
        
        # Parse and format date
        formatted_date = EmailParser._format_date(date)
        
        # Extract email body
        body = EmailParser._get_body(message['payload'])
        
        # Clean body text
        cleaned_body = EmailParser._clean_text(body)
        
        return {
            'from': sender,
            'subject': subject,
            'date': formatted_date,
            'content': cleaned_body,
            'message_id': message['id']
        }

    @staticmethod
    def _get_header(headers, name):
        """Extract specific header value from email headers"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''

    @staticmethod
    def _get_body(payload):
        """Extract email body from payload"""
        body = ''
        
        if 'parts' in payload:
            # Multipart email
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    # Fallback to HTML if no plain text
                    if 'data' in part['body']:
                        html_body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        body = EmailParser._html_to_text(html_body)
        else:
            # Simple email
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')
        
        return body

    @staticmethod
    def _html_to_text(html):
        """Convert HTML to plain text (basic conversion)"""
        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', html)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        return text

    @staticmethod
    def _clean_text(text):
        """Clean and format text content"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        
        # Limit length to prevent overly long cells (optional)
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length] + '...'
        
        return text

    @staticmethod
    def _format_date(date_string):
        """Format date string to readable format"""
        try:
            # Parse common email date formats
            # Example: "Wed, 15 Jan 2025 10:30:00 +0000"
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_string)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            # If parsing fails, return original
            return date_string

    @staticmethod
    def to_sheet_row(parsed_email):
        """Convert parsed email to Google Sheets row format"""
        return [
            parsed_email['from'],
            parsed_email['subject'],
            parsed_email['date'],
            parsed_email['content']
        ]

    @staticmethod
    def get_unique_key(parsed_email):
        """Generate unique key for duplicate detection"""
        return f"{parsed_email['from']}||{parsed_email['subject']}"