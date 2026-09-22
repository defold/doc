---
title: Defold per gli utenti di Flash
brief: Questa guida presenta Defold come alternativa per gli sviluppatori di giochi Flash. Illustra alcuni dei concetti fondamentali usati nello sviluppo di giochi Flash e spiega gli strumenti e i metodi corrispondenti in Defold.
---

# Defold per gli utenti di Flash {#defold-for-flash-users}

Questa guida presenta Defold come alternativa per gli sviluppatori di giochi Flash. Illustra alcuni dei concetti fondamentali usati nello sviluppo di giochi Flash e spiega gli strumenti e i metodi corrispondenti in Defold.

## Introduzione {#introduction}

Tra i principali vantaggi di Flash c'erano l'accessibilità e la facilità con cui si poteva iniziare a usarlo. I nuovi utenti potevano imparare rapidamente a usare il programma e creare giochi semplici con un investimento di tempo limitato. Defold offre un vantaggio simile grazie a una serie di strumenti dedicati alla progettazione di giochi, consentendo al tempo stesso agli sviluppatori esperti di creare soluzioni avanzate per esigenze più sofisticate (per esempio, permettendo di modificare lo script di rendering predefinito).

I giochi Flash sono programmati in ActionScript (la cui versione più recente è la 3.0), mentre gli script di Defold sono scritti in Lua. Questa guida non propone un confronto dettagliato tra Lua e ActionScript 3.0. Il [manuale di Defold](/manuals/lua) offre una buona introduzione alla programmazione in Lua in Defold e rimanda all'utilissimo [Programming in Lua](https://www.lua.org/pil/) (prima edizione), disponibile gratuitamente online.

Un articolo di Jesse Warden offre un [confronto di base tra ActionScript e Lua](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html), che può essere un buon punto di partenza. Tieni però presente che tra l'architettura di Defold e quella di Flash esistono differenze più profonde di quelle visibili a livello di linguaggio. ActionScript e Flash sono orientati agli oggetti nel senso classico, con classi ed ereditarietà. Defold non ha né classi né ereditarietà. Include il concetto di *oggetto di gioco (game object)*, che può contenere una rappresentazione audiovisiva, un comportamento e dei dati. Le operazioni sugli oggetti di gioco si eseguono con le *funzioni* disponibili nelle API di Defold. Inoltre, Defold incoraggia l'uso di *messaggi* per la comunicazione tra oggetti. I messaggi sono un costrutto di livello superiore rispetto alle chiamate ai metodi e non sono pensati per essere usati come tali. Queste differenze sono rilevanti e richiedono un po' di tempo per abituarsi, ma non verranno trattate in dettaglio in questa guida.

La guida esamina invece alcuni concetti fondamentali dello sviluppo di giochi in Flash e ne illustra gli equivalenti più vicini in Defold. Descrive somiglianze e differenze, insieme agli errori più comuni, per aiutarti a partire con il piede giusto nel passaggio da Flash a Defold.

## Clip filmato e oggetti di gioco {#movie-clips-and-game-objects}

I clip filmato sono un elemento fondamentale dello sviluppo di giochi Flash. Sono simboli, ciascuno con una propria linea temporale. Il concetto equivalente più vicino in Defold è l'oggetto di gioco.

![oggetto di gioco e clip filmato](images/flash/go_movieclip.png)

A differenza dei clip filmato di Flash, gli oggetti di gioco di Defold non hanno linee temporali. Un oggetto di gioco è invece composto da più componenti. Tra i componenti ci sono sprite, suoni e script, oltre a molti altri (per ulteriori dettagli sui componenti disponibili, consulta la [documentazione degli elementi fondamentali](/manuals/building-blocks) e gli articoli correlati). L'oggetto di gioco nella schermata seguente è composto da uno sprite e da uno script. Il componente script serve a controllare il comportamento e l'aspetto degli oggetti di gioco durante l'intero ciclo di vita dell'oggetto:

