---
title: Defold per chi usa Godot
brief: Questa guida presenta Defold a chi usa Godot confrontando concetti familiari e spiegando come usare gli strumenti e le API corrispondenti.
---

# Defold per chi usa Godot {#defold-for-godot-users}

Se hai già esperienza con Godot, conosci già gran parte di ciò che ti serve per creare un gioco con Defold. In questa guida vedrai come mettere a frutto quell'esperienza per iniziare subito e quali differenze tenere presenti per evitare gli errori più comuni. Per il confronto abbiamo usato Godot 4.7.

## Introduzione {#introduction}

Defold è un motore di gioco gratuito e multipiattaforma per giochi 2D e 3D, con un editor per Windows, Linux e macOS. Il codice sorgente completo del motore e dell'editor è disponibile su [GitHub](https://github.com/defold/defold/). Puoi compilarlo tu oppure scaricare una versione per il tuo sistema operativo.

A prima vista Defold somiglia molto a Godot. Entrambi i motori ti permettono di comporre un gioco a partire da elementi riutilizzabili e di definirne il comportamento con gli script. Godot offre molti nodi specializzati. Defold offre un insieme più ristretto di componenti generici e affida la logica di gioco agli script e ai moduli Lua che li utilizzano. In Defold, per esempio, il personaggio del giocatore potrebbe essere un oggetto di gioco (game object) con uno sprite o un modello, un oggetto di collisione e uno script come componenti.

Defold punta a mantenere piccolo il runtime e a usare le risorse in modo efficiente, due aspetti particolarmente importanti per i giochi web e mobili. Alcuni limiti del motore vengono impostati in anticipo per permettere la preallocazione della memoria.

Rispetto a Godot troverai meno elementi di gioco e di interfaccia pronti all'uso, ma puoi ottenere gli stessi risultati combinando o estendendo i componenti di base di Defold. Il nucleo del motore è progettato per essere il più leggero possibile. Puoi ridurlo ulteriormente escludendo le funzioni che non ti servono oppure ampliarlo con estensioni native e moduli Lua. Nel [Defold Asset Portal](https://defold.com/assets/) trovi centinaia di moduli, librerie ed estensioni per creare, ad esempio, interfacce complesse o pipeline di rendering avanzate, o per semplificare alcune attività di sviluppo.

