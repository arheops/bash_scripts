#!/usr/bin/env python3
"""
Script to check server connectivity in a CSV inventory file.
Reads a CSV file with columns: hostname, ip, class, provider
Adds an 'action' column with values: 'OK', 'FAILED', or 'skipped'
"""

import sys
import os
import csv
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_ssh_connection(ip_address):
    """
    Test SSH connection to the given IP address.
    Returns tuple: (success, hostname)
    """
    # Validate IP address format
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(ip_pattern, ip_address)
    if not match:
        return False, 'invalid ip'
    
    # Validate each octet is between 0-255
    for octet in match.groups():
        if int(octet) > 255:
            return False, 'invalid ip'
    
    try:
        # SSH through gateway: first to us.pro-sip.net:2323, then to target IP
        # Use ProxyJump to tunnel through the gateway
        cmd = []
        TIMEOUT = 15
        script_dir = os.path.dirname(os.path.abspath(__file__))
        check_script = os.path.join(script_dir, "check_hostname.sh")
        result = subprocess.run(f"{check_script} {ip_address}", capture_output=True, timeout=TIMEOUT+5, shell=True, check=True)
        if result.returncode == 0:
            hostname = result.stdout.decode().strip()
            return True, hostname
        return False, ''
    except subprocess.TimeoutExpired as e:
        return False, ''
    except Exception as e:
        print(f"Error during SSH check: {e}")
        return False, ''


def process_csv(input_file):
    """
    Process the CSV file to test SSH connectivity.
    """
    # Read all entries from CSV
    entries = []
    
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            
            # Verify required columns exist
            if not all(col in reader.fieldnames for col in ['hostname', 'ip', 'class', 'provider']):
                print("Error: CSV file must contain columns: hostname, ip, class, provider")
                sys.exit(1)
            
            for row in reader:
                entries.append(row)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    # Check SSH connectivity for entries with valid IPs (skip empty IPs and class=X/x)
    entries_to_check = []
    for idx, entry in enumerate(entries):
        ip = entry.get('ip', '').strip()
        class_value = entry.get('class', '').strip().lower()
        
        # Skip entries with empty IP or class=X/x
        if not ip or class_value == 'x':
            entry['action'] = 'skipped'
            entry['new_hostname'] = ''
            continue
            
        entries_to_check.append((idx, entry))
    
    # Use ThreadPoolExecutor to check connections in parallel
    def check_entry(idx_entry):
        idx, entry = idx_entry
        ip = entry['ip']
        hostname = entry['hostname']
        
        success, new_hostname = check_ssh_connection(ip)
        return idx, success, new_hostname, hostname, ip
    
    # Execute checks in parallel with 10 threads
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_entry, idx_entry): idx_entry for idx_entry in entries_to_check}
        
        for future in as_completed(futures):
            idx, success, new_hostname, hostname, ip = future.result()
            
            print(f"Checking SSH connection to {hostname} ({ip})...", end=' ')
            if success:
                entries[idx]['action'] = 'OK'
                entries[idx]['new_hostname'] = new_hostname
                print("OK")
            else:
                entries[idx]['action'] = 'FAILED'
                entries[idx]['new_hostname'] = ''
                print("FAILED")
    
    # Write results back to CSV (or to stdout)
    fieldnames = ['hostname', 'ip', 'class', 'provider', 'action', 'new_hostname']
    
    # Write to stdout
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for entry in entries:
        writer.writerow(entry)


def main():
    if len(sys.argv) != 2:
        print("Usage: check_servers.py <csv_file>")
        print("CSV file must contain columns: hostname, ip, class, provider")
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_csv(input_file)


if __name__ == '__main__':
    check_ssh_connection("140.82.23.241")
    main()
