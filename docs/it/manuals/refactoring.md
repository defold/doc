---
title: Riorganizzazione (refactoring)
brief: Questo manuale spiega come modificare facilmente la struttura del progetto grazie alle potenti funzionalità di riorganizzazione.
---

# Riorganizzazione (refactoring) {#refactoring}

Il refactoring consiste nel riorganizzare il codice e gli asset esistenti. Durante lo sviluppo di un progetto, spesso emerge la necessità di modificare o spostare alcuni elementi: i nomi devono cambiare per rispettare le convenzioni di denominazione o migliorare la chiarezza, mentre i file di codice o gli asset devono essere spostati in una posizione più logica nella gerarchia del progetto.

Defold ti aiuta a riorganizzare il progetto in modo efficiente tenendo traccia dell'utilizzo degli asset. Aggiorna automaticamente i riferimenti agli asset che vengono rinominati o spostati, anche quando le due operazioni avvengono insieme. Come sviluppatore, dovresti poter lavorare liberamente. Il tuo progetto è una struttura flessibile che puoi modificare a piacimento senza temere che tutto smetta di funzionare.

::: important
La riorganizzazione automatica funziona soltanto se le modifiche vengono effettuate all'interno dell'editor. Se rinomini o sposti un file al di fuori dell'editor, i riferimenti a quel file non vengono modificati automaticamente.
:::

Tuttavia, se interrompi un riferimento, per esempio eliminando un asset, l'editor non può risolvere il problema, ma fornisce utili segnalazioni di errore. Per esempio, se elimini un'animazione da un atlas e quell'animazione è utilizzata da qualche parte, Defold segnala un errore quando provi ad avviare il gioco. L'editor indica anche dove si verificano gli errori per aiutarti a individuare rapidamente il problema:

![Errore di riorganizzazione](images/workflow/delete_error.png)

Gli errori di build vengono visualizzati nel pannello *Build Errors* nella parte inferiore dell'editor. <kbd>Facendo doppio clic</kbd> su un errore, passi al punto in cui si trova il problema.
