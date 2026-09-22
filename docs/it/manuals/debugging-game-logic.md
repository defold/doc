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

Per avviare il debugger, seleziona <kbd>Debug ▸ Start/Attach</kbd>: il comando avvia il gioco con il debugger collegato oppure collega il debugger a un gioco già in esecuzione.

![panoramica](images/debugging/overview.png)

Non appena il debugger è collegato, puoi controllare l'esecuzione del gioco tramite i pulsanti del debugger nella console o tramite il menu <kbd>Debug</kbd>:

Break
: ![pausa](images/debugging/pause.svg){width=60px .left}
  Sospendi immediatamente l'esecuzione del gioco. Il gioco si fermerà nel punto corrente. Ora puoi ispezionare lo stato del gioco, farlo avanzare passo dopo passo oppure riprendere l'esecuzione fino al prossimo punto di interruzione. Il punto di esecuzione corrente è evidenziato nell'editor di codice:

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
Una riga di codice Lua non corrisponde a una singola espressione. L'avanzamento per passi nel debugger procede un'espressione alla volta: attualmente potresti quindi dover premere il pulsante di avanzamento più di una volta per passare alla riga successiva.
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
: Con il debugger collegato e il gioco fermo a un punto di interruzione, è disponibile un runtime Lua con il contesto corrente. Digita le espressioni Lua nella parte inferiore della console e premi <kbd>Enter</kbd> per valutarle:

  ![console](images/debugging/console.png)

  Attualmente non è possibile modificare le variabili tramite il valutatore.

Scollegamento del debugger
: Seleziona <kbd>Debug ▸ Detach Debugger</kbd> per scollegare il debugger dal gioco. Il gioco riprenderà immediatamente l'esecuzione.

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
