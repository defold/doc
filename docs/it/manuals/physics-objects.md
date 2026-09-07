---
title: Oggetti di collisione in Defold
brief: Un oggetto di collisione è un componente che usi per dare un comportamento fisico a un oggetto di gioco. Un oggetto di collisione ha proprietà fisiche e una forma nello spazio.
---

# Oggetti di collisione {#collision-objects}

Un oggetto di collisione è un componente che usi per dare un comportamento fisico a un oggetto di gioco. Un oggetto di collisione ha proprietà fisiche come peso, restituzione e attrito, e la sua estensione nello spazio è definita da una o più _forme_ che aggiungi al componente. Defold supporta i seguenti tipi di oggetti di collisione:

Oggetti statici
: Gli oggetti statici non si muovono mai, ma un oggetto dinamico che collide con un oggetto statico reagisce rimbalzando e/o scivolando. Gli oggetti statici sono molto utili per costruire la geometria immobile dei livelli (cioè il terreno e le pareti). Inoltre, richiedono meno risorse di calcolo rispetto agli oggetti dinamici. Non puoi spostare o modificare in altro modo gli oggetti statici.

Oggetti dinamici
: Gli oggetti dinamici sono simulati dal motore fisico. Il motore risolve tutte le collisioni e applica le forze risultanti. Gli oggetti dinamici sono adatti a oggetti che devono comportarsi in modo realistico. Il modo più comune per influenzarli è indirettamente, [applicando forze](/ref/physics/#apply_force) o modificando lo [smorzamento](/ref/stable/physics/#angular_damping) e la [velocità](/ref/stable/physics/#linear_velocity) angolari e lo [smorzamento](/ref/stable/physics/#linear_damping) e la [velocità](/ref/stable/physics/#angular_velocity) lineari. È anche possibile manipolare direttamente la posizione e l'orientamento di un oggetto dinamico quando l'[impostazione Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) è abilitata in *game.project*.

Oggetti cinematici
: Gli oggetti cinematici registrano le collisioni con altri oggetti fisici, ma il motore fisico non esegue alcuna simulazione automatica. Il compito di risolvere le collisioni, o di ignorarle, spetta a te ([scopri di più](/manuals/physics-resolving-collisions)). Gli oggetti cinematici sono molto adatti a oggetti controllati dal giocatore o da script che richiedono un controllo preciso delle reazioni fisiche, come un personaggio giocante.

Trigger
: I trigger sono oggetti che registrano collisioni semplici. Sono oggetti di collisione leggeri. Sono simili alle [proiezioni di raggi](/manuals/physics-ray-casts) perché leggono il mondo fisico anziché interagire con esso. Sono adatti a oggetti che devono soltanto registrare un impatto (come un proiettile) o a parti della logica di gioco in cui vuoi attivare determinate azioni quando un oggetto raggiunge un punto specifico. I trigger richiedono meno risorse di calcolo rispetto agli oggetti cinematici e, quando possibile, vanno preferiti a questi ultimi.


## Aggiungere un componente oggetto di collisione {#adding-a-collision-object-component}

Un componente oggetto di collisione ha un insieme di *Properties* che ne definiscono il tipo e le proprietà fisiche. Contiene inoltre una o più *Shapes* che definiscono la forma complessiva dell'oggetto fisico.

Per aggiungere un componente oggetto di collisione a un oggetto di gioco:

1. Nella vista *Outline*, <kbd>fai clic con il pulsante destro</kbd> sull'oggetto di gioco e seleziona <kbd>Add Component ▸ Collision Object</kbd> dal menu contestuale. Questo crea un nuovo componente senza forme.
2. <kbd>Fai clic con il pulsante destro</kbd> sul nuovo componente e seleziona <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. Questo aggiunge una nuova forma al componente oggetto di collisione. Puoi aggiungere al componente tutte le forme che vuoi. Puoi anche usare una mappa di tile o un inviluppo convesso per definire la forma dell'oggetto fisico.
3. Usa gli strumenti di spostamento, rotazione e scala per modificare le forme.
4. Seleziona il componente nella vista *Outline* e modifica le *Properties* dell'oggetto di collisione.

![Oggetto di collisione fisica](images/physics/collision_object.png)


## Aggiungere una forma di collisione {#adding-a-collision-shape}

Un componente di collisione può usare più forme primitive oppure una singola forma complessa. Per saperne di più sulle varie forme e su come aggiungerle a un componente di collisione, consulta il [manuale delle forme di collisione](/manuals/physics-shapes).


## Proprietà dell'oggetto di collisione {#collision-object-properties}

Id
: L'identità del componente.

Collision Shape
: Questa proprietà viene usata per la geometria delle mappe di tile o per le forme convesse che non usano forme primitive. Per ulteriori informazioni, consulta il [manuale delle forme di collisione](/manuals/physics-shapes).

Type
: Il tipo di oggetto di collisione: `Dynamic`, `Kinematic`, `Static` o `Trigger`. Se imposti l'oggetto su `Dynamic`, _devi_ impostare la proprietà *Mass* su un valore diverso da zero. Per gli oggetti `Dynamic` o `Static`, dovresti anche verificare che i valori di *Friction* e *Restitution* siano adatti al tuo caso d'uso.

Friction
: L'attrito permette agli oggetti di scivolare l'uno sull'altro in modo realistico. Il valore dell'attrito viene solitamente impostato tra `0` (nessun attrito---un oggetto molto scivoloso) e `1` (attrito elevato---un oggetto abrasivo). Tuttavia, è valido qualsiasi valore positivo.

  L'intensità dell'attrito è proporzionale alla forza normale (si tratta dell'attrito di Coulomb). Quando viene calcolata la forza di attrito tra due forme (`A` e `B`), i valori di attrito dei due oggetti vengono combinati tramite la media geometrica:

```math
F = sqrt( F_A * F_B )
```

  Questo significa che, se uno degli oggetti ha attrito nullo, anche il contatto tra loro avrà attrito nullo.

Restitution
: Il valore di restituzione determina quanto l'oggetto rimbalza. Il valore è solitamente compreso tra 0 (collisione anelastica—l'oggetto non rimbalza affatto) e 1 (collisione perfettamente elastica---la velocità dell'oggetto viene riflessa esattamente nel rimbalzo)

  I valori di restituzione tra due forme (`A` e `B`) vengono combinati usando la seguente formula:

```math
R = max( R_A, R_B )
```

  Quando una forma entra in contatto in più punti, la restituzione viene simulata in modo approssimativo perché Box2D usa un risolutore iterativo. Box2D usa anche collisioni anelastiche quando la velocità di collisione è bassa, per evitare tremolii dovuti ai rimbalzi

Linear damping
: Lo smorzamento lineare riduce la velocità lineare del corpo. È diverso dall'attrito, che si verifica soltanto durante il contatto, e può essere usato per dare agli oggetti l'impressione di fluttuare, come se si muovessero in un mezzo più denso dell'aria. I valori validi sono compresi tra 0 e 1.

  Box2D approssima lo smorzamento per ragioni di stabilità e prestazioni. Per valori bassi, l'effetto di smorzamento è indipendente dal passo temporale, mentre per valori di smorzamento più alti l'effetto varia con il passo temporale. Se esegui il gioco con un passo temporale fisso, questo non costituisce mai un problema.

Angular damping
: Lo smorzamento angolare funziona come quello lineare, ma riduce la velocità angolare del corpo. I valori validi sono compresi tra 0 e 1.

Locked rotation
: Abilitando questa proprietà disabiliti completamente la rotazione dell'oggetto di collisione, indipendentemente dalle forze che agiscono su di esso.

Bullet
: Abilitando questa proprietà attivi il rilevamento continuo delle collisioni (CCD) tra l'oggetto di collisione e gli altri oggetti di collisione dinamici. La proprietà *Bullet* viene ignorata se *Type* non è impostato su `Dynamic`.

Group
: Il nome del gruppo di collisione a cui deve appartenere l'oggetto. Puoi avere 16 gruppi diversi e nominarli come ritieni opportuno per il tuo gioco. Per esempio `players`, `bullets`, `enemies` e `world`. Se *Collision Shape* è impostato su una mappa di tile, questo campo non viene usato e i nomi dei gruppi vengono ricavati dalla sorgente di tile. [Scopri di più sui gruppi di collisione](/manuals/physics-groups).

Mask
: Gli altri _gruppi_ con cui questo oggetto deve collidere. Puoi indicare un gruppo oppure specificarne più di uno in un elenco separato da virgole. Se lasci il campo *Mask* vuoto, l'oggetto non colliderà con nulla. [Scopri di più sui gruppi di collisione](/manuals/physics-groups).

Generate Collision Events
: Se abilitata, consente a questo oggetto di inviare eventi di collisione

Generate Contact Events
: Se abilitata, consente a questo oggetto di inviare eventi di contatto

Generate Trigger Events
: Se abilitata, consente a questo oggetto di inviare eventi trigger


## Proprietà a runtime {#runtime-properties}

Un oggetto fisico ha diverse proprietà che possono essere lette e modificate usando `go.get()` e `go.set()`:

`angular_damping`
: Il valore di smorzamento angolare del componente oggetto di collisione (`number`). [Riferimento API](/ref/physics/#angular_damping).

`angular_velocity`
: La velocità angolare attuale del componente oggetto di collisione (`vector3`). [Riferimento API](/ref/physics/#angular_velocity).

`linear_damping`
: Il valore di smorzamento lineare dell'oggetto di collisione (`number`). [Riferimento API](/ref/physics/#linear_damping).

`linear_velocity`
: La velocità lineare attuale del componente oggetto di collisione (`vector3`). [Riferimento API](/ref/physics/#linear_velocity).

`mass`
: La massa fisica definita per il componente oggetto di collisione. SOLA LETTURA. (`number`). [Riferimento API](/ref/physics/#mass).
