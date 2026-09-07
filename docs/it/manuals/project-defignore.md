---
title: Esclusioni nei progetti Defold
brief: Questo manuale descrive come ignorare file e cartelle in Defold.
---

# Ignorare file {#ignoring-files}

Puoi configurare l'editor e gli strumenti Defold in modo che ignorino file e cartelle di un progetto. Questo può essere utile se il progetto contiene file con estensioni in conflitto con quelle usate da Defold. Un esempio sono i file del linguaggio Go con estensione `.go`, la stessa che l'editor usa per i file degli oggetti di gioco (game object).

## Il file `.defignore` {#the-defignore-file}
I file e le cartelle da escludere sono definiti in un file chiamato `.defignore` nella radice del progetto. Il file deve elencare i file e le cartelle da escludere, uno per riga. Esempio:

```
/path/to/file.png
/otherpath
```

Questo esclude il file `/path/to/file.png` e tutto ciò che si trova nel percorso `/otherpath`.

## Il file `.defunload` {#the-defunload-file}

In alcuni progetti di grandi dimensioni che contengono più moduli indipendenti, potresti voler escludere dal caricamento alcune parti per ridurre l'uso della memoria e i tempi di caricamento nell'editor. Per farlo, puoi elencare i percorsi da escludere dal caricamento in un file `.defunload` all'interno della directory del progetto.

In pratica, il file `.defunload` ti permette di nascondere parti del progetto all'editor senza che i riferimenti alle risorse nascoste causino errori di build.

I criteri di corrispondenza in `.defunload` seguono le stesse regole del file `.defignore`. Le collezioni (collection) e gli oggetti di gioco non caricati si comportano come se fossero vuoti quando le risorse caricate vi fanno riferimento. Le altre risorse che corrispondono ai criteri di `.defunload` rimangono in uno stato non caricato e non possono essere visualizzate nell'editor. Tuttavia, se una risorsa caricata dipende da esse, le risorse non caricate e le loro dipendenze vengono caricate automaticamente.

Per esempio, se uno sprite dipende da immagini contenute in un atlas, è necessario caricare l'atlas, altrimenti l'immagine mancante viene segnalata come errore. In questo caso, una notifica avvisa l'utente della situazione e indica a quale risorsa non caricata è stato fatto riferimento e da dove.

L'editor impedisce all'utente di aggiungere riferimenti a risorse `.defunloaded` dalle risorse caricate, quindi questa situazione si verifica solo quando le risorse vengono lette dal disco.

A differenza del file `.defignore`, dopo aver modificato il file `.defunload` devi riavviare l'editor affinché le modifiche abbiano effetto.
