---
title: Nodi GUI a settore circolare di Defold
brief: Questo manuale spiega come usare i nodi a settore circolare nelle scene GUI di Defold.
---

# Nodi GUI a settore circolare {#gui-pie-nodes}

I nodi a settore circolare (pie) consentono di creare oggetti circolari o ellissoidali, dai semplici cerchi ai settori circolari e agli anelli quadrati.

## Creazione di un nodo a settore circolare {#creating-a-pie-node}

<kbd>Fai clic con il pulsante destro</kbd> sulla sezione *Nodes* nella vista *Outline* e seleziona <kbd>Add ▸ Pie</kbd>. Il nuovo nodo a settore circolare viene selezionato e puoi modificarne le proprietà.

![Creazione di un nodo a settore circolare](images/gui-pie/create.png)

Le seguenti proprietà sono specifiche dei nodi a settore circolare:

Inner Radius
: Il raggio interno del nodo, espresso lungo l'asse X.

Outer Bounds
: La forma del contorno esterno del nodo.

  - `Ellipse` estende il nodo fino al raggio esterno.
  - `Rectangle` estende il nodo fino al suo rettangolo di delimitazione.

Perimeter Vertices
: Il numero di segmenti usati per costruire la forma, espresso come numero di vertici necessari a circoscrivere l'intero perimetro di 360 gradi del nodo.

Pie Fill Angle
: La porzione del settore circolare da riempire, espressa come angolo misurato in senso antiorario a partire da destra.

![Proprietà](images/gui-pie/properties.png)

Se imposti una texture sul nodo, l'immagine della texture viene applicata in piano, facendo corrispondere gli angoli della texture a quelli del rettangolo di delimitazione del nodo.

## Modifica dei nodi a settore circolare durante l'esecuzione {#modify-pie-nodes-at-runtime}

I nodi a settore circolare supportano tutte le funzioni generiche di manipolazione dei nodi per impostare dimensioni, punto di pivot, colore e così via. Esistono inoltre alcune funzioni e proprietà specifiche dei nodi a settore circolare:

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
