---
title: Kollisionsformen
brief: Kollisionsobjekte können primitive Formen, Hüllen oder Dreiecksmeshes enthalten oder Ressourcen für Kachelkarten und konvexe Formen verwenden.
---

# Kollisionsformen {#collision-shapes}

Ein Kollisionsobjekt (collision object) kann mehrere eingebettete Kollisionsformen (collision shapes) enthalten. In der 3D-Physik können dazu auch Hüllen und Dreiecksmeshes aus glTF- oder GLB-Dateien gehören. Du kannst auch eine Kachelkarte (tile map) oder eine Ressource für eine konvexe Form über die Eigenschaft *Collision Shape* des Kollisionsobjekts verwenden.

### Primitive Formen {#primitive-shapes}
Die primitiven Formen sind *Quader*, *Kugel* und *Kapsel*. Du fügst eine primitive Form hinzu, indem du mit der <kbd>rechten Maustaste</kbd> auf das Kollisionsobjekt klickst und <kbd>Add Shape</kbd> auswählst:

![Eine primitive Form hinzufügen](images/physics/add_shape.png)

## Quaderform {#box-shape}
Ein Quader hat eine Position, eine Drehung und Abmessungen (Breite, Höhe und Tiefe):

![Quaderform](images/physics/box.png)

## Kugelform {#sphere-shape}
Eine Kugel hat eine Position, eine Drehung und einen Durchmesser:

![Kugelform](images/physics/sphere.png)

## Kapselform {#capsule-shape}
Eine Kapsel hat eine Position, eine Drehung, einen Durchmesser und eine Höhe:

![Kugelform](images/physics/capsule.png)

::: important
Kapselformen werden nur bei Verwendung der 3D-Physik unterstützt (konfiguriert im Bereich Physics der Datei *game.project*).
:::

### Komplexe Formen {#complex-shapes}
Komplexe Formen können die Geometrie einer Kachelkarte oder Daten einer konvexen Hülle (convex hull) verwenden. Seit Defold 1.13.2 können 3D-Kollisionsobjekte auch Hüllen und Dreiecksmesh-Formen aus Meshes in glTF- oder GLB-Szenen erstellen.

## Hüllen- und Mesh-Formen in 3D {#hull-and-mesh-shapes-in-3d}

Verwende eine Form vom Typ *Hull* für eine konvexe Annäherung an ein Mesh oder eine Form vom Typ *Mesh*, wenn Kollisionen dessen Dreiecken folgen müssen, einschließlich konkaver Bereiche wie Öffnungen in der Levelgeometrie.

1. Setze **Physics → Type** in *game.project* auf `3D`.
2. Klicke in der Ansicht *Outline* mit der rechten Maustaste auf das Kollisionsobjekt und wähle <kbd>Add Shape ▸ Hull</kbd> oder <kbd>Add Shape ▸ Mesh</kbd>.
3. Wähle die neue Form aus und setze ihre Eigenschaft *Scene* auf eine *.gltf*- oder *.glb*-Datei.
4. Wähle im Feld *Mesh* ein benanntes Mesh aus. Falls es in der Liste fehlt, benenne das Mesh in deinem Modellierungswerkzeug und exportiere die Szene erneut.
5. Positioniere und drehe die Form, um sie an der sichtbaren Geometrie des Spielobjekts (game object) auszurichten. Wiederhole diese Schritte bei Bedarf, um weitere Formen hinzuzufügen.

Das ausgewählte Mesh liefert seine lokale Geometrie; Transformationen von glTF-Knoten werden nicht angewendet. Mesh-Kollisionsformen werden vom Bullet-3D-Backend unterstützt, auch für statische und nicht statische Kollisionsobjekte. Von den 2D-Physik-Backends werden sie nicht unterstützt.

