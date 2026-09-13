---
title: Atlas-Handbuch
brief: Dieses Handbuch erklärt, wie Atlas-Ressourcen in Defold funktionieren.
---

# Atlas

Einzelne Bilder werden häufig als Quelle für Sprites verwendet. Aus Leistungsgründen müssen Bilder jedoch zu größeren Bildsätzen zusammengefasst werden, die als Atlanten (atlases) bezeichnet werden. Das Zusammenfassen kleinerer Bilder zu Atlanten ist besonders auf Mobilgeräten wichtig, auf denen weniger Speicher und Rechenleistung zur Verfügung stehen als auf Desktoprechnern oder dedizierten Spielkonsolen.

In Defold ist eine Atlas-Ressource eine Liste separater Bilddateien, die automatisch zu einem größeren Bild zusammengefasst werden.

## Einen Atlas erstellen {#creating-an-atlas}

Wähle <kbd>New... ▸ Atlas</kbd> im Kontextmenü des Browsers *Assets*. Gib der neuen Atlas-Datei einen Namen. Der Editor öffnet die Datei nun im Atlas-Editor. Die Atlas-Eigenschaften werden im Bereich
*Properties* angezeigt, sodass du sie bearbeiten kannst (Einzelheiten findest du weiter unten).

Du musst einem Atlas Bilder oder Animationen hinzufügen, bevor du ihn als Grafikquelle für Komponenten (components) von Spielobjekten (game objects) wie Sprites und Partikeleffektkomponenten (ParticleFX) verwenden kannst.

Vergewissere dich, dass du deine Bilder zum Projekt hinzugefügt hast (ziehe die Bilddateien an die richtige Stelle im Browser *Assets* und lege sie dort ab)

Einzelne Bilder hinzufügen

: Ziehe Bilder aus dem Bereich *Asset* in die Editoransicht und lege sie dort ab.
  
  Führe alternativ einen <kbd>Rechtsklick</kbd> auf den obersten Atlas-Eintrag im Bereich *Outline* aus.

  Wähle im eingeblendeten Kontextmenü <kbd>Add Images</kbd>, um einzelne Bilder hinzuzufügen.

  Ein Dialogfeld öffnet sich, in dem du die Bilder suchen und auswählen kannst, die du dem Atlas hinzufügen möchtest. Beachte, dass du die Bilddateien filtern und mehrere Dateien gleichzeitig auswählen kannst.

  ![Einen Atlas erstellen und Bilder hinzufügen](images/atlas/add.png)

  Die hinzugefügten Bilder werden in *Outline* aufgelistet, und der vollständige Atlas ist in der mittleren Editoransicht zu sehen. Möglicherweise musst du <kbd>F</kbd> drücken (<kbd>View ▸ Frame Selection</kbd> im Menü), um die Ansicht auf die Auswahl auszurichten.

  ![Hinzugefügte Bilder](images/atlas/single_images.png)

Flipbook-Animationen hinzufügen
: Führe einen <kbd>Rechtsklick</kbd> auf den obersten Atlas-Eintrag im Bereich *Outline* aus.

  Wähle im eingeblendeten Kontextmenü <kbd>Add Animation Group</kbd>, um eine Flipbook-Animationsgruppe zu erstellen.

  Dem Atlas wird eine neue, leere Animationsgruppe mit einem Standardnamen (`New Animation`) hinzugefügt.

  Ziehe Bilder aus dem Bereich *Asset* in die Editoransicht und lege sie dort ab, um sie der aktuell ausgewählten Gruppe hinzuzufügen.
  
  Führe alternativ einen <kbd>Rechtsklick</kbd> auf die neue Gruppe aus und wähle im Kontextmenü <kbd>Add Images</kbd>.

  Ein Dialogfeld öffnet sich, in dem du die Bilder suchen und auswählen kannst, die du der Animationsgruppe hinzufügen möchtest.

  ![Einen Atlas erstellen und Bilder hinzufügen](images/atlas/add_animation.png)

  Drücke bei ausgewählter Animationsgruppe <kbd>Space</kbd>, um eine Vorschau anzuzeigen, und <kbd>Ctrl/Cmd+T</kbd>, um die Vorschau zu schließen. Passe die *Properties* der Animation nach Bedarf an (siehe unten).

  ![Animationsgruppe](images/atlas/animation_group.png)

