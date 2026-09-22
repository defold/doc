---
title: Connessioni socket
brief: Questo manuale spiega come creare connessioni socket.
---

## Connessioni socket {#socket-connections}

Defold include la [libreria LuaSocket](https://lunarmodules.github.io/luasocket/) per creare connessioni socket TCP e UDP. Ecco un esempio di come creare una connessione socket, inviare dati e leggere una risposta:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Questo codice crea un socket TCP e lo connette all'indirizzo IP 127.0.0.1 (localhost) sulla porta 8123. Imposta il timeout a 0 per rendere il socket non bloccante e invia la stringa "foobar" tramite il socket. Legge inoltre una riga di dati (byte che terminano con un carattere di nuova riga) dal socket. Tieni presente che l'esempio precedente non contiene alcuna gestione degli errori.

### Riferimento API ed esempi {#api-reference-and-examples}

Consulta il [riferimento API](/ref/socket/) per saperne di più sulle funzionalità disponibili tramite LuaSocket. Anche la [documentazione ufficiale di LuaSocket](https://lunarmodules.github.io/luasocket/) contiene molti esempi di utilizzo della libreria. Altri esempi e moduli di supporto sono disponibili nella [libreria DefNet](https://github.com/britzl/defnet/).
