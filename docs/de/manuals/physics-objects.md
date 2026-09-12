---
title: Kollisionsobjekte in Defold
brief: Ein Kollisionsobjekt ist eine Komponente, mit der du einem Spielobjekt physikalisches Verhalten gibst. Ein Kollisionsobjekt hat physikalische Eigenschaften und eine räumliche Form.
---

# Kollisionsobjekte {#collision-objects}

Ein Kollisionsobjekt (collision object) ist eine Komponente (component), mit der du einem Spielobjekt (game object) physikalisches Verhalten gibst. Ein Kollisionsobjekt hat physikalische Eigenschaften wie Gewicht, Rückprallkoeffizient und Reibung. Seine räumliche Ausdehnung wird durch eine oder mehrere _Formen_ bestimmt, die du der Komponente hinzufügst. Defold unterstützt die folgenden Arten von Kollisionsobjekten:

Statische Objekte
: Statische Objekte (static objects) bewegen sich nie, aber ein dynamisches Objekt, das mit einem statischen Objekt kollidiert, reagiert durch Abprallen und/oder Gleiten. Statische Objekte eignen sich sehr gut zum Aufbau unbeweglicher Levelgeometrie (z. B. Boden und Wände). Sie benötigen außerdem weniger Rechenleistung als dynamische Objekte. Du kannst statische Objekte weder bewegen noch anderweitig verändern.

