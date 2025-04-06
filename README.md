# SBSeg 2025

Repositório para dados relativos ao XXV Simpósio Brasileiro de Cibersegurança

Possivelmente usaremos o Suricata

https://github.com/OISF/suricata

Existe uma maneira de recarregar as regras usando um socket unix. Isso pode ser feito atravé do comando `suricatasc`.
Uma boa ideia parece ser criar um script python para analisar os logs e detectar que há necessidade de mudança de reputação. Então o script alteraria o arquivo de reputação e recarregaria as regras.

`hping3 -c 5000 -S -p 80 -i u100 -a 172.20.0.3 172.20.0.2`
