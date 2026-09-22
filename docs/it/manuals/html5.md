---
title: Sviluppo con Defold per la piattaforma HTML5
brief: Questo manuale descrive il processo di creazione di un gioco HTML5, insieme ai problemi noti e alle limitazioni.
---

# Sviluppo HTML5 {#html5-development}

Defold supporta la creazione di giochi per la piattaforma HTML5 tramite il normale menu di creazione dei bundle, come per le altre piattaforme. Inoltre, il gioco risultante viene incorporato in una normale pagina HTML, il cui aspetto può essere personalizzato tramite un semplice sistema di modelli.

Il file *game.project* contiene le impostazioni specifiche per HTML5:

![Impostazioni del progetto](images/html5/html5_project_settings.png)

## Dimensione dell'heap {#heap-size}

Il supporto HTML5 di Defold si basa su Emscripten (vedi http://en.wikipedia.org/wiki/Emscripten). In breve, crea un'area di memoria isolata per l'heap in cui opera l'applicazione. Per impostazione predefinita, il motore alloca una quantità abbondante di memoria (256MB), che dovrebbe essere più che sufficiente per un gioco tipico. Durante l'ottimizzazione, puoi scegliere di usare un valore inferiore. Per farlo, segui questi passaggi:

1. Imposta *heap_size* sul valore desiderato, espresso in megabyte.
2. Crea il tuo bundle HTML5 (vedi sotto)

## Test di una build HTML5 {#testing-html5-build}

Per eseguire i test, una build HTML5 richiede un server HTTP. Defold ne crea uno per te se scegli <kbd>Project ▸ Build HTML5</kbd>.

![Build HTML5](images/html5/html5_build_launch.png)

Se vuoi testare il tuo bundle, caricalo sul tuo server HTTP remoto oppure crea un server locale, ad esempio usando Python nella cartella del bundle.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

oppure

```sh
python3 -m http.server
```

::: important
Non puoi testare il bundle HTML5 aprendo il file `index.html` in un browser. È necessario un server HTTP.
:::

::: important
Se nella console compare l'errore `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."`, assicurati che il server utilizzi il tipo MIME `application/wasm` per i file `.wasm`.
:::

## Creazione di un bundle HTML5 {#creating-html5-bundle}

Creare contenuti HTML5 con Defold è semplice e segue la stessa procedura delle altre piattaforme supportate: seleziona <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd> dal menu:

![Creazione di un bundle HTML5](images/html5/html5_bundle.png)

I bundle HTML5 supportano due architetture WebAssembly:

* `wasm-web` - il normale motore WebAssembly, senza thread.
* `wasm_pthread-web` - un motore WebAssembly che può utilizzare i thread.

Puoi includere una delle due architetture oppure entrambe. Quando sono incluse entrambe, il caricatore seleziona `wasm_pthread-web` se il browser e l'ambiente di hosting lo supportano, altrimenti utilizza `wasm-web`. Consulta il [manuale di Bob](/manuals/bob/#usage) per i nomi canonici delle piattaforme di destinazione.

::: important
Il motore con supporto dei thread richiede `SharedArrayBuffer` in una pagina sicura e [isolata dalle altre origini](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated). Servi il bundle tramite HTTPS (o localhost) e configura il server con intestazioni compatibili con l'isolamento tra origini, generalmente:

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Anche le risorse caricate dalla pagina da altre origini devono utilizzare intestazioni CORS o Cross-Origin-Resource-Policy compatibili. Un bundle che contiene solo `wasm_pthread-web` non può essere eseguito se questi requisiti non sono soddisfatti; includi `wasm-web` come alternativa se il gioco potrebbe essere ospitato su un sito che non supporta l'isolamento tra origini.
:::

I bundle HTML5 di Defold richiedono un browser moderno con supporto WebAssembly. Internet Explorer 11 non è supportato.

Quando fai clic sul pulsante <kbd>Create bundle</kbd>, ti verrà chiesto di selezionare una cartella in cui creare l'applicazione. Al termine dell'esportazione, troverai tutti i file necessari per eseguirla.

## Versione del contesto WebGL {#webgl-context-version}

Seleziona il contesto grafico da richiedere tramite [`graphics.webgl_version_hint`](/manuals/project-settings/#webgl-version-hint). Il valore predefinito è WebGL 2; richiedi WebGL 1 per provarlo o usarlo come destinazione nei browser che supportano entrambe le versioni.

## Verifica dei download {#download-verification}

Per impostazione predefinita, il loader HTML5 verifica le dimensioni dei file scaricati del motore e dell'archivio. Se una verifica fallisce, il download viene ritentato prima che il loader segnali un errore:

* Gli errori di rete, gli stati HTTP di errore e le dimensioni non corrispondenti nel download JavaScript o WebAssembly del motore usano il limite di tentativi di `html5.retry_count`.
* La verifica dei file di archivio ha un proprio limite di tentativi in caso di dimensioni o SHA-1 non corrispondenti. Ogni nuovo tentativo di verifica scarica nuovamente le parti del file, con i normali tentativi di rete disponibili per ogni download.

L'impostazione `html5.retry_time` controlla l'intervallo tra i tentativi in entrambi i casi.

Se il server, il proxy o la CDN riscrive intenzionalmente i file serviti e ne cambia le dimensioni, disabilita la verifica delle dimensioni in *game.project*:

```ini
[html5]
verify_downloaded_file_size = 0
```

Disabilitando **Verify Downloaded File Size**, le eventuali verifiche SHA-1 incluse nel bundle rimangono attive. Consulta le [impostazioni di progetto HTML5](/manuals/project-settings/#verify-downloaded-file-size).

## Problemi noti e limitazioni {#known-issues-and-limitations}

* Hot Reload - L'hot reload non funziona nelle build HTML5. Per ricevere aggiornamenti dall'editor, le applicazioni Defold devono eseguire un proprio piccolo server web, cosa che non è possibile in una build HTML5.
* Chrome
  * Build di debug lente - Nelle build di debug per HTML5, verifichiamo tutte le chiamate grafiche WebGL per rilevare errori. Purtroppo, questa operazione è molto lenta durante i test in Chrome. Puoi disabilitarla impostando il campo *Engine Arguments* di *game.project* su `--verify-graphics-calls=false`.
* Supporto dei gamepad - [Consulta la documentazione dei gamepad](/manuals/input-gamepads/#gamepads-in-html5) per le considerazioni specifiche e i passaggi che potrebbero essere necessari su HTML5.

## Personalizzazione di un bundle HTML5 {#customizing-html5-bundle}

Quando generi una versione HTML5 del tuo gioco, Defold fornisce una pagina web predefinita. Questa fa riferimento a risorse di stile e script che determinano come viene presentato il gioco.

A ogni esportazione dell'applicazione, questi contenuti vengono ricreati. Se desideri personalizzare uno di questi elementi, devi modificare le impostazioni del progetto. Per farlo, apri *game.project* nell'editor Defold e scorri fino alla sezione *html5*:

![Sezione HTML5](images/html5/html5_section.png)

Puoi trovare maggiori informazioni su ciascuna opzione nel [manuale delle impostazioni del progetto](/manuals/project-settings/#html5).

::: important
Non puoi modificare i file del modello HTML/CSS predefinito nella cartella `builtins`. Per applicare le tue modifiche, copia e incolla il file necessario da `builtins` e selezionalo in *game.project*.
:::

::: important
Non applicare bordi o spaziatura interna al canvas. In caso contrario, le coordinate dell'input del mouse saranno errate.
:::

In *game.project* puoi disattivare il pulsante `Fullscreen` e il link `Made with Defold`.
Defold fornisce un tema scuro e uno chiaro per `index.html`. Il tema chiaro è quello predefinito, ma puoi cambiarlo modificando il file `Custom CSS`. Nel campo `Scale Mode` puoi inoltre scegliere tra quattro modalità di ridimensionamento predefinite.

::: important
I calcoli per tutte le modalità di ridimensionamento includono i DPI attuali dello schermo se attivi l'opzione `High Dpi` in *game.project* (sezione `Display`)
:::

### Downscale Fit e Fit {#downscale-fit-and-fit}

Nella modalità `Fit`, il canvas viene ridimensionato per mostrare l'intero canvas del gioco sullo schermo mantenendo le proporzioni originali. L'unica differenza di `Downscale Fit` è che il ridimensionamento avviene solo se le dimensioni interne della pagina web sono inferiori a quelle del canvas originale del gioco; il canvas non viene ingrandito quando la pagina web è più grande.

![Sezione HTML5](images/html5/html5_fit.png)

### Stretch

Nella modalità `Stretch`, il canvas viene ridimensionato per riempire completamente lo spazio interno della pagina web.

![Sezione HTML5](images/html5/html5_stretch.png)

### No Scale
Con la modalità `No Scale`, le dimensioni del canvas sono esattamente quelle definite nel file *game.project*, nella sezione `[display]`.

![Sezione HTML5](images/html5/html5_no_scale.png)

## Token {#tokens}

Per creare il file `index.html` utilizziamo il [linguaggio di modelli Mustache](https://mustache.github.io/mustache.5.html). Durante la creazione di una build o di un bundle, i file HTML e CSS vengono elaborati da un compilatore in grado di sostituire determinati token con valori che dipendono dalle impostazioni del progetto. Questi token sono sempre racchiusi tra doppie o triple parentesi graffe (`{{TOKEN}}` o `{{{TOKEN}}}`), a seconda che le sequenze di caratteri debbano essere sottoposte a escape oppure no. Questa funzionalità può essere utile se modifichi spesso le impostazioni del progetto o se intendi riutilizzare il materiale in altri progetti.

::: sidenote
Puoi trovare maggiori informazioni sul linguaggio di modelli Mustache nel [manuale](https://mustache.github.io/mustache.5.html).
:::

Qualsiasi impostazione di *game.project* può essere usata come token. Ad esempio, se vuoi usare il valore `Width` della sezione `Display`:

![Sezione Display](images/html5/html5_display.png)

Apri *game.project* come testo e controlla `[section_name]` e il nome del campo che vuoi usare. Puoi quindi utilizzarlo come token: `{{section_name.field}}` o `{{{section_name.field}}}`.

![Sezione Display](images/html5/html5_game_project.png)

Ad esempio, nel codice JavaScript del modello HTML:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Sono disponibili anche i seguenti token personalizzati:

DEFOLD_SPLASH_IMAGE
: Inserisce il nome del file dell'immagine iniziale oppure `false` se `html5.splash_image` in *game.project* è vuoto


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: Il nome del progetto senza simboli non consentiti

DEFOLD_ARCHIVE_LOCATION_PREFIX
: Il prefisso risolto del percorso dell'archivio usato dal loader, basato su `html5.archive_location_prefix`.

DEFOLD_ARCHIVE_LOCATION_SUFFIX
: Il suffisso risolto aggiunto agli URL dell'archivio, basato su `html5.archive_location_suffix`.

DEFOLD_HAS_ARCHIVE_ORIGIN
: `true` quando il prefisso dell'archivio specifica un'origine HTTP o HTTPS, incluso un URL relativo al protocollo come `//cdn.example.com/archive`. È `false` per i prefissi di archivio relativi. Disponibile da Defold 1.13.2.

DEFOLD_ARCHIVE_ORIGIN
: L'origine dell'archivio, inclusi schema, host e porta facoltativa, oppure una stringa vuota quando non è specificata alcuna origine. Un prefisso relativo al protocollo produce un'origine relativa al protocollo. Usata per l'indicazione preconnect e disponibile da Defold 1.13.2.

DEFOLD_HAS_WASM_ENGINE
: `true` se il bundle include un motore WebAssembly, `wasm-web` oppure `wasm_pthread-web`.

DEFOLD_HAS_WASM_PTHREAD_ENGINE
: `true` se il bundle include `wasm_pthread-web`. Usalo per evitare di precaricare la variante sbagliata del motore quando il loader sceglie l'architettura a runtime.


DEFOLD_CUSTOM_CSS_INLINE
: Il punto in cui viene inserito direttamente il contenuto del file CSS specificato nelle impostazioni di *game.project*.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
È importante che questo blocco inline compaia prima del caricamento dello script principale dell'applicazione. Poiché include tag HTML, questa macro deve essere racchiusa tra triple parentesi graffe `{{{TOKEN}}}` per evitare che le sequenze di caratteri vengano sottoposte a escape.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Questo token è `true` se `html5.scale_mode` è `Downscale Fit`.

DEFOLD_SCALE_MODE_IS_FIT
: Questo token è `true` se `html5.scale_mode` è `Fit`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Questo token è `true` se `html5.scale_mode` è `No Scale`.

DEFOLD_SCALE_MODE_IS_STRETCH
: Questo token è `true` se `html5.scale_mode` è `Stretch`.

DEFOLD_HEAP_SIZE
: La dimensione dell'heap specificata in *game.project* con `html5.heap_size`, convertita in byte.

DEFOLD_ENGINE_ARGUMENTS
: Gli argomenti del motore specificati in *game.project* con `html5.engine_arguments`, separati dal simbolo `,`.

build-timestamp
: Il timestamp della build corrente in secondi.


## Parametri aggiuntivi {#extra-parameters}

Se crei un modello personalizzato, puoi modificare i parametri del caricatore del motore assegnando valori nell'oggetto globale `CUSTOM_PARAMETERS`. Il modello integrato fornisce un blocco `<script id="engine-setup">` intenzionalmente vuoto per queste personalizzazioni.
::: important
Mantieni il blocco `engine-setup` dopo lo script che carica `dmloader.js` e prima del blocco `engine-start` che chiama `EngineLoader.load()`.
:::
Ad esempio:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` può contenere, tra gli altri, i seguenti campi:

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## Operazioni sui file in HTML5 {#file-operations-in-html5}

Le build HTML5 supportano operazioni sui file come `sys.save()`, `sys.load()` e `io.open()`, ma la gestione interna di queste operazioni è diversa rispetto alle altre piattaforme. Quando JavaScript viene eseguito in un browser, non esiste un vero e proprio concetto di file system e l'accesso ai file locali è bloccato per motivi di sicurezza. Emscripten (e quindi Defold) usa invece [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), un database interno al browser che permette di memorizzare dati in modo persistente, per creare un file system virtuale nel browser. La differenza importante rispetto all'accesso al file system sulle altre piattaforme è che può esserci un leggero ritardo tra la scrittura in un file e l'effettiva memorizzazione della modifica nel database. La console per sviluppatori del browser consente generalmente di ispezionare il contenuto di IndexedDB.


## Passaggio di argomenti a un gioco HTML5 {#passing-arguments-to-an-html5-game}

A volte è necessario fornire argomenti aggiuntivi a un gioco prima o durante il suo avvio. Potrebbe trattarsi, ad esempio, di un ID utente, di un token di sessione o del livello da caricare all'avvio del gioco. Puoi farlo in diversi modi, alcuni dei quali sono descritti qui.

### Argomenti del motore {#engine-arguments}

Puoi specificare argomenti aggiuntivi del motore durante la sua configurazione e il suo caricamento. Questi argomenti possono essere recuperati durante l'esecuzione tramite `sys.get_config_string()`. Assegna gli argomenti direttamente a `CUSTOM_PARAMETERS.engine_arguments` nel blocco `engine-setup` di `index.html`:


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

L'assegnazione di un nuovo array sostituisce tutti gli argomenti del motore configurati in *game.project*. Per conservare questi argomenti e aggiungerne un altro, usa invece `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")`.

Puoi anche aggiungere `--config=example.foo1=bar1, --config=example.foo2=bar2` al campo *Engine Arguments* nella sezione HTML5 di *game.project*. I valori separati da virgole vengono aggiunti a `CUSTOM_PARAMETERS.engine_arguments` nel file `dmloader.js` generato.

Durante l'esecuzione, puoi ottenere i valori in questo modo:

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Argomenti di query nell'URL {#query-arguments-in-the-url}

Puoi passare argomenti come parametri di query nell'URL della pagina e leggerli durante l'esecuzione:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Una funzione ausiliaria completa per ottenere tutti i parametri di query come tabella Lua:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Ottimizzazioni {#optimizations}
I giochi HTML5 hanno generalmente requisiti rigorosi in termini di dimensioni del download iniziale, tempo di avvio e utilizzo della memoria, affinché si carichino rapidamente e funzionino bene anche su dispositivi poco potenti e con connessioni Internet lente. Per ottimizzare un gioco HTML5, si consiglia di concentrarsi sui seguenti aspetti:

* [Utilizzo della memoria](/manuals/optimization-memory)
* [Dimensioni del motore](/manuals/optimization-size)
* [Dimensioni del gioco](/manuals/optimization-size)

## FAQ
:[HTML5 FAQ](../shared/html5-faq.md)
