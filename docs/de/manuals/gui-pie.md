---
title: GUI-Kreissektor-Knoten in Defold
brief: Dieses Handbuch erklärt, wie du Kreissektor-Knoten in GUI-Szenen von Defold verwendest.
---

# GUI-Kreissektor-Knoten {#gui-pie-nodes}

Mit Kreissektor-Knoten (pie nodes) kannst du kreisförmige oder ellipsenförmige Objekte erstellen, von einfachen Kreisen über Kreissektoren bis hin zu quadratischen Ringformen.

## Einen Kreissektor-Knoten erstellen {#creating-a-pie-node}

Klicke mit der <kbd>rechten Maustaste</kbd> auf den Bereich *Nodes* in der Ansicht *Outline* und wähle <kbd>Add ▸ Pie</kbd>. Der neue Kreissektor-Knoten ist ausgewählt und du kannst seine Eigenschaften ändern.

![Kreissektor-Knoten erstellen](images/gui-pie/create.png)

Die folgenden Eigenschaften gibt es nur bei Kreissektor-Knoten:

Inner Radius
: Der innere Radius des Knotens, angegeben entlang der X-Achse.

Outer Bounds
: Die Form der äußeren Begrenzung des Knotens.

  - `Ellipse` erweitert den Knoten bis zum äußeren Radius.
  - `Rectangle` erweitert den Knoten bis zu seinem Begrenzungsrechteck.

Perimeter Vertices
: Die Anzahl der Segmente, aus denen die Form aufgebaut wird, angegeben als Anzahl der Vertices, die benötigt werden, um den vollständigen Umfang des Knotens von 360 Grad zu umschreiben.

Pie Fill Angle
: Wie viel des Kreissektors gefüllt werden soll. Angegeben als Winkel gegen den Uhrzeigersinn, ausgehend von rechts.

![Eigenschaften](images/gui-pie/properties.png)

Wenn du dem Knoten eine Textur zuweist, wird das Texturbild flächig aufgebracht. Dabei entsprechen die Ecken der Textur den Ecken des Begrenzungsrechtecks des Knotens.

## Kreissektor-Knoten zur Laufzeit ändern {#modify-pie-nodes-at-runtime}

Kreissektor-Knoten unterstützen alle allgemeinen Funktionen zur Bearbeitung von Knoten, etwa zum Festlegen von Größe, Bezugspunkt (pivot), Farbe und so weiter. Außerdem gibt es einige Funktionen und Eigenschaften, die nur für Kreissektor-Knoten gelten:

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
