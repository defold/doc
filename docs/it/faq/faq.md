---
title: Domande frequenti sul motore e sull'editor Defold
brief: Domande frequenti sul motore di gioco, l'editor e la piattaforma Defold.
---

# Domande frequenti

## Domande generali

#### D: Defold è davvero gratuito?

R: Sì, il motore e l'editor Defold con tutte le loro funzionalità sono completamente gratuiti. Nessun costo nascosto, commissione o royalty. Tutto qui.


#### D: Perché la Defold Foundation darebbe Defold gratuitamente?

R: Uno degli obiettivi della [Defold Foundation](/foundation) è garantire che il software Defold sia disponibile per gli sviluppatori in tutto il mondo e che il codice sorgente sia disponibile gratuitamente.


#### D: Per quanto tempo supporterete Defold?

R: Siamo profondamente impegnati in Defold. La [Defold Foundation](/foundation) è stata costituita in modo da garantire che continui a essere la proprietaria responsabile di Defold per molti anni a venire. Non scomparirà.


#### D: Posso fidarmi di Defold per lo sviluppo professionale?

R: Assolutamente. Defold è utilizzato da un numero crescente di sviluppatori di giochi professionisti e studi di sviluppo. Dai un'occhiata alla [vetrina dei giochi](/showcase) per esempi di giochi creati con Defold.


#### D: Che tipo di tracciamento degli utenti state effettuando?

R: Registriamo dati anonimi sull'utilizzo dei nostri siti web e dell'editor Defold per migliorare i nostri servizi e prodotti. Non c'è tracciamento degli utenti nei giochi che crei (a meno che non sia tu ad aggiungere un servizio di analisi). Leggi di più su questo nella nostra [Politica sulla privacy](/privacy-policy).


#### D: Chi ha creato Defold?

R: Defold è stato creato da Ragnar Svensson e Christian Murray. Hanno iniziato a lavorare sul motore, sull'editor e sui server nel 2009. King e Defold hanno avviato una collaborazione nel 2013 e King ha acquisito Defold nel 2014. Leggi la storia completa [qui](/about).


#### D: Posso creare giochi 3D in Defold?

R: Assolutamente! Il motore è un vero e proprio motore 3D. Tuttavia, gli strumenti sono progettati per il 2D, quindi dovrai fare molto lavoro manuale. È previsto un miglior supporto per il 3D.


#### D: Quale linguaggio di programmazione utilizzo in Defold?

R: La logica di gioco nel tuo progetto Defold è scritta principalmente in Lua (nello specifico Lua 5.1/LuaJIT; consulta il [manuale di Lua](/manuals/lua) per i dettagli). Lua è un linguaggio dinamico leggero, veloce e molto potente. Puoi anche utilizzare codice nativo (C/C++, Objective-C, Java e JavaScript, a seconda della piattaforma) per estendere il motore Defold con nuove funzionalità. Quando crei materiali personalizzati, il linguaggio di shading OpenGL ES SL viene utilizzato per scrivere vertex shader e fragment shader.


## Domande sulla piattaforma

#### D: Su quali piattaforme gira Defold?

R: Le seguenti piattaforme sono supportate per l'editor/strumenti e il runtime del motore:

  | Sistema            | Versione           | Architetture       | Supportato         |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | editor e motore    |
  | Windows            | Vista              | `x86-32`, `x86-64` | editor e motore    |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | editor             |
  | Linux (2)          | Qualsiasi          | `x86-64`, `arm-64` | motore             |
  | iOS                | 15.0               | `arm-64`, `x86_64` | motore             |
  | Android            | 5.0 (API level 21) | `arm-32`, `arm-64` | motore             |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | motore       |

  (1) L'editor è compilato e testato per Ubuntu 18.04 a 64 bit. Dovrebbe funzionare anche su altre distribuzioni, ma non diamo garanzie.

  (2) Il runtime del motore dovrebbe funzionare sulla maggior parte delle distribuzioni Linux a 64 bit, purché i driver grafici siano aggiornati. Vedi sotto per ulteriori informazioni sulle API grafiche.


#### D: Su quali piattaforme posso sviluppare giochi con Defold?

