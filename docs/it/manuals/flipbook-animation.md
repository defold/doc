---
title: Manuale delle animazioni flipbook in Defold
brief: Questo manuale descrive come usare le animazioni flipbook in Defold.
---

# Animazione flipbook {#flip-book-animation}

Un'animazione flipbook consiste in una serie di immagini statiche mostrate in successione. La tecnica è molto simile all'animazione tradizionale su fogli di acetato (vedi http://en.wikipedia.org/wiki/Traditional_animation). Offre possibilità illimitate, poiché ogni fotogramma può essere modificato singolarmente. Tuttavia, dato che ogni fotogramma è memorizzato in un'immagine distinta, l'occupazione di memoria può essere elevata. La fluidità dell'animazione dipende anche dal numero di immagini mostrate ogni secondo, ma aumentare il numero di immagini comporta in genere anche un aumento del lavoro necessario. In Defold le animazioni flipbook sono memorizzate come immagini singole aggiunte a un [atlas](/manuals/atlas), oppure come una [sorgente di tile](/manuals/tilesource) con tutti i fotogrammi disposti in una sequenza orizzontale.

  ![Foglio dell'animazione](images/animation/animsheet.png){.inline}
  ![Ciclo di corsa](images/animation/runloop.gif){.inline}

## Riproduzione delle animazioni flipbook {#playing-flip-book-animations}

Gli sprite e i nodi box della GUI possono riprodurre animazioni flipbook e offrono ampie possibilità di controllo durante l'esecuzione.

Sprite
: Per riprodurre un'animazione durante l'esecuzione, usa la funzione [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Trovi un esempio più avanti.

Nodi box della GUI
: Per riprodurre un'animazione durante l'esecuzione, usa la funzione [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Trovi un esempio più avanti.

::: sidenote
La modalità di riproduzione `Once Ping Pong` riproduce l'animazione fino all'ultimo fotogramma, quindi inverte l'ordine e la riproduce a ritroso fino al **secondo** fotogramma dell'animazione, senza tornare al primo. Questo comportamento semplifica la concatenazione delle animazioni.
:::

### Esempio con uno sprite {#sprite-example}

Supponiamo che il tuo gioco abbia una funzionalità "dodge" che permette al giocatore di schivare premendo un pulsante specifico. Hai creato quattro animazioni per rappresentare visivamente questa funzionalità:

"idle"
: Un'animazione ciclica del personaggio del giocatore fermo.

"dodge_idle"
: Un'animazione ciclica del personaggio del giocatore fermo in posizione di schivata.

"start_dodge"
: Un'animazione di transizione, riprodotta una sola volta, che porta il personaggio del giocatore dalla posizione eretta a quella di schivata.

"stop_dodge"
: Un'animazione di transizione, riprodotta una sola volta, che riporta il personaggio del giocatore dalla posizione di schivata a quella eretta.

Lo script seguente implementa la logica:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### Esempio con un nodo box della GUI {#gui-box-node-example}

Quando selezioni un'animazione o un'immagine per un nodo, assegni in realtà la sorgente delle immagini (atlas o sorgente di tile) e l'animazione predefinita in un'unica operazione. La sorgente delle immagini è impostata staticamente nel nodo, ma l'animazione da riprodurre può essere cambiata durante l'esecuzione. Le immagini statiche sono trattate come animazioni di un solo fotogramma, quindi cambiare un'immagine durante l'esecuzione equivale a riprodurre un'animazione flipbook diversa per il nodo:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Callback di completamento {#completion-callbacks}

Le funzioni `sprite.play_flipbook()` e `gui.play_flipbook()` accettano come ultimo argomento una funzione di callback Lua facoltativa. Questa funzione viene chiamata quando l'animazione è stata riprodotta fino alla fine. Non viene mai chiamata per le animazioni cicliche. La callback può essere usata per attivare eventi al termine dell'animazione o per concatenare più animazioni. Esempi:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
