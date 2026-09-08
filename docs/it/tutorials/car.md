---
title: Creare una semplice auto in Defold.
brief: Se hai appena iniziato a usare Defold, questa guida ti aiuterà a orientarti nell'editor. Spiega anche le idee di base e gli elementi fondamentali più comuni di Defold - oggetti di gioco, collezioni, script e sprite.
---

# Creare un'auto {#building-a-car}

Se hai appena iniziato a usare Defold, questa guida ti aiuterà a orientarti nell'editor. Spiega anche le idee di base e gli elementi fondamentali più comuni di Defold: oggetti di gioco (game object), collezioni (collection), script e sprite.

Partiremo da un progetto vuoto e procederemo passo dopo passo fino a ottenere una piccola applicazione giocabile. Alla fine dovresti avere un'idea di come funziona Defold ed essere pronto ad affrontare un tutorial più completo o a consultare direttamente i manuali.

::: sidenote
In questo tutorial, le spiegazioni dettagliate dei concetti e di come eseguire determinate operazioni sono evidenziate come questo paragrafo. Se ritieni che queste sezioni siano troppo dettagliate, puoi saltarle.
:::

## Creare un nuovo progetto {#creating-a-new-project}

![Nuovo progetto](images/new_empty.png)

1. Avvia Defold.
2. Seleziona *New Project* sulla sinistra.
3. Seleziona la scheda *From Template*.
4. Seleziona *Empty Project*
5. Scegli una posizione per il progetto sul disco locale.
6. Fai clic su *Create New Project*.

## L'editor {#the-editor}

Inizia creando un [nuovo progetto](/manuals/project-setup/) e aprendolo nell'editor. Fai doppio clic sul file *main/main.collection* per aprirlo:

