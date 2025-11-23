#!/usr/bin/env python3
"""
Upload tab-separated data from stdin to Google Sheets
Requires: pip install gspread google-auth
"""

import sys
import csv
import gspread
from google.oauth2.service_account import Credentials

def upload_to_gsheet(spreadsheet_name, tab_name, data):
    """Upload data to Google Sheets"""
    
    # Define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    # Authenticate using service account credentials
    # You need to create credentials.json from Google Cloud Console
    try:
        creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(creds)
    except FileNotFoundError:
        print("Error: credentials.json not found", file=sys.stderr)
        print("\nTo set up Google Sheets API:", file=sys.stderr)
        print("1. Go to https://console.cloud.google.com/", file=sys.stderr)
        print("2. Create a new project or select existing", file=sys.stderr)
        print("3. Enable Google Sheets API", file=sys.stderr)
        print("4. Create Service Account credentials", file=sys.stderr)
        print("5. Download credentials.json to this directory", file=sys.stderr)
        print("6. Share your spreadsheet with the service account email", file=sys.stderr)
        return False
    
    try:
        # Open the spreadsheet
        try:
            spreadsheet = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            print(f"Creating new spreadsheet: {spreadsheet_name}", file=sys.stderr)
            spreadsheet = client.create(spreadsheet_name)
        
        # Get or create the worksheet
        try:
            worksheet = spreadsheet.worksheet(tab_name)
            # Clear existing data
            worksheet.clear()
        except gspread.WorksheetNotFound:
            print(f"Creating new worksheet: {tab_name}", file=sys.stderr)
            worksheet = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=20)
        
        # Upload data
        if data:
            worksheet.update('A1', data)
            print(f"Uploaded {len(data)} rows to {spreadsheet_name}/{tab_name}", file=sys.stderr)
        else:
            print("No data to upload", file=sys.stderr)
            return False
        
        return True
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 upload_to_gsheet.py <spreadsheet_name> <tab_name>", file=sys.stderr)
        sys.exit(1)
    
    spreadsheet_name = sys.argv[1]
    tab_name = sys.argv[2]
    
    # Read TSV data from stdin
    reader = csv.reader(sys.stdin, delimiter='\t')
    data = list(reader)
    
    if not data:
        print("Error: No data received from stdin", file=sys.stderr)
        sys.exit(1)
    
    # Upload to Google Sheets
    success = upload_to_gsheet(spreadsheet_name, tab_name, data)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
