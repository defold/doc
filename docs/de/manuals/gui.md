---
title: GUI-Szenen in Defold
brief: Dieses Handbuch behandelt den GUI-Editor von Defold, die verschiedenen Arten von GUI-Knoten und GUI-Skripte.
---

# GUI

Defold bietet dir einen eigens entwickelten GUI-Editor und leistungsfähige Skriptmöglichkeiten, die auf die Gestaltung und Implementierung von Benutzeroberflächen zugeschnitten sind.

Eine grafische Benutzeroberfläche in Defold ist eine Komponente (component), die du erstellst, einem Spielobjekt (game object) hinzufügst und in einer Sammlung (collection) platzierst. Diese Komponente hat die folgenden Eigenschaften:

* Sie bietet einfache, aber leistungsfähige Layoutfunktionen, mit denen deine Benutzeroberfläche unabhängig von Auflösung und Seitenverhältnis gerendert werden kann.
* Du kannst ihr durch ein *GUI-Skript (GUI script)* ein logisches Verhalten geben.
* Sie wird (standardmäßig) über anderen Inhalten gerendert, unabhängig von der Kameraansicht. Auch wenn sich deine Kamera bewegt, bleiben deine GUI-Elemente also an ihrer Position auf dem Bildschirm. Das Rendering-Verhalten lässt sich ändern.

GUI-Komponenten werden unabhängig von der Spielansicht gerendert. Deshalb werden sie nicht an einer bestimmten Position im Sammlungseditor platziert und haben dort auch keine visuelle Darstellung. GUI-Komponenten müssen jedoch zu einem Spielobjekt gehören, das eine Position in einer Sammlung hat. Das Ändern dieser Position hat keine Auswirkung auf die GUI.

## Eine GUI-Komponente erstellen {#creating-a-gui-component}

GUI-Komponenten werden aus einer Prototypdatei für eine GUI-Szene erstellt (in anderen Engines auch als „Prefabs“ oder „Baupläne“ bekannt). Um eine neue GUI-Komponente zu erstellen, klicke mit der <kbd>rechten Maustaste</kbd> auf eine Stelle im Browser *Assets* und wähle <kbd>New ▸ Gui</kbd>. Gib einen Namen für die neue GUI-Datei ein und drücke <kbd>Ok</kbd>.

![Neue GUI-Datei](images/gui/new_gui_file.png)

Defold öffnet die Datei nun automatisch im GUI-Szeneneditor.

![Neue GUI](images/gui/new_gui.png)

Die Ansicht *Outline* listet den gesamten Inhalt der GUI auf: die Liste ihrer Knoten (nodes) und alle Abhängigkeiten (siehe unten).

Der zentrale Bearbeitungsbereich zeigt die GUI. Die Werkzeugleiste oben rechts im Bearbeitungsbereich enthält die Werkzeuge *Move*, *Rotate* und *Scale* sowie eine Auswahl für das [Layout](/manuals/gui-layouts).

![Werkzeugleiste](images/gui/toolbar.png)

Ein weißes Rechteck zeigt die Grenzen des aktuell ausgewählten Layouts mit der standardmäßigen Anzeigebreite und -höhe aus den Projekteinstellungen.

## GUI-Eigenschaften {#gui-properties}

Wenn du den Wurzelknoten „Gui“ in der Ansicht *Outline* auswählst, zeigt *Properties* die Eigenschaften der GUI-Komponente an:

*Script*
: Das GUI-Skript, das an diese GUI-Komponente gebunden ist.

*Material*
: Das Material, das beim Rendern dieser GUI verwendet wird. Beachte, dass du einer GUI über den Bereich *Outline* auch mehrere Materialien hinzufügen und diese einzelnen Knoten zuweisen kannst.

*Adjust Reference*
: Steuert, wie der *Adjust Mode* jedes Knotens berechnet werden soll:

  - `Per Node` passt jeden Knoten an die angepasste Größe des übergeordneten Knotens oder an den Bildschirm mit geänderter Größe an.
  - `Disable` schaltet den Anpassungsmodus der Knoten aus. Dadurch behalten alle Knoten ihre eingestellte Größe bei.

