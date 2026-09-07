---
title: Scene GUI in Defold
brief: Questo manuale illustra l'editor GUI di Defold, i vari tipi di nodi GUI e la programmazione delle GUI tramite script.
---

# GUI

Defold offre un editor GUI dedicato e potenti possibilità di programmazione tramite script, pensati appositamente per la costruzione e l'implementazione di interfacce utente.

Un'interfaccia grafica utente in Defold è un componente che crei e aggiungi a un oggetto di gioco, da inserire in una collezione. Questo componente ha le seguenti proprietà:

* Dispone di funzionalità di layout semplici ma potenti, che consentono di visualizzare l'interfaccia utente indipendentemente dalla risoluzione e dal rapporto d'aspetto.
* Può avere un comportamento logico associato tramite uno *script GUI*.
* Viene visualizzato (per impostazione predefinita) sopra gli altri contenuti, indipendentemente dalla vista della telecamera: anche quando la telecamera si muove, gli elementi della GUI rimangono fermi sullo schermo. Il comportamento del rendering può essere modificato.

I componenti GUI vengono visualizzati indipendentemente dalla vista del gioco. Per questo motivo non vengono collocati in una posizione specifica nell'editor di collezioni e non hanno una rappresentazione visiva al suo interno. Tuttavia, i componenti GUI devono appartenere a un oggetto di gioco che occupa una posizione in una collezione. Modificare tale posizione non ha alcun effetto sulla GUI.

## Creazione di un componente GUI {#creating-a-gui-component}

I componenti GUI vengono creati a partire da un file prototipo di scena GUI (chiamato anche "prefab" o "blueprint" in altri motori). Per creare un nuovo componente GUI, <kbd>fai clic con il pulsante destro del mouse</kbd> in una posizione del browser *Assets* e seleziona <kbd>New ▸ Gui</kbd>. Digita un nome per il nuovo file GUI e premi <kbd>Ok</kbd>.

![Nuovo file GUI](images/gui/new_gui_file.png)

Defold apre automaticamente il file nell'editor di scene GUI.

![Nuova GUI](images/gui/new_gui.png)

La vista *Outline* elenca tutti i contenuti della GUI: l'elenco dei nodi e le eventuali dipendenze (vedi sotto).

L'area di modifica centrale mostra la GUI. La barra degli strumenti nell'angolo superiore destro dell'area di modifica contiene gli strumenti *Move*, *Rotate* e *Scale*, oltre a un selettore di [layout](/manuals/gui-layouts).

![Barra degli strumenti](images/gui/toolbar.png)

Un rettangolo bianco mostra i limiti del layout attualmente selezionato, corrispondenti alla larghezza e all'altezza predefinite dello schermo definite nelle impostazioni del progetto.

## Proprietà della GUI {#gui-properties}

Selezionando il nodo radice "Gui" nella vista *Outline*, il pannello *Properties* mostra le proprietà del componente GUI:

*Script*
: Lo script GUI associato a questo componente GUI.

*Material*
: Il materiale utilizzato per il rendering di questa GUI. È anche possibile aggiungere più materiali a una GUI dal pannello *Outline* e assegnarli ai singoli nodi.

*Adjust Reference*
: Controlla come viene calcolata la proprietà *Adjust Mode* di ciascun nodo:

  - `Per Node` adatta ogni nodo alle dimensioni adattate del nodo genitore o allo schermo ridimensionato.
  - `Disable` disattiva la modalità di adattamento dei nodi. Tutti i nodi sono quindi costretti a mantenere le dimensioni impostate.

*Current Nodes*
: Il numero di nodi attualmente utilizzati in questa GUI.

*Max Nodes*
: Il numero massimo di nodi per questa GUI.

*Max Dynamic Textures*
: Il numero massimo di texture dinamiche gestite da questo componente GUI, `128` per impostazione predefinita. Include le texture create con [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) e le texture esterne assegnate alla GUI con `go.set(..., "textures", ...)` o `gui.set(msg.url(), "textures", ...)`. Nei progetti che sostituiscono molte texture esterne potrebbe essere necessario aumentare questo limite.


