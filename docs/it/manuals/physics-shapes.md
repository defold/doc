---
title: Forme di collisione
brief: Gli oggetti di collisione possono contenere forme primitive, inviluppi convessi o mesh triangolari, oppure usare risorse tilemap e di forma convessa.
---

# Forme di collisione {#collision-shapes}

Un oggetto di collisione può contenere più forme incorporate. Nella fisica 3D, queste possono includere inviluppi convessi e mesh triangolari da file glTF o GLB. Puoi anche usare una tilemap o una risorsa di forma convessa tramite la proprietà *Collision Shape* dell'oggetto di collisione.

### Forme primitive {#primitive-shapes}
Le forme primitive sono *parallelepipedo*, *sfera* e *capsula*. Per aggiungere una forma primitiva, <kbd>fai clic con il pulsante destro</kbd> sull'oggetto di collisione e seleziona <kbd>Add Shape</kbd>:

![Aggiunta di una forma primitiva](images/physics/add_shape.png)

## Forma a parallelepipedo {#box-shape}
Un parallelepipedo ha una posizione, una rotazione e delle dimensioni (larghezza, altezza e profondità):

![Forma a parallelepipedo](images/physics/box.png)

## Forma sferica {#sphere-shape}
Una sfera ha una posizione, una rotazione e un diametro:

![Forma sferica](images/physics/sphere.png)

## Forma a capsula {#capsule-shape}
Una capsula ha una posizione, una rotazione, un diametro e un'altezza:

![Forma sferica](images/physics/capsule.png)

::: important
Le forme a capsula sono supportate solo quando si usa la fisica 3D (configurata nella sezione Physics del file *game.project*).
:::

### Forme complesse {#complex-shapes}
Le forme complesse possono usare la geometria di una tilemap o dati di inviluppi convessi. Da Defold 1.13.2, gli oggetti di collisione 3D possono anche creare inviluppi convessi e forme a mesh triangolare dalle mesh di scene glTF o GLB.

## Forme Hull e Mesh in 3D {#hull-and-mesh-shapes-in-3d}

Usa una forma *Hull* per un'approssimazione convessa di una mesh oppure una forma *Mesh* quando le collisioni devono seguirne i triangoli, comprese le aree concave come le aperture nella geometria di un livello.

1. Imposta **Physics → Type** su `3D` in *game.project*.
2. Fai clic con il pulsante destro sull'oggetto di collisione nella vista *Outline* e seleziona <kbd>Add Shape ▸ Hull</kbd> oppure <kbd>Add Shape ▸ Mesh</kbd>.
3. Seleziona la nuova forma e imposta la sua proprietà *Scene* su un file *.gltf* o *.glb*.
4. Seleziona una mesh con nome dal campo *Mesh*. Se non è nell'elenco, assegna un nome alla mesh nello strumento di modellazione ed esporta nuovamente la scena.
5. Sposta e ruota la forma per allinearla alla geometria visibile dell'oggetto di gioco. Ripeti questi passaggi per aggiungere altre forme, se necessario.

La mesh selezionata fornisce la propria geometria locale; le trasformazioni dei nodi glTF non vengono applicate. Le forme di collisione Mesh sono supportate dal backend Bullet 3D, anche per gli oggetti di collisione statici e non statici. Non sono supportate dai backend di fisica 2D.

