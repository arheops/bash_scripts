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

## inventory/proxmox_list.sh

Lists Proxmox containers across all nodes with their IP addresses.

### Description

This script queries Proxmox nodes to collect information about running containers (LXC). It can run locally on a single node or distribute execution across all nodes in the cluster via SSH.

The script automatically detects the Proxmox cluster nodes by reading `/etc/pve/nodes/` and can execute remotely on each node while running locally on the current node to avoid unnecessary SSH overhead.

### Output Format

The script generates CSV output with the following columns:
- IP address
- Node:VMID (e.g., pve22:2104)
- Hostname
- Empty fields (for compatibility with other inventory formats)
- IP address (repeated)

### Usage

Run on local node only:
```bash
./proxmox_list.sh pve22
```

Run on all nodes in cluster:
```bash
./proxmox_list.sh
```

Save to file:
```bash
./proxmox_list.sh > proxmox_inventory.csv
```

### Features

- Automatic cluster node detection from `/etc/pve/nodes/`
- Local execution when hostname matches node name (no SSH overhead)
- Remote execution via SSH with 5-second connection timeout
- Automatic script distribution to remote nodes (`~/bin/` directory)
- Only lists running containers
- Extracts IP addresses from `eth0` interface configuration
- Suppresses diagnostic output for clean CSV generation

### Requirements

- Proxmox VE cluster
- SSH access configured between cluster nodes
- `pct` command available on all nodes
- `~/bin/` directory on remote nodes (created automatically if needed)

### Configuration

The script uses these Proxmox commands:
- `pct list` - to enumerate containers
- `pct config <vmid>` - to extract hostname and IP configuration

SSH options used:
- `ConnectTimeout=5` - 5-second timeout for connections


