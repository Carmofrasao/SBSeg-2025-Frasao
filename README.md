# SBSeg 2025

Repositório para dados relativos ao XXV Simpósio Brasileiro de Cibersegurança

Usaremos o Suricata

https://github.com/OISF/suricata

## Alguns comando suteis

### Teste de funcionamento de rede

`wget -qO- 172.20.1.2:80`

### "Ataque"

`hping3 -c 5500 -S -p 80 -i u110 -a 172.20.1.3 172.20.1.2`

* O ataque não esta funcionando, o Suricata esta funcionando, de mais..., ele está jogando os pacotes do hping3 fora
