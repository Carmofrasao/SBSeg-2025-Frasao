#!/bin/sh
dnf install -y iptables
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.20.0.2:80
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -A FORWARD -p tcp -d 172.20.0.2 --dport 80 -j ACCEPT 
echo 1 > /proc/sys/net/ipv4/ip_forward
suricata -c /etc/suricata/suricata.yaml -q 0
