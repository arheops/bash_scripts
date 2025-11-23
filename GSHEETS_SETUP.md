# Google Sheets Upload Setup

## Prerequisites

Install required Python packages:
```bash
pip install gspread google-auth
```

## Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API
4. Create a Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "sheets-uploader")
   - Click "Create and Continue"
   - Skip granting roles (click Continue)
   - Click "Done"
5. Create credentials:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Download the file and save it as `credentials.json` in this directory
6. Note the service account email (looks like: `name@project-id.iam.gserviceaccount.com`)
7. Share your Google Spreadsheet with this service account email (give it Editor access)

## Usage

```bash
# Upload data to Google Sheets
./vultr_collect.sh | ./upload_to_gsheet.sh "Vultr Inventory" "Servers"

# Or from a file
cat data.tsv | ./upload_to_gsheet.sh "My Spreadsheet" "Sheet1"
```
