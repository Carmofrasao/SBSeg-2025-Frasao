# Cordeiro em Pele de Lobo: Desvelando a Negação de Serviço Baseada em Envenenamento de Reputação

Resumo. Sistemas de reputação são utilizados para medir a confiabilidade de usuários, dispositivos e serviços em ambientes digitais. Apesar de seu auxílio na segurança e tomada de decisão, identificando interações maliciosas, esses sistemas estão sujeitos a manipulações que podem comprometer sua integridade. Esse trabalho propõe e valida um novo vetor de ataque que explora sistemas de reputação para realizar negação de serviço contra usuários legítimos. O ataque consiste em um agente malicioso que se passa pela vítima, executa ações ofensivas e induz sistemas automatizados a penalizá-la com base em sua reputação. A estratégia explora falhas na verificação de identidade em mecanismos de confiança baseados em comportamento. Para demonstrar essa estratégia, um experimento foi conduzido em ambiente Docker com Nginx e Suricata para simular e observar o impacto da personificação e deterioração de credibilidade. Partindo desse ambiente, o atacante, uma máquina integrada a mesma rede, utilizando a ferramenta hping3, em apenas 3 minutos conseguiu fazer o bloqueio do usuário legítima, utilizando um ataque SYN-flood com personificação sobre o usuário legítimo. Demonstrando a viabilidade do ataque e a necessidade de contramedidas para mitigar esse tipo de ameaça.

Esse artefato tem como objetivo demonstrar a viabilidade em reproduzir o o ataque de negação de serviço a partir da deterioração de reputação.

## Estrutura do README.md

* [Título projeto](#cordeiro-em-pele-de-lobo-desvelando-a-negação-de-serviço-baseada-em-envenenamento-de-reputação)
* [Estrutura do readme.md](#estrutura-do-readmemd)
  * [Estrutura do Repositório](#estrutura-do-repositório)
  * [Definição dos diretórios](#definição-dos-diretórios)
* [Selos Considerados](#selos-considerados)
* [Informações básicas](#informações-básicas)
* [Dependências](#dependências)
* [Instalação](#instalação)
* [Teste mínimo](#teste-mínimo)
* [Experimentos](#experimentos)
  * [Reivindicação #1](#reivindicações-#1)
* [LICENSE](#license)

### Estrutura do Repositório


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

### Definição dos diretórios

* [ambiente/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente)
  * [attacker-config/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente/attacker-config)
    - Arquivo de configuração do atacante;
    - Arquivos usados para a execução do ataque;
    - Arquivo para coletar metricas de resultado;
    - Arquivo de resultados.
  * [client-config/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente/client-config)
    - Arquivo de configuração do cliente;
    - Arquivos para coletar metricas de resultado;
    - Arquivos de resultados.
  * [suricata-config/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente/suricata-config)
    - Arquivos de configuração do Suricata; 
    - Arquivos para coletar metricas de resultado;
    - Arquivos de resultados.
    * [iprep/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente/suricata-config/iprep)
      - Arquivos para a configuração de reputação do Suricata. 
    * [rules/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/ambiente/suricata-config/rules)
      - Arquivos para a configuração de regras do Suricata.
  * [docker-compose.yml](https://github.com/Carmofrasao/SBSeg-2025-Frasao/blob/main/ambiente/docker-compose.yml)
    - Arquivo de configuração do ambiente.

## Selos Considerados

Selo D + Selo F + Selo S + Selo R

## Informações básicas

Esta seção deve apresentar informações básicas de todos os componentes necessários para a execução e replicação dos experimentos. 
Descrevendo todo o ambiente de execução, com requisitos de hardware e software.

### Hardware

* CPU: AMD EPYC 7401 24-Core 2.0GHz
* RAM: 32 GB 
* Kernel: 6.12.13
* SO: Debian GNU/Linux 12 (bookworm)

### Software

* Docker - versão 20.10.24.

## Dependências

Todo o sistema foi rodado em Docker, então a unica coisa necessaria para executar o arterfato é o proprio Docker.

## Instalação

### Atualização do sistema
```
sudo apt update && sudo apt upgrade
```

### Curl
```
sudo apt install curl
```

### Script de instalação Docker (https://docs.docker.com/get-docker/)
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## Teste mínimo

* Todo o processo foi executado com a maquina principal (host) em modo root!

Antes de começar, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique a reputação do IP `172.20.1.3`, deve ser `3,127`, indicando que ele esta na categoria 3 (GoodHosts) com reputação de 127 (reputação maxima).

No diretorio `SBSeg-2025-Frasao/ambiente`, execute o comando:

```bash
docker-compose up
```

Aguarde todas as maquinas inicializarem.

#### Maquina suricata

Execute os seguintes comando:

```bash
docker exec -it suricata bash
cd /etc/suricata
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 monitor.py
```

#### Maquina attacker 

Execute os seguintes comando:

```bash
docker exec -it attacker bash
cd /home
./config.sh
./syn-flood.sh # Execute esse comando até aparecer a mensagem "{"message": "done", "return": "OK"}"
```

Após esse processo, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique novamente a reputação do IP `172.20.1.3`, agora, deve ser `3,107`, indicando que ele esta na categoria 3 (GoodHosts), porém, a reputação abaixou em 20, indicando que o Suricata reconheceu um ataque ao sistema, mesmo ele sendo executado por outra maquina (172.20.1.4).

## Experimentos

Cada reivindicações deve ser apresentada em uma subseção, com detalhes de arquivos de configurações a serem alterados, comandos a serem executados, flags a serem utilizadas, tempo esperado de execução, expectativa de recursos a serem utilizados como 1GB RAM/Disk e resultado esperado.

### Reivindicações #1

* Todo o processo foi executado com a maquina principal (host) em modo root!

No diretorio `SBSeg-2025-Frasao/ambiente`, execute o comando:

```bash
docker-compose up
```

Aguarde todas as maquinas inicializarem.

#### Maquina suricata

Execute os seguintes comando:

```bash
docker exec -it suricata bash
cd /etc/suricata
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
source venv/bin/activate
python3 monitor.py
```

O arquivo monitor.py é utilizado para atualizar a reputação dos IPs mal intencionados que tentam atacar o servidor web.

#### Maquina client

Execute os seguintes comando:

```bash
docker exec -it client bash
cd /home
/config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 time.py
# Após o syn-flood.py finalizar a execução, pode parar o time.py
wget -qO- 172.20.1.2 # Esse comando deve ficar travado, significa que o cliente foi bloqueado pelo Suricata
```

#### Maquina attacker 

Execute os seguintes comando:

```bash
docker exec -it attacker bash
cd /home
./config.sh
python3 syn-flood.py
```

Para confirmar que o processo foi concluido, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique novamente a reputação do IP `172.20.1.3`, agora, deve ser `1,127`, indicando que ele esta na categoria 1 (BadHosts), com reputação 127 (com certeza é um BadHost), indicando que o Suricata reconheceu o cliente como um IP perigoso, mesmo ele não executando nenhum comando malicioso.

## LICENSE

Apresente a licença.
