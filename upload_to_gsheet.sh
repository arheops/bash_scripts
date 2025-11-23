#!/bin/bash

# Usage: ./upload_to_gsheet.sh <spreadsheet_name> <tab_name>
# Example: cat data.tsv | ./upload_to_gsheet.sh "Vultr Inventory" "Servers"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <spreadsheet_name> <tab_name>"
    echo "Example: cat data.tsv | $0 \"My Sheet\" \"Sheet1\""
    exit 1
fi

SPREADSHEET_NAME="$1"
TAB_NAME="$2"

# Read stdin to temporary file
TEMP_FILE=$(mktemp)
cat > "$TEMP_FILE"

# Check if Python script exists
SCRIPT_DIR="$(dirname "$0")"
PYTHON_SCRIPT="$SCRIPT_DIR/upload_to_gsheet.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found"
    rm "$TEMP_FILE"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Upload using Python script
python3 "$PYTHON_SCRIPT" "$SPREADSHEET_NAME" "$TAB_NAME" < "$TEMP_FILE"
RESULT=$?

# Cleanup
rm "$TEMP_FILE"

if [ $RESULT -eq 0 ]; then
    echo "Data uploaded to spreadsheet: $SPREADSHEET_NAME, tab: $TAB_NAME"
else
    echo "Upload failed"
    exit 1
fi