Du kannst die Bilder in Outline neu anordnen, indem du sie auswählst und <kbd>Alt + Up/down</kbd> drückst. Du kannst auch leicht Duplikate erstellen, indem du Bilder in Outline kopierst und einfügst (über das Menü <kbd>Edit</kbd>, das Kontextmenü per Rechtsklick oder Tastenkombinationen).

## Atlas-Eigenschaften {#atlas-properties}

Jede Atlas-Ressource hat eine Reihe von Eigenschaften. Diese werden im Bereich *Properties* angezeigt, wenn du den obersten Eintrag in der Ansicht *Outline* auswählst.

Size
: Zeigt die berechnete Gesamtgröße der resultierenden Texturressource an. Breite und Höhe werden auf die nächstgelegene Zweierpotenz gesetzt. Beachte, dass einige Formate quadratische Texturen erfordern, wenn du die Texturkomprimierung aktivierst. Nicht quadratische Texturen werden dann in der Größe angepasst und mit leerem Raum aufgefüllt, um sie quadratisch zu machen. Einzelheiten findest du im [Handbuch zu Texturprofilen](/manuals/texture-profiles/).

Margin
: Die Anzahl der Pixel, die zwischen den einzelnen Bildern hinzugefügt werden sollen.

Inner Padding
: Die Anzahl der leeren Pixel, mit denen jedes Bild rundherum aufgefüllt werden soll.

Extrude Borders
: Die Anzahl der Randpixel, die wiederholt um jedes Bild herum hinzugefügt werden sollen. Wenn der Fragment-Shader Pixel am Rand eines Bildes abtastet, können Pixel eines benachbarten Bildes (auf derselben Atlas-Textur) übergreifen (texture bleeding). Das Erweitern der Randpixel nach außen löst dieses Problem.

Max Page Size
: Die maximale Größe einer Seite in einem mehrseitigen Atlas. Damit kannst du einen Atlas in mehrere Seiten desselben Atlas aufteilen, um die Atlas-Größe zu begrenzen und trotzdem nur einen einzigen Zeichenaufruf (draw call) zu verwenden. Diese Funktion muss in Kombination mit Materialien verwendet werden, die mehrseitige Atlanten unterstützen und unter `/builtins/materials/*_paged_atlas.material` zu finden sind.

![Mehrseitiger Atlas](images/atlas/multipage_atlas.png)

Rename Patterns
: Eine durch Kommas (´,´) getrennte Liste von Such- und Ersetzungsmustern, wobei jedes Muster die Form `search=replace` hat.
Der ursprüngliche Name jedes Bildes (der Basisname der Datei) wird mithilfe dieser Muster umgewandelt. (Ein Muster wie `hat=cat,_normal=` benennt beispielsweise ein Bild namens `hat_normal` in `cat` um.) Das ist nützlich, um Animationen zwischen Atlanten einander zuzuordnen.

Hier siehst du Beispiele für die verschiedenen Eigenschaftseinstellungen mit vier quadratischen Bildern der Größe 64 × 64, die einem Atlas hinzugefügt wurden. Beachte, wie die Atlas-Größe auf 256 × 256 springt, sobald die Bilder nicht mehr in 128 × 128 passen, wodurch viel Texturfläche verschwendet wird.

![Atlas-Eigenschaften](images/atlas/atlas_properties.png)

## Bildeigenschaften {#image-properties}

Jedes Bild in einem Atlas hat eine Reihe von Eigenschaften:

Id
: Die ID des Bildes (schreibgeschützt).

Size
: Die Breite und Höhe des Bildes (schreibgeschützt).

Pivot
: Der Bezugspunkt (pivot) des Bildes (in Einheiten). Oben links ist (0,0) und unten rechts ist (1,1). Der Standardwert ist (0.5, 0.5). Der Bezugspunkt kann außerhalb des Bereichs von 0 bis 1 liegen. Der Bezugspunkt ist die Stelle, an der das Bild zentriert wird, wenn es beispielsweise in einem Sprite verwendet wird. Du kannst den Bezugspunkt ändern, indem du seinen Anfasser in der Editoransicht ziehst. Der Anfasser ist nur sichtbar, wenn ein einzelnes Bild ausgewählt ist. Du kannst das Einrasten aktivieren, indem du beim Ziehen <kbd>Shift</kbd> gedrückt hältst.

