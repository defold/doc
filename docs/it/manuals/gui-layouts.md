---
title: Layout GUI in Defold
brief: Defold supporta GUI che si adattano automaticamente ai cambiamenti di orientamento dello schermo sui dispositivi mobili. Questo documento spiega come funziona questa funzionalità.
---

# Layout {#layouts}

Defold supporta GUI che si adattano automaticamente ai cambiamenti di orientamento dello schermo sui dispositivi mobili. Con questa funzionalità puoi progettare GUI che si adattano all'orientamento e al rapporto d'aspetto di schermi di varie dimensioni. Puoi anche creare layout specifici per determinati modelli di dispositivo.

## Creazione dei profili di visualizzazione {#creating-display-profiles}

Per impostazione predefinita, le impostazioni di *game.project* specificano l'uso di un file integrato per le impostazioni dei profili di visualizzazione ("builtins/render/default.display_profiles"). I profili predefiniti sono "Landscape" (1280 pixel di larghezza e 720 pixel di altezza) e "Portrait" (720 pixel di larghezza e 1280 pixel di altezza). Nei profili non sono specificati modelli di dispositivo, quindi possono essere utilizzati su qualsiasi dispositivo.

Per creare un nuovo file di impostazioni dei profili, copia quello della cartella "builtins" oppure <kbd>fai clic con il pulsante destro</kbd> in una posizione adatta nella vista *Assets* e seleziona <kbd>New... ▸ Display Profiles</kbd>. Assegna al nuovo file un nome adatto e fai clic su <kbd>Ok</kbd>.

L'editor apre il nuovo file per la modifica. Aggiungi nuovi profili facendo clic su <kbd>+</kbd> nell'elenco *Profiles*. Per ogni profilo, aggiungi un insieme di *qualificatori*:

Width
: La larghezza in pixel del qualificatore.

Height
: L'altezza in pixel del qualificatore.

