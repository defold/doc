---
title: Redes en Defold
brief: Este manual explica cómo conectarse a servidores remotos y realizar otros tipos de conexiones de red.
---

# Redes

No es raro que los juegos tengan algún tipo de conexión con un servicio backend, quizá para publicar puntuaciones, gestionar matchmaking o almacenar partidas guardadas en la nube. Muchos juegos también tienen conexiones peer to peer donde los clientes del juego se comunican directamente entre sí, sin la intervención de un servidor central. Las conexiones de red y el intercambio de datos pueden realizarse usando varios protocolos y estándares diferentes. Aprende más sobre las distintas formas de usar conexiones de red en Defold:

* [Solicitudes HTTP](/manuals/http-requests)
* [Conexiones socket](/manuals/socket-connections)
* [Conexiones WebSocket](/manuals/websocket-connections)
* [Servicios en línea](/manuals/online-services)


## Detalles técnicos

### IPv4 e IPv6

Defold admite conexiones IPv4 e IPv6 para sockets y solicitudes HTTP.

### Conexiones seguras

Defold admite conexiones SSL seguras para sockets y solicitudes HTTP.

Defold también puede verificar opcionalmente el certificado SSL de cualquier conexión segura. La verificación SSL estará activada cuando se proporcione un archivo PEM que contenga claves públicas de certificados raíz de CA o la clave pública de un certificado autofirmado en el campo de la opción [SSL Certificates](/manuals/project-settings/#network)) de la sección Network en *game.project*. Se incluye una lista de certificados raíz de CA en `builtins/ca-certificates`, pero se recomienda crear un nuevo archivo PEM y copiar y pegar los certificados raíz de CA necesarios según los servidores a los que se conecta el juego.
