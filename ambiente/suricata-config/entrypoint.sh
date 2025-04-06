#!/bin/sh
dnf check-update
dnf upgrade -y
dnf update -y
dnf install -y iptables-legacy iptables-nft libnetfilter_queue nftables
suricata -c /etc/suricata/suricata.yaml -q 0
#iptables -I FORWARD -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
iptables -I OUTPUT -j NFQUEUE --queue-num 0
