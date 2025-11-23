# Bash Scripts

## vultr_collect.sh

Collects and exports Vultr server inventory from multiple accounts.

### Description

This script retrieves both bare metal and virtual machine instances from all configured Vultr accounts and outputs them in tab-separated format. It automatically loops through all Vultr CLI configuration files (`~/.vultr-cli*.yaml`) and assigns unique prefixes to each account.

### Output Format

The script generates tab-separated output with the following columns:
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
- IP address (repeated)

### Usage

```bash
./vultr_collect.sh
```

Save to file:
```bash
./vultr_collect.sh > vultr_inventory.tsv
```

Upload to Google Sheets:
```bash
./vultr_collect.sh | ./upload_to_gsheet.sh "Vultr Inventory" "Servers"
```

### Requirements

- `vultr-cli` installed
- `jq` installed
- Vultr API keys configured in `~/.vultr-cli*.yaml` files

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

