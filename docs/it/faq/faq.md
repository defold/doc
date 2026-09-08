---
title: Domande frequenti sul motore e sull'editor Defold
brief: Domande frequenti sul motore di gioco, sull'editor e sulla piattaforma Defold.
---

# Domande frequenti {#frequently-asked-questions}

## Domande generali {#general-questions}

#### D: Defold è davvero gratuito? {#q-is-defold-really-free}

R: Sì, il motore e l'editor Defold, con tutte le loro funzionalità, sono completamente gratuiti. Nessun costo nascosto, commissione o royalty. Semplicemente gratuiti.


#### D: Perché mai la Defold Foundation dovrebbe distribuire Defold gratuitamente? {#q-why-on-earth-would-the-defold-foundation-give-defold-away}

R: Uno degli obiettivi della [Defold Foundation](/foundation) è garantire che il software Defold sia disponibile per gli sviluppatori di tutto il mondo e che il codice sorgente sia disponibile gratuitamente.


#### D: Per quanto tempo supporterete Defold? {#q-how-long-will-you-support-defold}

R: Crediamo fermamente in Defold. La [Defold Foundation](/foundation) è stata costituita in modo da garantire che continui a essere la proprietaria responsabile di Defold per molti anni a venire. Non scomparirà.


#### D: Posso fidarmi di Defold per lo sviluppo professionale? {#q-can-i-trust-defold-for-professional-development}

R: Assolutamente. Defold è utilizzato da un numero crescente di sviluppatori di giochi professionisti e studi di sviluppo. Consulta la [vetrina dei giochi](/showcase) per esempi di giochi creati con Defold.


#### D: Che tipo di tracciamento degli utenti effettuate? {#q-what-kind-of-user-tracking-are-you-doing}

R: Registriamo dati anonimi sull'utilizzo dei nostri siti web e dell'editor Defold per migliorare i nostri servizi e il prodotto. Non c'è tracciamento degli utenti nei giochi che crei (a meno che non sia tu ad aggiungere un servizio di analisi). Per saperne di più, consulta la nostra [politica sulla privacy](/privacy-policy).


#### D: Chi ha creato Defold? {#q-who-made-defold}

R: Defold è stato creato da Ragnar Svensson e Christian Murray. Hanno iniziato a lavorare sul motore, sull'editor e sui server nel 2009. King e Defold hanno avviato una collaborazione nel 2013 e King ha acquisito Defold nel 2014. Leggi la storia completa [qui](/about).


## Domande sullo sviluppo di giochi {#game-development-questions}

#### D: Posso creare giochi 3D in Defold? {#q-can-i-do-3d-games-in-defold}

R: Assolutamente! Il motore è un vero e proprio motore 3D. Tuttavia, gli strumenti sono progettati per il 2D, quindi dovrai occuparti personalmente di gran parte del lavoro. È previsto un supporto migliore per il 3D.


## Domande sui linguaggi di programmazione {#programming-language-questions}

#### D: Quale linguaggio di programmazione utilizzo in Defold? {#q-what-programming-language-do-i-work-with-in-defold}

R: La logica di gioco nel tuo progetto Defold è scritta principalmente in Lua (nello specifico Lua 5.1/LuaJIT; consulta il [manuale di Lua](/manuals/lua) per i dettagli). Lua è un linguaggio dinamico leggero, veloce e molto potente. Defold supporta i transpilatori che generano codice Lua. Installando un'estensione per il transpilatore, puoi usare linguaggi alternativi — come [Teal](https://github.com/defold/extension-teal) — per scrivere Lua con controlli statici. Puoi anche utilizzare codice nativo (C/C++, Objective-C, Java e JavaScript, a seconda della piattaforma) per [estendere il motore Defold con nuove funzionalità](/manuals/extensions/). Quando crei [materiali personalizzati](/manuals/material/), usi il linguaggio per shader OpenGL ES SL per scrivere vertex shader e fragment shader.


#### D: Posso usare C++ per scrivere la logica di gioco? {#q-can-i-use-c-to-write-game-logic}

