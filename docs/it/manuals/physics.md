---
title: La fisica in Defold
brief: Defold include motori fisici per il 2D e il 3D. Consentono di simulare interazioni basate sulla fisica newtoniana tra diversi tipi di oggetti di collisione.
---

# Fisica {#physics}

Defold include [Box2D](https://box2d.org/) per le simulazioni fisiche 2D e Bullet per la fisica 3D. L'[impostazione Physics 2D dell'App Manifest](/manuals/app-manifest/#physics-2d) permette di selezionare **Box2D Version 3**, **Box2D (Legacy Defold version)** o **None**. L'implementazione precedente è quella predefinita; Box2D 3 deve essere abilitato esplicitamente. Cambiare implementazione può modificare i risultati della simulazione e richiedere una nuova regolazione delle [impostazioni di progetto di Box2D](/manuals/project-settings/#box2d) specifiche della versione.

Il flusso di lavoro basato su componenti per gli oggetti di collisione e il modulo `physics` descritti in questi manuali funzionano con entrambe le implementazioni di Box2D; selezionando **None** si rimuove la fisica 2D. Defold espone anche le API di livello inferiore [`b2d`](/ref/stable/b2d/), `b2d.body`, `b2d.fixture`, `b2d.shape`, `b2d.joint`, `b2d.chain` e `b2d.world` per accedere direttamente a corpi, forme, giunti, catene e mondi 2D. Non tutte le funzioni di basso livello sono disponibili in entrambe le implementazioni di Box2D; verifica la documentazione API generata di ogni funzione in relazione all'implementazione selezionata nell'App Manifest.

I concetti principali dei motori fisici usati in Defold sono:

* **Oggetti di collisione** - Un oggetto di collisione è un componente che usi per assegnare un comportamento fisico a un oggetto di gioco (game object). Un oggetto di collisione ha proprietà fisiche come peso, attrito e forma. [Scopri come creare un oggetto di collisione](/manuals/physics-objects).
* **Forme di collisione** - Un oggetto di collisione può usare diverse forme primitive oppure una singola forma complessa per definire la sua estensione nello spazio. [Scopri come aggiungere forme a un oggetto di collisione](/manuals/physics-shapes).
* **Gruppi di collisione** - Tutti gli oggetti di collisione devono appartenere a un gruppo predefinito e ogni oggetto di collisione può specificare un elenco di altri gruppi con cui può entrare in collisione. [Scopri come usare i gruppi di collisione](/manuals/physics-groups).
* **Messaggi di collisione** - Quando due oggetti di collisione entrano in collisione, il motore fisico invia messaggi agli oggetti di gioco a cui appartengono i componenti. [Scopri di più sui messaggi di collisione](/manuals/physics-messages)

Oltre agli oggetti di collisione stessi, puoi anche definire **vincoli** tra gli oggetti di collisione, più comunemente chiamati **giunti**, per collegare due oggetti di collisione e limitarne il movimento o, in altri modi, applicare forze e influenzarne il comportamento nella simulazione fisica. [Scopri di più sui giunti](/manuals/physics-joints).

Puoi anche interrogare il mondo fisico e leggerne le informazioni lungo un raggio rettilineo, tramite un'operazione chiamata **proiezione di un raggio (ray cast)**. [Scopri di più sulle proiezioni di raggi](/manuals/physics-ray-casts).


## Unità usate nella simulazione del motore fisico {#units-used-by-the-physics-engine-simulation}

Il motore fisico simula la fisica newtoniana ed è progettato per funzionare bene con le unità metri, chilogrammi e secondi (MKS). Inoltre, il motore fisico è ottimizzato per oggetti in movimento con dimensioni comprese tra 0.1 e 10 metri (gli oggetti statici possono essere più grandi) e, per impostazione predefinita, considera 1 unità (pixel) equivalente a 1 metro. Questa conversione tra pixel e metri è comoda a livello di simulazione, ma non è molto utile dal punto di vista della creazione di un gioco. Con le impostazioni predefinite, una forma di collisione di 200 pixel verrebbe considerata grande 200 metri, un valore ben al di fuori dell'intervallo consigliato, almeno per un oggetto in movimento.

In generale, è necessario adattare la scala della simulazione fisica affinché funzioni bene con le dimensioni tipiche degli oggetti di un gioco. Puoi modificare la scala della simulazione fisica in *game.project* tramite l'[impostazione della scala della fisica](/manuals/project-settings/#physics). Impostando questo valore, per esempio, a 0.02, 200 pixel verrebbero considerati equivalenti a 4 metri. Tieni presente che anche la gravità (modificabile anch'essa in *game.project*) deve essere aumentata per compensare il cambiamento di scala.


## Aggiornamenti della fisica {#physics-updates}

È consigliabile aggiornare il motore fisico a intervalli regolari per garantire una simulazione stabile (invece di aggiornarlo a intervalli potenzialmente irregolari, dipendenti dalla frequenza dei fotogrammi). Puoi usare un aggiornamento a intervallo fisso per la fisica attivando l'[impostazione Use Fixed Timestep](/manuals/project-settings/#physics) della sezione Physics nel file *game.project*. La frequenza di aggiornamento è controllata dall'[impostazione Fixed Update Frequency](/manuals/project-settings/#engine) della sezione Engine nel file *game.project*. Quando usi un intervallo di tempo fisso per la fisica, è consigliabile usare anche la funzione del ciclo di vita `fixed_update(self, dt)` per interagire con gli oggetti di collisione del gioco, per esempio quando applichi loro delle forze.


## Avvertenze e problemi comuni {#caveats-and-common-issues}

Proxy di collezione
: Tramite i proxy di collezione (collection proxy) puoi caricare nel motore più di una collezione di primo livello, o *mondo di gioco*. In questo caso, è importante sapere che ogni collezione di primo livello costituisce un mondo fisico separato. Le interazioni fisiche ([collisioni, trigger](/manuals/physics-messages) e [proiezioni di raggi](/manuals/physics-ray-casts)) avvengono solo tra oggetti appartenenti allo stesso mondo. Quindi, anche se gli oggetti di collisione di due mondi si trovano visivamente uno sopra l'altro, non può verificarsi alcuna interazione fisica tra loro.

Collisioni non rilevate
: Se le collisioni non vengono gestite o rilevate correttamente, consulta la sezione sul [debug della fisica nel manuale di debug](/manuals/debugging-game-logic/#debugging-problems-with-physics).