La geometria delle mesh triangolari è di sola lettura nelle API delle forme a runtime. Per modificarne i triangoli, modifica la mesh sorgente e ricrea la build. Consulta [Scalare le forme di collisione](#scaling-collision-shapes) per la scala dell'oggetto di gioco.

## Forma di collisione di una mappa di tile {#tilemap-collision-shape}
Defold include una funzionalità che consente di generare facilmente forme fisiche per la sorgente di tile usata da una mappa di tile. Il [manuale delle sorgenti di tile](/manuals/tilesource/#tile-source-collision-shapes) spiega come aggiungere gruppi di collisione a una sorgente di tile e assegnare i tile ai gruppi di collisione ([esempio](/examples/tilemap/collisions/)).

Per aggiungere le collisioni a una mappa di tile:

1. Aggiungi la mappa di tile a un oggetto di gioco facendo <kbd>clic con il pulsante destro</kbd> sull'oggetto di gioco e selezionando <kbd>Add Component File</kbd>. Seleziona il file della mappa di tile.
2. Aggiungi un componente oggetto di collisione all'oggetto di gioco facendo <kbd>clic con il pulsante destro</kbd> sull'oggetto di gioco e selezionando <kbd>Add Component ▸ Collision Object</kbd>.
3. Invece di aggiungere forme al componente, imposta la proprietà *Collision Shape* sul file *tilemap*.
4. Configura le *Properties* del componente oggetto di collisione come di consueto.

![Collisione della sorgente di tile](images/physics/collision_tilemap.png)

::: important
Tieni presente che la proprietà *Group* **non** viene usata in questo caso, poiché i gruppi di collisione sono definiti nella sorgente di tile della mappa di tile.
:::

## Forma a inviluppo convesso {#convex-hull-shape}
Nella fisica 3D puoi creare un inviluppo convesso direttamente da una mesh usando la [procedura nell'editor descritta sopra](#hull-and-mesh-shapes-in-3d). La risorsa `.convexshape` precedente rimane supportata e può essere creata da punti usando un editor esterno:

1. Crea un file di forma a inviluppo convesso (con estensione `.convexshape`) usando un editor esterno.
2. Modifica manualmente il file usando un editor di testo o uno strumento esterno (vedi sotto)
3. Invece di aggiungere forme al componente oggetto di collisione, imposta la proprietà *Collision Shape* sul file della *forma convessa*.

### Formato del file {#file-format}
Il formato dei file di inviluppo convesso usa lo stesso formato dati di tutti gli altri file Defold, cioè il formato testuale Protobuf. Una forma a inviluppo convesso definisce i punti dell'inviluppo. Nella fisica 2D, i punti devono essere forniti in senso antiorario. In modalità fisica 3D viene usata una nuvola di punti astratta. Esempio 2D:

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

L'esempio precedente definisce i quattro vertici di un rettangolo:

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## Strumenti esterni {#external-tools}

Esistono diversi strumenti esterni che si possono usare per creare forme di collisione:

* [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) di CodeAndWeb consente di creare oggetti di gioco con sprite e forme di collisione corrispondenti.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) consente di creare forme a inviluppo convesso.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) consente di creare forme a inviluppo convesso.


# Modifica della scala delle forme di collisione {#scaling-collision-shapes}
L'oggetto di collisione e le sue forme ereditano la scala dell'oggetto di gioco. Per disattivare questo comportamento, deseleziona la casella [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) nella sezione Physics di *game.project*. Tieni presente che è supportata solo la scala uniforme e che, se la scala non è uniforme, verrà usato il valore di scala più piccolo.

# Ridimensionamento delle forme di collisione {#resizing-collision-shapes}
Le forme primitive possono essere ridimensionate a runtime usando `physics.set_shape()`. Questa funzione non sostituisce i vertici degli inviluppi convessi né la geometria delle mesh triangolari. Esempio:

```lua
-- set capsule shape data
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- set sphere shape data
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- set box shape data
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
Sull'oggetto di collisione deve già esistere una forma del tipo corretto con l'ID specificato.
:::

# Rotazione delle forme di collisione {#rotating-collision-shapes}

## Rotazione delle forme di collisione nella fisica 3D {#rotating-collision-shapes-in-3d-physics}
Le forme di collisione nella fisica 3D possono essere ruotate attorno a tutti gli assi.


## Rotazione delle forme di collisione nella fisica 2D {#rotating-collision-shapes-in-2d-physics}
Le forme di collisione nella fisica 2D possono essere ruotate solo attorno all'asse z. La rotazione attorno all'asse x o y produce risultati errati e va evitata, anche quando si ruota di 180 gradi per ribaltare di fatto la forma lungo l'asse x o y. Per ribaltare una forma fisica, si consiglia di usare [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) e [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip).


# Debug {#debugging}
Puoi [attivare il debug della fisica](/manuals/debugging-game-logic/#debugging-problems-with-physics) per visualizzare le forme di collisione durante l'esecuzione.
