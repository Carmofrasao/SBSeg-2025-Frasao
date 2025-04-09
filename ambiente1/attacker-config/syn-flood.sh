#!/bin/bash
hping3 -c 5000 -S -p 80 -i u100 -a 172.20.1.3 172.20.1.2
