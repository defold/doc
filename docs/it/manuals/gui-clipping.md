---
title: Manuale del ritaglio nella GUI
brief: Questo manuale descrive come creare nodi GUI che mascherano altri nodi tramite il ritaglio stencil.
---

# Ritaglio {#clipping}

I nodi GUI possono essere usati come nodi di *ritaglio (clipping)*---maschere che controllano il rendering degli altri nodi. Questo manuale spiega come funziona questa funzionalità.

## Creare un nodo di ritaglio {#creating-a-clipping-node}

I nodi Box, Text e Pie possono essere usati per il ritaglio. Per creare un nodo di ritaglio, aggiungi un nodo alla GUI, quindi imposta le sue proprietà come segue:

Clipping Mode
: La modalità usata per il ritaglio.
  - `None` esegue il rendering del nodo senza alcun ritaglio.
  - `Stencil` fa sì che il nodo scriva nella maschera stencil corrente.

Clipping Visible
: Seleziona questa opzione per eseguire il rendering del contenuto del nodo.

Clipping Inverted
: Seleziona questa opzione per scrivere nella maschera l'inverso della forma del nodo.

Quindi aggiungi i nodi da ritagliare come figli del nodo di ritaglio.

![Creare un ritaglio](images/gui-clipping/create.png)

## Maschera stencil {#stencil-mask}

Il ritaglio funziona tramite nodi che scrivono in un *buffer stencil*. Questo buffer contiene maschere di ritaglio: informazioni che indicano alla scheda grafica se un pixel deve essere visualizzato o meno.

- Un nodo senza un genitore di ritaglio, ma con la modalità di ritaglio impostata su `Stencil`, scrive la propria forma (o il suo inverso) in una nuova maschera di ritaglio memorizzata nel buffer stencil.
- Se un nodo di ritaglio ha un genitore di ritaglio, ritaglia invece la maschera del genitore. Un nodo figlio di ritaglio non può mai _estendere_ la maschera di ritaglio corrente, ma soltanto ritagliarla ulteriormente.
- I nodi che non eseguono ritagli e sono figli di nodi di ritaglio vengono visualizzati con la maschera di ritaglio creata dalla gerarchia dei genitori.

![Gerarchia di ritaglio](images/gui-clipping/setup.png)

Qui tre nodi sono organizzati in una gerarchia:

- Sia l'esagono sia il quadrato sono nodi di ritaglio stencil.
- L'esagono crea una nuova maschera di ritaglio, mentre il quadrato la ritaglia ulteriormente.
- Il nodo circolare è un normale nodo Pie, quindi viene visualizzato con la maschera di ritaglio creata dai suoi genitori di ritaglio.

Per questa gerarchia sono possibili quattro combinazioni di nodi di ritaglio normali e invertiti. L'area verde indica la parte del cerchio che viene visualizzata. Il resto è mascherato:

![Maschere stencil](images/gui-clipping/modes.png)

## Limitazioni degli stencil {#stencil-limitations}

- Il numero totale di nodi di ritaglio stencil non può superare 256.
- La profondità massima di annidamento dei nodi figli _stencil_ è di 8 livelli. (Contano solo i nodi con ritaglio stencil.)
- Il numero massimo di nodi stencil fratelli è 127. Per ogni livello in cui si scende nella gerarchia stencil, il limite massimo si dimezza.
- I nodi invertiti hanno un costo maggiore. Il limite è di 8 nodi di ritaglio invertiti e ciascuno dimezza il numero massimo di nodi di ritaglio non invertiti.
- Gli stencil generano una maschera stencil dalla _geometria_ del nodo (non dalla texture). Puoi invertire la maschera impostando la proprietà *Inverted clipper*.


## Livelli {#layers}

I livelli possono essere usati per controllare l'ordine di rendering (e il raggruppamento in batch) dei nodi. Quando usi livelli e nodi di ritaglio, il normale ordine dei livelli viene modificato. L'ordine dei livelli ha sempre la precedenza sull'ordine di ritaglio---se combini l'assegnazione dei livelli con i nodi di ritaglio, il ritaglio potrebbe avvenire in un ordine errato se un nodo genitore con il ritaglio abilitato appartiene a un livello superiore a quello dei suoi figli. I figli senza un livello assegnato rispettano comunque la gerarchia e vengono quindi disegnati e ritagliati dopo il genitore.

::: sidenote
Un nodo di ritaglio e la sua gerarchia vengono disegnati per primi se al nodo è assegnato un livello, oppure nell'ordine normale se non è assegnato alcun livello.
:::

![Livelli e ritaglio](images/gui-clipping/layers.png)

In questo esempio, entrambi i nodi di ritaglio "`Donut BG`" e "`BG`" usano lo stesso livello 1. Il loro ordine di rendering segue l'ordine nella gerarchia, dove "`Donut BG`" viene visualizzato prima di "`BG`". Tuttavia, il nodo figlio "`Donut Shadow`" è assegnato al livello 2, che ha un ordine superiore, e viene quindi visualizzato dopo entrambi i nodi di ritaglio. In questo caso, l'ordine di rendering è:

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Qui puoi vedere che l'oggetto "`Donut Shadow`" viene ritagliato da entrambi i nodi di ritaglio a causa dell'ordine dei livelli, anche se è figlio di uno solo di essi.
