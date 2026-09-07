---
title: Input da mouse e tocco in Defold
brief: Questo manuale spiega come funziona l'input da mouse e tocco.
---

::: sidenote
Ti consigliamo di familiarizzare con il funzionamento generale dell'input in Defold, con le modalità di ricezione dell'input e con l'ordine in cui viene ricevuto nei file di script. Per saperne di più sul sistema di input, consulta il [manuale introduttivo sull'input](/manuals/input).
:::

# Trigger del mouse {#mouse-triggers}
I trigger del mouse consentono di associare l'input dei pulsanti e delle rotelle del mouse alle azioni di gioco.

![](images/input/mouse_bindings.png)

::: sidenote
Gli input dei pulsanti del mouse `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` e `MOUSE_BUTTON_MIDDLE` equivalgono a `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` e `MOUSE_BUTTON_3`.
:::

::: important
Gli esempi seguenti utilizzano le azioni mostrate nell'immagine sopra. Come per qualsiasi input, puoi assegnare alle azioni di input i nomi che preferisci.
:::

## Pulsanti del mouse {#mouse-buttons}
I pulsanti del mouse generano eventi `pressed`, `released` e `repeated`. Questo esempio mostra come rilevare l'input del pulsante sinistro del mouse (quando viene premuto o rilasciato):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- left mouse button pressed
        elseif action.released then
            -- left mouse button released
        end
    end
end
```

::: important
Le azioni di input `MOUSE_BUTTON_LEFT` (o `MOUSE_BUTTON_1`) vengono inviate anche per gli input a tocco singolo.
:::

## Rotella del mouse {#mouse-wheel}
Gli input della rotella del mouse rilevano le azioni di scorrimento. Il campo `action.value` vale `1` se la rotella viene fatta scorrere e `0` altrimenti. (Le azioni di scorrimento vengono gestite come pressioni di pulsanti. Defold attualmente non supporta l'input di scorrimento preciso dei touchpad.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- mouse wheel is scrolled up
        end
    end
end
```

## Movimento del mouse {#mouse-movement}
Il movimento del mouse viene gestito separatamente. Gli eventi di movimento del mouse vengono ricevuti solo se nei binding di input è configurato almeno un trigger del mouse.

Il movimento del mouse non viene associato nei binding di input: `action_id` viene impostato a `nil` e la tabella `action` viene popolata con la posizione del mouse e la variazione di tale posizione.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- let game object follow mouse/touch movement
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Trigger tattili {#touch-triggers}
I trigger per tocchi singoli e multipli sono disponibili sui dispositivi iOS e Android nelle applicazioni native e nei bundle HTML5.

![](images/input/touch_bindings.png)

## Tocco singolo {#single-touch}
I trigger per tocchi singoli non si configurano nella sezione Touch Triggers dei binding di input. **I trigger per tocchi singoli vengono invece configurati automaticamente quando configuri l'input di un pulsante del mouse per `MOUSE_BUTTON_LEFT` o `MOUSE_BUTTON_1`**.

## Tocchi multipli {#multi-touch}
I trigger per tocchi multipli popolano una tabella chiamata `touch` all'interno della tabella dell'azione. Gli elementi della tabella sono indicizzati con i numeri interi `1`--`N`, dove `N` è il numero di punti di contatto. Ogni elemento della tabella contiene campi con i dati di input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Spawn at each touch point
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Ai tocchi multipli non deve essere assegnata la stessa azione dell'input del pulsante del mouse per `MOUSE_BUTTON_LEFT` o `MOUSE_BUTTON_1`. Assegnare la stessa azione sostituisce di fatto l'input a tocco singolo e impedisce di ricevere qualsiasi evento di tocco singolo.
:::

::: sidenote
Puoi usare l'[asset Defold-Input](https://defold.com/assets/defoldinput/) per configurare facilmente controlli virtuali sullo schermo, come pulsanti e stick analogici, con supporto per tocchi multipli.
:::


## Rilevare clic o tocchi sugli oggetti {#detecting-click-or-tap-on-objects}
Rilevare quando l'utente fa clic o tocca un componente visivo è un'operazione molto comune, necessaria in molti giochi. Può trattarsi dell'interazione dell'utente con un pulsante o un altro elemento dell'interfaccia, oppure con un oggetto di gioco, come un'unità controllata dal giocatore in un gioco di strategia, un tesoro in un livello di un dungeon crawler o un personaggio che assegna missioni in un gioco di ruolo. L'approccio da usare varia a seconda del tipo di componente visivo.

### Rilevare l'interazione con i nodi GUI {#detecting-interaction-with-gui-nodes}
Per gli elementi dell'interfaccia è disponibile la funzione `gui.pick_node(node, x, y)`, che restituisce `true` o `false` a seconda che la coordinata specificata rientri o meno nei limiti di un nodo GUI. Per saperne di più, consulta la [documentazione API](/ref/gui/#gui.pick_node:node-x-y), l'[esempio del puntatore sopra un nodo](/examples/gui/pointer_over/) o l'[esempio di un pulsante](/examples/gui/button/).

### Rilevare l'interazione con gli oggetti di gioco {#detecting-interaction-with-game-objects}
Per gli oggetti di gioco, rilevare l'interazione è più complicato, perché fattori come la traslazione della camera e la proiezione dello script di rendering influiscono sui calcoli necessari. Esistono due approcci generali per rilevare l'interazione con gli oggetti di gioco:

  1. Tenere traccia della posizione e delle dimensioni degli oggetti di gioco con cui l'utente può interagire e verificare se la coordinata del mouse o del tocco rientra nei limiti di uno degli oggetti.
  2. Collegare oggetti di collisione agli oggetti di gioco con cui l'utente può interagire, aggiungere un oggetto di collisione che segua il mouse o il dito e verificare le collisioni tra questi oggetti.

::: sidenote
Nell'[asset Defold-Input](https://defold.com/assets/defoldinput/) puoi trovare una soluzione pronta all'uso che utilizza gli oggetti di collisione per rilevare l'input dell'utente, con supporto per trascinamenti e clic.
:::

In entrambi i casi è necessario convertire le coordinate dell'evento del mouse o del tocco nello spazio dello schermo in coordinate nello spazio del mondo degli oggetti di gioco. Puoi farlo in diversi modi:

  * Tenere traccia manualmente della vista e della proiezione utilizzate dallo script di rendering e usarle per convertire le coordinate da e verso lo spazio del mondo. Consulta il [manuale della camera per un esempio](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Usare una [soluzione di terze parti per la camera](/manuals/camera/#third-party-camera-solutions) e le funzioni di conversione dallo spazio dello schermo allo spazio del mondo che mette a disposizione.
