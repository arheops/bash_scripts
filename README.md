# Bash Scripts

## vultr_collect.sh

Collects and exports Vultr server inventory from multiple accounts.

### Description

This script retrieves both bare metal and virtual machine instances from all configured Vultr accounts and outputs them in CSV format. It automatically loops through all Vultr CLI configuration files (`~/.vultr-cli*.yaml`) and assigns unique prefixes to each account.

The script extracts API keys from config files and validates them before processing. For each account, it fetches account information (name and email) and appends this metadata to each server entry.

### Output Format

The script generates CSV output with the following columns:
- IP address
- Type (VLBM/VLVM for first account, V2BM/V2VM for second, etc.)
- Hostname/Label
- CPU count
- RAM
- Disk
- Instance ID
- MAC address (for bare metal, prefixed with `_`)
- Operating System
- Status
- Region
- Features
- Tags
- (empty columns)
- IP address (repeated)
- API Key Suffix (last 4 digits)
- Account Name
- Account Email

Each collection run starts with a header line showing the collection date, API key suffix, email, and account name.

### Usage

```bash
./vultr_collect.sh
```

Save to file:
```bash
./vultr_collect.sh > vultr_inventory.csv
```

Upload to Google Sheets:
```bash
./vultr_collect.sh | ./upload_to_gsheet.sh "Vultr Inventory" "Servers"
```

### Configuration

- API keys must be configured in `~/.vultr-cli*.yaml` files
- Each config file should contain a valid `api-key` entry
- Do not create a default `~/.vultr-cli.yaml` if using multiple accounts
- API keys shorter than 10 characters will be skipped with a warning

### Requirements

- `vultr-cli` installed and configured
- `jq` installed for JSON parsing

## upload_to_gsheet.sh

Uploads tab-separated data from stdin to Google Sheets.

### Setup

See [GSHEETS_SETUP.md](GSHEETS_SETUP.md) for detailed setup instructions.

### Usage

```bash
cat data.tsv | ./upload_to_gsheet.sh "Spreadsheet Name" "Tab Name"
```

### Requirements

- Python 3
- `gspread` and `google-auth` packages
- Google Cloud credentials.json file

