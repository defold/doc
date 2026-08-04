---
title: Il servizio del motore e le API HTTP a runtime
brief: Questo manuale spiega il servizio HTTP di sviluppo in un motore di debug Defold in esecuzione e come le estensioni a runtime o gli strumenti esterni possono utilizzarlo.
---

# Il servizio del motore e le API HTTP a runtime

L'esecuzione di un progetto in modalità Debug crea un processo per una determinata istanza del motore a runtime, contenente il gioco e uno speciale servizio del motore accessibile per l'infrastruttura di sviluppo e profilazione, la logica e i messaggi a runtime, lo stato del motore e le estensioni.

Il servizio del motore è un servizio HTTP di sviluppo appartenente a un motore di debug (`dmengine`) in esecuzione.

È distinto dal [server dell'editor](/manuals/editor-http-api), che appartiene all'editor Defold e controlla il progetto aperto.

I due servizi utilizzano porte diverse. Uno strumento connesso alla porta dell'editor non può richiamare lì le route delle estensioni a runtime e, viceversa, uno strumento connesso al servizio del motore non può richiamare operazioni dell'editor.

Il servizio del motore fa parte dell'infrastruttura di debug, sviluppo e profilazione. Le istanze release del motore non creano il servizio.

## Disponibilità e individuazione della porta {#availability-and-port-discovery}

Quando l'editor avvia un motore di debug, richiede una porta del servizio assegnata dinamicamente. Il motore comunica la porta selezionata nella `Console` (e nel proprio log se viene eseguito da una CLI):

![Informazioni sulla porta del servizio del motore in una build di debug Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

La riga compare nella console dell'editor quando il gioco è stato avviato dall'editor. Un semplice controller locale può analizzarla, ma un'integrazione riutilizzabile dovrebbe consentire all'editor o al relativo wrapper di tenere traccia dell'istanza del motore e della porta registrata. Ciò evita di confondere una vecchia porta con un processo appena avviato o riutilizzato.

Il motore pubblicizza inoltre le destinazioni di sviluppo tramite il rilevamento dei servizi sulle piattaforme supportate. Tale meccanismo viene utilizzato principalmente dagli strumenti Defold e non dovrebbe essere sostituito con una porta codificata in modo permanente.

Il server è accessibile su localhost (`127.0.0.1`) alla porta indicata:

![Accesso al server del motore](images/automation/engine-server.png)

## Endpoint integrati {#built-in-endpoints}

Il motore di debug corrente registra un piccolo insieme di route principali.

| Endpoint | Scopo |
| --- | --- |
| `GET /ping` | Verifica che il servizio del motore risponda |
| `GET /info` | Legge la versione del motore, la piattaforma, l'identificatore di build e le informazioni sul servizio di log |
| `GET /state` | Legge lo stato della connessione di sviluppo utilizzato dagli strumenti Defold |
| `POST /post/<socket>/<message-type>` | Invia un messaggio Defold codificato in Protobuf a un socket del motore denominato |

Ad esempio:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

La route `/post` è utilizzata da operazioni di sviluppo come hot reload, riavvio, ridimensionamento e controllo dei processi. Il relativo corpo è un messaggio binario Protobuf del tipo indicato nella route; non è un'API per messaggi JSON.

Queste route fanno parte dell'infrastruttura di sviluppo; nell'implementazione del motore sono presenti ulteriori route per la profilazione e l'ispezione delle risorse.

## Route a runtime definite dalle estensioni {#extension-defined-runtime-routes}

Nelle build di debug, l'SDK delle estensioni native può fornire accesso al server web del motore. Un'estensione può registrare un prefisso di route su tale server ed esporre operazioni che dipendono dai dati a runtime.

Ciò è utile per gli strumenti di sviluppo, perché un'estensione può condividere il servizio del motore esistente anziché aprire un altro server HTTP.

Un'API di automazione a runtime definita da un'estensione dovrebbe:

* utilizzare un prefisso di route distinto e con versione;
* esporre le capacità supportate;
* restituire errori strutturati;
* gestire esplicitamente le funzionalità della piattaforma o del motore non disponibili;
* limitare le operazioni allo sviluppo e ai test locali;
* documentare se viene omessa dalle build release.

## Estensione Automation Bridge {#automation-bridge-extension}

L'estensione ufficiale [Automation Bridge](https://github.com/defold/extension-automation-bridge) di Defold è un'estensione nativa disponibile soltanto in modalità debug e basata sul servizio del motore. Registra un'API di automazione a runtime con versione in:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

La sua API runtime offre funzionalità quali ispezione di scene e nodi, input, informazioni sullo schermo, schermate, registrazione, informazioni sul ciclo di vita e sincronizzazione facoltativa definita dall'applicazione. Alcune operazioni includono:

| Operazione | Azione |
| --- | --- |
| `GET  /automation-bridge/v1/health` | Report sullo stato, capacità dell'API e compatibilità |
| `POST /automation-bridge/v1/input/click` | Interazioni di input a runtime |
| `GET  /automation-bridge/v1/screenshot` | Schermate a runtime |

Consulta la [documentazione dell'API nativa](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) e la [documentazione dell'helper Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) dell'estensione per la versione installata nel progetto.

Automation Bridge non espone né la propria API HTTP né il proprio modulo Lua nelle build release.

### Client dell'editor e del runtime {#editor-and-runtime-clients}

Gli helper Python di Automation Bridge illustrano l'architettura a due client. La funzione `editor.open_project()` restituisce un client del progetto nell'editor, mentre `project.build_and_run()` restituisce un client del motore separato.

| Client | Scopo |
| --- | --- |
| Progetto | API HTTP dell'editor, comandi, debugger, console, preferenze, documentazione di riferimento, anteprime, build e individuazione della porta |
| Gioco - servizio del motore | Scena, input, schermate, stato a runtime e sincronizzazione |

La divisione tra `project` e `game` rende esplicito il confine tra i processi. Le operazioni dell'editor restano sul server dell'editor, mentre le osservazioni e le azioni sul gioco in esecuzione restano sul servizio del motore.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limitazioni e sicurezza {#limitations-and-security}

Il servizio del motore e le route definite dalle estensioni sono strumenti di sviluppo e devono essere considerati tali.

::: important
Il servizio del motore attualmente non pubblica un documento OpenAPI. Le integrazioni dovrebbero limitarsi al comportamento documentato o all'API con versione di un'estensione.
:::

Script a runtime, fisica, input, oggetti creati dinamicamente e rendering della piattaforma richiedono un motore in esecuzione e dovrebbero essere verificati tramite [test automatici a runtime](/manuals/automated-testing).

* Non pubblicare il servizio tramite un router, un'interfaccia pubblica o un tunnel non attendibile.
* Non presupporre che le route del servizio del motore richiedano autenticazione.
* Le route a runtime possono variare in base alla versione dell'estensione, alla piattaforma, al backend grafico e alle capacità del motore.
* Utilizza la negoziazione di versione o capacità per API aggiornate definite dalle estensioni.
