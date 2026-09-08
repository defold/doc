---
title: Manuale del ciclo di vita delle applicazioni Defold
brief: Questo manuale descrive in dettaglio il ciclo di vita dei giochi e delle applicazioni Defold.
---

# Ciclo di vita dell'applicazione {#application-lifecycle}

Il ciclo di vita di un'applicazione o di un gioco Defold è, a grandi linee, semplice. Il motore attraversa tre fasi di esecuzione: l'inizializzazione, il ciclo di aggiornamento (in cui applicazioni e giochi trascorrono la maggior parte del tempo) e la finalizzazione.

::: sidenote
Questo manuale riguarda le versioni di Defold a partire dalla 1.12.0. Nella versione 1.12.0 sono state introdotte modifiche al ciclo di vita e la nuova funzione `late_update()`.
:::

![Panoramica del ciclo di vita](images/application_lifecycle/application_lifecycle.png)

In molti casi è sufficiente una conoscenza di base del funzionamento interno di Defold. Potresti però incontrare casi particolari in cui l'ordine esatto in cui Defold esegue le proprie attività diventa fondamentale. Questo documento descrive come il motore esegue un'applicazione dall'inizio alla fine.

L'applicazione inizia inizializzando tutto ciò che serve per eseguire il motore. Carica la collezione principale e chiama [`init()`](/ref/go#init) su tutti i componenti caricati che dispongono di una funzione Lua `init()` (componenti script e componenti GUI con script GUI). Questo ti consente di eseguire un'inizializzazione personalizzata.

L'applicazione entra quindi nel ciclo di aggiornamento, dove trascorrerà la maggior parte della propria vita. A ogni fotogramma vengono aggiornati gli oggetti di gioco e i componenti che contengono. Vengono chiamate tutte le funzioni [`update()`](/ref/go#update) degli script e degli script GUI. Durante il ciclo di aggiornamento i messaggi vengono consegnati ai rispettivi destinatari, i suoni vengono riprodotti e viene eseguito il rendering di tutta la grafica.

A un certo punto, il ciclo di vita dell'applicazione giunge al termine. Prima che l'applicazione si chiuda, il motore esce dal ciclo di aggiornamento ed entra in una fase di finalizzazione. Prepara tutti gli oggetti di gioco caricati per l'eliminazione. Vengono chiamate tutte le funzioni [`final()`](/ref/go#final) dei componenti degli oggetti, consentendo di eseguire operazioni di pulizia personalizzate. Poi gli oggetti vengono eliminati e la collezione principale viene scaricata dalla memoria.

Per chiarezza, i passaggi dell'operazione di ["consegna dei messaggi"](#dispatching-messages) sono illustrati in un diagramma separato alla fine di questo manuale e sono contrassegnati nei diagrammi da una piccola icona a forma di "busta con una freccia" 📩.

## Inizializzazione {#initialization}

È qui che il tuo gioco inizia ed è il primo passo della sua esecuzione. Si può suddividere in 3 fasi:

![Inizializzazione](images/application_lifecycle/initialization.png)

### Preinizializzazione {#preinitialization}

Durante la fase `Preinitialization`, il motore esegue numerosi passaggi prima di caricare la collezione principale (di bootstrap). Vengono configurati il profilatore della memoria, i socket, la grafica, HID (dispositivi di input), l'audio, la fisica e molto altro. Viene inoltre caricata e applicata la configurazione dell'applicazione (*game.project*).

![Preinizializzazione](images/application_lifecycle/pre_init.png)

Il primo punto di ingresso controllabile dall'utente, al termine dell'inizializzazione del motore, è la chiamata alla funzione `init()` dello script di rendering corrente.

La collezione principale viene quindi caricata e inizializzata.

### Inizializzazione della collezione {#collection-init}

Durante la fase `Collection Init`, tutti gli oggetti di gioco della collezione applicano ai propri figli le loro trasformazioni: traslazione (cambio di posizione), rotazione e ridimensionamento. Vengono quindi chiamate tutte le funzioni `init()` presenti nei componenti.

![Inizializzazione della collezione](images/application_lifecycle/collection_init.png)

