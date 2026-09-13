---
title: Shader-Programme in Defold
brief: Dieses Handbuch beschreibt Vertex- und Fragment-Shader im Detail und erklärt, wie du sie in Defold verwendest.
---

# Shader {#shaders}

Shader-Programme bilden den Kern des Grafik-Renderings. Es sind Programme in einer C-ähnlichen Sprache namens GLSL (GL Shading Language), die von der Grafikhardware ausgeführt werden, um Operationen entweder auf den zugrunde liegenden 3D-Daten (den Vertices) oder auf den Pixeln durchzuführen, die schließlich auf dem Bildschirm erscheinen (den „Fragmenten“). Shader werden zum Zeichnen von Sprites, zum Beleuchten von 3D-Modellen, zum Erstellen bildschirmfüllender Nachbearbeitungseffekte und für vieles mehr verwendet.

Dieses Handbuch beschreibt, wie Defolds Rendering-Pipeline mit GPU-Shadern zusammenarbeitet. Um Shader für deine Inhalte zu erstellen, musst du auch das Konzept der Materialien und die Funktionsweise der Rendering-Pipeline verstehen.

* Einzelheiten zur Rendering-Pipeline findest du im [Rendering-Handbuch](/manuals/render).
* Einzelheiten zu Materialien findest du im [Materialhandbuch](/manuals/material).
* Einzelheiten zu Compute-Programmen findest du im [Compute-Handbuch](/manuals/compute).

