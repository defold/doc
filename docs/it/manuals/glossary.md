---
title: Glossario di Defold
brief: Questo manuale elenca tutti gli elementi che incontri lavorando in Defold e ne fornisce una breve descrizione.
---

# Glossario di Defold {#defold-glossary}

Questo glossario fornisce una breve descrizione di tutti gli elementi che incontri in Defold. Nella maggior parte dei casi trovi un link alla documentazione di approfondimento.

## Insieme di animazioni {#animation-set}

![Insieme di animazioni](images/icons/animationset.png){.left} Una risorsa insieme di animazioni (animation set) contiene un elenco di file glTF o di altri file .animationset da cui leggere le animazioni. Aggiungere un file .animationset a un altro è utile se condividi insiemi parziali di animazioni tra più modelli. Consulta il [manuale sull'animazione dei modelli](/manuals/model-animation/) per i dettagli.

## Atlas

![Atlas](images/icons/atlas.png){.left} Un atlas è un insieme di immagini separate che vengono riunite in un'immagine più grande per ragioni di prestazioni e di memoria. Può contenere immagini statiche o sequenze di immagini animate fotogramma per fotogramma (flip-book). Gli atlas vengono utilizzati da diversi componenti per condividere risorse grafiche. Consulta la [documentazione sugli atlas](/manuals/atlas) per ulteriori informazioni.

## Risorse integrate {#builtins}

![Risorse integrate](images/icons/builtins.png){.left} La cartella di progetto builtins è una cartella di sola lettura che contiene utili risorse predefinite. Qui trovi il renderer predefinito, lo script di rendering, i materiali e altro ancora. Se devi personalizzare una di queste risorse, copiala nel tuo progetto e modificala secondo le tue esigenze.

## Camera

![Camera](images/icons/camera.png){.left} Il componente camera aiuta a decidere quale parte del mondo di gioco deve essere visibile e come deve essere proiettata. Un caso d'uso comune consiste nell'associare una camera all'oggetto di gioco del giocatore oppure nell'avere un oggetto di gioco separato con una camera che segue il giocatore tramite un algoritmo che ne rende fluido il movimento. Consulta la [documentazione sulla camera](/manuals/camera) per ulteriori informazioni.

## Oggetto di collisione {#collision-object}

![Oggetto di collisione](images/icons/collision-object.png){.left} Gli oggetti di collisione sono componenti che aggiungono proprietà fisiche agli oggetti di gioco, come forma nello spazio, peso, attrito e restituzione. Queste proprietà determinano come l'oggetto di collisione deve collidere con altri oggetti di collisione. I tipi più comuni sono gli oggetti cinematici, gli oggetti dinamici e i trigger. Un oggetto cinematico fornisce informazioni dettagliate sulle collisioni, alle quali devi rispondere manualmente; un oggetto dinamico viene simulato automaticamente dal motore fisico secondo le leggi della fisica newtoniana. I trigger sono semplici forme che rilevano se altre forme sono entrate o uscite dal trigger. Consulta la [documentazione sulla fisica](/manuals/physics) per i dettagli sul loro funzionamento.

## Componente {#component}

I componenti (component) servono a dare agli oggetti di gioco un aspetto e/o funzionalità specifici, come grafica, animazione, comportamento definito tramite codice e suono. Non hanno una vita autonoma, ma devono essere contenuti negli oggetti di gioco. Defold offre molti tipi di componenti. Consulta il [manuale sugli elementi costitutivi](/manuals/building-blocks) per una descrizione dei componenti.

## Collezione {#collection}

![Collezione](images/icons/collection.png){.left} Le collezioni (collection) sono il meccanismo di Defold per creare modelli, chiamati "prefab" in altri motori, che permettono di riutilizzare gerarchie di oggetti di gioco. Le collezioni sono strutture ad albero che contengono oggetti di gioco e altre collezioni. Una collezione viene sempre salvata in un file e inserita nel gioco in modo statico, posizionandola manualmente nell'editor, oppure in modo dinamico, generandola durante l'esecuzione. Consulta il [manuale sugli elementi costitutivi](/manuals/building-blocks) per una descrizione delle collezioni.

## Fabbrica di collezioni {#collection-factory}

![Fabbrica di collezioni](images/icons/collection-factory.png){.left} Un componente fabbrica di collezioni (collection factory) serve a generare dinamicamente gerarchie di oggetti di gioco in un gioco in esecuzione. Consulta il [manuale sulle fabbriche di collezioni](/manuals/collection-factory) per i dettagli.

## Proxy di collezione {#collection-proxy}

![Collezione](images/icons/collection.png){.left} Un proxy di collezione (collection proxy) serve a caricare e abilitare collezioni al volo mentre un'applicazione o un gioco è in esecuzione. Il caso d'uso più comune dei proxy di collezione è il caricamento dei livelli quando è il momento di giocarli. Consulta la [documentazione sui proxy di collezione](/manuals/collection-proxy) per i dettagli.

## Mappa cubica {#cubemap}

![Mappa cubica](images/icons/cubemap.png){.left} Una mappa cubica (cubemap) è un tipo speciale di texture composto da 6 texture diverse mappate sulle facce di un cubo. È utile per il rendering di skybox e di vari tipi di mappe di riflessione e illuminazione.

## Debug {#debugging}

Prima o poi il tuo gioco si comporterà in modo imprevisto e dovrai capire che cosa non va. Imparare a eseguire il debug è un'arte e, fortunatamente, Defold include un debugger per aiutarti. Consulta il [manuale sul debug](/manuals/debugging) per ulteriori informazioni.

## Profili di visualizzazione {#display-profiles}

![Profili di visualizzazione](images/icons/display-profiles.png){.left} Il file di risorsa dei profili di visualizzazione serve a specificare i layout della GUI in base all'orientamento, al rapporto d'aspetto o al modello del dispositivo. Ti aiuta ad adattare l'interfaccia utente a qualsiasi tipo di dispositivo. Per saperne di più, consulta il [manuale sui layout](/manuals/gui-layouts).

## Fabbrica {#factory}

![Fabbrica](images/icons/factory.png){.left} In alcune situazioni non puoi posizionare manualmente tutti gli oggetti di gioco necessari in una collezione: devi crearli dinamicamente, al volo. Per esempio, un giocatore potrebbe sparare proiettili e ogni colpo dovrebbe essere generato dinamicamente e lanciato quando il giocatore preme il grilletto. Per creare oggetti di gioco dinamicamente, a partire da un pool di oggetti preallocato, usa un componente fabbrica (factory). Consulta il [manuale sulle fabbriche](/manuals/factory) per i dettagli.

## Font

![File di font](images/icons/font.png){.left} Una risorsa font viene creata a partire da un file di font TrueType o OpenType. La risorsa specifica la dimensione a cui eseguire il rendering del font e il tipo di decorazione, contorno e ombra, da applicare. I font vengono usati dai componenti GUI ed etichetta. Consulta il [manuale sui font](/manuals/font/) per i dettagli.

## Fragment shader

![Fragment shader](images/icons/fragment-shader.png){.left} È un programma eseguito sul processore grafico per ogni pixel (frammento) di un poligono quando viene disegnato sullo schermo. Lo scopo del fragment shader è determinare il colore di ogni frammento risultante. Lo fa tramite calcoli, campionamenti delle texture (uno o più) o una combinazione di campionamenti e calcoli. Consulta il [manuale sugli shader](/manuals/shader) per ulteriori informazioni.

## Gamepad {#gamepads}

![Gamepad](images/icons/gamepad.png){.left} Un file di risorsa gamepads definisce come l'input di specifici dispositivi gamepad viene associato ai trigger di input del gamepad su una determinata piattaforma. Consulta il [manuale sull'input](/manuals/input) per i dettagli.

