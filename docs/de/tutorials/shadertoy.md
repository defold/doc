---
brief: In diesem Tutorial passt du einen Shader von shadertoy.com für Defold an.
layout: tutorial
locale: de
title: Tutorial zur Übertragung von Shadertoy nach Defold
---

# Shadertoy-Tutorial

[Shadertoy.com](https://www.shadertoy.com/) ist eine Website, die von Nutzern beigesteuerte GL-Shader sammelt. Sie ist eine hervorragende Quelle für Shader-Code und Inspiration. In diesem Tutorial nehmen wir einen Shader von Shadertoy und bringen ihn in Defold zum Laufen. Grundkenntnisse über Shader werden vorausgesetzt. Falls du dich erst einlesen möchtest, ist [das Shader-Handbuch](/manuals/shader/) ein guter Einstieg.

Wir verwenden den Shader [Star Nest](https://www.shadertoy.com/view/XlfGRj) von Pablo Andrioli (Benutzer „Kali“ auf Shadertoy). Er ist ein rein prozeduraler Fragment-Shader, der mit mathematischer schwarzer Magie einen wirklich coolen Sternenfeldeffekt rendert.

![Star Nest](../images/shadertoy/starnest.png)

Der Shader besteht aus nur 65 Zeilen ziemlich kompliziertem GLSL-Code, aber keine Sorge. Wir behandeln ihn als Blackbox, die ihre Arbeit auf Grundlage einiger einfacher Eingaben erledigt. Unsere Aufgabe ist es, den Shader so anzupassen, dass er mit Defold statt mit Shadertoy zusammenarbeitet.

## Ein Objekt zum Texturieren {#something-to-texture}

Der Star-Nest-Shader ist ein reiner Fragment-Shader. Wir brauchen daher nur etwas, das der Shader texturieren kann. Dafür gibt es mehrere Möglichkeiten: ein Sprite, eine Kachelkarte (tile map), eine GUI oder ein Modell. In diesem Tutorial verwenden wir ein einfaches 3D-Modell. So können wir das Rendering des Modells leicht in einen Vollbildeffekt verwandeln – das brauchen wir beispielsweise für eine visuelle Nachbearbeitung.

Wir können mit einem leeren Projekt beginnen.

1. Öffne Defold und wähle Create From *Templates*.
2. Wähle *Empty Project*.
3. Lege den *Title* fest und wähle unter *Location* einen Speicherort auf deinem Datenträger.
4. Klicke auf <kbd>Create New Project</kbd>.

![Start](../images/shadertoy/empty_project.png)

Du kannst das integrierte Mesh `quad.gltf` aus `builtins/assets/meshes` verwenden.

Optional kannst du auch in Blender oder einem anderen 3D-Modellierungsprogramm ein Mesh in Form einer quadratischen Ebene erstellen – der Einfachheit halber liegen die Koordinaten der 4 Vertices bei -1 und 1 auf der X-Achse sowie bei -1 und 1 auf der Y-Achse. In Blender zeigt die Z-Achse standardmäßig nach oben. Deshalb musst du das Mesh um 90° um die X-Achse drehen. Du solltest außerdem darauf achten, korrekte UV-Koordinaten für das Mesh zu erzeugen. Wechsle in Blender bei ausgewähltem Mesh in den *Edit Mode* und wähle dann <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender ist eine kostenlose Open-Source-3D-Software, die du von [blender.org](https://www.blender.org) herunterladen kannst.
</div>

![Quad in Blender](../images/shadertoy/quad_blender.png)

1. Öffne deine Datei „main.collection“ in Defold und erstelle ein neues Spielobjekt (game object) namens „star-nest“.
2. Füge dem Spielobjekt „star-nest“ eine Komponente (component) vom Typ *Model* hinzu.
3. Setze die Eigenschaft *Mesh* auf unser `quad.gltf`.
4. Wir müssen das Material für das Modell festlegen. Wähle dafür zunächst das integrierte `model.material`.

Das Modell sollte im Szeneneditor erscheinen, wird aber vollständig schwarz gerendert. Das liegt daran, dass noch keine Textur zugewiesen ist:

![Quad in Defold](../images/shadertoy/quad_default_material.png)

## Das Material erstellen {#creating-the-material}

1. Erstelle eine neue Materialdatei *`star-nest.material`*, indem du im Bereich `Assets` mit der <kbd>rechten Maustaste</kbd> auf den Ordner `main` klickst, <kbd>New</kbd>-><kbd>Material</kbd> wählst und sie `star-nest` nennst.

 ![Material](../images/shadertoy/new_material.png)

2. Erstelle auf dieselbe Weise ein Vertex-Shader-Programm `star-nest.vp` und ein Fragment-Shader-Programm `star-nest.fp`:
3. Öffne die Datei *star-nest.material*.
4. Setze *Vertex Program* auf `star-nest.vp`.
5. Setze *Fragment Program* auf `star-nest.fp`.
6. Füge eine *Vertex Constant* hinzu, nenne sie „`view_proj`“ und gib ihr den Typ `Viewproj` (für „Ansichtsprojektion“).
8. Füge unter *Tags* das Tag „tile“ hinzu. So wird das Quad in den Renderdurchlauf aufgenommen, in dem Sprites und Kacheln gezeichnet werden.

 ![Material](../images/shadertoy/material.png)

### Vertex-Programm {#vertex-program}

1. Öffne die Datei `star-nest.vp` des Vertex-Shader-Programms. Sie sollte den folgenden Code enthalten:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Fragment-Programm {#fragment-program}

1. Öffne die Datei `star-nest.fp` des Fragment-Shader-Programms und ändere den Code so, dass die Fragmentfarbe anhand der X- und Y-Werte der UV-Koordinaten (`var_texcoord0`) gesetzt wird. So stellen wir sicher, dass wir das Modell korrekt eingerichtet haben:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Setze die Eigenschaft `Material` der Modellkomponente im Spielobjekt `star-nest` in der Sammlung (collection) `main.collection` auf unser neu erstelltes Material `star-nest`.

Jetzt sollte der Editor das Modell mit dem neuen Shader rendern, und wir können deutlich erkennen, ob die UV-Koordinaten korrekt sind: Die linke untere Ecke sollte schwarz (0, 0, 0), die linke obere Ecke grün (0, 1, 0), die rechte obere Ecke gelb (1, 1, 0) und die rechte untere Ecke rot (1, 0, 0) sein:

![Quad in Defold](../images/shadertoy/quad_material.png)

## Kamera {#camera}

Wir können unser Projekt jetzt ausführen (<kbd>Project</kbd>-><kbd>Build</kbd> oder die Tastenkombination <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), sehen aber einen schwarzen Bildschirm (na ja, fast – abgesehen von vielleicht einem winzigen Pixel in der linken unteren Ecke). Das liegt daran, dass es keine Kamera gibt und das Standard-Render-Skript auf eine einfache Ersatzdarstellung zurückgreift. Diese zeigt einen riesigen 2D-Raum, während unser Modell an Position (0,0,0) steht und eine Breite von nur 1 hat.

Fügen wir ein Spielobjekt mit einer Kamerakomponente hinzu, um festzulegen, was wir im Spiel sehen werden.

1. Füge ein Spielobjekt namens `camera` an Position (0,0,1) hinzu. (Es ist wichtig, die Z-Koordinate auf 1 zu setzen, damit dieses Spielobjekt vor unserem Modell liegt, denn die Z-Achse zeigt in der standardmäßigen 2D-Konfiguration auf uns zu).
2. Füge eine Komponente vom Typ `Camera` hinzu. Daraufhin siehst du eine Kameravorschau mit unserem Quad darin. In dieser Konfiguration haben wir das Glück, dass die Standardeigenschaften bereits passen und wir das korrekte Ergebnis sehen sollten. Eine einzige Sache können wir noch ändern: Wir brauchen kein so großes Sichtvolumen der Kamera und können daher `Far Z` auf `2` reduzieren.

![Kamera](../images/shadertoy/camera.png)

Optional können wir den Kameratyp ändern, indem wir `Orthographic Projection` auf `true` setzen und anschließend auch `Orthographic Zoom` auf einen Wert wie 600 einstellen. In diesem Fall wird das Seitenverhältnis jedoch nicht automatisch angepasst, sodass unser Modell den Bildschirm nicht ausfüllt.

## Der Star-Nest-Shader {#the-star-nest-shader}

Jetzt ist alles vorbereitet, und wir können mit dem eigentlichen Shader-Code beginnen. Sehen wir uns zunächst den Originalcode an. Er besteht aus mehreren Abschnitten:

![Code des Star-Nest-Shaders](../images/shadertoy/starnest_code.png)

Wir verwenden eine moderne Pipeline mit GLSL in Version 140. Dazu geben wir die Version am Anfang der Datei mit `#version 140` an.

1. Die Zeilen 5--18 definieren eine Reihe von Konstanten. Wir können sie unverändert lassen. Es sind gewöhnliche GLSL-Konstanten, die weder speziell von Shadertoy noch von Defold abhängen.

2. Die Zeilen 21 und 63 enthalten die X- und Y-Texturkoordinaten des Eingabefragments im Bildschirmkoordinatensystem (`in vec2 fragCoord`) und die Fragmentfarbe der Ausgabe (`out vec4 fragColor`).

    Defold übergibt Texturkoordinaten vom Vertex-Shader an den Fragment-Shader über eine interpolierte Variable als UV-Koordinaten (im Bereich 0--1). In unserem Vertex-Shader wird diese mit einem `out`-Qualifizierer deklariert:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     Im Fragment-Shader wird derselbe Wert mit einem `in`-Qualifizierer empfangen:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Anschließend deklarieren wir in GLSL 140 mit dem `out`-Qualifizierer eine explizite Fragmentausgabe:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Wo der ursprüngliche Shadertoy-Code in `fragColor` schreibt, schreibt unser Defold-Shader also in `out_fragColor`.

3. Die Zeilen 23--27 legen die Abmessungen der Textur sowie die Bewegungsrichtung und die skalierte Zeit fest. In Shadertoy erhält der Shader die Pixelposition über `fragCoord`, und die Auflösung des Ansichtsbereichs (viewport) beziehungsweise der Textur wird als `uniform vec3 iResolution` an den Shader übergeben. Aus den Fragmentkoordinaten und der Auflösung berechnet der Shader Koordinaten im Stil von UV-Koordinaten mit dem richtigen Seitenverhältnis. Außerdem werden einige auflösungsbezogene Verschiebungen vorgenommen, um einen schöneren Bildausschnitt zu erhalten.

    In Defold gehen wir nicht von Pixelkoordinaten aus. Stattdessen erhalten wir vom Vertex-Shader über `var_texcoord0` bereits normalisierte UV-Koordinaten. Diese Koordinaten liegen über das gerenderte Quad hinweg im Bereich von `0.0` bis `1.0`.

    In der Defold-Version müssen diese Berechnungen angepasst werden, damit sie die UV-Koordinaten aus `var_texcoord0` verwenden.
    Eine typische Umrechnung sieht so aus:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    Der genaue Wert von `aspect` hängt vom Aufbau des Beispiels ab. Wird der Effekt auf einem Quad gerendert, das bei bekannter Anzeigegröße den gesamten Bildschirm ausfüllt, kann das Seitenverhältnis für das Tutorial fest im Code vorgegeben werden. Soll der Effekt beliebige Fenstergrößen unterstützen, übergib die Auflösung als Fragmentkonstante und platziere sie in einem GLSL-140-Uniform-Block.

    Hier wird auch die Zeit eingerichtet. Sie wird als `uniform float iGlobalTime` an den Shader übergeben. Defold stellt Shadern seit Version 1.12.3 die Zeit über eine spezielle `Time`-Konstante bereit, die wir verwenden werden.

    In aktuellen Defold-Versionen werden nicht opake Uniforms innerhalb von Uniform-Blöcken deklariert.
    Im Fragment-Shader deklarieren wir sie so:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Anschließend fügen wir in `star-nest.material` eine Fragment Constant namens `time` hinzu und setzen ihren Typ auf `Time`.

    Der Wert kann dann so verwendet werden:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    Dabei ist `time.x` die Zeit seit dem Start der Engine und `time.y` die seit dem vorherigen Frame vergangene Zeit.

4. Die Zeilen 29--39 richten die Drehung des volumetrischen Renderings ein, wobei die Mausposition die Drehung beeinflusst. Die Mauskoordinaten werden als `uniform vec4 iMouse` an den Shader übergeben.

    In diesem Tutorial lassen wir die Mauseingabe weg.

5. Die Zeilen 41--62 bilden den Kern des Shaders. Wir können diesen Code unverändert lassen.

## Der angepasste Star-Nest-Shader {#the-modified-star-nest-shader}

Wenn wir die obigen Abschnitte durchgehen und die erforderlichen Änderungen vornehmen, erhalten wir den folgenden Shader-Code. Er wurde für eine bessere Lesbarkeit etwas aufgeräumt. Die Unterschiede zwischen der Defold- und der Shadertoy-Version sind gekennzeichnet:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Wir geben am Anfang der Datei #version 140 an, um Defolds moderne GLSL-Pipeline zu verwenden. Die Konstantendefinitionen lassen wir anschließend unverändert.
2. Der Vertex-Shader übergibt UV-Koordinaten über var_texcoord0 an den Fragment-Shader. In GLSL 140 empfängt der Fragment-Shader diesen interpolierten Wert mit in als Qualifizierer.
3. In GLSL 140 sollte der Fragment-Shader eine explizite Ausgabevariable deklarieren, statt in gl_FragColor zu schreiben. Hier verwenden wir out vec4 out_fragColor.
4. Defolds Materialkonstante Time wird dem Shader über einen Uniform-Block zugänglich gemacht. Füge in star-nest.material eine Fragment Constant namens time hinzu und setze ihren Typ auf Time.
5. Shadertoy verwendet mainImage(out vec4 fragColor, in vec2 fragCoord). In Defold verwenden wir den normalen Einstiegspunkt void main(), lesen die interpolierten UV-Koordinaten aus var_texcoord0 und schreiben die endgültige Farbe in out_fragColor.
6. Für dieses Tutorial definieren wir einen festen Wert für Auflösung und Seitenverhältnis des Renderings. Das Modell ist derzeit quadratisch, daher können wir vec2 res = vec2(1.0, 1.0); verwenden. Bei einem rechteckigen Modell mit den Abmessungen 1280 × 720 könnten wir stattdessen vec2 res = vec2(1.78, 1.0); verwenden und die UV-Koordinaten damit multiplizieren, um das korrekte Seitenverhältnis beizubehalten.
7. Der ursprüngliche Shadertoy-Shader verwendet iGlobalTime. In dieser Defold-Version enthält time.x die Zeit seit dem Start der Engine. Deshalb weisen wir sie einer lokalen Variablen iGlobalTime zu und verwenden sie, um die Kamerabewegung durch das Sternenfeld zu animieren.
8. Wir halten dieses Tutorial einfach, indem wir die iMouse-Werte vollständig entfernen. Die Drehung selbst behalten wir bei, da sie die visuelle Symmetrie im volumetrischen Rendering verringert.
9. Abschließend schreibt der Shader die resultierende Fragmentfarbe in out_fragColor.

Speichere das Fragment-Shader-Programm. Das Modell sollte jetzt im Szeneneditor und zur Laufzeit mit einem schönen Sternenfeld texturiert sein:

![Quad mit Star Nest](../images/shadertoy/quad_starnest.png)


## Animation

Das letzte Puzzleteil ist die Zeit, mit der wir die Sterne in Bewegung versetzen. Defold stellt sie seit Version 1.12.3 automatisch über eine Fragmentkonstante vom Typ `Time` bereit.

1. Öffne *star-nest.material*.
2. Füge eine *Fragment Constant* hinzu und nenne sie „time“.
3. Setze ihren *Type* auf `Time`.

![Zeitkonstante](../images/shadertoy/time_constant.png)

Das ist alles! Den Wert `time` verarbeiten wir bereits im Fragment-Shader. Wir sind fertig!

## Übungen {#exercises}

Eine unterhaltsame weiterführende Übung ist es, dem Shader die ursprüngliche Eingabe durch Mausbewegungen hinzuzufügen. Dafür musst du eine neue Fragment Constant erstellen, diesmal vom Typ `User`. Aktualisiere sie in `on_input` in einem Skript, das Mausbewegungen erkennt, indem du mit der Funktion `go.set()` die Eingabekoordinaten der neuen Konstante zuweist.

Viel Spaß mit Defold!