Die Spezifikationen von OpenGL ES 2.0 (OpenGL for Embedded Systems) und OpenGL ES Shading Language findest du im [Khronos OpenGL Registry](https://www.khronos.org/registry/gles/).

Beachte, dass du auf Desktop-Computern Shader schreiben kannst, die Funktionen verwenden, die in OpenGL ES 2.0 nicht verfügbar sind. Dein Grafikkartentreiber kompiliert und führt möglicherweise problemlos Shader-Code aus, der auf Mobilgeräten nicht funktioniert.


## Konzepte {#concepts}

Vertex-Shader
: Ein Vertex-Shader kann keine Vertices erstellen oder löschen, sondern nur die Position eines Vertex ändern. Vertex-Shader werden häufig verwendet, um die Positionen von Vertices aus dem 3D-Weltkoordinatensystem in das 2D-Bildschirmkoordinatensystem zu transformieren.

  Die Eingabe eines Vertex-Shaders besteht aus Vertex-Daten (in Form von `attributes`) und Konstanten (`uniforms`). Häufig verwendete Konstanten sind die Matrizen, die benötigt werden, um die Position eines Vertex in das Bildschirmkoordinatensystem zu transformieren und zu projizieren.

  Die Ausgabe des Vertex-Shaders ist die berechnete Bildschirmposition des Vertex (`gl_Position`). Außerdem können Daten über `varying`-Variablen vom Vertex-Shader an den Fragment-Shader übergeben werden.

Fragment-Shader
: Nachdem der Vertex-Shader fertig ist, bestimmt der Fragment-Shader die Farbe jedes Fragments (oder Pixels) der resultierenden Primitive.

  Die Eingabe eines Fragment-Shaders besteht aus Konstanten (`uniforms`) sowie allen `varying`-Variablen, die vom Vertex-Shader gesetzt wurden.

  Die Ausgabe des Fragment-Shaders ist der Farbwert für das jeweilige Fragment (`gl_FragColor`).

Compute-Shader
: Ein Compute-Shader ist ein universell einsetzbarer Shader, mit dem beliebige Aufgaben auf einer GPU ausgeführt werden können. Er ist überhaupt kein Teil der Grafik-Pipeline. Compute-Shader laufen in einem separaten Ausführungskontext und sind nicht von der Eingabe anderer Shader abhängig.

  Die Eingabe eines Compute-Shaders besteht aus Konstantenpuffern (`uniforms`), Texturbildern (`image2D`), Samplern (`sampler2D`) und Speicherpuffern (`buffer`).

  Die Ausgabe des Compute-Shaders ist nicht ausdrücklich festgelegt. Anders als bei Vertex- und Fragment-Shadern gibt es keine bestimmte Ausgabe, die erzeugt werden muss. Da Compute-Shader universell einsetzbar sind, legt die programmierende Person fest, welche Art von Ergebnis der Compute-Shader erzeugen soll.

Weltmatrix
: Die Vertex-Positionen der Form eines Modells werden relativ zum Ursprung des Modells gespeichert. Das wird als „Modellkoordinatensystem“ (model space) bezeichnet. Die Spielwelt hingegen ist ein „Weltkoordinatensystem“ (world space), in dem Position, Ausrichtung und Skalierung jedes Vertex relativ zum Weltursprung angegeben werden. Durch diese Trennung kann die Game-Engine jedes Modell verschieben, drehen und skalieren, ohne die ursprünglichen Vertex-Werte zu zerstören, die in der Modellkomponente (model component) gespeichert sind.

  Wenn ein Modell in der Spielwelt platziert wird, müssen die lokalen Vertex-Koordinaten des Modells in Weltkoordinaten umgerechnet werden. Diese Umrechnung erfolgt durch eine *Welttransformationsmatrix*, die angibt, welche Verschiebung (Bewegung), Drehung und Skalierung auf die Vertices eines Modells angewendet werden sollen, damit sie korrekt im Koordinatensystem der Spielwelt platziert werden.

  ![Welttransformation](images/shader/world_transform.png)

Ansichts- und Projektionsmatrix
: Damit die Vertices der Spielwelt auf dem Bildschirm erscheinen, werden die 3D-Koordinaten jeder Matrix zunächst in Koordinaten relativ zur Kamera umgerechnet. Dies erfolgt mit einer _Ansichtsmatrix_. Anschließend werden die Vertices mit einer _Projektionsmatrix_ in das 2D-Bildschirmkoordinatensystem projiziert:

  ![Projektion](images/shader/projection.png)

Attribute
: Ein Wert, der einem einzelnen Vertex zugeordnet ist. Attribute werden von der Engine an den Shader übergeben. Wenn du auf ein Attribut zugreifen möchtest, deklarierst du es einfach in deinem Shader-Programm. Verschiedene Komponententypen (component types) haben unterschiedliche Sätze von Attributen:
  - Ein Sprite besitzt `position` und `texcoord0`.
  - Ein Kachelraster (Tilegrid) besitzt `position` und `texcoord0`.
  - Ein GUI-Knoten (GUI node) besitzt `position`, `textcoord0` und `color`.
  - Ein Partikeleffekt (ParticleFX) besitzt `position`, `texcoord0` und `color`.
  - Ein Modell besitzt `position`, `texcoord0` und `normal`.
  - Eine Schriftressource besitzt `position`, `texcoord0`, `face_color`, `outline_color` und `shadow_color`.

Konstanten
: Shader-Konstanten bleiben für die Dauer des Zeichenaufrufs (draw call) unverändert. Konstanten werden den Abschnitten *Constants* der Materialdatei hinzugefügt und anschließend im Shader-Programm als `uniform` deklariert. Sampler-Uniforms werden dem Abschnitt *Samplers* des Materials hinzugefügt und anschließend im Shader-Programm als `uniform` deklariert. Die Matrizen, die für Vertex-Transformationen in einem Vertex-Shader benötigt werden, sind als Konstanten verfügbar:

  - `CONSTANT_TYPE_WORLD` ist die *Weltmatrix*, die vom lokalen Koordinatensystem eines Objekts in das Weltkoordinatensystem abbildet.
  - `CONSTANT_TYPE_VIEW` ist die *Ansichtsmatrix*, die vom Weltkoordinatensystem in das Kamerakoordinatensystem abbildet.
  - `CONSTANT_TYPE_PROJECTION` ist die *Projektionsmatrix*, die vom Kamerakoordinatensystem in das Bildschirmkoordinatensystem abbildet.
  - `CONSTANT_TYPE_WORLDVIEW`, `CONSTANT_TYPE_VIEWPROJ` und `CONSTANT_TYPE_WORLDVIEWPROJ` stellen die entsprechenden kombinierten Matrizen bereit.
  - `CONSTANT_TYPE_WORLD_INVERSE`, `CONSTANT_TYPE_VIEW_INVERSE`, `CONSTANT_TYPE_PROJECTION_INVERSE`, `CONSTANT_TYPE_VIEWPROJ_INVERSE`, `CONSTANT_TYPE_WORLDVIEW_INVERSE` und `CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE` stellen inverse Matrizen bereit, ohne dass der Shader sie berechnen muss.
  - `CONSTANT_TYPE_TIME` ist ein von der Engine bereitgestellter `vec4`: die seit dem Engine-Start vergangene Zeit in `.x`, die Frame-Deltazeit in `.y` und null in `.z` und `.w`.
  - `CONSTANT_TYPE_USER` ist eine Konstante vom Typ `vec4`, die du nach Belieben verwenden kannst.

  Das [Materialhandbuch](/manuals/material) erklärt, wie du Konstanten festlegst.

Sampler
: Shader können Uniform-Variablen vom Typ *sampler* deklarieren. Sampler werden verwendet, um Werte aus einer Bildquelle zu lesen:

  - `sampler2D` tastet eine 2D-Bildtextur ab.
  - `sampler2DArray` tastet eine Array-Textur aus 2D-Bildern ab. Dies wird hauptsächlich für mehrseitige Atlanten verwendet.
  - `samplerCube` tastet eine Cubemap-Textur aus 6 Bildern ab.
  - `image2D` lädt (und speichert gegebenenfalls) Texturdaten in ein Bildobjekt. Dies wird hauptsächlich zur Speicherung in Compute-Shadern verwendet.

  Du kannst einen Sampler nur in den Texturabfragefunktionen der GLSL-Standardbibliothek verwenden. Das [Materialhandbuch](/manuals/material) erklärt, wie du Sampler-Einstellungen festlegst.

UV-Koordinaten
: Einem Vertex ist eine 2D-Koordinate zugeordnet, die auf einen Punkt auf einer 2D-Textur abbildet. Ein Teil oder die gesamte Textur kann deshalb auf die Form aufgetragen werden, die durch einen Satz von Vertices beschrieben wird.

  ![UV-Koordinaten](images/shader/uv_map.png)

  Eine UV-Abbildung wird üblicherweise im 3D-Modellierungsprogramm erzeugt und im Mesh gespeichert. Die Texturkoordinaten für jeden Vertex werden dem Vertex-Shader als Attribut bereitgestellt. Anschließend wird eine `varying`-Variable verwendet, um die UV-Koordinate für jedes Fragment durch Interpolation der Vertex-Werte zu ermitteln.

Varying-Variablen
: Variablen vom Typ `Varying` werden verwendet, um Informationen zwischen der Vertex-Stufe und der Fragment-Stufe zu übergeben.

  1. Eine Varying-Variable wird im Vertex-Shader für jeden Vertex gesetzt.
  2. Während der Rasterisierung wird dieser Wert für jedes Fragment des gerenderten Primitivs interpoliert. Der Abstand des Fragments zu den Vertices der Form bestimmt den interpolierten Wert.
  3. Die Variable wird für jeden Aufruf des Fragment-Shaders gesetzt und kann für Fragmentberechnungen verwendet werden.

  ![Varying-Interpolation](images/shader/varying_vertex.png)

  Wenn du beispielsweise an jeder Ecke eines Dreiecks ein `varying` auf einen RGB-Farbwert vom Typ `vec3` setzt, werden die Farben über die gesamte Form interpoliert. Ebenso ermöglicht das Setzen von Texturabfragekoordinaten (oder *UV-Koordinaten*) an jedem Vertex eines Rechtecks dem Fragment-Shader, Texturfarbwerte für die gesamte Fläche der Form abzufragen.

  ![Varying-Interpolation](images/shader/varying.png)

## Moderne GLSL-Shader schreiben {#writing-modern-glsl-shaders}

Da die Defold-Engine mehrere Plattformen und Grafik-APIs unterstützt, muss es für Entwickler einfach sein, Shader zu schreiben, die überall funktionieren. Die Asset-Pipeline erreicht dies hauptsächlich auf zwei Wegen (im Folgenden als `Shader-Pipelines` bezeichnet):

1. Die alte Pipeline, in der Shader in ES2-kompatiblem GLSL-Code geschrieben werden.
2. Die moderne Pipeline, in der Shader in SPIR-v-kompatiblem GLSL-Code geschrieben werden.

Seit Defold 1.9.2 wird empfohlen, Shader zu schreiben, die die neue Pipeline verwenden. Dafür müssen die meisten Shader so umgestellt werden, dass sie mindestens Version 140 (OpenGL 3.1) verwenden. Stelle beim Umstellen eines Shaders sicher, dass diese Anforderungen erfüllt sind:

### Versionsdeklaration {#version-declaration}
Setze mindestens #version 140 an den Anfang des Shaders:

```glsl
#version 140
```

Auf diese Weise wird die Shader-Pipeline im Build-Vorgang ausgewählt, weshalb du die alten Shader weiterhin verwenden kannst. Wird keine Präprozessordirektive für die Version gefunden, greift Defold auf die alte Pipeline zurück.

### Attribute {#attributes}
Ersetze in Vertex-Shadern das Schlüsselwort `attribute` durch `in`:

```glsl
// instead of:
// attribute vec4 position;
// do:
in vec4 position;
```

Hinweis: Fragment-Shader (und Compute-Shader) erhalten keine Vertex-Eingaben.

### Varyings
In Vertex-Shadern sollte Varyings ein `out` vorangestellt werden. In Fragment-Shadern werden Varyings zu `in`:

```glsl
// In a vertex shader, instead of:
// varying vec4 var_color;
// do:
out vec4 var_color;

// In a fragment shader, instead of:
// varying vec4 var_color;
// do:
in vec4 var_color;
```

### Uniforms (in Defold Konstanten genannt) {#uniforms-called-constants-in-defold}

Opake Uniform-Typen (Sampler, Images, Atomics, SSBOs) müssen nicht umgestellt werden. Du kannst sie wie bisher verwenden:

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

Nicht opake Uniform-Typen musst du in einem `uniform block` unterbringen. Ein Uniform-Block ist einfach eine Gruppe von Uniform-Variablen und wird mit dem Schlüsselwort `uniform` deklariert:

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Individual members of the uniform block can be used as-is
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

Alle Elemente des Uniform-Blocks werden Materialien und Komponenten als einzelne Konstanten bereitgestellt. Für die Verwendung von Render-Konstantenpuffern oder `go.set` und `go.get` ist keine Umstellung erforderlich.

### Integrierte Variablen {#built-in-variables}

In Fragment-Shadern ist `gl_FragColor` ab Version 140 veraltet und zur Ablösung vorgesehen. Verwende stattdessen `out`:

```glsl
// instead of:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// do:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### Texturfunktionen {#texture-functions}

Spezifische Funktionen zur Texturabtastung wie `texture2D` und `texture2DArray` gibt es nicht mehr. Verwende stattdessen einfach die Funktion `texture`:

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// instead of:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// do:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### Genauigkeit {#precision}

Defold erzeugt beim Cross-Kompilieren von Shadern für GLSL ES globale Standardqualifizierer für die Genauigkeit. Die Standardwerte sind `mediump` für Gleitkommawerte und `highp` für Ganzzahlen. Sie können mit **GLSL ES Default Precision Float** (`shader.glsl_es_default_precision_float`) und **GLSL ES Default Precision Int** (`shader.glsl_es_default_precision_int`) in den [Projekteinstellungen](/manuals/project-settings/#shader) geändert werden; beide akzeptieren `mediump` oder `highp`.

Ein expliziter Qualifizierer an einer Variablen, Eingabe oder Ausgabe hat Vorrang vor dem erzeugten globalen Standardwert. Bei Fragment-Shadern für OpenGL ES 2.0 und WebGL 1.0 wird `highp` nicht von jedem Gerät unterstützt. Wenn `highp` als globaler Standardwert ausgewählt ist, sichert Defold ihn mit `GL_FRAGMENT_PRECISION_HIGH` ab und greift auf Geräten, die ihn nicht unterstützen, auf `mediump` zurück.

### Alles zusammenführen {#putting-it-together}

Als abschließendes Beispiel, in dem all diese Regeln angewendet werden, folgen hier die integrierten Sprite-Shader, die in das neue Format umgewandelt wurden:

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// positions are in world space
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Premultiply alpha since all runtime textures already are
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## Codeausschnitte in Shader einbinden {#including-snippets-into-shaders}

Shader in Defold unterstützen das Einbinden von Quellcode aus Dateien innerhalb des Projekts, die die Erweiterung `.glsl` haben. Um eine GLSL-Datei aus einem Shader einzubinden, verwende das Pragma `#include` mit doppelten Anführungszeichen oder spitzen Klammern. Includes müssen entweder Pfade relativ zum Projekt oder einen Pfad relativ zu der Datei verwenden, die sie einbindet:

```glsl
// In file /main/my-shader.fp

// Absolute path
#include "/main/my-snippet.glsl"
// The file is in the same folder
#include "my-snippet.glsl"
// The file is in a sub-folder on the same level as 'my-shader'
#include "sub-folder/my-snippet.glsl"
// The file is in a sub-folder on the parent directory, i.e /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// The file is on the parent directory, i.e /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

Bei der Verarbeitung von Includes gibt es einige Besonderheiten:

  - Dateien müssen relativ zum Projekt angegeben werden, das heißt, du kannst nur Dateien einbinden, die sich innerhalb des Projekts befinden. Jeder absolute Pfad muss mit einem führenden `/` angegeben werden
  - Du kannst Code überall in der Datei einbinden, aber keine Datei innerhalb einer Anweisung. Beispielsweise funktioniert `const float #include "my-float-name.glsl" = 1.0` nicht

### Include-Schutz {#header-guards}

Codeausschnitte können selbst weitere `.glsl`-Dateien einbinden. Dadurch kann der endgültig erzeugte Shader denselben Code mehrfach enthalten. Je nach Inhalt der Dateien können Kompilierungsprobleme entstehen, weil dieselben Symbole mehr als einmal deklariert werden. Um dies zu vermeiden, kannst du einen *Include-Schutz (header guards)* verwenden, ein in mehreren Programmiersprachen verbreitetes Konzept. Beispiel:

```glsl
// In my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// In math-functions.glsl
#include "pi.glsl"

// In pi.glsl
const float PI = 3.14159265359;
```

In diesem Beispiel wird die Konstante `PI` zweimal definiert, was beim Ausführen des Projekts zu Compilerfehlern führt. Du solltest die Inhalte stattdessen mit einem Include-Schutz versehen:

```glsl
// In pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

Der Code aus `pi.glsl` wird zweimal in `my-shader.vs` eingefügt. Da du ihn jedoch mit einem Include-Schutz umschlossen hast, wird das Symbol PI nur einmal definiert und der Shader erfolgreich kompiliert.

Je nach Anwendungsfall ist dies jedoch nicht immer zwingend erforderlich. Wenn du Code stattdessen lokal in einer Funktion oder an anderer Stelle wiederverwenden möchtest, an der die Werte nicht global im Shader-Code verfügbar sein müssen, solltest du wahrscheinlich keinen Include-Schutz verwenden. Beispiel:

```glsl
// In red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// In my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## Editorspezifischer Shader-Code {#editor-specific-shader-code}

Wenn Shader im Ansichtsbereich (viewport) des Defold-Editors gerendert werden, steht die Präprozessordefinition `EDITOR` zur Verfügung. Dadurch kannst du Shader-Code schreiben, der sich bei der Ausführung im Editor anders verhält als bei der Ausführung in der eigentlichen Game-Engine.

Dies ist besonders nützlich für:
  - Das Hinzufügen von Debug-Visualisierungen, die nur im Editor erscheinen sollen.
  - Die Implementierung editorspezifischer Funktionen wie Drahtgittermodi oder Materialvorschauen.
  - Das Bereitstellen einer alternativen Rendering-Darstellung für Materialien, die im Ansichtsbereich des Editors möglicherweise nicht richtig funktionieren.

Verwende die Präprozessordirektive `#ifdef EDITOR`, um Code bedingt zu kompilieren, der nur im Editor ausgeführt werden soll:

```glsl
#ifdef EDITOR
    // This code will only execute when the shader is rendered in the Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Magenta color for editor preview
#else
    // This code will execute when running in the game
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## Der Rendering-Vorgang {#the-rendering-process}

Bevor die Daten, die du für dein Spiel erstellst, auf dem Bildschirm erscheinen, durchlaufen sie eine Reihe von Schritten:

![Rendering-Pipeline](images/shader/pipeline.png)

Alle visuellen Komponenten (Sprites, GUI-Knoten, Partikeleffekte oder Modelle) bestehen aus Vertices, Punkten in der 3D-Welt, die die Form der Komponente beschreiben. Der Vorteil dabei ist, dass die Form aus jedem Winkel und aus jeder Entfernung betrachtet werden kann. Die Aufgabe des Vertex-Shader-Programms besteht darin, einen einzelnen Vertex in eine Position im Ansichtsbereich umzurechnen, damit die Form auf dem Bildschirm erscheinen kann. Bei einer Form mit 4 Vertices wird das Vertex-Shader-Programm 4 Mal ausgeführt, jeweils parallel.

![Vertex-Shader](images/shader/vertex_shader.png)

Die Eingabe des Programms ist die Vertex-Position (und weitere Attributdaten, die dem Vertex zugeordnet sind). Die Ausgabe ist eine neue Vertex-Position (`gl_Position`) sowie alle `varying`-Variablen, die für jedes Fragment interpoliert werden sollen.

Das einfachste Vertex-Shader-Programm setzt die Ausgabeposition lediglich auf einen Vertex am Nullpunkt (was nicht besonders nützlich ist):

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Ein vollständigeres Beispiel ist der integrierte Sprite-Vertex-Shader:

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. Ein Uniform (eine Konstante), das das Produkt aus Ansichts- und Projektionsmatrix enthält.
2. Attribute für den Sprite-Vertex. `position` wurde bereits in das Weltkoordinatensystem transformiert. `texcoord0` enthält die UV-Koordinate für den Vertex.
3. Deklariere eine Varying-Ausgabevariable. Diese Variable wird für jedes Fragment zwischen den für jeden Vertex gesetzten Werten interpoliert und an den Fragment-Shader gesendet.
4. `gl_Position` wird auf die Ausgabeposition des aktuellen Vertex im Projektionskoordinatensystem gesetzt. Dieser Wert hat 4 Komponenten: `x`, `y`, `z` und `w`. Die Komponente `w` wird verwendet, um eine perspektivisch korrekte Interpolation zu berechnen. Dieser Wert ist normalerweise 1,0 für jeden Vertex, bevor eine Transformationsmatrix angewendet wird.
5. Setze die Varying-UV-Koordinate für diese Vertex-Position. Nach der Rasterisierung wird sie für jedes Fragment interpoliert und an den Fragment-Shader gesendet.




Nach dem Vertex-Shading steht die Form der Komponente auf dem Bildschirm fest: Primitive Formen werden erzeugt und gerastert. Das bedeutet, dass die Grafikhardware jede Form in *Fragmente* oder Pixel aufteilt. Anschließend führt sie das Fragment-Shader-Programm einmal für jedes Fragment aus. Bei einem Bild auf dem Bildschirm mit einer Größe von 16 × 24 Pixeln wird das Programm 384 Mal ausgeführt, jeweils parallel.

![Fragment-Shader](images/shader/fragment_shader.png)

Die Eingabe des Programms ist alles, was die Rendering-Pipeline und der Vertex-Shader senden, üblicherweise die *UV-Koordinaten* des Fragments, Einfärbungsfarben usw. Die Ausgabe ist die endgültige Farbe des Pixels (`gl_FragColor`).

Das einfachste Fragment-Shader-Programm setzt die Farbe jedes Pixels lediglich auf Schwarz (auch dies ist kein besonders nützliches Programm):

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

Auch hier ist der integrierte Sprite-Fragment-Shader ein vollständigeres Beispiel:

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. Die Varying-Variable für die Texturkoordinate wird deklariert. Der Wert dieser Variablen wird für jedes Fragment zwischen den Werten interpoliert, die für jeden Vertex der Form gesetzt wurden.
2. Eine Uniform-Variable vom Typ `sampler2D` wird deklariert. Der Sampler wird zusammen mit den interpolierten Texturkoordinaten verwendet, um die Textur abzufragen, damit das Sprite korrekt texturiert werden kann. Da es sich um ein Sprite handelt, ordnet die Engine diesem Sampler das Bild zu, das in der Eigenschaft *Image* des Sprites festgelegt ist.
3. Eine Konstante vom Typ `CONSTANT_TYPE_USER` wird im Material definiert und als `uniform` deklariert. Ihr Wert ermöglicht die Einfärbung des Sprites. Der Standardwert ist reines Weiß.
4. Der Farbwert der Einfärbung wird mit seinem Alphawert vormultipliziert, da alle Texturen zur Laufzeit bereits vormultipliziertes Alpha enthalten.
5. Taste die Textur an der interpolierten Koordinate ab und gib den abgetasteten Wert zurück.
6. `gl_FragColor` wird auf die Ausgabefarbe für das Fragment gesetzt: die diffuse Farbe aus der Textur, multipliziert mit dem Einfärbungswert.

Der resultierende Fragmentwert durchläuft anschließend Tests. Ein häufiger Test ist der *Tiefentest*, bei dem der Tiefenwert des Fragments mit dem Wert im Tiefenpuffer für das getestete Pixel verglichen wird. Je nach Test kann das Fragment verworfen oder ein neuer Wert in den Tiefenpuffer geschrieben werden. Eine häufige Anwendung dieses Tests besteht darin, näher an der Kamera liegende Grafik weiter hinten liegende Grafik verdecken zu lassen.

Wenn der Test ergibt, dass das Fragment in den Framebuffer geschrieben werden soll, wird es mit den bereits im Puffer vorhandenen Pixeldaten *gemischt*. Mischparameter, die im Render-Skript festgelegt werden, ermöglichen es, die Quellfarbe (den vom Fragment-Shader geschriebenen Wert) und die Zielfarbe (die Farbe aus dem Bild im Framebuffer) auf verschiedene Weise zu kombinieren. Eine häufige Anwendung des Mischens besteht darin, transparente Objekte rendern zu können.

## Weiterführende Informationen {#further-study}

- [Shadertoy](https://www.shadertoy.com) enthält eine riesige Anzahl von Shadern, die von Nutzern beigetragen wurden. Die Website ist eine großartige Inspirationsquelle, auf der du verschiedene Shading-Techniken kennenlernen kannst. Viele der dort vorgestellten Shader lassen sich mit sehr wenig Aufwand nach Defold portieren. Das [Shadertoy-Tutorial](https://www.defold.com/tutorials/shadertoy/) erklärt die einzelnen Schritte, um einen vorhandenen Shader für Defold umzuwandeln.

- Das [Tutorial zur Farbkorrektur](https://www.defold.com/tutorials/grading/) zeigt, wie du einen bildschirmfüllenden Farbkorrektureffekt mithilfe von Texturen mit Farbnachschlagetabellen erstellst.

- [The Book of Shaders](https://thebookofshaders.com/00/) zeigt dir, wie du Shader in deinen Projekten verwendest und integrierst und dadurch deren Leistung und Grafikqualität verbesserst.
