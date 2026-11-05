---
title: Il servizio del motore e le API HTTP a runtime
brief: Questo manuale spiega il servizio HTTP di sviluppo in un motore Defold di debug in esecuzione e come le estensioni a runtime o gli strumenti esterni possono utilizzarlo.
---

# Il servizio del motore e le API HTTP a runtime {#the-engine-service-and-runtime-http-apis}

L'esecuzione di un progetto in modalità Debug crea un processo per una determinata istanza del motore a runtime, contenente il gioco e uno speciale servizio del motore. Questo servizio consente di accedere all'infrastruttura di sviluppo e profilazione, alla logica e ai messaggi a runtime, allo stato del motore e alle estensioni.

Il servizio del motore è un servizio HTTP di sviluppo appartenente a un motore di debug o headless in esecuzione (`dmengine` o `dmengine_headless`).

È distinto dal [server dell'editor](/manuals/editor-http-api), che appartiene all'editor Defold e controlla il progetto aperto.

I due servizi utilizzano porte diverse. Uno strumento connesso alla porta dell'editor non può richiamare lì le route delle estensioni a runtime e, viceversa, uno strumento connesso al servizio del motore non può richiamare operazioni dell'editor.

Il servizio del motore fa parte dell'infrastruttura di debug, sviluppo e profilazione. Le istanze del motore nelle build di release non creano il servizio.

## Disponibilità e individuazione della porta {#availability-and-port-discovery}

Quando avvia un motore di debug, l'editor richiede una porta del servizio assegnata dinamicamente. Il motore riporta la porta selezionata nella *Console* e nel proprio log quando viene eseguito dalla CLI:

![Informazioni sulla porta del servizio del motore in una build di debug Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Il motore registra anche l'URL completo di rilevamento OpenAPI usando il proprio indirizzo effettivo e la porta assegnata:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Queste righe compaiono nella console dell'editor quando il gioco è stato avviato dall'editor. Un semplice controller locale può analizzarle, ma un'integrazione riutilizzabile dovrebbe lasciare che l'editor o il suo wrapper tengano traccia dell'istanza del motore e della porta registrata. Ciò evita di confondere una vecchia porta con quella di un processo appena avviato o riutilizzato.

Il motore annuncia inoltre le destinazioni di sviluppo tramite il rilevamento dei servizi sulle piattaforme supportate. Tale meccanismo viene utilizzato principalmente dagli strumenti Defold e non dovrebbe essere sostituito con un numero di porta fisso nel codice.

Il server è accessibile su localhost (`127.0.0.1`) alla porta indicata:

![Accesso al server del motore](images/automation/engine-server.png)

## Rilevamento delle operazioni tramite OpenAPI {#discovering-operations-through-openapi}

`GET /openapi.json` restituisce un documento OpenAPI 3.0.3 che descrive l'API HTTP a runtime. Usa la porta del servizio del motore riportata nel log. Per un motore locale, sostituisci `<port>` di seguito con quella porta:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

Il documento descrive percorsi, metodi, parametri, corpi delle richieste e risposte forniti dai gestori attualmente registrati, comprese le estensioni native che forniscono metadati OpenAPI. Il suo oggetto `paths` cambia quando vengono aggiunti o rimossi gestori. Le route del profiler e delle estensioni dipendono dalla piattaforma, dalla configurazione e dalle estensioni registrate del motore in esecuzione: recupera quindi il documento dall'istanza che stai usando.

I gestori registrati senza metadati OpenAPI restano richiamabili, ma non compaiono nel documento. Anche una route documentata può segnalare una funzionalità non disponibile; esamina le descrizioni delle risposte e gli eventuali endpoint delle funzionalità prima di usare operazioni dipendenti dalla piattaforma.

L'editor dispone di un proprio [documento OpenAPI](/manuals/editor-http-api/#discovering-operations-through-openapi) sulla porta dell'editor. Usa il documento del motore per le operazioni a runtime.

## Endpoint integrati {#built-in-endpoints}

Il motore di debug corrente registra un piccolo insieme di route principali.

| Endpoint | Scopo |
| --- | --- |
| `GET /openapi.json` | Rileva le operazioni HTTP a runtime attualmente registrate che forniscono metadati OpenAPI |
| `GET /ping` | Verifica che il servizio del motore risponda |
| `GET /info` | Legge la versione del motore, la piattaforma, l'identificatore di build e le informazioni sul servizio di log |
| `GET /state` | Legge lo stato della connessione di sviluppo utilizzato dagli strumenti Defold |
| `POST /post/<socket>/<message-type>` | Invia un messaggio Defold codificato in Protobuf a un socket del motore identificato per nome |

Ad esempio:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

La route `/post` è utilizzata da operazioni di sviluppo come hot reload, riavvio, ridimensionamento e controllo dei processi. Il relativo corpo è un messaggio binario Protobuf del tipo indicato nella route; non è un'API per messaggi JSON. Il messaggio Protobuf serializzato non può superare i 1024 byte; in caso contrario, viene restituito `400 Too large message`.

Queste route fanno parte dell'infrastruttura di sviluppo; nell'implementazione del motore sono presenti ulteriori route per la profilazione e l'ispezione delle risorse.

## Endpoint di registrazione {#recording-endpoints}

I motori di debug desktop espongono anche la registrazione MP4 nativa tramite le route seguenti. Queste sono escluse dalle build di release, headless, mobili e web e quando **Exclude Record** è abilitato nell'[App Manifest](/manuals/app-manifest/#exclude-record).

| Endpoint | Funzione |
| --- | --- |
| `GET /recording/capabilities` | Rileva il supporto video/audio, i requisiti del backend e l'`instance_id` del servizio di registrazione |
| `GET /recording/status` | Legge l'operazione corrente, l'avanzamento asincrono e le informazioni sul file finalizzato |
| `POST /recording/start` | Richiede la registrazione e riceve il suo `operation_id` |
| `POST /recording/stop` | Richiede l'arresto e la finalizzazione dell'operazione specificata |
| `GET /recording/files/{id}` | Scarica un MP4 finalizzato |
| `DELETE /recording/files/{id}` | Elimina un file completato conservato dal servizio |

Rileva queste route tramite `/openapi.json`, quindi controlla `/recording/capabilities` per conoscere il supporto della piattaforma corrente. Le operazioni che modificano la registrazione richiedono l'intestazione `X-Recording-Instance`; l'arresto richiede anche l'`operation_id` accettato. Avvio e arresto sono asincroni: attendi la finalizzazione prima di scaricare il file. Consulta il [manuale della registrazione](/manuals/recording/#recording-through-http) per il flusso di lavoro completo.

Il servizio HTTP condivide il registratore con Lua. Gli avvii tramite HTTP abilitano l'audio dell'applicazione per impostazione predefinita, se supportato; quelli da Lua registrano soltanto il video per impostazione predefinita. Solo le registrazioni avviate tramite HTTP dispongono di una ricevuta `file` scaricabile. Prima del download, attendi `pending: false`, `finalized: true` e `file.state: "complete"`, quindi [verifica le dimensioni e lo SHA-256 del file](/manuals/recording/#download-and-release-the-file). Consulta [Condivisione del registratore](/manuals/recording/#sharing-the-recorder-with-http-clients) se usi insieme client Lua e HTTP.

## Endpoint delle tracce GPU Metal {#metal-gpu-trace-endpoint}

Su macOS, i motori di debug espongono `/profiler/gputrace` per acquisire tracce GPU Metal. La route compare in `/openapi.json` solo su macOS. L'acquisizione richiede l'adattatore Metal nativo e `METAL_CAPTURE_ENABLED=1` nell'ambiente di avvio del motore. Se l'acquisizione non è disponibile, la richiesta restituisce HTTP 501 con `error.code: "gputrace_unsupported"`.

| Endpoint | Funzione |
| --- | --- |
| `POST /profiler/gputrace` | Pianifica l'acquisizione in un percorso assoluto `.gputrace` scrivibile; `frames` ha come valore predefinito `1` e può essere compreso tra `1` e `10000`. |
| `GET /profiler/gputrace` | Legge lo stato, il percorso e i conteggi dei frame dell'acquisizione corrente o più recente. |
| `DELETE /profiler/gputrace` | Annulla un'acquisizione in attesa o termina un'acquisizione attiva dopo il frame attualmente renderizzato; conserva la traccia su disco. |

Le richieste accettate restituiscono HTTP 200 con `ok: true` e un oggetto `data`. L'acquisizione procede in modo asincrono: interroga `GET` finché `data.state` non è `complete`, `canceled` o `failed`. Gli errori di avvio nativi vengono riportati in `data.error`. La traccia viene scritta sull'host del motore. Consulta la [guida all'acquisizione delle tracce GPU Metal](/manuals/profiling/#metal-gpu-trace-capture) per i comandi di avvio, il rilevamento del supporto, gli esempi di acquisizione e l'apertura del risultato in Xcode.

## Route a runtime definite dalle estensioni {#extension-defined-runtime-routes}

Nelle build di debug, l'SDK delle estensioni native può fornire accesso al server web del motore. Un'estensione può registrare un prefisso di route su tale server ed esporre operazioni che dipendono dai dati a runtime.

Ciò è utile per gli strumenti di sviluppo, perché un'estensione può condividere il servizio del motore esistente anziché aprire un altro server HTTP.

Un'API di automazione a runtime definita da un'estensione dovrebbe:

* utilizzare un prefisso di route distinto e con versione;
* esporre le capacità supportate;
* restituire errori strutturati;
* gestire esplicitamente le funzionalità della piattaforma o del motore non disponibili;
* limitare le operazioni allo sviluppo e ai test locali;
* documentare se viene omessa dalle build di release.

### Pubblicazione delle operazioni delle estensioni in OpenAPI {#publishing-extension-operations-in-openapi}

Nel callback di inizializzazione dell'applicazione di un'estensione nativa, ottieni il server con `dmEngine::GetWebServer(app_params)` e registra i gestori solo se l'handle restituito non è nullo. Consulta il [ciclo di vita delle estensioni](/manuals/extensions/#extension-lifecycle) per la configurazione del callback.

L'overload a quattro argomenti di `dmWebServer::AddHandler()` accetta un oggetto Paths di OpenAPI 3.0.3 come stringa JSON. L'oggetto ha i percorsi delle route come chiavi di primo livello. Ogni percorso deve iniziare con il prefisso registrato e non essere già documentato da un altro gestore. Usa schemi inline o riferimenti a percorsi nel documento risultante.

Per esempio, questa funzione di supporto registra un callback e la descrizione del relativo endpoint di stato:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Passa un callback che implementi `GET /example/v1/status` e restituisca la risposta `text/plain` documentata. Il callback rimane responsabile di controllare i percorsi e i metodi delle richieste e di produrre le risposte. Controlla il risultato della registrazione: metadati non validi o in conflitto restituiscono `dmWebServer::RESULT_ERROR_INVAL`.

Il server conserva il puntatore JSON senza copiare la stringa. Mantienine la memoria invariata e valida finché il gestore non viene rimosso con `dmWebServer::RemoveHandler()` o il server non viene distrutto. L'array `static const char` dell'esempio soddisfa questo requisito. La rimozione del gestore rimuove anche i suoi percorsi dalle successive risposte di `/openapi.json`.

L'overload a tre argomenti `dmWebServer::AddHandler(server, prefix, &params)` resta supportato. Equivale a passare `0` come quarto argomento: il gestore viene registrato senza metadati OpenAPI ed escluso dal rilevamento.

## Estensione Automation Bridge {#automation-bridge-extension}

L'estensione ufficiale [Automation Bridge](https://github.com/defold/extension-automation-bridge) di Defold è un'estensione nativa disponibile soltanto in modalità debug e basata sul servizio del motore. Registra un'API di automazione a runtime con versione in:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

La sua API di runtime offre funzionalità quali ispezione di scene e nodi, input, informazioni sullo schermo, schermate, registrazione, informazioni sul ciclo di vita e sincronizzazione facoltativa definita dall'applicazione. Alcune operazioni includono:

| Operazione | Azione |
| --- | --- |
| `GET  /automation-bridge/v1/health` | Report sullo stato, capacità dell'API e compatibilità |
| `POST /automation-bridge/v1/input/click` | Interazioni di input a runtime |
| `GET  /automation-bridge/v1/screenshot` | Schermate a runtime |

Consulta la [documentazione dell'API nativa](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) e la [documentazione dell'helper Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) dell'estensione per la versione installata nel progetto.

Automation Bridge non espone né la propria API HTTP né il proprio modulo Lua nelle build di release.

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
Usa il documento `/openapi.json` del motore in esecuzione per il rilevamento in Defold 1.14.1 e versioni successive. I motori precedenti non forniscono questo endpoint. Per i gestori registrati senza metadati OpenAPI, consulta la documentazione API dell'estensione relativa alla versione utilizzata.
:::

Script a runtime, fisica, input, oggetti creati dinamicamente e rendering della piattaforma richiedono un motore in esecuzione e dovrebbero essere verificati tramite [test automatici a runtime](/manuals/automated-testing).

* Non pubblicare il servizio tramite un router, un'interfaccia pubblica o un tunnel non attendibile.
* Non presupporre che le route del servizio del motore richiedano autenticazione.
* Le route a runtime possono variare in base alla versione dell'estensione, alla piattaforma, al backend grafico e alle capacità del motore.
* Utilizza la negoziazione di versione o capacità per API aggiornate definite dalle estensioni.
