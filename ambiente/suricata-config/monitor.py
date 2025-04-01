import pyinotify
import json
import os
import subprocess

log_file = '/etc/suricata/eve.json'
reputation_file = '/etc/suricata/iprep/reputation.list'
categories = {
    'BadHosts': (1, 40),
    'GoodHosts': (2, 100)
    'Brute Force Attack': (3, 20),
    'Port Scan': (4, 60),
    'Malware Distribution': (5, 5),
}

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
    category_id, reputation_score = categorize_alert(alert_msg)
    if not os.path.exists(reputation_file):
        with open(reputation_file, 'w') as f:
            f.write(f"{ip},{category_id},{reputation_score}\n")
    else:
        with open(reputation_file, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(ip):
                    lines[i] = f"{ip},{category_id},{reputation_score}\n"
                    break
            else:
                lines.append(f"{ip},{category_id},{reputation_score}\n")
            f.seek(0)
            f.writelines(lines)
    reload_suricata()

def categorize_alert(alert_msg):
    for key, (cat_id, score) in categories.items():
        if key.lower() in alert_msg.lower():
            return cat_id, score
    return 0, 50

def reload_suricata():
    subprocess.run(['kill', '-USR2', str(os.getpid())])
    # suricatasc -c "reload-rules"

wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch(log_file, pyinotify.IN_MODIFY)

print(f"Monitorando {log_file} para atualizações...")
notifier.loop()
