#!/bin/bash

# Loop through all vultr-cli config files
counter=1
for config_file in ~/.vultr-cli*.yaml; do
  [ -f "$config_file" ] || continue
  
  # Determine prefix based on counter
  if [ $counter -eq 1 ]; then
    bm_prefix="VLBM"
    vm_prefix="VLVM"
  else
    bm_prefix="V${counter}BM"
    vm_prefix="V${counter}VM"
  fi
  
  # Bare Metal Servers
  vultr-cli bare-metal list --per-page 500 -o json --config "$config_file" 2>/dev/null | jq -r --arg prefix "$bm_prefix" '
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
    ] | @tsv
  '
  
  # Virtual Instances
  vultr-cli instance list --per-page 500 -o json --config "$config_file" 2>/dev/null | jq -r --arg prefix "$vm_prefix" '
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
    ] | @tsv
  '
  
  ((counter++))
done
