#!/bin/sh
apt update -y
apt install -y wget iproute2 iputils-ping python3 python3-venv
#ip route replace default via 172.20.1.2 dev eth0
