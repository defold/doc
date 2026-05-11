---
title: Rede no Defold
brief: Este manual explica como se conectar a servidores remotos e realizar outros tipos de conexões de rede.
---

# Rede

Não é incomum que jogos tenham algum tipo de conexão com um serviço de backend, talvez para enviar pontuações, lidar com matchmaking ou armazenar jogos salvos na nuvem. Muitos jogos também têm conexões peer-to-peer, nas quais os clientes do jogo se comunicam diretamente entre si, sem envolvimento de um servidor central. Conexões de rede e troca de dados podem ser feitas usando vários protocolos e padrões diferentes. Saiba mais sobre as diferentes formas de usar conexões de rede no Defold:

* [Requisições HTTP](/manuals/http-requests)
* [Conexões por socket](/manuals/socket-connections)
* [Conexões WebSocket](/manuals/websocket-connections)
* [Serviços online](/manuals/online-services)


## Detalhes técnicos

### IPv4 e IPv6

O Defold oferece suporte a conexões IPv4 e IPv6 para sockets e requisições HTTP.

### Conexões seguras

O Defold oferece suporte a conexões SSL seguras para sockets e requisições HTTP.

O Defold também pode, opcionalmente, verificar o certificado SSL de qualquer conexão segura. A verificação SSL será habilitada quando um arquivo PEM contendo chaves públicas de certificados CA raiz ou a chave pública de um certificado autoassinado for fornecido no campo [configuração SSL Certificates](/manuals/project-settings/#network) da seção Network em *game.project*. Uma lista de certificados CA raiz está incluída em `builtins/ca-certificates`, mas é recomendado criar um novo arquivo PEM e copiar e colar os certificados CA raiz necessários dependendo do(s) servidor(es) aos quais o jogo se conecta.