::: sidenote
L'ordine in cui vengono chiamate le funzioni `init()` dei componenti degli oggetti di gioco non è specificato. Non devi presumere che il motore inizializzi in un determinato ordine gli oggetti appartenenti alla stessa collezione.
:::

### Aggiornamento finale durante l'inizializzazione {#post-update-in-initialization}

Il motore esegue quindi un'intera fase `Post Update`, la stessa che in seguito viene eseguita dopo ogni iterazione di `Update Loop`. Viene eseguita al termine dell'inizializzazione perché il codice di `init()` può inviare nuovi messaggi, richiedere alle fabbriche (factory) di generare nuovi oggetti, contrassegnare oggetti per l'eliminazione ed eseguire altre azioni.

![Aggiornamento finale](images/application_lifecycle/post_init.png)

Questa fase consegna i messaggi, genera effettivamente gli oggetti di gioco tramite le fabbriche ed elimina gli oggetti. Tieni presente che la fase `Post Update` include una sequenza di "consegna dei messaggi" che, oltre a consegnare i messaggi in coda, elabora anche i messaggi inviati ai proxy di collezione. Tutti gli aggiornamenti successivi dei proxy (abilitazione, disabilitazione, inizializzazione, finalizzazione, caricamento e contrassegno per lo scaricamento) vengono eseguiti durante questi passaggi.

È del tutto possibile caricare un [proxy di collezione](/manuals/collection-proxy) durante `init()`, assicurarsi che tutti gli oggetti al suo interno siano inizializzati e poi scaricare la collezione dalla memoria tramite il proxy, il tutto prima che venga chiamata la prima funzione `update()` di un componente, cioè prima che il motore abbia lasciato la fase di inizializzazione e sia entrato nel ciclo di aggiornamento:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## Ciclo di aggiornamento {#update-loop}

Il ciclo `Update Loop` esegue una sequenza specifica una volta per fotogramma. Questa sequenza può essere suddivisa in 5 fasi principali:

![Ciclo di aggiornamento](images/application_lifecycle/update_loop.png)

1. Input (elaborazione e gestione)
2. Aggiornamento (che include gli aggiornamenti a passo fisso, regolari, tardivi e dei componenti del motore)
3. Aggiornamento del rendering
4. Aggiornamento finale (scaricamento dei proxy di collezione dalla memoria, generazione ed eliminazione degli oggetti di gioco)
5. Rendering del fotogramma (viene eseguito il rendering della grafica finale)

### Fase di input {#input-phase}

L'input viene letto dai dispositivi disponibili, associato ai [binding di input](/manuals/input) e quindi distribuito. Ogni oggetto di gioco che ha acquisito il focus dell'input riceve l'input nelle funzioni `on_input()` di tutti i suoi componenti. Un oggetto di gioco con un componente script e un componente GUI dotato di script GUI riceverà l'input nelle funzioni `on_input()` di entrambi i componenti, a condizione che siano definite e che abbiano acquisito il focus dell'input.

![Fase di input](images/application_lifecycle/input_phase.png)

Ogni oggetto di gioco che ha acquisito il focus dell'input e contiene componenti proxy di collezione distribuisce l'input ai componenti all'interno della collezione del proxy. Questo processo prosegue ricorsivamente nei proxy di collezione abilitati contenuti in altri proxy di collezione abilitati.

### Fase di aggiornamento {#update-phase}

La fase `Update` fa parte del ciclo `Update Loop`. Viene avviata una volta per la collezione radice, quindi viene eseguita ricorsivamente per ogni proxy di collezione abilitato.

All'interno di una collezione, Defold elabora le callback per tipo di componente: scorre tutte le istanze di un tipo di componente che implementa la fase in questione, chiama la callback Lua per ogni istanza, consegna i messaggi in coda e poi passa al tipo di componente successivo.

A grandi linee, l'ordine delle fasi delle callback Lua dei componenti *script* è il seguente:

1. `fixed_update()` - chiamata 0..N volte per fotogramma (se si usa un passo temporale fisso)
2. `update()` - chiamata 1 volta per fotogramma
3. `late_update()` - chiamata 1 volta per fotogramma

![Fase di aggiornamento](images/application_lifecycle/update_phase.png)


