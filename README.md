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
  * [Hardware](#hardware)
  * [Software](#software)
* [Dependências](#dependências)
* [Instalação](#instalação)
* [Teste mínimo](#teste-mínimo)
* [Experimentos](#experimentos)
  * [Reivindicação #1](#reivindicações-1)
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
│   │   ├── requirements.txt
│   │   ├── rtt.txt
│   │   └── time.py
│   ├── docker-compose.yml
│   └── suricata-config
│       ├── classification.config
│       ├── count.py
│       ├── entrypoint.sh
│       ├── eve.json
│       ├── monitor.py
│       ├── reference.config
│       ├── requirements.txt
│       ├── suricata-server.txt
│       ├── suricata.yaml
│       ├── threshold.config
│       ├── update.yaml
│       ├── iprep
│       │   ├── categories.txt
│       │   └── reputation.list
│       └── rules
│           ├── script.lua
│           └── suricata.rules
├── imagens
│   ├── rtt.pdf
│   └── variacao_de_pacotes.pdf
├── LICENSE
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
* [imagens/](https://github.com/Carmofrasao/SBSeg-2025-Frasao/tree/main/imagens)
  - Figuras para auxiliar no entendimento do processo.

## Selos Considerados

Selo D + Selo F + Selo S + Selo R

## Informações básicas

### Hardware

* CPU: AMD EPYC 7401 24-Core 2.0GHz
* RAM: 32 GB 
* Kernel: 6.12.13
* SO: Debian GNU/Linux 12 (bookworm)

### Software

* Docker - versão 28.1.1.

## Dependências

Todo o sistema foi rodado em Docker, então a unica coisa necessaria para executar o arterfato é o proprio Docker.

## Instalação

### Atualização do sistema
```
sudo apt update && sudo apt upgrade
```
### Dependencias 
```
sudo apt install ca-certificates curl gnupg
```
### Adicione a chave GPG oficial da Docker 
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
### Configure o repositório da Docker
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
### Atualize o índice de pacotes
```
sudo apt update
```
### Instale o Docker Engine e o plugin do Docker Compose
```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Teste mínimo

* Todo o processo foi executado com a maquina principal (host) em modo root!
* Para a execução do teste minimo, são necessario 3 terminais.

Antes de começar, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique a reputação do IP `172.20.1.3`, deve ser `3,127`, indicando que ele esta na categoria 3 (GoodHosts) com reputação de 127 (reputação maxima).

No diretorio `SBSeg-2025-Frasao/ambiente`, execute o comando:

```bash
docker compose up
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
./syn-flood.sh 
# Execute esse comando até aparecer a mensagem "{"message": "done", "return": "OK"}" no monitor.py (maquina do Suricata)
```

Após esse processo, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique novamente a reputação do IP `172.20.1.3`, agora, deve ser `3,107`, indicando que ele esta na categoria 3 (GoodHosts), porém, a reputação abaixou em 20, indicando que o Suricata reconheceu um ataque ao sistema, mesmo ele sendo executado por outra maquina (172.20.1.4).

## Experimentos

### Reivindicações #1

* Todo o processo foi executado com a maquina principal (host) em modo root!
* Para a execução do Experimento, são necessario 4 terminais.

No diretorio `SBSeg-2025-Frasao/ambiente`, execute o comando:

```bash
docker compose up
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

A Figura a seguir demonstra a execução do ataque de negação de serviço baseado em envenenamento. Ao final, o servidor para de receber os pacotes que o cliente esta mandando, demonstrando a eficacia do ataque!

![Evolução do volume de pacotes gerados na rede.](./imagens/variacao_de_pacotes.pdf)

#### Maquina client

Execute os seguintes comando:

```bash
docker exec -it client bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 time.py # Execute esse comando junto ao syn-flood.py
# Após o syn-flood.py finalizar a execução, pode parar o time.py
wget -qO- 172.20.1.2 # Esse comando deve ficar travado, significa que o cliente foi bloqueado pelo Suricata
```

O gráfico de tempo de resposta às requisições legítimas, presente na Figura a seguir apresenta um padrão de aumento contínuo, refletindo a degradação gradual no desempenho da comunicação entre o cliente legítimo e o servidor. Ao final, o tempo de resposta tende ao infinito, mostrando que o cliente esta bloqueado.

![Variação do tempo de resposta percebido pelo cliente legítimo ao fazer requisições para o servidor](./imagens/rtt.pdf)

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

GNU GPL v3