Device Models
: Un elenco di modelli di dispositivo separati da virgole. La corrispondenza viene verificata rispetto all'inizio del nome del modello di dispositivo: ad esempio, `iPhone10` corrisponde ai modelli "iPhone10,\*". I nomi dei modelli che contengono virgole devono essere racchiusi tra virgolette: ad esempio, `"iPhone10,3", "iPhone10,6"` corrisponde ai modelli iPhone X (consulta il [wiki dell'iPhone](https://www.theiphonewiki.com/wiki/Models)). Tieni presente che le uniche piattaforme che restituiscono un modello di dispositivo quando chiami `sys.get_sys_info()` sono Android e iOS. Le altre piattaforme restituiscono una stringa vuota e quindi non selezionano mai un profilo di visualizzazione con un qualificatore del modello di dispositivo.

![Nuovi profili di visualizzazione](images/gui-layouts/new_profiles.png)

Devi anche indicare al motore di usare i nuovi profili. Apri *game.project* e seleziona il file dei profili di visualizzazione nell'impostazione *Display Profiles* della sezione *display*:

![Impostazioni](images/gui-layouts/settings.png)

Se vuoi che il motore passi automaticamente dal layout verticale a quello orizzontale e viceversa quando ruoti il dispositivo, seleziona la casella *Dynamic Orientation*. Il motore seleziona dinamicamente un layout corrispondente e cambia la selezione anche quando cambia l'orientamento del dispositivo.

### Selezione automatica del layout (Display Profiles) {#auto-layout-selection-display-profiles}

La risorsa Display Profiles ha un'opzione “Auto Layout Selection” (ON per impostazione predefinita). Quando è ON, il motore seleziona automaticamente il layout GUI più adatto sia alla creazione della scena sia quando cambiano le dimensioni della finestra o dello schermo. Quando è OFF, il motore non cambia automaticamente il layout: usa `gui.set_layout()` nello script GUI per cambiarlo manualmente. Questa impostazione viene salvata nel file Display Profiles e si applica a tutte le scene GUI.

## Layout GUI {#gui-layouts}

Puoi usare l'insieme corrente di profili di visualizzazione per creare varianti del layout dei tuoi nodi GUI. Per aggiungere un nuovo layout a una scena GUI, fai clic con il pulsante destro sull'icona *Layouts* nella vista *Outline* e seleziona <kbd>Add ▸ Layout ▸ ...</kbd>:

![Aggiunta di un layout alla scena](images/gui-layouts/add_layout.png)

Quando modifichi una scena GUI, tutti i nodi vengono modificati in un layout specifico. Il layout attualmente selezionato è indicato nel menu a discesa dei layout della scena GUI nella barra degli strumenti. Se non è selezionato alcun layout, i nodi vengono modificati nel layout *Default*.

![Barra degli strumenti dei layout](images/gui-layouts/toolbar.png)

![Modifica del layout verticale](images/gui-layouts/portrait.png)

Ogni modifica che apporti a una proprietà di un nodo con un layout selezionato _sovrascrive_ la proprietà rispetto al layout *Default*. Le proprietà sovrascritte sono evidenziate in blu, così come i nodi che contengono proprietà sovrascritte. Puoi fare clic sul pulsante di ripristino accanto a qualsiasi proprietà sovrascritta per riportarla al valore originale.

![Modifica del layout orizzontale](images/gui-layouts/landscape.png)

Un layout non può eliminare o creare nodi, ma solo sovrascriverne le proprietà. Se devi rimuovere un nodo da un layout, puoi spostarlo fuori dallo schermo oppure eliminarlo tramite la logica di uno script. Presta attenzione anche al layout attualmente selezionato. Se aggiungi un layout al progetto, il nuovo layout viene configurato in base a quello attualmente selezionato. Anche le operazioni di copia e incolla dei nodi tengono conto del layout attualmente selezionato, sia quando copi *sia* quando incolli.

## Selezione dinamica del profilo {#dynamic-profile-selection}

Quando Auto Layout Selection è attiva, il motore seleziona automaticamente il layout più adatto. La selezione dinamica del layout assegna un punteggio a ogni qualificatore dei profili di visualizzazione secondo le seguenti regole:

1. Se non è impostato alcun modello di dispositivo, oppure se il modello di dispositivo corrisponde, viene calcolato un punteggio (S) per il qualificatore.

2. Il punteggio (S) viene calcolato usando l'area dello schermo (A), l'area del qualificatore (A_Q), il rapporto d'aspetto dello schermo (R) e il rapporto d'aspetto del qualificatore (R_Q):

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. Viene selezionato il profilo con il qualificatore dal punteggio più basso, se l'orientamento del qualificatore (orizzontale o verticale) corrisponde a quello dello schermo.

4. Se non viene trovato alcun profilo con un qualificatore dello stesso orientamento, viene selezionato il profilo con il qualificatore dal punteggio migliore nell'altro orientamento.

5. Se non è possibile selezionare alcun profilo, viene usato il profilo di ripiego *Default*.

Poiché il layout *Default* viene usato come ripiego durante l'esecuzione quando non esiste un layout più adatto, se aggiungi un layout "Landscape", questo risulta il più adatto per *tutti* gli orientamenti finché non aggiungi anche un layout "Portrait".

## Messaggi di cambio del layout {#layout-change-messages}

Quando cambia il layout, viene inviato un messaggio `layout_changed` allo script del componente GUI. Questo avviene quando il motore cambia automaticamente il layout (Auto Layout Selection ON) oppure quando lo script chiama `gui.set_layout()` e il layout cambia effettivamente. Il messaggio contiene l'ID hash del layout, così lo script può eseguire la logica in base al layout selezionato:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- switching layout to landscape
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- switching layout to portrait
  end
end
```

Inoltre, lo script di rendering corrente riceve un messaggio ogni volta che cambia la finestra (vista di gioco), anche in caso di cambiamenti di orientamento.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- The window was resized. message.width and message.height contain the
    -- new dimensions of the window.
  end
end
```

Quando cambia l'orientamento, il gestore dei layout GUI ridimensiona e riposiziona automaticamente i nodi GUI in base al layout e alle proprietà dei nodi. Il contenuto di gioco, invece, viene renderizzato in un passaggio separato (per impostazione predefinita), con una proiezione che lo allunga per adattarlo alla finestra corrente. Per modificare questo comportamento, fornisci uno script di rendering modificato oppure usa una [libreria](/assets/) per la camera.

## Selezione manuale del layout (Lua) {#manual-layout-selection-lua}

Quando Auto Layout Selection è OFF per i Display Profiles in uso, il motore non cambia automaticamente il layout. Usa queste funzioni da uno script GUI per gestire i layout manualmente:

### gui.set_layout(layout)

- Accetta una stringa o un hash (ID del layout).
- Restituisce un valore booleano: `true` se il layout esiste nella scena ed è stato applicato; `false` altrimenti.
- Se il layout esiste in Display Profiles, aggiorna la risoluzione della scena in base alla larghezza e all'altezza del profilo.
- Emette `layout_changed` quando il layout cambia effettivamente.

Esempio:

```lua
function init(self)
    -- Manually apply the "Portrait" layout
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- Restituisce una tabella che associa l'hash dell'ID di ogni layout a `vmath.vector3(width, height, 0)`.
- Per il layout predefinito, restituisce la risoluzione corrente della scena.

Esempio:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Nota: se un layout GUI esiste nella scena ma non è presente in Display Profiles, `gui.set_layout()` applica comunque le proprietà dei nodi sovrascritte per quel layout, ma non modifica la risoluzione della scena.
