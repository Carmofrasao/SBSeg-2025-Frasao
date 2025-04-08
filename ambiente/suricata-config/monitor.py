import pyinotify
import json
import os
import subprocess

log_file = '/etc/suricata/eve.json'
reputation_file = '/etc/suricata/iprep/reputation.list'

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        if event.pathname == log_file:
            with open(log_file, 'r') as f:
                for line in f:
                    pass
                event = json.loads(line)
                if 'alert' in event:
                    print(event)
                    src_ip = event['src_ip']
                    if src_ip:
                        update_reputation(src_ip)

def update_reputation(ip):
    if not os.path.exists(reputation_file):
        with open(reputation_file, 'w') as f:
            f.write(f"{ip},3,117\n")
    else:
        with open(reputation_file, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Caso onde o IP ja esta em reputation.list
                if line.startswith(ip):
                    # Para o GoodHost, quanto mais alta a reputação, melhor
                    # Para o GreyHost e BadHost, quanto mais alta a reputação, pior
                    new_category = int(line.split(",")[1])
                    new_reputation = int(line.split(",")[2])
                    # Caso onde a categoria é GoodHost
                    if new_category == 3:
                      # Caso onde a reputação esta baixa de mais, abaixa a categoria e reseta a reputação
                      if new_reputation < 10:
                        new_reputation = 10 
                        new_category = 2
                      # Caso onde a reputação ainda esta boa 
                      else:
                        new_reputation -= 10
                    # Caso onde a categoria é GreyHost
                    elif new_category == 2:
                      # Caso onde a reputação esta alta de mais, abaixa a categoria e reseta a reputação
                      if new_reputation > 100:
                        new_reputation = 10
                        new_category = 1
                      # Caso onde a reputação ainda esta boa 
                      else:
                        new_reputation += 10
                    # Caso onde a categoria é BadHost
                    elif new_category == 1:
                      # Caso onde a reputação ainda esta "boa" 
                      if new_reputation <= 100:
                        new_reputation += 10
                      # Depois disso, a regra de drop joga os pacotes fora! 

                    lines[i] = f"{ip},{new_category},{new_reputation}\n"
                    break
            else:
                lines.append(f"{ip},3,117\n")
            f.seek(0)
            f.writelines(lines)
    reload_suricata()

def reload_suricata():
    subprocess.run(['suricatasc', '-c', 'ruleset-reload-nonblocking'])

wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch(log_file, pyinotify.IN_MODIFY)

print(f"Monitorando {log_file} para atualizações...")
notifier.loop()
