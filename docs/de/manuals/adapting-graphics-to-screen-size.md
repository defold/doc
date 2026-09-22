---
title: Grafiken an unterschiedliche Bildschirmgrößen anpassen
brief: Dieses Handbuch erklärt, wie du dein Spiel und deine Grafiken an unterschiedliche Bildschirmgrößen anpasst.
---

# Einführung {#introduction}

Wenn du dein Spiel und deine Grafiken an unterschiedliche Bildschirmgrößen anpasst, gibt es einiges zu beachten:

* Ist es ein Retrospiel mit niedrig aufgelöster, pixelgenauer Grafik oder ein modernes Spiel mit Grafik in HD-Qualität?
* Wie soll sich das Spiel im Vollbildmodus auf unterschiedlich großen Bildschirmen verhalten?
  * Soll der Spieler auf einem hochauflösenden Bildschirm mehr vom Spielinhalt sehen, oder soll sich der Zoom der Grafik so anpassen, dass immer derselbe Inhalt angezeigt wird?
* Wie soll das Spiel mit Seitenverhältnissen umgehen, die von dem in *game.project* festgelegten Seitenverhältnis abweichen?
  * Soll der Spieler mehr vom Spielinhalt sehen? Oder soll es vielleicht schwarze Balken geben? Oder GUI-Elemente, deren Größe angepasst wird?
* Welche Menüs und GUI-Komponenten (GUI components) benötigst du auf dem Bildschirm, und wie sollen sie sich an unterschiedliche Bildschirmgrößen und Bildschirmausrichtungen anpassen?
  * Sollen Menüs und andere GUI-Komponenten bei einem Wechsel der Ausrichtung ihr Layout ändern oder unabhängig von der Ausrichtung dasselbe Layout behalten?

Dieses Handbuch behandelt einige dieser Fragen und schlägt bewährte Vorgehensweisen vor.


## Ändern, wie deine Inhalte gerendert werden {#how-to-change-how-your-content-is-rendered}

