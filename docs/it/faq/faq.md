---
title: Domande frequenti su Defold engine ed editor
brief: Domande frequenti sul motore di gioco, l'editor e la piattaforma Defold.
---

# Domande frequenti

## Domande generali

#### D: Defold è davvero gratuito?

R: Sì, il motore e l'editor di Defold con funzionalità complete sono completamente gratuiti. Nessun costo nascosto, commissioni o royalties. Solo gratuito.


#### D: Perché la Defold Foundation darebbe Defold gratuitamente?

R: Uno degli obiettivi della [Defold Foundation](/foundation) è garantire che il software Defold sia disponibile per gli sviluppatori in tutto il mondo e che il codice sorgente sia disponibile gratuitamente.


#### D: Per quanto tempo supporterete Defold?

R: Siamo profondamente impegnati in Defold. La [Defold Foundation](/foundation) è stata costituita in modo tale da garantire che esista come proprietario responsabile di Defold per molti anni a venire. Non andrà via.


#### D: Posso fidarmi di Defold per lo sviluppo professionale?

R: Assolutamente. Defold è utilizzato da un numero crescente di sviluppatori di giochi professionisti e studi di sviluppo. Dai un'occhiata alla [vetrina dei giochi](/showcase) per esempi di giochi creati con Defold.


#### D: Che tipo di tracciamento degli utenti state effettuando?

R: Registriamo dati anonimi sull'utilizzo dai nostri siti web e dall'editor Defold per migliorare i nostri servizi e prodotti. Non c'è tracciamento degli utenti nei giochi che crei (a meno che tu non aggiunga un servizio di analisi tu stesso). Leggi di più su questo nella nostra [Politica sulla privacy](/privacy-policy).


#### D: Chi ha creato Defold?

R: Defold è stato creato da Ragnar Svensson e Christian Murray. Hanno iniziato a lavorare sul motore, sull'editor e sui server nel 2009. King e Defold hanno iniziato una partnership nel 2013 e King ha acquisito Defold nel 2014. Leggi la storia completa [qui](/about).


#### D: Posso creare giochi 3D in Defold?

R: Assolutamente! Il motore è un vero e proprio motore 3D. Tuttavia, gli strumenti sono progettati per il 2D, quindi dovrai fare molto lavoro manuale. È previsto un miglior supporto per il 3D.


#### D: Quale linguaggio di programmazione utilizzo in Defold?

R: La logica di gioco nel tuo progetto Defold è scritta principalmente utilizzando il linguaggio Lua (specificamente Lua 5.1/LuaJIT, consulta il [manuale Lua](/manuals/lua) per i dettagli). Lua è un linguaggio dinamico leggero che è veloce e molto potente. Puoi anche utilizzare codice nativo (C/C++, Objective-C, Java e JavaScript a seconda della piattaforma) per estendere il motore Defold con nuove funzionalità. Quando crei materiali personalizzati, viene utilizzato il linguaggio shader OpenGL ES SL per scrivere vertex e fragment shaders.


## Domande sulla piattaforma

#### D: Su quali piattaforme gira Defold?