## Oggetto di gioco {#game-object}

![Oggetto di gioco](images/icons/game-object.png){.left} Gli oggetti di gioco (game object) sono oggetti semplici con un proprio ciclo di vita durante l'esecuzione del gioco. Gli oggetti di gioco sono contenitori e in genere includono componenti visivi o sonori, come un suono o uno sprite. Possono anche ricevere un comportamento tramite componenti script. Puoi creare oggetti di gioco e posizionarli nelle collezioni nell'editor oppure generarli dinamicamente durante l'esecuzione tramite fabbriche. Consulta il [manuale sugli elementi costitutivi](/manuals/building-blocks) per una descrizione degli oggetti di gioco.

## GUI

![Componente GUI](images/icons/gui.png){.left} Un componente GUI contiene elementi usati per costruire interfacce utente: testo e blocchi colorati e/o con texture. Gli elementi possono essere organizzati in strutture gerarchiche, controllati tramite script e animati. I componenti GUI vengono in genere usati per creare interfacce sovrapposte al gioco (HUD), sistemi di menu e notifiche sullo schermo. I componenti GUI sono controllati da script GUI che definiscono il comportamento della GUI e gestiscono l'interazione dell'utente con essa. Per saperne di più, consulta la [documentazione sulla GUI](/manuals/gui).

