#!/bin/bash

# Loop through all vultr-cli config files
counter=1
# vultr cli for some reason do not obey own docs and ignoring config flag when using global config file
# do not put DEFAULT config file if you expect more than one account
for config_file in ~/.vultr-cli*.yaml; do
  [ -f "$config_file" ] || continue
  
  # Extract API key from config file and export it
  VULTR_API_KEY=$(grep -oP '(?<=api-key: ).*' "$config_file" | tr -d ' ')
  
  # Check if API key is valid (at least 10 characters)
  if [ ${#VULTR_API_KEY} -lt 10 ]; then
    echo "Warning: Invalid or missing API key in $config_file (length: ${#VULTR_API_KEY}), skipping..." >&2
    continue
  fi
  
  export VULTR_API_KEY
  
  # Get last 4 digits of API key
  api_key_last4="${VULTR_API_KEY: -4}"
  
  # Get account info and parse NAME and EMAIL
  account_info=$(vultr-cli account info -o json 2>/dev/null)
  account_name=$(echo "$account_info" | jq -r '.account.name // ""')
  account_email=$(echo "$account_info" | jq -r '.account.email // ""')
  
  # Determine prefix based on counter
  if [ $counter -eq 1 ]; then
    bm_prefix="VLBM"
    vm_prefix="VLVM"
  else
    bm_prefix="V${counter}BM"
    vm_prefix="V${counter}VM"
  fi
  
  echo "Collection,`date`, AccountSuffix:$api_key_last4, Email, $account_email, Name, $account_name"
  # Bare Metal Servers
  vultr-cli bare-metal list --per-page 500 -o json 2>/dev/null | jq -r --arg prefix "$bm_prefix" '
    .bare_metals[]? |
    [
      .main_ip,
      $prefix,
      .label,
      .cpu_count,
      .ram,
      .disk,
      .id,
      ("_" + (.mac_address // "" | tostring)),
      .os,
      .status,
      .region,
      ((.features // []) | tostring),
      "",
      ((.tags // []) | tostring),
      "",
      "",
      "",
      .main_ip
    ] | @csv
  '
  
  # Virtual Instances
  vultr-cli instance list --per-page 500 -o json 2>/dev/null | jq -r --arg prefix "$vm_prefix" '
    .instances[]? |
    [
      .main_ip,
      $prefix,
      .label,
      .vcpu_count,
      (.ram | tostring + " MB"),
      (.disk | tostring + " GB"),
      .id,
      "",
      .os,
      .status,
      .region,
      ((.features // []) | tostring),
      "",
      ((.tags // []) | tostring),
      "",
      "",
      "",
      .main_ip
    ] | @csv
  '
  
  ((counter++))
done

# Unset the API key after the loop
unset VULTR_API_KEY
