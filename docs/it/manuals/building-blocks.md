---
title: Gli elementi fondamentali di Defold
brief: Questo manuale approfondisce il funzionamento di oggetti di gioco, componenti e collezioni.
---

#  Elementi fondamentali {#building-blocks}

Alla base della progettazione di Defold ci sono alcuni concetti che è molto importante comprendere bene. Questo manuale spiega quali sono gli elementi fondamentali di Defold. Dopo averlo letto, prosegui con il [manuale sull'indirizzamento](/manuals/addressing) e il [manuale sullo scambio di messaggi](/manuals/message-passing). Nell'editor è disponibile anche una serie di [tutorial](/tutorials/getting-started) per iniziare rapidamente.

![Elementi fondamentali](images/building_blocks/building_blocks.png)

Per costruire un gioco con Defold utilizzi tre tipi di elementi fondamentali:

Collezione (collection)
: Una collezione è un file usato per strutturare il gioco. Nelle collezioni costruisci gerarchie di oggetti di gioco e altre collezioni. In genere vengono usate per strutturare livelli di gioco, gruppi di nemici o personaggi composti da più oggetti di gioco.

Oggetto di gioco (game object)
: Un oggetto di gioco è un contenitore dotato di ID, posizione, rotazione e scala. Serve a contenere componenti. In genere gli oggetti di gioco vengono usati per creare i personaggi del giocatore, proiettili, il sistema di regole del gioco o un sistema di caricamento dei livelli.

Componente (component)
: I componenti sono entità inserite negli oggetti di gioco per dar loro una rappresentazione visiva, sonora e/o logica nel gioco. In genere vengono usati per creare gli sprite dei personaggi, file di script, aggiungere effetti sonori o effetti particellari.

## Collezioni {#collections}

Le collezioni sono strutture ad albero che contengono oggetti di gioco e altre collezioni. Una collezione viene sempre salvata in un file.

All'avvio, il motore Defold carica una singola _collezione di bootstrap_, specificata nel file delle impostazioni *game.project*. La collezione di bootstrap si chiama spesso "main.collection", ma puoi usare il nome che preferisci.

Una collezione può contenere oggetti di gioco e altre collezioni (tramite un riferimento al file della sottocollezione), annidate a qualsiasi profondità. Ecco un file di esempio chiamato "main.collection". Contiene un oggetto di gioco (con ID "can") e una sottocollezione (con ID "bean"). La sottocollezione, a sua volta, contiene due oggetti di gioco: "bean" e "shield".

![Collezione](images/building_blocks/collection.png)

Nota che la sottocollezione con ID "bean" è salvata in un proprio file, chiamato "/main/bean.collection", e in "main.collection" è presente soltanto un riferimento ad essa:

![Collezione bean](images/building_blocks/bean_collection.png)

Non puoi indirizzare direttamente le collezioni, perché durante l'esecuzione non esistono oggetti corrispondenti alle collezioni "main" e "bean". Tuttavia, a volte devi usare l'identità di una collezione come parte del _percorso_ di un oggetto di gioco (consulta il [manuale sull'indirizzamento](/manuals/addressing) per i dettagli):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Una collezione viene sempre aggiunta a un'altra collezione come riferimento a un file di collezione:

<kbd>Fai clic con il pulsante destro</kbd> sulla collezione nella vista *Outline* e seleziona <kbd>Add Collection File</kbd>.

## Oggetti di gioco {#game-objects}

Gli oggetti di gioco sono oggetti semplici, ciascuno con una durata di vita indipendente durante l'esecuzione del gioco. Gli oggetti di gioco hanno una posizione, una rotazione e una scala, tutte modificabili e animabili durante l'esecuzione.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Gli oggetti di gioco possono essere usati vuoti (per esempio, come indicatori di posizione), ma di solito sono dotati di vari componenti, come sprite, suoni, script, modelli, fabbriche (factory) e altro ancora. Gli oggetti di gioco vengono creati nell'editor e inseriti nei file di collezione, oppure generati dinamicamente durante l'esecuzione tramite componenti _fabbrica_.

Gli oggetti di gioco vengono aggiunti direttamente a una collezione oppure come riferimento a un file di oggetto di gioco:

<kbd>Fai clic con il pulsante destro</kbd> sulla collezione nella vista *Outline* e seleziona <kbd>Add Game Object</kbd> (aggiunta diretta) o <kbd>Add Game Object File</kbd> (aggiunta come riferimento a un file).


## Componenti {#components}

:[components](../shared/components.md)

Consulta la [panoramica dei componenti](/manuals/components/) per un elenco di tutti i tipi di componenti disponibili.

## Oggetti aggiunti direttamente o per riferimento {#objects-added-in-place-or-by-reference}

Quando crei un _file_ di collezione, oggetto di gioco o componente, crei ciò che chiamiamo un prototipo (noto anche come "prefab" o "blueprint" in altri motori). Questa operazione aggiunge soltanto un file alla struttura dei file del progetto, senza aggiungere nulla al gioco in esecuzione. Per aggiungere un'istanza di una collezione, di un oggetto di gioco o di un componente basata su un file di prototipo, aggiungine un'istanza a uno dei tuoi file di collezione.

Nella vista Outline puoi vedere su quale file si basa un'istanza di un oggetto. Il file "main.collection" contiene tre istanze basate su file:

1. La sottocollezione "bean".
2. Il componente script "bean" nell'oggetto di gioco "bean" della sottocollezione "bean".
3. Il componente script "can" nell'oggetto di gioco "can".

![Istanza](images/building_blocks/instance.png)

Il vantaggio di creare file di prototipo diventa evidente quando hai più istanze di un oggetto di gioco o di una collezione e vuoi modificarle tutte:

![Istanze di oggetti di gioco](images/building_blocks/go_instance.png)

Modificando il file di prototipo, tutte le istanze che usano quel file vengono aggiornate immediatamente.

![Modifica del prototipo di un oggetto di gioco](images/building_blocks/go_change_blueprint.png)

Qui viene modificata l'immagine dello sprite nel file di prototipo e tutte le istanze che usano il file vengono aggiornate immediatamente:

![Istanze di oggetti di gioco aggiornate](images/building_blocks/go_instance2.png)

## Gerarchie genitore-figlio tra oggetti di gioco {#childing-game-objects}

In un file di collezione puoi costruire gerarchie di oggetti di gioco in cui uno o più oggetti di gioco sono figli di un unico oggetto di gioco genitore. È sufficiente <kbd>trascinare</kbd> un oggetto di gioco e <kbd>rilasciarlo</kbd> su un altro per rendere l'oggetto trascinato figlio dell'oggetto di destinazione:

![Gerarchie genitore-figlio tra oggetti di gioco](images/building_blocks/childing.png)

Le gerarchie genitore-figlio tra oggetti sono relazioni dinamiche che influiscono sul modo in cui gli oggetti reagiscono alle trasformazioni. Qualsiasi trasformazione (spostamento, rotazione o modifica della scala) applicata a un oggetto viene a sua volta applicata ai suoi figli, sia nell'editor sia durante l'esecuzione:

![Trasformazione di un figlio](images/building_blocks/child_transform.png)

Le traslazioni di un figlio, invece, avvengono nello spazio locale del genitore. Nell'editor puoi scegliere di modificare un oggetto di gioco figlio nello spazio locale o nello spazio globale selezionando <kbd>Edit ▸ World Space</kbd> (l'impostazione predefinita) o <kbd>Edit ▸ Local Space</kbd>.

È anche possibile cambiare il genitore di un oggetto durante l'esecuzione inviando all'oggetto un messaggio `set_parent`.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Un equivoco comune è pensare che la posizione di un oggetto di gioco nella gerarchia delle collezioni cambi quando entra a far parte di una gerarchia genitore-figlio. Si tratta, invece, di due cose molto diverse. Le gerarchie genitore-figlio modificano dinamicamente il grafo della scena, permettendo di collegare visivamente gli oggetti tra loro. L'unico elemento che determina l'indirizzo di un oggetto di gioco è la sua posizione nella gerarchia delle collezioni. L'indirizzo rimane invariato per tutta la durata di vita dell'oggetto.
:::