## Script GUI {#gui-script}

![Script GUI](images/icons/script.png){.left} Gli script GUI servono a controllare il comportamento dei componenti GUI. Controllano le animazioni della GUI e il modo in cui l'utente interagisce con essa. Consulta il [manuale su Lua in Defold](/manuals/lua) per i dettagli sull'uso degli script Lua in Defold.

## Hot reload

L'editor Defold permette di aggiornare i contenuti di un gioco già in esecuzione, sia su desktop sia su dispositivo. Questa funzionalità è estremamente potente e può migliorare molto il flusso di lavoro di sviluppo. Consulta il [manuale sull'hot reload](/manuals/hot-reload) per ulteriori informazioni.

## Binding di input {#input-binding}

![Binding di input](images/icons/input-binding.png){.left} I file di binding di input definiscono come il gioco deve interpretare l'input hardware (mouse, tastiera, touchscreen e gamepad). Il file associa l'input hardware ad _azioni_ di input di alto livello, come "jump" e "move_forward". Nei componenti script che ricevono l'input puoi definire le azioni che il gioco o l'applicazione deve eseguire in risposta a un determinato input. Consulta la [documentazione sull'input](/manuals/input) per i dettagli.

## Etichetta {#label}

![Etichetta](images/icons/label.png){.left} Il componente etichetta (label) permette di associare contenuti testuali a qualsiasi oggetto di gioco. Visualizza sullo schermo un testo con un font specifico, nello spazio di gioco. Consulta il [manuale sulle etichette](/manuals/label) per ulteriori informazioni.

## Libreria {#library}

![Oggetto di gioco](images/icons/builtins.png){.left} Defold permette di condividere dati tra progetti tramite un potente meccanismo di librerie. Puoi usarlo per configurare librerie condivise accessibili da tutti i tuoi progetti, per uso personale o per l'intero team. Per saperne di più sul meccanismo delle librerie, consulta la [documentazione sulle librerie](/manuals/libraries).

## Linguaggio Lua {#lua-language}

Il linguaggio di programmazione Lua viene usato in Defold per creare la logica di gioco. Lua è un linguaggio di scripting potente, efficiente e molto compatto. Supporta la programmazione procedurale, la programmazione orientata agli oggetti, la programmazione funzionale, la programmazione guidata dai dati e la descrizione dei dati. Puoi approfondire il linguaggio sul sito ufficiale di Lua all'indirizzo https://www.lua.org/ e nel [manuale su Lua in Defold](/manuals/lua).

## Modulo Lua {#lua-module}

![Modulo Lua](images/icons/lua-module.png){.left} I moduli Lua permettono di strutturare il progetto e creare codice di libreria riutilizzabile. Per saperne di più, consulta il [manuale sui moduli Lua](/manuals/modules/)

## Materiale {#material}

![Materiale](images/icons/material.png){.left} I materiali definiscono come devono essere renderizzati i vari oggetti, specificando gli shader e le loro proprietà. Consulta il [manuale sui materiali](/manuals/material) per ulteriori informazioni.

## Messaggio {#message}

I componenti comunicano tra loro e con altri sistemi tramite lo scambio di messaggi. Rispondono inoltre a una serie di messaggi predefiniti che li modificano o attivano azioni specifiche. Puoi inviare messaggi per nascondere elementi grafici o dare una spinta agli oggetti fisici. Anche il motore usa i messaggi per notificare eventi ai componenti, per esempio quando le forme fisiche collidono. Il meccanismo di scambio dei messaggi richiede un destinatario per ogni messaggio inviato. Per questo, ogni elemento del gioco ha un indirizzo univoco. Per consentire la comunicazione tra gli oggetti, Defold estende Lua con lo scambio di messaggi. Defold fornisce anche una libreria di funzioni utili.

Per esempio, il codice Lua necessario per nascondere un componente sprite in un oggetto di gioco è il seguente:

```lua
msg.post("#weapon", "disable")
```

Qui, `"#weapon"` è l'indirizzo del componente sprite dell'oggetto corrente. `"disable"` è un messaggio a cui i componenti sprite rispondono. Consulta la [documentazione sullo scambio di messaggi](/manuals/message-passing) per una spiegazione approfondita del suo funzionamento.

## Modello {#model}

![Modello](images/icons/model.png){.left} Il componente modello 3D può importare nel gioco asset glTF di mesh, scheletri e animazioni. Consulta il [manuale sui modelli](/manuals/model/) per ulteriori informazioni.

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Le particelle sono molto utili per creare effetti visivi accattivanti, soprattutto nei giochi. Puoi usarle per creare nebbia, fumo, fuoco, pioggia o foglie che cadono. Defold include un potente editor di effetti particellari che permette di creare e perfezionare gli effetti mentre li esegui in tempo reale nel gioco. La [documentazione su ParticleFX](/manuals/particlefx) spiega nel dettaglio come funziona.

## Profilazione {#profiling}

Buone prestazioni sono fondamentali nei giochi ed è essenziale poter eseguire la profilazione delle prestazioni e della memoria per misurare il comportamento del gioco e individuare i colli di bottiglia delle prestazioni e i problemi di memoria da risolvere. Consulta il [manuale sulla profilazione](/manuals/profiling) per ulteriori informazioni sugli strumenti di profilazione disponibili per Defold.

## Rendering {#render}

![Rendering](images/icons/render.png){.left} I file di rendering contengono le impostazioni usate per visualizzare il gioco sullo schermo. Definiscono quale script di rendering e quali materiali usare. Consulta il [manuale sul rendering](/manuals/render/) per ulteriori dettagli.

## Script di rendering {#render-script}

![Script di rendering](images/icons/script.png){.left} Uno script di rendering è uno script Lua che controlla come il gioco o l'applicazione deve essere renderizzato sullo schermo. Esiste uno script di rendering predefinito che copre i casi più comuni, ma puoi scriverne uno tuo se hai bisogno di modelli di illuminazione personalizzati o altri effetti. Consulta il [manuale sul rendering](/manuals/render/) per ulteriori dettagli sul funzionamento della pipeline di rendering e il [manuale su Lua in Defold](/manuals/lua) per i dettagli sull'uso degli script Lua in Defold.

## Script

![Script](images/icons/script.png){.left}  Uno script è un componente che contiene un programma che definisce i comportamenti degli oggetti di gioco. Con gli script puoi specificare le regole del gioco e come gli oggetti devono rispondere alle varie interazioni, sia con il giocatore sia con altri oggetti. Tutti gli script sono scritti nel linguaggio di programmazione Lua. Per lavorare con Defold, è necessario che tu o qualcuno del tuo team impari a programmare in Lua. Consulta il [manuale su Lua in Defold](/manuals/lua) per una panoramica di Lua e per i dettagli sull'uso degli script Lua in Defold.

## Suono {#sound}

![Suono](images/icons/sound.png){.left} Il componente suono si occupa di riprodurre un suono specifico. Defold supporta i file WAV, Ogg Vorbis e Ogg Opus. Il supporto a Opus deve essere abilitato nell'App Manifest. Consulta il [manuale sui suoni](/manuals/sound) per ulteriori informazioni.

## Sprite

![Sprite](images/icons/sprite.png){.left} Uno sprite è un componente che aggiunge grafica agli oggetti di gioco. Visualizza un'immagine proveniente da una sorgente di tasselli o da un atlas. Gli sprite supportano nativamente l'animazione fotogramma per fotogramma e l'animazione scheletrica. In genere vengono usati per personaggi e oggetti.

## Profili di texture {#texture-profiles}

![Profili di texture](images/icons/texture-profiles.png){.left} Il file di risorsa dei profili di texture viene usato durante la creazione del bundle per elaborare e comprimere automaticamente i dati delle immagini, contenuti in atlas, sorgenti di tasselli, mappe cubiche e texture autonome usate per modelli, GUI e altro. Per saperne di più, consulta il [manuale sui profili di texture](/manuals/texture-profiles).

## Mappa di tasselli {#tile-map}

![Mappa di tasselli](images/icons/tilemap.png){.left} I componenti mappa di tasselli (tile map) visualizzano immagini di una sorgente di tasselli in una o più griglie sovrapposte. Vengono usati soprattutto per costruire ambienti di gioco: terreno, muri, edifici e ostacoli. Una mappa di tasselli può visualizzare diversi livelli allineati e sovrapposti con una modalità di fusione specifica. È utile, per esempio, per posizionare fogliame sopra i tasselli d'erba dello sfondo. È anche possibile modificare dinamicamente l'immagine visualizzata in un tassello. Questo permette, per esempio, di distruggere un ponte e renderlo impraticabile semplicemente sostituendo i tasselli con altri che raffigurano il ponte distrutto e contengono la forma fisica corrispondente. Consulta la [documentazione sulle mappe di tasselli](/manuals/tilemap) per ulteriori informazioni.

## Sorgente di tasselli {#tile-source}

![Sorgente di tasselli](images/icons/tilesource.png){.left} Una sorgente di tasselli (tile source) descrive una texture composta da più immagini piccole, tutte della stessa dimensione. Puoi definire animazioni fotogramma per fotogramma a partire da una sequenza di immagini in una sorgente di tasselli. Le sorgenti di tasselli possono anche calcolare automaticamente le forme di collisione a partire dai dati delle immagini. È molto utile per creare livelli composti da tasselli con cui gli oggetti possono collidere e interagire. Le sorgenti di tasselli vengono usate dai componenti mappa di tasselli, sprite e ParticleFX per condividere risorse grafiche. Tieni presente che gli atlas sono spesso più adatti delle sorgenti di tasselli. Consulta la [documentazione sulle mappe di tasselli](/manuals/tilemap) per ulteriori informazioni.

## Vertex shader

![Vertex shader](images/icons/vertex-shader.png){.left} Il vertex shader calcola la geometria sullo schermo delle primitive poligonali di un componente. Per qualsiasi tipo di componente visivo, che sia uno sprite, una mappa di tasselli o un modello, la forma è rappresentata da un insieme di posizioni dei vertici dei poligoni. Il programma vertex shader elabora ogni vertice nello spazio del mondo e calcola la coordinata risultante che ciascun vertice di una primitiva deve avere. Consulta il [manuale sugli shader](/manuals/shader) per ulteriori informazioni.
