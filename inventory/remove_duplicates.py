#!/usr/bin/env python3
"""

create script remove_duplicate. read csv provided as command lne arg columns hostname,ip,class,provider in memory.
 If all values are empty or ip column not looks like ip regexp - delete this column. search by ip. 
 If there are more then one column with ip, we should leave last one only, remove any others. put result as csv to stdin.
"""
import sys
import csv
import re

ip_re = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

# usage check
if len(sys.argv) != 2:
    sys.exit("usage: remove_duplicate input.csv")

path = sys.argv[1]

rows = []
with open(path, newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f)
    rows = list(rdr)

cleaned = []
for r in rows:
    h = (r.get("hostname") or "").strip()
    ip = (r.get("ip") or "").strip()
    c = (r.get("class") or "").strip()
    p = (r.get("provider") or "").strip()

    all_empty = not (h or ip or c or p)
    bad_ip = not ip_re.match(ip)

    if all_empty or bad_ip:
        continue

    cleaned.append({"hostname": h, "ip": ip, "class": c, "provider": p})

# dedupe by ip, keep last
keep = {}
for r in cleaned:
    keep[r["ip"]] = r

# output to stdout
w = csv.DictWriter(sys.stdout, fieldnames=["hostname", "ip", "class", "provider"])
w.writeheader()
for r in keep.values():
    w.writerow(r)