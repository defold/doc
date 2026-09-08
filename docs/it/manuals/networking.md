---
title: Connessioni di rete in Defold
brief: Questo manuale spiega come connettersi a server remoti e stabilire altri tipi di connessioni di rete.
---

# Connessioni di rete {#networking}

È comune che i giochi abbiano qualche tipo di connessione a un servizio backend, ad esempio per inviare punteggi, gestire l'abbinamento dei giocatori o archiviare i salvataggi nel cloud. Molti giochi hanno anche connessioni peer-to-peer in cui i client di gioco comunicano direttamente tra loro, senza coinvolgere un server centrale. Le connessioni di rete e lo scambio di dati possono avvenire tramite diversi protocolli e standard. Scopri di più sui diversi modi di utilizzare le connessioni di rete in Defold:

* [Richieste HTTP](/manuals/http-requests)
* [Connessioni socket](/manuals/socket-connections)
* [Connessioni WebSocket](/manuals/websocket-connections)
* [Servizi online](/manuals/online-services)


## Dettagli tecnici {#technical-details}

### IPv4 e IPv6 {#ipv4-and-ipv6}

Defold supporta connessioni IPv4 e IPv6 per i socket e le richieste HTTP.

### Connessioni sicure {#secure-connections}

Defold supporta connessioni SSL sicure per i socket e le richieste HTTP.

Defold può anche verificare, facoltativamente, il certificato SSL di qualsiasi connessione sicura. La verifica SSL viene abilitata quando nel campo dell'[impostazione SSL Certificates](/manuals/project-settings/#network)) della sezione Network in *game.project* viene specificato un file PEM contenente le chiavi pubbliche dei certificati CA radice oppure la chiave pubblica di un certificato autofirmato. Un elenco di certificati CA radice è incluso in `builtins/ca-certificates`, ma si consiglia di creare un nuovo file PEM e di copiarvi e incollarvi i certificati CA radice necessari in base ai server a cui si connette il gioco.