Das Render-Skript (render script) von Defold gibt dir die vollständige Kontrolle über die gesamte Rendering-Pipeline. Das Render-Skript legt die Reihenfolge fest und entscheidet, was und wie gezeichnet wird. Standardmäßig zeichnet das Render-Skript immer denselben Pixelbereich, der durch die Breite und Höhe in der Datei *game.project* definiert ist. Das gilt unabhängig davon, ob die Fenstergröße geändert wird oder die tatsächliche Bildschirmauflösung davon abweicht. Dadurch wird der Inhalt bei einer Änderung des Seitenverhältnisses gestreckt und bei einer Änderung der Fenstergröße vergrößert oder verkleinert. Für manche Spiele ist das möglicherweise akzeptabel. Wahrscheinlicher ist jedoch, dass du bei einer anderen Bildschirmauflösung oder einem anderen Seitenverhältnis mehr oder weniger Spielinhalt anzeigen möchtest oder zumindest sicherstellen willst, dass der Inhalt vergrößert oder verkleinert wird, ohne sein Seitenverhältnis zu ändern. Das standardmäßige Strecken lässt sich leicht ändern. Wie das geht, erfährst du im [Rendering-Handbuch](https://www.defold.com/manuals/render/#default-view-projection).


## Retro-/8-Bit-Grafik {#retro8-bit-graphics}

Retro-/8-Bit-Grafik bezeichnet häufig Spiele, die den Grafikstil alter Spielkonsolen oder Computer mit ihrer niedrigen Auflösung und begrenzten Farbpalette nachahmen. Beispielsweise hatte das Nintendo Entertainment System (NES) eine Bildschirmauflösung von 256 × 240, der Commodore 64 von 320 × 200 und der Gameboy von 160 × 144. All diese Auflösungen entsprechen nur einem Bruchteil der Größe moderner Bildschirme. Damit Spiele, die diesen Grafikstil und diese Bildschirmauflösungen nachahmen, auf einem modernen hochauflösenden Bildschirm spielbar sind, muss die Grafik um ein Mehrfaches hochskaliert oder vergrößert werden. Eine einfache Möglichkeit besteht darin, alle Grafiken in der niedrigen Auflösung und dem Stil zu zeichnen, die du nachahmen möchtest, und sie beim Rendern zu vergrößern. In Defold lässt sich das leicht mit dem Render-Skript und der [festen Projektion](/manuals/render/#fixed-projection) erreichen, die auf einen geeigneten Zoomwert eingestellt wird.

Verwenden wir diesen Kachelsatz (tileset) und diese Spielfigur ([Quelle](https://ansimuz.itch.io/grotto-escape-game-art-pack)) für ein 8-Bit-Retrospiel mit einer Auflösung von 320 × 200:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

Wenn du in der Datei *game.project* 320 × 200 einstellst und das Spiel startest, sieht es so aus:

![](images/screen_size/retro-original_320x200.png)

Auf einem modernen hochauflösenden Bildschirm ist das Fenster winzig! Wenn du die Fenstergröße auf das Vierfache, also 1280 × 800, erhöhst, passt es besser zu einem modernen Bildschirm:

![](images/screen_size/retro-original_1280x800.png)

Jetzt hat das Fenster eine vernünftigere Größe, aber auch an der Grafik müssen wir etwas ändern. Sie ist so klein, dass man kaum erkennen kann, was im Spiel passiert. Mit dem Render-Skript können wir eine feste, vergrößerte Projektion einstellen:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
Du kannst dasselbe Ergebnis erzielen, indem du einem Spielobjekt (game object) eine [Kamerakomponente (camera component)](/manuals/camera/) hinzufügst, *Orthographic Projection* aktivierst und *Orthographic Zoom* auf 4.0 setzt:

![](images/screen_size/retro-camera_zoom.png)
:::

Das führt zu folgendem Ergebnis:

![](images/screen_size/retro-zoomed_1280x800.png)

Das ist besser. Sowohl das Fenster als auch die Grafik haben eine gute Größe. Bei genauerem Hinsehen gibt es jedoch ein offensichtliches Problem:

![](images/screen_size/retro-zoomed_linear.png)

Die Grafik sieht unscharf aus! Das liegt daran, wie die vergrößerte Grafik beim Rendern durch die GPU aus der Textur abgetastet wird. Die Standardeinstellung in der Datei *game.project* im Abschnitt *Graphics* ist *linear*:

![](images/screen_size/retro-settings_linear.png)

Wenn du sie auf *nearest* änderst, erhalten wir das gewünschte Ergebnis:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

Jetzt haben wir scharfe, *pixelgenaue* Grafik für unser Retrospiel. Es gibt noch weitere Dinge zu beachten, etwa das Deaktivieren von Subpixeln für Sprites in *game.project*:

![](images/screen_size/retro-subpixels.png)

Wenn die Option *Subpixels* deaktiviert ist, werden Sprites nie auf halben Pixeln gerendert, sondern rasten immer am nächsten ganzen Pixel ein.

## Hochauflösende Grafik {#high-resolution-graphics}

Bei hochauflösender Grafik müssen wir Projekt und Inhalte anders einrichten als bei Retro-/8-Bit-Grafik. Bei Bitmap-Grafik musst du deine Inhalte so erstellen, dass sie auf einem hochauflösenden Bildschirm im Maßstab 1:1 gut aussehen.

Wie bei Retro-/8-Bit-Grafik musst du das Render-Skript ändern. In diesem Fall soll die Grafik mit der Bildschirmgröße skaliert werden, während das ursprüngliche Seitenverhältnis erhalten bleibt:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

Dadurch wird die Darstellung auf dem Bildschirm so angepasst, dass immer der in der Datei *game.project* festgelegte Inhaltsumfang angezeigt wird. Je nachdem, ob das Seitenverhältnis abweicht, können darüber und darunter oder an den Seiten zusätzliche Inhalte angezeigt werden.

Du solltest die Breite und Höhe in der Datei *game.project* so einstellen, dass du deine Spielinhalte unskaliert anzeigen kannst.

### Einstellung für hohe Pixeldichte und Retina-Bildschirme {#high-dpi-setting-and-retina-screens}

Wenn du auch hochauflösende Retina-Bildschirme unterstützen möchtest, kannst du dies in der Datei *game.project* im Abschnitt Display aktivieren:

![](images/screen_size/highdpi-enabled.png)

Dadurch wird auf Bildschirmen, die dies unterstützen, ein Backbuffer mit hoher Pixeldichte erstellt. Das Spiel rendert mit der doppelten Auflösung der Werte in den Einstellungen Width und Height. Diese Werte bleiben weiterhin die logische Auflösung, die in Skripten und Eigenschaften verwendet wird. Das bedeutet, dass alle Maße gleich bleiben und Inhalte, die mit dem Skalierungsfaktor 1x gerendert werden, gleich aussehen. Wenn du jedoch hochauflösende Bilder importierst und sie auf 0,5x skalierst, werden sie auf dem Bildschirm mit hoher Pixeldichte angezeigt.


## Eine anpassungsfähige GUI erstellen {#creating-an-adaptive-gui}

Das System zum Erstellen von GUI-Komponenten basiert auf einer Reihe grundlegender Bausteine, den [Knoten (nodes)](/manuals/gui/#node-types). Auch wenn es übermäßig einfach erscheinen mag, kannst du damit alles von Schaltflächen bis hin zu komplexen Menüs und Popups erstellen. Die von dir erstellten GUIs lassen sich so konfigurieren, dass sie sich automatisch an Änderungen der Bildschirmgröße und -ausrichtung anpassen. Beispielsweise kannst du *Knoten* am oberen, unteren oder an den seitlichen Bildschirmrändern verankern. Knoten können dabei entweder ihre Größe beibehalten oder gestreckt werden. Auch die Beziehungen zwischen *Knoten* sowie ihre Größe und ihr Aussehen lassen sich so konfigurieren, dass sie sich bei einer Änderung der Bildschirmgröße oder -ausrichtung ändern.

### Eigenschaften von *Knoten* {#node-properties}

Jeder *Knoten* in einer GUI hat einen Bezugspunkt (pivot), eine horizontale und vertikale Verankerung sowie einen Anpassungsmodus.

* Der Bezugspunkt definiert den Mittelpunkt eines Knotens.
* Der Verankerungsmodus steuert, wie sich die vertikale und horizontale Position des Knotens ändert, wenn die Grenzen der Szene oder des übergeordneten Knotens gestreckt werden, um sie an die physische Bildschirmgröße anzupassen.
* Der Anpassungsmodus steuert, was mit einem Knoten geschieht, wenn die Grenzen der Szene oder des übergeordneten Knotens an die physische Bildschirmgröße angepasst werden.

Mehr über diese Eigenschaften erfährst du [im GUI-Handbuch](/manuals/gui/#node-properties).

### Layouts

Defold unterstützt GUIs, die sich auf Mobilgeräten automatisch an Änderungen der Bildschirmausrichtung anpassen. Mit dieser Funktion kannst du eine GUI gestalten, die sich an die Ausrichtung und das Seitenverhältnis verschiedener Bildschirmgrößen anpasst. Du kannst auch Layouts erstellen, die auf bestimmte Gerätemodelle abgestimmt sind. Mehr über dieses System erfährst du im [Handbuch zu GUI-Layouts](/manuals/gui-layouts/)


## Unterschiedliche Bildschirmgrößen testen {#testing-different-screen-sizes}

Das Menü *Debug* enthält eine Option, mit der du die Auflösung eines bestimmten Gerätemodells oder eine benutzerdefinierte Auflösung simulieren kannst. Während die Anwendung läuft, kannst du <kbd>Debug->Simulate Resolution</kbd> wählen und eines der Gerätemodelle aus der Liste auswählen. Die Größe des Fensters der laufenden Anwendung wird angepasst, und du kannst sehen, wie dein Spiel bei einer anderen Auflösung oder einem anderen Seitenverhältnis aussieht.

![](images/screen_size/simulate-resolution.png)
