---
title: Komponenten von Spielobjekten
brief: Dieses Handbuch gibt einen Überblick über die Komponenten und ihre Verwendung.
---

#  Komponenten {#components}

:[components](../shared/components.md)

## Komponententypen {#component-types}

Defold unterstützt die folgenden Komponententypen:

* [Sammlungsfabrik (collection factory)](/manuals/collection-factory) - Sammlungen (collections) dynamisch erzeugen
* [Sammlungs-Proxy (collection proxy)](/manuals/collection-proxy) - Sammlungen laden und entladen
* [Kollisionsobjekt (collision object)](/manuals/physics) - 2D- und 3D-Physik
* [Kamera (camera)](/manuals/camera) - Den Ansichtsbereich (viewport) und die Projektion der Spielwelt ändern
* [Fabrik (factory)](/manuals/factory) - Spielobjekte dynamisch erzeugen
* [GUI](/manuals/gui) - Eine grafische Benutzeroberfläche rendern
* [Beschriftung (label)](/manuals/label) - Einen Text rendern
* [Licht (light)](/manuals/light) - Lichtdaten für Shader hinzufügen
* [Mesh](/manuals/mesh) Ein 3D-Mesh anzeigen (mit Erstellung und Bearbeitung zur Laufzeit)
* [Modell (model)](/manuals/model) Ein 3D-Modell anzeigen (mit optionalen Animationen)
* [Partikeleffekt (Particle FX)](/manuals/particlefx) -  Partikel dynamisch erzeugen
* [Skript (script)](/manuals/script) - Spiellogik hinzufügen
* [Audiokomponente (sound)](/manuals/sound) - Audio oder Musik abspielen
* [Sprite](/manuals/sprite) - Ein 2D-Bild anzeigen (mit optionaler Flipbook-Animation)
* [Kachelkarte (tile map)](/manuals/tilemap) - Ein Raster aus Kacheln anzeigen

Weitere Komponenten können durch Erweiterungen hinzugefügt werden:

* [Rive-Modell](/extension-rive) - Eine Rive-Animation rendern
* [Spine-Modell](/extension-spine) - Eine Spine-Animation rendern


## Komponenten aktivieren und deaktivieren {#enabling-and-disabling-components}