Dynamische Objekte
: Dynamische Objekte (dynamic objects) werden von der Physik-Engine simuliert. Die Engine löst alle Kollisionen auf und wendet die daraus resultierenden Kräfte an. Dynamische Objekte eignen sich für Objekte, die sich realistisch verhalten sollen. Meist beeinflusst du sie indirekt, indem du [Kräfte anwendest](/ref/physics/#apply_force) oder die [Winkeldämpfung](/ref/stable/physics/#angular_damping) und [Winkelgeschwindigkeit](/ref/stable/physics/#linear_velocity) sowie die [lineare Dämpfung](/ref/stable/physics/#linear_damping) und [lineare Geschwindigkeit](/ref/stable/physics/#angular_velocity) änderst. Du kannst die Position und Ausrichtung eines dynamischen Objekts auch direkt verändern, wenn die [Einstellung Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) in *game.project* aktiviert ist.

Kinematische Objekte
: Kinematische Objekte (kinematic objects) registrieren Kollisionen mit anderen Physikobjekten, aber die Physik-Engine führt keine automatische Simulation durch. Die Aufgabe, Kollisionen aufzulösen oder zu ignorieren, bleibt dir überlassen ([mehr erfahren](/manuals/physics-resolving-collisions)). Kinematische Objekte eignen sich sehr gut für vom Spieler oder durch Skripte gesteuerte Objekte, deren physikalische Reaktionen genau kontrolliert werden müssen, etwa eine Spielfigur.

Trigger
: Trigger sind Objekte, die einfache Kollisionen registrieren. Trigger sind Kollisionsobjekte mit geringem Rechenaufwand. Sie ähneln [Strahlabfragen (raycast)](/manuals/physics-ray-casts), da sie die Physikwelt abfragen, statt mit ihr zu interagieren. Sie eignen sich für Objekte, die lediglich einen Treffer registrieren müssen (etwa ein Geschoss), oder als Teil der Spiellogik, wenn du bestimmte Aktionen auslösen möchtest, sobald ein Objekt einen bestimmten Punkt erreicht. Trigger benötigen weniger Rechenleistung als kinematische Objekte und sollten daher möglichst an deren Stelle verwendet werden.


## Eine Kollisionsobjekt-Komponente hinzufügen {#adding-a-collision-object-component}

Eine Kollisionsobjekt-Komponente hat eine Reihe von *Properties*, die ihren Typ und ihre physikalischen Eigenschaften festlegen. Außerdem enthält sie eine oder mehrere *Shapes*, die zusammen die gesamte Form des Physikobjekts bestimmen.

So fügst du einem Spielobjekt eine Kollisionsobjekt-Komponente hinzu:

1. Klicke in der Ansicht *Outline* <kbd>mit der rechten Maustaste</kbd> auf das Spielobjekt und wähle im Kontextmenü <kbd>Add Component ▸ Collision Object</kbd>. Dadurch wird eine neue Komponente ohne Formen erstellt.
2. Klicke <kbd>mit der rechten Maustaste</kbd> auf die neue Komponente und wähle <kbd>Add Shape</kbd>. Wähle anschließend eine Form: <kbd>Box</kbd>, <kbd>Capsule</kbd>, <kbd>Sphere</kbd>, <kbd>Hull</kbd> oder <kbd>Mesh</kbd> in Projekten mit 3D-Physik, <kbd>Box</kbd> oder <kbd>Circle</kbd> in Projekten mit 2D-Physik. Die Formen Hull und Mesh sind seit Defold 1.13.2 verfügbar und verwenden ein benanntes Mesh aus einer glTF- oder GLB-Szene. Du kannst der Komponente mehrere Formen hinzufügen. Über die Eigenschaft *Collision Shape* kannst du auch eine Kachelkarte (tile map) oder eine `.convexshape`-Ressource verwenden.
3. Verwende die Werkzeuge zum Verschieben, Drehen und Skalieren, um die Formen zu bearbeiten.
4. Wähle die Komponente in *Outline* aus und bearbeite die *Properties* des Kollisionsobjekts.

![Physikalisches Kollisionsobjekt](images/physics/collision_object.png)


## Eine Kollisionsform hinzufügen {#adding-a-collision-shape}

Eine Kollisionskomponente kann mehrere eingebettete Formen enthalten, darunter Hüllen und Dreiecks-Meshes bei 3D-Physik, oder eine Kachelkarte beziehungsweise eine Ressource für eine konvexe Form verwenden. Mehr über die verschiedenen Formen und wie du sie einer Kollisionskomponente hinzufügst, erfährst du im [Handbuch zu Kollisionsformen](/manuals/physics-shapes).


## Eigenschaften von Kollisionsobjekten {#collision-object-properties}

Id
: Die Kennung der Komponente.

Collision Shape
: Eine Kachelkarte oder eine `.convexshape`-Ressource. Um ein glTF- oder GLB-Mesh zu verwenden, füge der Komponente eine Form vom Typ Hull oder Mesh hinzu und lege stattdessen die Eigenschaften *Scene* und *Mesh* dieser Form fest. Weitere Informationen findest du unter [Kollisionsformen](/manuals/physics-shapes).

Type
: Der Typ des Kollisionsobjekts: `Dynamic`, `Kinematic`, `Static` oder `Trigger`. Wenn du das Objekt auf `Dynamic` setzt, _musst_ du die Eigenschaft *Mass* auf einen Wert ungleich null setzen. Bei Objekten vom Typ `Dynamic` oder `Static` solltest du außerdem prüfen, ob die Werte von *Friction* und *Restitution* für deinen Anwendungsfall geeignet sind.

Friction
: Reibung ermöglicht es Objekten, realistisch aneinander entlangzugleiten. Der Reibungswert liegt normalerweise zwischen `0` (keine Reibung---ein sehr rutschiges Objekt) und `1` (starke Reibung---ein raues Objekt). Es ist jedoch jeder positive Wert zulässig.

  Die Stärke der Reibung ist proportional zur Normalkraft (dies wird als Coulomb-Reibung bezeichnet). Wenn die Reibungskraft zwischen zwei Formen (`A` und `B`) berechnet wird, werden die Reibungswerte beider Objekte über das geometrische Mittel kombiniert:

```math
F = sqrt( F_A * F_B )
```

  Wenn eines der Objekte keine Reibung hat, ist der Kontakt zwischen ihnen also ebenfalls reibungsfrei.

Restitution
: Der Rückprallkoeffizient legt fest, wie stark das Objekt abprallt. Der Wert liegt normalerweise zwischen 0 (unelastischer Stoß—das Objekt prallt überhaupt nicht ab) und 1 (vollkommen elastischer Stoß---die Geschwindigkeit des Objekts wird beim Abprallen exakt gespiegelt).

  Die Rückprallkoeffizienten zweier Formen (`A` und `B`) werden mit folgender Formel kombiniert:

```math
R = max( R_A, R_B )
```

  Wenn eine Form mehrere Kontakte hat, wird der Rückprall nur näherungsweise simuliert, da Box2D einen iterativen Solver verwendet. Box2D verwendet bei geringer Kollisionsgeschwindigkeit außerdem unelastische Stöße, um Zittern durch wiederholtes Abprallen zu verhindern.

Linear damping
: Lineare Dämpfung verringert die lineare Geschwindigkeit des Körpers. Sie unterscheidet sich von Reibung, die nur bei Kontakt auftritt, und kann Objekten ein schwebendes Erscheinungsbild verleihen, als bewegten sie sich durch etwas Zähflüssigeres als Luft. Zulässige Werte liegen zwischen 0 und 1.

  Box2D berechnet die Dämpfung aus Gründen der Stabilität und Leistung näherungsweise. Bei kleinen Werten ist die Dämpfungswirkung unabhängig vom Zeitschritt, während sie bei größeren Dämpfungswerten mit dem Zeitschritt variiert. Wenn dein Spiel mit einem festen Zeitschritt läuft, stellt dies kein Problem dar.

Angular damping
: Winkeldämpfung funktioniert wie lineare Dämpfung, verringert aber die Winkelgeschwindigkeit des Körpers. Zulässige Werte liegen zwischen 0 und 1.

Locked rotation
: Wenn du diese Eigenschaft aktivierst, wird die Drehung des Kollisionsobjekts vollständig unterbunden, unabhängig davon, welche Kräfte darauf wirken.

Bullet
: Wenn du diese Eigenschaft aktivierst, wird die kontinuierliche Kollisionserkennung (CCD) zwischen dem Kollisionsobjekt und anderen dynamischen Kollisionsobjekten eingeschaltet. Die Eigenschaft *Bullet* wird ignoriert, wenn *Type* nicht auf `Dynamic` gesetzt ist.

Group
: Der Name der Kollisionsgruppe, der das Objekt angehören soll. Du kannst 16 verschiedene Gruppen verwenden und sie so benennen, wie es für dein Spiel passt, zum Beispiel `players`, `bullets`, `enemies` und `world`. Wenn *Collision Shape* auf eine Kachelkarte gesetzt ist, wird dieses Feld nicht verwendet. Stattdessen werden die Gruppennamen aus der Kachelquelle übernommen. [Erfahre mehr über Kollisionsgruppen](/manuals/physics-groups).

Mask
: Die anderen _Gruppen_, mit denen dieses Objekt kollidieren soll. Du kannst eine Gruppe angeben oder mehrere Gruppen in einer durch Kommas getrennten Liste aufführen. Wenn du das Feld *Mask* leer lässt, kollidiert das Objekt mit nichts. [Erfahre mehr über Kollisionsgruppen](/manuals/physics-groups).

Generate Collision Events
: Wenn diese Eigenschaft aktiviert ist, kann das Objekt Kollisionsereignisse senden.

Generate Contact Events
: Wenn diese Eigenschaft aktiviert ist, kann das Objekt Kontaktereignisse senden.

Generate Trigger Events
: Wenn diese Eigenschaft aktiviert ist, kann das Objekt Trigger-Ereignisse senden.


## Eigenschaften zur Laufzeit {#runtime-properties}

Ein Physikobjekt hat verschiedene Eigenschaften, die mit `go.get()` und `go.set()` gelesen und geändert werden können:

`angular_damping`
: Der Wert der Winkeldämpfung der Kollisionsobjekt-Komponente (`number`). [API-Referenz](/ref/physics/#angular_damping).

`angular_velocity`
: Die aktuelle Winkelgeschwindigkeit der Kollisionsobjekt-Komponente (`vector3`). [API-Referenz](/ref/physics/#angular_velocity).

`linear_damping`
: Der Wert der linearen Dämpfung des Kollisionsobjekts (`number`). [API-Referenz](/ref/physics/#linear_damping).

`linear_velocity`
: Die aktuelle lineare Geschwindigkeit der Kollisionsobjekt-Komponente (`vector3`). [API-Referenz](/ref/physics/#linear_velocity).

`mass`
: Die festgelegte physikalische Masse der Kollisionsobjekt-Komponente. NUR LESBAR. (`number`). [API-Referenz](/ref/physics/#mass).