Sprite Trim Mode
: Legt fest, wie das Sprite gerendert wird. Standardmäßig wird das Sprite als Rechteck gerendert (Sprite Trim Mode ist auf Off gesetzt). Wenn das Sprite viele transparente Pixel enthält, kann es effizienter sein, das Sprite als nicht rechteckige Form mit 4 bis 8 Vertices zu rendern. Beachte, dass das Beschneiden von Sprites nicht zusammen mit Sprites mit Neun-Segment-Skalierung (9-slice) funktioniert.

Image
: Pfad zum Bild selbst.

![Bildeigenschaften](images/atlas/image_properties.png)

## Animationseigenschaften {#animation-properties}

Zusätzlich zur Liste der Bilder, die zu einer Animationsgruppe gehören, steht eine Reihe von Eigenschaften zur Verfügung:

Id
: Der Name der Animation.

Fps
: Die Wiedergabegeschwindigkeit der Animation, angegeben in Bildern pro Sekunde (FPS).

Flip horizontal
: Spiegelt die Animation horizontal.

Flip vertical
: Spiegelt die Animation vertikal.

Playback
: Legt fest, wie die Animation abgespielt werden soll:

  - `None` spielt die Animation überhaupt nicht ab; das erste Bild wird angezeigt.
  - `Once Forward` spielt die Animation einmal vom ersten bis zum letzten Bild ab.
  - `Once Backward` spielt die Animation einmal vom letzten bis zum ersten Bild ab.
  - `Once Ping Pong` spielt die Animation einmal vom ersten bis zum letzten Bild und dann zurück zum ersten Bild ab.
  - `Loop Forward` spielt die Animation wiederholt vom ersten bis zum letzten Bild ab.
  - `Loop Backward` spielt die Animation wiederholt vom letzten bis zum ersten Bild ab.
  - `Loop Ping Pong` spielt die Animation wiederholt vom ersten bis zum letzten Bild und dann zurück zum ersten Bild ab.

## Texturen und Atlanten zur Laufzeit erstellen {#runtime-texture-and-atlas-creation}

Du kannst eine Textur und einen Atlas zur Laufzeit erstellen.

### Eine Texturressource zur Laufzeit erstellen {#creating-a-texture-resource-at-runtime}

Verwende [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table), um eine neue Texturressource zu erstellen:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Nachdem die Textur erstellt wurde, kannst du [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) verwenden, um die Pixel der Textur festzulegen:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
Mit `resource.set_texture()` kannst du auch einen Teilbereich der Textur aktualisieren, indem du eine Pufferbreite und -höhe verwendest, die kleiner als die volle Größe der Textur sind, und die Parameter x und y von `resource.set_texture()` änderst.
:::

Die Textur kann mit `go.set()` direkt auf einer [Modellkomponente](/manuals/model/) verwendet werden:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Einen Atlas zur Laufzeit erstellen {#creating-an-atlas-at-runtime}

Wenn die Textur auf einer [Sprite-Komponente](/manuals/sprite/) verwendet werden soll, muss sie zunächst von einem Atlas verwendet werden. Verwende [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table), um einen Atlas zu erstellen:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

Die Einträge in `frames` sind bei 1 beginnende Indizes in die Tabelle `geometries`. Eine Liste kann Geometrien wiederverwenden, neu anordnen oder überspringen; das lässt sich mit den veralteten, zur Ablösung vorgesehenen Intervallfeldern `frame_start` und `frame_end` nicht darstellen. `resource.get_atlas()` gibt `frames` zurück; verwende dieselbe Darstellung, wenn du Atlas-Daten an `resource.set_atlas()` oder `resource.create_atlas()` übergibst. Die Intervallfelder werden aus Kompatibilitätsgründen weiterhin von den Funktionen zum Festlegen und Erstellen akzeptiert, neuer Code sollte jedoch `frames` verwenden.