![componente script](images/flash/script_component.png)

Mentre i clip filmato possono contenere altri clip filmato, gli oggetti di gioco non possono *contenere* altri oggetti di gioco. Tuttavia, gli oggetti di gioco possono essere *collegati come figli* ad altri oggetti di gioco, creando gerarchie che possono essere spostate, scalate o ruotate insieme.

## Flash—creazione manuale di clip filmato {#flashmanually-creating-movie-clips}

In Flash, puoi aggiungere manualmente istanze di clip filmato alla scena trascinandole dalla libreria alla linea temporale. La schermata seguente illustra questa operazione: ogni logo Flash è un'istanza del clip filmato `logo`:

![clip filmato creati manualmente](images/flash/manual_movie_clips.png)

## Defold—creazione manuale di oggetti di gioco {#defoldmanually-creating-game-objects}

Come già accennato, Defold non prevede il concetto di linea temporale. Gli oggetti di gioco sono invece organizzati in collezioni. Le collezioni sono contenitori (o prefab) che racchiudono oggetti di gioco e altre collezioni. Nel caso più semplice, un gioco può essere costituito da una sola collezione. Più spesso, i giochi Defold usano più collezioni, aggiunte manualmente alla collezione di bootstrap `main` oppure caricate dinamicamente tramite [proxy di collezione](/manuals/collection-proxy). Questo concetto di caricamento di "livelli" o "schermate" non ha un equivalente diretto in Flash.

Nell'esempio seguente, la collezione `main` contiene tre istanze (elencate a destra, nella finestra *Outline*) dell'oggetto di gioco `logo` (visibile a sinistra, nella finestra di esplorazione *Assets*):

![oggetti di gioco creati manualmente](images/flash/manual_game_objects.png)

## Flash—riferimenti ai clip filmato creati manualmente {#flashreferencing-manually-created-movie-clips}

Per fare riferimento ai clip filmato creati manualmente in Flash è necessario usare un nome di istanza definito manualmente:

![nome di istanza in Flash](images/flash/flash_instance_name.png)

## Defold—ID dell'oggetto di gioco {#defoldgame-object-id}

In Defold, tutti gli oggetti di gioco e i componenti vengono identificati tramite un indirizzo. Nella maggior parte dei casi è sufficiente un semplice nome o una forma abbreviata. Per esempio:

- `"."` indica l'oggetto di gioco corrente.
- `"#"` indica il componente corrente (lo script).
- `"logo"` indica l'oggetto di gioco con ID `logo`.
- `"#script"` indica il componente con ID `script` nell'oggetto di gioco corrente.
- `"logo#script"` indica il componente con ID `script` nell'oggetto di gioco con ID `logo`.

L'indirizzo degli oggetti di gioco posizionati manualmente è determinato dalla proprietà *Id* assegnata (vedi in basso a destra nella schermata). L'ID deve essere univoco all'interno del file di collezione su cui stai lavorando. L'editor imposta automaticamente un ID, ma puoi modificarlo per ogni istanza di oggetto di gioco che crei.

