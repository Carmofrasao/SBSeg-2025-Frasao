# SBSeg 2025

Repositório para dados relativos ao XXV Simpósio Brasileiro de Cibersegurança

## Maquina host utilizada

* CPU: AMD EPYC 7401 24-Core 2.0GHz
* RAM: 32 GB 
* SO: Debian GNU/Linux 12 (bookworm)

## Sistema utilizado (Ambiente 1)

Para simular o sistema utilizado nesse estudo, foi utilizado o sistema de contêineres Docker.

O sistema de reputação utilizado foi presente no Suricata (https://github.com/OISF/suricata) implementado em Docker (https://hub.docker.com/r/jasonish/suricata/).

Para simular um servidor web, foi utilizado uma imagem Nginx implementado em Docker (https://hub.docker.com/_/nginx).

Para simular as outras maquinas da rede, foi utilizado uma imagem Debian implementada em Docker (https://hub.docker.com/_/debian).

## Passo a passo para reproduzir o ataque (Ambiente 1)

* Todo o processo foi executado com a maquina principal (host) em modo root!

No diretorio `SBSeg-2025-Frasao/ambiente1`, execute o comando:

```bash
docker-compose up
```

Aguarde todas as maquinas inicializarem.

As configurações a serem executadas por esse comando estão no arquivo `SBSeg-2025-Frasao/ambiente/docker-compose.yml`

### Maquina suricata

Execute os seguintes comando:

```bash
docker exec -it suricata bash
cd /etc/suricata
source venv/bin/activate
python3 monitor.py
```

O arquivo monitor.py é utilizado para atualizar a reputação dos IPs mal intencionados que tentam atacar o servidor web.

### Maquina client

Execute os seguintes comando:

```bash
docker exec -it client bash
/home/config.sh
wget -qO- 172.20.1.2
```

O arquivo config.sh atualiza o sistema e baixa algumas ferramentas para o experimento.

O `wget` é para teste de funcionamento de rede (Recomendo executar esse comando durante todo o teste, em algum momento, ele vai parar de funcionar, o ataque funcionou!).

### Maquina attacker 

Execute os seguintes comando:

```bash
docker exec -it client bash
/home/config.sh
wget -qO- 172.20.1.2
/home/syn-flood.sh
```

`hping3`: É uma ferramenta de rede capaz de enviar pacotes ICMP/UDP/TCP personalizados e exibir as respostas do alvo. E foi utilizada no ataque de SYN Flood.

`-c`: Numero de pacotes enviados.

`-S`: Flag utilizada no ataque (SYN).

`-p`: Porta de destino.

`-i`: Taxa de envio (u100 = 1000 pacotes por segundo).

`-a`: Endereço de spoof.

Provalvelmente será necessario executar o `hping3` umas 40 vezes (na configuração atual do suricata.rules e monitor.py) até que o client seja bloqueado.

## Sistema utilizado (Ambiente 1)



## Passo a passo para reproduzir o ataque (Ambiente 1)



### Maquina fail2ban



### Maquina client



### Maquina attacker 


