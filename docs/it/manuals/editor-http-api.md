---
title: Automatizzare l'editor Defold con HTTP
brief: Questo manuale spiega come gli strumenti esterni possono individuare e utilizzare l'API HTTP locale di un progetto aperto nell'editor Defold.
---

# Automatizzare l'editor Defold

L'editor Defold apre un server speciale per le azioni automatizzate. L'API HTTP controlla il progetto aperto. Utilizzala per comandi dell'editor, build, risorse del progetto, anteprime, preferenze, output della console, ricerca nella documentazione o integrazioni con script dell'editor. Per ispezionare o controllare invece il gioco in esecuzione, utilizza il [servizio del motore o un'API di automazione a runtime](/manuals/engine-service).

::: important
L'API HTTP dell'editor è sperimentale e può cambiare tra le versioni di Defold. Il documento `/openapi.json` generato dall'editor in esecuzione è la fonte autorevole per le operazioni e gli schemi disponibili.
:::

## Avviare l'editor da uno strumento esterno {#starting-the-editor-from-an-external-tool}

Uno strumento esterno necessita dell'eseguibile dell'editor e del percorso assoluto del file `game.project` del progetto.

Le versioni di Defold installate possono essere individuate tramite `installations.json`, come descritto nel [manuale dell'editor](/manuals/editor/#editor-installation-metadata). Il relativo campo `launcherPath` contiene l'eseguibile da avviare. Passa il percorso di `game.project` come primo argomento posizionale per aprire direttamente il progetto.

L'argomento facoltativo `--port` o `-p` seleziona la porta del server dell'editor. Se viene omesso, Defold sceglie una porta disponibile; questa soluzione è solitamente preferibile quando possono essere aperti più progetti.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

L'editor è un'applicazione desktop grafica. Avvialo in una sessione utente interattiva con accesso allo schermo. Utilizza [Bob](/manuals/bob) quando non è disponibile una sessione grafica, ad esempio nella CI headless, oppure per l'automazione della sola compilazione e la creazione di bundle autonomi.

Dopo avere avviato l'editor, attendi che il progetto sia aperto e che esista `.internal/editor.port`. Quindi interroga ripetutamente `/openapi.json` finché non restituisce un documento valido. Non presupporre che la creazione del processo significhi che il progetto sia pronto.

## Individuare il server dell'editor {#locating-the-editor-server}

L'editor avvia un server HTTP locale mentre è aperto un progetto. Seleziona <kbd>Help ▸ Open Editor Server</kbd> per aprirne la pagina iniziale nel browser predefinito:

![La pagina iniziale del server locale dell'editor](images/automation/editor_server.png)

La porta selezionata viene scritta all'interno del progetto in:

```text
.internal/editor.port
```

D'ora in poi, gli esempi e i comandi di questo manuale faranno riferimento alle seguenti variabili della shell:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

Il file della porta appartiene alla sessione corrente dell'editor. Leggilo nuovamente dopo avere riavviato l'editor.

::: important
Il server dell'editor è un'interfaccia di controllo locale attendibile. Non esporlo tramite un indirizzo pubblico, un inoltro di porta o un tunnel non attendibile.
:::

## Individuare le operazioni tramite OpenAPI {#discovering-operations-through-openapi}

Le uniche informazioni di bootstrap specifiche di Defold necessarie a uno strumento esterno sono la porta dell'editor e il documento OpenAPI:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

Il documento OpenAPI 3.0.3 restituito descrive le operazioni supportate dalla versione dell'editor in esecuzione, inclusi percorsi, metodi, parametri, nomi dei comandi, formati delle richieste, risposte, codici di stato e requisiti di autenticazione.

Elenca i percorsi documentati:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Elenca i comandi dell'editor disponibili:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

Un'integrazione compatibile con più versioni dovrebbe verificare ogni operazione richiesta e configurare le richieste in base allo schema restituito. Sconsigliamo di mantenere una copia che si presume esaustiva dei nomi degli endpoint o dei comandi, poiché può diventare obsoleta.

Anche le route definite dal progetto compaiono in `/openapi.json` quando i relativi script dell'editor forniscono una descrizione dell'operazione OpenAPI.

## Eseguire i comandi dell'editor {#executing-editor-commands}

I comandi dell'editor vengono richiamati tramite:

```text
POST /command/{command}
```

Ad esempio, il comando corrente `build` compila ed esegue il progetto:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

Una build riuscita restituisce un risultato strutturato:

```json
{
  "success": true,
  "issues": []
}
```

Una build non riuscita restituisce lo stato HTTP `422` con problemi come:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

I campi disponibili dipendono dall'errore. Utilizza il percorso della risorsa e l'intervallo nel codice sorgente quando sono presenti, ma gestisci anche i problemi che contengono soltanto un messaggio.

Tra i comandi comunemente utili, quando sono elencati dall'editor in esecuzione, figurano:

`build`
: Compila ed esegue il progetto.

`clean-build`
: Svuota la cache di build, quindi compila ed esegue il progetto. Utilizzalo soltanto quando una build normale si comporta in modo incoerente o sembra non rilevare le modifiche.

`build-html5`
: Crea la build HTML5 del progetto e rende l'output disponibile tramite il server dell'editor.

`fetch-libraries`
: Scarica e ricarica le dipendenze del progetto.

`hot-reload`
: Ricarica le risorse modificate in un gioco in esecuzione.

`reload-extensions`
: Ricarica gli script dell'editor.

`debugger-start`, `debugger-stop` e i comandi di avanzamento del debugger
: Controllano una sessione di debug e il progetto in esecuzione.

I nomi esatti e la disponibilità dipendono dalla versione dell'editor e dal suo stato corrente; individuali tramite `/openapi.json`.

I comandi che operano sulle risorse del progetto sincronizzano le modifiche esterne ai file prima dell'esecuzione.

### Risposte dei comandi e attività asincrone {#command-responses-and-asynchronous-work}

L'operazione dei comandi documenta i codici di risposta nello schema OpenAPI corrente.

| Stato | Significato |
| --- | --- |
| `200` | Il comando è stato completato e ha restituito un risultato |
| `202` | Il comando è stato accettato e prosegue in modo asincrono |
| `403` | Il comando non è attivo nello stato corrente dell'editor |
| `404` | Il comando non è disponibile |
| `422` | La build o la convalida non è riuscita |
| `500` | Si è verificato un errore interno dell'editor |

Una risposta HTTP `202` non dimostra che il risultato richiesto esista. Attendi l'output, la risorsa, l'indicatore nella console o l'URL servito pertinente e imponi un timeout.

### Creare una build HTML5 {#building-html5}

Se il documento OpenAPI corrente elenca `build-html5`, richiamalo tramite l'operazione dei comandi:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

Il comando viene eseguito in modo asincrono e normalmente restituisce HTTP `202`. Al termine della build, l'editor la serve all'indirizzo:

```text
http://127.0.0.1:<editor-port>/html5/
```

Attendi che l'URL sia disponibile prima di avviare i test nel browser. Per ulteriori dettagli, consulta [Test nel browser per HTML5](/manuals/automated-testing/#browser-tests-for-html5).

## Cercare nella documentazione API {#searching-api-documentation}

Quando è presente in `/openapi.json`, l'operazione `/ref` cerca nella documentazione API inclusa nella versione dell'editor in esecuzione. Fornisce nomi e firme corrispondenti a tale versione.

Ad esempio, per cercare una funzione, usa:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtra in base all'ambiente e al linguaggio:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

I parametri di ricerca sono:

`environment`
: `editor`, `runtime` o valori separati da virgole.

`language`
: `Lua`, `C`, `C++` o valori separati da virgole.

`q`
: Un'espressione senza distinzione tra maiuscole e minuscole. Gli spazi rappresentano AND, mentre `|` rappresenta OR.

Esistono anche risorse di documentazione condensate: l'[indice della documentazione per LLM](https://defold.com/llms.txt) rimanda ai manuali ufficiali, ai namespace API e agli esempi, mentre la [documentazione completa per LLM](https://defold.com/llms-full.txt) elenca la documentazione completa per consentire la ricerca offline e l'indicizzazione locale.

Gli agenti IA dovrebbero tuttavia preferire ricerche specifiche anziché recuperare un intero documento di riferimento quando occorre soltanto un'API o un messaggio, in modo da risparmiare token e disporre di un contesto pulito e meglio preparato per l'attività specifica.

## Leggere l'output della console {#reading-console-output}

Leggi la console dell'editor in formato JSON:

```sh
curl -sS "$BASE_URL/console" | jq
```

La risposta contiene il testo della console in `lines` e regioni semantiche in `regions`, inclusi errori, risultati delle valutazioni e riferimenti alle risorse.

Per seguire continuamente l'output della console, usa:

```sh
curl -N "$BASE_URL/console/stream"
```

Il flusso include le righe già presenti nella console e poi rimane aperto per il nuovo output. Chiudilo dopo aver ricevuto un indicatore di completamento o un errore, aver rilevato la terminazione del processo o aver raggiunto un timeout o un limite di righe.

Per l'inquadramento dei risultati dei test e la classificazione degli errori, consulta [Test automatici e verifica](/manuals/automated-testing/#structured-test-results).

## Renderizzare le anteprime delle scene {#rendering-scene-previews}

L'editor Defold (a partire dalla versione 1.13.1) può renderizzare in formato PNG una "schermata" di una risorsa scena supportata tramite il comando `/preview/{path}`:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Questo comando renderizza la collection principale del progetto aperto basato sul modello Basic 3D in una vista iniziale predefinita:

![Anteprima della collection principale renderizzata dall'editor](images/automation/main-preview.png)

Puoi utilizzare il rendering per ottenere anteprime delle risorse che usano l'editor visuale delle scene. Ad esempio, puoi renderizzare allo stesso modo un componente modello, così da verificarne l'aspetto o, per esempio, la correttezza dello shader:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Anteprima del modello del cubo renderizzata dall'editor](images/automation/cube-preview.png)

Il percorso dopo `/preview/` non include una barra iniziale. Le dimensioni facoltative utilizzano per impostazione predefinita le dimensioni di visualizzazione del progetto e devono essere comprese tra `1` e `4096`.

| Stato | Significato |
| --- | --- |
| `200` | L'anteprima è stata renderizzata |
| `400` | Le dimensioni non sono valide |
| `404` | La risorsa non è stata trovata |
| `422` | La risorsa non è caricata o non supporta le anteprime delle scene |

Le anteprime possono essere molto utili per l'analisi visiva del progetto: controllo dei layout dei livelli e delle GUI, configurazione di shader e illuminazione, regressioni visive o creazione di miniature per la documentazione.

::: important
Un'anteprima dell'editor non è una schermata del gioco in esecuzione. Non verifica gli oggetti creati dinamicamente, la post-elaborazione a runtime o il rendering specifico della piattaforma. Utilizza una [schermata a runtime](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) quando sono necessari questi elementi.
:::

## Eseguire Lua nell'editor {#executing-editor-lua}

L'operazione autenticata `POST /eval` esegue Lua nell'ambiente delle estensioni dell'editor. Il token bearer valido per la sessione è memorizzato in:

```text
.internal/editor.token
```

Leggi il token ed esegui il codice:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

L'output stampato e i valori restituiti vengono inviati come testo. Le risposte tipiche sono:

| Stato | Significato |
| --- | --- |
| `200` | Il codice è stato eseguito |
| `401` | Il token bearer è mancante o non valido |
| `422` | Non è stato possibile analizzare o eseguire il codice Lua |
| `503` | L'ambiente delle estensioni dell'editor non è pronto |

Un client può riprovare dopo `503`, ma dovrebbe utilizzare un numero limitato di tentativi. Correggi il codice prima di ripetere una richiesta che ha restituito `422`.

Il codice valutato può utilizzare l'[API dell'editor](https://defold.com/ref/editor-lua/) e l'ambiente di scripting dell'editor. Non può utilizzare le API di runtime del gioco come `go.*` per manipolare un gioco in esecuzione. Per il gameplay, utilizza un test a runtime, il debugger, un test nel browser o un'[API di automazione a runtime](/manuals/engine-service/#automation-bridge-extension).

### Modificare risorse e file {#modifying-resources-and-files}

Molte risorse sorgente Defold utilizzano formati testuali e possono essere modificate con qualsiasi strumento di editing del testo. Per modificare risorse strutturate di un progetto Defold, prediligi le transazioni dell'editor.

| Modifica | Metodo preferito |
| --- | --- |
| Lua, shader, JSON o un altro formato testuale noto | Modifica diretta del file |
| Testo non salvato in una scheda aperta dell'editor | `editor.get()` e `editor.transact()` |
| Collection, game object, GUI, atlas o un'altra risorsa strutturata | Transazione dell'editor |
| Contenuti generati ripetutamente | Generatore autonomo |
| Operazione ripetibile sul progetto | Comando dell'editor o endpoint HTTP personalizzato |
| Trasformazione riservata alla CI | Script autonomo eseguito prima di Bob |

Ispeziona una risorsa prima di modificarla:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Controlla `editor.can_get()`, `editor.can_set()` e le altre funzioni `editor.can_*()` prima di eseguire una transazione.

Usa `editor.execute()` in Lua dell'editor per eseguire un formatter, un validatore o un generatore:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Quando il comando non modifica le risorse del progetto, imposta `reload_resources = false` per evitare un ricaricamento non necessario.

::: important
Non modificare i file in `.internal/` o i contenuti generati in `build/`.
:::

## Preferenze {#preferences}

Le preferenze dell'editor possono essere lette e scritte tramite il percorso documentato in OpenAPI, attualmente `/prefs/{path}`.

Ad esempio, puoi leggere la dimensione configurata del carattere del codice:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Oppure impostarla, ad esempio, su 16:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

L'editor convalida il valore rispetto allo schema delle preferenze. Un percorso o un valore non valido restituisce HTTP `400`.

Le preferenze sono impostazioni persistenti dell'utente o dell'utente del progetto, non configurazioni del progetto archiviate in `game.project`. Se l'automazione deve modificare temporaneamente una preferenza, salva il valore precedente e ripristinalo in seguito.

## Route definite dal progetto {#project-defined-routes}

Gli script dell'editor possono definire route aggiuntive con [`get_http_server_routes()`](/manuals/editor-scripts/#http-server). Una tabella facoltativa delle operazioni OpenAPI espone una route tramite lo stesso documento `/openapi.json` delle operazioni integrate.

Le route definite dal progetto possono fornire generazione di contenuti, convalida, report, controlli di localizzazione, analisi delle risorse, test specifici del progetto o un'interfaccia più piccola per un IDE o un controller esterno.

Una buona route dovrebbe eseguire un'unica operazione dal nome chiaro, convalidarne l'input, restituire un risultato strutturato, essere idempotente ove possibile e limitare le attività dispendiose.

Le route definite dal progetto non sono protette automaticamente dal token di `/eval`. Aggiungi autenticazione e controlli di sicurezza specifici del progetto quando una route esegue operazioni sensibili.

## Hook del ciclo di vita {#lifecycle-hooks}

Gli hook sono funzioni eseguibili prima e dopo le build, prima e dopo la creazione dei bundle e quando un processo di gioco viene avviato o terminato. Un progetto può contenere un file `hooks.editor_script` nella propria root. Soltanto il file hook nella root riceve questi eventi, offrendo al progetto un unico punto in cui definirne l'ordine.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Un errore generato da `on_build_started()` interrompe la build dell'editor. Gli hook del ciclo di vita vengono eseguiti soltanto nell'editor; inserisci la logica condivisa di convalida e generazione in script autonomi che possano essere richiamati anche dalla CI.

## Sicurezza e compatibilità {#security-and-compatibility}

Considera l'intero server dell'editor come un'interfaccia locale attendibile:

* Non esporre pubblicamente l'accesso alla porta.
* Proteggi `.internal/editor.token`; autorizza `/eval` per la sessione corrente.
* Non concedere a soggetti esterni accesso senza restrizioni a `/eval`.
* Mantieni il token nel livello di integrazione locale anziché nei prompt, nei report o nei log.
* Ricorda che le route definite dal progetto non ereditano l'autenticazione di `/eval`.
* Utilizza un `/openapi.json` aggiornato.
* Utilizza attese limitate per i comandi automatici asincroni e per l'avvio dell'editor.

## Server del motore {#engine-server}

Il server dell'editor appartiene al processo dell'editor. Un gioco in esecuzione dispone di una porta diversa e di responsabilità differenti, descritte nel [manuale del servizio del motore e dell'API HTTP a runtime](/manuals/engine-service).