Die Komponenten eines Spielobjekts werden bei dessen Erstellung aktiviert. Wenn du eine Komponente deaktivieren möchtest, sende eine [`disable`](/ref/go/#disable)-Nachricht an die Komponente:

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

Um eine Komponente wieder zu aktivieren, kannst du eine [`enable`](/ref/go/#enable)-Nachricht an die Komponente senden:

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Komponenteneigenschaften {#component-properties}

Die Komponententypen von Defold haben jeweils unterschiedliche Eigenschaften. Der Bereich [Properties](/manuals/editor/#the-editor-views) im Editor zeigt die Eigenschaften der Komponente an, die gerade im Bereich [Outline](/manuals/editor/#the-editor-views) ausgewählt ist. In den Handbüchern zu den einzelnen Komponententypen erfährst du mehr über die verfügbaren Komponenteneigenschaften.

## Position, Drehung und Skalierung von Komponenten {#component-position-rotation-and-scale}

Visuelle Komponenten haben normalerweise Eigenschaften für Position und Drehung und meist auch eine Eigenschaft für die Skalierung. Du kannst diese Eigenschaften im Editor ändern. In fast allen Fällen lassen sie sich jedoch nicht zur Laufzeit ändern (die einzige Ausnahme ist die Skalierung von Sprite- und Beschriftungskomponenten, die zur Laufzeit geändert werden kann).

Wenn du die Position, Drehung oder Skalierung einer Komponente zur Laufzeit ändern musst, änderst du stattdessen die Position, Drehung oder Skalierung des Spielobjekts, zu dem die Komponente gehört. Das wirkt sich auch auf alle anderen Komponenten dieses Spielobjekts aus. Wenn du nur eine einzelne von mehreren Komponenten eines Spielobjekts verändern möchtest, wird empfohlen, diese Komponente in ein separates Spielobjekt zu verschieben. Füge dieses dann als untergeordnetes Spielobjekt dem Spielobjekt hinzu, zu dem die Komponente ursprünglich gehörte.

## Zeichenreihenfolge von Komponenten {#component-draw-order}

Die Zeichenreihenfolge visueller Komponenten hängt von zwei Dingen ab:

### Prädikate im Render-Skript {#render-script-predicates}
Jeder Komponente ist ein [Material](/manuals/material/) zugewiesen, und jedes Material hat ein oder mehrere Tags. Das Render-Skript definiert wiederum eine Reihe von Prädikaten, die jeweils einem oder mehreren Material-Tags entsprechen. Die [Prädikate werden nacheinander](/manuals/render/#render-predicates) in der Funktion *update()* des Render-Skripts gezeichnet. Dabei werden jeweils die Komponenten gezeichnet, die den im Prädikat definierten Tags entsprechen. Das standardmäßige Render-Skript zeichnet zuerst Sprites und Kachelkarten in einem Durchlauf, dann Partikeleffekte in einem weiteren Durchlauf, jeweils im Weltkoordinatensystem. Anschließend zeichnet das Render-Skript GUI-Komponenten in einem separaten Durchlauf im Bildschirmkoordinatensystem.

### Z-Wert von Komponenten {#component-z-value}
Alle Spielobjekte und Komponenten sind im 3D-Raum positioniert, wobei ihre Positionen als `vector3`-Objekte angegeben werden. Wenn du den grafischen Inhalt deines Spiels in 2D betrachtest, bestimmen der X- und der Y-Wert die Position eines Objekts entlang der Achsen für „Breite“ und „Höhe“. Die Z-Position bestimmt die Position entlang der „Tiefenachse“. Mit der Z-Position kannst du die Sichtbarkeit überlappender Objekte steuern: Ein Sprite mit einem Z-Wert von 1 erscheint vor einem Sprite an der Z-Position 0. Standardmäßig verwendet Defold ein Koordinatensystem, das Z-Werte zwischen -1 und 1 zulässt:

![Modell](images/graphics/z-order.png)

Die Komponenten, die einem [Render-Prädikat](/manuals/render/#render-predicates) entsprechen, werden gemeinsam gezeichnet. Ihre Zeichenreihenfolge hängt vom endgültigen Z-Wert der jeweiligen Komponente ab. Der endgültige Z-Wert einer Komponente ist die Summe der Z-Werte der Komponente selbst, des Spielobjekts, zu dem sie gehört, und aller übergeordneten Spielobjekte.

::: sidenote
Die Reihenfolge, in der mehrere GUI-Komponenten gezeichnet werden, wird **nicht** durch den Z-Wert der GUI-Komponenten bestimmt. Die Zeichenreihenfolge der GUI-Komponenten wird durch die Funktion [gui.set_render_order()](/ref/gui/#gui.set_render_order:order) gesteuert.
:::

Beispiel: Zwei Spielobjekte A und B. B ist A untergeordnet. B hat eine Sprite-Komponente.

| Objekt   | Z-Wert  |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Bei der obigen Hierarchie beträgt der endgültige Z-Wert der Sprite-Komponente von B: 2 + 1 + 0.5 = 3.5.

::: important
Wenn zwei Komponenten genau denselben Z-Wert haben, ist ihre Reihenfolge nicht definiert. Dadurch können die Komponenten abwechselnd voreinander erscheinen und flackern oder auf verschiedenen Plattformen in unterschiedlicher Reihenfolge gerendert werden.

Das Render-Skript definiert eine nahe und eine ferne Begrenzungsebene für Z-Werte. Komponenten mit einem Z-Wert außerhalb dieses Bereichs werden nicht gerendert. Der Standardbereich reicht von -1 bis 1, [kann aber leicht geändert werden](/manuals/render/#default-view-projection). Die numerische Genauigkeit der Z-Werte ist bei einer nahen und fernen Grenze von -1 und 1 sehr hoch. Wenn du mit 3D-Assets arbeitest, musst du möglicherweise die nahe und ferne Grenze der Standardprojektion in einem eigenen Render-Skript ändern. Weitere Informationen findest du im [Rendering-Handbuch](/manuals/render/).
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