R: Il supporto per C++ in Defold serve principalmente a scrivere estensioni native che si interfacciano con SDK di terze parti o API specifiche della piattaforma. Il [dmSDK](https://defold.com/ref/stable/dmGameObject/) (l'API C++ di Defold utilizzata nelle estensioni native) verrà gradualmente ampliato con nuove funzionalità, in modo da consentire agli sviluppatori che lo desiderano di scrivere tutta la logica di gioco in C++. Lua rimarrà il linguaggio principale per la logica di gioco, ma con l'ampliamento dell'API C++ sarà possibile scriverla anche in C++. Il lavoro di ampliamento dell'API C++ consiste principalmente nello spostare i file header privati esistenti nella sezione pubblica e nel sistemare le API per l'uso pubblico.


#### D: Posso usare TypeScript con Defold? {#q-can-i-use-typescript-with-defold}

R: TypeScript non è supportato ufficialmente. La comunità mantiene un insieme di strumenti, [ts-defold](https://ts-defold.dev/), per scrivere TypeScript e transpilarlo in Lua direttamente da VSCode.


#### D: Posso usare Haxe con Defold? {#q-can-i-use-haxe-with-defold}

R: Haxe non è supportato ufficialmente. La comunità mantiene [hxdefold](https://github.com/hxdefold/hxdefold) per scrivere Haxe e transpilarlo in Lua.


#### D: Posso usare C# con Defold? {#q-can-i-use-c-with-defold}

R: La Defold Foundation ha aggiunto il supporto per C# e lo ha reso disponibile come dipendenza di libreria. C# è un linguaggio di programmazione molto diffuso e aiuterà gli studi e gli sviluppatori che hanno investito molto in C# a passare a Defold.


#### D: Temo che l'aggiunta del supporto per C# avrà un impatto negativo su Defold. Devo preoccuparmi? {#q-i-am-concerned-that-adding-c-support-will-have-a-negative-impact-on-defold-should-i-be-worried}

R: Defold NON sta abbandonando Lua come linguaggio di scripting principale. Il supporto per C# viene aggiunto come nuovo linguaggio per le estensioni. Non avrà alcun impatto sul motore, a meno che tu non scelga di usare estensioni C# nel tuo progetto.

Il supporto per C# comporterà dei costi (dimensioni dell'eseguibile, prestazioni a runtime e così via), ma spetta al singolo sviluppatore o studio valutarli.

Per quanto riguarda C# in sé, si tratta di una modifica relativamente contenuta, poiché il sistema di estensioni supporta già molti linguaggi (C/C++/Java/Objective-C/Zig). Gli SDK verranno mantenuti sincronizzati generando i binding C#. In questo modo i binding resteranno aggiornati con uno sforzo minimo.

La Defold Foundation in passato era contraria all'aggiunta del supporto per C# in Defold, ma ha cambiato opinione per diversi motivi:

* Studi e sviluppatori continuano a richiedere il supporto per C#.
* Il supporto per C# è stato limitato alle sole estensioni (richiedendo quindi uno sforzo ridotto).
* Il nucleo del motore non subirà alcun impatto.
* Le API C# possono essere mantenute sincronizzate con uno sforzo minimo se vengono generate.
* Il supporto per C# si baserà su DotNet 9 con NativeAOT, generando quindi librerie statiche a cui la pipeline di build esistente può collegarsi (come per qualsiasi altra estensione Defold).


## Domande sulla piattaforma {#platform-questions}

#### D: Su quali piattaforme funziona Defold? {#q-what-platforms-does-defold-run-on}

R: Le seguenti piattaforme sono supportate per l'editor e gli strumenti e per il runtime del motore:

  | Sistema            | Versione           | Architetture       | Supporto           |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Editor e motore    |
  | Windows            | Vista              | `x86-32`, `x86-64` | Editor e motore    |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Editor             |
  | Linux (2)          | Qualsiasi          | `x86-64`, `arm-64` | Motore             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Motore             |
  | Android            | 5.0 (livello API 21) | `arm-32`, `arm-64` | Motore             |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | Motore       |

  (1 L'editor è compilato e testato per Ubuntu a 64 bit. Dovrebbe funzionare anche su altre distribuzioni, ma non diamo garanzie.)

  (2 Il runtime del motore dovrebbe funzionare sulla maggior parte delle distribuzioni Linux a 64 bit, purché i driver grafici siano aggiornati; vedi sotto per ulteriori informazioni sulle API grafiche)


#### D: Per quali piattaforme di destinazione posso sviluppare giochi con Defold? {#q-what-target-platforms-can-i-develop-games-for-with-defold}

R: Con un solo clic puoi pubblicare su PS4™, PS5™, Nintendo Switch, iOS (64 bit), Android (32 bit e 64 bit) e HTML5, oltre che su macOS (x86-64 e arm64), Windows (32 bit e 64 bit) e Linux (x86-64 e arm64). È davvero un'unica base di codice con più piattaforme supportate.


#### D: Su quale API di rendering si basa Defold? {#q-what-rendering-api-does-defold-rely-on}

R: Come sviluppatore, devi occuparti soltanto di un'unica API di rendering, che utilizza una [pipeline di rendering completamente scriptabile](/manuals/render/). L'API degli script di rendering di Defold traduce le operazioni di rendering nelle seguenti API grafiche:

:[Graphics API](../shared/graphics-api.md)

#### D: C'è un modo per sapere quale versione sto usando? {#q-is-there-a-way-to-know-what-version-im-running}

R: Sì, seleziona l'opzione "About" nel menu Help. La finestra mostra chiaramente la versione beta di Defold e, soprattutto, lo SHA1 specifico della release. Per verificare la versione a runtime, usa [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

Puoi verificare l'ultima versione beta disponibile per il download da [http://d.defold.com/beta](http://d.defold.com/beta) aprendo [http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json) (lo stesso file esiste anche per le versioni stabili: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)).


#### D: C'è un modo per sapere su quale piattaforma è in esecuzione il gioco a runtime? {#q-is-there-a-way-to-know-what-platform-the-game-is-running-on-at-runtime}

R: Sì, consulta [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Domande sull'editor {#editor-questions}
:[Editor FAQ](../shared/editor-faq.md)


## Domande su Linux {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Domande su Android {#android-questions}
:[Android FAQ](../shared/android-faq.md)


## Domande su HTML5 {#html5-questions}
:[HTML5 FAQ](../shared/html5-faq.md)


## Domande su iOS {#ios-questions}
:[iOS FAQ](../shared/ios-faq.md)


## Domande su Windows {#windows-questions}
:[Windows FAQ](../shared/windows-faq.md)


## Domande sulle console {#console-questions}
:[Consoles FAQ](../shared/consoles-faq.md)


## Pubblicazione di giochi {#publishing-games}

#### D: Sto cercando di pubblicare il mio gioco sull'App Store. Come dovrei rispondere alla domanda sull'IDFA? {#q-im-trying-to-publish-my-game-to-appstore-how-should-i-respond-to-idfa}

R: Durante l'invio, Apple presenta tre caselle di controllo per i tre casi d'uso validi dell'IDFA:

  1. Mostrare annunci pubblicitari all'interno dell'app
  2. Attribuire le installazioni agli annunci pubblicitari
  3. Attribuire le azioni degli utenti agli annunci pubblicitari

  Se selezioni l'opzione 1, il revisore dell'app verificherà che compaiano annunci nell'app. Se il tuo gioco non mostra annunci, potrebbe essere rifiutato. Defold stesso non utilizza l'identificatore pubblicitario.


#### D: Come posso monetizzare il mio gioco? {#q-how-do-i-monetize-my-game}

R: Defold supporta gli acquisti in-app e varie soluzioni pubblicitarie. Consulta la [categoria dedicata alla monetizzazione nell'Asset Portal](https://defold.com/tags/stars/monetization/) per un elenco aggiornato delle opzioni di monetizzazione disponibili.


## Errori nell'uso di Defold {#errors-using-defold}

#### D: Non riesco ad avviare il gioco e non c'è alcun errore di build. Cosa c'è che non va? {#q-i-cant-start-the-game-and-there-is-no-build-error-whats-wrong}

R: In rari casi, il processo di build può non ricostruire i file dopo aver rilevato errori di build che hai già risolto. Forza una ricostruzione completa selezionando *Project > Rebuild And Launch* dal menu.



## Contenuto del gioco {#game-content}

#### D: Defold supporta i prefab? {#q-does-defold-support-prefabs}

R: Sì, li supporta. Si chiamano [collezioni (collection)](/manuals/building-blocks/#collections). Ti permettono di creare gerarchie complesse di oggetti di gioco (game object) e salvarle come blocchi separati che puoi istanziare nell'editor o a runtime (tramite la generazione di collezioni). Per i nodi GUI sono disponibili i modelli GUI.


#### D: Non riesco ad aggiungere un oggetto di gioco come figlio di un altro oggetto di gioco, perché? {#q-i-cant-add-a-game-object-as-a-child-to-another-game-object-why}

R: Probabilmente stai cercando di aggiungere un figlio nel file dell'oggetto di gioco, ma ciò non è possibile. Puoi farlo soltanto nel file di collezione. Per capire perché, devi ricordare che le gerarchie genitore-figlio costituiscono esclusivamente una gerarchia di trasformazioni del _grafo della scena_ (scene graph). Un oggetto di gioco che non è stato posizionato (o generato) in una scena (collezione) non fa parte di un grafo della scena e quindi non può far parte di una gerarchia del grafo della scena. Puoi ottenere l'ID del genitore dell'oggetto di gioco usando [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id).


#### D: Perché non posso inviare messaggi a tutti i figli di un oggetto di gioco? {#q-why-cant-i-broadcast-messages-to-all-children-of-a-game-object}

R: Le relazioni genitore-figlio esprimono soltanto le relazioni di trasformazione del grafo della scena e non devono essere confuse con le aggregazioni della programmazione orientata agli oggetti. Se ti concentri sui dati del tuo gioco e sul modo migliore di trasformarli mentre il gioco cambia stato, probabilmente avrai meno bisogno di inviare continuamente messaggi con dati di stato a molti oggetti. Quando servono gerarchie di dati, queste possono essere costruite e gestite facilmente in Lua.


#### D: Perché compaiono artefatti visivi attorno ai bordi dei miei sprite? {#q-why-am-i-experiencing-visual-artifacts-around-the-edges-of-my-sprites}

R: Si tratta di un artefatto visivo chiamato "edge bleeding", nel quale i pixel ai bordi delle immagini adiacenti in un atlas contaminano l'immagine assegnata allo sprite. La soluzione consiste nell'aggiungere ai bordi delle immagini dell'atlas righe e colonne extra di pixel identici. Fortunatamente, l'editor degli atlas di Defold può farlo automaticamente. Apri l'atlas e imposta il valore *Extrude Borders* su 1.


#### D: Posso modificare la tinta dei miei sprite o renderli trasparenti, oppure devo scrivere uno shader apposito? {#q-can-i-tint-my-sprites-or-make-them-transparent-or-do-i-have-to-write-my-own-shader-for-it}

R: Lo shader integrato utilizzato per impostazione predefinita da tutti gli sprite definisce una costante "tint":

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### D: Se imposto la coordinata z di uno sprite a 100, non viene renderizzato. Perché? {#q-if-i-set-the-z-coordinate-of-a-sprite-to-100-then-its-not-rendered-why}

R: La posizione Z di un oggetto di gioco controlla l'ordine di rendering. I valori bassi vengono disegnati prima dei valori alti. Nello script di rendering predefinito vengono disegnati gli oggetti di gioco con una profondità compresa tra -1 e 1; qualsiasi valore inferiore o superiore non viene disegnato. Puoi trovare maggiori informazioni sullo script di rendering nella [documentazione ufficiale sul rendering](/manuals/render). Nei nodi GUI il valore Z viene ignorato e non influisce in alcun modo sull'ordine di rendering. I nodi vengono invece renderizzati nell'ordine in cui sono elencati e in base alle gerarchie dei figli (e ai livelli). Per saperne di più sul rendering della GUI e sull'ottimizzazione delle chiamate di disegno tramite i livelli, consulta la [documentazione ufficiale sulla GUI](/manuals/gui).


#### D: Cambiare l'intervallo Z della proiezione della vista in un intervallo da -100 a 100 influirebbe sulle prestazioni? {#q-would-changing-the-view-projection-z-range-to-100-to-100-impact-performance}

R: No. L'unico effetto riguarda la precisione. Il buffer Z è logaritmico e ha una risoluzione molto fine dei valori Z vicini a 0 e una risoluzione minore lontano da 0. Ad esempio, con un buffer a 24 bit i valori 10.0 e 10.000005 possono essere distinti, mentre 10000 e 10005 no.


#### D: Non c'è coerenza nel modo in cui sono rappresentati gli angoli, perché? {#q-there-is-no-consistency-to-how-angles-are-represented-why}

R: In realtà c'è coerenza. Gli angoli sono espressi in gradi ovunque nell'editor e nelle API di gioco. Le librerie matematiche utilizzano i radianti. Attualmente la convenzione non viene rispettata dalla proprietà fisica `angular_velocity`, espressa in radianti/s. Si prevede che questo cambierà.


#### D: Quando creo un nodo box GUI con solo colore (senza texture), come viene renderizzato? {#q-when-creating-a-gui-box-node-with-only-color-no-texture-how-will-it-be-rendered}

R: È semplicemente una forma colorata tramite i vertici. Tieni presente che comporta comunque un costo in termini di fill-rate.


#### D: Se cambio gli asset al volo, il motore li rimuoverà automaticamente dalla memoria? {#q-if-i-change-assets-on-the-fly-will-the-engine-automatically-unload-them}

R: Tutte le risorse hanno un conteggio dei riferimenti interno. Non appena il conteggio dei riferimenti raggiunge zero, la risorsa viene rilasciata.


#### D: È possibile riprodurre l'audio senza un componente audio collegato a un oggetto di gioco? {#q-is-it-possible-to-play-audio-without-the-use-of-an-audio-component-attached-to-a-game-object}

R: Tutto è basato su componenti. È possibile creare un oggetto di gioco privo di rappresentazione visiva con più suoni e riprodurli inviando messaggi all'oggetto che li controlla.


#### D: È possibile cambiare il file audio associato a un componente audio a runtime? {#q-is-it-possible-to-change-the-audio-file-associated-with-an-audio-component-at-run-time}

R: In generale, tutte le risorse sono dichiarate staticamente, con il vantaggio che la loro gestione è automatica. Puoi usare le [proprietà delle risorse](/manuals/script-properties/#resource-properties) per cambiare la risorsa assegnata a un componente.


#### D: C'è un modo per accedere alle proprietà delle forme di collisione della fisica? {#q-is-there-a-way-to-access-the-physics-collision-shape-properties}

R: Sì, consulta l'API della fisica, in particolare [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) e [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table).


#### D: C'è un modo rapido per visualizzare gli oggetti di collisione nella mia scena? (come la visualizzazione di debug di Box2D) {#q-is-there-any-quick-way-to-render-the-collision-objects-in-my-scene-like-box2ds-debug-draw}

R: Sì, imposta il flag *physics.debug* in *game.project*. (Consulta la [documentazione ufficiale sulle impostazioni del progetto](/manuals/project-settings/#debug))


#### D: Quali sono i costi in termini di prestazioni di un gran numero di contatti/collisioni? {#q-what-are-the-performance-costs-of-having-many-contactscollisions}

R: Defold esegue internamente una versione modificata di Box2D e il costo in termini di prestazioni dovrebbe essere abbastanza simile. Puoi sempre vedere quanto tempo il motore dedica alla fisica aprendo il [profilatore](/manuals/debugging). Dovresti anche considerare quale tipo di oggetti di collisione utilizzi. Gli oggetti statici, ad esempio, hanno un costo minore in termini di prestazioni. Per ulteriori dettagli, consulta la [documentazione ufficiale sulla fisica](/manuals/physics) in Defold.


#### D: Qual è l'impatto sulle prestazioni di un gran numero di componenti di effetti particellari? {#q-whats-the-performance-impact-of-having-many-particle-effect-components}

R: Dipende dal fatto che siano in riproduzione o meno. Un ParticleFx non in riproduzione non ha alcun costo in termini di prestazioni. L'impatto di un ParticleFx in riproduzione deve essere valutato con il profilatore, poiché dipende dalla sua configurazione. Come nella maggior parte degli altri casi, la memoria viene allocata in anticipo per il numero di ParticleFx definito da max_count in *game.project*.


#### D: Come ricevo input su un oggetto di gioco all'interno di una collezione caricata tramite un proxy di collezione? {#q-how-do-i-receive-input-to-a-game-object-inside-a-collection-loaded-via-a-collection-proxy}

R: Ogni collezione caricata tramite proxy ha il proprio stack di input. L'input viene instradato dallo stack di input della collezione principale, attraverso il componente proxy, agli oggetti della collezione. Ciò significa che non basta che l'oggetto di gioco nella collezione caricata acquisisca il focus dell'input: anche l'oggetto di gioco che _contiene_ il componente proxy deve acquisirlo. Consulta la [documentazione sull'input](/manuals/input) per i dettagli.


#### D: Posso usare proprietà degli script di tipo stringa? {#q-can-i-use-string-type-script-properties}

R: No. Defold supporta proprietà di tipo [hash](/ref/builtins#hash). Queste possono essere utilizzate per indicare tipi, identificatori di stato o chiavi di qualsiasi tipo. Gli hash possono anche essere utilizzati per memorizzare gli ID degli oggetti di gioco (percorsi), sebbene le proprietà [url](/ref/msg#msg.url) siano spesso preferibili perché l'editor popola automaticamente un menu a discesa con gli URL pertinenti. Consulta la [documentazione sulle proprietà degli script](/manuals/script-properties) per i dettagli.


#### D: Come accedo alle singole celle di una matrice (creata usando [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) o simile)? {#q-how-do-i-access-the-individual-cells-of-a-matrix-created-using-vmathmatrix4refvmathvmathmatrix4m1-or-similar}

R: Accedi alle celle usando `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` ecc.


#### D: Ricevo `Not enough resources to clone the node` quando uso [gui.clone()](/ref/gui/#gui.clone:node) o [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) {#q-i-am-getting-not-enough-resources-to-clone-the-node-when-using-guiclonerefguiguiclonenode-or-guiclone_treerefguiguiclone_treenode}

R: Aumenta il valore `Max Nodes` del componente GUI. Trovi questo valore nel pannello Properties quando selezioni la radice del componente in Outline.


## Il forum {#the-forum}

#### D: Posso pubblicare un thread in cui pubblicizzo il mio lavoro? {#q-can-i-post-a-thread-where-i-advertise-my-work}

R: Certamente! Abbiamo una [categoria "Work for hire"](https://forum.defold.com/c/work-for-hire) apposita. Incoraggeremo sempre tutto ciò che giova alla comunità, e offrire i tuoi servizi alla comunità — a pagamento o meno — ne è un buon esempio.


#### D: Ho creato un thread e aggiunto il mio lavoro: posso aggiungerne altro? {#q-i-made-a-thread-and-added-my-workcan-i-add-more}

R: Per ridurre i continui rilanci dei thread "Work for hire", non puoi pubblicare più di una volta ogni 14 giorni nel tuo thread (a meno che non sia una risposta diretta a un commento nel thread, nel qual caso puoi rispondere). Se vuoi aggiungere ulteriori lavori al tuo thread entro il periodo di 14 giorni, devi modificare i post esistenti aggiungendovi il nuovo contenuto.


#### D: Posso utilizzare la categoria Work for Hire per pubblicare offerte di lavoro? {#q-can-i-use-the-work-for-hire-category-to-post-job-offerings}

R: Certo, fai pure! Può essere utilizzata sia per offerte che per richieste, ad esempio: "Programmatore cerca artista di pixel art 2D; sono ricco e ti pagherò bene".
