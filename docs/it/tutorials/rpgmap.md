---
title: Esempio di mappa RPG
brief: In questo progetto di esempio impari un metodo per creare mappe RPG molto grandi.
---
# Mappa RPG - progetto di esempio {#rpg-map-sample-project}

In questo progetto di esempio, che puoi [aprire dall'editor](/manuals/project-setup/) o [scaricare da GitHub](https://github.com/defold/sample-rpgmap), mostriamo un metodo per creare mappe RPG molto grandi in Defold. La progettazione si basa sui seguenti presupposti:

1. Il mondo viene presentato una schermata alla volta. Questo permette al gioco di mantenere naturalmente nemici e personaggi non giocanti (NPC) entro i confini di una singola schermata. Chi progetta i livelli ha il pieno controllo su come il mondo viene presentato sullo schermo del giocatore.
2. Il personaggio del giocatore deve poter viaggiare per distanze arbitrarie senza che il gioco presenti problemi di precisione dei numeri in virgola mobile. Questi problemi fanno tipicamente tremolare gli oggetti in modo strano quando si allontanano molto dall'origine.
3. Il movimento del giocatore è limitato dagli ostacoli sulla mappa, quindi chi progetta i livelli può guidarlo tra le schermate usando alberi, rocce, acqua e altri ostacoli.
4. Deve essere possibile combinare mappe di tile, sprite e altri contenuti visivi.

Per prima cosa, esegui l'esempio ed esplora il mondo di 3x3 schermate per farti un'idea di come è organizzato. Controlli il personaggio con i tasti freccia.

## La collezione principale {#the-main-collection}

Apri "/main/main.collection" per visualizzare la collezione di bootstrap di questo esempio.

![](images/rpgmap/main_collection.png)

La collezione principale contiene l'oggetto di gioco del personaggio del giocatore, controllato in 8 direzioni con i tasti freccia, e un secondo oggetto di gioco chiamato "game" che controlla il flusso del gioco. L'oggetto "game" è composto da uno script e da una fabbrica di collezioni (collection factory) per ogni schermata del gioco. Le fabbriche sono denominate secondo lo schema di denominazione della griglia delle schermate.

Lo script "/main/game.script" tiene traccia della schermata in cui si trova attualmente il giocatore. Lo script risponde anche a un messaggio personalizzato chiamato "load_screen". Questo messaggio carica una nuova schermata e la sostituisce a quella attuale nella direzione in cui si muove l'eroe. All'inizio viene caricata una schermata al centro dello schermo e non ci sono altre schermate con cui scambiarla.

## Cambio di schermata {#changing-screens}

L'eroe è controllato dallo script "/main/hero.script". Lo script controlla se l'oggetto di gioco dell'eroe oltrepassa una linea superiore, inferiore, sinistra o destra vicina al bordo dello schermo:

![](images/rpgmap/change_screen.png)

1. Se l'eroe si avvicina abbastanza a un bordo dello schermo, viene inviato un messaggio allo script dell'oggetto "game" per caricare la schermata successiva.
2. La collezione della schermata successiva viene generata chiamando `factory.create()` sul componente collectionfactory appropriato. Il contenuto della collezione viene posizionato fuori dallo schermo.
3. La schermata successiva scorre fino al centro dell'area visibile e quella attuale scorre verso l'esterno nella direzione opposta. Anche il personaggio del giocatore viene spostato della stessa distanza e alla stessa velocità.
4. La vecchia schermata attuale, ormai fuori dallo schermo, viene eliminata e la schermata successiva diventa la nuova schermata attuale.
5. L'eroe entra nell'area visibile della nuova schermata con un'animazione e il giocatore riprende il controllo.

Tutto questo avviene nell'arco di un secondo, quindi la transizione è fluida e non interrompe l'esperienza di gioco.

## Schermate {#screens}

Ogni schermata del mondo di gioco è costruita all'interno di una collezione separata che contiene la mappa di tile, l'oggetto di collisione e gli altri oggetti di gioco specifici della schermata. Per facilitare la gestione e il caricamento delle schermate, le relative collezioni vengono denominate secondo uno schema semplice:

![](images/rpgmap/screens.png)

Ogni collezione di una schermata prende il nome dalla sua posizione nella griglia del mondo. Il primo numero è la posizione X nella griglia e il secondo è la posizione Y.

Nella vista *Assets*, trova e apri la collezione "/main/screens/0-0.collection", che descrive la schermata nell'angolo in basso a sinistra della mappa:

![](images/rpgmap/screen_collection.png)

Nota che c'è un oggetto di gioco chiamato "root" che è il genitore di tutto il contenuto della schermata. Questa è un'altra convenzione usata nell'esempio e ha uno scopo molto importante: quando una schermata viene portata nell'area visibile, è sufficiente spostare l'oggetto di gioco "root". Tutti gli oggetti figli vengono spostati automaticamente insieme al genitore radice. Se in una schermata ci sono oggetti di gioco particolari, anche questi possono essere animati liberamente, poiché il loro movimento è relativo al genitore radice. Quando la schermata scorre verso l'interno o l'esterno, questi figli si muovono insieme a essa. Serve codice specifico solo se un oggetto deve spostarsi tra schermate diverse.

Le api nella schermata 0-1 sono semplici esempi di questa idea:

![](images/rpgmap/bees.png)

## Modificare le schermate nel contesto del mondo {#editing-screens-in-the-world-context}

Ogni schermata ha la propria mappa di tile, che può essere modificata nell'editor di mappe di tile integrato. Tuttavia, il principale svantaggio di modificare ogni schermata isolatamente è che non è facile vedere come si collega a quelle adiacenti, un aspetto importante per creare continuità nel mondo di gioco.

Per questo motivo è stata creata una collezione apposita. Apri "/main/map/test_layout.collection" per visualizzare questa collezione di test della disposizione del mondo:

![](images/rpgmap/test_layout.png)

L'unico scopo di questa collezione è fungere da strumento di modifica durante lo sviluppo. Modificare una schermata specifica affiancandola alla collezione di test della disposizione ti permette di vedere il contesto della schermata su cui stai lavorando e rende il processo di modifica molto più comodo:

![](images/rpgmap/side_by_side.png)

Qualsiasi modifica alla mappa di tile della schermata (qui nel riquadro di destra) si riflette immediatamente nella collezione di test (nel riquadro di sinistra). Nota inoltre che la collezione di test della disposizione non viene aggiunta alla gerarchia statica, quindi viene esclusa automaticamente da tutte le build.

## Riepilogo {#summary}

Come hai visto, questo esempio è costruito secondo vincoli specifici riguardanti il mondo di gioco e il modo in cui l'eroe lo attraversa. Se il tuo gioco ha requisiti diversi, probabilmente dovrai trovare una soluzione diversa. Per esempio, se il tuo gioco richiede che la telecamera si muova senza interruzioni sulla mappa del mondo, ti serviranno un modo diverso di suddividere i contenuti, un meccanismo di caricamento diverso e anche strumenti diversi che ti aiutino a creare il mondo di gioco.

Questo conclude la presentazione dell'esempio di mappa RPG. Come sempre, puoi usare liberamente il contenuto dell'esempio nel modo che preferisci. Per saperne di più su Defold, consulta le nostre [pagine di documentazione](https://defold.com/learn) per altri esempi, tutorial, manuali e documentazione API.

Se incontri problemi o hai domande, [visita il nostro forum](https://forum.defold.com/).

Buon lavoro con Defold!