R: Con un solo clic puoi pubblicare su PS4™, Nintendo Switch, iOS, Android e HTML5, oltre che su macOS, Windows e Linux. È davvero una base di codice unica con più piattaforme supportate.


#### D: Su quale API di rendering si basa Defold?

R: Come sviluppatore, devi occuparti soltanto di un'unica API di rendering, esposta tramite una [pipeline di rendering completamente scriptabile](/manuals/render/). L'API di script di rendering di Defold traduce le operazioni di rendering nelle seguenti API grafiche:

:[Graphics API](../shared/graphics-api.md)

#### D: C'è un modo per sapere quale versione sto usando?

R: Sì, seleziona <kbd>Help ▸ About</kbd>. La finestra mostra chiaramente la versione beta di Defold e, soprattutto, lo SHA1 esatto della release. Per verificare la versione del runtime, usa [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

L'ultima versione beta disponibile per il download da http://d.defold.com/beta può essere verificata aprendo http://d.defold.com/beta/info.json (lo stesso file esiste anche per le versioni stabili: http://d.defold.com/stable/info.json)


#### D: C'è un modo per sapere su quale piattaforma sta girando il gioco a runtime?

R: Sì, consulta [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Domande sull'editor
:[Editor FAQ](../shared/editor-faq.md)


## Domande su Linux {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Domande su Android
:[Android FAQ](../shared/android-faq.md)


## Domande su HTML5
:[HTML5 FAQ](../shared/html5-faq.md)


## Domande su iOS
:[iOS FAQ](../shared/ios-faq.md)


## Domande su Windows
:[Windows FAQ](../shared/windows-faq.md)


## Domande su Console
:[Consoles FAQ](../shared/consoles-faq.md)


## Pubblicazione di giochi

#### D: Sto cercando di pubblicare il mio gioco sull'App Store. Come dovrei rispondere alla domanda sull'IDFA?

R: Quando invii il gioco, Apple presenta tre caselle di controllo per i casi d'uso validi dell'IDFA:

  1. Servire annunci all'interno dell'app
  2. Attribuzione dell'installazione dagli annunci
  3. Attribuzione delle azioni dell'utente dagli annunci

  Se selezioni l'opzione 1, il revisore dell'app cercherà annunci da mostrare nell'app. Se il tuo gioco non mostra annunci, potrebbe essere rifiutato. Defold stesso non utilizza l'identificatore pubblicitario.


#### D: Come posso monetizzare il mio gioco?

R: Defold supporta acquisti in-app e varie soluzioni pubblicitarie. Controlla la [categoria Monetizzazione nell'Asset Portal](https://defold.com/tags/stars/monetization/) per un elenco aggiornato delle opzioni di monetizzazione disponibili.


## Errori usando Defold

#### D: Non riesco ad avviare il gioco e non c'è alcun errore di build. Cosa c'è di sbagliato?

R: In rari casi, il processo di build può non ricostruire i file dopo aver rilevato errori di build che hai già risolto. Forza una ricostruzione completa selezionando <kbd>Project ▸ Rebuild And Launch</kbd> dal menu.


## Contenuto del gioco

#### D: Defold supporta i prefab?

R: Sì, li supporta. Si chiamano [collezioni (collections)](/manuals/building-blocks/#collections). Ti permettono di creare gerarchie complesse di oggetti di gioco e memorizzarle come blocchi separati che puoi istanziare nell'editor o a runtime (tramite il caricamento di collezioni). Per i nodi GUI sono disponibili i modelli GUI.


#### D: Non riesco ad aggiungere un oggetto di gioco come figlio di un altro oggetto di gioco, perché?

R: Probabilmente stai cercando di aggiungere un figlio nel file dell'oggetto di gioco, ma ciò non è possibile. Per capire perché, devi ricordare che le gerarchie genitore-figlio costituiscono esclusivamente una gerarchia di trasformazioni del _grafo della scena_ (scene graph). Un oggetto di gioco che non è stato posizionato (o generato) in una scena (collezione) non fa parte di un grafo della scena e quindi non può far parte di una simile gerarchia.


#### D: Perché non posso inviare messaggi a tutti i figli di un oggetto di gioco?

R: Le relazioni genitore-figlio esprimono soltanto le relazioni di trasformazione del grafo della scena e non devono essere confuse con le aggregazioni orientate agli oggetti. Se ti concentri sui dati del tuo gioco e sul modo migliore di trasformarli mentre il gioco cambia stato, probabilmente avrai meno bisogno di inviare continuamente messaggi con dati di stato a molti oggetti. Quando servono, le gerarchie di dati possono essere costruite e gestite facilmente in Lua.


#### D: Perché sto riscontrando artefatti visivi attorno ai bordi dei miei sprite?

R: Si tratta di un artefatto visivo chiamato "edge bleeding", nel quale i pixel ai bordi delle immagini adiacenti in un atlas contaminano l'immagine assegnata allo sprite. La soluzione consiste nell'aggiungere ai bordi delle immagini dell'atlas righe e colonne extra di pixel identici. Fortunatamente, l'editor degli atlas di Defold può farlo automaticamente. Apri l'atlas e imposta <kbd>Extrude Borders</kbd> su 1.


#### D: Posso tingere i miei sprite o renderli trasparenti, o devo scrivere il mio shader per farlo?

R: Lo shader integrato utilizzato per impostazione predefinita da tutti gli sprite definisce una costante `tint`:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```

#### D: Se imposto la coordinata z di uno sprite a 100, non viene renderizzato. Perché?

R: La posizione Z di un oggetto di gioco controlla l'ordine di rendering. I valori bassi vengono disegnati prima dei valori alti. Nello script di rendering predefinito vengono disegnati gli oggetti di gioco con una profondità compresa tra -1 e 1; qualsiasi valore inferiore o superiore non viene disegnato. Puoi trovare maggiori informazioni sullo script di rendering nella documentazione ufficiale sul [rendering](/manuals/render). Nei nodi GUI il valore Z viene ignorato e non influisce sull'ordine di rendering. I nodi vengono invece renderizzati nell'ordine in cui sono elencati e in base alle gerarchie dei figli (e ai livelli). La documentazione ufficiale sulla [GUI](/manuals/gui) descrive il rendering della GUI e l'ottimizzazione delle chiamate di disegno tramite i livelli.


#### D: Cambiare l'intervallo di proiezione della vista Z a -100 a 100 influirebbe sulle prestazioni?

R: No. L'unico effetto è la precisione. Il buffer Z è logaritmico e ha una risoluzione molto fine dei valori Z vicini a 0 e meno risoluzione lontano da 0. Ad esempio, con un buffer a 24 bit i valori 10.0 e 10.000005 possono essere differenziati mentre 10000 e 10005 no.


#### D: Non c'è coerenza su come sono rappresentati gli angoli, perché?

R: In realtà c'è coerenza. Gli angoli sono espressi in gradi ovunque nell'editor e nelle API di gioco, mentre le librerie matematiche utilizzano i radianti. L'unica eccezione attuale è la proprietà fisica `angular_velocity`, espressa in radianti/s; si prevede che cambierà.


#### D: Quando creo un nodo di una GUI con solo colore (senza texture), come verrà renderizzato?

R: È semplicemente una forma colorata con vertici. Tieni presente che costerà comunque in termini di fill-rate.


#### D: Se cambio le risorse al volo, il motore le scaricherà automaticamente?

R: Tutte le risorse hanno un conteggio dei riferimenti interno. Non appena il conteggio dei riferimenti raggiunge zero, la risorsa viene rilasciata.


#### D: È possibile riprodurre l'audio senza l'uso di un componente audio collegato a un oggetto di gioco?

R: Tutto è basato su componenti. È possibile creare un oggetto di gioco privo di rappresentazione visiva con più suoni e riprodurli inviando messaggi all'oggetto che li controlla.


#### D: È possibile cambiare il file audio associato a un componente audio a runtime?

R: In generale, tutte le risorse sono dichiarate staticamente, quindi il motore può gestirle automaticamente. Puoi usare le [proprietà delle risorse](/manuals/script-properties/#resource-properties) per cambiare la risorsa assegnata a un componente.


#### D: C'è un modo per accedere alle proprietà delle forme di collisione della fisica?

R: No, attualmente non è possibile.


#### D: C'è un modo rapido per visualizzare gli oggetti di collisione nella mia scena? (come il debugdraw di Box2D)

R: Sì, imposta il flag `physics.debug` in `game.project`. Consulta la documentazione ufficiale sulle [impostazioni del progetto](/manuals/project-settings/#debug).


#### D: Quali sono i costi in termini di prestazioni per avere molti contatti/collisioni?

R: Defold esegue internamente una versione modificata di Box2D e il costo in termini di prestazioni dovrebbe essere abbastanza simile. Puoi sempre vedere quanto tempo il motore dedica alla fisica aprendo il [profilatore](/manuals/debugging). Dovresti anche considerare quale tipo di oggetti di collisione utilizzi: gli oggetti statici, ad esempio, sono meno costosi. Per ulteriori dettagli, consulta la documentazione ufficiale sulla [fisica](/manuals/physics) in Defold.


#### D: Qual è l'impatto sulle prestazioni di avere molti componenti di effetti particellari?

R: Dipende dal fatto che siano in riproduzione o meno. Un ParticleFx non in riproduzione non ha alcun costo in termini di prestazioni. L'impatto di un ParticleFx in riproduzione deve essere valutato con il profilatore, poiché dipende dalla sua configurazione. Come per la maggior parte delle altre risorse, la memoria viene allocata in anticipo per il numero di ParticleFx definito da `max_count` in `game.project`.


#### D: Come ricevo input su un oggetto di gioco all'interno di una collezione caricata tramite un proxy di collezione?

R: Ogni collezione caricata tramite proxy ha il proprio stack di input. L'input viene instradato dallo stack di input della collezione principale, attraverso il componente proxy, agli oggetti della collezione. Ciò significa che non basta che l'oggetto di gioco nella collezione caricata acquisisca il focus dell'input: anche l'oggetto di gioco che _contiene_ il componente proxy deve acquisirlo. Consulta la documentazione sull'[input](/manuals/input) per i dettagli.


#### D: Posso utilizzare proprietà di tipo stringa negli script?

R: No. Defold supporta proprietà di tipo [hash](/ref/builtins#hash). Queste possono essere utilizzate per indicare tipi, identificatori di stato o chiavi di qualsiasi tipo. Gli hash possono anche essere utilizzati per memorizzare gli ID degli oggetti di gioco (percorsi), sebbene le proprietà [URL](/ref/msg#msg.url) siano spesso preferibili perché l'editor popola automaticamente un menu a discesa con gli URL pertinenti. Consulta la documentazione sulle [proprietà degli script](/manuals/script-properties) per i dettagli.


#### D: Come accedo alle singole celle di una matrice (creata usando [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) o simile)?

R: Accedi alle celle usando `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` ecc.


#### D: Sto ricevendo `Not enough resources to clone the node` quando uso [gui.clone()](/ref/gui/#gui.clone:node) o [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

R: Aumenta il valore `Max Nodes` del componente GUI. Trovi questo valore nel pannello <kbd>Properties</kbd> quando selezioni la radice del componente in <kbd>Outline</kbd>.


## Il forum

#### D: Posso pubblicare un thread in cui pubblicizzo il mio lavoro?

R: Certamente! Abbiamo una categoria speciale, ["Work for hire"](https://forum.defold.com/c/work-for-hire), per questo. Incoraggeremo sempre tutto ciò che giova alla comunità, e offrire i tuoi servizi alla comunità — a pagamento o meno — ne è un buon esempio.


#### D: Ho creato un thread e aggiunto il mio lavoro: posso aggiungerne di più?

R: Per ridurre i continui rilanci dei thread "Work for hire", non puoi pubblicare più di una volta ogni 14 giorni nel tuo thread (a meno che non sia una risposta diretta a un commento nel thread, nel qual caso puoi rispondere). Se vuoi aggiungere ulteriori lavori al tuo thread entro il periodo di 14 giorni, devi modificare i post esistenti e aggiungervi il nuovo contenuto.


#### D: Posso utilizzare la categoria "Work for hire" per pubblicare offerte di lavoro?

R: Certo, sentiti libero! Può essere utilizzata sia per offerte che per richieste, ad esempio "Programmatore cerca artista pixel 2D; sono ricco e ti pagherò bene".
