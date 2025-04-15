#!/bin/bash
hping3 -c 100 -S -p 80 -i u20000 -a 172.20.1.3 172.20.1.2