*Current Nodes*
: Die Anzahl der Knoten, die derzeit in dieser GUI verwendet werden.

*Max Nodes*
: Die maximale Anzahl der Knoten für diese GUI.

*Max Dynamic Textures*
: Die maximale Anzahl dynamischer Texturen, die diese GUI-Komponente verwaltet, standardmäßig `128`. Dazu gehören Texturen, die mit [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) erstellt werden, sowie externe Texturen, die der GUI mit `go.set(..., "textures", ...)` oder `gui.set(msg.url(), "textures", ...)` zugewiesen werden. Projekte, die viele externe Texturen ersetzen, müssen diesen Grenzwert möglicherweise erhöhen.


## Änderungen zur Laufzeit {#runtime-manipulation}

Du kannst GUI-Eigenschaften zur Laufzeit aus einer Skriptkomponente heraus mit `go.get()` und `go.set()` ändern:

Schriftarten
: Eine in einer GUI verwendete Schriftart abrufen oder festlegen.

![Schriftart abrufen und festlegen](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- get the font file currently assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- set the font with id 'default' to the font file assigned to the resource property 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- get the new font file assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materialien
: Ein in einer GUI verwendetes Material abrufen oder festlegen.

![Material abrufen und festlegen](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- get the material file currently assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- set the material id 'effect' to the material file assigned to the resource property 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- get the new material file assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Texturen
: Eine in einer GUI verwendete Textur (Atlas) abrufen oder festlegen.

![Textur abrufen und festlegen](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- get the texture file currently assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- set the texture with id 'theme' to the texture file assigned to the resource property 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- get the new texture file assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Abhängigkeiten {#dependencies}

Der Ressourcenbaum eines Defold-Spiels ist statisch. Daher musst du alle Abhängigkeiten, die du für deine GUI-Knoten benötigst, zur Komponente hinzufügen. Die Ansicht *Outline* gruppiert alle Abhängigkeiten nach Typ in „Ordnern“:

![Abhängigkeiten](images/gui/dependencies.png)

Um eine neue Abhängigkeit hinzuzufügen, ziehe sie aus dem Bereich *Asset* in die Editoransicht und lege sie dort ab.

Alternativ kannst du mit der <kbd>rechten Maustaste</kbd> auf den Wurzelknoten „Gui“ in der Ansicht *Outline* klicken und anschließend <kbd>Add ▸ [type]</kbd> aus dem eingeblendeten Kontextmenü wählen.

Du kannst auch mit der <kbd>rechten Maustaste</kbd> auf das Ordnersymbol des Typs klicken, den du hinzufügen möchtest, und <kbd>Add ▸ [type]</kbd> wählen.

## Knotentypen {#node-types}

Eine GUI-Komponente besteht aus einer Menge von Knoten. Knoten sind einfache Elemente. Du kannst sie entweder im Editor oder zur Laufzeit per Skript transformieren (verschieben, skalieren und drehen) und in Eltern-Kind-Hierarchien anordnen. Es gibt die folgenden Knotentypen:

Box-Knoten
: ![Box-Knoten](images/icons/gui-box-node.png){.left}
  Rechteckiger Knoten mit einer einzelnen Farbe, einer Textur oder einer Flipbook-Animation. Einzelheiten findest du in der [Dokumentation zu Box-Knoten](/manuals/gui-box).

<div style="clear: both;"></div>

Textknoten
: ![Textknoten](images/icons/gui-text-node.png){.left}
  Zeigt Text an. Einzelheiten findest du in der [Dokumentation zu Textknoten](/manuals/gui-text).

<div style="clear: both;"></div>

Kreissektor-Knoten
: ![Kreissektor-Knoten](images/icons/gui-pie-node.png){.left}
  Ein kreisförmiger oder elliptischer Knoten, der teilweise gefüllt oder invertiert werden kann. Einzelheiten findest du in der [Dokumentation zu Kreissektor-Knoten](/manuals/gui-pie).

<div style="clear: both;"></div>

Vorlagenknoten
: ![Vorlagenknoten](images/icons/gui.png){.left}
  Vorlagen werden verwendet, um Instanzen auf Basis anderer GUI-Szenendateien zu erstellen. Einzelheiten findest du in der [Dokumentation zu Vorlagenknoten](/manuals/gui-template).

<div style="clear: both;"></div>

Partikeleffektknoten
: ![Partikeleffektknoten](images/icons/particlefx.png){.left}
  Spielt einen Partikeleffekt ab. Einzelheiten findest du in der [Dokumentation zu Partikeleffektknoten](/manuals/gui-particlefx).

<div style="clear: both;"></div>

Füge Knoten hinzu, indem du mit der rechten Maustaste auf den Ordner *Nodes* klickst und <kbd>Add ▸</kbd> und anschließend <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> oder <kbd>ParticleFx</kbd> wählst.

![Knoten hinzufügen](images/gui/add_node.png)

Du kannst auch <kbd>A</kbd> drücken und den Typ auswählen, den du der GUI hinzufügen möchtest.

## Knoteneigenschaften {#node-properties}

Jeder Knoten verfügt über eine umfangreiche Menge von Eigenschaften, die sein Aussehen steuern:

Id
: Der Bezeichner des Knotens. Dieser Name muss innerhalb der GUI-Szene eindeutig sein.

Position, Rotation und Scale
: Steuern die Position, Ausrichtung und Streckung des Knotens. Du kannst die Werkzeuge *Move*, *Rotate* und *Scale* verwenden, um diese Werte zu ändern. Die Werte lassen sich per Skript animieren ([mehr erfahren](/manuals/property-animation)).

Size (Box-Knoten, Textknoten und Kreissektor-Knoten)
: Die Größe des Knotens wird standardmäßig automatisch festgelegt. Wenn du *Size Mode* auf `Manual` setzt, kannst du den Wert jedoch ändern. Die Größe legt die Grenzen des Knotens fest und wird verwendet, um Knoten bei Eingaben zu ermitteln. Dieser Wert lässt sich per Skript animieren ([mehr erfahren](/manuals/property-animation)).

Size Mode (Box- und Kreissektor-Knoten)
: Bei `Automatic` legt der Editor eine Größe für den Knoten fest. Bei `Manual` kannst du die Größe selbst festlegen.

Enabled
: Wenn dieses Kontrollkästchen nicht aktiviert ist, wird der Knoten weder gerendert noch animiert und kann nicht mit `gui.pick_node()` ermittelt werden. Verwende `gui.set_enabled()` und `gui.is_enabled()`, um diese Eigenschaft per Code zu ändern und zu prüfen.

Visible
: Wenn dieses Kontrollkästchen nicht aktiviert ist, wird der Knoten nicht gerendert, kann aber weiterhin animiert und mit `gui.pick_node()` ermittelt werden. Verwende `gui.set_visible()` und `gui.get_visible()`, um diese Eigenschaft per Code zu ändern und zu prüfen.

Text (Textknoten)
: Der Text, der auf dem Knoten angezeigt werden soll.

Line Break (Textknoten)
: Aktivieren, damit der Text entsprechend der Breite des Knotens umgebrochen wird.

Font (Textknoten)
: Die Schriftart, die beim Rendern des Textes verwendet werden soll.

Texture (Box- und Kreissektor-Knoten)
: Die Textur, die auf dem Knoten gezeichnet werden soll. Dies ist eine Referenz auf ein Bild oder eine Animation in einem Atlas oder einer Kachelquelle (tile source).

Material (Box-Knoten, Kreissektor-Knoten, Textknoten und Partikeleffektknoten)
: Das Material, das beim Zeichnen des Knotens verwendet werden soll. Du kannst hier ein Material angeben, das dem Abschnitt Materials in der Ansicht *Outline* hinzugefügt wurde, oder das Feld leer lassen, um das Standardmaterial der GUI-Komponente zu verwenden.

Slice 9 (Box-Knoten)
: Aktivieren, um die Pixelgröße der Knotentextur an den Rändern beizubehalten, wenn die Größe des Knotens geändert wird. Einzelheiten findest du in der [Dokumentation zu Box-Knoten](/manuals/gui-box).

Inner Radius (Kreissektor-Knoten)
: Der innere Radius des Knotens, angegeben entlang der X-Achse. Einzelheiten findest du in der [Dokumentation zu Kreissektor-Knoten](/manuals/gui-pie).

Outer Bounds (Kreissektor-Knoten)
: Steuert das Verhalten der äußeren Grenzen. Einzelheiten findest du in der [Dokumentation zu Kreissektor-Knoten](/manuals/gui-pie).

Perimeter Vertices (Kreissektor-Knoten)
: Die Anzahl der Segmente, aus denen die Form aufgebaut wird. Einzelheiten findest du in der [Dokumentation zu Kreissektor-Knoten](/manuals/gui-pie).

Pie Fill Angle (Kreissektor-Knoten)
: Wie viel des Kreissektors gefüllt werden soll. Einzelheiten findest du in der [Dokumentation zu Kreissektor-Knoten](/manuals/gui-pie).

Template (Vorlagenknoten)
: Die GUI-Szenendatei, die als Vorlage für den Knoten verwendet werden soll. Einzelheiten findest du in der [Dokumentation zu Vorlagenknoten](/manuals/gui-template).

ParticleFX (Partikeleffektknoten)
: Der Partikeleffekt, der auf diesem Knoten verwendet werden soll. Einzelheiten findest du in der [Dokumentation zu Partikeleffektknoten](/manuals/gui-particlefx).

Color
: Die Farbe des Knotens. Wenn der Knoten eine Textur hat, färbt die Farbe diese Textur ein. Die Farbe lässt sich per Skript animieren ([mehr erfahren](/manuals/property-animation)).

Alpha
: Die Transparenz des Knotens. Der Alphawert lässt sich per Skript animieren ([mehr erfahren](/manuals/property-animation)).

Inherit Alpha
: Wenn du dieses Kontrollkästchen aktivierst, erbt ein Knoten den Alphawert des übergeordneten Knotens. Der Alphawert des Knotens wird dann mit dem Alphawert des übergeordneten Knotens multipliziert.

Leading (Textknoten)
: Ein Skalierungsfaktor für den Zeilenabstand. Ein Wert von `0` ergibt keinen Zeilenabstand. `1` (der Standardwert) ergibt den normalen Zeilenabstand.

Tracking (Textknoten)
: Ein Skalierungsfaktor für den Zeichenabstand. Der Standardwert ist 0.

Layer
: Wenn du dem Knoten eine Ebene zuweist, wird die normale Zeichenreihenfolge überschrieben und stattdessen die Reihenfolge der Ebenen verwendet. Einzelheiten findest du weiter unten.

Blend mode
: Steuert, wie die Grafik des Knotens mit der Hintergrundgrafik gemischt wird:
  - `Alpha` mischt die Pixelwerte des Knotens anhand des Alphawerts mit dem Hintergrund. Dies entspricht dem Mischmodus „Normal“ in Grafikprogrammen.
  - `Add` addiert die Pixelwerte des Knotens zu denen des Hintergrunds. Dies entspricht „Linear dodge“ in manchen Grafikprogrammen.
  - `Multiply` multipliziert die Pixelwerte des Knotens mit denen des Hintergrunds.
  - `Screen` multipliziert die Pixelwerte des Knotens mit denen des Hintergrunds invers. Dies entspricht dem Mischmodus „Screen“ in Grafikprogrammen.

Pivot
: Legt den Bezugspunkt (pivot) für den Knoten fest. Dieser kann als „Mittelpunkt“ des Knotens betrachtet werden. Jede Drehung, Skalierung oder Größenänderung erfolgt um diesen Punkt.

  Mögliche Werte sind `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` oder `South East`.

  ![Bezugspunkt](images/gui/pivot.png)

  Wenn du den Bezugspunkt eines Knotens änderst, wird der Knoten so verschoben, dass sich der neue Bezugspunkt an der Position des Knotens befindet. Textknoten werden so ausgerichtet, dass `Center` den Text zentriert, `West` ihn linksbündig und `East` ihn rechtsbündig ausrichtet.

X Anchor, Y Anchor
: Die Verankerung steuert, wie die vertikale und horizontale Position des Knotens geändert wird, wenn die Grenzen der Szene oder des übergeordneten Knotens gestreckt werden, um sie an die physische Bildschirmgröße anzupassen.

  ![Verankerung ohne Anpassung](images/gui/anchoring_unadjusted.png)

  Die folgenden Verankerungsmodi sind verfügbar:

  - `None` (sowohl für *X Anchor* als auch für *Y Anchor*) behält die Position des Knotens vom Mittelpunkt des übergeordneten Knotens oder der Szene aus relativ zu dessen bzw. deren *angepasster* Größe bei.
  - `Left` oder `Right` (*X Anchor*) skaliert die horizontale Position des Knotens so, dass der prozentuale Abstand zum linken und rechten Rand des übergeordneten Knotens oder der Szene gleich bleibt.
  - `Top` oder `Bottom` (*Y Anchor*) skaliert die vertikale Position des Knotens so, dass der prozentuale Abstand zum oberen und unteren Rand des übergeordneten Knotens oder der Szene gleich bleibt.

  ![Verankerung](images/gui/anchoring.png)

Adjust Mode
: Legt den Anpassungsmodus für den Knoten fest. Diese Einstellung steuert, was mit einem Knoten geschieht, wenn die Grenzen der Szene oder des übergeordneten Knotens an die physische Bildschirmgröße angepasst werden.

  Ein Knoten, der in einer Szene mit einer typischen logischen Auflösung im Querformat erstellt wurde:

  ![Ohne Anpassung](images/gui/unadjusted.png)

  Wenn die Szene an einen Bildschirm im Hochformat angepasst wird, wird sie gestreckt. Das Begrenzungsrechteck jedes Knotens wird auf dieselbe Weise gestreckt. Über den Anpassungsmodus lässt sich jedoch das Seitenverhältnis des Knoteninhalts beibehalten. Die folgenden Modi sind verfügbar:

  - `Fit` skaliert den Knoteninhalt so, dass er der Breite oder Höhe des gestreckten Begrenzungsrechtecks entspricht, je nachdem, welcher Wert kleiner ist. Mit anderen Worten: Der Inhalt passt vollständig in das gestreckte Begrenzungsrechteck des Knotens.
  - `Zoom` skaliert den Knoteninhalt so, dass er der Breite oder Höhe des gestreckten Begrenzungsrechtecks entspricht, je nachdem, welcher Wert größer ist. Mit anderen Worten: Der Inhalt bedeckt das gestreckte Begrenzungsrechteck des Knotens vollständig.
  - `Stretch` streckt den Knoteninhalt so, dass er das gestreckte Begrenzungsrechteck des Knotens ausfüllt.

  ![Anpassungsmodi](images/gui/adjusted.png)

  Wenn die Eigenschaft *Adjust Reference* der GUI-Szene auf `Disabled` gesetzt ist, wird diese Einstellung ignoriert.

Clipping Mode (Box- und Kreissektor-Knoten)
: Legt den Modus zum Beschneiden (Clipping) des Knotens fest:

  - `None` rendert den Knoten wie gewohnt.
  - `Stencil` lässt die Knotengrenzen eine Stencil-Maske definieren, mit der die untergeordneten Knoten beschnitten werden.

  Einzelheiten findest du im [Handbuch zum Beschneiden von GUIs](/manuals/gui-clipping).

Clipping Visible (Box- und Kreissektor-Knoten)
: Aktivieren, um den Inhalt des Knotens im Stencil-Bereich zu rendern. Einzelheiten findest du im [Handbuch zum Beschneiden von GUIs](/manuals/gui-clipping).

Clipping Inverted (Box- und Kreissektor-Knoten)
: Invertiert die Stencil-Maske. Einzelheiten findest du im [Handbuch zum Beschneiden von GUIs](/manuals/gui-clipping).


## Bezugspunkt, Verankerungen und Anpassungsmodus {#pivot-anchors-and-adjust-mode}

Die Kombination aus Bezugspunkt, Verankerungen und Anpassungsmodus ermöglicht eine sehr flexible Gestaltung von GUIs. Ohne ein konkretes Beispiel kann es jedoch etwas schwierig sein, ihr Zusammenspiel zu verstehen. Nehmen wir diesen GUI-Entwurf für einen Bildschirm mit 640 × 1136 Pixeln als Beispiel:

![](images/gui/adjustmode_example_original.png)

Die Benutzeroberfläche wurde erstellt, indem X Anchor und Y Anchor auf None gesetzt wurden und Adjust Mode für jeden Knoten auf dem Standardwert Fit belassen wurde. Der Bezugspunkt Pivot des oberen Bereichs ist North, der Bezugspunkt des unteren Bereichs ist South und die Bezugspunkte der Balken im oberen Bereich sind auf West gesetzt. Bei den übrigen Knoten sind die Bezugspunkte auf Center gesetzt. Wenn wir das Fenster verbreitern, geschieht Folgendes:

![](images/gui/adjustmode_example_resized.png)

Was ist nun, wenn der obere und der untere Balken immer so breit wie der Bildschirm sein sollen? Wir können Adjust Mode für die grauen Hintergrundbereiche oben und unten auf Stretch ändern:

![](images/gui/adjustmode_example_resized_stretch.png)

Das ist besser. Die grauen Hintergrundbereiche werden nun immer auf die Breite des Fensters gestreckt, aber die Balken im oberen Bereich und die beiden Rechtecke unten sind nicht richtig positioniert. Wenn die oberen Balken links positioniert bleiben sollen, müssen wir X Anchor von None auf Left ändern:

![](images/gui/adjustmode_example_top_anchor_left.png)

Genau so soll der obere Bereich aussehen. Die Bezugspunkte Pivot der Balken im oberen Bereich waren bereits auf West gesetzt. Dadurch werden die Balken passend positioniert: Ihr linker bzw. westlicher Rand (Pivot) ist am linken Rand des übergeordneten Bereichs verankert (X Anchor).

Wenn wir nun X Anchor für das linke Rechteck auf Left und X Anchor für das rechte Rechteck auf Right setzen, erhalten wir folgendes Ergebnis:

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Das ist nicht ganz das erwartete Ergebnis. Die beiden Rechtecke sollten genauso nahe am linken und rechten Rand bleiben wie die beiden Balken im oberen Bereich. Der Grund dafür ist der falsche Bezugspunkt Pivot:

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Bei beiden Rechtecken ist der Bezugspunkt Pivot auf Center gesetzt. Das bedeutet, dass der Mittelpunkt (der Bezugspunkt) der Rechtecke bei einer Verbreiterung des Bildschirms denselben relativen Abstand von den Rändern behält. Beim linken Rechteck betrug er im ursprünglichen Fenster mit 640 × 1136 Pixeln 17 % vom linken Rand:

![](images/gui/adjustmode_example_original_ratio.png)

Wenn die Bildschirmgröße geändert wird, bleibt der Mittelpunkt des linken Rechtecks beim selben Abstand von 17 % vom linken Rand:

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Wenn wir den Bezugspunkt Pivot für das linke Rechteck von Center auf West und für das rechte Rechteck auf East ändern und die Rechtecke neu positionieren, erhalten wir auch bei einer Änderung der Bildschirmgröße das gewünschte Ergebnis:

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Zeichenreihenfolge {#draw-order}

Alle Knoten werden in der Reihenfolge gerendert, in der sie im Ordner „Nodes“ aufgelistet sind. Der oberste Knoten in der Liste wird zuerst gezeichnet und erscheint daher hinter allen anderen Knoten. Der letzte Knoten in der Liste wird zuletzt gezeichnet und erscheint somit vor allen anderen Knoten. Das Ändern des Z-Werts eines Knotens steuert nicht seine Zeichenreihenfolge. Wenn du den Z-Wert jedoch außerhalb des Renderbereichs deines Render-Skripts setzt, wird der Knoten nicht mehr auf dem Bildschirm gerendert. Du kannst die Indexreihenfolge der Knoten mit Ebenen überschreiben (siehe unten).

![Zeichenreihenfolge](images/gui/draw_order.png)

Wähle einen Knoten aus und drücke <kbd>Alt + Up/Down</kbd>, um ihn nach oben oder unten zu verschieben und seine Indexreihenfolge zu ändern.

Die Zeichenreihenfolge lässt sich per Skript ändern:

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Eltern-Kind-Hierarchien {#parent-child-hierarchies}

Du ordnest einen Knoten einem anderen unter, indem du ihn auf den Knoten ziehst, der sein übergeordneter Knoten werden soll. Ein untergeordneter Knoten erbt die Transformation (Position, Drehung und Skalierung), die auf den übergeordneten Knoten angewendet wird, relativ zu dessen Bezugspunkt.

![Über- und untergeordnete Knoten](images/gui/parent_child.png)

Übergeordnete Knoten werden vor ihren untergeordneten Knoten gezeichnet. Verwende Ebenen, um die Zeichenreihenfolge über- und untergeordneter Knoten zu ändern und das Rendering der Knoten zu optimieren (siehe unten).


## Ebenen und Zeichenaufrufe {#layers-and-draw-calls}

Ebenen ermöglichen eine genaue Steuerung, wie Knoten gezeichnet werden, und können die Anzahl der Zeichenaufrufe (draw calls) verringern, die die Engine zum Zeichnen einer GUI-Szene erzeugen muss. Bevor die Engine die Knoten einer GUI-Szene zeichnet, bündelt sie deren Zeichenoperationen (Batching) anhand der folgenden Bedingungen:

- Die Knoten müssen denselben Typ verwenden.
- Die Knoten müssen denselben Atlas oder dieselbe Kachelquelle verwenden.
- Die Knoten müssen mit demselben Mischmodus gerendert werden.
- Sie müssen dieselbe Schriftart verwenden.

Wenn sich ein Knoten in einem dieser Punkte vom vorherigen unterscheidet, unterbricht er die Bündelung und erzeugt einen weiteren Zeichenaufruf. Beschneidende Knoten unterbrechen die Bündelung immer, ebenso jeder Stencil-Gültigkeitsbereich.

Die Möglichkeit, Knoten in Hierarchien anzuordnen, erleichtert die Gruppierung von Knoten zu überschaubaren Einheiten. Wenn du verschiedene Knotentypen mischst, können Hierarchien das gebündelte Rendern jedoch praktisch unterbinden:

![Hierarchie unterbricht die Bündelung](images/gui/break_batch.png)

Wenn die Rendering-Pipeline die Knotenliste durchläuft, muss sie für jeden einzelnen Knoten eine eigene Gruppe von Zeichenoperationen anlegen, weil sich die Typen unterscheiden. Insgesamt erfordern diese drei Schaltflächen sechs Zeichenaufrufe.

Indem du den Knoten Ebenen zuweist, kannst du sie anders anordnen. Dadurch kann die Rendering-Pipeline die Knoten in weniger Zeichenaufrufen zusammenfassen. Füge zunächst der Szene die benötigten Ebenen hinzu. Klicke mit der <kbd>rechten Maustaste</kbd> auf das Ordnersymbol „Layers“ in der Ansicht *Outline* und wähle <kbd>Add ▸ Layer</kbd>. Markiere die neue Ebene und weise ihr für die Eigenschaft *Name* in der Ansicht *Properties* einen Wert zu.

![Ebenen](images/gui/layers.png)

Setze anschließend die Eigenschaft *Layer* jedes Knotens auf die entsprechende Ebene. Die Zeichenreihenfolge der Ebenen hat Vorrang vor der regulären Indexreihenfolge der Knoten. Wenn du die Box-Knoten mit den Schaltflächengrafiken auf „graphics“ und die Textknoten der Schaltflächen auf „text“ setzt, ergibt sich daher folgende Zeichenreihenfolge:

* Zuerst alle Knoten der Ebene „graphics“, von oben nach unten:

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Dann alle Knoten der Ebene „text“, von oben nach unten:

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Die Knoten können nun in zwei statt sechs Zeichenaufrufen gebündelt werden. Ein großer Leistungsgewinn!

Beachte, dass ein untergeordneter Knoten ohne festgelegte Ebene die Ebeneneinstellung seines übergeordneten Knotens implizit erbt. Wenn du für einen Knoten keine Ebene festlegst, wird er implizit der Ebene „null“ hinzugefügt, die vor allen anderen Ebenen gezeichnet wird.
