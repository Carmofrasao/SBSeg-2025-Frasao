from scapy.all import *
import time, sys, numpy

target = "172.20.1.2"
now = time.perf_counter() 
rtt = 0

for j in range(40):
  ss = []
  for i in range(5):
    ans = None
    start = time.time()
    try:
      while (not ans):
        ans = sr1(IP(dst=target)/TCP(dport=80), timeout=2, verbose=0)
    except KeyboardInterrupt:
      rtt = (time.time() - start) * 1000  # em ms
      ss.append(rtt)

      if ss:
        #sys.stdout.write(f"Tamanho: {len(ss)}\n")
        sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
        sys.stdout.write(f"RTT: {numpy.mean(ss):.2f}ms\n")
        exit(0)
      
    rtt = (time.time() - start) * 1000  # em ms
    ss.append(rtt)
  
  if ss:
    #sys.stdout.write(f"Tamanho: {len(ss)}\n")
    sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
    sys.stdout.write(f"RTT: {numpy.mean(ss):.2f}ms\n")
  else:
    sys.stdout.write("Sem resposta\n")
  if rtt/1000 < 10:
    time.sleep(10-(rtt/1000))