## Modifiche durante l'esecuzione {#runtime-manipulation}

Puoi modificare le proprietà della GUI durante l'esecuzione da un componente script, usando `go.get()` e `go.set()`:

Caratteri
: Recupera o imposta un carattere utilizzato in una GUI.

![Recupero e impostazione di un carattere](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- get the font file currently assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- set the font with id 'default' to the font file assigned to the resource property 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- get the new font file assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materiali
: Recupera o imposta un materiale utilizzato in una GUI.

![Recupero e impostazione di un materiale](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- get the material file currently assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- set the material id 'effect' to the material file assigned to the resource property 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- get the new material file assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Texture
: Recupera o imposta una texture (atlas) utilizzata in una GUI.

![Recupero e impostazione di una texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- get the texture file currently assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- set the texture with id 'theme' to the texture file assigned to the resource property 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- get the new texture file assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Dipendenze {#dependencies}

L'albero delle risorse di un gioco Defold è statico, quindi tutte le dipendenze necessarie ai nodi GUI devono essere aggiunte al componente. La vista *Outline* raggruppa tutte le dipendenze per tipo in "cartelle":

![Dipendenze](images/gui/dependencies.png)

Per aggiungere una nuova dipendenza, trascinala dal pannello *Asset* alla vista dell'editor.

In alternativa, <kbd>fai clic con il pulsante destro del mouse</kbd> sulla radice "Gui" nella vista *Outline*, quindi seleziona <kbd>Add ▸ [type]</kbd> dal menu contestuale.

Puoi anche <kbd>fare clic con il pulsante destro del mouse</kbd> sull'icona della cartella del tipo che vuoi aggiungere e selezionare <kbd>Add ▸ [type]</kbd>.

## Tipi di nodi {#node-types}

Un componente GUI è costituito da un insieme di nodi. I nodi sono elementi semplici. Possono essere trasformati (spostati, scalati e ruotati) e organizzati in gerarchie genitore-figlio sia nell'editor sia durante l'esecuzione tramite script. Sono disponibili i seguenti tipi di nodi:

Nodo Box
: ![Nodo Box](images/icons/gui-box-node.png){.left}
  Nodo rettangolare con un colore uniforme, una texture o un'animazione flipbook. Per i dettagli, consulta la [documentazione del nodo Box](/manuals/gui-box).

<div style="clear: both;"></div>

Nodo Text
: ![Nodo Text](images/icons/gui-text-node.png){.left}
  Visualizza del testo. Per i dettagli, consulta la [documentazione del nodo Text](/manuals/gui-text).

<div style="clear: both;"></div>

Nodo Pie
: ![Nodo Pie](images/icons/gui-pie-node.png){.left}
  Un nodo circolare o ellittico che può essere parzialmente riempito o invertito. Per i dettagli, consulta la [documentazione del nodo Pie](/manuals/gui-pie).

<div style="clear: both;"></div>

Nodo Template
: ![Nodo Template](images/icons/gui.png){.left}
  I modelli vengono utilizzati per creare istanze basate su altri file di scena GUI. Per i dettagli, consulta la [documentazione del nodo Template](/manuals/gui-template).

<div style="clear: both;"></div>

Nodo ParticleFX
: ![Nodo ParticleFX](images/icons/particlefx.png){.left}
  Riproduce un effetto particellare. Per i dettagli, consulta la [documentazione del nodo ParticleFX](/manuals/gui-particlefx).

<div style="clear: both;"></div>

Aggiungi nodi facendo clic con il pulsante destro del mouse sulla cartella *Nodes* e selezionando <kbd>Add ▸</kbd>, quindi <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> o <kbd>ParticleFx</kbd>.

![Aggiunta di nodi](images/gui/add_node.png)

Puoi anche premere <kbd>A</kbd> e selezionare il tipo che vuoi aggiungere alla GUI.

## Proprietà dei nodi {#node-properties}

Ogni nodo dispone di un ampio insieme di proprietà che ne controllano l'aspetto:

Id
: L'identità del nodo. Questo nome deve essere univoco all'interno della scena GUI.

Position, Rotation e Scale
: Controllano la posizione, l'orientamento e la deformazione del nodo. Puoi usare gli strumenti *Move*, *Rotate* e *Scale* per modificare questi valori. I valori possono essere animati tramite script ([approfondisci](/manuals/property-animation)).

Size (nodi Box, Text e Pie)
: Le dimensioni del nodo sono automatiche per impostazione predefinita, ma puoi modificarne il valore impostando *Size Mode* su `Manual`. Le dimensioni definiscono i limiti del nodo e vengono usate per individuare il nodo interessato dall'input. Questo valore può essere animato tramite script ([approfondisci](/manuals/property-animation)).

Size Mode (nodi Box e Pie)
: Se impostata su `Automatic`, l'editor definisce le dimensioni del nodo. Se impostata su `Manual`, puoi definirle tu.

Enabled
: Se deselezionata, il nodo non viene visualizzato, non viene animato e non può essere individuato tramite `gui.pick_node()`. Usa `gui.set_enabled()` e `gui.is_enabled()` per modificare e verificare questa proprietà da codice.

Visible
: Se deselezionata, il nodo non viene visualizzato, ma può comunque essere animato e individuato tramite `gui.pick_node()`. Usa `gui.set_visible()` e `gui.get_visible()` per modificare e verificare questa proprietà da codice.

Text (nodi Text)
: Il testo da visualizzare sul nodo.

Line Break (nodi Text)
: Attivala per mandare a capo il testo in base alla larghezza del nodo.

Font (nodi Text)
: Il carattere da utilizzare per il rendering del testo.

Texture (nodi Box e Pie)
: La texture da disegnare sul nodo. È un riferimento a un'immagine o a un'animazione in un atlas o in una sorgente di tile.

Material (nodi Box, Pie, Text e ParticleFX)
: Il materiale da utilizzare per disegnare il nodo. Può essere un materiale aggiunto alla sezione Materials della vista *Outline*, oppure puoi lasciare il campo vuoto per usare il materiale predefinito assegnato al componente GUI.

Slice 9 (nodi Box)
: Impostala per mantenere le dimensioni in pixel della texture lungo i bordi quando il nodo viene ridimensionato. Per i dettagli, consulta la [documentazione del nodo Box](/manuals/gui-box).

Inner Radius (nodi Pie)
: Il raggio interno del nodo, espresso lungo l'asse X. Per i dettagli, consulta la [documentazione del nodo Pie](/manuals/gui-pie).

Outer Bounds (nodi Pie)
: Controlla il comportamento dei limiti esterni. Per i dettagli, consulta la [documentazione del nodo Pie](/manuals/gui-pie).

Perimeter Vertices (nodi Pie)
: Il numero di segmenti che verranno utilizzati per costruire la forma. Per i dettagli, consulta la [documentazione del nodo Pie](/manuals/gui-pie).

Pie Fill Angle (nodi Pie)
: La porzione del nodo Pie da riempire. Per i dettagli, consulta la [documentazione del nodo Pie](/manuals/gui-pie).

Template (nodi Template)
: Il file di scena GUI da utilizzare come modello per il nodo. Per i dettagli, consulta la [documentazione del nodo Template](/manuals/gui-template).

ParticleFX (nodi ParticleFX)
: L'effetto particellare da utilizzare su questo nodo. Per i dettagli, consulta la [documentazione del nodo ParticleFX](/manuals/gui-particlefx).

Color
: Il colore del nodo. Se il nodo ha una texture, il colore ne modifica la tinta. Il colore può essere animato tramite script ([approfondisci](/manuals/property-animation)).

Alpha
: La traslucenza del nodo. Il valore alfa può essere animato tramite script ([approfondisci](/manuals/property-animation)).

Inherit Alpha
: Selezionando questa casella, il nodo eredita il valore alfa del nodo genitore. Il valore alfa del nodo viene quindi moltiplicato per quello del genitore.

Leading (nodi Text)
: Un fattore di scala per l'interlinea. Il valore `0` elimina l'interlinea. `1` (il valore predefinito) corrisponde all'interlinea normale.

Tracking (nodi Text)
: Un fattore di scala per la spaziatura tra le lettere. Il valore predefinito è 0.

Layer
: Assegnare un livello al nodo sostituisce il normale ordine di disegno con l'ordine dei livelli. Vedi sotto per i dettagli.

Blend mode
: Controlla come la grafica del nodo viene fusa con la grafica dello sfondo:
  - `Alpha` fonde i valori dei pixel del nodo con quelli dello sfondo usando il valore alfa. Corrisponde alla modalità di fusione "Normal" dei programmi di grafica.
  - `Add` somma i valori dei pixel del nodo a quelli dello sfondo. Corrisponde alla modalità "Linear dodge" di alcuni programmi di grafica.
  - `Multiply` moltiplica i valori dei pixel del nodo per quelli dello sfondo.
  - `Screen` applica una moltiplicazione inversa ai valori dei pixel del nodo e dello sfondo. Corrisponde alla modalità di fusione "Screen" dei programmi di grafica.

Pivot
: Imposta il punto di perno del nodo. Puoi considerarlo il "punto centrale" del nodo. Ogni rotazione, ridimensionamento o modifica delle dimensioni avviene attorno a questo punto.

  I valori possibili sono `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` o `South East`.

  ![Punto di perno](images/gui/pivot.png)

  Se modifichi il perno di un nodo, il nodo viene spostato in modo che il nuovo perno si trovi nella posizione del nodo. Per i nodi Text, `Center` allinea il testo al centro, `West` lo allinea a sinistra ed `East` lo allinea a destra.

X Anchor, Y Anchor
: L'ancoraggio controlla come cambia la posizione verticale e orizzontale del nodo quando i limiti della scena, o quelli del nodo genitore, vengono estesi per adattarsi alle dimensioni fisiche dello schermo.

  ![Ancoraggio senza adattamento](images/gui/anchoring_unadjusted.png)

  Sono disponibili le seguenti modalità di ancoraggio:

  - `None` (sia per *X Anchor* sia per *Y Anchor*) mantiene la posizione del nodo rispetto al centro del nodo genitore o della scena, in relazione alle dimensioni *adattate*.
  - `Left` o `Right` (*X Anchor*) scala la posizione orizzontale del nodo, mantenendo la stessa percentuale di distanza dai bordi sinistro e destro del nodo genitore o della scena.
  - `Top` o `Bottom` (*Y Anchor*) scala la posizione verticale del nodo, mantenendo la stessa percentuale di distanza dai bordi superiore e inferiore del nodo genitore o della scena.

  ![Ancoraggio](images/gui/anchoring.png)

Adjust Mode
: Imposta la modalità di adattamento del nodo. Questa impostazione controlla cosa succede al nodo quando i limiti della scena, o quelli del nodo genitore, vengono adattati alle dimensioni fisiche dello schermo.

  Un nodo creato in una scena la cui risoluzione logica è una tipica risoluzione orizzontale:

  ![Senza adattamento](images/gui/unadjusted.png)

  Adattare la scena a uno schermo verticale ne provoca la deformazione. Il rettangolo di delimitazione di ciascun nodo viene deformato allo stesso modo. Tuttavia, impostando la modalità di adattamento puoi mantenere inalterato il rapporto d'aspetto del contenuto del nodo. Sono disponibili le seguenti modalità:

  - `Fit` scala il contenuto del nodo in base alla larghezza o all'altezza del rettangolo di delimitazione deformato, scegliendo quella minore. In altre parole, il contenuto rientra interamente nel rettangolo di delimitazione deformato del nodo.
  - `Zoom` scala il contenuto del nodo in base alla larghezza o all'altezza del rettangolo di delimitazione deformato, scegliendo quella maggiore. In altre parole, il contenuto copre interamente il rettangolo di delimitazione deformato del nodo.
  - `Stretch` deforma il contenuto del nodo in modo che riempia il rettangolo di delimitazione deformato del nodo.

  ![Modalità di adattamento](images/gui/adjusted.png)

  Se la proprietà *Adjust Reference* della scena GUI è impostata su `Disabled`, questa impostazione viene ignorata.

Clipping Mode (nodi Box e Pie)
: Imposta la modalità di ritaglio del nodo:

  - `None` visualizza il nodo normalmente.
  - `Stencil` fa sì che i limiti del nodo definiscano una maschera stencil, utilizzata per ritagliare i nodi figli.

  Per i dettagli, consulta il [manuale sul ritaglio delle GUI](/manuals/gui-clipping).

Clipping Visible (nodi Box e Pie)
: Attivala per visualizzare il contenuto del nodo nell'area dello stencil. Per i dettagli, consulta il [manuale sul ritaglio delle GUI](/manuals/gui-clipping).

Clipping Inverted (nodi Box e Pie)
: Inverte la maschera stencil. Per i dettagli, consulta il [manuale sul ritaglio delle GUI](/manuals/gui-clipping).


## Perno, ancoraggi e modalità di adattamento {#pivot-anchors-and-adjust-mode}

La combinazione delle proprietà Pivot, Anchors e Adjust Mode consente di progettare GUI molto flessibili, ma può essere difficile capirne il funzionamento senza un esempio concreto. Prendiamo come esempio questo prototipo di GUI, creato per uno schermo da 640x1136:

![](images/gui/adjustmode_example_original.png)

L'interfaccia è stata creata con gli ancoraggi X e Y impostati su None e con Adjust Mode di ogni nodo lasciata sul valore predefinito Fit. Il perno del pannello superiore è North, quello del pannello inferiore è South e i perni delle barre nel pannello superiore sono impostati su West. Tutti gli altri nodi hanno il perno impostato su Center. Se ridimensioniamo la finestra per renderla più larga, ecco cosa succede:

![](images/gui/adjustmode_example_resized.png)

E se volessimo che le barre superiore e inferiore fossero sempre larghe quanto lo schermo? Possiamo impostare Adjust Mode su Stretch per i pannelli grigi di sfondo in alto e in basso:

![](images/gui/adjustmode_example_resized_stretch.png)

Il risultato è migliore. Ora i pannelli grigi di sfondo si estendono sempre per tutta la larghezza della finestra, ma le barre nel pannello superiore e i due riquadri in basso non sono posizionati correttamente. Per mantenere le barre in alto posizionate a sinistra, dobbiamo cambiare X Anchor da None a Left:

![](images/gui/adjustmode_example_top_anchor_left.png)

È esattamente il risultato desiderato per il pannello superiore. Le barre nel pannello superiore avevano già il perno impostato su West: si posizionano quindi correttamente, con il bordo sinistro/ovest delle barre (Pivot) ancorato al bordo sinistro del pannello genitore (X Anchor).

Ora, se impostiamo X Anchor su Left per il riquadro a sinistra e su Right per il riquadro a destra, otteniamo questo risultato:

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Il risultato non è proprio quello atteso. I due riquadri dovrebbero rimanere vicini ai bordi sinistro e destro, come le due barre nel pannello superiore. Il motivo è che il punto di perno è sbagliato:

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Entrambi i riquadri hanno il perno impostato su Center. Questo significa che, quando lo schermo diventa più largo, il punto centrale (il perno) dei riquadri rimane alla stessa distanza relativa dai bordi. Per il riquadro sinistro, nella finestra originale da 640x1136 questa distanza era pari al 17% dal bordo sinistro:

![](images/gui/adjustmode_example_original_ratio.png)

Quando lo schermo viene ridimensionato, il punto centrale del riquadro sinistro rimane alla stessa distanza del 17% dal bordo sinistro:

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Se cambiamo il perno da Center a West per il riquadro a sinistra e a East per quello a destra, e riposizioniamo i riquadri, otteniamo il risultato desiderato anche quando lo schermo viene ridimensionato:

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Ordine di disegno {#draw-order}

Tutti i nodi vengono visualizzati nell'ordine in cui sono elencati nella cartella "Nodes". Il nodo in cima all'elenco viene disegnato per primo e appare quindi dietro tutti gli altri. L'ultimo nodo nell'elenco viene disegnato per ultimo e appare davanti a tutti gli altri. Modificare il valore Z di un nodo non ne controlla l'ordine di disegno; tuttavia, se imposti il valore Z al di fuori dell'intervallo di rendering dello script di rendering, il nodo non viene più visualizzato sullo schermo. Puoi sostituire l'ordine dei nodi basato sugli indici usando i livelli (vedi sotto).

![Ordine di disegno](images/gui/draw_order.png)

Seleziona un nodo e premi <kbd>Alt + Up/Down</kbd> per spostarlo in alto o in basso e modificarne l'ordine nell'elenco.

L'ordine di disegno può essere modificato tramite script:

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Gerarchie genitore-figlio {#parent-child-hierarchies}

Per rendere un nodo figlio di un altro, trascinalo sul nodo che vuoi usare come genitore. Un nodo con un genitore eredita la trasformazione (posizione, rotazione e scala) applicata al genitore e riferita al perno del genitore.

![Genitore e figlio](images/gui/parent_child.png)

I genitori vengono disegnati prima dei figli. Usa i livelli per modificare l'ordine di disegno dei nodi genitori e figli e per ottimizzare il rendering dei nodi (vedi sotto).


## Livelli e chiamate di disegno {#layers-and-draw-calls}

I livelli offrono un controllo preciso su come vengono disegnati i nodi e possono essere utilizzati per ridurre il numero di chiamate di disegno che il motore deve creare per disegnare una scena GUI. Quando il motore sta per disegnare i nodi di una scena GUI, li raggruppa in batch di chiamate di disegno in base alle seguenti condizioni:

- I nodi devono essere dello stesso tipo.
- I nodi devono usare lo stesso atlas o la stessa sorgente di tile.
- I nodi devono essere visualizzati con la stessa modalità di fusione.
- Devono usare lo stesso carattere.

Se un nodo differisce dal precedente per uno qualsiasi di questi aspetti, interrompe il batch e genera un'altra chiamata di disegno. I nodi di ritaglio interrompono sempre il batch e anche ogni ambito stencil lo interrompe.

La possibilità di organizzare i nodi in gerarchie permette di raggrupparli facilmente in unità gestibili. Tuttavia, le gerarchie possono interrompere il rendering in batch se mescoli tipi di nodi diversi:

![Gerarchia che interrompe il batch](images/gui/break_batch.png)

Quando la pipeline di rendering percorre l'elenco dei nodi, è costretta a creare un batch separato per ciascun nodo perché i tipi sono diversi. In totale, questi tre pulsanti richiedono sei chiamate di disegno.

Assegnando livelli ai nodi, puoi ordinarli diversamente e consentire alla pipeline di rendering di raggrupparli in un numero minore di chiamate di disegno. Inizia aggiungendo alla scena i livelli necessari. <kbd>Fai clic con il pulsante destro del mouse</kbd> sull'icona della cartella "Layers" nella vista *Outline* e seleziona <kbd>Add ▸ Layer</kbd>. Seleziona il nuovo livello e assegnagli un valore per la proprietà *Name* nella vista *Properties*.

![Livelli](images/gui/layers.png)

Quindi imposta la proprietà *Layer* di ogni nodo sul livello corrispondente. L'ordine di disegno dei livelli ha la precedenza sul normale ordine dei nodi basato sugli indici. Assegnando i nodi Box della grafica dei pulsanti a "graphics" e i nodi Text dei pulsanti a "text", ottieni quindi il seguente ordine di disegno:

* Prima tutti i nodi del livello "graphics", dall'alto:

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Poi tutti i nodi del livello "text", dall'alto:

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Ora i nodi possono essere raggruppati in due chiamate di disegno anziché sei. Un grande vantaggio per le prestazioni!

Un nodo figlio senza un livello impostato eredita implicitamente il livello del nodo genitore. Non impostare un livello su un nodo lo aggiunge implicitamente al livello "null", che viene disegnato prima di qualsiasi altro livello.
