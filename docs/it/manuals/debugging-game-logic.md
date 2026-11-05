---
title: Debug in Defold
brief: Questo manuale spiega gli strumenti di debug disponibili in Defold.
---

# Debug della logica di gioco {#debugging-game-logic}

Defold include un debugger Lua integrato con funzioni di ispezione. Insieme agli [strumenti di profilazione](/manuals/profiling) integrati, è uno strumento potente che può aiutarti a trovare la causa dei bug nella logica di gioco o ad analizzare problemi di prestazioni.

## Debug con stampe e visualizzazioni {#print-and-visual-debugging}

Il modo più semplice per eseguire il debug di un gioco in Defold è usare il [debug tramite istruzioni di stampa](http://en.wikipedia.org/wiki/Debugging#Techniques). Usa le istruzioni `print()` o [`pprint()`](/ref/builtins#pprint) per osservare le variabili o indicare il flusso di esecuzione. Se un oggetto di gioco privo di script si comporta in modo strano, puoi semplicemente aggiungergli uno script con il solo scopo di eseguire il debug. Tutte le funzioni di stampa scrivono nella vista *Console* dell'editor e nel [log del gioco](/manuals/debugging-game-and-system-logs).

Oltre a stampare, il motore può anche disegnare testo di debug e linee rette sullo schermo. Per farlo, invia messaggi al socket `@render`:

```lua
-- Draw value of "my_val" with debug text on the screen
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Draw colored text on the screen
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Draw debug line between player and enemy on the screen
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

I messaggi di debug visivo aggiungono dati alla pipeline di rendering, che li disegna durante la normale esecuzione.

* `"draw_line"` aggiunge dati che vengono disegnati con la funzione `render.draw_debug3d()` nello script di rendering.
* `"draw_text"` viene disegnato con il font `/builtins/fonts/debug/always_on_top.font`, che usa il materiale `/builtins/fonts/debug/always_on_top_font.material`.
* `"draw_debug_text"` equivale a `"draw_text"`, ma viene disegnato con un colore personalizzato.

Probabilmente vorrai aggiornare questi dati a ogni fotogramma, quindi è consigliabile inviare i messaggi nella funzione `update()`.

## Avvio del debugger {#running-the-debugger}

Il debugger Lua è disponibile nelle build native di debug e headless. Usa un motore della stessa versione di Defold dell'editor. Le build di release e Web non supportano il collegamento del debugger.

Per avviare il debugger, seleziona <kbd>Debug ▸ Start/Attach</kbd>. Il comando avvia il gioco con il debugger collegato oppure collega il debugger a un gioco già in esecuzione. Quando avvia un gioco per il debug, l'editor installa i breakpoint abilitati prima di eseguire gli script di avvio, così puoi impostare un breakpoint in `init()` prima del lancio.

Per collegarti a un dispositivo, selezionalo in <kbd>Project ▸ Targets</kbd>, quindi scegli <kbd>Debug ▸ Start/Attach</kbd>. Il collegamento sospende l'esecuzione alla riga Lua successiva. L'editor configura automaticamente la connessione del debugger per le destinazioni locali e remote supportate. Consulta [Destinazioni remote](#remote-targets) per i requisiti di connessione oppure scopri come [collegare un debugger esterno](#native-dap-connections).

![panoramica](images/debugging/overview.png)

Non appena il debugger è collegato, puoi controllare l'esecuzione del gioco tramite i pulsanti del debugger nella console o tramite il menu <kbd>Debug</kbd>:

Break
: ![pausa](images/debugging/pause.svg){width=60px .left}
  Sospende l'esecuzione Lua alla riga sorgente successiva. Puoi quindi ispezionare lo stato del gioco, avanzare passo per passo o riprendere l'esecuzione fino al breakpoint successivo. Il punto di esecuzione corrente è indicato nell'editor di codice:

  ![script](images/debugging/script.png)

Continue
: ![ripresa](images/debugging/play.svg){width=60px .left}
  Riprendi l'esecuzione del gioco. Il codice del gioco continuerà a essere eseguito finché non premi il pulsante di pausa o l'esecuzione raggiunge un punto di interruzione che hai impostato. Se l'esecuzione si ferma in un punto di interruzione impostato, il punto di esecuzione viene evidenziato nell'editor di codice sopra l'indicatore del punto di interruzione:

  ![interruzione](images/debugging/break.png)

Stop
: ![arresto](images/debugging/stop.svg){width=60px .left}
  Arresta il debugger. Premendo questo pulsante, il debugger viene immediatamente arrestato e scollegato dal gioco, e il gioco in esecuzione viene terminato.

Step Over
: ![passo senza entrare nella funzione](images/debugging/step_over.svg){width=60px .left}
  Fai avanzare l'esecuzione del programma di un passo. Se l'esecuzione prevede una chiamata a un'altra funzione Lua, l'esecuzione _non entrerà nella funzione_, ma proseguirà e si fermerà alla riga successiva alla chiamata. In questo esempio, se premi "step over", il debugger eseguirà il codice e si fermerà all'istruzione `end` sotto la riga che contiene la chiamata alla funzione `nextspawn()`:

  ![passo](images/debugging/step.png)

::: sidenote
L'esecuzione passo per passo segue le righe sorgente Lua. Un passo può tornare sulla stessa riga, per esempio quando si ripete un ciclo, quindi non avanza sempre alla riga successiva nel file.
:::

Step Into
: ![passo dentro la funzione](images/debugging/step_in.svg){width=60px .left}
  Fai avanzare l'esecuzione del programma di un passo. Se l'esecuzione prevede una chiamata a un'altra funzione Lua, l'esecuzione _entrerà nella funzione_. La chiamata alla funzione aggiunge una voce allo stack delle chiamate. Puoi fare clic su ogni voce nell'elenco dello stack delle chiamate per vedere il punto di ingresso e il contenuto di tutte le variabili in quella chiusura. Qui l'esecuzione è entrata nella funzione `nextspawn()`:

  ![ingresso nella funzione](images/debugging/step_into.png)

Step Out
: ![uscita dalla funzione](images/debugging/step_out.svg){width=60px .left}
  Continua l'esecuzione fino al ritorno dalla funzione corrente. Se hai fatto avanzare l'esecuzione all'interno di una funzione, premendo il pulsante "step out" l'esecuzione continuerà finché la funzione non termina e restituisce il controllo.

Impostazione e rimozione dei punti di interruzione
: Puoi impostare un numero arbitrario di punti di interruzione nel codice Lua. Quando il gioco viene eseguito con il debugger collegato, l'esecuzione si fermerà al prossimo punto di interruzione che incontra e attenderà un tuo ulteriore intervento.

  ![aggiunta di un punto di interruzione](images/debugging/add_breakpoint.png)

  Per impostare o rimuovere un punto di interruzione, fai clic nella colonna immediatamente a destra dei numeri di riga nell'editor di codice. Puoi anche selezionare <kbd>Edit ▸ Toggle Breakpoint</kbd> dal menu.

Disattivazione e attivazione dei punti di interruzione
: Puoi disattivare temporaneamente i punti di interruzione senza rimuoverli. Quando sono disattivati, vengono ignorati durante l'esecuzione, ma puoi riattivarli in qualsiasi momento. Fai clic con il pulsante destro del mouse sul punto di interruzione nel margine dell'editor di codice, quindi seleziona o deseleziona la casella `Enabled`. I punti di interruzione disattivati appaiono vuoti all'interno per indicare che sono inattivi.

  ![disattivazione di un punto di interruzione](images/debugging/disable_breakpoint.png)

Impostazione dei punti di interruzione condizionali
: Puoi configurare un punto di interruzione in modo che contenga una condizione che deve risultare vera affinché il punto di interruzione si attivi. La condizione può accedere alle variabili locali disponibili in quella riga durante l'esecuzione del codice.

  ![modifica di un punto di interruzione](images/debugging/edit_breakpoint.png)

  Per modificare la condizione del punto di interruzione, fai clic con il pulsante destro del mouse nella colonna immediatamente a destra dei numeri di riga nell'editor di codice oppure seleziona <kbd>Edit ▸ Edit Breakpoint</kbd> dal menu.

Valutazione delle espressioni Lua
: Con il gioco in pausa, seleziona un frame in *Call Stack*, digita un'espressione o un'istruzione Lua nella parte inferiore della console e premi <kbd>Enter</kbd>. La valutazione usa le variabili locali, gli upvalue e le variabili globali del frame selezionato. I risultati di tipo tabella comprendono i contenuti annidati.

  ![console](images/debugging/console.png)

  Puoi anche modificare i valori tramite assegnazioni, per esempio `self.score = 100` in un frame in cui è disponibile `self`. Il codice valutato ha sullo stato del gioco gli stessi effetti del codice eseguito dal gioco.

Ispezione delle variabili
: Seleziona un frame in *Call Stack* per ispezionarne le variabili locali e gli upvalue nella vista *Variables*. Espandi `_G` per ispezionare le variabili globali ed espandi le tabelle o `self` per ispezionarne i campi. L'editor conserva i percorsi espansi, la selezione e la posizione di scorrimento durante l'esecuzione passo per passo, il cambio di frame o l'aggiornamento dopo una valutazione, recuperando i valori correnti.

Scollegamento del debugger
: Seleziona <kbd>Debug ▸ Detach Debugger</kbd> per scollegare il debugger dal gioco. L'esecuzione riprende immediatamente. Usa <kbd>Debug ▸ Start/Attach</kbd> per ricollegarti senza riavviare il gioco.

## Connessioni DAP native {#native-dap-connections}

Il motore fornisce un server nativo Debug Adapter Protocol (DAP) su TCP. Per usare un client DAP esterno, avvia il listener in un motore Defold nativo di debug o headless, quindi collega il client all'indirizzo e alla porta del motore. L'editor configura automaticamente il listener quando usi <kbd>Debug ▸ Start/Attach</kbd>.

L'editor corrente non può collegarsi ai motori precedenti che supportano soltanto MobDebug. Nelle versioni correnti la chiamata `require "builtins.scripts.mobdebug"` non è necessaria né disponibile.

### Avvio del listener {#starting-the-listener}

Prima crea una build del progetto. Dalla directory del progetto che contiene `build/default/game.projectc`, esegui il motore nativo di debug con queste [sostituzioni della configurazione all'avvio](/manuals/project-settings/#setting-config-values-on-engine-startup):

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

Collega il client DAP a `127.0.0.1:8172`. Il motore attende che il client configuri i breakpoint prima di eseguire gli script di avvio.

| Impostazione | Valore predefinito | Funzione |
| --- | --- | --- |
| `debugger.enabled` | `0` | Imposta a `1` per avviare il listener durante l'avvio del motore. |
| `debugger.address` | `127.0.0.1` | Indirizzo IPv4 su cui ascoltare. Il valore predefinito accetta connessioni dallo stesso computer. |
| `debugger.port` | `8172` | Porta TCP di ascolto. Usa `0` per selezionare una porta disponibile. |
| `debugger.wait` | `0` | Imposta a `1` per attendere la configurazione del client debugger prima di eseguire gli script di avvio. |

Puoi anche aggiungere questi valori alla [sezione Debugger di game.project](/manuals/project-settings/#debugger). L'editor configura automaticamente il listener per <kbd>Debug ▸ Start/Attach</kbd>, quindi la configurazione manuale serve soltanto quando avvii tu il listener.

Il log del motore riporta l'indirizzo e la porta selezionati. Con `debugger.wait=0`, il gioco parte immediatamente e puoi collegarti in seguito. Con `debugger.wait=1`, attende che il client completi la configurazione della sessione, compresi i breakpoint. Per i lanci locali di debug, l'editor seleziona automaticamente una porta disponibile.

Scollegare un client riprende l'esecuzione e lascia il listener disponibile per un nuovo collegamento. Anche uno scollegamento durante l'attesa della configurazione iniziale sblocca il motore. Se il listener non può avviarsi, il motore registra l'errore e prosegue l'avvio; puoi riprovare da Lua con `debugger.start(0)` per selezionare una porta disponibile.

### Abilitazione del listener durante l'esecuzione {#enabling-the-listener-while-running}

Per abilitare il listener da uno script senza riavviare il gioco:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` restituisce immediatamente la porta di ascolto. Non attende un client e non mette in pausa il gioco. Gli argomenti omessi usano `debugger.port` e `debugger.address`; passando `0` si seleziona una porta disponibile. Le chiamate ripetute restituiscono la porta del listener esistente senza cambiarne indirizzo o porta. Il modulo `debugger` è fornito dai motori nativi di debug e headless.

La porta deve essere un intero compreso tra `0` e `65535`. Passa `nil` come primo argomento per sostituire soltanto l'indirizzo. Argomenti non validi o l'impossibilità di associare il listener generano un errore Lua.

### Destinazioni remote {#remote-targets}

Per una connessione diretta da un altro computer, associa il listener all'interfaccia IPv4 del dispositivo o a `0.0.0.0` (tutte le interfacce IPv4). Per esempio, usa `debugger.start(8172, "0.0.0.0")` oppure aggiungi `--config=debugger.address=0.0.0.0` al comando di avvio precedente. Collega il client all'indirizzo IP effettivo del dispositivo e consenti l'accesso TCP alla porta di ascolto. `0.0.0.0` è un indirizzo di associazione, non l'indirizzo da inserire nel client.

L'editor Defold richiede automaticamente questa associazione remota e usa la porta `8172 + project.instance_index` per le destinazioni remote. Non può rilevare una porta remota selezionata dinamicamente. Se hai già avviato il listener remoto su localhost o su una porta diversa, riavvia il motore prima di collegarti dall'editor.

Il debugger può valutare codice Lua e non dispone di autenticazione. Abilita l'accesso remoto soltanto su una rete di sviluppo affidabile.

### Client esterni {#external-clients}

Usa un client che supporti il collegamento diretto a un server DAP su TCP. Configura la mappatura dei sorgenti alla cartella contenente `game.project` (l'argomento DAP di collegamento `localRoot`). Avvia prima il listener del motore, quindi collega il client.

#### VS Code

Installa l'[estensione Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`), apri in VS Code la cartella contenente `game.project` e aggiungi questa configurazione a `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

Se VS Code apre un file `.script`, `.gui_script` o `.render_script` come testo semplice, seleziona **Lua** dall'indicatore della lingua nella barra di stato prima di impostare i breakpoint.

Imposta un breakpoint, per esempio nella funzione `init()` di uno script. Avvia il motore usando il [comando di avvio precedente](#starting-the-listener), quindi seleziona **Attach to Defold Lua** nella vista **Run and Debug** di VS Code. Con `debugger.wait=1`, il motore esegue gli script di avvio dopo che il client ha installato i breakpoint. Imposta `stopOnEntry` a `true` se vuoi anche fermarti alla riga Lua successiva dopo il collegamento.

L'[impostazione `debugServer`](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug) di VS Code si collega direttamente al listener TCP locale del motore. Il campo `address` è richiesto dalla configurazione di collegamento dell'estensione Lua Debug. Se cambi la porta del listener, aggiorna entrambi i campi. `localRoot` deve indicare la cartella del progetto affinché il client possa associare i nomi dei sorgenti Lua del motore ai tuoi file.

Per un motore remoto, inoltra la sua porta DAP a localhost e inserisci la porta inoltrata in entrambi i campi, oppure usa un client DAP che si colleghi direttamente all'host remoto.

## Scheda Breakpoints {#breakpoints-tab}

  ![scheda Breakpoints](images/debugging/breakpoints_tab.png)

  Quando lavori con più punti di interruzione in script diversi, la scheda Breakpoints offre una vista centralizzata per gestirli tutti in un unico posto.

##### Controlli dei singoli punti di interruzione {#individual-breakpoint-controls}

  Per lavorare con i singoli punti di interruzione:
  - Fai clic sull'icona rossa del cestino per rimuovere un punto di interruzione
  - Fai doppio clic sulla riga (fuori dall'area della condizione) per passare a quella riga nella Code View
  - Fai doppio clic sulla cella della condizione o fai clic sull'icona della penna per modificare i punti di interruzione condizionali
  - Fai clic sul pulsante X che compare quando passi il puntatore sopra la cella di una condizione per cancellarla

##### Operazioni in blocco {#batch-operations}

  Seleziona più punti di interruzione usando Ctrl/Cmd+clic o Shift+clic, quindi fai clic con il pulsante destro del mouse per eseguire operazioni in blocco. Puoi modificare le condizioni di più punti di interruzione contemporaneamente, attivarli o disattivarli, oppure rimuoverli del tutto.

  I pulsanti della barra degli strumenti permettono di attivare, disattivare o invertire lo stato di tutti i punti di interruzione contemporaneamente: è utile quando vuoi eseguire il gioco senza fermarlo, ma vuoi conservarne le posizioni. Puoi anche rimuoverli tutti al termine della sessione di debug.

## Libreria di debug di Lua {#lua-debug-library}

Lua include una libreria di debug utile in alcune situazioni, soprattutto se devi ispezionare i meccanismi interni dell'ambiente Lua. Puoi trovare maggiori informazioni nel [capitolo sulla libreria di debug nel manuale Lua](http://www.lua.org/pil/contents.html#23).

## Lista di controllo per il debug {#debugging-checklist}

Se riscontri un errore o il gioco non si comporta come previsto, ecco una lista di controllo per il debug:

1. Controlla l'output della console e verifica che non ci siano errori durante l'esecuzione.

2. Aggiungi istruzioni `print` al codice per verificare che venga effettivamente eseguito.

3. Se non viene eseguito, controlla di aver effettuato nell'editor la configurazione necessaria per eseguire il codice. Lo script è stato aggiunto all'oggetto di gioco corretto? Lo script ha acquisito il focus dell'input? I trigger di input sono corretti? Il codice dello shader è stato aggiunto al materiale? E così via.

4. Se il codice dipende dai valori di alcune variabili (per esempio in un'istruzione if), usa `print` per stampare quei valori dove vengono usati o verificati, oppure ispezionali con il debugger.

A volte trovare un bug può essere un processo difficile e lungo, che richiede di esaminare il codice un pezzo alla volta, controllando tutto, circoscrivendo il codice difettoso ed eliminando le possibili fonti di errore. Il metodo più adatto è quello chiamato "dividi e conquista":

1. Individua la metà (o una porzione più piccola) del codice che deve contenere il bug.
2. Individua di nuovo quale metà di quella porzione deve contenere il bug.
3. Continua a restringere la porzione di codice che deve causare il bug finché non lo trovi.

Buona caccia!

## Debug dei problemi con la fisica {#debugging-problems-with-physics}

Se riscontri problemi con la fisica e le collisioni non funzionano come previsto, è consigliabile attivare il debug della fisica. Seleziona la casella *Debug* nella sezione *Physics* del file *game.project*:

![impostazione di debug della fisica](images/debugging/physics_debug_setting.png)

Quando questa casella è selezionata, Defold disegna tutte le forme di collisione e i punti di contatto delle collisioni:

![visualizzazione di debug della fisica](images/debugging/physics_debug_visualisation.png)