![Panoramica dell'editor](../manuals/images/editor/editor2_overview.png)

L'editor è composto dalle seguenti aree principali:

Pannello Assets
: Mostra tutti i file del progetto. I diversi tipi di file hanno icone diverse. Fai doppio clic su un file per aprirlo nell'editor dedicato a quel tipo di file. La cartella speciale di sola lettura *builtins* è comune a tutti i progetti e include elementi utili come uno script di rendering predefinito, un font, materiali per il rendering di vari componenti e altro ancora.

Vista principale dell'editor
: A seconda del tipo di file che stai modificando, questa vista mostra l'editor corrispondente. Quello più usato è l'editor della scena che vedi qui. Ogni file aperto viene mostrato in una scheda separata.

Changed Files
: Contiene i file aggiunti, modificati, rinominati o eliminati localmente rispetto al commit Git corrente. Qui puoi visualizzare le differenze testuali e annullare le modifiche locali. Usa un client Git esterno o la riga di comando per sincronizzarti con un repository remoto.

Outline
: Mostra il contenuto del file attualmente in modifica in una vista gerarchica. Da questa vista puoi aggiungere, eliminare, modificare e selezionare oggetti e componenti.

Properties
: Le proprietà impostate sull'oggetto o sul componente attualmente selezionato.

Console
: Durante l'esecuzione del gioco, questa vista raccoglie l'output del motore di gioco (log, errori, informazioni di debug e così via), oltre ai messaggi di debug personalizzati prodotti da `print()` e `pprint()` nei tuoi script. Se l'applicazione o il gioco non si avvia, la console è la prima cosa da controllare. Dietro la console trovi alcune schede che mostrano informazioni sugli errori e un editor di curve usato per creare effetti particellari.

## Eseguire il gioco {#running-the-game}

Il modello di progetto "Empty" è effettivamente del tutto vuoto. Seleziona comunque <kbd>Project ▸ Build</kbd> per creare una build del progetto e avviare il gioco.

![Creazione della build](images/car/start_build_and_launch.png)

Una schermata nera forse non è molto entusiasmante, ma è un'applicazione di gioco Defold in esecuzione e possiamo facilmente trasformarla in qualcosa di più interessante. Facciamolo.

::: sidenote
L'editor Defold lavora sui file. Facendo doppio clic su un file nel pannello *Assets*, lo apri in un editor adatto. Puoi quindi lavorare sul contenuto del file.

Quando hai finito di modificare un file, devi salvarlo. Seleziona <kbd>File ▸ Save</kbd> nel menu principale. L'editor segnala i file con modifiche non salvate aggiungendo un asterisco '\*' al nome del file nella relativa scheda.

![File con modifiche non salvate](images/car/file_changed.png)
:::

## Assemblare l'auto {#assembling-the-car}

La prima cosa che faremo è creare una nuova collezione. Una collezione è un contenitore di oggetti di gioco che hai inserito e posizionato. Le collezioni sono usate soprattutto per costruire i livelli di gioco, ma sono molto utili ogni volta che devi riutilizzare gruppi e/o gerarchie di oggetti di gioco che fanno parte di un insieme. Può essere utile pensare alle collezioni come a una sorta di prefab.

Fai clic sulla cartella *main* nel pannello *Assets*, poi fai clic con il tasto destro e seleziona <kbd>New ▸ Collection File</kbd>. Puoi anche selezionare <kbd>File ▸ New ▸ Collection File</kbd> dal menu principale.

![Nuovo file di collezione](images/car/start_new_collection.png)

Assegna al nuovo file di collezione il nome *car.collection* e aprilo. Useremo questa nuova collezione vuota per costruire una piccola auto con alcuni oggetti di gioco. Un oggetto di gioco è un contenitore di componenti (come sprite, suoni, script di logica e così via) che usi per creare il gioco. Ogni oggetto di gioco è identificato in modo univoco nel gioco dal proprio ID. Gli oggetti di gioco possono comunicare tra loro scambiandosi messaggi, ma ne parleremo più avanti.

È anche possibile creare un oggetto di gioco direttamente all'interno di una collezione, come abbiamo fatto qui. In questo modo si ottiene un oggetto unico. Puoi copiarlo, ma ogni copia è indipendente---modificarne una non influisce sulle altre. Questo significa che, se crei 10 copie di un oggetto di gioco e poi decidi di modificarle tutte, dovrai modificare tutte e 10 le istanze dell'oggetto. Perciò è preferibile creare gli oggetti di gioco direttamente nella collezione quando non prevedi di farne molte copie.

Un oggetto di gioco salvato in un _file_, invece, funziona come un prototipo (chiamato anche "prefab" o "blueprint" in altri motori). Quando inserisci in una collezione le istanze di un oggetto di gioco salvato in un file, ogni oggetto viene inserito _per riferimento_---è un clone basato sul prototipo. Se decidi di modificare il prototipo, ogni oggetto di gioco inserito che si basa su quel prototipo viene aggiornato immediatamente.

![Aggiunta dell'oggetto di gioco dell'auto](images/car/start_add_car_gameobject.png)

Seleziona il nodo radice "Collection" nella vista *Outline*, fai clic con il tasto destro e seleziona <kbd>Add Game Object</kbd>. Nella collezione apparirà un nuovo oggetto di gioco con l'ID "go". Selezionalo e imposta il suo ID su "car" nella vista *Properties*. Per ora "car" non è molto interessante. È vuoto e non ha né una rappresentazione visiva né una logica. Per dargli una rappresentazione visiva, dobbiamo aggiungere un _componente_ sprite.

I componenti servono a dare agli oggetti di gioco una presenza (grafica, suono) e funzionalità (factory per la generazione, collisioni, comportamenti definiti da script). Un componente non può esistere da solo: deve trovarsi all'interno di un oggetto di gioco. Di solito i componenti sono definiti direttamente nello stesso file dell'oggetto di gioco. Tuttavia, se vuoi riutilizzare un componente, puoi salvarlo in un file separato (come per gli oggetti di gioco) e includerlo come riferimento in qualsiasi file di oggetto di gioco. Alcuni tipi di componente (per esempio gli script Lua) devono essere salvati in un file di componente separato e poi inclusi come riferimento nei tuoi oggetti.

Tieni presente che non manipoli direttamente i componenti---puoi spostare, ruotare, ridimensionare e animare le proprietà degli oggetti di gioco che li contengono.

![Aggiunta di un componente all'auto](images/car/start_add_car_component.png)

Seleziona l'oggetto di gioco "car", fai clic con il tasto destro e seleziona <kbd>Add Component</kbd>, poi seleziona *Sprite* e fai clic su *Ok*. Se selezioni lo sprite nella vista *Outline*, vedrai che occorre impostare alcune proprietà:

Image
: Richiede un'immagine sorgente per lo sprite. Crea un file atlas selezionando "main" nel pannello *Assets*, facendo clic con il tasto destro e selezionando <kbd>New ▸ Atlas File</kbd>. Assegna al nuovo file atlas il nome *sprites.atlas* e fai doppio clic per aprirlo nell'editor degli atlas. Salva sul computer i due file immagine seguenti e trascinali in *main* nel pannello *Assets*. Ora puoi selezionare il nodo radice Atlas nell'editor degli atlas, fare clic con il tasto destro e selezionare <kbd>Add Images</kbd>. Aggiungi all'atlas le immagini dell'auto e dello pneumatico e salva. Ora puoi selezionare *sprites.atlas* come immagine sorgente per il componente sprite nell'oggetto di gioco "car" della collezione "car".

Immagini per il nostro gioco:

![Immagine dell'auto](images/car/start_car.png)
![Immagine dello pneumatico](images/car/start_tire.png)

Aggiungi queste immagini all'atlas:

![Atlas degli sprite](images/car/start_sprites_atlas.png)

![Proprietà dello sprite](images/car/start_sprite_properties.png)

Default Animation
: Imposta questa proprietà su "car" (o sul nome che hai assegnato all'immagine dell'auto). Ogni sprite deve avere un'animazione predefinita da riprodurre quando viene mostrato nel gioco. Quando aggiungi immagini a un atlas, Defold crea comodamente animazioni di un solo fotogramma (statiche) per ogni file immagine.

## Completare l'auto {#completing-the-car}

Continua aggiungendo altri due oggetti di gioco alla collezione. Chiamali "left_wheel" e "right_wheel" e inserisci in ciascuno un componente sprite che mostri l'immagine dello pneumatico aggiunta a *sprites.atlas*. Poi trascina gli oggetti di gioco delle ruote su "car" per renderli figli di "car". Gli oggetti di gioco che sono figli di altri oggetti di gioco seguono il proprio genitore quando questo si muove. Possono anche essere spostati singolarmente, ma ogni movimento avviene rispetto all'oggetto genitore. Per gli pneumatici è perfetto: vogliamo che restino attaccati all'auto e possiamo semplicemente ruotarli un poco a sinistra e a destra quando sterziamo. Una collezione può contenere un numero qualsiasi di oggetti di gioco, affiancati, organizzati in alberi complessi di relazioni genitore-figlio, oppure in una combinazione delle due disposizioni.

Posiziona gli oggetti di gioco degli pneumatici selezionandoli e scegliendo <kbd>Scene ▸ Move Tool</kbd>. Trascina le maniglie a forma di freccia o il quadrato verde centrale per spostare l'oggetto nella posizione desiderata. L'ultima cosa da fare è assicurarci che gli pneumatici vengano disegnati sotto l'auto. Per farlo, impostiamo la componente Z della posizione su -0.5. Ogni elemento visivo del gioco viene disegnato dal fondo verso il primo piano, in ordine di valore Z. Un oggetto con valore Z pari a 0 viene disegnato sopra un oggetto con valore Z pari a -0.5. Poiché il valore Z predefinito dell'oggetto di gioco dell'auto è 0, il nuovo valore assegnato agli oggetti degli pneumatici li posizionerà sotto l'immagine dell'auto.

![Collezione dell'auto completata](images/car/start_car_collection_complete.png)

## Lo script dell'auto {#the-car-script}

L'ultimo pezzo del puzzle è uno _script_ per controllare l'auto. Uno script è un componente che contiene un programma che definisce i comportamenti degli oggetti di gioco. Con gli script puoi specificare le regole del gioco e il modo in cui gli oggetti devono rispondere alle diverse interazioni (sia con il giocatore sia con altri oggetti). Tutti gli script sono scritti nel linguaggio di programmazione Lua. Per lavorare con Defold, tu o qualcuno del tuo team dovete imparare a programmare in Lua.

Seleziona "main" nel pannello *Assets*, fai clic con il tasto destro e seleziona <kbd>New ▸ Script File</kbd>. Assegna al nuovo file il nome *car.script*, poi aggiungilo all'oggetto di gioco "car" selezionando "car" nella vista *Outline*, facendo clic con il tasto destro e selezionando <kbd>Add Component File</kbd>. Seleziona *car.script* e fai clic su *OK*. Salva il file di collezione.

Fai doppio clic su *car.script* per aprirlo.

::: sidenote
Defold fornisce diverse funzioni del ciclo di vita per programmare la logica di gioco. Trovi maggiori informazioni nel [manuale degli script](/manuals/script).
:::

Inizia eliminando le funzioni `final`, `on_message` e `on_reload`, perché non ci serviranno
in questo tutorial.

Poi aggiungi le seguenti righe di codice prima dell'inizio della funzione `init`.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Le modifiche sono piuttosto semplici: abbiamo solo aggiunto alcune `costanti` allo script che useremo in seguito per programmare la nostra auto.

::: sidenote
Osserva come memorizziamo in anticipo gli hash nelle variabili. È una buona pratica, perché rende il codice più leggibile e migliora le prestazioni.
:::

Ora modifica la funzione `init` in modo che contenga quanto segue:

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Ti stai chiedendo che cosa abbiamo appena cambiato? Ecco una spiegazione.

1. Inviamo un messaggio al nostro script di rendering chiedendogli di impostare il colore di sfondo su grigio. Gli script di rendering sono script speciali di Defold che controllano come vengono mostrati gli oggetti sullo schermo.
2. Per ricevere azioni di input in un componente script o in uno script GUI, occorre inviare il messaggio `acquire_input_focus` all'oggetto di gioco che contiene il componente. Nel nostro caso, inviamo questo messaggio all'oggetto di gioco che contiene lo script dell'auto.
3. Poi dichiariamo alcune variabili che useremo per tenere traccia dello stato corrente della nostra auto.

È stato facile, vero? Continuiamo modificando la funzione `update` in modo che contenga quanto segue:

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Era una funzione bella lunga! Ma non preoccuparti, ecco come funziona:

1. Per prima cosa impostiamo il vettore di accelerazione in base al vettore di input. Questo assicura che l'accelerazione dell'auto sia nella direzione dell'input.
2. Poi calcoliamo lo spostamento di entrambe le coppie di ruote seguendo una logica semplice: le ruote posteriori dell'auto si muovono sempre in avanti, mentre quelle anteriori si muovono nella direzione in cui sono orientate.
3. In base allo spostamento delle ruote, calcoliamo la nuova direzione di movimento dell'auto.
4. Qui aggiungiamo alla velocità l'accelerazione calcolata.
5. Infine aggiorniamo la posizione dell'auto in base alla velocità corrente.
6. Interpoliamo l'angolo di sterzata con una slerp in base all'input sinistra/destra. Questo evita che le ruote scattino istantaneamente ogni volta che l'input cambia.
7. Impostiamo poi la rotazione delle ruote in base all'angolo di sterzata corrente dell'auto. Allo stesso modo, impostiamo la rotazione dell'auto in base alla direzione in cui si sta muovendo.
8. Infine azzeriamo i vettori di accelerazione e di input.

Ora è il momento di far reagire la nostra auto all'input. Aggiorna la funzione `on_input` in questo modo:

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Questa funzione è piuttosto semplice: riceviamo l'input e impostiamo il nostro vettore di input.

Non dimenticare di salvare le modifiche.

## Input

Non abbiamo ancora configurato le azioni di input, quindi facciamolo ora. Apri il file */input/game.input_bindings* e aggiungi binding *key_trigger* per "accelerate", "brake", "left" e "right". Li associamo ai tasti freccia (KEY_LEFT, KEY_RIGHT, KEY_UP e KEY_DOWN):

![Binding di input](images/car/start_input_bindings.png)

## Aggiungere l'auto al gioco {#adding-the-car-to-the-game}

Ora l'auto è pronta a partire. L'abbiamo creata all'interno di "car.collection", ma non è ancora presente nel gioco. Questo accade perché al momento il motore carica "main.collection" all'avvio. Per risolvere il problema basta aggiungere *car.collection* a *main.collection*. Apri *main.collection*, seleziona il nodo radice "Collection" nella vista *Outline*, fai clic con il tasto destro e seleziona <kbd>Add Collection From File</kbd>, poi seleziona *car.collection* e fai clic su *OK*. Ora i contenuti di *car.collection* verranno inseriti in *main.collection* come nuove istanze. Se modifichi il contenuto di *car.collection*, ogni istanza della collezione verrà aggiornata automaticamente quando viene creata una build del gioco.

![Aggiunta della collezione dell'auto](images/car/start_adding_car_collection.png)

Ora seleziona <kbd>Project ▸ Build</kbd> e fai un giro con la tua nuova auto!
Noterai che ora puoi muovere l'auto come vuoi. Ma c'è ancora qualcosa che non va. Quando rilasci i comandi, l'auto non si ferma come dovrebbe. È il momento di aggiungere questo comportamento!

## La resistenza al moto ci viene in aiuto {#drag-to-the-rescue}

Quando un oggetto si muove nel mondo reale, la forza di resistenza si oppone al movimento e lo rallenta. Questa forza è approssimativamente proporzionale al quadrato della velocità dell'oggetto in movimento e può quindi essere descritta come `D = k * |V| * V`, dove `k` è una costante, `V` è la velocità e `|V|` il suo modulo (la velocità scalare). Aggiungiamola.

Nella sezione delle costanti, all'inizio dello script, aggiungi la seguente costante

```lua
local drag = 1.1	        --the drag constant <1>
```

Poi, nella funzione `update`, subito prima della riga mostrata qui sotto, aggiungi le righe del blocco successivo e salva il file.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Dichiariamo il valore della resistenza come costante.
2. Calcoliamo la velocità a cui ci stiamo muovendo.
3. Applichiamo la resistenza all'accelerazione corrente in base alla formula
4. Fermiamo l'auto se è già abbastanza lenta.

## Lo script completo dell'auto {#the-complete-car-script}

Dopo aver completato i passaggi precedenti, il tuo *car.script* dovrebbe apparire così:

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Provare il gioco completo {#trying-the-final-game}

Ora seleziona <kbd>Project ▸ Build</kbd> dal menu principale e fai un giro con la tua nuova auto!

Questo conclude il tutorial introduttivo. Ecco alcune sfide che puoi provare ad affrontare da solo:

1. Al momento l'auto si muove con la stessa accelerazione sia in avanti sia all'indietro. Puoi modificare questo comportamento in modo che l'auto si muova più lentamente in retromarcia.
2. Trasforma alcune costanti (come l'accelerazione) in `proprietà`, così da poterle modificare per istanze diverse dell'auto.
3. Aggiungi suoni alla tua auto e falla rombare! ([Suggerimento](/manuals/sound/))

Ora continua a esplorare Defold. Abbiamo preparato molti [manuali e tutorial](/learn) per guidarti e, se ti blocchi, sei il benvenuto sul [forum](//forum.defold.com).

Buon divertimento con Defold!
