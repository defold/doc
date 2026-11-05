---
title: Etichette di testo in Defold
brief: Questo manuale spiega come usare i componenti etichetta per visualizzare testo con gli oggetti di gioco nel mondo di gioco.
---

# Etichette {#label}

Un componente *Label* (etichetta) visualizza del testo sullo schermo, nello spazio di gioco. Per impostazione predefinita, viene ordinato e disegnato insieme a tutta la grafica composta da sprite e tasselli. Il componente ha un insieme di proprietà che regolano il rendering del testo. La GUI di Defold supporta il testo, ma posizionare elementi GUI nel mondo di gioco può essere complicato. Le etichette semplificano questa operazione.

## Creare un'etichetta {#creating-a-label}

Per creare un componente Label, <kbd>fai clic con il pulsante destro</kbd> sull'oggetto di gioco e seleziona <kbd>Add Component ▸ Label</kbd>.

![Aggiungere un'etichetta](images/label/add_label.png)

(Se vuoi istanziare più etichette dallo stesso modello, puoi anche creare un nuovo file di componente etichetta: <kbd>fai clic con il pulsante destro</kbd> su una cartella nel pannello *Assets* e seleziona <kbd>New... ▸ Label</kbd>, quindi aggiungi il file come componente agli oggetti di gioco desiderati)

![Nuova etichetta](images/label/label.png)

Imposta la proprietà *Font* sul font che vuoi usare e assicurati di impostare la proprietà *Material* su un materiale adatto al tipo di font:

![Font e materiale](images/label/font_material.png)

## Font vettoriali ed emoji a colori {#vector-fonts-and-color-emoji}

Per usare un font Vector, segui la [configurazione dei font vettoriali](/manuals/font/#vector-fonts), assegna la risorsa `.font` alla proprietà *Font* del Label e imposta *Material* del Label su `/builtins/fonts/label-vector.material`. Usa *Font Size* per controllare le dimensioni visualizzate.

Per le emoji a colori, completa anche la [configurazione del ripiego COLRv1 e del bundle](/manuals/font/#color-emoji). L'esempio seguente presuppone un Label con l'ID `label` e uno script sullo stesso oggetto di gioco. Lascia vuoto *Text* del Label per mostrare il saluto soltanto quando i suoi glifi sono pronti:

```lua
function init(self)
    local text = "Hello 😀 🍎 🚀"
    local font_resource = go.get("#label", "font")
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            go.set("#label", "text", text)
        else
            print("Could not prepare label text:", err)
        end
    end)
end
```

Le lettere ordinarie usano il font originale e le emoji usano il font a colori aggiunto. Se altri Label o nodi di testo GUI condividono questa risorsa font, inizializza il ripiego in un solo punto e riutilizzalo.

## Proprietà delle etichette {#label-properties}

Oltre alle proprietà *Id*, *Position*, *Rotation* e *Scale*, sono disponibili le seguenti proprietà specifiche del componente:

*Text*
: Il contenuto testuale dell'etichetta.

*Size*
: Le dimensioni del riquadro che contiene il testo. Se *Line Break* è attiva, la larghezza specifica il punto in cui il testo deve andare a capo.

*Color*
: Il colore del testo.

*Outline*
: Il colore del contorno.

*Shadow*
: Il colore dell'ombra.

::: sidenote
Tieni presente che il materiale predefinito ha il rendering dell'ombra disattivato per motivi di prestazioni.
:::

*Leading*
: Un fattore di scala per l'interlinea. Un valore di 0 annulla la spaziatura tra le righe. Il valore predefinito è 1.

*Tracking*
: Un fattore di scala per la spaziatura tra le lettere. Il valore predefinito è 0.

*Pivot*
: Il punto di ancoraggio (pivot) del testo. Usalo per modificare l'allineamento del testo (vedi sotto).

*Blend Mode*
: La modalità di fusione da usare per il rendering dell'etichetta.

*Line Break*
: L'allineamento del testo segue l'impostazione del punto di ancoraggio e l'attivazione di questa proprietà permette al testo di disporsi su più righe. La larghezza del componente determina dove il testo va a capo. Tieni presente che il testo deve contenere uno spazio perché possa andare a capo.

*Font*
: La risorsa font da usare per questa etichetta.

*Material*
: Il materiale da usare per renderizzare questo Label. Seleziona un materiale corrispondente alla modalità o sorgente del font (Bitmap, SDF, Vector o BMFont). Consulta [Materiali dei font](/manuals/font/#font-materials) per i materiali Label integrati corrispondenti.

### Modalità di fusione {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Punto di ancoraggio e allineamento {#pivot-and-alignment}

Impostando la proprietà *Pivot* puoi cambiare la modalità di allineamento del testo.

*Centrato*
: Se il punto di ancoraggio è impostato su `Center`, `North` o `South`, il testo è centrato.

*A sinistra*
: Se il punto di ancoraggio è impostato su una delle modalità `West`, il testo è allineato a sinistra.

*A destra*
: Se il punto di ancoraggio è impostato su una delle modalità `East`, il testo è allineato a destra.

![Allineamento del testo](images/label/align.png)

## Modifiche a runtime {#runtime-manipulation}

Puoi modificare le etichette durante l'esecuzione leggendo e impostando il testo dell'etichetta e le altre proprietà.

`text`
: Il contenuto testuale del Label (`string`). Disponibile tramite `go.get()` e `go.set()`.

`color`
: Il colore dell'etichetta (`vector4`)

`outline`
: Il colore del contorno dell'etichetta (`vector4`)

`shadow`
: Il colore dell'ombra dell'etichetta (`vector4`)

`scale`
: La scala dell'etichetta, espressa come `number` per una scala uniforme oppure come `vector3` per una scala indipendente lungo ciascun asse.

`size`
: Le dimensioni dell'etichetta (`vector3`)

```lua
function init(self)
    -- Set the text of the "my_label" component in the same game object
    -- as this script.
    go.set("#my_label", "text", "New text")
    local text = go.get("#my_label", "text")
    print(text) -- New text
end
```

::: sidenote
`label.set_text()` e `label.get_text()` sono deprecate a favore della proprietà `text`. Le vecchie funzioni restano disponibili per compatibilità. Il vecchio setter accoda un messaggio, mentre `go.set()` aggiorna il testo immediatamente.
:::

```lua
function init(self)
    -- Set the color of the "my_label" component in the same game object
    -- as this script. Color is a RGBA value stored in a vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...and remove the outline, by setting its alpha to 0...
    go.set("#my_label", "outline.w", 0)

    -- ...and scale it x2 along x axis.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Configurazione del progetto {#project-configuration}

Il file *game.project* contiene alcune [impostazioni del progetto](/manuals/project-settings#label) relative alle etichette.
