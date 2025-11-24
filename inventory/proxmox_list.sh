#!/bin/bash

# Function to list containers and IPs on a specific node
list_containers() {
    local node=$1

    # Get list of running containers
    pct list | awk 'NR>1 && $2=="running" {print $1}' | while read vmid; do
        # Extract hostname from container config
        hostname=$(pct config "$vmid" | grep -oP 'hostname:\s*\K\S+' || echo "")
        
        # Extract IP address from container config
        ip=$(pct config "$vmid" | grep eth0 | grep -oP 'ip=\K[^,]+' | head -1 | cut -d'/' -f1)
        
        # Output in CSV format: ip, node:vmid, hostname, empty fields, ip
        echo "${ip},${node}:${vmid},${hostname},,,,,,,,,,,,${ip}"
    done
}

# If first argument is provided, run on that specific node
if [ -n "$1" ]; then
    # Run locally on the specified node
    list_containers "$1"
else
    # No argument provided - loop over all nodes
    # Get list of all nodes
    NODES=$(ls /etc/pve/nodes/)
    CURRENT_NODE=$(hostname)

    for node in $NODES; do
        if [ "$node" = "$CURRENT_NODE" ]; then
            # Run locally if it's the current node
            list_containers "$node"
        else
            # Copy script to remote node before executing
            scp -o ConnectTimeout=5 "$0" "${node}:~/bin/" > /dev/null 2>&1
            # SSH to remote node
            ssh -o ConnectTimeout=5 "$node" "~/bin/$(basename "$0")" "$node" 2>/dev/null
        fi
    done
fi