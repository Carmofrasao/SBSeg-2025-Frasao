# Cordeiro em Pele de Lobo: Desvelando a Negação de Serviço Baseada em Envenenamento de Reputação

Resumo. Sistemas de reputação são utilizados para medir a confiabilidade de usuários, dispositivos e serviços em ambientes digitais. Apesar de seu auxílio na segurança e tomada de decisão, identificando interações maliciosas, esses sistemas estão sujeitos a manipulações que podem comprometer sua integridade. Esse trabalho propõe e valida um novo vetor de ataque que explora sistemas de reputação para realizar negação de serviço contra usuários legítimos. O ataque consiste em um agente malicioso que se passa pela vítima, executa ações ofensivas e induz sistemas automatizados a penalizá-la com base em sua reputação. A estratégia explora falhas na verificação de identidade em mecanismos de confiança baseados em comportamento. Para demonstrar essa estratégia, um experimento foi conduzido em ambiente Docker com Nginx e Suricata para simular e observar o impacto da personificação e deterioração de credibilidade. Partindo desse ambiente, o atacante, uma máquina integrada a mesma rede, utilizando a ferramenta hping3, em apenas 3 minutos conseguiu fazer o bloqueio do usuário legítima, utilizando um ataque SYN-flood com personificação sobre o usuário legítimo. Demonstrando a viabilidade do ataque e a necessidade de contramedidas para mitigar esse tipo de ameaça.

Esse artefato tem como objetivo demonstrar a viabilidade em reproduzir o o ataque de negação de serviço a partir da deterioração de reputação.

## Estrutura do README.md

* [Título projeto](#cordeiro-em-pele-de-lobo-desvelando-a-negação-de-serviço-baseada-em-envenenamento-de-reputação)
* [Estrutura do readme.md](#estrutura-do-readmemd)
  * [Estrutura do Repositório](#estrutura-do-repositório)
* [Selos Considerados](#selos-considerados)
* [Informações básicas](#informações-básicas)
* [Dependências](#dependências)
* [Preocupações com segurança](#preocupações-com-segurança)
* [Instalação](#instalação)
* [Teste mínimo](#teste-mínimo)
* [Experimentos](#experimentos)
  * [Reivindicação #1](#reivindicações-#1)
* [LICENSE](#licence)

### Estrutura do Repositório

* ambiente

Contém todos os arquivos de configuração para os testes.
  * attacker-config/
    - Arquivo de configuração do atacante;
    - Arquivos usados para a execução do ataque;
    - Arquivo para coletar metricas de resultado;
    - Arquivo de resultados.
  * client-config/
    - Arquivo de configuração do cliente;
    - Arquivos para coletar metricas de resultado;
    - Arquivos de resultados.
  * suricata-config/
    * iprep/
      - Arquivos para a configuração de reputação do Suricata. 
    * rules/
      - Arquivos para a configuração de regras do Suricata.
    - Arquivos de configuração do Suricata; 
    - Arquivos para coletar metricas de resultado;
    - Arquivos de resultados.
  * docker-compose.yml
    - Arquivo de configuração do ambiente.

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
