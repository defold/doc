---
title: 2D-Bilder anzeigen
brief: Dieses Handbuch beschreibt, wie du mit der Sprite-Komponente 2D-Bilder und Animationen anzeigst.
---

# Sprites

Eine Sprite-Komponente (sprite component) zeigt ein einfaches Bild oder eine Flipbook-Animation auf dem Bildschirm an.

![Sprite](images/graphics/sprite.png)

Die Sprite-Komponente kann für ihre Grafik entweder einen [Atlas](/manuals/atlas) oder eine [Kachelquelle (tile source)](/manuals/tilesource) verwenden.

## Sprite-Eigenschaften {#sprite-properties}

Neben den Eigenschaften *Id*, *Position* und *Rotation* gibt es die folgenden komponentenspezifischen Eigenschaften:

*Image*
: Wenn der Shader nur einen Sampler hat, heißt dieses Feld `Image`. Andernfalls ist jeder Platz nach dem Textur-Sampler im Material benannt.
Jeder Platz legt die Atlas- oder Kachelquellenressource fest, die das Sprite für diesen Textur-Sampler verwendet.

*Default Animation*
: Die Animation, die für das Sprite verwendet werden soll. Die Animationsinformationen werden aus dem ersten Atlas oder der ersten Kachelquelle übernommen.

*Material*
: Das Material, das zum Rendern des Sprites verwendet werden soll.

*Blend Mode*
: Der Mischmodus, der beim Rendern des Sprites verwendet werden soll.

*Size Mode*
: Bei `Automatic` legt der Editor die Größe des Sprites fest. Bei `Manual` kannst du die Größe selbst festlegen.

*Slice 9*
: Lege hier fest, dass die Pixelgröße der Sprite-Textur an den Rändern erhalten bleibt, wenn du die Größe des Sprites änderst.

:[Slice-9](../shared/slice-9-texturing.md)

### Mischmodi {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## Änderungen zur Laufzeit {#runtime-manipulation}

Du kannst Sprites zur Laufzeit mit verschiedenen Funktionen und Eigenschaften ändern (Hinweise zur Verwendung findest du in der [API-Dokumentation](/ref/sprite/)). Funktionen:

* `sprite.play_flipbook()` - Spielt eine Animation auf einer Sprite-Komponente ab.
* `sprite.set_hflip()` und `sprite.set_vflip()` - Legen die horizontale und vertikale Spiegelung der Animation eines Sprites fest.

Ein Sprite hat außerdem verschiedene Eigenschaften, die du mit `go.get()` und `go.set()` ändern kannst:

`cursor`
: Die normalisierte Wiedergabeposition der Animation (`number`).

`image`
: Das Bild des Sprites (`hash`). Du kannst es mit einer Ressourceneigenschaft für einen Atlas oder eine Kachelquelle und `go.set()` ändern. Ein Beispiel findest du in der [API-Referenz](/ref/sprite/#image).

`material`
: Das Material des Sprites (`hash`). Du kannst es mit einer Ressourceneigenschaft für ein Material und `go.set()` ändern. Ein Beispiel findest du in der [API-Referenz](/ref/sprite/#material).

`playback_rate`
: Die Wiedergabegeschwindigkeit der Animation (`number`).

`scale`
: Die ungleichmäßige Skalierung des Sprites (`vector3`).

`size`
: Die Größe des Sprites (`vector3`). Sie kann nur geändert werden, wenn `Size Mode` des Sprites auf `Manual` gesetzt ist.

## Materialkonstanten {#material-constants}

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: Die Einfärbung des Sprites (`vector4`). Der `vector4` stellt die Einfärbung dar, wobei `x`, `y`, `z` und `w` dem Rot-, Grün-, Blau- und Alphaanteil entsprechen.

## Materialattribute {#material-attributes}

Ein Sprite kann Vertex-Attribute des aktuell zugewiesenen Materials überschreiben. Die Komponente übergibt diese Attribute an den Vertex-Shader (weitere Informationen findest du im [Handbuch zu Materialien](/manuals/material/#attributes)).

Die im Material angegebenen Attribute erscheinen als reguläre Eigenschaften im Inspektor und können für einzelne Sprite-Komponenten festgelegt werden. Wenn eines der Attribute überschrieben wird, erscheint es als überschriebene Eigenschaft und wird in der Sprite-Datei auf dem Datenträger gespeichert:

![Sprite-Attribute](../images/graphics/sprite-attributes.png)

## Projektkonfiguration {#project-configuration}

Die Datei *game.project* enthält einige [Projekteinstellungen](/manuals/project-settings#sprite) für Sprites.

## Sprites mit mehreren Texturen {#multi-textured-sprites}

Wenn ein Sprite mehrere Texturen verwendet, gibt es einige Dinge zu beachten.

### Animationen {#animations}

Die Animationsdaten (Bildrate, Einzelbildnamen) werden derzeit aus der ersten Textur übernommen. Wir nennen diese die „steuernde Animation“.

Die Bild-IDs der steuernden Animation werden verwendet, um die Bilder in einer anderen Textur zu finden.
Daher musst du sicherstellen, dass die Einzelbild-IDs zwischen den Texturen übereinstimmen.

Wenn dein `diffuse.atlas` beispielsweise eine Animation `run` wie diese enthält:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Dann lauten die Einzelbild-IDs etwa `run/hero_run_color_1`, was beispielsweise in einem `normal.atlas` wahrscheinlich nicht zu finden ist:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Deshalb verwenden wir `Rename patterns` im [Atlas](/manuals/material/), um sie umzubenennen.
Trage in den jeweiligen Atlanten `_color=` und `_normal=` ein, und du erhältst in beiden Atlanten Einzelbildnamen wie diese:

```
run/hero_run_1
run/hero_run_2
...
```

### UV-Koordinaten {#uvs}

Die UV-Koordinaten werden aus der ersten Textur übernommen. Da es nur einen Satz von Vertices gibt, können wir ohnehin keine gute Übereinstimmung garantieren,
wenn die weiteren Texturen mehr UV-Koordinaten oder eine andere Form haben.

Das musst du beachten: Stelle sicher, dass die Bilder hinreichend ähnliche Formen haben, da es sonst zum Übergreifen benachbarter Texturpixel (texture bleeding) kommen kann.

Die Abmessungen der Bilder in den einzelnen Texturen können unterschiedlich sein.