![ID dell'oggetto di gioco](images/flash/game_object_id.png)

::: sidenote
Puoi trovare l'ID di un oggetto di gioco eseguendo il seguente codice nel suo componente script: `print(go.get_id())`. Questo stamperà nella console l'ID dell'oggetto di gioco corrente.
:::

Il modello di indirizzamento e lo scambio di messaggi sono concetti fondamentali nello sviluppo di giochi con Defold. Il [manuale sull'indirizzamento](/manuals/addressing) e il [manuale sullo scambio di messaggi](/manuals/message-passing) li spiegano in modo approfondito.

## Flash—creazione dinamica di clip filmato {#flashdynamically-creating-movie-clips}

Per creare dinamicamente clip filmato in Flash, devi prima configurare ActionScript Linkage:

![collegamento ActionScript](images/flash/actionscript_linkage.png)

Questa operazione crea una classe (`Logo` in questo caso), di cui puoi poi creare nuove istanze. Puoi aggiungere un'istanza della classe `Logo` allo Stage come segue:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold—creazione di oggetti di gioco tramite fabbriche {#defoldcreating-game-objects-using-factories}

In Defold, la generazione dinamica di oggetti di gioco avviene tramite le *fabbriche* (factory). Le fabbriche sono componenti usati per generare copie di uno specifico oggetto di gioco. In questo esempio è stata creata una fabbrica che usa l'oggetto di gioco `logo` come prototipo:

![Fabbrica del logo](images/flash/logo_factory.png)

Tieni presente che le fabbriche, come tutti i componenti, devono essere aggiunte a un oggetto di gioco prima di poter essere usate. In questo esempio abbiamo creato un oggetto di gioco chiamato `factories` per contenere il componente fabbrica:

![componente fabbrica](images/flash/factory_component.png)

La funzione da chiamare per generare un'istanza dell'oggetto di gioco `logo` è:

```lua
local logo_id = factory.create("factories#logo_factory")
```

L'URL è un parametro obbligatorio di `factory.create()`. Puoi inoltre aggiungere parametri facoltativi per impostare posizione, rotazione, proprietà e scala. Per ulteriori informazioni sul componente fabbrica, consulta il [manuale sulle fabbriche](/manuals/factory). La chiamata a `factory.create()` restituisce l'ID dell'oggetto di gioco creato. Questo ID può essere memorizzato in una tabella (l'equivalente Lua di un array) per farvi riferimento in seguito.

## Flash—Stage

In Flash conosciamo la Timeline (la sezione superiore della schermata seguente) e lo Stage (visibile sotto la Timeline):

![linea temporale e Stage](images/flash/stage.png)

Come descritto nella sezione precedente sui clip filmato, lo Stage è essenzialmente il contenitore di livello più alto di un gioco Flash e viene creato ogni volta che un progetto viene esportato. Per impostazione predefinita, lo Stage ha un solo figlio, *`MainTimeline`*. Ogni clip filmato generato nel progetto ha una propria linea temporale e può fungere da contenitore per altri simboli (compresi i clip filmato).

## Defold—collezioni {#defoldcollections}

L'equivalente dello Stage di Flash in Defold è una collezione. All'avvio, il motore crea un nuovo mondo di gioco sulla base del contenuto di un file di collezione. Per impostazione predefinita questo file si chiama `main.collection`, ma puoi cambiare la collezione caricata all'avvio tramite il file delle impostazioni *game.project*, che si trova nella radice di ogni progetto Defold:

![game.project](images/flash/game_project.png)

Le collezioni sono contenitori usati nell'editor per organizzare oggetti di gioco e altre collezioni. Il contenuto di una collezione può anche essere generato durante l'esecuzione tramite script, usando una [fabbrica di collezioni](/manuals/collection-factory/#spawning-a-collection), che funziona come una normale fabbrica di oggetti di gioco. È utile, per esempio, per generare gruppi di nemici o una disposizione di monete da raccogliere. Nella schermata seguente abbiamo posizionato manualmente due istanze della collezione `logos` nella collezione `main`.

![collezione](images/flash/collection.png)

In alcuni casi vuoi caricare un mondo di gioco completamente nuovo. Il componente [proxy di collezione](/manuals/collection-proxy/) permette di creare un nuovo mondo di gioco sulla base del contenuto di un file di collezione. È utile in situazioni come il caricamento di nuovi livelli di gioco, minigiochi o sequenze narrative.

## Flash—linea temporale {#flashtimeline}

La linea temporale di Flash viene usata principalmente per le animazioni, tramite varie tecniche fotogramma per fotogramma o interpolazioni di forma e di movimento. L'impostazione globale degli FPS (fotogrammi al secondo) del progetto definisce per quanto tempo viene visualizzato un fotogramma. Gli utenti esperti possono modificare gli FPS complessivi del gioco o persino quelli dei singoli clip filmato.

Le interpolazioni di forma consentono di interpolare la grafica vettoriale tra due stati. In genere sono utili solo per forme e applicazioni semplici, come dimostra l'esempio seguente, in cui un quadrato viene trasformato in un triangolo tramite un'interpolazione di forma:

![linea temporale](images/flash/timeline.png)

Le interpolazioni di movimento consentono di animare varie proprietà di un oggetto, tra cui dimensioni, posizione e rotazione. Nell'esempio seguente sono state modificate tutte le proprietà elencate.

![interpolazione di movimento](images/flash/tween.png)

## Defold—animazione delle proprietà {#defoldproperty-animation}

Defold lavora con immagini composte da pixel anziché con grafica vettoriale, quindi non ha un equivalente delle interpolazioni di forma. Le interpolazioni di movimento hanno invece un potente equivalente nell'[animazione delle proprietà](/ref/go/#go.animate). Questa si realizza tramite script, usando la funzione `go.animate()`. La funzione `go.animate()` interpola una proprietà (come colore, scala, rotazione o posizione) dal valore iniziale al valore finale desiderato, usando una delle numerose funzioni di easing disponibili (anche personalizzate). Mentre Flash richiedeva all'utente di implementare le funzioni di easing più avanzate, Defold include [molte funzioni di easing](/manuals/property-animation/#easing) integrate nel motore.

Mentre Flash usa fotogrammi chiave di elementi grafici su una linea temporale per le animazioni, uno dei principali metodi di animazione grafica in Defold è l'animazione flipbook di sequenze di immagini importate. Le animazioni sono organizzate in un componente dell'oggetto di gioco chiamato atlas. In questo caso abbiamo un atlas per un personaggio del gioco con una sequenza di animazione chiamata `run`. Questa è composta da una serie di file PNG:

![animazione flipbook](images/flash/flipbook.png)

## Flash—indice di profondità {#flashdepth-index}

In Flash, la lista di visualizzazione determina cosa viene mostrato e in quale ordine. L'ordinamento degli oggetti in un contenitore (come lo Stage) è gestito da un indice. Gli oggetti aggiunti a un contenitore tramite il metodo `addChild()` occupano automaticamente la posizione più alta dell'indice, che parte da 0 e aumenta con ogni nuovo oggetto. Nella schermata seguente abbiamo generato tre istanze del clip filmato `logo`:

![indice di profondità](images/flash/depth_index.png)

Le posizioni nella lista di visualizzazione sono indicate dai numeri accanto a ciascuna istanza di `logo`. Tralasciando il codice per gestire la posizione x/y dei clip filmato, il risultato mostrato sopra potrebbe essere stato generato così:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

Il fatto che un oggetto venga visualizzato sopra o sotto un altro dipende dalle rispettive posizioni nell'indice della lista di visualizzazione. Per vedere chiaramente questo comportamento, basta scambiare le posizioni di due oggetti nell'indice, per esempio:

```as
swapChildren(logo2,logo3);
```

Il risultato sarebbe il seguente (con la posizione nell'indice aggiornata):

![indice di profondità](images/flash/depth_index_2.png)

## Defold—posizione z {#defoldz-position}

Le posizioni degli oggetti di gioco in Defold sono rappresentate da vettori composti da tre variabili: x, y e z. La posizione z determina la profondità di un oggetto di gioco. Nello [script di rendering](/manuals/render) predefinito, le posizioni z disponibili vanno da -1 a 1.

::: sidenote
Gli oggetti di gioco con una posizione z al di fuori dell'intervallo da -1 a 1 non vengono renderizzati e quindi non sono visibili. È un errore comune per chi inizia a sviluppare con Defold: tienilo presente se un oggetto di gioco non è visibile quando ti aspetti che lo sia.
:::

In Flash l'editor rappresenta l'ordine di profondità in modo implicito (e permette di modificarlo tramite comandi come *Bring Forward* e *Send Backward*); Defold consente invece di impostare la posizione z degli oggetti direttamente nell'editor. Nella schermata seguente puoi vedere che `logo3` viene visualizzato sopra gli altri e ha una posizione z di 0.2. Gli altri oggetti di gioco hanno posizioni z di 0.0 e 0.1.

![ordine z](images/flash/z_order.png)

Tieni presente che la posizione z di un oggetto di gioco annidato in una o più collezioni è determinata dalla sua posizione z insieme a quella di tutti i suoi genitori. Per esempio, immagina che gli oggetti di gioco `logo` mostrati sopra siano stati inseriti in una collezione `logos`, a sua volta inserita in `main` (vedi la schermata seguente). Se la collezione `logos` avesse una posizione z di 0.9, le posizioni z degli oggetti di gioco al suo interno sarebbero 0.9, 1.0 e 1.1. Pertanto, `logo3` non verrebbe renderizzato, perché la sua posizione z sarebbe maggiore di 1.

![ordine z](images/flash/z_order_outline.png)

Naturalmente, la posizione z di un oggetto di gioco può essere modificata tramite script. Supponiamo che il codice seguente si trovi nel componente script di un oggetto di gioco:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Rilevamento delle collisioni in Flash con `hitTestObject` e `hitTestPoint` {#flash-hittestobject-and-hittestpoint-collision-detection}

Il rilevamento di base delle collisioni in Flash si esegue con il metodo `hitTestObject()`. In questo esempio abbiamo due clip filmato: `bullet` e `bullseye`, illustrati nella schermata seguente. Il rettangolo di delimitazione blu è visibile quando selezioni i simboli nell'editor Flash ed è proprio in base a questi rettangoli che viene determinato il risultato del metodo `hitTestObject()`.

![test di collisione](images/flash/hittest.png)

Il rilevamento delle collisioni con `hitTestObject()` si esegue come segue:

```as
bullet.hitTestObject(bullseye);
```

In questo caso, usare i rettangoli di delimitazione non sarebbe appropriato, perché verrebbe registrata una collisione nella situazione seguente:

![test di collisione con rettangoli di delimitazione](images/flash/hitboundingbox.png)

Un'alternativa a `hitTestObject()` è il metodo `hitTestPoint()`. Questo metodo include un parametro `shapeFlag`, che permette di eseguire i test di collisione sui pixel effettivi di un oggetto anziché sul rettangolo di delimitazione. Il rilevamento delle collisioni con `hitTestPoint()` può essere eseguito come segue:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Questa riga verifica la posizione x e y del proiettile (l'angolo superiore sinistro in questo caso) rispetto alla forma del bersaglio. Poiché `hitTestPoint()` verifica un punto rispetto a una forma, scegliere quale punto (o quali punti!) controllare è fondamentale.

## Defold—oggetti di collisione {#defoldcollision-objects}

Defold include un motore fisico in grado di rilevare le collisioni e consentire a uno script di reagire. Il rilevamento delle collisioni in Defold inizia con l'assegnazione di componenti oggetto di collisione agli oggetti di gioco. Nella schermata seguente abbiamo aggiunto un oggetto di collisione all'oggetto di gioco `bullet`. L'oggetto di collisione è rappresentato dal rettangolo rosso trasparente (visibile solo nell'editor):

![oggetto di collisione](images/flash/collision_object.png)

Defold include una versione modificata del motore fisico Box2D, che può simulare automaticamente collisioni realistiche. Questa guida presuppone l'uso di oggetti di collisione cinematici, perché sono quelli più simili al rilevamento delle collisioni in Flash. Per saperne di più sugli oggetti di collisione dinamici, consulta il [manuale sulla fisica](/manuals/physics) di Defold.

L'oggetto di collisione include le seguenti proprietà:

![proprietà dell'oggetto di collisione](images/flash/collision_object_properties.png)

È stata usata una forma rettangolare perché era la più adatta alla grafica del proiettile. L'altra forma usata per le collisioni 2D, la sfera, verrà usata per il bersaglio. Impostare il tipo su Kinematic significa che la risoluzione delle collisioni viene gestita dal tuo script anziché dal motore fisico integrato (per ulteriori informazioni sugli altri tipi, consulta il [manuale sulla fisica](/manuals/physics)). Le proprietà *Group* e *Mask* determinano, rispettivamente, a quale gruppo di collisione appartiene l'oggetto e con quale gruppo di collisione deve essere verificato. La configurazione attuale fa sì che un `bullet` possa collidere solo con un `target`. Immagina di modificare la configurazione come segue:

![gruppo e maschera di collisione](images/flash/collision_groupmask.png)

Ora i proiettili possono collidere con i bersagli e con altri proiettili. Come riferimento, abbiamo configurato per il bersaglio un oggetto di collisione come questo:

![oggetto di collisione del proiettile](images/flash/collision_object_bullet.png)

Osserva come la proprietà *Group* sia impostata su `target` e *Mask* su `bullet`.

In Flash, il rilevamento delle collisioni avviene solo quando viene richiamato esplicitamente dallo script. In Defold, il rilevamento delle collisioni avviene continuamente in background finché un oggetto di collisione rimane abilitato. Quando si verifica una collisione, vengono inviati messaggi a tutti i componenti di un oggetto di gioco (in particolare ai componenti script). Si tratta dei messaggi [`collision_response` e `contact_point_response`](/manuals/physics-messages), che contengono tutte le informazioni necessarie per risolvere la collisione nel modo desiderato.

Il vantaggio del rilevamento delle collisioni di Defold è che è più avanzato di quello di Flash: consente di rilevare collisioni tra forme relativamente complesse con pochissima configurazione. Il rilevamento delle collisioni è automatico, quindi non è necessario scorrere i vari oggetti nei diversi gruppi di collisione ed eseguire esplicitamente i test. Lo svantaggio principale è che non esiste un equivalente di `shapeFlag` di Flash. Tuttavia, per la maggior parte degli usi sono sufficienti combinazioni delle forme di base rettangolo e sfera. Per i casi più complessi, [è possibile usare](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985) forme personalizzate.

## Flash—gestione degli eventi {#flashevent-handling}

Gli oggetti evento e i relativi listener servono a rilevare vari eventi (per esempio clic del mouse, pressioni di pulsanti o caricamento di clip) e ad attivare azioni in risposta. Esistono diversi tipi di eventi con cui lavorare.

## Defold—funzioni di callback e messaggi {#defoldcall-back-functions-and-messaging}

L'equivalente in Defold del sistema di gestione degli eventi di Flash è composto da vari elementi. Innanzitutto, ogni componente script dispone di un insieme di funzioni di callback che rilevano eventi specifici. Queste sono:

init
:   Chiamata quando il componente script viene inizializzato. Equivale alla funzione costruttore in Flash.

final
:   Chiamata quando il componente script viene distrutto (per esempio quando viene rimosso un oggetto di gioco generato).

update
:   Chiamata a ogni fotogramma. Equivale a `enterFrame` in Flash.

on_message
:   Chiamata quando il componente script riceve un messaggio.

on_input
:   Chiamata quando l'input dell'utente (per esempio dal mouse o dalla tastiera) viene inviato a un oggetto di gioco con il [focus dell'input](/ref/go/#acquire_input_focus), che quindi riceve tutti gli input e può reagire.

on_reload
:   Chiamata quando il componente script viene ricaricato.

Le funzioni di callback elencate sopra sono tutte facoltative e possono essere rimosse se non vengono usate. Per dettagli su come configurare l'input, consulta il [manuale sull'input](/manuals/input). Quando si lavora con i proxy di collezione è facile incorrere in un errore comune: consulta [questa sezione](/manuals/input/#input-dispatch-and-on_input) del manuale sull'input per ulteriori informazioni.

Come descritto nella sezione sul rilevamento delle collisioni, gli eventi di collisione vengono gestiti inviando messaggi agli oggetti di gioco coinvolti. I rispettivi componenti script ricevono il messaggio nelle loro funzioni di callback `on_message`.

## Flash—simboli pulsante {#flashbutton-symbols}

Flash usa un tipo di simbolo dedicato ai pulsanti. I pulsanti usano metodi specifici per la gestione degli eventi (per esempio `click` e `buttonDown`) per eseguire azioni quando viene rilevata un'interazione dell'utente. La forma grafica di un pulsante nella sezione "Hit" del simbolo pulsante determina l'area cliccabile del pulsante.

![pulsante](images/flash/button.png)

## Defold—scene GUI e script {#defoldgui-scenes-and-scripts}

Defold non include un componente pulsante nativo e non permette di rilevare facilmente i clic sulla forma di un determinato oggetto di gioco come avviene per i pulsanti in Flash. L'uso di un componente [GUI](/manuals/gui) è la soluzione più comune, anche perché le posizioni dei componenti GUI di Defold non sono influenzate dalla camera di gioco (se usata). L'API GUI contiene inoltre funzioni per rilevare se gli input dell'utente, come clic ed eventi touch, rientrano nei limiti di un elemento GUI.

## Debug {#debugging}

In Flash, il comando `trace()` è un valido aiuto durante il debug. L'equivalente in Defold è `print()` e si usa nello stesso modo di `trace()`:

```lua
print("Hello world!"")
```

Puoi stampare più variabili con un'unica chiamata a `print()`:

```lua
print(score, health, ammo)
```

Esiste anche una funzione `pprint()` (stampa formattata), utile quando lavori con le tabelle. Questa funzione stampa il contenuto delle tabelle, comprese quelle annidate. Considera lo script seguente:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Contiene una tabella (`factions`) annidata in un'altra tabella (`world`). Il normale comando `print()` stamperebbe l'ID univoco della tabella, ma non il suo contenuto effettivo:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

L'uso della funzione `pprint()` come mostrato sopra dà risultati più significativi:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Se il tuo gioco usa il rilevamento delle collisioni, puoi attivare o disattivare il debug della fisica inviando il messaggio seguente:

```lua
msg.post("@system:", "toggle_physics_debug")
```

Il debug della fisica può essere abilitato anche nelle impostazioni del progetto. Prima di attivare il debug della fisica, il nostro progetto avrebbe questo aspetto:

![debug disattivato](images/flash/no_debug.png)

Attivando il debug della fisica vengono visualizzati gli oggetti di collisione aggiunti ai nostri oggetti di gioco:

![debug attivato](images/flash/with_debug.png)

Quando si verificano collisioni, gli oggetti di collisione coinvolti si illuminano. Viene inoltre visualizzato il vettore di collisione:

![collisione](images/flash/collision.png)

Infine, consulta la [documentazione del profilatore](/ref/profiler/) per sapere come monitorare l'uso della CPU e della memoria. Per ulteriori informazioni sulle tecniche di debug avanzate, consulta la [sezione sul debug](/manuals/debugging) del manuale di Defold.

## Come proseguire {#where-to-go-from-here}

- [Esempi di Defold](/examples)
- [Tutorial](/tutorials)
- [Manuali](/manuals)
- [Riferimento API](/ref/go)
- [FAQ](/faq/faq)

Se hai domande o incontri difficoltà, i [forum di Defold](//forum.defold.com) sono un ottimo posto dove chiedere aiuto.