Per maggiori dettagli, consulta la [panoramica delle funzionalità di Defold](https://defold.com/product/).

## Installazione {#installation}

1. Scarica Defold per il tuo sistema operativo dalla [pagina di download](https://defold.com/download/).
2. Estrai l'archivio e avvia l'editor.

Puoi creare ed eseguire il tuo primo progetto senza installare un hub separato o modelli di esportazione. Consulta il [manuale di installazione](/manuals/install/) per le istruzioni specifiche per la tua piattaforma.

Puoi aggiornare Defold direttamente dall'editor. Quando aggiorni un progetto esistente, leggi le note di rilascio e prova il gioco sulle piattaforme di destinazione.

## Schermata iniziale {#welcome-screen}

All'avvio Defold mostra una schermata da cui puoi aprire un progetto recente o crearne uno nuovo. Svolge una funzione simile a quella del gestore dei progetti di Godot.

![Gestore dei progetti di Godot e schermata iniziale di Defold](images/godot/godot_1.png)

In Defold puoi creare un progetto a partire da queste sezioni:

- **Templates** offre progetti vuoti di base o specifici per una piattaforma.
- **Tutorials** contiene progetti introduttivi con istruzioni da seguire.
- **Samples** raccoglie esempi e progetti di partenza da eseguire ed esplorare.

![Gestore dei progetti di Godot e schermata iniziale di Defold](images/godot/godot_2.png)

Nella sezione Samples di Defold trovi progetti di partenza ed esempi simili a quelli del Godot Asset Store:

![Gestore dei progetti di Godot e schermata iniziale di Defold](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Panoramica dell'editor Defold {#defold-editor-overview}

Riconoscerai i pannelli principali, anche se i nomi e le posizioni sono diversi. Per facilitare il confronto abbiamo disposto i pannelli dell'editor di Godot in modo simile alla disposizione predefinita di Defold:

![Panoramica dell'editor di Godot](images/godot/godot_4.png)
![Panoramica dell'editor Defold](images/godot/godot_5.png)

| Godot | Defold | Funzione nell'editor Defold |
|---|---|---|
| Pannello FileSystem | Assets | Permette di gestire i file e le cartelle del progetto e ne rispecchia esattamente la struttura su disco. |
| Vista 2D/3D ed editor delle risorse | Main editor | Cambia in base al file che apri, per esempio una collezione, una GUI, un atlas o uno script. Puoi dividerlo in due pannelli. |
| Pannello Scene | Outline | Mostra la struttura della risorsa corrente. Non rappresenta l'albero globale della scena in esecuzione. |
| Inspector | Properties | Mostra le proprietà dell'oggetto, del componente o della risorsa che hai selezionato. |
| Output e Debugger | Tools | Comprende Console, Build Errors, Search Results e il debugger. |
| Integrazione del controllo di versione | Changed Files | Mostra le modifiche se il progetto usa Git. |

Nell'editor 3D di Defold trovi anche una barra degli strumenti nell'angolo in alto a destra. Puoi approfondire [nel manuale sulla modifica delle scene](/manuals/scene-editing/#toolbar-overview).

### Orientamento della scena in 2D e 3D {#2d-and-3d-scene-orientation}

:[Orientamento della scena in 2D e 3D](../shared/2d-and-3d-scene-orientation.md)

### Pannelli {#panes}

I pannelli di Defold rimangono nella stessa finestra. Puoi ridimensionarli trascinandone i bordi e mostrarli o nasconderli con `F6`, `F7` e `F8` oppure dal menu `View`:

![Visibilità dei pannelli](images/editor/editor_panes.png)

### Coordinate {#coordinates}

In un progetto 2D, se usi lo script di rendering predefinito e la collezione di Defold non contiene un componente camera, le coordinate `(0, 0)` corrispondono all'angolo in basso a sinistra della finestra di gioco. L'asse Y positivo punta **verso l'alto** e l'asse X positivo verso destra.

Nelle consuete coordinate schermo 2D di Godot, l'asse Y positivo punta **verso il basso**. Tienine conto quando trasferisci posizioni o codice di movimento.

![Differenza tra le coordinate 2D di Defold e Godot](images/godot/godot_6.png)

Nel sistema di coordinate 3D di Godot l'asse Y positivo punta verso l'alto, come in Defold. Defold usa lo stesso sistema di coordinate 3D per i giochi 2D e 3D. Una tipica configurazione 2D usa il piano XY con una proiezione ortografica. Se necessario, puoi configurare la camera diversamente.

![Corrispondenza tra le coordinate 3D di Defold e Godot](images/godot/godot_7.png)

Per approfondire, consulta il [manuale sulla panoramica dell'editor Defold](/manuals/editor/).

---

## Concetti fondamentali {#key-concepts}

In Godot crei le **scene** a partire dai nodi. In Defold lavori con componenti, oggetti di gioco e collezioni di oggetti di gioco.

In Godot, per esempio, potresti creare il personaggio del giocatore con un `Node2D`, aggiungere uno `Sprite2D` come figlio e collegare uno script alla radice. Inseriresti il tutto nella tua prima `Scene`.
In Defold potresti creare il personaggio a partire da un oggetto di gioco con i componenti `Sprite` e `Script`, per poi inserirlo in una collezione.

![Confronto tra i nodi di Godot e gli oggetti di gioco e i componenti di Defold](images/godot/key_concepts.png)

Il [manuale sugli elementi costitutivi](/manuals/building-blocks/) spiega questi concetti in dettaglio.

### Oggetti di gioco {#game-objects}

In Defold un **oggetto di gioco** è un *contenitore* di componenti dotato di:

- **identità**
- **trasformazione** (posizione, rotazione e scala)

Un oggetto di gioco può svolgere una funzione simile a un `Node2D` o a un `Node3D` di Godot. Defold non prevede un tipo di oggetto distinto per il 2D. Tutti gli oggetti di gioco usano una trasformazione 3D, anche nei giochi 2D.

In Defold puoi assegnare a un oggetto di gioco un altro oggetto come genitore, in modo che ne erediti le trasformazioni. Puoi stabilire queste relazioni in una collezione o cambiarle durante l'esecuzione. L'indirizzo di un oggetto di gioco resta lo stesso anche quando cambia il genitore.

In una collezione puoi definire un oggetto di gioco **incorporato** direttamente nel file `.collection` oppure aggiungere un riferimento a un prototipo `.go` riutilizzabile. Se modifichi la definizione di un oggetto incorporato, modifichi la collezione che lo contiene. Gli altri oggetti definiti indipendentemente mantengono le loro definizioni. Se modifichi un prototipo `.go`, si aggiornano le istanze che vi fanno riferimento, salvo le proprietà ridefinite nelle singole istanze. Più oggetti, anche incorporati, possono condividere le risorse dei componenti tramite riferimenti. Una modifica a una di queste risorse può quindi riguardare tutti gli oggetti che la usano. Se riutilizzi una collezione, le modifiche ai suoi oggetti incorporati si riflettono ovunque sia usata.

### Componenti {#components}

I componenti sono elementi costitutivi specializzati che danno agli oggetti di gioco, per esempio, un aspetto visivo, proprietà fisiche, audio o un comportamento.

Aggiungi un componente `Sprite` per visualizzare un'immagine, un componente `Sound` per riprodurre un suono o un componente `Script` per eseguire codice Lua.

I componenti appartengono agli oggetti di gioco e non possono avere componenti figli. Per costruire una gerarchia, stabilisci relazioni genitore-figlio tra gli oggetti di gioco di una collezione.

In Godot puoi modificare il comportamento di un componente collegandogli uno script. In Defold puoi regolarlo nel pannello Properties oppure creare componenti personalizzati tramite estensioni native, in modo simile alle GDExtension. Alcuni esempi sono i componenti ufficiali [Rive](https://github.com/defold/extension-rive) e [Spine](https://github.com/defold/extension-spine) e quelli realizzati dalla comunità, come [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) e [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation).

In Defold lo script è un componente distinto che puoi aggiungere a qualsiasi oggetto di gioco. Uno stesso oggetto di gioco può avere più componenti, inclusi più script.

I componenti sono organizzati in una struttura priva di gerarchie e sono indipendenti dagli script personalizzati. Grazie a questa progettazione orientata ai dati Defold può disporli in memoria in modo efficiente.

| Nodo di Godot | Componente di Defold | Note |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Visualizza texture 2D e animazioni flipbook a partire da un atlas (una texture che raggruppa più immagini) o da una sorgente di tile. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` ed equivalenti 3D | [Oggetto di collisione](/manuals/physics-objects/) | Gestisce la fisica e i trigger. Le forme di collisione si definiscono direttamente nel componente, anziché in nodi figli separati. Puoi scegliere tra i tipi statico, dinamico, cinematico e trigger. |
| Script `.gd` collegato a un nodo | Script | Contiene il codice Lua che implementa la logica, gestisce l'input e controlla altri componenti e oggetti di gioco. |
| `TileMapLayer` | [Tilemap](/manuals/tilemap/) | Disegna una mappa a griglia usando una sorgente di tile e i livelli della tilemap. |
| `Label` | [Nodo di testo GUI](/manuals/gui-text/) | Usa il testo della GUI per l'interfaccia e un [componente Label](/manuals/label/) per il testo nel mondo di gioco. |
| `AudioStreamPlayer` | [Sound](/manuals/sound/) | Riproduce audio. Puoi impostare Speed, Pan e Gain. |
| `Camera2D` / `Camera3D` | [Camera](/manuals/camera/) | Supporta la proiezione ortografica e quella prospettica. |
| Gerarchia di `Control` / `CanvasLayer` | [GUI](/manuals/gui/) | Il componente GUI contiene una propria gerarchia di nodi (per esempio Box, Text e Pie). La logica della GUI usa uno script `.gui_script` dedicato. |
| `MeshInstance3D` | [Modello](/manuals/model/) o [mesh](/manuals/mesh/) | Il componente Model supporta i contenuti 3D importati. Il componente Mesh permette di usare geometrie personalizzate definite in un buffer. |
| `CPUParticles2D` / `GPUParticles2D` ed equivalenti 3D | [ParticleFX](/manuals/particlefx/) | Emette particelle 2D o 3D configurate nell'editor di particelle di Defold. |
| `PackedScene.instantiate()` | Factory / Collection Factory | In Defold due componenti distinti definiscono quali oggetti di gioco o collezioni possono essere generati durante l'esecuzione. |

### Collezioni e mondi {#collections-and-worlds}

Una **collezione** (collection) descrive gli oggetti di gioco, i loro componenti e le relazioni genitore-figlio. Puoi annidare una collezione in un'altra per riutilizzare un gruppo di oggetti, come faresti con una scena annidata in Godot. Defold non offre un meccanismo generale di ereditarietà delle scene come quello di Godot. Puoi riutilizzare prototipi e collezioni e personalizzare le istanze tramite proprietà o script.

Il file di una collezione non corrisponde a un'entità a runtime. Non esiste un oggetto collezione su cui chiamare metodi, né un nodo radice che corrisponda alla collezione stessa. Il file contiene le definizioni da cui Defold crea gli oggetti di gioco, i componenti e la loro gerarchia durante l'esecuzione.

All'avvio del gioco Defold legge `game.project` e carica la collezione indicata in **Bootstrap ▸ Main Collection**. Nasce così il mondo di gioco iniziale. Anche gli oggetti delle collezioni annidate ne fanno parte.

Il componente **fabbrica di collezioni** (Collection Factory) istanzia un gruppo di oggetti di gioco e i loro componenti nel mondo **già esistente** che contiene la fabbrica.

Il **proxy di collezione** (Collection Proxy) carica invece una collezione separata e crea un **nuovo mondo**, con un proprio spazio di indirizzi e una simulazione fisica indipendente. Tieni presente questa distinzione quando devi, per esempio, generare un nemico in un livello esistente perché interagisca con la sua geometria oppure caricare un livello completamente nuovo, anche in modo asincrono. Vedremo entrambe le operazioni più avanti.

Godot usa `PackedScene` sia per istanziare oggetti sia per cambiare scena. Il cambio di scena tramite `SceneTree` è simile al caricamento di un mondo separato tramite un proxy di collezione.

Ecco un riepilogo:

| Godot | Defold | Note |
|---|---|---|
| `Node3D` con nodi figli | Oggetto di gioco con componenti | I componenti forniscono funzionalità e comportamento. Gli oggetti di gioco forniscono trasformazione e identità. |
| Trasformazione di `Node2D` / `Node3D` | Trasformazione dell'oggetto di gioco | È integrata in ogni oggetto di gioco. |
| Scena / `PackedScene` | Prototipo di oggetto di gioco (`.go`) o collezione (`.collection`) | Un prototipo descrive un singolo oggetto. Una collezione descrive un gruppo di oggetti e la loro gerarchia. |
| `PackedScene.instantiate()` | Fabbrica o fabbrica di collezioni | Crea un oggetto di gioco o un gruppo di oggetti nel mondo corrente e ne restituisce gli identificatori. |
| Cambio di scena tramite `SceneTree` + `PackedScene.instantiate()` | Proxy di collezione | Crea e carica un nuovo mondo separato e genera gli oggetti di gioco al suo interno. |

---

## Scrittura del codice {#code-writing}

L'editor Defold include un editor di testo per tutti i file di testo e gli script. Offre il completamento automatico, la formattazione, la vista Structure con i dati e le funzioni del file e altre funzionalità. Per approfondire, consulta la sezione sull'[uso dell'editor di codice integrato](/manuals/writing-code/#using-the-built-in-code-editor).

Puoi anche aprire tutti gli script e i file di testo di Defold in un editor esterno. Defold include diverse funzioni che ne facilitano l'integrazione e l'uso con strumenti esterni come VS Code. Per maggiori dettagli, consulta la sezione sull'[uso di un editor di codice esterno](/manuals/writing-code/#using-an-external-code-editor).

### Lua e gli script {#lua-and-scripts}

Gli script di gioco di Defold usano Lua. Il linguaggio può ricordare GDScript, ma ci sono alcune differenze importanti. Defold supporta anche Teal, un dialetto di Lua con tipizzazione statica. Come con le GDExtension, puoi usare estensioni native scritte in C, C++, C#, Objective-C, Java o JavaScript a seconda della piattaforma di destinazione. Ne parleremo più avanti.

In Defold lavorerai principalmente con questi file Lua:

| File | Funzione |
|---|---|
| `.script` | Definisce la logica e i comportamenti di gioco. Usa API come `go`, `factory`, `sprite`, `tilemap` o `physics` per controllare gli altri oggetti di gioco e componenti. |
| `.gui_script` | È dedicato alla GUI e ne definisce il comportamento tramite l'API `gui`. |
| `.render_script` | Gestisce il rendering tramite l'API `render`. |
| `.lua` | Contiene moduli Lua riutilizzabili da caricare con `require()`, per esempio librerie di codice o script di utilità. |

Le tabelle Lua possono contenere dati, funzioni o entrambi. Per organizzare il codice non devi ricreare la gerarchia di classi di GDScript. Inserisci la logica riutilizzabile nei moduli e richiamala dallo script che gestisce il comportamento interessato.

Defold usa un ambiente di scripting compatibile con Lua 5.1. Per le differenze tra i linguaggi e i dettagli specifici delle piattaforme, consulta [Lua in Defold](/manuals/lua/).

### Ciclo di vita dell'applicazione {#application-lifecycle}

In generale, un gioco Defold inizia con una fase di inizializzazione e termina con una fase di finalizzazione. Tra queste due fasi, a ogni fotogramma il ciclo di aggiornamento aggiorna le trasformazioni e i componenti, esegue il codice e gestisce i messaggi.

![Ciclo di vita di un'applicazione in Defold](images/application_lifecycle/application_lifecycle.png)

Come in Godot e in altri motori di gioco, gli script di Defold usano funzioni di callback, scritte in Lua, che il motore richiama durante il ciclo di vita dell'applicazione. I nomi cambiano, ma le loro funzioni ti saranno familiari:

| Godot | Defold | Note |
|---|---|---|
| `_ready()` | `init(self)` | Inizializza i dati dell'istanza e, se necessario, acquisisci il focus dell'input. |
| `_process(delta)` | `update(self, dt)` | Esegui l'aggiornamento una volta per fotogramma. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | Esegui l'aggiornamento a intervalli fissi se l'opzione è attiva. |
| `_input(event)` | `on_input(self, action_id, action)` | Gestisci l'input inviato ai componenti dell'oggetto in ascolto. |
| Callback di un segnale | `on_message(self, message_id, message, sender)` | Ricevi messaggi dagli script o dai componenti del motore. |
| `_exit_tree()` | `final(self)` | Esegui le operazioni di pulizia quando viene finalizzata l'istanza dello script. |

Godot chiama `_ready()` sui nodi figli prima di chiamarla sul genitore. Defold non garantisce un ordine di inizializzazione o di aggiornamento tra oggetti di gioco e componenti. Per coordinarli usa i messaggi, senza fare affidamento sul fatto che la funzione `init()` di un particolare oggetto venga eseguita per prima.

Se vuoi usare `fixed_update()`, imposta **Engine ▸ Fixed Update Frequency** in `game.project` su un valore positivo, per esempio 60, e attiva **Physics ▸ Use Fixed Timestep**.

Defold fornisce anche `late_update(self, dt)` per le operazioni da eseguire dopo gli aggiornamenti ordinari e prima del rendering, per esempio regolare una camera. Se necessario, il motore può aggiornare un'ultima volta le trasformazioni dopo questa callback.

Tieni presente che disattivare un componente ed eliminarlo sono operazioni diverse.

Consulta il [manuale sul ciclo di vita dell'applicazione](/manuals/application-lifecycle/) per la sequenza completa e le callback disponibili per ciascun tipo di script.

### Dati di istanza e dati locali {#instance-data-vs-local-data}

Nelle callback ogni istanza di un componente script riceve il proprio `self`, in cui può conservare lo stato dell'istanza, per esempio `self.health` o `self.target`. Anche due componenti script dello stesso oggetto di gioco hanno valori di `self` distinti. `self` è un valore userdata i cui campi sono accessibili come quelli di una tabella, ma non è una tabella Lua. Operazioni come `pairs(self)` quindi non funzionano. In Godot le variabili di istanza (`var`) svolgono una funzione simile.

Godot tratta ogni file `.gd` come la definizione di una classe. Se colleghi un file `.gd` a dieci nemici, Godot crea dieci istanze distinte della classe, ciascuna con la propria copia delle variabili dichiarate al livello più esterno.

Defold esegue il file `.script` come un blocco di codice Lua quando carica la risorsa script. Ogni istanza del componente script riceve il proprio `self` nelle callback del ciclo di vita, come `init(self)` e `update(self, dt)`.

Una variabile locale dichiarata al livello più esterno di un file `.script` di Defold, invece, è condivisa da **tutte le istanze** dello script. In Godot l'equivalente delle variabili locali a livello di file di Defold sono le variabili statiche (`static var`).

![Differenza tra dati di istanza e dati locali in Defold](images/lua/self_local.png)

Nell'esempio qui sopra, impostare `self.has_shield` su `true` per un'istanza non influisce sulle altre. La variabile locale `color` è invece condivisa dalle istanze che usano questo file di script. Modificandola puoi quindi influire su tutte quelle istanze.

### Proprietà {#properties}

Per definire una **proprietà** di istanza modificabile, usa `go.property()`. Puoi accedervi tramite `self`. Come `@export`, rende il valore modificabile nell'editor. In Defold trovi queste proprietà nel pannello `Properties`:

![Proprietà nell'editor Defold](images/script-properties/properties.png)

Per un confronto, ecco il codice **GDScript** di Godot collegato a un `Node3D`:

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

In **Lua** per Defold, in uno script aggiunto come componente:

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

La proprietà Lua è accessibile come `self.speed`. Puoi anche specificarla quando generi un oggetto. Le trasformazioni di Defold usano `vector3` anche in 2D, quindi devi indicare anche la coordinata Z.

Consulta il manuale sulle [proprietà degli script](/manuals/script-properties/) per i tipi di proprietà supportati e quello sugli [script](/manuals/script/) per altri esempi.

---

## Messaggi e indirizzamento {#messages-and-addressing}

I segnali di Godot permettono a un oggetto di annunciare un evento a chi è in ascolto. In Defold gli script comunicano di solito inviando un messaggio all'indirizzo di un oggetto o di un componente.

In Defold puoi inviare un messaggio da qualsiasi script con la funzione `msg.post()` e ricevere e gestire i messaggi nella callback `on_message()` dello script.

![Messaggi in Defold](images/message_passing/messages_overview.png)

Per esempio, il personaggio del giocatore può comunicare una variazione del punteggio all'HUD.

In Godot il nodo `Player` (`Node2D`) usa `player.gd`. Il nodo `GUI` (`CanvasLayer`), che ha lo stesso genitore, usa `gui.gd` e contiene un nodo Label chiamato `ScoreText`:

![Configurazione dei segnali in Godot](images/godot/godot_signals.png)

In Defold l'oggetto di gioco `player` contiene `player.script`. L'oggetto di gioco `hud` contiene un componente `gui` che include un nodo di testo chiamato `score` e usa `hud.gui_script`:

![Configurazione dei messaggi in Defold](images/godot/defold_messages.png)

### Invio dei messaggi {#sending-messages}

In Godot Player e GUI hanno lo stesso genitore. Player collega il segnale `score_changed` a un metodo dello script della GUI, che a sua volta aggiorna il nodo Label.

**GDScript**, `player.gd`:

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

In Godot `Player` definisce un segnale chiamato `score_changed`. Durante `_ready()` lo collega al metodo `set_score()` dello script della GUI. Ogni volta che viene chiamata `collect()`, il punteggio aumenta e il segnale comunica il nuovo valore.

In Defold associa il tasto **Space** all'azione `collect` nelle associazioni di input. L'oggetto `player` inizializza il punteggio in `init()` e richiede il focus dell'input per ricevere gli eventi. Quando viene chiamata `collect(self)`, incrementa il punteggio e invia il messaggio `score_changed` a `/hud#gui`, con il nuovo punteggio nella tabella del messaggio.

**Lua**, `player.script`:

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

In Defold Player non deve collegare un segnale alla GUI in anticipo come in Godot. Invia direttamente il messaggio all'indirizzo del destinatario. Se usi l'indirizzamento relativo di Defold puoi scrivere funzioni e script riutilizzabili.

### Ricezione e gestione dei messaggi {#receiving-and-handling-messages}

La GUI riceve il valore e aggiorna il testo del punteggio.

**GDScript**, `gui.gd`, collegato a `GUI` (`CanvasLayer`):

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

Lo script della GUI riceve il valore emesso tramite `set_score()`, quindi aggiorna il nodo Label figlio `ScoreText`. Player non accede direttamente al nodo Label e non lo modifica.

In Defold lo script della GUI recupera prima il nodo di testo del punteggio con `gui.get_node()`. Quando il componente GUI riceve un messaggio, `on_message()` ne controlla l'identificatore. Se è `score_changed`, lo script legge `message.value` e aggiorna il testo con `gui.set_text()`.

**Lua**, `hud.gui_script`, assegnato al componente GUI:

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

Il destinatario del messaggio di Defold è il **componente** GUI. Il nodo di testo del punteggio non lo riceve direttamente. È lo script della GUI che decide come usare il messaggio e quale nodo di testo aggiornare.

Entrambe le schermate mostrano il testo iniziale `Score: 0`. Quando il punteggio cambia, gli script di esempio sostituiscono l'intero testo con il valore numerico.

`msg.post()` mette il messaggio in coda per la consegna successiva. Non chiama subito il destinatario e non restituisce un risultato dal suo script. I messaggi vengono spesso consegnati nello stesso fotogramma, ma il numero di passaggi di consegna è limitato e una lunga catena di messaggi può proseguire nel fotogramma successivo. Per rispondere, il destinatario può inviare un altro messaggio al mittente originale usando l'URL del mittente fornito a `on_message()`. Trovi i dettagli nella sezione sulle [catene di messaggi](/manuals/message-passing/#message-chains).

C'è un'altra differenza quando hai più destinatari. In Godot puoi collegare un segnale a diversi metodi. All'emissione del segnale, tutti i destinatari collegati ricevono la notifica. In Defold ogni messaggio ha un indirizzo preciso. Per avvisare più destinatari puoi inviare messaggi separati oppure implementare un sistema di sottoscrizione nel gioco.

### Trovare un oggetto con l'indirizzamento di Defold {#finding-an-object-addressing-in-defold}

In Defold non esiste un equivalente generico di `get_node()` che restituisca un oggetto Lua corrispondente a un'altra istanza di script. Usi invece un identificatore o un **URL** nelle chiamate alle API del motore come `go.get_position()`, `go.set()` o `msg.post()`.

In Defold un URL è formato da tre parti:

```lua
socket:/path#component
```

- **Socket**: identifica un mondo, per esempio quello della collezione principale caricata all'avvio o un mondo caricato tramite un proxy di collezione.
- **Percorso**: identifica un oggetto di gioco in quel mondo.
- **Componente**: identifica un componente di quell'oggetto.

Puoi usare l'URL completo oppure ometterne alcune parti per ottenere un indirizzo relativo. Per esempio, a uno script basta la parte relativa al componente per indirizzare un messaggio a un componente dello stesso oggetto di gioco. Ecco alcune forme comuni:

| Indirizzo | Significato |
|---|---|
| `"#sprite"` | Il componente sprite dell'oggetto di gioco corrente. |
| `"/player#controller"` | Il componente controller dell'oggetto player nel mondo corrente. |
| `"level:/player#controller"` | Il componente controller dell'oggetto player nel mondo caricato che si chiama level. |
| `"."` | Forma abbreviata per il `Game Object` corrente. Il messaggio viene consegnato ai suoi componenti. |
| `"#"` | Forma abbreviata per il componente `Script` corrente. |

Le collezioni annidate possono aggiungere prefissi ai percorsi degli oggetti. Assegnare un genitore per ereditarne la trasformazione lascia invariato l'indirizzo dell'oggetto.

Per gli oggetti generati dinamicamente, conserva nel codice gli identificatori restituiti da `factory.create()` o `collectionfactory.create()`.

In Godot puoi usare i gruppi per cercare oggetti nella logica di gioco o per chiamare `call_group()`. Defold non offre un equivalente integrato. Per ottenere lo stesso effetto, crea un registro degli oggetti o gestisci l'inoltro dei messaggi.

In Defold i gruppi fisici degli oggetti di collisione servono a filtrare le collisioni. La maschera definisce con quali gruppi un oggetto può entrare in collisione. Questi gruppi non intervengono nello scambio di messaggi.

Leggi fin dall'inizio i manuali sull'[indirizzamento](/manuals/addressing/) e sullo [scambio di messaggi](/manuals/message-passing/). Rispondono a molte delle domande che sorgono durante il primo progetto.

---

## Autoload e stato condiviso {#autoloads-and-shared-state}

Con i moduli Lua puoi anche chiamare direttamente le funzioni Lua, in alternativa al sistema di messaggi di Defold.

Se in Godot usi un **Autoload** per conservare dati condivisi, in Defold puoi usare un modulo Lua. Salvalo, per esempio, come `modules/game_state.lua` e caricalo con `require "modules.game_state"`.

**GDScript**, con `game_state.gd` registrato come Autoload con il nome `GameState`:

```gdscript
extends Node
var score: int = 0
```

L'equivalente in **Lua**, `modules/game_state.lua`:

```lua
local M = { score = 0 }
return M
```

Un altro script può quindi usare i dati condivisi:

**GDScript**:

```gdscript
func add_point():
    GameState.score += 1
```

**Lua**:

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

La funzione `require()` conserva il modulo nella cache, quindi chi lo carica condivide la tabella restituita. Gli script degli oggetti di gioco, della GUI e di rendering condividono lo stato Lua. Scaricare una collezione caricata tramite proxy non azzera i dati del modulo. Puoi azzerarli esplicitamente all'inizio di una nuova partita.

In Defold un modulo Lua non è un oggetto di gioco e non riceve le callback del ciclo di vita, dei messaggi o dell'input. Se usi un Autoload per eseguire la logica a ogni fotogramma, riprodurre suoni o gestire i cambi di livello, affida queste operazioni allo script di un oggetto della collezione. Puoi anche definire una funzione nel modulo e chiamarla esplicitamente dalle callback del ciclo di vita negli script.

Il modulo Lua `my_module`:

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Lo script Lua:
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Se ti servono dati per ogni istanza, il modulo può restituire una funzione che crea una nuova tabella da memorizzare in `self`. Per maggiori dettagli e indicazioni sull'hot reload, consulta il [manuale sui moduli](/manuals/modules/).

---

## Generare oggetti e caricare livelli {#spawning-objects-and-loading-levels}

### Fabbriche {#factories}

Per generare un singolo oggetto di gioco in Defold, aggiungi un componente **Factory** e imposta **Prototype** sul file `.go` desiderato.

Analogamente, per le collezioni aggiungi un componente **Collection Factory** e seleziona un file `.collection`. La fabbrica genererà un gruppo di oggetti conservando le loro relazioni genitore-figlio.

Nell'esempio di Godot che segue, all'origine della scena c'è un `Node2D` con uno script che istanzia i proiettili:

**GDScript**:

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

Nell'esempio di Defold un oggetto di gioco contiene un componente fabbrica con ID `bullet_factory`. Con la funzione `factory.create()` possiamo chiedergli di generare l'oggetto di gioco a cui fa riferimento la proprietà `Prototype`:

![Configurazione di una fabbrica in Defold](images/godot/defold_factory.png)

Nella schermata la fabbrica viene chiamata in `init()`. Questa funzione mostra come specificare la posizione in cui generare l'oggetto e restituirne l'identificatore:

**Lua**:

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

La funzione di Defold restituisce l'**identificatore** dell'oggetto. Poiché questo valore non espone metodi, passalo alle funzioni di `go` oppure costruisci l'URL di un componente con `msg.url(nil, id, "controller")`, se l'oggetto generato contiene un componente script chiamato `controller`.

Una fabbrica di collezioni restituisce una tabella che associa gli ID degli oggetti del prototipo a quelli delle istanze generate. Conserva la tabella per eliminare gli oggetti in seguito:

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

A differenza di `queue_free()` di Godot, per impostazione predefinita `go.delete(id)` non elimina ricorsivamente i figli. Usa `go.delete(id, true)` per eliminare un oggetto e tutti i suoi discendenti attuali. Se passi la tabella della fabbrica a `go.delete(ids)`, vengono eliminati gli oggetti elencati. Gli altri oggetti aggiunti in seguito come loro figli rimangono. Se invece elimini ricorsivamente un oggetto radice di cui conosci l'ID, elimini anche tutti gli oggetti che in quel momento ne sono discendenti. Consulta [`go.delete()`](/ref/go/#go.delete).

Defold prealloca lo spazio per gli oggetti di gioco e i componenti. Se non riesci a generare un oggetto perché è stato raggiunto un limite, controlla **Collection ▸ Max Instances** e i limiti dei componenti interessati in `game.project`. Aumentando tutti i limiti aumenti anche la memoria utilizzata.

Per le proprietà, le trasformazioni e il caricamento dinamico, consulta i manuali sulle [fabbriche](/manuals/factory/) e sulle [fabbriche di collezioni](/manuals/collection-factory/).

### Proxy di collezione {#collection-proxies}

Per caricare una collezione in Defold, ad esempio per passare a un nuovo livello, aggiungi un componente **Collection Proxy** a un oggetto persistente e imposta la proprietà **Collection** sul file `.collection` desiderato.

![Configurazione di un proxy di collezione in Defold](images/godot/defold_proxy.png)

Invia `"load"` o `"async_load"` con `msg.post()`. Una volta completato il caricamento, il proxy risponde con un messaggio `"proxy_loaded"`. Per inizializzare e avviare il mondo, puoi quindi inviare `"init"` ed `"enable"` alla collezione caricata usando l'indirizzo che on_message riceve nel parametro `sender`.

Decidi così esplicitamente quali mondi caricare e quali eseguire. La scena corrente non viene sostituita automaticamente come accade quando cambi scena in Godot. Per scaricare un'altra collezione e rimuovere il suo mondo, invia un messaggio `"unload"`. Il proxy disattiva e finalizza il mondo prima di scaricarlo, poi risponde con `"proxy_unloaded"`. Puoi anche inviare `"disable"` e `"final"` separatamente se vuoi controllare queste fasi.

Gli oggetti di collisione in mondi caricati da proxy diversi non entrano in collisione tra loro, anche se sono caricati contemporaneamente e sono visibili sullo schermo. Oggetti di gioco e componenti possono comunque scambiarsi messaggi usando URL che includono il socket di destinazione.

Prima di implementare le transizioni, leggi il [manuale sui proxy di collezione](/manuals/collection-proxy/). Spiega come caricare e scaricare un mondo, inoltrare l'input e controllare la frequenza di aggiornamento del mondo caricato.

## Risorse e asset del progetto {#project-resources-and-assets}

Un progetto Defold è una cartella che contiene `game.project`, gli script e le risorse. Il pannello **Assets** rispecchia la struttura della cartella. La maggior parte delle risorse di Defold è definita in file di testo, quindi puoi esaminare le modifiche nel sistema di controllo di versione.

Quando esegui una build del gioco o ne crei un bundle, Defold converte le risorse sorgente nei formati usati a runtime. Le risorse a cui fanno riferimento la collezione principale, le fabbriche e i proxy di collezione formano un albero di dipendenze. Un file che inserisci nella cartella del progetto senza che nulla vi faccia riferimento non verrà incluso nel bundle.

Defold non offre un unico equivalente generico delle classi `Resource` personalizzate e dei file `.tres` di Godot. Usa i tipi di risorsa di Defold per i contenuti gestiti dal motore e tabelle Lua o file di dati per i dati specifici del gioco. Con l'[API `resource`](/ref/resource/) puoi creare o modificare i tipi di risorsa supportati durante l'esecuzione.

Di norma, le risorse di una fabbrica vengono caricate insieme alla fabbrica. Per rimandare il caricamento, attiva **Load Dynamically**. Puoi quindi preparare le risorse in modo asincrono con `factory.load()` o `collectionfactory.load()`. I contenuti di un proxy di collezione vengono caricati su richiesta.

Caricare in un secondo momento contenuti già presenti nel bundle è diverso dallo scaricarli dalla rete. Con [Live Update](/manuals/live-update/) puoi escludere contenuti dal bundle iniziale e distribuirli separatamente.

Per approfondire, consulta il [manuale sulla gestione delle risorse](/manuals/resource/).

---

## Input {#input}

L'equivalente dell'`InputMap` di Godot è il file `.input_binding` di Defold. Qui puoi associare un evento di input (da tastiera, gamepad, mouse, touch o immissione di testo) al nome di un'azione. Seleziona poi il file in **Input ▸ Game Binding** in `game.project`.

![Associazioni di input](images/input/defold_input.png)

In Defold l'oggetto di gioco che deve ricevere l'input deve **acquisire il focus dell'input**. In questo modo entra nello stack dell'input e i suoi componenti script e GUI possono ricevere le callback `on_input()`.

Nella schermata la barra spaziatrice è associata a `collect`. L'esempio che segue è indipendente dal precedente e usa un'azione chiamata `fire`, che devi aggiungere alle associazioni di input:

**GDScript**:

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua**:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

A seconda dell'input, la tabella `action` contiene campi come `pressed`, `released` e `value`.

L'input attraversa lo stack a partire dall'oggetto in ascolto che ha acquisito il focus più di recente. Restituisci `true` da `on_input()` per consumare l'azione, per esempio quando un menu gestisce un clic.

Se il mondo è stato caricato tramite proxy, devono acquisire il focus dell'input sia l'oggetto che contiene il proxy sia gli oggetti in ascolto nel mondo caricato. Se uno script che funzionava smette di ricevere input dopo un cambio di livello, verifica entrambi i passaggi.

Per approfondire, consulta il [manuale sull'input](/manuals/input/), quello su [mouse e touch](/manuals/input-mouse-and-touch/) e quello sui [gamepad](/manuals/input-gamepads/).

---

## Fisica e collisioni {#physics-and-collisions}

L'**oggetto di collisione** (Collision Object) di Defold corrisponde ai corpi fisici di Godot. Riunisce in un unico componente le impostazioni della fisica **e** le forme di collisione. In `game.project` puoi scegliere tra fisica 2D e 3D. Nel manifesto dell'applicazione (App Manifest) puoi anche selezionare la versione del motore fisico o disattivare del tutto la fisica.

Defold offre quattro tipi di oggetti di collisione:

| Godot | Tipo in Defold | Note |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Rimane fermo. Gli oggetti dinamici reagiscono alle collisioni con esso. |
| `RigidBody2D` / `3D` | `Dynamic` | Il motore fisico simula il movimento e risolve le collisioni. |
| `CharacterBody2D` / `3D` | `Kinematic` | Il motore fisico fornisce tutti i dati delle collisioni. Il tuo codice deve reagire e risolverle. |
| `Area2D` | `Trigger` | Segnala solo l'ingresso e l'uscita, senza risposta fisica. |

Un oggetto cinematico di Defold non si comporta esattamente come un `CharacterBody2D` che usa `move_and_slide()`. Defold rileva i contatti e ne invia i dati nel messaggio di risposta alla collisione. Spetta al tuo script implementare il movimento e la risposta al contatto. Per creare un controller del personaggio consulta il [manuale sulla risoluzione delle collisioni](/manuals/physics-resolving-collisions/).

I gruppi e le maschere di collisione usano nomi anziché livelli numerati. Perché venga rilevata una collisione, **ciascun oggetto deve includere nella propria maschera il gruppo dell'altro**.

![Gruppi e maschere di collisione in Defold](images/physics/collision_groups.png)

Nella schermata l'oggetto di gioco chiamato `danger` appartiene al gruppo `player`, mentre l'oggetto `player` appartiene al gruppo `danger`. I nomi dei gruppi possono differire dagli ID degli oggetti e le maschere permettono comunque ai due gruppi di interagire.

Per impostazione predefinita, gli oggetti di collisione inviano i messaggi agli script del proprio oggetto di gioco. Gestisci `"collision_response"`, `"contact_point_response"` o `"trigger_response"` in `on_message()`. I messaggi dei trigger includono il campo `enter` per distinguere l'ingresso dall'uscita. I messaggi di collisione e di contatto possono ripetersi finché gli oggetti si toccano. Non considerare quindi ogni messaggio come un nuovo impatto.

Puoi anche gestire gli eventi fisici con un [listener degli eventi di collisione](/manuals/physics-events/). Devi scegliere quale meccanismo usare. Quando registri un listener, questo sostituisce l'invio predefinito dei messaggi della fisica e gli script smettono di riceverli.

Puoi scegliere tra diverse forme di collisione primitive e complesse. Consulta il [manuale sulle forme di collisione](/manuals/physics-shapes).

![Forma di collisione mesh](images/physics/mesh.png)

Per ulteriori informazioni e per le API, consulta la [panoramica della fisica](/manuals/physics/) e i manuali su [oggetti di collisione](/manuals/physics-objects/), [messaggi di collisione](/manuals/physics-messages/) e [ray cast](/manuals/physics-ray-casts/).

---

## GUI {#gui}

In Defold l'interfaccia utente si realizza in un **componente GUI** creato a partire da un file `.gui`. Al suo interno puoi disporre nodi GUI, per esempio riquadri, testi e settori circolari. Uno script `.gui_script` dedicato controlla il componente, in modo simile a uno script collegato a un `CanvasLayer` di Godot.

Questi nodi appartengono alla GUI e sono indipendenti dalla gerarchia delle trasformazioni dell'oggetto di gioco. Per impostazione predefinita la GUI viene disegnata sopra il gioco e non si sposta con la camera di gioco né con l'oggetto che contiene il componente GUI.

Assegna uno script `.gui_script` per controllare i nodi con `gui.get_node()`, `gui.set_text()` e le altre funzioni di `gui`. L'API `gui` è disponibile soltanto negli script GUI, mentre l'API `go` è riservata agli script degli oggetti di gioco. Per farli comunicare usa i messaggi, come nell'esempio del punteggio.

I modelli GUI ti permettono di riutilizzare la gerarchia dei nodi di un'altra GUI, in modo simile al riutilizzo di un nodo in Godot.

Per costruire le interfacce Defold fornisce nodi molto semplici anziché widget già pronti come Button o i Container di layout di Godot. Per creare un pulsante puoi per esempio combinare un riquadro e un testo, gestire l'input nello script GUI e usare `gui.pick_node()` per verificare se il puntatore si trova sopra il nodo.

Defold supporta anche i **livelli** nella GUI, con una funzione simile ai livelli di `CanvasLayer` in Godot. I livelli di Defold hanno nomi invece di numeri e la loro posizione nell'elenco "Layers" determina l'ordine di disegno.

Ancoraggi, pivot, modalità di adattamento e [layout GUI](/manuals/gui-layouts/) permettono di adattare l'interfaccia a schermi diversi. Ricordano i Container di layout di Godot, ma le loro funzioni non coincidono del tutto.

Per un'interfaccia più estesa o complessa puoi aggiungere codice per gestire layout e widget oppure usare una libreria della comunità come [Druid](https://defold.com/assets/druid/).

Per approfondire, consulta i manuali sulla [GUI](/manuals/gui/) e sugli [script GUI](/manuals/gui-script/).

## Animazione {#animation}

In Defold le animazioni si realizzano con diversi strumenti, anziché con un unico equivalente di `AnimationPlayer`:

- L'**animazione flipbook** riproduce sequenze di immagini sugli sprite e sui nodi Box della GUI.
- L'**animazione dei modelli** riproduce animazioni scheletriche importate sui modelli 3D.
- L'**animazione delle proprietà** interpola valori con `go.animate()` o `gui.animate()`.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** e **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** sono altri formati di animazione disponibili tramite estensioni.

### Tween e animazioni delle proprietà in Defold {#tweens-defold-property-animations}

Una semplice interpolazione (Tween) di Godot si traduce bene in un'animazione di proprietà di Defold. Entrambi gli esempi spostano un oggetto fino a `X = 200` in mezzo secondo:

**GDScript**, su un `Node2D`:

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

**Lua**, in uno script di un oggetto di gioco:

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Per le sequenze che modificano più proprietà, riproducono suoni o attivano eventi di gioco, coordina i passaggi in Lua. Defold non dispone ancora di un editor con una timeline dedicata alle animazioni. Il Curve Editor nel pannello Tools di Defold serve a modificare le curve delle proprietà di ParticleFX durante la vita di una particella.

Consulta i manuali su [animazione](/manuals/animation/), [animazione delle proprietà](/manuals/property-animation/), [animazione flipbook](/manuals/flipbook-animation/) e [animazione dei modelli](/manuals/model-animation/). Nella panoramica trovi anche i link alle estensioni Spine e Rive.

## Tilemap {#tilemaps}

In Defold il componente `Tilemap` usa una **sorgente di tile** che contiene una griglia di tile. Nell'editor di tilemap integrato puoi disegnare i tile su più livelli e, durante l'esecuzione, modificarli con l'API `tilemap`.

La tilemap integrata in Defold usa una griglia rettangolare. Gli insiemi di terreni e le regole per il posizionamento automatico dei tile di Godot non si possono ancora trasferire direttamente in Defold. Puoi ricreare il comportamento che ti serve tramite codice o usare uno strumento esterno per le mappe che consenta l'esportazione in Defold, come [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) o [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold).

Consulta il [manuale sulle tilemap](/manuals/tilemap/).

---

## Pipeline di rendering {#rendering-pipeline}

Defold offre una pipeline di rendering interamente programmabile tramite script, con un file `.render` personalizzato, uno script `.render_script` e il supporto per gli shader. Include una pipeline predefinita adatta alla maggior parte dei giochi.

Lo script di rendering predefinito di Defold gestisce i contenuti 2D e 3D più comuni. Con uno script `.render_script` personalizzato puoi controllare i passaggi di disegno, le destinazioni di rendering e altre operazioni. I tag dei materiali consentono allo script di selezionare gruppi di componenti tramite i predicati di rendering. Defold supporta il rendering PBR fin dall'installazione. La comunità ha inoltre realizzato numerose pipeline di rendering e shader personalizzati.


Defold usa shader GLSL con file separati per i vertex shader e i fragment shader. Godot usa un proprio linguaggio simile a GLSL con funzioni e variabili integrate specifiche del motore. Potresti quindi dover adattare gli shader provenienti da Godot o da altre fonti come Shadertoy. Consulta il [manuale sugli shader](/manuals/shader/) per i requisiti di Defold.

In Defold i **materiali** collegano i vertex program e i fragment program (shader) alle texture, alle costanti e agli attributi degli shader. I materiali predefiniti nella cartella `builtins` sono un buon punto di partenza.

Per modificare il comportamento predefinito, consulta i manuali su [rendering](/manuals/render/), [materiali](/manuals/material/) e [shader](/manuals/shader/).

### Ordine di disegno e livelli {#draw-order-and-layers}

Il valore intero `z_index` di Godot non ha un equivalente diretto tra le proprietà di Defold. Il rapporto tra uno spostamento lungo l'asse Z e la profondità dipende dalla configurazione del rendering. Defold è un motore 3D e usa quindi una vera coordinata spaziale Z, mentre Godot offre un intero dedicato all'ordinamento in 2D.

Con la configurazione ortografica **predefinita** di Defold vengono disegnati solo gli oggetti con una posizione Z compresa tra -1,0 e 1,0. Puoi usare valori decimali come 0,1 o 0,2 per i livelli oppure cambiare l'intervallo inviando un messaggio allo script di rendering. In questo intervallo, con la configurazione predefinita, Defold ordina gli oggetti di gioco o i componenti sprite in base alla loro coordinata Z. Gli elementi con Z maggiore vengono disegnati sopra quelli con Z minore, con un effetto simile a `z_index` in Godot. Il comportamento può cambiare se passi a una camera prospettica o modifichi il file `.render_script`.

I nodi GUI di Defold ignorano la coordinata Z del mondo. Per impostazione predefinita i componenti GUI vengono disegnati in un passaggio separato, dopo gli sprite del mondo. Cambiare la posizione Z di un nodo GUI quindi non ne modifica l'ordine di disegno. Contano l'ordine dei nodi nella gerarchia della GUI (dall'alto verso il basso nel pannello Outline) e i `Layers` della GUI. I livelli hanno la precedenza sull'ordine dei nodi e consentono di raggruppare le chiamate di disegno, in modo simile ai livelli di `CanvasLayer`.

### Camere e coordinate {#cameras-and-coordinates}

Aggiungi un componente `Camera` a un oggetto di gioco. Per spostare la camera, sposta l'oggetto. Scegli la proiezione ortografica per una vista 2D tipica o quella prospettica per il 3D.

Con lo script di rendering predefinito viene usata automaticamente l'ultima camera attivata. Se non ci sono camere, viene usata una vista ortografica 2D. Se ce n'è una sola, viene usata quella. Puoi iniziare con questa configurazione e personalizzare il rendering quando il gioco lo richiede.

La camera determina come le coordinate del mondo vengono proiettate sullo schermo. Quando gestisci l'input del puntatore nel mondo, usa le funzioni di conversione dell'[API Camera](/ref/camera/). Le coordinate del puntatore non coincidono necessariamente con quelle del mondo. Per individuare il nodo GUI sotto il puntatore, per impostazione predefinita si usano comunque le coordinate GUI.

Per la proiezione, lo zoom e la conversione delle coordinate, consulta il [manuale sulla camera](/manuals/camera/).

---

## Esportare un gioco {#exporting-a-game}

In Defold l'esportazione si chiama **creazione del bundle** (bundling). Scegli **Project ▸ Bundle**, seleziona la piattaforma di destinazione e configura le opzioni del bundle. L'editor fornisce tutti gli strumenti di build. Non occorre installare separatamente modelli di esportazione come quelli di Godot.

Il file `game.project` contiene le impostazioni del progetto e delle piattaforme, fra cui la collezione principale, le associazioni di input e le dimensioni dello schermo. Restano validi gli eventuali requisiti di firma e distribuzione degli store e delle piattaforme. I progetti con estensioni native richiedono una connessione di rete per creare un motore personalizzato con il servizio di build nel cloud. In alternativa, puoi configurare manualmente il servizio per lavorare in locale.

Le dimensioni finali del bundle dipendono dagli asset, dalle estensioni e dalle impostazioni di build. Genera un `Build Report` per vedere cosa è incluso nel gioco.

Consulta i manuali su [creazione di bundle](/manuals/bundling/), [impostazioni del progetto](/manuals/project-settings/) e [HTML5](/manuals/html5/). Prova fin dall'inizio un bundle sulla piattaforma di destinazione, soprattutto se usi shader, estensioni native o servizi della piattaforma.

## Librerie ed estensioni {#libraries-and-extensions}

A un progetto Defold puoi aggiungere **dipendenze da librerie** (Library Dependencies) che contengono script e risorse condivisi. Aggiungi gli URL degli archivi in `game.project` e scarica le librerie. Per trovarle, consulta il [Defold Asset Portal](https://defold.com/assets/). Con l'estensione **Asset Store** puoi anche cercare e scaricare asset direttamente nell'editor Defold, come in Godot.

Per personalizzare l'editor, puoi usare **gli script dell'editor e le API per l'interfaccia** per aggiungere comandi, automatizzare attività e creare interfacce su misura. Possono servirti per velocizzare la modifica dei livelli, creare risorse, disporre i tile automaticamente o semplificare altre operazioni frequenti. Coprono alcuni degli usi di `EditorPlugin` e `@tool` di Godot, ma seguono il ciclo di vita e usano l'API `editor` di Defold.

Per estendere il motore oltre le funzionalità offerte da Lua, le **estensioni native** possono rendere disponibile il codice nativo agli script o aggiungere componenti e integrazioni con le piattaforme. Svolgono una funzione simile a GDExtension, con un'API e un processo di build diversi.

Consulta i manuali su [librerie](/manuals/libraries/), [script dell'editor](/manuals/editor-scripts/) ed [estensioni native](/manuals/extensions/).

## Hot reload {#hot-reload}

In Defold puoi usare l'hot reload mentre il gioco è in esecuzione. Esegui la build e avvia il gioco, modifica una risorsa supportata, salvala e scegli **File ▸ Hot Reload** per aggiornarla. L'hot reload funziona anche con una build di debug su un dispositivo selezionato come destinazione.

Quando ricarichi uno script, `init()` non viene eseguita di nuovo. I dati delle istanze esistenti rimangono in memoria, quindi un nuovo valore di inizializzazione non compare automaticamente in `self`. Per aggiornare lo stato esistente usa `on_reload(self)`. Se vuoi ripartire da zero, esegui di nuovo la build. Se un modulo Lua restituisce una nuova tabella quando viene ricaricato, gli altri script che conservano un riferimento alla vecchia tabella continuano a usarla. Per approfondire, consulta il [manuale sui moduli](/manuals/modules/).

Consulta il [manuale sull'hot reload](/manuals/hot-reload/).

## Punti di interruzione e debug {#breakpoints-and-debugging}

Il debugger integrato nell'editor ti permette di impostare punti di interruzione, eseguire il codice passo per passo e ispezionare i valori. Usa la Console per l'output durante l'esecuzione e Build Errors per i problemi di build. Il profiler ti aiuta ad analizzare la durata dei fotogrammi, la memoria e il rendering. I report di build mostrano quanto incide ciascuna risorsa sulle dimensioni del bundle.

Consulta i manuali sul [debug della logica di gioco](/manuals/debugging-game-logic/) e sulla [profilazione](/manuals/profiling/).

## Flussi di lavoro automatizzati {#automated-workflows}

Defold offre diverse interfacce per automatizzare il lavoro o sviluppare con l'assistenza dell'IA. Gli script dell'editor possono automatizzare le operazioni ripetitive, mentre l'API HTTP dell'editor, documentata con OpenAPI, permette a strumenti esterni e agenti IA di esaminare i progetti, eseguire comandi e avviare build. Il servizio HTTP del motore e l'estensione Automation Bridge permettono di ispezionare il gioco durante l'esecuzione, simulare l'input e acquisire schermate. Con questi strumenti gli agenti di programmazione IA come Codex, Claude Code e Cursor possono modificare il progetto, eseguire la build, verificare il comportamento del gioco e correggere i problemi, ripetendo il ciclo secondo necessità.

Per approfondire, consulta i manuali su [automazione](/manuals/automation/), [API HTTP dell'editor](/manuals/editor-http-api/), [servizio del motore](/manuals/engine-service/) e [test automatici](/manuals/automated-testing/).

---

## Errori comuni {#common-pitfalls}

### Trattare una collezione come un nodo radice {#treating-a-collection-as-a-root-node}

Una collezione di Defold descrive gli oggetti di gioco e le loro relazioni, ma non diventa un oggetto radice durante l'esecuzione. Per coordinare gli oggetti di un livello aggiungi un oggetto di gioco con uno script dedicato. Vedi [Collezioni e mondi](#collections-and-worlds).

### Eliminare una gerarchia {#deleting-a-hierarchy}

In Godot `queue_free()` elimina anche i discendenti del nodo. In Defold `go.delete(id)` lascia al loro posto gli oggetti di gioco figli, a meno che tu non richieda l'eliminazione ricorsiva. Nella sezione [Fabbriche](#factories) trovi un esempio e le indicazioni per rimuovere gli oggetti generati da una fabbrica di collezioni.

### Aspettarsi l'ereditarietà delle scene {#expecting-scene-inheritance}

In Defold non puoi ridefinire a piacimento la struttura di una scena derivata come con le scene ereditate di Godot. Puoi riutilizzare prototipi e collezioni e personalizzare le istanze tramite proprietà o script. Vedi [Collezioni e mondi](#collections-and-worlds).

### Chiamare un altro script tramite un riferimento a un oggetto {#calling-another-script-through-an-object-reference}

In Defold l'identificatore di un oggetto di gioco non dà accesso diretto alle funzioni di un'altra istanza di script. Per comunicare tra componenti usa i messaggi oppure inserisci le funzioni condivise in un modulo Lua. Vedi [Messaggi e indirizzamento](#messages-and-addressing) e [Autoload e stato condiviso](#autoloads-and-shared-state).

### Conservare lo stato dell'istanza in una variabile locale a livello di file {#keeping-instance-state-in-a-top-level-local}

Una variabile locale dichiarata al livello più esterno di uno script è condivisa dalle istanze che usano quel file. Se la modifichi per un'istanza, puoi influire anche sulle altre. Conserva lo stato di ogni istanza in `self`, come descritto in [Dati di istanza e dati locali](#instance-data-vs-local-data).

### Dare per scontato che l'input sia attivo automaticamente {#assuming-input-is-enabled-automatically}

In Defold l'oggetto di gioco deve acquisire il focus dell'input prima che i suoi componenti possano ricevere input. Se il mondo è caricato tramite un proxy, anche l'oggetto che contiene il proxy deve acquisire il focus. Per le associazioni, il focus e il funzionamento dello stack dell'input, vedi [Input](#input).

### Aspettarsi che un oggetto cinematico scivoli automaticamente lungo gli ostacoli {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold rileva i contatti degli oggetti di collisione cinematici, ma non fornisce automaticamente il comportamento di `move_and_slide()` di Godot. Lo script deve gestire sia il movimento sia la risposta alle collisioni. Vedi [Fisica e collisioni](#physics-and-collisions).

### Configurare una sola maschera di collisione {#configuring-only-one-collision-mask}

Se solo uno degli oggetti è configurato per interagire con l'altro, la collisione non verrà rilevata. Ciascun oggetto deve includere nella propria maschera il gruppo dell'altro. Vedi [Fisica e collisioni](#physics-and-collisions).

### Copiare le coordinate 2D senza adattarle {#copying-2d-coordinates-unchanged}

L'asse Y di Godot e quello di una tipica configurazione 2D di Defold hanno versi opposti. Copiando il codice di movimento, potresti quindi far muovere gli oggetti nella direzione sbagliata. Anche le coordinate schermo e quelle del mondo possono differire quando c'è una camera. Vedi [Coordinate](#coordinates) e [Camere e coordinate](#cameras-and-coordinates).

### Usare la Z del mondo per ordinare i nodi GUI {#using-world-z-to-sort-gui-nodes}

In Defold la posizione Z di un nodo GUI non ne determina l'ordine di disegno. Usa l'ordine dei nodi nella GUI e i livelli, come descritto in [Ordine di disegno e livelli](#draw-order-and-layers).

### Aspettarsi che l'hot reload riavvii l'oggetto {#expecting-hot-reload-to-restart-the-object}

Quando ricarichi uno script con l'hot reload, `init()` non viene eseguita di nuovo e lo stato dell'istanza può conservare i valori precedenti. Consulta [Hot reload](#hot-reload) per gestire lo stato e il ricaricamento dei moduli.

### Aspettarsi che scaricare un livello azzeri lo stato condiviso {#expecting-a-level-unload-to-clear-shared-state}

Sia lo stato di un Autoload di Godot sia quello di un modulo Lua conservato nella cache possono persistere tra un livello e l'altro. Quando serve, azzera esplicitamente i dati condivisi. Un modulo Lua, a differenza di un nodo Autoload, non riceve automaticamente le callback. Vedi [Autoload e stato condiviso](#autoloads-and-shared-state).

## Come proseguire? {#where-to-go-from-here}

Nel [Defold Learn Hub](https://defold.com/learn/) trovi manuali, esempi, tutorial, video, corsi e altro materiale per muovere i primi passi e approfondire la conoscenza di Defold. Ecco alcune risorse da cui iniziare:

- [Elementi costitutivi](/manuals/building-blocks/)
- [Indirizzamento](/manuals/addressing/)
- [Scambio di messaggi](/manuals/message-passing/)
- [Esempi di Defold](/examples/)
- [Tutorial](/tutorials/)
- [Riferimento API](/ref/go/)

Se hai bisogno di aiuto, chiedi sul [forum di Defold](https://forum.defold.com/) o su [Discord](https://defold.com/discord/). Un piccolo progetto di esempio e una descrizione del comportamento di Godot che vuoi riprodurre aiutano gli altri a darti una risposta.
