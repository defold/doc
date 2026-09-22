---
title: Gestione delle risorse in Defold
brief: Questo manuale spiega come Defold gestisce automaticamente le risorse e come puoi gestirne manualmente il caricamento per rispettare i limiti di occupazione della memoria e dimensioni del bundle.
---

# Gestione delle risorse {#resource-management}

Se realizzi un gioco molto piccolo, i limiti della piattaforma di destinazione (occupazione della memoria, dimensioni del bundle, potenza di calcolo e consumo della batteria) potrebbero non creare mai problemi. Quando realizzi giochi più grandi, invece, soprattutto per dispositivi portatili, il consumo di memoria sarà probabilmente uno dei vincoli principali. Un team esperto stabilisce con cura i budget delle risorse in base ai limiti della piattaforma. Defold offre diverse funzionalità per aiutarti a gestire la memoria e le dimensioni del bundle. Questo manuale ne fornisce una panoramica.

## L'albero statico delle risorse {#the-static-resource-tree}

Quando crei una build di un gioco in Defold, dichiari staticamente l'albero delle risorse. Ogni parte del gioco è collegata all'albero, a partire dalla collezione di bootstrap (di solito chiamata "main.collection"). L'albero delle risorse segue tutti i riferimenti e include tutte le risorse a essi associate:

- Dati degli oggetti di gioco (game object) e dei componenti (atlas, suoni ecc.).
- Prototipi dei componenti di fabbrica (factory), ossia oggetti di gioco e collezioni.
- Riferimenti dei componenti proxy di collezione (collection proxy), ossia collezioni.
- [Risorse personalizzate](/manuals/project-settings/#custom-resources) dichiarate in *game.project*.

![Albero delle risorse](images/resource/resource_tree.png)

::: sidenote
Defold prevede anche il concetto di [risorse del bundle](/manuals/project-settings/#bundle-resources). Queste risorse vengono incluse nel bundle dell'applicazione, ma non fanno parte dell'albero delle risorse. Possono comprendere file di supporto specifici della piattaforma o file esterni [caricati dal file system](/manuals/file-access/#how-to-access-files-bundled-with-the-application) e utilizzati dal gioco (per esempio, banchi di suoni FMOD).
:::

Quando *crei il bundle* del gioco, viene incluso soltanto ciò che si trova nell'albero delle risorse. Tutto ciò che non è referenziato nell'albero viene escluso. Non occorre selezionare manualmente cosa includere o escludere dal bundle.

Quando il gioco viene *eseguito*, il motore parte dalla radice di bootstrap dell'albero e carica in memoria le risorse:

- Ogni collezione referenziata e il suo contenuto.
- Oggetti di gioco e dati dei componenti.
- Prototipi dei componenti di fabbrica (oggetti di gioco e collezioni).

Il motore, tuttavia, non carica automaticamente durante l'esecuzione i seguenti tipi di risorse referenziate:

- Collezioni dei mondi di gioco referenziate tramite proxy di collezione. I mondi di gioco sono relativamente grandi, quindi devi attivarne manualmente il caricamento e lo scaricamento tramite codice. Consulta [il manuale sui proxy di collezione](/manuals/collection-proxy) per i dettagli.
- File aggiunti tramite l'impostazione *Custom Resources* in *game.project*. Questi file vengono caricati manualmente con la funzione [`sys.load_resource()`](/ref/sys/#sys.load_resource).

Puoi modificare il comportamento predefinito con cui Defold include le risorse nel bundle e le carica, per controllare in dettaglio come e quando entrano in memoria.

![Caricamento delle risorse](images/resource/loading.png)

## Caricamento dinamico delle risorse delle fabbriche {#dynamically-loading-factory-resources}

Le risorse referenziate dai componenti di fabbrica vengono normalmente caricate in memoria quando viene caricato il componente. Le risorse sono quindi pronte per generare oggetti nel gioco non appena la fabbrica esiste nel runtime. Per modificare il comportamento predefinito e rimandare il caricamento delle risorse di una fabbrica, basta selezionare la sua casella *Load Dynamically*.

![Caricamento dinamico](images/resource/load_dynamically.png)

Con questa casella selezionata, il motore include comunque le risorse referenziate nel bundle del gioco, ma non carica automaticamente le risorse della fabbrica. Hai invece due possibilità:

1. Chiama [`factory.create()`](/ref/factory/#factory.create) o [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) quando vuoi generare oggetti. Le risorse vengono caricate in modo sincrono, dopodiché vengono generate nuove istanze.
2. Chiama [`factory.load()`](/ref/factory/#factory.load) o [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) per caricare le risorse in modo asincrono. Quando le risorse sono pronte per generare oggetti, viene invocata una callback.

Consulta il [manuale sulle fabbriche](/manuals/factory) e il [manuale sulle fabbriche di collezioni (collection factory)](/manuals/collection-factory) per i dettagli sul funzionamento.

## Scaricamento delle risorse caricate dinamicamente {#unloading-dynamically-loaded-resources}

Defold mantiene un contatore dei riferimenti per ogni risorsa. Se il contatore di una risorsa raggiunge zero, significa che non ci sono più riferimenti a essa. La risorsa viene quindi scaricata automaticamente dalla memoria. Per esempio, se elimini tutti gli oggetti generati da una fabbrica e anche l'oggetto che contiene il componente di fabbrica, le risorse a cui la fabbrica faceva riferimento vengono scaricate dalla memoria.

Per le fabbriche con l'opzione *Load Dynamically* selezionata, puoi chiamare la funzione [`factory.unload()`](/ref/factory/#factory.unload) o [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload). Questa chiamata rimuove il riferimento del componente di fabbrica alla risorsa. Se non ci sono altri riferimenti alla risorsa (per esempio, se tutti gli oggetti generati sono stati eliminati), la risorsa viene scaricata dalla memoria.

## Esclusione delle risorse dal bundle {#excluding-resources-from-bundle}

Con i proxy di collezione, puoi escludere dal processo di creazione del bundle tutte le risorse a cui il componente fa riferimento. È utile se devi ridurre al minimo le dimensioni del bundle. Per esempio, quando esegui giochi sul web in HTML5, il browser scarica l'intero bundle prima di eseguire il gioco.

![Esclusione](images/resource/exclude.png)

Selezionando l'opzione *Exclude* di un proxy di collezione, la risorsa referenziata viene esclusa dal bundle del gioco. Puoi invece archiviare le collezioni escluse su un servizio di archiviazione cloud a tua scelta. Il [manuale su Live Update](/manuals/live-update/) spiega come funziona questa funzionalità.
