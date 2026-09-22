---
title: Componenti degli oggetti di gioco
brief: Questo manuale offre una panoramica dei componenti e spiega come usarli.
---

#  Componenti {#components}

:[components](../shared/components.md)

## Tipi di componenti {#component-types}

Defold supporta i seguenti tipi di componenti:

* [Fabbrica di collezioni (collection factory)](/manuals/collection-factory) - Genera collezioni
* [Proxy di collezione (collection proxy)](/manuals/collection-proxy) - Carica e scarica collezioni
* [Oggetto di collisione](/manuals/physics) - Fisica 2D e 3D
* [Telecamera](/manuals/camera) - Modifica il viewport e la proiezione del mondo di gioco
* [Fabbrica (factory)](/manuals/factory) - Genera oggetti di gioco
* [GUI](/manuals/gui) - Esegue il rendering di un'interfaccia utente grafica
* [Etichetta](/manuals/label) - Esegue il rendering di un testo
* [Luce](/manuals/light) - Aggiunge dati di illuminazione per gli shader
* [Mesh](/manuals/mesh) Mostra una mesh 3D (con creazione e modifica a runtime)
* [Modello](/manuals/model) Mostra un modello 3D (con animazioni facoltative)
* [Effetti particellari (Particle FX)](/manuals/particlefx) -  Genera particelle
* [Script](/manuals/script) - Aggiunge la logica di gioco
* [Suono](/manuals/sound) - Riproduce suoni o musica
* [Sprite](/manuals/sprite) - Mostra un'immagine 2D (con animazione flipbook facoltativa)
* [Mappa di tessere (tilemap)](/manuals/tilemap) - Mostra una griglia di tessere

È possibile aggiungere altri componenti tramite estensioni:

* [Modello Rive](/extension-rive) - Esegue il rendering di un'animazione Rive
* [Modello Spine](/extension-spine) - Esegue il rendering di un'animazione Spine


## Abilitazione e disabilitazione dei componenti {#enabling-and-disabling-components}

I componenti di un oggetto di gioco vengono abilitati quando viene creato l'oggetto di gioco. Per disabilitare un componente, inviagli un messaggio [`disable`](/ref/go/#disable):

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

Per abilitare nuovamente un componente, puoi inviargli un messaggio [`enable`](/ref/go/#enable):

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Proprietà dei componenti {#component-properties}

Ogni tipo di componente di Defold ha proprietà diverse. Il [pannello Properties](/manuals/editor/#the-editor-views) dell'editor mostra le proprietà del componente attualmente selezionato nel [pannello Outline](/manuals/editor/#the-editor-views). Consulta i manuali dei diversi tipi di componenti per maggiori informazioni sulle proprietà disponibili.

## Posizione, rotazione e scala dei componenti {#component-position-rotation-and-scale}

I componenti visivi hanno solitamente proprietà di posizione e rotazione e, nella maggior parte dei casi, anche una proprietà di scala. Puoi modificare queste proprietà nell'editor, ma quasi sempre non puoi modificarle durante l'esecuzione (l'unica eccezione è la scala dei componenti sprite ed etichetta, che può essere modificata a runtime).

Se devi modificare la posizione, la rotazione o la scala di un componente durante l'esecuzione, modifica invece la posizione, la rotazione o la scala dell'oggetto di gioco a cui appartiene. Questo influisce anche su tutti gli altri componenti dell'oggetto di gioco. Se vuoi modificare un solo componente tra i molti associati a un oggetto di gioco, ti consigliamo di spostarlo in un oggetto di gioco separato e di aggiungere quest'ultimo come figlio dell'oggetto di gioco a cui il componente apparteneva in origine.

## Ordine di disegno dei componenti {#component-draw-order}

L'ordine di disegno dei componenti visivi dipende da due fattori:

### Predicati dello script di rendering {#render-script-predicates}
A ogni componente viene assegnato un [materiale](/manuals/material/) e ogni materiale ha uno o più tag. Lo script di rendering definisce a sua volta una serie di predicati, ciascuno dei quali corrisponde a uno o più tag dei materiali. I [predicati vengono disegnati uno alla volta](/manuals/render/#render-predicates) nella funzione *update()* dello script di rendering e vengono disegnati i componenti che corrispondono ai tag definiti in ciascun predicato. Lo script di rendering predefinito disegna prima gli sprite e le mappe di tessere in un passaggio, poi gli effetti particellari in un altro passaggio, entrambi nello spazio del mondo. Quindi disegna i componenti GUI in un passaggio separato nello spazio dello schermo.

### Valore Z dei componenti {#component-z-value}
Tutti gli oggetti di gioco e i componenti sono posizionati nello spazio 3D, con posizioni espresse come oggetti `vector3`. Quando visualizzi il contenuto grafico del gioco in 2D, i valori X e Y determinano la posizione di un oggetto lungo gli assi della "larghezza" e dell'"altezza", mentre la posizione Z determina la posizione lungo l'asse della "profondità". La posizione Z ti permette di controllare la visibilità degli oggetti sovrapposti: uno sprite con un valore Z di 1 apparirà davanti a uno sprite con posizione Z pari a 0. Per impostazione predefinita, Defold usa un sistema di coordinate che consente valori Z compresi tra -1 e 1:

![modello](images/graphics/z-order.png)

I componenti che corrispondono a un [predicato di rendering](/manuals/render/#render-predicates) vengono disegnati insieme e il loro ordine di disegno dipende dal valore Z finale del componente. Il valore Z finale di un componente è la somma dei valori Z del componente stesso, dell'oggetto di gioco a cui appartiene e di tutti gli oggetti di gioco genitori.

::: sidenote
L'ordine di disegno di più componenti GUI **non** è determinato dal loro valore Z. L'ordine di disegno dei componenti GUI è controllato dalla funzione [gui.set_render_order()](/ref/gui/#gui.set_render_order:order).
:::

Esempio: due oggetti di gioco A e B. B è figlio di A. B ha un componente sprite.

| Elemento | Valore Z |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Con la gerarchia riportata sopra, il valore Z finale del componente sprite di B è 2 + 1 + 0.5 = 3.5.

::: important
Se due componenti hanno esattamente lo stesso valore Z, l'ordine è indefinito: i componenti potrebbero sfarfallare, alternando la loro posizione davanti e dietro, oppure essere disegnati in un ordine su una piattaforma e in un altro ordine su un'altra piattaforma.

Lo script di rendering definisce un piano vicino e un piano lontano per i valori Z. I componenti con un valore Z al di fuori di questo intervallo non vengono disegnati. L'intervallo predefinito va da -1 a 1, ma [puoi modificarlo facilmente](/manuals/render/#default-view-projection). La precisione numerica dei valori Z con limiti vicino e lontano pari a -1 e 1 è molto elevata. Quando lavori con asset 3D, potrebbe essere necessario modificare i limiti vicino e lontano della proiezione predefinita in uno script di rendering personalizzato. Consulta il [manuale del rendering](/manuals/render/) per maggiori informazioni.
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
