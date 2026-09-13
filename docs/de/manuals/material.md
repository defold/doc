---
title: Handbuch zu Materialien in Defold
brief: Dieses Handbuch erklärt die Arbeit mit Materialien, Shader-Konstanten und Samplern.
---

# Materialien {#materials}

Materialien legen fest, wie eine grafische Komponente (component), etwa ein Sprite, eine Kachelkarte (tile map), eine Schriftart, ein GUI-Knoten oder ein Modell, gerendert werden soll.

Ein Material enthält _Tags_, also Informationen, mit denen die Rendering-Pipeline die zu rendernden Objekte auswählt. Es enthält außerdem Referenzen auf _Shader-Programme_, die über den verfügbaren Grafiktreiber kompiliert und auf die Grafikhardware hochgeladen werden. Sie werden in jedem Frame ausgeführt, wenn die Komponente gerendert wird.

* Weitere Informationen zur Rendering-Pipeline findest du in der [Rendering-Dokumentation](/manuals/render).
* Eine ausführliche Erklärung von Shader-Programmen findest du in der [Shader-Dokumentation](/manuals/shader).

## Ein Material erstellen {#creating-a-material}

Um ein Material zu erstellen, führe im Browser *Assets* einen <kbd>Rechtsklick</kbd> auf einen Zielordner aus und wähle <kbd>New... ▸ Material</kbd>. (Du kannst auch im Menü <kbd>File ▸ New...</kbd> und anschließend <kbd>Material</kbd> wählen.) Benenne die neue Materialdatei und drücke <kbd>Ok</kbd>.

![Materialdatei](images/materials/material_file.png)

Das neue Material wird im *Material Editor* geöffnet.

![Materialeditor](images/materials/material.png)

Die Materialdatei enthält die folgenden Informationen:

Name
: Die Kennung des Materials. Mit diesem Namen wird das Material in der Ressource *Render* aufgeführt, um es in den Build aufzunehmen. Der Name wird auch in der Render-API-Funktion `render.enable_material()` verwendet. Der Name sollte eindeutig sein.

Vertex Program
: Die Datei des Vertex-Shader-Programms (*`.vp`*), die beim Rendern mit diesem Material verwendet wird. Das Vertex-Shader-Programm wird auf der GPU für jeden Vertex der Primitive einer Komponente ausgeführt. Es berechnet die Bildschirmposition jedes Vertex und gibt optional auch „varying“-Variablen aus, die interpoliert und an das Fragment-Programm übergeben werden.

Fragment Program
: Die Datei des Fragment-Shader-Programms (*`.fp`*), die beim Rendern mit diesem Material verwendet wird. Das Programm läuft auf der GPU für jedes Fragment (Pixel) eines Primitivs und bestimmt die Farbe jedes Fragments. Dies geschieht üblicherweise durch Texturabfragen und Berechnungen anhand von Eingabevariablen (Varying-Variablen oder Konstanten).

Vertex Constants
: Uniforms, die an das Vertex-Shader-Programm übergeben werden. Weiter unten findest du eine Liste der verfügbaren Konstanten.

Fragment Constants
: Uniforms, die an das Fragment-Shader-Programm übergeben werden. Weiter unten findest du eine Liste der verfügbaren Konstanten.

Samplers
: Du kannst in der Materialdatei optional bestimmte Sampler konfigurieren. Füge einen Sampler hinzu, gib ihm den im Shader-Programm verwendeten Namen und lege die Einstellungen für Texturadressierung und Filterung nach deinen Anforderungen fest.

