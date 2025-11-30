#!/usr/bin/bash
ssh root@gate -p 2323 -- \
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -o BatchMode=yes root@$1 -- \
 cat /etc/hostname