R: Le seguenti piattaforme sono supportate per l'editor/strumenti e il runtime del motore:

  | Sistema            | Versione           | Architetture   | Supportato           |
  | ------------------ | ------------------ | -------------- | -------------------- |
  | macOS              | 11 Big Sur         | x86-64, arm-64 | Editor e Motore      |
  | Windows            | Vista              | x86-32, x86-64 | Editor e Motore      |
  | Ubuntu (1)         | 18.04              | x86-64         | Editor               |
  | Linux (2)          | Qualsiasi          | x86-64         | Motore               |
  | iOS                | 11.0               | arm-64         | Motore               |
  | Android            | 4.4 (API level 19) | arm-32, arm-64 | Motore               |
  | HTML5              |                    | asm.js, wasm   | Motore               |

  (1 L'editor è costruito e testato per Ubuntu 18.04 a 64 bit. Dovrebbe funzionare anche su altre distribuzioni ma non diamo garanzie.)

  (2 Il runtime del motore dovrebbe funzionare sulla maggior parte delle distribuzioni Linux a 64 bit purché i driver grafici siano aggiornati, vedi sotto per ulteriori informazioni sulle API grafiche)


#### D: Su quali piattaforme posso sviluppare giochi con Defold?

R: Con un solo clic puoi pubblicare su PS4™, Nintendo Switch, iOS, Android e HTML5, oltre che su macOS, Windows e Linux. È davvero una base di codice unica con più piattaforme supportate.


#### D: Su quale API di rendering si basa Defold?

R: Come sviluppatore devi preoccuparti solo di una singola API di rendering utilizzando una [pipeline di rendering completamente scriptabile](/manuals/render/). L'API di script di rendering di Defold traduce le operazioni di rendering nelle seguenti API grafiche:

:[Graphics API](../shared/graphics-api.md)

#### D: C'è un modo per sapere quale versione sto usando?

R: Sì, seleziona l'opzione "Informazioni" nel menu Aiuto. Il popup mostra chiaramente la versione beta di Defold e, più importante, lo specifico SHA1 di rilascio. Per il lookup della versione runtime, usa [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

L'ultima versione beta disponibile per il download da http://d.defold.com/beta può essere verificata aprendo http://d.defold.com/beta/info.json (lo stesso file esiste anche per le versioni stabili: http://d.defold.com/stable/info.json)


#### D: C'è un modo per sapere su quale piattaforma sta girando il gioco a runtime?

R: Sì, consulta [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Domande sull'editor
:[Editor FAQ](../shared/editor-faq.md)


## Domande su Linux
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

#### D: Sto cercando di pubblicare il mio gioco su AppStore. Come dovrei rispondere a IDFA?

R: Quando invii, Apple ha tre caselle di controllo per i loro tre casi d'uso validi per l'IDFA:

  1. Servire annunci all'interno dell'app
  2. Attribuzione dell'installazione dagli annunci
  3. Attribuzione delle azioni dell'utente dagli annunci

  Se selezioni l'opzione 1, il revisore dell'app cercherà annunci da mostrare nell'app. Se il tuo gioco non mostra annunci, il gioco potrebbe essere rifiutato. Defold stesso non utilizza l'ID pubblicitaria.


#### D: Come posso monetizzare il mio gioco?

R: Defold supporta acquisti in-app e varie soluzioni pubblicitarie. Controlla la [categoria Monetizzazione nel portale delle risorse](https://defold.com/tags/stars/monetization/) per un elenco aggiornato delle opzioni di monetizzazione disponibili.


## Errori usando Defold

#### D: Non riesco ad avviare il gioco e non c'è alcun errore di build. Cosa c'è di sbagliato?

R: Il processo di build può non riuscire a ricostruire i file in rari casi in cui ha precedentemente incontrato errori di build che hai risolto. Forza una ricostruzione completa selezionando *Progetto > Ricostruisci e avvia* dal menu.


## Contenuto del gioco

#### D: Defold supporta i prefab?

R: Sì, li supporta. Si chiamano [collections](/manuals/building-blocks/#collections). Ti permettono di creare gerarchie complesse di oggetti di gioco e memorizzarli come blocchi separati che puoi istanziare nell'editor o a runtime (tramite il caricamento di collezioni). Per i nodi GUI c'è supporto per i modelli GUI.


#### D: Non riesco ad aggiungere un oggetto di gioco come figlio di un altro oggetto di gioco, perché?

R: Probabilmente stai cercando di aggiungere un figlio nel file dell'oggetto di gioco e ciò non è possibile. Per capire perché, devi ricordare che le gerarchie genitore-figlio sono strettamente una gerarchia di trasformazione del _scene-graph_. Un oggetto di gioco che non è stato posizionato (o generato) in una scena (collezione) non fa parte di un scene-graph e quindi non può far parte di una gerarchia scene-graph.


#### D: Perché non posso inviare messaggi a tutti i figli di un oggetto di gioco?

R: Le relazioni genitore-figlio non esprimono altro che le relazioni di trasformazione del scene-graph e non devono essere confuse con gli aggregati di orientamento agli oggetti. Se ti concentri sui dati del tuo gioco e su come trasformarli al meglio mentre il tuo gioco cambia stato, troverai probabilmente meno bisogno di inviare messaggi con dati di stato a molti oggetti tutto il tempo. Nei casi in cui avrai bisogno di gerarchie di dati, queste sono facilmente costruite e gestite in Lua.


#### D: Perché sto riscontrando artefatti visivi attorno ai bordi dei miei sprite?

R: Questo è un artefatto visivo chiamato "edge bleeding" in cui i pixel di bordo dei pixel adiacenti in un atlas si mescolano nell'immagine assegnata al tuo sprite. La soluzione è imbottire il bordo delle tue immagini dell'atlas con righe e colonne extra di pixel identici. Fortunatamente questo può essere fatto automaticamente dall'editor di atlas in Defold. Apri il tuo atlas e imposta il valore *Extrude Borders* su 1.


#### D: Posso tingere i miei sprite o renderli trasparenti, o devo scrivere il mio shader per farlo?

R: Lo shader sprite integrato che viene utilizzato per impostazione predefinita per tutti gli sprite ha una costante "tint" definita:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```

#### D: Se imposto la coordinata z di uno sprite a 100, non viene renderizzato. Perché?

R: La posizione Z di un oggetto di gioco controlla l'ordine di rendering. I valori bassi vengono disegnati prima dei valori alti. Nello script di rendering predefinito, gli oggetti di gioco con una profondità compresa tra -1 e 1 vengono disegnati, qualsiasi valore inferiore o superiore non verrà disegnato. Puoi leggere di più sullo script di rendering nella documentazione ufficiale [Render](/manuals/render). Sui nodi GUI il valore Z viene ignorato e non influisce sull'ordine di rendering. Invece, i nodi vengono renderizzati nell'ordine in cui sono elencati e secondo le gerarchie di figli (e i livelli). Leggi di più sul rendering GUI e sull'ottimizzazione delle chiamate di disegno utilizzando i livelli nella documentazione ufficiale [GUI](/manuals/gui).


#### D: Cambiare l'intervallo di proiezione della vista Z a -100 a 100 influirebbe sulle prestazioni?

R: No. L'unico effetto è la precisione. Il buffer Z è logaritmico e ha una risoluzione molto fine dei valori Z vicini a 0 e meno risoluzione lontano da 0. Ad esempio, con un buffer a 24 bit i valori 10.0 e 10.000005 possono essere differenziati mentre 10000 e 10005 no.


#### D: Non c'è coerenza su come sono rappresentati gli angoli, perché?

R: In realtà c'è coerenza. Gli angoli sono espressi in gradi ovunque nell'editor e nelle API di gioco. Le librerie matematiche utilizzano i radianti. Attualmente la convenzione si interrompe per la proprietà fisica `angular_velocity` che è attualmente espressa in radianti/s. Ci si aspetta che cambi.


#### D: Quando creo un nodo di una GUI con solo colore (senza texture), come verrà renderizzato?

R: È semplicemente una forma colorata con vertici. Tieni presente che costerà comunque in termini di fill-rate.


#### D: Se cambio le risorse al volo, il motore le scaricherà automaticamente?

R: Tutte le risorse sono conteggiate internamente. Non appena il conteggio delle referenze è zero, la risorsa viene rilasciata.


#### D: È possibile riprodurre l'audio senza l'uso di un componente audio collegato a un oggetto di gioco?

R: Tutto è basato su componenti. È possibile creare un oggetto di gioco senza testa con più suoni e riprodurre i suoni inviando messaggi all'oggetto controller del suono.


#### D: È possibile cambiare il file audio associato a un componente audio a runtime?

R: In generale tutte le risorse sono dichiarate staticamente con il vantaggio che ottieni la gestione delle risorse gratuitamente. Puoi usare le [proprietà delle risorse](/manuals/script-properties/#resource-properties) per cambiare quale risorsa è assegnata a un componente.


#### D: C'è un modo per accedere alle proprietà delle forme di collisione della fisica?

R: No, attualmente non è possibile.


#### D: C'è un modo rapido per visualizzare gli oggetti di collisione nella mia scena? (come il debugdraw di Box2D)

R: Sì, imposta il flag *physics.debug* in *game.project*. (Consulta la documentazione ufficiale [Project settings](/manuals/project-settings/#debug))


#### D: Quali sono i costi in termini di prestazioni per avere molti contatti/collisioni?

R: Defold esegue una versione modificata di Box2D in background e il costo delle prestazioni dovrebbe essere abbastanza simile. Puoi sempre vedere quanto tempo il motore trascorre sulla fisica aprendo il [profilatore](/manuals/debugging). Dovresti anche considerare quale tipo di oggetti di collisione utilizzi. Gli oggetti statici sono più economici in termini di prestazioni, ad esempio. Consulta la documentazione ufficiale [Physics](/manuals/physics) in Defold per ulteriori dettagli.


#### D: Qual è l'impatto sulle prestazioni di avere molti componenti di effetti particellari?

R: Dipende se stanno suonando o meno. Un ParticleFx che non sta suonando non ha alcun costo in termini di prestazioni. L'impatto sulle prestazioni di un ParticleFx in riproduzione deve essere valutato utilizzando il profilatore poiché il suo impatto dipende da come è configurato. Come per la maggior parte delle altre cose, la memoria è allocata in anticipo per il numero di ParticleFx definito come max_count in *game.project*.


#### D: Come ricevo input su un oggetto di gioco all'interno di una collezione caricata tramite un proxy di collezione?

R: Ogni collezione caricata tramite proxy ha il proprio stack di input. L'input viene instradato dallo stack di input della collezione principale tramite il componente proxy agli oggetti nella collezione. Ciò significa che non basta che l'oggetto di gioco nella collezione caricata acquisisca il focus dell'input, l'oggetto di gioco che _detiene_ il componente proxy deve acquisire anche il focus dell'input. Consulta la documentazione [Input](/manuals/input) per i dettagli.


#### D: Posso utilizzare proprietà di tipo stringa negli script?

R: No. Defold supporta proprietà di tipo [hash](/ref/builtins#hash). Queste possono essere utilizzate per indicare tipi, identificatori di stato o chiavi di qualsiasi tipo. Gli hash possono anche essere utilizzati per memorizzare ID degli oggetti di gioco (percorsi) sebbene le proprietà [url](/ref/msg#msg.url) siano spesso preferibili poiché l'editor popola automaticamente un menu a discesa con gli URL rilevanti per te. Consulta la documentazione [Script properties](/manuals/script-properties) per i dettagli.


#### D: Come accedo alle singole celle di una matrice (creata usando [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) o simile)?

R: Accedi alle celle usando `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` ecc


#### D: Sto ricevendo `Not enough resources to clone the node` quando uso [gui.clone()](/ref/gui/#gui.clone:node) o [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

R: Aumenta il valore `Max Nodes` del componente GUI. Trovi questo valore nel pannello Proprietà quando selezioni la radice del componente nel Riepilogo.


## Il forum

#### D: Posso pubblicare un thread dove pubblicizzo il mio lavoro?

R: Certamente! Abbiamo una categoria speciale ["Work for hire"](https://forum.defold.com/c/work-for-hire) per questo. Incoraggeremo sempre tutto ciò che beneficia la comunità, e offrire i tuoi servizi alla comunità---a pagamento o meno---è un buon esempio di ciò.


#### D: Ho creato un thread e aggiunto il mio lavoro: posso aggiungerne di più?

R: Per ridurre il bumping dei thread "Work for hire", non puoi pubblicare più di una volta ogni 14 giorni nel tuo thread (a meno che non sia una risposta diretta a un commento nel thread, nel qual caso puoi rispondere). Se vuoi aggiungere ulteriori lavori al tuo thread entro il periodo di 14 giorni, devi modificare i tuoi post esistenti con il contenuto aggiunto.


#### D: Posso utilizzare la categoria Work for Hire per pubblicare offerte di lavoro?

R: Certo, sentiti libero! Può essere utilizzata sia per offerte che per richieste, ad esempio "Programmatore cerca artista pixel 2D; sono ricco e ti pagherò bene".
