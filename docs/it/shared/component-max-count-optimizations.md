## Ottimizzazioni del numero massimo di componenti {#component-max-count-optimizations}
Il file delle impostazioni *game.project* contiene molti valori che specificano il numero massimo di risorse di un determinato tipo che possono esistere contemporaneamente, spesso conteggiato per ciascuna collezione caricata (detta anche mondo). Il motore Defold usa questi valori massimi per preallocare la memoria necessaria, evitando allocazioni dinamiche e frammentazione della memoria durante l'esecuzione del gioco.

Le strutture dati di Defold usate per rappresentare i componenti e le altre risorse sono ottimizzate per occupare meno memoria possibile, ma occorre comunque impostare i valori con attenzione per evitare di allocare più memoria di quanta sia effettivamente necessaria.

Per ottimizzare ulteriormente l'uso della memoria, il processo di build di Defold analizza il contenuto del gioco e sostituisce i valori massimi quando è possibile determinare con certezza le quantità esatte:

* Se una collezione non contiene alcun componente fabbrica (factory), viene allocata la quantità esatta di ciascun tipo di componente e di oggetto di gioco e i valori massimi vengono ignorati.
* Se una collezione contiene un componente fabbrica, vengono analizzati gli oggetti generati e il valore massimo viene usato per i componenti che possono essere generati dalle fabbriche e per gli oggetti di gioco.
* Se una collezione contiene una fabbrica o una fabbrica di collezioni (collection factory) con l'opzione "Dynamic Prototype" attivata, questa collezione usa i valori massimi dei contatori.
