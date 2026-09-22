---
title: Manuale dei modelli GUI
brief: Questo manuale spiega il sistema di modelli GUI di Defold, utilizzato per creare componenti visivi GUI riutilizzabili basati su modelli condivisi o 'prefab'.
---

# Nodi modello GUI {#gui-template-nodes}

I nodi modello GUI (GUI template) offrono un potente meccanismo per creare componenti GUI riutilizzabili basati su modelli condivisi o "prefab". Questo manuale spiega la funzionalità e come utilizzarla.

Un modello GUI è una scena GUI che viene istanziata, nodo per nodo, in un'altra scena GUI. È poi possibile sovrascrivere qualsiasi valore delle proprietà dei nodi del modello originale.

## Creazione di un modello {#creating-a-template}

Un modello GUI è una normale scena GUI, quindi si crea come qualsiasi altra scena GUI. <kbd>Fai clic con il pulsante destro</kbd> su una posizione nel pannello *Assets* e seleziona <kbd>New... ▸ Gui</kbd>.

![Creazione di un modello](images/gui-templates/create.png)

Crea il modello e salvalo. Tieni presente che i nodi dell'istanza saranno posizionati rispetto all'origine, quindi è consigliabile creare il modello nella posizione 0, 0, 0.

## Creazione di istanze da un modello {#creating-instances-from-a-template}

Puoi creare un numero qualsiasi di istanze basate sul modello. Crea o apri la scena GUI in cui vuoi collocare il modello, poi <kbd>fai clic con il pulsante destro</kbd> sulla sezione *Nodes* della vista *Outline* e seleziona <kbd>Add ▸ Template</kbd>.

![Creazione di un'istanza](images/gui-templates/create_instance.png)

Imposta la proprietà *Template* sul file della scena GUI del modello.

Puoi aggiungere un numero qualsiasi di istanze del modello e, per ogni istanza, puoi sovrascrivere le proprietà di ciascun nodo, modificandone la posizione, il colore, le dimensioni, la texture e così via.

![Istanze](images/gui-templates/instances.png)

Ogni proprietà che modifichi viene evidenziata in blu nell'editor. Premi il pulsante di ripristino accanto alla proprietà per riportarla al valore del modello:

![Proprietà](images/gui-templates/properties.png)

Anche tutti i nodi con proprietà sovrascritte sono evidenziati in blu nella vista *Outline*:

![Vista della struttura](images/gui-templates/outline.png)

L'istanza del modello viene elencata come voce comprimibile nella vista *Outline*. Tuttavia, tieni presente che questa voce nella vista della struttura *non è un nodo*. L'istanza del modello non esiste nemmeno durante l'esecuzione, mentre esistono tutti i nodi che ne fanno parte.

I nodi che fanno parte di un'istanza del modello vengono denominati automaticamente anteponendo un prefisso e una barra (`"/"`) al loro *Id*. Il prefisso è l'*Id* impostato nell'istanza del modello.

## Modifica dei modelli a runtime {#modifying-templates-in-runtime}

Gli script che modificano o interrogano i nodi aggiunti tramite il meccanismo dei modelli devono soltanto tenere conto dei nomi dei nodi dell'istanza e includere l'*Id* dell'istanza del modello come prefisso del nome del nodo:

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Do something...
end
```

Non esiste un nodo che corrisponda all'istanza del modello stessa. Se ti serve un nodo radice per un'istanza, aggiungilo al modello.

Se uno script è associato alla scena GUI di un modello, lo script non fa parte dell'albero dei nodi dell'istanza. Puoi associare un solo script a ciascuna scena GUI, quindi la logica dello script deve risiedere nella scena GUI in cui hai istanziato i modelli.
