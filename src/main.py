#!/usr/bin/env python3
"""
Gmail to Google Sheets Automation
Fetches unread emails and logs them to Google Sheets
"""

import os
import sys
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gmail_service import GmailService
from src.sheets_service import SheetsService
from src.email_parser import EmailParser
import config


class EmailToSheetsAutomation:
    def __init__(self):
        print("=" * 50)
        print("Gmail to Google Sheets Automation")
        print("=" * 50)
        
        self.gmail = GmailService()
        self.sheets = SheetsService()
        self.parser = EmailParser()
        self.processed_count = 0
        self.skipped_count = 0

    def run(self):
        """Main execution flow"""
        print("\n📧 Fetching unread emails...")
        
        # Get unread emails from Gmail
        messages = self.gmail.get_unread_emails()
        
        if not messages:
            print("\n✓ No unread emails to process")
            return
        
        # Get existing emails from sheet to prevent duplicates
        print("\n📊 Checking existing emails in sheet...")
        existing_emails = self.sheets.get_existing_emails()
        print(f"Found {len(existing_emails)} existing email(s) in sheet")
        
        # Process each email
        new_emails = []
        processed_ids = []
        
        print("\n🔄 Processing emails...")
        for msg in messages:
            email_details = self.gmail.get_email_details(msg['id'])
            
            if email_details:
                # Parse email
                parsed = self.parser.parse_email(email_details)
                unique_key = self.parser.get_unique_key(parsed)
                
                # Check for duplicates
                if unique_key in existing_emails:
                    print(f"⊗ Skipping duplicate: {parsed['subject'][:50]}...")
                    self.skipped_count += 1
                else:
                    # Add to batch
                    row = self.parser.to_sheet_row(parsed)
                    new_emails.append(row)
                    processed_ids.append(msg['id'])
                    existing_emails.add(unique_key)  # Track to avoid dups in same run
                    
                    print(f"✓ Queued: {parsed['subject'][:50]}...")
                    self.processed_count += 1
        
        # Batch append to Google Sheets
        if new_emails:
            print(f"\n📝 Adding {len(new_emails)} new email(s) to Google Sheet...")
            success = self.sheets.append_emails_batch(new_emails)
            
            if success:
                # Mark emails as read
                print("\n📭 Marking emails as read...")
                for msg_id in processed_ids:
                    self.gmail.mark_as_read(msg_id)
                
                self.save_state()
        
        # Print summary
        self.print_summary()

    def save_state(self):
        """Save last processed timestamp for tracking"""
        with open(config.LAST_PROCESSED_FILE, 'w') as f:
            f.write(datetime.now().isoformat())

    def print_summary(self):
        """Print execution summary"""
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"✓ Processed: {self.processed_count} email(s)")
        print(f"⊗ Skipped (duplicates): {self.skipped_count} email(s)")
        print(f"✓ Total handled: {self.processed_count + self.skipped_count} email(s)")
        print("=" * 50)


def main():
    """Entry point"""
    try:
        automation = EmailToSheetsAutomation()
        automation.run()
        print("\n✅ Automation completed successfully!\n")
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure credentials.json is in the credentials/ folder")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()