Auf die Geometrie eines Dreiecksmeshes kann über die Laufzeit-APIs für Formen nur lesend zugegriffen werden. Bearbeite das Quellmesh und erstelle einen neuen Build, um seine Dreiecke zu ändern. Informationen zur Skalierung des Spielobjekts findest du unter [Kollisionsformen skalieren](#scaling-collision-shapes).

## Kollisionsform einer Kachelkarte {#tilemap-collision-shape}
Defold enthält eine Funktion, mit der du ganz einfach Physikformen für die Kachelquelle (tile source) einer Kachelkarte erzeugen kannst. Das [Handbuch zu Kachelquellen](/manuals/tilesource/#tile-source-collision-shapes) erklärt, wie du einer Kachelquelle Kollisionsgruppen hinzufügst und Kacheln den Kollisionsgruppen zuweist ([Beispiel](/examples/tilemap/collisions/)).

So fügst du einer Kachelkarte Kollisionen hinzu:

1. Füge die Kachelkarte einem Spielobjekt hinzu, indem du mit der <kbd>rechten Maustaste</kbd> auf das Spielobjekt klickst und <kbd>Add Component File</kbd> auswählst. Wähle die Kachelkartendatei aus.
2. Füge dem Spielobjekt eine Komponente (component) vom Typ Kollisionsobjekt hinzu, indem du mit der <kbd>rechten Maustaste</kbd> auf das Spielobjekt klickst und <kbd>Add Component ▸ Collision Object</kbd> auswählst.
3. Statt der Komponente Formen hinzuzufügen, setze die Eigenschaft *Collision Shape* auf die *tilemap*-Datei.
4. Richte die *Properties* der Kollisionsobjekt-Komponente wie gewohnt ein.

![Kollision einer Kachelquelle](images/physics/collision_tilemap.png)

::: important
Beachte, dass die Eigenschaft *Group* hier **nicht** verwendet wird, da die Kollisionsgruppen in der Kachelquelle der Kachelkarte definiert sind.
:::

## Form einer konvexen Hülle {#convex-hull-shape}
In der 3D-Physik kannst du eine Hülle direkt aus einem Mesh erstellen, indem du den [oben beschriebenen Arbeitsablauf im Editor](#hull-and-mesh-shapes-in-3d) verwendest. Die ältere Ressource `.convexshape` wird ebenfalls unterstützt und kann mit einem externen Editor aus Punkten erstellt werden:

1. Erstelle mit einem externen Editor eine Datei für eine konvexe Hüllform (Dateierweiterung `.convexshape`).
2. Bearbeite die Datei manuell mit einem Texteditor oder einem externen Werkzeug (siehe unten)
3. Statt der Kollisionsobjekt-Komponente Formen hinzuzufügen, setze die Eigenschaft *Collision Shape* auf die Datei der *konvexen Form*.

### Dateiformat {#file-format}
Das Dateiformat für konvexe Hüllen verwendet dasselbe Datenformat wie alle anderen Defold-Dateien, nämlich das Protobuf-Textformat. Eine konvexe Hüllform definiert die Punkte der Hülle. In der 2D-Physik sollten die Punkte gegen den Uhrzeigersinn angegeben werden. Im 3D-Physikmodus wird eine abstrakte Punktwolke verwendet. 2D-Beispiel:

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

Das obige Beispiel definiert die vier Ecken eines Rechtecks:

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

## Externe Werkzeuge {#external-tools}

Es gibt verschiedene externe Werkzeuge, mit denen sich Kollisionsformen erstellen lassen:

* Mit dem [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) von CodeAndWeb kannst du Spielobjekte mit Sprites und passenden Kollisionsformen erstellen.
* Mit dem [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) kannst du konvexe Hüllformen erstellen.
* Mit dem [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) kannst du konvexe Hüllformen erstellen.


# Kollisionsformen skalieren {#scaling-collision-shapes}
Das Kollisionsobjekt und seine Formen erben die Skalierung des Spielobjekts. Um dieses Verhalten zu deaktivieren, entferne das Häkchen im Kontrollkästchen [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) im Bereich Physics von *game.project*. Beachte, dass nur eine gleichmäßige Skalierung unterstützt wird und der kleinste Skalierungswert verwendet wird, wenn die Skalierung nicht gleichmäßig ist.

# Die Größe von Kollisionsformen ändern {#resizing-collision-shapes}
Die Größe primitiver Formen kann zur Laufzeit mit `physics.set_shape()` geändert werden. Diese Funktion ersetzt weder die Vertices einer Hülle noch die Geometrie eines Dreiecksmeshes. Beispiel:

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
Auf dem Kollisionsobjekt muss bereits eine Form des richtigen Typs mit dem angegebenen Bezeichner vorhanden sein.
:::

# Kollisionsformen drehen {#rotating-collision-shapes}

## Kollisionsformen in der 3D-Physik drehen {#rotating-collision-shapes-in-3d-physics}
Kollisionsformen in der 3D-Physik können um alle Achsen gedreht werden.


## Kollisionsformen in der 2D-Physik drehen {#rotating-collision-shapes-in-2d-physics}
Kollisionsformen in der 2D-Physik können nur um die z-Achse gedreht werden. Eine Drehung um die x- oder y-Achse führt zu falschen Ergebnissen und sollte vermieden werden, auch wenn die Drehung um 180 Grad die Form im Wesentlichen entlang der x- oder y-Achse spiegelt. Um eine Physikform zu spiegeln, wird empfohlen, [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) und [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip) zu verwenden.


# Fehlersuche {#debugging}
Du kannst das [Physik-Debugging aktivieren](/manuals/debugging-game-logic/#debugging-problems-with-physics), um die Kollisionsformen zur Laufzeit zu sehen.
