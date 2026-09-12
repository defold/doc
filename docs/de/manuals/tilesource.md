---
title: Handbuch zu Kachelquellen in Defold
brief: Hier erfährst du, wie du eine Kachelquelle verwendest und erstellst.
---

# Kachelquelle {#tile-source}

Eine *Kachelquelle* (tile source) kann von einer [Kachelkartenkomponente (tile map component)](/manuals/tilemap) verwendet werden, um Kacheln auf eine Rasterfläche zu zeichnen, oder als Grafikquelle für ein [Sprite](/manuals/sprite) oder eine [Partikeleffektkomponente (particle effect component)](/manuals/particlefx) dienen. Du kannst auch die *Kollisionsformen* (collision shapes) der Kachelquelle in einer Kachelkarte für die [Kollisionserkennung und Physiksimulation](/manuals/physics) verwenden ([Beispiel](/examples/tilemap/collisions/)).

## Eine Kachelquelle erstellen {#creating-a-tile-source}

Du benötigst ein Bild, das alle Kacheln enthält. Jede Kachel muss genau dieselben Abmessungen haben und in einem Raster angeordnet sein. Defold unterstützt _Abstände_ zwischen den Kacheln und einen _Rand_ um jede Kachel.

![Kachelbild](images/tilemap/small_map.png)

Sobald du das Quellbild erstellt hast, kannst du eine Kachelquelle erstellen:

- Importiere das Bild in dein Projekt, indem du es an einen Speicherort im Projekt im Browser *Assets* ziehst.
- Erstelle eine neue Kachelquelldatei (<kbd>Rechtsklick</kbd> auf einen Speicherort im Browser *Assets*, dann <kbd>New... ▸ Tile Source</kbd> auswählen).
- Gib der neuen Datei einen Namen.
- Die Datei wird nun im Kachelquelleneditor geöffnet.
- Klicke auf die Schaltfläche zum Durchsuchen neben der Eigenschaft *Image* und wähle dein Bild aus. Jetzt solltest du das Bild im Editor sehen.
- Passe die *Properties* an das Quellbild an. Wenn alles richtig eingestellt ist, sind die Kacheln genau ausgerichtet.

![Eine Kachelquelle erstellen](images/tilemap/tilesource.png)

Size
: Die Größe des Quellbilds.

Tile Width
: Die Breite jeder Kachel.

Tile Height
: Die Höhe jeder Kachel.

Tile Margin
: Die Anzahl der Pixel, die jede Kachel umgeben (im Bild oben orange).

Tile Spacing
: Die Anzahl der Pixel zwischen den Kacheln (im Bild oben blau).

Inner Padding
: Legt fest, wie viele leere Pixel automatisch um die Kachel herum in der resultierenden Textur hinzugefügt werden sollen, die beim Ausführen des Spiels verwendet wird.

Extrude Border
: Legt fest, wie oft die Randpixel automatisch um die Kachel herum in der resultierenden Textur wiederholt werden sollen, die beim Ausführen des Spiels verwendet wird.

Collision
: Legt das Bild fest, mit dem automatisch Kollisionsformen für Kacheln erzeugt werden.

## Flipbook-Animationen einer Kachelquelle {#tile-source-flip-book-animations}

Um eine Animation in einer Kachelquelle zu definieren, müssen die Kacheln der Einzelbilder in einer Folge von links nach rechts nebeneinanderliegen. Die Folge kann von einer Zeile in die nächste übergehen. Alle neu erstellten Kachelquellen haben eine Standardanimation namens „`anim`“. Du kannst neue Animationen hinzufügen, indem du einen <kbd>Rechtsklick</kbd> auf den obersten Eintrag der Kachelquelle in der Ansicht *Outline* ausführst und <kbd>Add ▸ Animation</kbd> auswählst.

Wenn du eine Animation auswählst, werden ihre *Properties* angezeigt.

![Animation einer Kachelquelle](images/tilemap/animation.png)

Id
: Die Kennung der Animation. Sie muss innerhalb der Kachelquelle eindeutig sein.

Start Tile
: Die erste Kachel der Animation. Die Nummerierung beginnt bei 1 in der oberen linken Ecke und verläuft nach rechts, Zeile für Zeile bis zur unteren rechten Ecke.

End Tile
: Die letzte Kachel der Animation.

Playback
: Legt fest, wie die Animation abgespielt werden soll:

  - `None` spielt die Animation nicht ab; das erste Bild wird angezeigt.
  - `Once Forward` spielt die Animation einmal vom ersten bis zum letzten Bild ab.
  - `Once Backward` spielt die Animation einmal vom letzten bis zum ersten Bild ab.
  - `Once Ping Pong` spielt die Animation einmal vom ersten bis zum letzten Bild und dann zurück zum ersten Bild ab.
  - `Loop Forward` spielt die Animation wiederholt vom ersten bis zum letzten Bild ab.
  - `Loop Backward` spielt die Animation wiederholt vom letzten bis zum ersten Bild ab.
  - `Loop Ping Pong` spielt die Animation wiederholt vom ersten bis zum letzten Bild und dann zurück zum ersten Bild ab.

Fps
: Die Wiedergabegeschwindigkeit der Animation, angegeben in Bildern pro Sekunde (FPS).

Flip horizontal
: Spiegelt die Animation horizontal.

Flip vertical
: Spiegelt die Animation vertikal.

## Kollisionsformen einer Kachelquelle {#tile-source-collision-shapes}

Defold verwendet ein Bild, das in der Eigenschaft *Collision* angegeben ist, um eine _konvexe_ Form für jede Kachel zu erzeugen. Die Form umschließt den Teil der Kachel, der Farbinformationen enthält, also nicht zu 100 % transparent ist.

Oft ist es sinnvoll, für die Kollision dasselbe Bild zu verwenden, das auch die eigentliche Grafik enthält. Du kannst jedoch ein separates Bild angeben, wenn du Kollisionsformen möchtest, die von der Darstellung abweichen. Wenn du ein Kollisionsbild angibst, wird die Vorschau aktualisiert und zeigt auf jeder Kachel einen Umriss der erzeugten Kollisionsform.

Die Ansicht *Outline* der Kachelquelle listet die Kollisionsgruppen (collision groups) auf, die du der Kachelquelle hinzugefügt hast. Neue Kachelquelldateien erhalten eine Kollisionsgruppe namens "default". Du kannst neue Gruppen hinzufügen, indem du einen <kbd>Rechtsklick</kbd> auf den obersten Eintrag der Kachelquelle in der Ansicht *Outline* ausführst und <kbd>Add ▸ Collision Group</kbd> auswählst.

Um die Kachelformen auszuwählen, die zu einer bestimmten Gruppe gehören sollen, wähle die Gruppe in der Ansicht *Outline* aus und klicke dann auf jede Kachel, die du der Gruppe zuordnen möchtest. Der Umriss der Kachel und der Form wird in der Farbe der Gruppe dargestellt. Die Farbe wird der Gruppe im Editor automatisch zugewiesen.

![Kollisionsformen](images/tilemap/collision.png)

Um eine Kachel aus ihrer Kollisionsgruppe zu entfernen, wähle den obersten Eintrag der Kachelquelle in der Ansicht *Outline* aus und klicke dann auf die Kachel.