Tags
: Die dem Material zugeordneten Tags. Die Engine stellt Tags als _Bitmaske_ dar, die [`render.predicate()`](/ref/render#render.predicate) verwendet, um Komponenten zusammenzufassen, die gemeinsam gezeichnet werden sollen. Wie das geht, erfährst du in der [Rendering-Dokumentation](/manuals/render). In einem Projekt kannst du höchstens 32 Tags verwenden.

## Attribute {#attributes}

Shader-Attribute (auch Vertex-Datenströme oder Vertex-Attribute genannt) legen fest, wie die GPU Vertices aus dem Speicher abruft, um Geometrie zu rendern. Der Vertex-Shader gibt mit dem Schlüsselwort `attribute` eine Menge von Datenströmen an. In den meisten Fällen erzeugt und bindet Defold die Daten im Hintergrund automatisch anhand der Namen dieser Datenströme. In manchen Fällen möchtest du jedoch zusätzliche Daten pro Vertex übergeben, um einen bestimmten Effekt zu erzielen, dessen Daten die Engine nicht erzeugt. Ein Vertex-Attribut kann mit den folgenden Feldern konfiguriert werden:

Name
: Der Attributname. Ähnlich wie bei Shader-Konstanten wird die Attributkonfiguration nur verwendet, wenn der Name mit einem im Vertex-Programm angegebenen Attribut übereinstimmt.

Semantic type
: Ein semantischer Typ gibt die Bedeutung des Attributs an, also *was* das Attribut darstellt und/oder *wie* es im Editor angezeigt werden soll. Wenn du beispielsweise für ein Attribut `SEMANTIC_TYPE_COLOR` angibst, zeigt der Editor eine Farbauswahl an. Die Engine übergibt die Daten dabei weiterhin unverändert an den Shader.

  - `SEMANTIC_TYPE_NONE` Der standardmäßige semantische Typ. Hat keinen weiteren Einfluss auf das Attribut, außer die Materialdaten für das Attribut direkt an den Vertex-Puffer zu übergeben (Standard)
  - `SEMANTIC_TYPE_POSITION` Erzeugt Positionsdaten pro Vertex für das Attribut. Kann zusammen mit dem Koordinatensystem verwendet werden, um der Engine vorzugeben, wie die Positionen berechnet werden
  - `SEMANTIC_TYPE_TEXCOORD` Erzeugt Texturkoordinaten pro Vertex für das Attribut
  - `SEMANTIC_TYPE_PAGE_INDEX` Erzeugt Seitenindizes pro Vertex für das Attribut
  - `SEMANTIC_TYPE_COLOR` Beeinflusst, wie der Editor das Attribut interpretiert. Wenn ein Attribut mit Farbsemantik konfiguriert ist, wird im Inspektor ein Farbauswahlfeld angezeigt
  - `SEMANTIC_TYPE_NORMAL` Erzeugt Normalendaten pro Vertex für das Attribut
  - `SEMANTIC_TYPE_TANGENT` Erzeugt Tangentendaten pro Vertex für das Attribut
  - `SEMANTIC_TYPE_WORLD_MATRIX` Erzeugt Weltmatrixdaten pro Vertex für das Attribut
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Erzeugt Normalenmatrixdaten pro Vertex für das Attribut
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Erzeugt eine 3x3-Texturtransformationsmatrix pro Vertex für das Attribut. Für Partikelkomponenten stellt die Engine eine Matrix bereit, die Koordinaten für die Bildeigenschaft der Komponente in das Atlas-Koordinatensystem transformiert. Für Sprite-Komponenten stellt die Engine für jedes von der Komponente verwendete Bild eine Matrix bereit (bei Verwendung mehrerer Texturen). Für Modellkomponenten wird eine Einheitsmatrix bereitgestellt.

Data type
: Der Datentyp der zugrunde liegenden Daten des Attributs.

  - `TYPE_BYTE` Vorzeichenbehaftete 8-Bit-Byte-Werte
  - `TYPE_UNSIGNED_BYTE` Vorzeichenlose 8-Bit-Byte-Werte
  - `TYPE_SHORT` Vorzeichenbehaftete 16-Bit-Short-Werte
  - `TYPE_UNSIGNED_SHORT` Vorzeichenlose 16-Bit-Short-Werte
  - `TYPE_INT` Vorzeichenbehaftete Ganzzahlwerte
  - `TYPE_UNSIGNED_INT` Vorzeichenlose Ganzzahlwerte
  - `TYPE_FLOAT` Gleitkommawerte (Standard)

Normalize
: Wenn diese Einstellung aktiviert ist, normalisiert der GPU-Treiber die Attributwerte. Das kann nützlich sein, wenn du nicht die volle Genauigkeit benötigst, aber Berechnungen durchführen möchtest, ohne die jeweiligen Grenzwerte zu kennen. Ein Farbvektor benötigt beispielsweise meist nur Byte-Werte von 0..255, wird im Shader aber trotzdem als Wert von 0..1 behandelt.

Coordinate space
: Einige semantische Typen unterstützen die Bereitstellung von Daten in unterschiedlichen Koordinatensystemen. Um einen Billboarding-Effekt mit Sprites umzusetzen, benötigst du üblicherweise ein Positionsattribut im lokalen Koordinatensystem sowie eine vollständig transformierte Position im Weltkoordinatensystem, damit Zeichenoperationen möglichst effektiv gebündelt werden können (Batching).

Vector type
: Der Vektortyp des Attributs.

  - `VECTOR_TYPE_SCALAR` Einzelner Skalarwert
  - `VECTOR_TYPE_VEC2` 2D-Vektor
  - `VECTOR_TYPE_VEC3` 3D-Vektor
  - `VECTOR_TYPE_VEC4` 4D-Vektor (Standard)
  - `VECTOR_TYPE_MAT2` 2D-Matrix
  - `VECTOR_TYPE_MAT3` 3D-Matrix
  - `VECTOR_TYPE_MAT4` 4D-Matrix

Step function
: Gibt an, wie die Attributdaten an die Vertex-Funktion übergeben werden sollen. Dies ist nur für Instancing relevant.

  - `Vertex` Einmal pro Vertex; ein Positionsattribut wird beispielsweise üblicherweise für jeden Vertex im Mesh an die Vertex-Funktion übergeben (Standard)
  - `Instance` Einmal pro Instanz; ein Weltmatrixattribut wird beispielsweise üblicherweise einmal pro Instanz an die Vertex-Funktion übergeben

Value
: Der Wert des Attributs. Attributwerte können für jede Komponente einzeln überschrieben werden; andernfalls dient dieser Wert als Standardwert des Vertex-Attributs. Hinweis: Bei *Standardattributen* (Position, Texturkoordinaten und Seitenindizes) wird der Wert ignoriert.

::: sidenote
Mit benutzerdefinierten Attributen kannst du auch den Speicherbedarf sowohl auf der CPU als auch auf der GPU verringern, indem du die Datenströme für einen kleineren Datentyp oder eine andere Elementanzahl konfigurierst.
:::

### Standardsemantik von Attributen {#default-attribute-semantics}

Das Materialsystem weist zur Laufzeit für eine bestimmte Menge von Attributnamen automatisch einen standardmäßigen semantischen Typ anhand des Namens zu:

  - `position` - semantischer Typ: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - semantischer Typ: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - semantischer Typ: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - semantischer Typ: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - semantischer Typ: `SEMANTIC_TYPE_COLOR`
  - `normal` - semantischer Typ: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - semantischer Typ: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - semantischer Typ: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - semantischer Typ: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - semantischer Typ: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Wenn du im Material Einträge für diese Attribute anlegst, wird der standardmäßige semantische Typ durch den im Materialeditor konfigurierten Typ überschrieben.

### Daten benutzerdefinierter Vertex-Attribute setzen {#setting-custom-vertex-attribute-data}

Ähnlich wie benutzerdefinierte Shader-Konstanten kannst du auch Vertex-Attribute zur Laufzeit aktualisieren, indem du `go.get`, `go.set` und `go.animate` aufrufst:

![Benutzerdefiniertes Materialattribut](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

Beim Aktualisieren von Vertex-Attributen gibt es jedoch einige Einschränkungen: Ob eine Komponente den Wert verwenden kann, hängt vom semantischen Typ des Attributs ab. Eine Sprite-Komponente unterstützt beispielsweise `SEMANTIC_TYPE_POSITION`. Wenn du ein Attribut mit diesem semantischen Typ aktualisierst, ignoriert die Komponente den überschriebenen Wert, da der semantische Typ vorgibt, dass die Daten immer aus der Position des Sprites erzeugt werden sollen.

Modellkomponenten stellen benutzerdefinierte Materialattribute ebenfalls über `go.get()`, `go.set()` und `go.animate()` bereit. Nachdem du beispielsweise ein Attribut namens `my_attribute` im Modellmaterial definiert hast:

```lua
go.set("#model", "my_attribute", vmath.vector4(1, 0, 0, 1))
go.animate("#model", "my_attribute", go.PLAYBACK_LOOP_PINGPONG,
    vmath.vector4(0, 1, 0, 1), go.EASING_LINEAR, 2)
```

Bei einem Modell mit mehreren Meshes kann derzeit nur das erste Mesh auf diese Weise angesprochen werden. Das Aktualisieren eines nicht instanzierten Attributs pro Vertex kann außerdem dazu führen, dass Vertex-Daten in einem zur Mesh-Größe proportionalen Umfang neu erstellt und hochgeladen werden. Häufige Aktualisierungen können daher bei großen Meshes aufwendig sein.

Wenn ein Vertex-Attribut ein Skalar oder ein anderer Vektortyp als `Vec4` ist, kannst du die Daten trotzdem mit `go.set` setzen:

```lua
-- The last two components in the vec4 will not be used!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

Dasselbe gilt für Matrixattribute: Wenn das Attribut einen anderen Matrixtyp als `Mat4` hat, kannst du die Daten trotzdem mit `go.set` setzen.

### Beispiele für benutzerdefinierte Vertex-Attribute {#examples-of-using-custom-vertex-attributes}

Ein Texturtransformationsattribut verwenden, um UV-Koordinaten in das Atlas-Koordinatensystem umzuwandeln:

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extract position from the transform
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extract the scale from the transform
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // convert to local UV (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Alternatively, if the UV coordinates already are in the 0..1 range,
  // you can transform into atlas space directly by multiplying the transform:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Pass the value into the fragment shader
  var_texcoord0 = localUV;

  // ... rest of vertex shader
}
```

### Instancing

Instancing ist eine Technik, mit der mehrere Kopien desselben Objekts in einer Szene effizient gezeichnet werden. Anstatt bei jeder Verwendung eine separate Kopie des Objekts zu erzeugen, kann die Grafik-Engine mit Instancing ein einzelnes Objekt erstellen und es mehrfach wiederverwenden. In einem Spiel mit einem großen Wald kannst du beispielsweise ein einziges Baummodell erstellen und es dann hunderte oder tausende Male mit unterschiedlichen Positionen und Skalierungen platzieren, anstatt für jeden Baum ein eigenes Modell anzulegen. Der Wald kann nun mit einem einzigen Zeichenaufruf (draw call) gerendert werden statt mit einzelnen Zeichenaufrufen für jeden Baum.

::: sidenote
Instancing ist derzeit nur für Modellkomponenten verfügbar.
:::

Instancing wird automatisch aktiviert, wenn es möglich ist. Defold setzt stark darauf, Zeichenoperationen mit gleichem Zustand möglichst weitgehend zu bündeln. Damit Instancing funktioniert, müssen einige Voraussetzungen erfüllt sein:

- Für alle Instanzen muss dasselbe Material verwendet werden. Instancing funktioniert auch dann, wenn ein benutzerdefiniertes Material mit `render.enable_material` gesetzt wurde
- Das Material muss für den Vertex-Koordinatenraum 'local' konfiguriert sein
- Das Material muss mindestens ein Vertex-Attribut haben, das pro Instanz wiederholt wird
- Konstantenwerte müssen für alle Instanzen gleich sein. Stattdessen können Konstantenwerte in benutzerdefinierten Vertex-Attributen oder auf andere Weise gespeichert werden (z. B. in einer Textur)
- Shader-Ressourcen wie Texturen oder Speicherpuffer müssen für alle Instanzen gleich sein

Damit ein Vertex-Attribut pro Instanz wiederholt wird, muss `Step function` auf `Instance` gesetzt sein. Bei bestimmten semantischen Typen geschieht dies automatisch anhand des Namens (siehe die Tabelle `Standardsemantik von Attributen` weiter oben). Du kannst dies aber auch im Materialeditor manuell einstellen, indem du `Step function` auf `Instance` setzt.

Als einfaches Beispiel enthält die folgende Szene vier Spielobjekte (game objects) mit jeweils einer Modellkomponente:

![Einrichtung von Instancing](images/materials/instancing-setup.png)

Das Material ist wie folgt konfiguriert, mit einem einzelnen benutzerdefinierten Vertex-Attribut, das pro Instanz wiederholt wird:

![Material für Instancing](images/materials/instancing-material.png)

Im Vertex-Shader sind mehrere Attribute pro Instanz angegeben:

```glsl
// Per vertex attributes
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Per instance attributes
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

Beachte, dass `mtx_world` und `mtx_normal` standardmäßig mit der Schritt-Funktion `Instance` konfiguriert werden. Du kannst dies im Materialeditor ändern, indem du für sie einen Eintrag hinzufügst und `Step function` auf `Vertex` setzt. Dadurch wird das Attribut pro Vertex statt pro Instanz wiederholt.

Um zu überprüfen, ob Instancing in diesem Fall funktioniert, kannst du den Web-Profiler verwenden. Da sich die Instanzen des Quaders in diesem Fall nur durch die Attribute pro Instanz unterscheiden, kann er mit einem einzigen Zeichenaufruf gerendert werden:

![Zeichenaufrufe beim Instancing](images/materials/instancing-draw-calls.png)

#### Abwärtskompatibilität {#backwards-compatibility}

OpenGL 3.1 auf Desktop-Geräten und OpenGL ES 3.0 auf Mobilgeräten bieten Instancing als Kernfunktion. Ältere OpenGL-ES- und WebGL-Kontexte können es weiterhin über eine Erweiterung wie `ANGLE_instanced_arrays` unterstützen; andere ältere Adapter unterstützen es nicht. Wenn Instancing nicht verfügbar ist, funktioniert das Rendering standardmäßig weiterhin, kann jedoch weniger leistungsfähig sein.

Verwende `graphics.get_adapter_info()`, um die Unterstützung zu erkennen und bei Bedarf ein weniger aufwendiges Material zu wählen oder Inhalte mit vielen Instanzen auszulassen. Das Feld `features` ist ein Array der unterstützten Funktionskonstanten, keine Tabelle mit diesen Konstanten als Schlüsseln:

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local instancing_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_INSTANCING
)
```

## Vertex- und Fragment-Konstanten {#vertex-and-fragment-constants}

Shader-Konstanten oder „Uniforms“ sind Werte, die die Engine an Vertex- und Fragment-Shader-Programme übergibt. Um eine Konstante zu verwenden, definierst du sie in der Materialdatei entweder als Eigenschaft *Vertex Constant* oder als Eigenschaft *Fragment Constant*. Entsprechende `uniform`-Variablen müssen im Shader-Programm definiert werden. Die folgenden Konstanten können in einem Material gesetzt werden:

`CONSTANT_TYPE_WORLD`
: Die Weltmatrix. Verwende sie, um Vertices in das Weltkoordinatensystem zu transformieren. Bei einigen Komponententypen liegen die Vertices bereits im Weltkoordinatensystem vor, wenn sie an das Vertex-Programm übergeben werden (aufgrund der Bündelung von Zeichenoperationen). In diesen Fällen liefert die Multiplikation mit der Weltmatrix im Shader falsche Ergebnisse.

`CONSTANT_TYPE_VIEW`
: Die Ansichtsmatrix. Verwende sie, um Vertices in das Ansichtskoordinatensystem (Kamerakoordinatensystem) zu transformieren.

`CONSTANT_TYPE_PROJECTION`
: Die Projektionsmatrix. Verwende sie, um Vertices in das Bildschirmkoordinatensystem zu transformieren.

`CONSTANT_TYPE_VIEWPROJ`
: Eine Matrix, in der die Ansichts- und Projektionsmatrix bereits miteinander multipliziert wurden.

`CONSTANT_TYPE_WORLDVIEW`
: Eine Matrix, in der die Welt- und Ansichtsmatrix bereits miteinander multipliziert wurden.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Eine Matrix, in der die Welt-, Ansichts- und Projektionsmatrix bereits miteinander multipliziert wurden.

`CONSTANT_TYPE_WORLD_INVERSE`
: Die Inverse der Weltmatrix. Verwende sie, um vom Weltkoordinatensystem zurück in das lokale Koordinatensystem des Objekts zu transformieren.

`CONSTANT_TYPE_VIEW_INVERSE`
: Die Inverse der Ansichtsmatrix. Verwende sie, um vom Kamerakoordinatensystem zurück in das Weltkoordinatensystem zu transformieren.

`CONSTANT_TYPE_PROJECTION_INVERSE`
: Die Inverse der Projektionsmatrix. Verwende sie, um vom Clip-Koordinatensystem zurück in das Kamerakoordinatensystem zu transformieren.

`CONSTANT_TYPE_VIEWPROJ_INVERSE`
: Die Inverse der kombinierten Ansichts- und Projektionsmatrix. Verwende sie, um vom Clip-Koordinatensystem zurück in das Weltkoordinatensystem zu transformieren.

`CONSTANT_TYPE_WORLDVIEW_INVERSE`
: Die Inverse der kombinierten Welt- und Ansichtsmatrix. Verwende sie, um vom Kamerakoordinatensystem zurück in das lokale Koordinatensystem des Objekts zu transformieren.

`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`
: Die Inverse der kombinierten Welt-, Ansichts- und Projektionsmatrix. Verwende sie, um vom Clip-Koordinatensystem zurück in das lokale Koordinatensystem des Objekts zu transformieren. Diese inversen Konstanten ersparen die Berechnung einer inversen Matrix im Shader.

`CONSTANT_TYPE_NORMAL`
: Eine Matrix zur Berechnung der Normalenausrichtung. Die Welttransformation kann eine ungleichmäßige Skalierung enthalten, die die Orthogonalität der kombinierten Welt-Ansichts-Transformation aufhebt. Die Normalenmatrix verhindert Richtungsprobleme beim Transformieren von Normalen. (Die Normalenmatrix ist die transponierte Inverse der Welt-Ansichts-Matrix.)

`CONSTANT_TYPE_TIME`
: Ein von der Engine bereitgestellter `vector4`, bei dem `.x` die seit dem Start der Engine verstrichene Zeit und `.y` die Zeitdifferenz zum vorherigen Frame enthält. `.z` und `.w` sind derzeit null. Die Engine aktualisiert diesen Wert automatisch; er muss nicht mit `go.set()` aktualisiert werden. Ein Beispiel findest du im [Shadertoy-Tutorial](/tutorials/shadertoy/#animation).

  Deklariere eine Time-Konstante namens `time` in einem modernen GLSL-Uniform-Block:

  ```glsl
  uniform fragment_inputs
  {
      vec4 time;
  };
  ```

`CONSTANT_TYPE_USER`
: Eine vector4-Konstante, die du für beliebige benutzerdefinierte Daten verwenden kannst, die du an deine Shader-Programme übergeben möchtest. Du kannst den Anfangswert der Konstante in ihrer Definition setzen und ihn anschließend über die Funktionen [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) ändern. Mit [go.get()](/ref/stable/go/#go.get) kannst du den Wert auch abrufen. Wenn du eine Materialkonstante einer einzelnen Komponenteninstanz änderst, [wird die Bündelung von Zeichenoperationen unterbrochen und es entstehen zusätzliche Zeichenaufrufe](/manuals/render/#draw-calls-and-batching).

Beispiel:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Eine matrix4-Konstante, die du für beliebige benutzerdefinierte Daten verwenden kannst, die du an deine Shader-Programme übergeben möchtest. Du kannst den Anfangswert der Konstante in ihrer Definition setzen und ihn anschließend über die Funktionen [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) ändern. Mit [go.get()](/ref/stable/go/#go.get) kannst du den Wert auch abrufen. Wenn du eine Materialkonstante einer einzelnen Komponenteninstanz änderst, [wird die Bündelung von Zeichenoperationen unterbrochen und es entstehen zusätzliche Zeichenaufrufe](/manuals/render/#draw-calls-and-batching).

Beispiel:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

### Materialkonstanten von GUI-Knoten {#gui-node-material-constants}

Lies und schreibe die Materialkonstanten eines Knotens innerhalb eines GUI-Skripts mit `gui.get()` und `gui.set()` statt mit den `go`-Funktionen. Vektorkomponenten, Matrixkonstanten und Konstantenarrays werden unterstützt. Array-Indizes in der Optionstabelle beginnen bei 1:

```lua
local node = gui.get_node("button")

local tint = gui.get(node, "tint")
gui.set(node, "tint.x", 0.5)
gui.set(node, "light_matrix", vmath.matrix4())
gui.set(node, "tint_array", vmath.vector4(1, 0, 0, 1), { index = 1 })
```

::: sidenote
Damit eine Materialkonstante vom Typ `CONSTANT_TYPE_USER` oder `CONSTANT_TYPE_USER_MATRIX4` über `go.get()` und `go.set()` oder `gui.get()` und `gui.set()` verfügbar ist, muss sie im Shader-Programm verwendet werden. Wenn die Konstante im Material definiert ist, aber im Programm nicht verwendet wird, wird sie aus dem Material entfernt und ist zur Laufzeit nicht verfügbar.
:::

## Sampler {#samplers}

Sampler dienen dazu, Farbinformationen aus einer Textur (einer Kachelquelle oder einem Atlas) abzutasten. Die Farbinformationen können anschließend für Berechnungen im Shader-Programm verwendet werden.

Sprite-, Kachelkarten-, GUI- und Partikeleffektkomponenten binden ihre Bildtextur automatisch an den zuerst deklarierten `sampler2D`. Sprite-Komponenten unterstützen außerdem mehrere Texturen: Jeder im Material deklarierte Sampler wird zu einem benannten Bildplatz in der Sprite-Komponente. Die erste Textur liefert die Animationsdaten des Sprites und steuert die Einzelbildfolge. Für jedes Einzelbild wird anhand seiner Bild-ID das entsprechende Bild in jeder zusätzlichen Textur gesucht, die jeweils ihre eigenen UV-Koordinaten liefert. Die zugewiesenen Atlanten oder Kachelquellen sollten daher übereinstimmende Einzelbild-IDs und ähnlich geformte Bilder enthalten; unterschiedliche polygonal gepackte Formen können zum Übergreifen benachbarter Texturpixel (texture bleeding) führen. Weitere Informationen findest du unter [Sprites mit mehreren Texturen](/manuals/sprite/#multi-textured-sprites).

Bei einer Komponente oder einem Rendering-Arbeitsablauf, der keinen zusätzlichen Texturplatz bereitstellt, kannst du mit [`render.enable_texture()`](/ref/render/#render.enable_texture) zusätzliche Textur-Sampler aus dem Render-Skript binden.

![Sprite-Sampler](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Du kannst die Sampler-Einstellungen einer Komponente festlegen, indem du den Sampler mit seinem Namen in der Materialdatei hinzufügst. Wenn du deinen Sampler nicht in der Materialdatei konfigurierst, werden die globalen Projekteinstellungen unter *graphics* verwendet.

![Sampler-Einstellungen](images/materials/my_sampler.png)

Für Modellkomponenten musst du deine Sampler mit den gewünschten Einstellungen in der Materialdatei angeben. Anschließend kannst du im Editor Texturen für jede Modellkomponente setzen, die das Material verwendet:

![Modell-Sampler](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Modell](images/materials/model.png)

## Sampler-Einstellungen {#sampler-settings}

Name
: Der Name des Samplers. Dieser Name sollte mit dem im Fragment-Shader deklarierten `sampler2D` übereinstimmen.

Wrap U/W
: Der Texturadressierungsmodus für die U- und V-Achse:

  - `WRAP_MODE_REPEAT` wiederholt Texturdaten außerhalb des Bereichs [0,1].
  - `WRAP_MODE_MIRRORED_REPEAT` wiederholt Texturdaten außerhalb des Bereichs [0,1], wobei jede zweite Wiederholung gespiegelt wird.
  - `WRAP_MODE_CLAMP_TO_EDGE` begrenzt Texturdaten für Werte größer als 1.0 auf 1.0 und setzt alle Werte kleiner als 0.0 auf 0.0---das heißt, die Randpixel werden bis zum Rand wiederholt.

Filter Min/Mag
: Die Filterung beim Vergrößern und Verkleinern. Nächster-Nachbar-Filterung erfordert weniger Berechnungen als lineare Interpolation, kann jedoch zu Aliasing-Artefakten führen. Lineare Interpolation liefert oft glattere Ergebnisse:

  - `Default` verwendet die Standardfilteroption, die in der Datei `game.project` unter `Graphics` als `Default Texture Min Filter` und `Default Texture Mag Filter` angegeben ist.
  - `FILTER_MODE_NEAREST` verwendet das Texel, dessen Koordinaten dem Mittelpunkt des Pixels am nächsten liegen.
  - `FILTER_MODE_LINEAR` berechnet einen gewichteten linearen Mittelwert des 2x2-Arrays der Texel, die dem Mittelpunkt des Pixels am nächsten liegen.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` wählt den nächstgelegenen Texelwert innerhalb einer einzelnen Mipmap.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` wählt das nächstgelegene Texel in den beiden am besten passenden Mipmaps und interpoliert anschließend linear zwischen diesen beiden Werten.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` interpoliert linear innerhalb einer einzelnen Mipmap.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` berechnet den Wert in jeder von zwei Mipmaps durch lineare Interpolation und interpoliert anschließend linear zwischen diesen beiden Werten.

Max Anisotropy
: Anisotrope Filterung ist eine fortgeschrittene Filtertechnik, die mehrere Abtastwerte nimmt und die Ergebnisse miteinander mischt. Diese Einstellung steuert den Anisotropiegrad für die Textur-Sampler. Wenn die GPU anisotrope Filterung nicht unterstützt, hat der Parameter keine Wirkung und wird standardmäßig auf 1 gesetzt.

## Konstantenpuffer {#constants-buffers}

Beim Zeichnen ruft die Rendering-Pipeline Konstantenwerte aus einem standardmäßigen Systemkonstantenpuffer ab. Du kannst einen benutzerdefinierten Konstantenpuffer erstellen, um die Standardkonstanten zu überschreiben und die Uniforms des Shader-Programms stattdessen im Render-Skript programmatisch zu setzen:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Erstelle einen neuen Konstantenpuffer
2. Setze die Konstante `tint` auf leuchtendes Rot
3. Zeichne das Prädikat mit unseren benutzerdefinierten Konstanten

Beachte, dass du die Konstantenelemente des Puffers wie die Einträge einer gewöhnlichen Lua-Tabelle ansprichst, den Puffer jedoch nicht mit `pairs()` oder `ipairs()` durchlaufen kannst.
