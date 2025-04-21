# SBSeg 2025

Repositório para dados relativos ao XXV Simpósio Brasileiro de Cibersegurança

## Estrutura do Repositório

```bash
├── ambiente
│   ├── attacker-config
│   │   ├── attacker-suricata.txt
│   │   ├── config.sh
│   │   ├── count.py
│   │   ├── syn-flood.py
│   │   └── syn-flood.sh
│   ├── client-config
│   │   ├── client-suricata.txt
│   │   ├── config.sh
│   │   ├── count.py
│   │   ├── rtt.txt
│   │   └── time.py
│   ├── docker-compose.yml
│   └── suricata-config
│       ├── classification.config
│       ├── count.py
│       ├── entrypoint.sh
│       ├── eve.json
│       ├── iprep
│       │   ├── categories.txt
│       │   └── reputation.list
│       ├── monitor.py
│       ├── reference.config
│       ├── rules
│       │   ├── script.lua
│       │   └── suricata.rules
│       ├── suricata-server.txt
│       ├── suricata.yaml
│       ├── threshold.config
│       └── update.yaml
└── README.md
```

## Maquina host utilizada

* CPU: AMD EPYC 7401 24-Core 2.0GHz
* RAM: 32 GB 
* Kernel: 6.12.13
* SO: Debian GNU/Linux 12 (bookworm)

## Sistema utilizado para reproduzir o ataque

Para simular o sistema utilizado nesse estudo, foi utilizado o sistema de contêineres Docker, versão 20.10.24.

O sistema de reputação utilizado foi presente no Suricata (https://github.com/OISF/suricata) implementado em Docker (https://hub.docker.com/r/jasonish/suricata/).

Para simular um servidor web, foi utilizado uma imagem Nginx implementado em Docker (https://hub.docker.com/_/nginx).

Para simular as outras maquinas da rede, foi utilizado uma imagem Debian implementada em Docker (https://hub.docker.com/_/debian).

## Passo a passo para reproduzir o ataque

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
