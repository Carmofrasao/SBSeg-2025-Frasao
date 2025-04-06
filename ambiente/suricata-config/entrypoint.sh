#!/bin/sh
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -j NFQUEUE --queue-num 0
#iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables -I OUTPUT -j NFQUEUE --queue-num 0
# IPS
suricata -c /etc/suricata/suricata.yaml -q 0
# IDS
# suricata -c /etc/suricata/suricata.yaml -i br-eb94eaeaaf5a -v
