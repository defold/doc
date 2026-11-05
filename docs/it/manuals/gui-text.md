---
title: Nodi di testo GUI in Defold
brief: Questo manuale descrive come aggiungere testo alle scene GUI.
---

# Nodi di testo GUI {#gui-text-nodes}

Defold supporta un tipo specifico di nodo GUI che permette di visualizzare testo in una scena GUI. Per il rendering dei nodi di testo puoi utilizzare qualsiasi risorsa font aggiunta al progetto.

L'anteprima dell'editor supporta la composizione dei glifi e il layout da destra a sinistra usando il renderer dei font del motore. Consulta [Supporto per il layout del testo](/manuals/font/#text-layout-support-eg-right-to-left) per le impostazioni richieste dei font e dell'App Manifest.

## Aggiungere nodi di testo {#adding-text-nodes}

I font che vuoi utilizzare nei nodi di testo GUI devono essere aggiunti al componente GUI. Fai clic con il pulsante destro del mouse sulla cartella *Fonts*, utilizza il menu superiore <kbd>GUI</kbd> oppure premi la scorciatoia da tastiera corrispondente.

![Font](images/gui-text/fonts.png)

I nodi di testo hanno alcune proprietà specifiche:

*Font*
: Per ogni nodo di testo che crei devi impostare la proprietà *Font*.

*Text*
: Questa proprietà contiene il testo visualizzato.

*Line Break*
: L'allineamento del testo segue l'impostazione del pivot; attivando questa proprietà, il testo può andare a capo su più righe. La larghezza del nodo determina il punto in cui il testo va a capo.

## Font vettoriali ed emoji a colori {#vector-fonts-and-color-emoji}

Segui la [configurazione dei font vettoriali](/manuals/font/#vector-fonts), aggiungi la risorsa `.font` a *Fonts* della scena GUI e selezionala sul nodo di testo. Imposta *Material* della risorsa font su `/builtins/fonts/font-vector.material`. Usa *Font Size* del nodo per controllare le dimensioni visualizzate.

Per le emoji a colori, completa anche la [configurazione del ripiego COLRv1 e del bundle](/manuals/font/#color-emoji). Crea un nodo di testo con l'ID `text`, lascia vuoto *Text* e aggiungi quanto segue al `.gui_script` della scena GUI:

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font) restituisce il nome del font nella scena GUI; [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) risolve quel nome nella risorsa font usata da `font.add_font()`. Anche gli altri nodi e Label che condividono quella risorsa ricevono il font di ripiego, quindi inizializzalo una sola volta. Il testo viene impostato dopo il completamento del preriscaldamento.

## Allineamento {#alignment}

Impostando il pivot del nodo puoi cambiare la modalità di allineamento del testo.

*Centrato*
: Se il pivot è impostato su `Center`, `North` o `South`, il testo è centrato.

*A sinistra*
: Se il pivot è impostato su una qualsiasi delle modalità `West`, il testo è allineato a sinistra.

*A destra*
: Se il pivot è impostato su una qualsiasi delle modalità `East`, il testo è allineato a destra.

![Allineamento del testo](images/gui-text/align.png)

## Modificare i nodi di testo a runtime {#modifying-text-nodes-in-runtime}

I nodi di testo rispondono a tutte le funzioni generiche di manipolazione dei nodi per impostare dimensioni, pivot, colore e così via. Esistono anche alcune funzioni specifiche per i nodi di testo:

* Per cambiare il font di un nodo di testo, utilizza la funzione [`gui.set_font()`](/ref/gui/#gui.set_font).
* Per cambiare il comportamento di ritorno a capo di un nodo di testo, utilizza la funzione [`gui.set_line_break()`](/ref/gui/#gui.set_line_break).
* Per cambiare il contenuto di un nodo di testo, utilizza la funzione [`gui.set_text()`](/ref/gui/#gui.set_text).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
