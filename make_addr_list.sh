#!/bin/bash

# Take hosts file and convert to addr_list preference line
# Usage: ./make_addr_list.sh [url] 

URL=${1:-"http://naboo:5000/hosts"}

ips=$(curl -s "$URL" \
    | grep -v '^#' \
    | awk '{print $1}' \
    | tr '\n' ' ' \
    | sed 's/ $//')

echo "org.phoebus.pv/default=ca" > "workspace.prefs"
echo "org.phoebus.pv.ca/addr_list=$ips" >> "workspace.prefs"
echo "org.phoebus.pv.sssca/auto_addr_list=true" >> "workspace.prefs"
