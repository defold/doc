---
title: Defold per chi usa Unity
brief: Questa guida ti aiuta a passare rapidamente a Defold se hai già esperienza con Unity. Presenta alcuni dei concetti fondamentali usati in Unity e spiega gli strumenti e i metodi corrispondenti in Defold.
---

# Defold per chi usa Unity {#defold-for-unity-users}

Se hai già esperienza con Unity, questa guida ti aiuta a diventare produttivo in Defold rapidamente. Si concentra sugli aspetti essenziali e rimanda ai manuali ufficiali di Defold quando servono approfondimenti.

## Introduzione {#introduction}

Defold è un motore di gioco 3D completamente gratuito e realmente multipiattaforma, con un editor per Windows, Linux e macOS. Il codice sorgente completo è disponibile su [GitHub](https://github.com/defold/defold/).

Defold punta sulle prestazioni, anche sui dispositivi di fascia bassa. Usa un modello a componenti essenziale, in cui molte interazioni di gameplay vengono gestite tramite codice e scambio di messaggi.

Defold è molto più piccolo di Unity. Con un progetto vuoto, le dimensioni del motore sono comprese tra 1 e 3 MB su tutte le piattaforme. Puoi rimuovere altre parti del motore e spostare alcuni contenuti del gioco in [Live Update](/manuals/live-update) per scaricarli separatamente in un secondo momento. Un confronto delle dimensioni e altri motivi per scegliere Defold sono descritti nella [pagina Perché Defold](https://defold.com/why/).

Per adattare Defold alle tue esigenze, puoi creare o usare versioni già disponibili di:

1. Una pipeline di rendering interamente programmabile tramite script (script di rendering + materiali/shader), con diversi backend tra cui scegliere (OpenGL, Vulkan, ecc.).
2. Codice e componenti sotto forma di estensioni native (C++/C#).
3. Script dell'editor e widget dell'interfaccia per personalizzare l'editor.
3. Una build modificata del motore e dell'editor, poiché sono disponibili il codice sorgente completo e una pipeline di build.

Ti consigliamo anche di guardare un video di Game From Scratch su [Defold per gli sviluppatori Unity](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Installazione {#installation}

1. Scarica Defold per il tuo sistema operativo.
2. Estrai l'archivio e avvialo.

È tutto. Non devi installare hub, SDK aggiuntivi, toolchain o bundle per le piattaforme. Ecco perché diciamo che Defold non richiede alcuna configurazione iniziale.

Se ti servono altri dettagli, leggi questo breve [manuale di installazione](/manuals/install/).

### Versioni {#versions}

Defold viene aggiornato di frequente e non prevede un ramo “LTS”. Ti consigliamo di usare sempre la versione più recente. Le nuove versioni vengono pubblicate regolarmente, di solito ogni mese, con circa due settimane di beta pubblica. Puoi aggiornare Defold direttamente nell'editor.

---

## Schermata iniziale {#welcome-screen}

Defold ti accoglie con una schermata iniziale simile a Unity Hub, da cui puoi aprire i progetti recenti:

![Confronto delle schermate iniziali](images/unity/unity_defold_start.png)

Oppure crearne uno nuovo a partire da:
- `Templates` - progetti vuoti di base per iniziare più rapidamente su una piattaforma o un genere specifici,
- `Tutorials` - percorsi di apprendimento guidati che ti aiutano a muovere i primi passi,
- `Samples` - casi d'uso ed esempi ufficiali o forniti dalla comunità,

![Confronto dei modelli nella schermata iniziale](images/unity/unity_defold_templates.png)

Quando crei il tuo primo progetto e/o lo apri, viene visualizzato nell'editor Defold.

## Ciao mondo {#hello-world}

Ecco un modo per ottenere rapidamente un primo risultato in Defold: segui questi passaggi, poi torna a leggere il resto del manuale.

1. Seleziona un progetto vuoto da `Templates`, assegnagli un nome in `Title`, scegli la posizione e crealo facendo clic su `Create New Project`. Si aprirà nell'editor Defold.
![Ciao mondo, passaggio 1](images/unity/helloworld_1.png)
2. A sinistra, nel pannello `Assets`, apri la cartella `main` e fai doppio clic su `main.collection` per aprirla.
3. A destra, nel pannello `Outline`, fai clic con il pulsante destro su `Collection` e seleziona `Add Game Object`.
![Ciao mondo, passaggio 2](images/unity/helloworld_2.png)
4. Fai clic con il pulsante destro sull'oggetto di gioco `go` appena creato e seleziona `Add Component`, poi `Label`.
![Ciao mondo, passaggio 3](images/unity/helloworld_3.png)
5. Più in basso, a sinistra, nel pannello `Properties`, scrivi qualcosa nella proprietà `Text`.
6. Nella vista centrale principale della scena, trascina l'etichetta e rilasciala in una posizione vicina a `(480,320,0)`, oppure modifica la posizione in `Properties`: `Position`.
![Ciao mondo, passaggio 4](images/unity/helloworld_4.png)
7. Dopo aver cambiato la posizione dell'etichetta, salva il progetto facendo clic su `File` -> `Save All` o usando la scorciatoia <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> su Mac).
8. Crea una build del progetto facendo clic su `Project` -> `Build` o usando la scorciatoia <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> su Mac).
![Ciao mondo, passaggio 5](images/unity/helloworld_5.png)

Hai appena creato la build del tuo primo progetto in Defold e dovresti vedere il testo nella finestra. I concetti di oggetto di gioco e componente dovrebbero esserti già noti. Qui sotto trovi una spiegazione delle collezioni, della vista Outline, delle proprietà e del motivo per cui abbiamo dovuto spostare leggermente l'etichetta in alto a destra.

---

## Panoramica dell'editor Defold {#defold-editor-overview}

Qui presentiamo l'editor Defold dal punto di vista di ciò che potrebbe interessare subito a chi usa Unity, ma ti invitiamo a consultare in seguito il [manuale completo sulla panoramica dell'editor](/manuals/editor).

### Confronto degli editor {#editors-comparison}

La prima differenza che noterai tra Unity e Defold è il layout predefinito dell'editor. Mostriamo l'editor Unity con un layout leggermente modificato per farlo corrispondere a quello predefinito di Defold. Sono affiancati per facilitare il confronto visivo dei pannelli principali, dato che dovresti riconoscere più facilmente le schede di Unity.

![Confronto degli editor](images/unity/defold_unity_editor.png)

Per impostazione predefinita, l'editor Defold si apre con un'anteprima ortografica 2D. Se lavorerai a un progetto 3D o desideri semplicemente un'esperienza più simile a Unity, ti consigliamo di passare dal 2D al 3D disattivando l'opzione `2D` nella barra degli strumenti e di impostare la proiezione prospettica della camera attivando l'opzione `Perspective`:

![Barra degli strumenti di Defold](images/unity/defold_2d.png)

Puoi anche regolare le `Grid Settings` nella barra degli strumenti per usare il piano `Y`, come in Unity:

![Impostazioni 3D di Defold](images/unity/defold_3d.png)

### Panoramica dei pannelli di Defold {#defold-panes-overview}

L'editor Defold è suddiviso in 6 pannelli principali.

![Editor 2](images/editor/editor_overview.png)

Di seguito trovi un confronto dei nomi usati in Defold e delle differenze funzionali:

| Defold | Unity | Differenze |
|---|---|---|
| 1. Assets | Project (Assets Browser) | In Defold il pannello Assets è ancorato a sinistra. Defold non crea file `meta`. |
| 2. Main Editor | Scene View | L'editor Defold si adatta al contesto (editor diversi per tipi di file diversi), mentre Unity usa finestre specializzate separate (per esempio Animator e Shader Graph). Defold dispone anche di un editor di codice integrato. |
| 3. Outline | Hierarchy | Defold mostra soltanto il file attualmente aperto o l'elemento selezionato (oggetto di gioco o componente), anziché una gerarchia globale. |
| 4. Properties | Inspector | Defold mostra soltanto le proprietà della **selezione corrente** nella vista Outline, anziché quelle di tutti i componenti dell'oggetto di gioco. |
| 5. Tools | Console | Defold mette a disposizione strumenti in schede come Console, Curve Editor, Build Errors, Search Results, Breakpoints e Debugger. |
| 6. Changed Files | Unity Version Control (Plastic) | In Defold, una volta integrato Git nel progetto, i file modificati vengono mostrati qui. Puoi comunque usare Git esternamente. |

Altri nomi utili relativi all'editor:

| Defold | Unity | Differenze |
|---|---|---|
| Game Build | Game Preview | Mostra il gioco in esecuzione, creato con il motore. Defold può eseguire più istanze del gioco dall'editor, in modo simile a Multiplayer Play Mode di Unity 6+. In Defold il gioco viene sempre eseguito in una finestra separata, non ancorata. Defold può anche eseguire il gioco su un dispositivo esterno (per esempio un telefono), in modo simile a Unity Remote. |
| Tabs | Tabs | Defold permette di modificare contenuti affiancati in due pannelli all'interno della vista Main Editor. Le schede e i pannelli sono ancorati all'interno di un'unica finestra dell'editor; puoi attivare e disattivare la visibilità dei pannelli (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>) e regolarne le dimensioni. |
| Toolbar | Toolbar / Scene View Options | Soltanto nelle versioni più recenti di Unity gli strumenti di trasformazione sono stati spostati nella vista Scene, in modo simile a Defold. |
| Console | Console | La Console di Defold non può essere separata dalla finestra. Gli errori di build in Defold compaiono in una scheda dedicata, `Build Errors`. |
| Build Errors | Errori di compilazione nella Console | Gli script Lua sono interpretati, quindi non ci sono errori di compilazione. Il progetto viene però sottoposto a una build, durante la quale possono verificarsi alcuni errori. Defold usa anche un Lua Language Server per l'analisi statica degli script. |
| Search Results | Search / Project Search | Defold non dispone di filtri per tipi ed etichette. |
| Curve Editor | Unity Curve Editor | Il Curve Editor di Defold permette di modificare soltanto le curve delle proprietà degli effetti particellari. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Il debugger è completamente integrato in Defold fin dall'installazione. Una scheda aggiuntiva permette di tenere traccia dei punti di interruzione e di attivarli e disattivarli. |

---

## Concetti fondamentali {#key-concepts}

A un livello sufficientemente generale, i concetti fondamentali alla base della maggior parte dei motori di gioco sono molto simili. Servono ad aiutare gli sviluppatori a creare giochi più facilmente, come se assemblassero blocchi, mentre il motore gestisce autonomamente le operazioni complesse e specifiche delle piattaforme.

### Elementi costitutivi {#building-blocks}

Defold si basa su pochi elementi fondamentali:

![Elementi costitutivi](images/unity/blocks.png)

Per maggiori dettagli, consulta il manuale completo sugli [elementi costitutivi di Defold](/manuals/building-blocks/).

### Oggetti di gioco {#game-objects}
Defold usa gli **"oggetti di gioco" (game object)**, in modo simile a Unity. In entrambi i motori, gli oggetti di gioco sono contenitori di dati con un ID e hanno tutti una trasformazione: posizione, rotazione e scala. In Defold, però, la trasformazione è integrata anziché essere un componente separato.

Puoi creare relazioni genitore-figlio tra gli oggetti di gioco. In Defold puoi farlo soltanto nell'editor all'interno di una "collezione" (spiegata più avanti) oppure dinamicamente in uno script. Gli oggetti di gioco non possono contenere altri oggetti di gioco annidati come avviene in Unity.

### Componenti {#components}
In entrambi i motori, gli oggetti di gioco possono essere estesi con **"componenti" (component)**. Defold fornisce un insieme minimo di componenti essenziali. La distinzione tra 2D e 3D è meno marcata rispetto a Unity (per esempio per i collider), quindi nel complesso ci sono meno componenti e potresti sentire la mancanza di alcuni di quelli di Unity.

#### Componenti di comportamento {#behaviour-components}

In Unity, "componente" indica di solito un `MonoBehaviour` collegato a un `GameObject`. Puoi crearne uno ereditando da `MonoBehaviour` oppure usare i componenti integrati, come Light, quelli relativi alla fisica e così via.

In Defold, "componente" si riferisce esclusivamente a ciò che corrisponderebbe ai componenti integrati di Unity o a elementi analoghi, ma Defold non tratta uno script come un MonoBehaviour e non richiede alcuna "marcatura" esplicita per collegarlo a un oggetto di gioco, a parte la creazione di funzioni che ricevono eventi o callback.

Il comportamento di gameplay personalizzato di solito non viene aggiunto sotto forma di tanti componenti script separati sullo stesso oggetto di gioco. Viene invece comunemente implementato in moduli Lua usati da un unico `.script` di coordinamento, oppure gestito da uno script di sistema più ampio che controlla molti oggetti. La sezione Scrittura del codice più avanti approfondisce questo aspetto.

Leggi altri dettagli sui [componenti di Defold](/manuals/components/).

La tabella seguente presenta i componenti Unity simili per un rapido confronto, con i link al manuale di ciascun componente Defold:

| Defold | Unity | Differenze |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | In Defold puoi cambiare la tinta (proprietà del colore) soltanto tramite codice. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold dispone di un editor di tilemap integrato che supporta griglie quadrate (ma esistono estensioni, per esempio per [Hexagon](https://github.com/selimanac/defold-hexagon/)) e non ha regole integrate per il posizionamento automatico dei tile. Strumenti come [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) o [Sprite Fusion](https://defold.com/assets/spritefusion/) offrono opzioni di esportazione per Defold. |
| [Label](/manuals/label/) | Text / TextMeshPro | Da Defold 1.13.2, i componenti Label e i nodi di testo GUI supportano il [markup del testo formattato](/manuals/font-richtext/) integrato per colori, gradienti, contorni ed effetti animati. È disponibile anche un'[estensione RichText](https://defold.com/assets/richtext/) separata. |
| [Sound](/manuals/sound/) | AudioSource | Defold dispone soltanto di una sorgente sonora globale (non spaziale). È disponibile un'[estensione FMOD](https://github.com/defold/extension-fmod) ufficiale per Defold. |
| [Fabbrica](/manuals/factory/) | Prefab Instantiate() | In Defold una fabbrica (factory) è un componente con un prototipo specifico (prefab). |
| [Fabbrica di collezioni](/manuals/collection-factory/) | - (Nessun componente direttamente equivalente) | Un componente fabbrica di collezioni (collection factory) in Defold può generare contemporaneamente più oggetti di gioco con relazioni genitore-figlio. |
| [Oggetto di collisione](/manuals/physics-objects) | Rigidbody + Collider | In Defold gli oggetti fisici e le forme di collisione sono riuniti in un unico componente. |
| [Forme di collisione](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | In Defold le forme (parallelepipedo, sfera, capsula) si configurano all'interno del componente oggetto di collisione. Entrambi supportano forme di collisione ricavate da tilemap e dati di inviluppi convessi. |
| [Camera](/manuals/camera/) | Camera | In Unity la camera ha più impostazioni integrate per il rendering e la post-elaborazione, mentre Defold affida la loro personalizzazione all'utente tramite lo script di rendering. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | La GUI di Defold è un componente potente per creare interfacce e modelli completi. Unity non ha un singolo componente UI equivalente, ma diversi framework per le interfacce. Defold dispone anche di un'[estensione](https://github.com/britzl/extension-imgui). |
| [Script GUI](/manuals/gui-script/) | Script Unity UI / uGUI | La GUI di Defold può essere controllata tramite script GUI usando l'API dedicata `gui`. |
| [Modello](/manuals/model/) | MeshRenderer + Material | In Defold un componente modello riunisce un file di modello 3D, le texture e un materiale con shader. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Mesh procedurale | In Defold Mesh è un componente per gestire un insieme di vertici tramite codice. È simile a un modello Defold, ma opera a un livello ancora più basso. |
| [ParticleFX](/manuals/particlefx/) | Particle System | L'editor di particelle di Defold supporta effetti particellari 2D/3D con molte proprietà e permette di animarle nel tempo mediante curve nel Curve Editor. Non dispone di scie o collisioni. |
| [Script](/manuals/script/) | Script | Le differenze di programmazione sono spiegate più in dettaglio di seguito. |

#### Estensioni e componenti personalizzati {#extensions-and-custom-components}

Defold dispone anche di componenti ufficiali [Spine](/extension-spine/) e [Rive](/extension-rive/) disponibili tramite estensioni.

Puoi anche creare [componenti personalizzati](https://github.com/defold/extension-simpledata) usando le estensioni native, come questo [componente di interpolazione degli oggetti](https://github.com/indiesoftby/defold-object-interpolation) creato dalla comunità.

Alcuni componenti di Unity non hanno un equivalente già incluso in Defold, per esempio Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth o Animator. Tuttavia, tutte queste funzionalità possono essere implementate negli script e sono già disponibili alcune soluzioni: per esempio diverse pipeline di illuminazione, il componente Mesh per generare mesh arbitrarie (compresi i terreni) o [Hyper Trails](https://defold.com/assets/hypertrails/) per effetti di scia personalizzabili. In futuro Defold potrebbe anche aggiungere nuovi componenti integrati, come le luci.

### Risorse {#resources}

Alcuni componenti richiedono **"risorse" (resource)**, in modo simile a Unity: per esempio, sprite e modelli hanno bisogno di texture. La tabella seguente ne confronta alcune:

| Defold | Unity | Differenze |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold dispone anche di un'[estensione per Texture Packer](https://defold.com/extension-texturepacker/). |
| [Sorgente di tile](/manuals/tilesource/) | Tile Palette + Asset | In Defold una sorgente di tile può essere usata come texture per le tilemap, ma anche per sprite o particelle. |
| [Font](/manuals/font/) | Font | Usato dal componente Label di Defold o dai nodi di testo della GUI, in modo simile a Text/TextMeshPro in Unity. |
| [Materiale](/manuals/material/) | Material | In Defold gli shader prendono il nome di vertex program e fragment program. |

### Collezione e scena a confronto {#collection-vs-scene}

In Defold gli oggetti di gioco e i componenti possono essere inseriti in file separati, come i prefab di Unity, oppure definiti insieme in un file di **"collezione" (collection)**.

Una collezione in Defold è essenzialmente un file di testo che contiene una descrizione statica della scena. **Non** è un oggetto a runtime. Definisce soltanto quali oggetti di gioco devono essere istanziati nel gioco e come devono essere stabilite le relazioni genitore-figlio tra questi oggetti.

#### Mondi di gioco {#game-worlds}

Per impostazione predefinita, le scene di Unity condividono lo stesso stato globale del gioco e la stessa simulazione fisica: in pratica, lo stesso *mondo* (*mondo di gioco*). In Defold hai due possibilità:
1. Istanziare oggetti di gioco da un singolo file di oggetto di gioco tramite una `Factory` o da un file di collezione tramite una `Collection Factory` in un determinato *mondo* già istanziato, come con i prefab.
2. Creare un *mondo* di gioco separato durante l'esecuzione, con i propri oggetti di gioco, mondo fisico, operazioni del motore e namespace di indirizzamento, tramite una collezione caricata all'avvio o tramite un componente `Collection Proxy`.

Anche i componenti fabbrica e proxy sono spiegati più avanti.
Leggi altri dettagli sulle collezioni nel [manuale degli elementi costitutivi](/manuals/building-blocks/#collections).

---

## Risorse e asset del progetto {#project-resources-and-assets}

Unity e Defold memorizzano entrambi i contenuti del gioco nella directory del progetto, ma differiscono nel modo in cui tengono traccia degli asset e li preparano.

### Asset {#assets}

Unity conserva gli asset in `Assets/` e genera file `.meta`. Defold non ha file meta. In Defold il progetto è semplicemente la struttura delle tue cartelle, esattamente come sul disco, e il pannello `Assets` la rispecchia sempre.

### Formati delle risorse {#resource-formats}

Unity importa gli asset e li converte in altri formati dietro le quinte. In Defold lavori direttamente con le risorse sorgente (`.png`, `.gltf`, `.wav`, `.ogg`, ecc.) e le assegni ai `Components`.

Unity può usare una singola immagine come sprite. In Defold le immagini possono essere usate direttamente per modelli e mesh, mentre sprite, GUI, tilemap e particelle richiedono un atlas (texture raggruppate) o una sorgente di tile (tile disposti su una griglia).

La maggior parte delle risorse di Defold viene memorizzata come testo, facilitando l'uso del controllo di versione.

### Cache delle librerie {#library-cache}

Unity genera una cartella `Library/` per gli asset importati. Defold non ha una directory di questo tipo: gli asset vengono elaborati durante le build e i risultati vengono conservati nella cache sotto la cartella di build (con cache di build locali o remote opzionali).

---

## Scrittura del codice {#code-writing}

L'equivalente degli script `MonoBehaviour` in Defold è il componente Script, ma ci sono alcune differenze che vale la pena conoscere.

### Lua

Gli script di Defold sono scritti in [Lua](https://www.lua.org/), un linguaggio a tipizzazione dinamica che supporta più paradigmi.

Esistono diversi tipi di script Lua: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` e i moduli `*.lua`.

### Teal

Defold supporta l'uso di transpiler che generano codice Lua, come [Teal](https://teal-language.org/), un dialetto di Lua a tipizzazione statica, ma questa funzionalità è più limitata e richiede una configurazione aggiuntiva. I dettagli sono disponibili nel [repository dell'estensione Teal](https://github.com/defold/extension-teal).

### Estensioni native C++/C# {#cc-native-extensions}

In Defold le estensioni native possono essere scritte in diversi altri linguaggi: C, C++, C#, Objective-C, Java o JS, a seconda della piattaforma di destinazione. Se hai molta dimestichezza con C#, è tecnicamente possibile organizzare gran parte della logica del gioco in un'estensione C# e richiamarla da un piccolo script Lua di bootstrap, anche se questo richiede una conoscenza avanzata dell'API ed è sconsigliato ai principianti.

Leggi altri dettagli sulle estensioni nel [manuale delle estensioni native di Defold](/manuals/extensions/).


### Dai MonoBehaviour ai moduli Lua {#from-monobehaviours-to-lua-modules}

Unity ha un modello di scripting aperto. Poiché `MonoBehaviour` è il modo principale per aggiungere comportamenti nell'editor, molti progetti Unity iniziano con uno script di tipo controller per ogni oggetto di gioco importante: `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager` e così via.

Defold è più specifico riguardo alla sua architettura predefinita. Un oggetto di gioco può avere uno `.script`, ma raramente è necessario creare uno script per ogni oggetto di gioco: un singolo script in Defold può controllare centinaia o migliaia di altri oggetti e dei loro componenti, anche se non hanno alcuno script, grazie ai potenti sistemi di indirizzamento e scambio di messaggi di Defold. Creare uno script per ogni oggetto di gioco è raramente necessario e può introdurre una complessità controproducente.

Per ottenere comportamenti di gameplay riutilizzabili, gli sviluppatori Unity spesso passano alla composizione: script `MonoBehaviour` più piccoli, come `Health.cs`, `Attack.cs` o `EnemyFinder.cs`, collegati allo stesso oggetto di gioco. In Defold, di solito mantieni un solo `.script` collegato come contenitore o coordinatore e inserisci la logica riutilizzabile in normali moduli Lua.

In Unity questa composizione potrebbe avere il seguente aspetto:

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

In Defold le stesse responsabilità sono spesso suddivise tra un unico script collegato e moduli riutilizzabili:

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

Lo `.script` collegato diventa il contenitore o coordinatore. I moduli Lua contengono logica riutilizzabile, in modo simile ai piccoli script `MonoBehaviour` che in Unity spesso si occupano di una singola responsabilità.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

La differenza importante non è che Defold impedisca un'architettura modulare: riguarda il punto in cui avviene la composizione e il modo in cui il codice di gameplay comunica:

| Unity | Defold |
|---|---|
| Collega diversi script `MonoBehaviour` nell'Inspector | Collega un unico `.script` e componi i moduli Lua nel codice |
| Usa `GetComponent<T>()` o campi serializzati per collegare i comportamenti | Memorizza le istanze dei moduli in `self` e usa indirizzi e messaggi tra gli oggetti |
| Ogni componente può avere i propri metodi del ciclo di vita | Lo script coordinatore inoltra `init()`, `update()`, `on_message()`, `final()`, ecc. |
| Sono possibili molti stili architetturali | La pratica comune è la composizione esplicita nel codice, orientata ai messaggi |

All'inizio può sembrare insolito, soprattutto se sei abituato a configurare i comportamenti aggiungendo componenti nell'Inspector. In Defold molti degli elementi che potresti configurare visivamente in Unity possono invece essere creati, collegati, attivati, disattivati o aggiornati tramite codice. Il sistema di messaggistica di Defold aiuta a disaccoppiare la logica: il mittente invia dati a un indirizzo e il destinatario decide che cosa farne.

Questo approccio, pur essendo consigliato, non è obbligatorio e puoi comunque scrivere gli script come preferisci, anche collegando più script a un oggetto di gioco o avvicinandoti a uno stile di programmazione orientato agli oggetti. Esistono persino librerie che possono aiutarti a farlo ([defold-oop](https://github.com/xiyoo0812/defold-oop) o [lua-class](https://github.com/d954mas/lua-class)).

Quando hai molti oggetti dello stesso tipo, come proiettili, nemici, particelle, tile o semplici elementi interattivi, spesso è meglio controllarli da uno script di sistema o di gestione anziché assegnare uno script separato a ogni oggetto. Usa script per singolo oggetto quando un oggetto ha uno stato e un comportamento propri significativi. Usa i moduli quando vuoi logica riutilizzabile. Usa gli script di sistema quando un solo script può controllare molti oggetti in modo efficiente.

Trovi [qui](https://defold.com/examples/factory/spawn_manager/) un esempio che mostra come usare le proprietà degli script, le fabbriche, l'indirizzamento e i messaggi di Defold per controllare più unità.

Manuali utili sulla scrittura del codice:
- [Manuale degli script](/manuals/script/)
- [Scrittura del codice](/manuals/writing-code/)
- [Debug](/manuals/debugging/)


### Editor di codice integrato {#built-in-code-editor}

L'editor Defold include un editor di codice integrato con completamento del codice, evidenziazione della sintassi, consultazione rapida della documentazione, analisi del codice e un debugger integrato.

![Editor di codice di Defold](/images/editor/code-editor.png)

### VS Code e altri editor {#vs-code-and-other-editors}

Se preferisci, puoi comunque usare il tuo editor esterno. Tutti i componenti di Defold e i file correlati sono in formato testuale, quindi puoi modificarli con qualsiasi editor di testo, ma devi rispettare la formattazione e la struttura degli elementi corrette, poiché si basano su Protobuf.

Se sei abituato a VS Code e vuoi usarlo per scrivere il codice del gioco, ti consigliamo di installare [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) o [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) dal Visual Studio Marketplace.

Puoi anche configurare le preferenze dell'editor Defold per aprire i file di testo in VS Code (o in qualsiasi altro editor esterno) per impostazione predefinita. Consulta le [preferenze dell'editor](/manuals/editor-preferences/) per i dettagli.

### Shader - GLSL {#shaders-glsl}

Defold usa GLSL (OpenGL Shading Language) per gli shader, ovvero `Vertex Programs` e `Fragment Programs`, in modo simile a Unity. Sebbene Defold non offra uno Shader Graph come Unity (il che può essere uno svantaggio), puoi comunque creare shader equivalenti scrivendo codice.

Leggi altri dettagli sugli shader nel [manuale degli shader](/manuals/shader).

#### Materiali {#materials}

Defold usa il concetto di `Material` per collegare shader `.fp` e `.vp`, campionatori (texture) e altri elementi come attributi dei vertici o costanti.

Leggi altri dettagli sui materiali nel [manuale dei materiali](/manuals/material).

---

## Sistema di messaggistica {#messaging-system}

In Defold gli oggetti non conservano riferimenti diretti l'uno all'altro. Non esistono `GetComponent`, chiamate a metodi tra script di oggetti diversi o un accesso globale alla scena come in Unity.

Gli script comunicano invece tramite scambio di messaggi: invii messaggi ad altri script anziché chiamare metodi o accedere direttamente ai componenti. Spetta agli oggetti destinatari decidere che cosa fare con i messaggi.

All'inizio può sembrare poco familiare, ma favorisce un accoppiamento debole e riduce le interdipendenze strette.


### Invio di un messaggio {#sending-a-message}

In Unity la comunicazione ha di solito questo aspetto:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Gli oggetti possono quindi fare riferimento direttamente l'uno all'altro e chiamare metodi su altri script. Tutto esiste in un unico spazio di scena condiviso.

In Defold invii un messaggio da uno script a un altro script (o a un altro componente):

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

E puoi gestire questi messaggi nello script:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Per ora ignora `#` e `hash`: ci torneremo più avanti. Il resto dovrebbe essere chiaro. Puoi inviare un messaggio a qualsiasi componente (anche allo stesso script) di qualsiasi oggetto di gioco istanziato.

#### Componenti diversi dagli script {#components-other-than-scripts}

A volte invii messaggi, per esempio, ai componenti `Sprite` o `Collision` per attivarli o disattivarli. A volte sono i `Components` a inviare messaggi al tuo script, per esempio quando si verifica una collisione, in modo che tu possa gestirla. Defold usa internamente lo stesso sistema di messaggistica per gli eventi del motore e per la comunicazione di gameplay. 

Il sistema di messaggistica è in parte simile a SendMessage di Unity o ai sistemi a eventi, anche se l'indirizzamento e le convenzioni sono diversi.

Puoi leggere altri dettagli nel [manuale dello scambio di messaggi](/manuals/message-passing/).

### Indirizzamento {#addressing}

Gli oggetti e i componenti in Defold sono identificati da indirizzi, chiamati URL.

Ogni oggetto e componente istanziato ha un proprio indirizzo univoco e non devi attraversare un grafo della scena per trovarli. Questo rende l'indirizzamento esplicito e diretto.

Un semplice URL in Defold potrebbe avere questo aspetto:
```lua
"/player"
```

È *concettualmente* simile a:
```c#
GameObject.Find("player")
```

Ora è il momento di spiegare perché negli indirizzi venivano usati `"/"` o `"#"`.

Un URL di Defold (simile a un [URL](https://en.wikipedia.org/wiki/URL)) è composto da tre parti:

```yaml
socket: /path #fragment
```

oppure, usando una terminologia più vicina a quella di Defold:

```yaml
collection: /gameobject #component 
```
Gli spazi nelle descrizioni qui sopra servono soltanto a separare visivamente le 3 parti.

In termini semplici:
1. `collection:` identifica il contesto della collezione, con `:` alla fine.
2. `/path` identifica l'oggetto di gioco, con `/` prima dell'ID.
3. `#fragment` identifica il componente specifico dell'oggetto (come uno script, uno sprite o un componente di collisione), con `#` prima dell'ID.

#### Indirizzo statico {#static-address}

Questi identificatori vengono stabiliti alla creazione di ciascun elemento e non cambiano mai, anche se modifichi le relazioni genitore-figlio. Puoi impostarli nella proprietà `Id` nei file oppure ottenerli durante l'esecuzione dalle chiamate a `factory.create` o `collectionfactory.create`, al momento dell'istanziazione.

#### Indirizzamento relativo {#relative-addressing}

Non devi sempre usare un URL completo.

Se invii messaggi all'interno della stessa collezione (lo stesso *mondo*), puoi omettere la parte relativa al socket:

```yaml
/gameobject #component
```
Se invii messaggi a un componente all'interno dello stesso oggetto di gioco, puoi omettere anche la parte relativa all'oggetto di gioco:

```yaml
#component
```

Due abbreviazioni utili sono:
- `#` per inviare a questo componente *Script*
- `.` per inviare a tutti i componenti di questo *oggetto di gioco*

L'indirizzamento relativo e le abbreviazioni ti permettono di scrivere URL riutilizzabili in contesti e oggetti di gioco diversi senza specificare percorsi completi.

### Messaggi alla GUI e al rendering {#messaging-to-gui-and-render}

Poiché Defold separa il mondo della GUI da quello degli oggetti di gioco, puoi anche inviare messaggi dai `.scripts` degli oggetti di gioco ai `.gui_scripts`.

Puoi anche inviare messaggi a namespace di sistema speciali usando un identificatore che inizia con `@`. Per esempio, il sistema di rendering è raggiungibile tramite `@render`: e puoi sfruttarlo per controllare alcune funzionalità di rendering integrate, come cambiare la proiezione nello script di rendering predefinito:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Trovi altri dettagli nel [manuale dell'indirizzamento](/manuals/addressing/).

---

## Prefab e istanze {#prefabs-and-instances}

Unity può istanziare qualsiasi elemento della scena in modo statico o dinamico e Defold può fare lo stesso. In Unity prendi un prefab e chiami `Instantiate(prefab)`. In Defold hai 3 componenti per istanziare i contenuti:

- `Factory` - istanzia un **singolo oggetto di gioco** da un prototipo specificato: un file `*.go` (prefab).
- `Collection Factory` - istanzia un **insieme di oggetti di gioco** con relazioni genitore-figlio da un prototipo specificato: un file `*.collection`.
- `Collection Proxy` - **carica** e istanzia un nuovo *mondo* da un file `*.collection`.

### Fabbrica {#factory}

Una volta definito un componente `Factory` con la proprietà `Prototype` impostata sul file di oggetto di gioco appropriato, per generare un'istanza basta chiamare nel codice:

```lua
factory.create("#my_factory")
```

La chiamata usa l'indirizzo del componente, in questo caso un percorso relativo con l'identificatore `"#my_factory"`.

Restituisce l'identificatore dell'istanza appena creata, quindi, se dovrai usarlo in seguito, conviene memorizzarlo in una variabile:

```lua
local new_instance_id = factory.create("#my_factory")
```

Ricorda che in Defold non devi gestire manualmente un pool di oggetti: il motore esegue già il pooling internamente.

Consulta altri dettagli nel [manuale delle fabbriche](/manuals/factory/). 

### Fabbrica di collezioni {#collection-factory}

La differenza tra i componenti `Factory` e `Collection Factory` è che una fabbrica di collezioni può generare **più** oggetti di gioco contemporaneamente, stabilendo alla creazione le relazioni genitore-figlio definite nel file `*.collection`.

Questa distinzione non esiste in Unity, che non ha un concetto dedicato corrispondente alla fabbrica di collezioni di Defold. L'analogia più vicina è semplicemente un prefab annidato che contiene una gerarchia di oggetti.

Restituisce una **tabella** con gli ID di tutte le istanze generate:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Consulta altri dettagli nel [manuale delle fabbriche di collezioni](/manuals/collection-factory/).

#### Proprietà personalizzate delle istanze {#custom-properties-of-instances}

Quando chiami `factory.create()` o `collectionfactory.create()`, puoi anche specificare parametri opzionali come posizione, rotazione, scala e proprietà dello script, per controllare esattamente come e dove appare l'istanza e come si comporta, per esempio:

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

L'ordine degli argomenti opzionali prevede prima le proprietà e poi la scala. Usa un `vector3` con Z impostato esplicitamente a `1.0` quando vuoi scalare soltanto gli assi X e Y di un oggetto 2D; una scala numerica viene applicata in modo uniforme a tutti e tre gli assi.

#### Caricamento dinamico {#dynamic-loading}

Sia nei componenti `Factory` sia nei componenti `Collection Factory` puoi contrassegnare un prototipo per il caricamento dinamico delle risorse, in modo che i suoi asset più pesanti vengano caricati in memoria soltanto quando servono e scaricati quando non sono più in uso.

Consulta altri dettagli nel [manuale della gestione delle risorse](/manuals/resource/). 

### Proxy di collezione {#collection-proxy}

Il componente `Collection Proxy` fa riferimento a uno specifico file `*.collection`, ma anziché inserire gli oggetti nel *mondo corrente* (come le fabbriche), **carica e istanzia un nuovo mondo di gioco**. È in parte simile al caricamento di un'intera scena in Unity, ma con una separazione più rigorosa.

In Unity potresti caricare una scena in modalità additiva in questo modo:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

In Defold carichi la nuova collezione semplicemente inviando un messaggio al componente `Collection Proxy`:

```lua
msg.post("#myproxy", "load")
```

1. Quando invii al proxy un messaggio `"load"` (o `"async_load"` per il caricamento asincrono), il motore alloca un nuovo mondo, vi istanzia tutti gli elementi della collezione e lo mantiene isolato.
2. Una volta completato il caricamento, il proxy invia in risposta un messaggio `"proxy_loaded"` per indicare che il mondo è pronto.
3. Di solito invii poi i messaggi `"init"` ed `"enable"`, affinché gli oggetti di quel nuovo mondo inizino il loro normale ciclo di vita.

Per comunicare tra i mondi caricati devi usare messaggi espliciti con URL che includano il nome del mondo (`collection:`, la prima parte dell'URL).

Questo isolamento può essere un grande vantaggio quando implementi transizioni tra livelli, minigiochi o grandi sistemi modulari, perché impedisce interazioni indesiderate e permette anche, se necessario, di controllare separatamente la temporizzazione degli aggiornamenti (per esempio per la pausa o il rallentatore).

Se hai già usato più scene in Unity e hai avuto bisogno che si comportassero in modo indipendente, considera un `Collection Proxy` come un modo per portare questo concetto direttamente in Defold.

Consulta altri dettagli nel [manuale dei proxy di collezione](/manuals/collection-proxy/).

---

## Ciclo di vita dell'applicazione {#application-lifecycle}

Conosci già alcuni eventi del ciclo di vita di Unity: `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` o `OnApplicationQuit`.

Anche Defold ha un ciclo di vita dell'applicazione ben definito, ma i concetti e la terminologia sono diversi. Defold espone le fasi del ciclo di vita tramite una serie di callback Lua predefinite, chiamate dal motore durante l'inizializzazione, a ogni fotogramma e durante la finalizzazione.

Ecco un confronto:

| Defold | Unity | Commento |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold ha un unico punto di ingresso e una sola callback di inizializzazione: init(). Viene chiamata su ogni componente alla sua creazione. |
| `on_input` | Metodi di input | Defold riceve gli input quando [lo script ha acquisito il focus dell'input](/manuals/input/#input-focus). Vengono elaborati per primi nel ciclo di aggiornamento. |
| `fixed_update()` | `FixedUpdate()` | Chiamata a intervalli di tempo fissi. Per abilitarla in Defold devi impostare `Use Fixed Timestep` - [dettagli](https://defold.com/manuals/project-settings/#use-fixed-timestep). Dalla versione 1.12.0 viene eseguita prima di `update()`. |
| `update()` | `Update()` | Chiamata una volta per fotogramma, con il tempo trascorso dal fotogramma precedente. |
| `late_update()` | `LateUpdate()` | Chiamata dopo `update()`, immediatamente prima del rendering del fotogramma. Disponibile dalla versione 1.12.0. |
| `on_message` | Ricevitore di messaggi | La callback principale di Defold per ricevere messaggi. Viene elaborata quando c'è un messaggio in coda. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold chiama le callback `final()` di ogni componente quando il suo oggetto di gioco viene distrutto durante l'esecuzione (usando `go.delete()`) oppure quando il mondo o la collezione vengono scaricati, e per tutti gli oggetti rimanenti alla chiusura dell'applicazione. |

::: sidenote
Ricorda che Defold non garantisce alcun ordine di esecuzione tra i componenti quando più componenti vengono inizializzati, aggiornati o rimossi contemporaneamente. È consigliabile una progettazione che riduca le dipendenze reciproche.
:::

### Inizializzazione {#initialization}

Puoi pensare a `init()` di Defold come a una combinazione di elementi di `Awake()`, `Start()` e `OnEnable()` di Unity in un unico punto di ingresso, in cui il motore ha già predisposto tutto e puoi preparare in sicurezza lo stato del componente.

### Quando vengono gestiti i messaggi? {#when-messages-are-handled}

Poiché puoi già inviare messaggi in `init()`, il primo inoltro dei messaggi avviene subito dopo l'inizializzazione.

I messaggi vengono poi gestiti dopo ogni ciclo di elaborazione interno, ogni volta che c'è qualcosa in coda: `on_message()` può quindi essere chiamata, per esempio, anche più volte all'interno di un ciclo di aggiornamento.

### Ciclo di aggiornamento {#update-loop}

A ogni fotogramma, Defold esegue una sequenza di operazioni: gestisce l'input, inoltra i messaggi, attiva gli aggiornamenti degli script e della GUI, applica la fisica e le trasformazioni e infine esegue il rendering della grafica.

### Finalizzazione {#finalization}

In Defold la pulizia è sempre legata all'eliminazione o allo scaricamento del mondo e l'unico hook di uscita per ciascun componente è `final()`.

Una differenza sottile rispetto al modello di Unity è che non c'è distinzione tra la disattivazione di un componente e la chiusura dell'intera applicazione.

### Rendering

Lo script di rendering (`*.render_script`) fa parte della pipeline di rendering e partecipa anch'esso al ciclo di vita con le proprie callback `init()`, `update()` e `on_message()`, che però operano sul thread di rendering e sono separate dalla logica degli script degli oggetti di gioco e della GUI.

Per altri dettagli, leggi il [manuale del ciclo di vita dell'applicazione](/manuals/application-lifecycle/).

---

## GUI

La GUI di Defold è un unico framework completo dedicato alle interfacce utente: menu, elementi sovrapposti, finestre di dialogo e altri elementi, simile a UI Toolkit o uGUI con Canvas.

La GUI è un componente ed è separata dagli oggetti di gioco e dalle collezioni. Anziché usare oggetti di gioco, lavori con nodi GUI organizzati in una gerarchia e controllati da uno script GUI.

### Nodi GUI {#gui-nodes}

Quando apri un file di componente `*.gui` in Defold, viene mostrato un canvas su cui posizionare i `"GUI nodes"`. Sono gli elementi costitutivi della GUI. Puoi aggiungere nodi GUI di tipo:

- Box (forma rettangolare con una texture)
- Text (con qualsiasi font)
- Pie (elemento a settore circolare con riempimento radiale e una texture)
- ParticleFX
- Template (un altro file `.gui` completo annidato, come un prefab GUI)
- e un nodo Spine, quando usi l'estensione Spine.

### Script GUI {#gui-script}

I componenti GUI hanno una proprietà speciale per gli script GUI: assegni un file `*.gui_script` a ogni componente e questo ti permette di modificarne il comportamento. È quindi molto simile agli script normali, ma non usa il namespace `go.*` (dedicato agli script degli oggetti di gioco). Usa invece un'API speciale nel namespace `gui.*`, che funziona soltanto all'interno degli script GUI (`*.gui_script`). Puoi considerarlo come una scena separata, come Unity UI (uGUI) con Canvas.

### Rendering della GUI {#gui-rendering}

Gli elementi GUI vengono disegnati indipendentemente dalla camera del gioco, di solito nello spazio dello schermo, ma questo comportamento può essere modificato nelle pipeline di rendering personalizzate.

Per altri dettagli, leggi il [manuale della GUI](/manuals/gui/).

## Dove sono i Sorting Layers? {#where-are-sorting-layers}

È una fonte di confusione molto comune quando si passa da Unity a Defold.

I componenti GUI hanno i `Layers`, che funzionano quasi come i "Sorting Layers" di Unity, ma per gli altri componenti, come `Sprites`, `Tilemaps`, `Models` e così via, non c'è un equivalente diretto.

Di solito combini invece:
- Un ordinamento preciso tramite l'asse Z quando usi una camera predefinita, oppure tramite la profondità quando usi un componente Camera.
- Un ordinamento generale tramite lo script di rendering, usando i predicati di rendering per selezionare che cosa disegnare in base ai tag dei materiali.

Non dovresti però imitare i Sorting Layers di Unity con molti tag, perché in Defold i tag sono un meccanismo che opera a livello di rendering. Un uso eccessivo può compromettere il batching e aumentare il costo delle operazioni di disegno.

---

## Come proseguire? {#where-to-go-from-here}

- [Esempi di Defold](/examples)
- [Tutorial](/tutorials)
- [Manuali](/manuals)
- [Riferimenti API](/ref/go)
- [FAQ](/faq/faq)

Se hai domande o incontri difficoltà, il [forum di Defold](//forum.defold.com) o [Discord](https://defold.com/discord/) sono ottimi posti in cui chiedere aiuto.
