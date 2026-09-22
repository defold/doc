I componenti (component) consentono di assegnare agli oggetti di gioco (game object) un aspetto specifico e/o funzionalità specifiche. I componenti devono essere contenuti in oggetti di gioco e risentono della posizione, della rotazione e della scala dell'oggetto di gioco che li contiene:

![Componenti](../shared/images/components.png)

Molti componenti hanno proprietà specifiche del proprio tipo che possono essere modificate; sono inoltre disponibili funzioni specifiche per ciascun tipo di componente, che consentono di interagire con essi durante l'esecuzione:

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

I componenti vengono aggiunti direttamente a un oggetto di gioco oppure come riferimenti a file di componenti:

<kbd>Fai clic con il pulsante destro</kbd> sull'oggetto di gioco nella vista *Outline* e seleziona <kbd>Add Component</kbd> (aggiunta diretta) oppure <kbd>Add Component File</kbd> (aggiunta come riferimento a un file).

Nella maggior parte dei casi conviene creare i componenti direttamente nell'oggetto di gioco, ma i seguenti tipi di componenti devono essere creati in file di risorsa separati prima di essere aggiunti a un oggetto di gioco tramite riferimento:

* Script
* GUI
* Particle FX
* Tile Map
