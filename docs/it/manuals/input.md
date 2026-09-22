---
title: Input dai dispositivi in Defold
brief: Questo manuale spiega come funziona l'input, come acquisire le azioni di input e come creare script che vi reagiscano.
---

# Input

Tutti gli input dell'utente vengono acquisiti dal motore e inviati sotto forma di azioni ai componenti script e script GUI negli oggetti di gioco (game object) che hanno acquisito il focus dell'input e che implementano la funzione `on_input()`. Questo manuale spiega come configurare i binding per acquisire l'input e come creare codice che vi risponda.

Il sistema di input si basa su un insieme di concetti semplici e potenti, che ti consentono di gestire l'input nel modo più adatto al tuo gioco.

![Binding di input](images/input/overview.png)

Dispositivi
: I dispositivi di input integrati nel computer o nel dispositivo mobile, oppure collegati a essi, forniscono al runtime di Defold l'input grezzo a livello di sistema. Sono supportati i seguenti tipi di dispositivi:

  1. Tastiera (input da singoli tasti e immissione di testo)
  2. Mouse (posizione, clic dei pulsanti e azioni della rotellina)
  3. Tocco singolo e multitocco (su dispositivi iOS e Android e in HTML5 sui dispositivi mobili)
  4. Gamepad (secondo il supporto del sistema operativo e la mappatura nel file [gamepads](/manuals/input-gamepads/#gamepads-settings-file))

Binding di input
: Prima che l'input venga inviato a uno script, l'input grezzo del dispositivo viene convertito in *azioni* significative attraverso la tabella dei binding di input.

Azioni
: Le azioni sono identificate dai nomi (sottoposti a hash) elencati nel file dei binding di input. Ogni azione contiene anche dati pertinenti sull'input: se un pulsante è stato premuto o rilasciato, le coordinate del mouse e dei tocchi e così via.

Componenti in ascolto dell'input
: Qualsiasi componente script o script GUI può ricevere azioni di input *acquisendo il focus dell'input*. Più componenti possono essere in ascolto contemporaneamente.

Stack di input
: L'elenco dei componenti in ascolto dell'input, con il primo che ha acquisito il focus in fondo allo stack e l'ultimo in cima.

Consumo dell'input
: Uno script può scegliere di consumare l'input ricevuto, impedendo ai componenti in ascolto più in basso nello stack di riceverlo.

## Configurazione dei binding di input {#setting-up-input-bindings}

I binding di input sono una tabella valida per l'intero progetto che consente di specificare come convertire l'input dei dispositivi in *azioni* con un nome prima di inviarle ai componenti script e agli script GUI. Per creare un nuovo file di binding di input, <kbd>fai clic con il pulsante destro</kbd> in una posizione della vista *Assets* e seleziona <kbd>New... ▸ Input Binding</kbd>. Per fare in modo che il motore utilizzi il nuovo file, modifica la voce *Game Binding* in *game.project*.

![Impostazione del binding di input](images/input/setting.png)

Tutti i modelli di nuovo progetto creano automaticamente un file di binding di input predefinito, quindi in genere non è necessario crearne uno nuovo. Il file predefinito si chiama `game.input_binding` e si trova nella cartella `input` nella radice del progetto. <kbd>Fai doppio clic</kbd> sul file per aprirlo nell'editor:

![Configurazione dei binding di input](images/input/input_binding.png)

Per creare un nuovo binding, fai clic sul pulsante <kbd>+</kbd> in fondo alla sezione del tipo di trigger pertinente. Ogni voce ha due campi:

*Input*
: L'input grezzo da rilevare, selezionato da un elenco scorrevole degli input disponibili.

*Action*
: Il nome assegnato alle azioni di input quando vengono create e inviate agli script. Lo stesso nome di azione può essere assegnato a più input. Ad esempio, puoi associare il tasto <kbd>Space</kbd> e il pulsante `A` del gamepad all'azione `jump`. Tieni presente che, a causa di un bug noto, gli input tattili purtroppo non possono avere gli stessi nomi di azione degli altri input.

## Tipi di trigger {#trigger-types}

Puoi creare cinque tipi di trigger specifici per i dispositivi:

Key Triggers
: Input da singoli tasti della tastiera. Ogni tasto viene associato separatamente a un'azione corrispondente. Per saperne di più, consulta il [manuale sull'input da tastiera e sull'immissione di testo](/manuals/input-key-and-text).

Text Triggers
: I trigger di testo servono a leggere testo arbitrario immesso dall'utente. Per saperne di più, consulta il [manuale sull'input da tastiera e sull'immissione di testo](/manuals/input-key-and-text)

Mouse Triggers
: Input dai pulsanti e dalle rotelline del mouse. Per saperne di più, consulta il [manuale sull'input da mouse e tattile](/manuals/input-mouse-and-touch).

Touch Triggers
: I trigger di tipo Single-touch e Multi-touch sono disponibili sui dispositivi iOS e Android nelle applicazioni native e nei bundle HTML5. Per saperne di più, consulta il [manuale sul mouse e sul tocco](/manuals/input-mouse-and-touch).

Gamepad Triggers
: I trigger del gamepad consentono di associare gli input standard del gamepad alle funzioni del gioco. Per saperne di più, consulta il [manuale sui gamepad](/manuals/input-gamepads).

### Input dall'accelerometro {#accelerometer-input}

Oltre ai cinque tipi di trigger elencati sopra, Defold supporta anche l'input dall'accelerometro nelle applicazioni native Android e iOS. Seleziona la casella *Use Accelerometer* nella sezione *Input* del file *game.project*.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- react to accelerometer data
    end
end
```

## Focus dell'input {#input-focus}

Per ricevere le azioni di input in un componente script o in uno script GUI, invia il messaggio `acquire_input_focus` all'oggetto di gioco che contiene il componente:

```lua
-- tell the current game object (".") to acquire input focus
msg.post(".", "acquire_input_focus")
```

Questo messaggio indica al motore di aggiungere allo *stack di input* i componenti degli oggetti di gioco in grado di gestire l'input (componenti script, componenti GUI e proxy di collezione). I componenti degli oggetti di gioco vengono inseriti in cima allo stack di input; l'ultimo componente aggiunto si troverà in cima allo stack. Tieni presente che, se l'oggetto di gioco contiene più di un componente in grado di gestire l'input, tutti questi componenti verranno aggiunti allo stack:

![Stack di input](images/input/input_stack.png)

Se un oggetto di gioco che ha già acquisito il focus dell'input lo acquisisce di nuovo, i suoi componenti vengono spostati in cima allo stack.


## Distribuzione dell'input e on_input() {#input-dispatch-and-on_input}

Le azioni di input vengono distribuite seguendo lo stack di input, dall'alto verso il basso.

![Distribuzione delle azioni](images/input/actions.png)

Per ogni componente nello stack che contiene una funzione `on_input()`, questa funzione viene chiamata una volta per ciascuna azione di input durante il fotogramma, con i seguenti argomenti:

`self`
: L'istanza corrente dello script.

`action_id`
: Il nome dell'azione sottoposto a hash, come configurato nei binding di input.

`action`
: Una tabella contenente i dati utili sull'azione, come il valore dell'input, la sua posizione (assoluta e relativa allo spostamento), se l'input del pulsante è stato `pressed` e così via. Consulta [on_input()](/ref/go#on_input) per i dettagli sui campi disponibili dell'azione.

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- move left
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- move right
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Focus dell'input e componenti proxy di collezione {#input-focus-and-collection-proxy-components}

Ogni mondo di gioco caricato dinamicamente attraverso un proxy di collezione ha il proprio stack di input. Affinché la distribuzione delle azioni raggiunga lo stack di input del mondo caricato, il componente proxy deve trovarsi nello stack di input del mondo principale. Tutti i componenti nello stack di un mondo caricato vengono gestiti prima che la distribuzione prosegua verso il basso nello stack principale:

![Distribuzione delle azioni ai proxy](images/input/proxy.png)

::: important
Un errore comune è dimenticare di inviare `acquire_input_focus` all'oggetto di gioco che contiene il componente proxy di collezione. Saltare questo passaggio impedisce all'input di raggiungere qualsiasi componente nello stack di input del mondo caricato.
:::


### Rilascio dell'input {#releasing-input}

Per smettere di ricevere le azioni di input, invia un messaggio `release_input_focus` all'oggetto di gioco. Questo messaggio rimuove dallo stack di input tutti i componenti dell'oggetto di gioco:

```lua
-- tell the current game object (".") to release input focus.
msg.post(".", "release_input_focus")
```


## Consumo dell'input {#consuming-input}

La funzione `on_input()` di un componente può controllare attivamente se le azioni debbano essere trasmesse ai componenti più in basso nello stack:

- Se `on_input()` restituisce `false`, oppure non restituisce esplicitamente un valore (il che equivale a restituire `nil`, un valore considerato falso in Lua), le azioni di input vengono trasmesse al componente successivo nello stack di input.
- Se `on_input()` restituisce `true`, l'input viene consumato. Nessun componente più in basso nello stack di input riceverà l'input. Tieni presente che questo vale per *tutti* gli stack di input. Un componente nello stack di un mondo caricato tramite proxy può consumare l'input, impedendo ai componenti nello stack principale di riceverlo:

![Consumo dell'input](images/input/consuming.png)

In molti casi, il consumo dell'input offre un modo semplice e potente per passare la gestione dell'input da una parte del gioco a un'altra. Ad esempio, se hai bisogno di un menu a comparsa che sia temporaneamente l'unica parte del gioco in ascolto dell'input:

![Consumo dell'input](images/input/game.png)

Il menu di pausa è inizialmente nascosto (disabilitato) e viene abilitato quando il giocatore tocca l'elemento `PAUSE` dell'HUD:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- Did the player press PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Tell the pause menu to take over.
            msg.post("pause_menu", "show")
        end
    end
end
```

![Menu di pausa](images/input/game_paused.png)

La GUI del menu di pausa acquisisce il focus dell'input e consuma l'input, impedendo la gestione di qualsiasi input che non sia pertinente al menu a comparsa:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Show the pause menu.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Acquire input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- do things...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Hide the pause menu
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Release input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume all input. Anything below us on the input stack
  -- will never see input until we release input focus.
  return true
end
```
