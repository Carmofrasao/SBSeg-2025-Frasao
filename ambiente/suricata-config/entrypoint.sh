#!/bin/sh
echo 1 > /proc/sys/net/ipv4/ip_forward
#dnf install -y iptables-legacy iptables-nft libnetfilter_queue nftables
#update-alternatives --set iptables /usr/sbin/iptables-legacy
iptables -I FORWARD -j NFQUEUE --queue-num 0
iptables -t mangle -A PREROUTING -j NFQUEUE --queue-num 0
#iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables -I OUTPUT -j NFQUEUE --queue-num 0
suricata -c /etc/suricata/suricata.yaml -q 0
