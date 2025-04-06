import pyinotify
import json
import os
import subprocess

log_file = '/etc/suricata/eve.json'
reputation_file = '/etc/suricata/iprep/reputation.list'
categories = {
    'BadHosts': 1,
    'GreyHosts': 2,
    'GoodHosts': 3,
}
seen_ips = {}

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        if event.pathname == log_file:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if 'alert' in event:
                            src_ip = event['src_ip']
                            alert_msg = event['alert'].get('signature')
                            if src_ip and alert_msg:
                                update_reputation(src_ip, alert_msg)
                    except json.JSONDecodeError:
                        continue

def update_reputation(ip, alert_msg):
    if not os.path.exists(reputation_file):
        with open(reputation_file, 'w') as f:
            f.write(f"{ip},3,90\n")
    else:
        with open(reputation_file, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Caso onde o IP ja esta em reputation.list
                if line.startswith(ip):
                    new_reputation = int(line.strip(",")[2])
                    if new_reputation > 0:
                        new_reputation -= 10
                     
                    new_category = int(line.strip(",")[1])
                    if new_reputation < 70:
                        new_category = 2
                    elif new_reputation < 30:
                        new_category = 1
                        
                    lines[i] = f"{ip},{new_category},{new_reputation}\n"
                    break
            else:
                lines.append(f"{ip},3,90\n")
            f.seek(0)
            f.writelines(lines)
    reload_suricata()

def reload_suricata():
    subprocess.run(['suricatasc', '-c', 'ruleset-reload-nonblocking'])
    # suricatasc -c "reload-rules"

wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch(log_file, pyinotify.IN_MODIFY)

print(f"Monitorando {log_file} para atualizações...")
notifier.loop()
