---
title: 3D-Modelle in Defold
brief: Dieses Handbuch beschreibt, wie du 3D-Modelle, Skelette und Animationen in dein Spiel einbindest.
---

# Modellkomponente {#model-component}

Defold ist im Kern eine 3D-Engine. Selbst wenn du ausschließlich mit 2D-Material arbeitest, erfolgt das gesamte Rendering in 3D, wird aber orthografisch auf den Bildschirm projiziert. Defold ermöglicht dir, vollständige 3D-Inhalte zu nutzen, indem du 3D-Assets oder _Modelle_ (models) in deine Sammlungen (collections) einbindest. Du kannst reine 3D-Spiele ausschließlich mit 3D-Assets erstellen oder 3D- und 2D-Inhalte nach Belieben mischen.

## Eine Modellkomponente erstellen {#creating-a-model-component}

Modellkomponenten werden genauso erstellt wie jede andere Komponente (component) eines Spielobjekts (game object). Dafür gibt es zwei Möglichkeiten:

- Erstelle eine *Modelldatei*, indem du im Browser *Assets* einen <kbd>Rechtsklick</kbd> auf einen Speicherort ausführst und <kbd>New... ▸ Model</kbd> auswählst.
- Erstelle die Komponente direkt in ein Spielobjekt eingebettet, indem du in der Ansicht *Outline* einen <kbd>Rechtsklick</kbd> auf ein Spielobjekt ausführst und <kbd>Add Component ▸ Model</kbd> auswählst.

![Modell in einem Spielobjekt](images/model/model_gltf.png)

Nachdem du das Modell erstellt hast, musst du einige Eigenschaften festlegen:

### Modelleigenschaften {#model-properties}

Neben den Eigenschaften *Id*, *Position* und *Rotation* gibt es die folgenden komponentenspezifischen Eigenschaften:

*Scene*
: Die glTF-Datei mit der Erweiterung *.gltf* oder *.glb*, die die Geometrie des Modells enthält. Wenn die Datei Morph-Ziele (morph targets) enthält, werden sie zusammen mit der Szene importiert. Vor Defold 1.13.2 hieß diese Eigenschaft *Mesh*.

*Mesh*
: Ein optionales benanntes Mesh aus der ausgewählten *Scene*, verfügbar seit Defold 1.13.2. Lasse dieses Feld leer, um die gesamte Szene mit ihren importierten Transformationen zu rendern. Wähle ein Mesh aus, um dieses Mesh einmal in seinen lokalen Koordinaten ohne die glTF-Knotentransformationen zu rendern. Positioniere, drehe und skaliere die Modellkomponente oder ihr Spielobjekt, um das ausgewählte Mesh zu platzieren.

*Create GO Bones*
: Aktiviere diese Option, um für jeden Knochen des Modells ein Spielobjekt zu erstellen. Du kannst diese Spielobjekte verwenden, um andere Spielobjekte anzuhängen, beispielsweise Waffen an Handknochen und so weiter. 

*Skeleton*
: Diese Eigenschaft sollte auf die glTF-Datei mit der Erweiterung *.gltf* oder *.glb* verweisen, die das für die Animation zu verwendende Skelett enthält. Beachte, dass Defold einen einzigen Wurzelknochen in deiner Hierarchie voraussetzt.

*Animations*
: Setze diese Eigenschaft auf die *Animationssatzdatei*, die die Animationen enthält, die du für das Modell verwenden möchtest.

*Default Animation*
: Dies ist die Animation (aus dem Animationssatz), die automatisch auf dem Modell abgespielt wird.

Zusätzlich zu den oben genannten Eigenschaften gibt es für jedes Mesh des Modells ein Feld, in dem du ein Material zuweisen kannst:

*Material*
: Setze diese Eigenschaft auf ein von dir erstelltes Material, das für ein texturiertes 3D-Objekt geeignet ist. Es gibt einige integrierte Materialien, die du als Ausgangspunkt verwenden kannst:

  * Verwende *model.material* für statische Modelle ohne Instanziierung
  * Verwende *model_instanced.material* für statische instanziierte Modelle
  * Verwende *model_skinned.material* für Modelle mit Skinning (animiert) ohne Instanziierung
  * Verwende *model_skinned_instanced.material* für instanziierte Modelle mit Skinning (animiert)

Je nach Material gibt es eine oder mehrere Textureigenschaften:

*Texture*
: Diese Eigenschaft sollte auf die Texturbilddatei verweisen, die du auf das Objekt anwenden möchtest.


## Bearbeitung im Editor {#editor-manipulation}

Sobald die Modellkomponente vorhanden ist, kannst du die Komponente und/oder das Spielobjekt, das sie enthält, mit den üblichen Werkzeugen des *Scene Editor* bearbeiten und verändern, um das Modell nach deinen Wünschen zu verschieben, zu drehen und zu skalieren.

## Änderungen zur Laufzeit {#runtime-manipulation}

Du kannst Modelle zur Laufzeit über verschiedene Funktionen und Eigenschaften verändern (Hinweise zur Verwendung findest du in der [API-Dokumentation](/ref/model/)).

![Wiggler im Spiel](images/model/runtime.png)

### Animation zur Laufzeit {#runtime-animation}