Viene esaminato ogni componente degli oggetti di gioco nella collezione principale. Se uno di questi componenti ha uno script con una funzione `fixed_update()`/`update()`/`late_update()`, questa viene chiamata. Se il componente è un proxy di collezione, ogni componente nella collezione del proxy viene aggiornato ricorsivamente eseguendo tutti i passaggi della fase `Update`.

::: sidenote
L'ordine in cui vengono chiamate le funzioni `update()` dei componenti degli oggetti di gioco non è specificato. Non devi presumere che il motore aggiorni in un determinato ordine gli oggetti appartenenti alla stessa collezione. Lo stesso vale per `fixed_update()` e `late_update()` (dalla versione 1.12.0).
:::

#### Fisica {#physics}

Per i componenti oggetto di collisione, i messaggi della fisica (collisioni, trigger, risposte ai ray cast ecc.) vengono distribuiti a tutto l'oggetto di gioco che li contiene, raggiungendo tutti i componenti che contengono uno script con la funzione `on_message()`.

Se per la simulazione fisica viene usato un [passo temporale fisso](/manuals/physics/#physics-updates), può essere chiamata anche la funzione `fixed_update()` in tutti i componenti script. Questa funzione è utile nei giochi basati sulla fisica quando vuoi manipolare gli oggetti fisici a intervalli regolari per ottenere una simulazione fisica stabile.

#### Trasformazioni {#transforms}

Prima dell'aggiornamento di **ogni** tipo di componente, più volte durante il ciclo `Update Loop`, se necessario vengono aggiornate le trasformazioni, applicando qualsiasi movimento, rotazione e ridimensionamento degli oggetti di gioco a ogni loro componente e ai componenti degli eventuali oggetti di gioco figli.

Alla fine del ciclo `Update Loop`, se necessario, viene eseguito un ulteriore aggiornamento finale delle trasformazioni.

#### Fase di aggiornamento del motore (senza aggiornamenti a passo fisso) {#engine-update-phase-no-fixed-updates}

Le tabelle seguenti descrivono le fasi di aggiornamento *a livello del motore*. Omettono volutamente l'esatto ordine di priorità interno dei componenti (che è un dettaglio di implementazione del motore), ma riflettono le garanzie sull'ordine rilevanti per gli script:

- `fixed_update()` viene eseguita prima di `update()`
- `late_update()` viene eseguita dopo `update()`
- i messaggi inviati vengono consegnati tra gli aggiornamenti dei diversi tipi di componente e anche tra le fasi delle callback degli script

Quando `Use Fixed Timestep` è `false` e/o Fixed Update Frequency è `0`, all'inizio della fase viene preparato `dt` e poi il flusso procede come illustrato nella tabella seguente:

:::sidenote
Tieni presente che dopo l'aggiornamento di **ogni** tipo di componente vengono consegnati tutti i messaggi; per mantenere la tabella seguente leggibile, questo passaggio non è indicato.
:::

| Passaggio | Fase del motore | Callback Lua | Commento |
|-|-|-|-|
| 1 | **Aggiornamento** | `update()` | Chiamata una volta per fotogramma per ogni tipo di componente che implementa l'aggiornamento, secondo l'ordine di priorità interno. Inoltre, qui vengono aggiornate come tipo di componente separato le animazioni delle proprietà degli oggetti di gioco avviate con `go.animate()`. Qui vengono aggiornati i componenti della **fisica**. Per ogni proxy di collezione abilitato, l'intera fase `Update` viene chiamata ricorsivamente dal passaggio 1. |
| 2 | **Aggiornamento tardivo** | `late_update()` | Chiamata una volta per fotogramma per ogni tipo di componente che implementa l'aggiornamento tardivo, secondo l'ordine di priorità interno. |
| 3 | **Trasformazioni** | | Alla fine, se necessario, viene eseguito un ulteriore aggiornamento finale delle trasformazioni per ogni componente. |

#### Fase di aggiornamento del motore con passo temporale fisso {#engine-update-phase-with-fixed-timestep}

Quando `Use Fixed Timestep` è `true` e Fixed Update Frequency è diverso da zero, all'inizio della fase vengono preparati `dt` (tempo trascorso), `fixed_dt` e `num_fixed_steps` (`0..N`), cioè il numero di volte in cui verrà chiamato l'aggiornamento a passo fisso, determinato dal tempo trascorso dall'ultimo aggiornamento per garantire un numero fisso di aggiornamenti.

:::sidenote
Tieni presente che dopo l'aggiornamento di **ogni** tipo di componente vengono consegnati tutti i messaggi; per mantenere la tabella seguente leggibile, questo passaggio non è indicato.
:::

Il ciclo procede quindi così:

| Passaggio | Fase del motore | Callback Lua | Commento |
|-|-|-|-|
| 1 | **Aggiornamento a passo fisso** | `fixed_update()` | Chiamata `0..N` volte per fotogramma in base al tempo trascorso, per ogni tipo di componente che implementa l'aggiornamento a passo fisso, secondo l'ordine di priorità interno. Include i passaggi di aggiornamento a passo fisso dei componenti della *fisica*. |
| 2 | **Aggiornamento** | `update()` | Chiamata una volta per fotogramma per ogni tipo di componente che implementa l'aggiornamento, secondo l'ordine di priorità interno. Inoltre, qui vengono aggiornate come tipo di componente separato le animazioni delle proprietà degli oggetti di gioco avviate con `go.animate()`. Per ogni proxy di collezione abilitato, la fase `Update` viene chiamata ricorsivamente dal passaggio 1. |
| 3 | **Aggiornamento tardivo** | `late_update()` | Chiamata una volta per fotogramma per ogni tipo di componente che implementa l'aggiornamento tardivo, secondo l'ordine di priorità interno. |
| 4 | **Trasformazioni** | | Alla fine, se necessario, viene eseguito un ulteriore aggiornamento finale delle trasformazioni per ogni componente. |

Se hai bisogno di maggiori dettagli sul funzionamento interno di Defold durante la fase di aggiornamento, è utile leggere direttamente il codice di [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Fase di aggiornamento del rendering {#render-update-phase}

Il blocco di aggiornamento del rendering consegna prima tutti i messaggi inviati al socket `@render` (per esempio i messaggi `set_view_projection` del componente camera, i messaggi `set_clear_color` ecc.). Viene poi chiamata la funzione `update()` dello script di rendering.

![Fase di aggiornamento del rendering](images/application_lifecycle/render_update_phase.png)

### Fase di aggiornamento finale {#post-update-phase}

Dopo gli aggiornamenti viene eseguita una sequenza di aggiornamento finale. Questa scarica dalla memoria i proxy di collezione contrassegnati per lo scaricamento (ciò avviene durante la sequenza di "consegna dei messaggi"). Per ogni oggetto di gioco contrassegnato per l'eliminazione vengono chiamate tutte le funzioni `final()` dei suoi componenti, se presenti. Il codice nelle funzioni `final()` spesso aggiunge nuovi messaggi alla coda, quindi in seguito viene eseguita l'operazione di "consegna dei messaggi".

![Fase di aggiornamento finale](images/application_lifecycle/post_update_phase.png)

Successivamente, ogni componente fabbrica a cui è stato richiesto di generare un oggetto di gioco lo genera. Infine, gli oggetti di gioco contrassegnati per l'eliminazione vengono effettivamente eliminati.

### Fase di rendering {#render-phase}

L'ultimo passaggio del ciclo di aggiornamento prevede la consegna dei messaggi `@system` (messaggi `exit` e `reboot`, attivazione e disattivazione del profilatore, avvio e arresto dell'acquisizione video ecc.).

![Fase di rendering](images/application_lifecycle/render_phase.png)

Viene quindi eseguito il rendering della grafica, incluso quello dell'eventuale profilatore visivo (consulta la [documentazione sul debug](/manuals/debugging)). Dopo il rendering della grafica viene effettuata l'acquisizione video.

#### Frequenza dei fotogrammi e passo temporale della collezione {#frame-rate-and-collection-time-step}

Il numero di aggiornamenti dei fotogrammi al secondo (che corrisponde al numero di esecuzioni del ciclo di aggiornamento al secondo) può essere impostato nelle impostazioni del progetto oppure tramite codice, inviando un messaggio `set_update_frequency` al socket `@system`. Inoltre, è possibile impostare singolarmente il _passo temporale_ dei proxy di collezione inviando un messaggio `set_time_step` al proxy. Modificare il passo temporale di una collezione non influisce sulla frequenza dei fotogrammi. Influisce invece sul passo temporale degli aggiornamenti della fisica e sulla variabile `dt` passata a `update().` Tieni inoltre presente che modificare il passo temporale non cambia il numero di volte in cui `update()` viene chiamata a ogni fotogramma: è sempre esattamente una.

(Consulta il [manuale dei proxy di collezione](/manuals/collection-proxy) e [`set_time_step`](/ref/collectionproxy#set-time-step) per maggiori dettagli)

#### Limitazione dell'attività del motore {#engine-throttling}

Defold 1.12.0 ha introdotto un'API per limitare l'attività del motore che può saltare completamente gli aggiornamenti del motore e il rendering, continuando però a rilevare l'input. Qualsiasi input riattiva il motore, che può tornare a limitare la propria attività dopo un intervallo di attesa.

Consulta l'API `sys.set_engine_throttle()` per i dettagli e gli esempi d'uso.

## Finalizzazione {#finalization}

Quando l'applicazione si chiude, per prima cosa completa l'ultima sequenza del ciclo di aggiornamento, che scarica dalla memoria tutti i proxy di collezione, finalizzando ed eliminando tutti gli oggetti di gioco presenti nella collezione di ciascun proxy.

Una volta completata questa operazione, il motore entra in una sequenza di finalizzazione che gestisce la collezione principale e i suoi oggetti:

![Finalizzazione](images/application_lifecycle/finalization.png)

Per prima cosa vengono chiamate le funzioni `final()` dei componenti. Segue la consegna dei messaggi. Infine, tutti gli oggetti di gioco vengono eliminati e la collezione principale viene scaricata dalla memoria.

Il motore procede quindi alla chiusura interna dei sottosistemi: viene eliminata la configurazione del progetto, viene arrestato il profilatore della memoria e così via.

L'applicazione è ora completamente chiusa.

## Consegna dei messaggi {#dispatching-messages}

La **consegna dei messaggi** è un'operazione speciale che viene eseguita dopo l'aggiornamento di **ogni** tipo di componente, per esempio dopo l'aggiornamento degli sprite, degli script e dopo qualsiasi altra azione che possa inviare messaggi. Durante questa operazione vengono consegnati tutti i messaggi inviati che sono stati raccolti in una coda. Questi passaggi sono contrassegnati nei diagrammi da piccole icone a forma di "busta con una freccia" 📩.

![Consegna dei messaggi](images/application_lifecycle/dispatch_messages.png)

Dopo la consegna di tutti i **messaggi dell'utente** mediante la chiamata a `on_message()` per ogni componente, i messaggi speciali di Defold vengono gestiti nell'ordine seguente (illustrato anche nel diagramma) per ciascun proxy di collezione:

1. Messaggi `load` - caricano i proxy di collezione contrassegnati per il caricamento e inviano in risposta il messaggio `proxy_loaded`.
2. Messaggi `unload` - scaricano dalla memoria i proxy di collezione contrassegnati per lo scaricamento e inviano in risposta il messaggio `proxy_unloaded`.
3. Messaggi `init` - attivano la fase `Collection Init` per tutti i proxy di collezione da inizializzare.
4. Messaggi `final` - attivano `final()` su tutti i componenti del proxy contrassegnato per la finalizzazione.
5. Messaggi `enable` - abilitano il proxy di collezione, in modo che il ciclo `Update Loop` venga eseguito per esso nel fotogramma successivo; questo attiva implicitamente `init()` per ogni componente della collezione.
6. Messaggi `disable` - disabilitano il proxy di collezione, in modo che il ciclo `Update Loop` **non** venga eseguito per esso nel fotogramma successivo; ne interrompono completamente l'esecuzione di `Update Loop`.

Poiché il codice di `on_message()` di qualsiasi componente destinatario può inviare ulteriori messaggi, il sistema di consegna dei messaggi continua a consegnare ricorsivamente i messaggi inviati finché la coda non è vuota. Esiste però un limite al numero di passaggi che il sistema di consegna esegue sulla coda dei messaggi. Consulta [Catene di messaggi](/manuals/message-passing) per maggiori dettagli.
