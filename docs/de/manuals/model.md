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
: Die glTF-Datei *.gltf* oder *.glb*, die die Geometrie des Modells enthält. Enthält die Datei Morph Targets, werden diese zusammen mit der Szene importiert. Diese Eigenschaft hieß zuvor *Mesh*.

*Mesh*
: Ein optionales benanntes Mesh aus der ausgewählten *Scene*. Lasse dieses Feld leer, um die gesamte Szene mit ihren importierten Transformationen zu rendern. Wähle ein Mesh, um es einmal in seinen lokalen Koordinaten ohne glTF-Knotentransformationen zu rendern. Positioniere, drehe und skaliere die Modellkomponente oder ihr Spielobjekt, um das ausgewählte Mesh zu platzieren.

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
: Setze diese Eigenschaft auf ein für das Modell geeignetes Material. Verwende ein integriertes `gltf`-Material für physikalisch basiertes Rendering der glTF-Materialeigenschaften, ein integriertes `model`-Material für allgemeine Modellschattierung oder ein eigenes Material. Siehe die [Materialvarianten unten](#material) und das [PBR-Handbuch](/manuals/physically-based-rendering/#built-in-pbr-materials).

Je nach Material gibt es eine oder mehrere Textureigenschaften:

*Texture*
: Diese Eigenschaft sollte auf das Texturbild zeigen, das auf das Objekt angewendet werden soll. Es kann ein separates Projekt-Asset oder ein eingebettetes Bild unter einer glTF- oder GLB-Datei im Bereich *Assets* sein.

Bei der Auswahl einer glTF- oder GLB-*Scene* oder beim Ändern ihrer *Mesh*-Auswahl kann das Ausfüllen von Material- und Texturbindungen angeboten werden. <kbd>Auto Fill</kbd> ersetzt vorhandene Bindungen durch die der Quelle; <kbd>Keep Current</kbd> behält deine Bindungen bei und übernimmt dabei die neue Szenen- oder Mesh-Auswahl. Siehe den [Ablauf des Modellimports](/manuals/importing-models/#using-a-model).


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

Folgende integrierte Materialien sind unter `/builtins/materials/` verfügbar:

| Modelltyp | Allgemeine Modellschattierung | glTF-PBR-Schattierung |
|---|---|---|
| Statisch, nicht instanziert | `model.material` | `gltf.material` |
| Statisch, instanziert | `model_instanced.material` | `gltf_instanced.material` |
| Mit Skinning (animiert), nicht instanziert | `model_skinned.material` | `gltf_skinned.material` |
| Mit Skinning (animiert), instanziert | `model_skinned_instanced.material` | `gltf_skinned_instanced.material` |

Die `gltf`-Materialien bieten integrierte Metallic-/Roughness-Beleuchtung mit den importierten glTF-Materialdaten. Texturbindungen, Lichtquellen und benutzerdefinierte Shader beschreibt das [PBR-Handbuch](/manuals/physically-based-rendering/#built-in-pbr-materials).

Alle diese integrierten Materialien verwenden lokalen Vertex-Raum. Bei geskinnten Modellen kann der Vertex-Shader dadurch das Skinning auf der GPU mithilfe einer Knochenmatrixtextur durchführen; lokaler Vertex-Raum ist auch für Modellinstanzierung erforderlich. Ein benutzerdefiniertes Material für GPU-Skinning oder instanzierte Modelle sollte deshalb die Vertex-Raum-Einstellung *Local* verwenden.

Der Knochenmatrix-Cache verwendet eine `RGBA32F`-Textur. Wenn der aktive Grafikadapter dieses Texturformat nicht unterstützt, kann Defold keine animierte Modellkomponente erstellen, die ein Material mit lokalem Koordinatensystem verwendet. Bei OpenGL ES 2.0 und WebGL 1.0 hängt die Unterstützung daher von der Erweiterung des Adapters für Gleitkommatexturen ab. Für die Kompatibilität mit einem Adapter, dem diese Erweiterung fehlt, verwende ein benutzerdefiniertes Material mit Weltkoordinatensystem. Dieses verwendet CPU-Skinning und kann keine Modellinstanziierung nutzen. Die Abmessungen des Caches kannst du über die [Projekteinstellungen für Model](/manuals/project-settings/#model) anpassen.

Wenn du benutzerdefinierte Materialien für deine Modelle erstellen musst, findest du Informationen dazu in der [Materialdokumentation](/manuals/material). Das [Shader-Handbuch](/manuals/shader) enthält Informationen zur Funktionsweise von Shader-Programmen.


### Materialkonstanten {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: Die Einfärbung des Modells (`vector4`). Der `vector4` stellt die Einfärbung dar, wobei x, y, z und w den Rot-, Grün-, Blau- und Alpha-Anteilen der Einfärbung entsprechen.


## Rendering

Das Standard-Renderskript zeichnet Materialien mit dem Tag `model`, einschließlich der integrierten Modell- und glTF-Materialien. Um sie in einem eigenen Renderskript zu rendern, erstelle ein passendes Prädikat und zeichne es mit einer für die Szene geeigneten Ansicht und Projektion. Zum Beispiel:

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