Defold bietet umfangreiche Unterstützung für die Steuerung von Animationen zur Laufzeit. Mehr dazu findest du im [Handbuch zu Modellanimationen](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

Der Wiedergabecursor der Animation kann entweder von Hand oder über das System für Eigenschaftsanimationen animiert werden:

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Modelle können auch glTF-Animationen mit Morph-Zielen verwenden. Die Gewichtungen der Morph-Ziele werden wie andere Modellanimationen mit `model.play_anim()` animiert und können zur Laufzeit mit [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) und [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) gelesen oder überschrieben werden. Einzelheiten findest du im [Abschnitt zu Morph-Zielen](/manuals/model-animation#morph-targets) im Handbuch zu Modellanimationen.

### Eigenschaften ändern {#changing-properties}

Ein Modell hat außerdem verschiedene Eigenschaften, die mit `go.get()` und `go.set()` verändert werden können:

`animation`
: Die aktuelle Modellanimation (`hash`) (NUR LESBAR). Du änderst die Animation mit `model.play_anim()` (siehe oben).

`cursor`
: Der normalisierte Animationscursor (`number`).

`material`
: Das Material des Modells (`hash`). Du kannst es mit einer Materialressourceneigenschaft und `go.set()` ändern. Ein Beispiel findest du in der [API-Referenz](/ref/model/#material).

`playback_rate`
: Die Wiedergabegeschwindigkeit der Animation (`number`).

`textureN`
: Die Texturen des Modells, wobei N den Bereich 0-15 abdeckt (`hash`). Du kannst diese Eigenschaften mit `go.get()` lesen und mit einer Texturressourceneigenschaft und `go.set()` ändern. Defold unterstützt höchstens 16 Texturen pro Zeichenaufruf (draw call). Die Anzahl der von einem Shader nutzbaren Texturen kann auf Grafikadaptern mit einer niedrigeren Grenze für Textur-Sampler jedoch geringer sein.


## Material

In 3D-Software kannst du üblicherweise Eigenschaften an den Vertices deiner Objekte festlegen, etwa zur Farbgebung und Texturierung. Diese Informationen werden in der glTF-Datei mit der Erweiterung *.gltf* oder *.glb* gespeichert, die du aus deiner 3D-Software exportierst. Je nach den Anforderungen deines Spiels musst du geeignete und _leistungsfähige_ Materialien für deine Objekte auswählen und/oder erstellen. Ein Material kombiniert _Shader-Programme_ mit einem Satz von Parametern für das Rendering des Objekts.

Es gibt einige integrierte Materialien, die du als Ausgangspunkt verwenden kannst:

  * Verwende *model.material* für statische Modelle ohne Instanziierung
  * Verwende *model_instanced.material* für statische instanziierte Modelle
  * Verwende *model_skinned.material* für Modelle mit Skinning (animiert) ohne Instanziierung
  * Verwende *model_skinned_instanced.material* für instanziierte Modelle mit Skinning (animiert)

Die integrierten Modellmaterialien verwenden ein lokales Koordinatensystem für Vertices. Bei Modellen mit Skinning ermöglicht dieses lokale Koordinatensystem dem Vertex-Shader, das Skinning auf der GPU mithilfe einer Knochenmatrix-Textur durchzuführen. Das lokale Koordinatensystem für Vertices ist auch für die Instanziierung von Modellen erforderlich. Ein benutzerdefiniertes Material für Modelle mit GPU-Skinning oder instanziierte Modelle sollte daher die Einstellung *Local* für das Vertex-Koordinatensystem verwenden.

Der Knochenmatrix-Cache verwendet eine `RGBA32F`-Textur. Wenn der aktive Grafikadapter dieses Texturformat nicht unterstützt, kann Defold keine animierte Modellkomponente erstellen, die ein Material mit lokalem Koordinatensystem verwendet. Bei OpenGL ES 2.0 und WebGL 1.0 hängt die Unterstützung daher von der Erweiterung des Adapters für Gleitkommatexturen ab. Für die Kompatibilität mit einem Adapter, dem diese Erweiterung fehlt, verwende ein benutzerdefiniertes Material mit Weltkoordinatensystem. Dieses verwendet CPU-Skinning und kann keine Modellinstanziierung nutzen. Die Abmessungen des Caches kannst du über die [Projekteinstellungen für Model](/manuals/project-settings/#model) anpassen.

Wenn du benutzerdefinierte Materialien für deine Modelle erstellen musst, findest du Informationen dazu in der [Materialdokumentation](/manuals/material). Das [Shader-Handbuch](/manuals/shader) enthält Informationen zur Funktionsweise von Shader-Programmen.


### Materialkonstanten {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: Die Einfärbung des Modells (`vector4`). Der `vector4` stellt die Einfärbung dar, wobei x, y, z und w den Rot-, Grün-, Blau- und Alpha-Anteilen der Einfärbung entsprechen.


## Rendering

Das standardmäßige Render-Skript ist auf 2D-Spiele zugeschnitten und funktioniert nicht mit 3D-Modellen. Indem du das standardmäßige Render-Skript kopierst und einige Codezeilen zum Render-Skript hinzufügst, kannst du jedoch das Rendering deiner Modelle aktivieren. Zum Beispiel:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Einzelheiten zur Funktionsweise von Render-Skripten findest du in der [Render-Dokumentation](/manuals/render).
