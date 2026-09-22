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
