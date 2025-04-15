#!/bin/bash
hping3 -c 500 -S -p 80 -i u1000 -a 172.20.1.3 172.20.1.2
