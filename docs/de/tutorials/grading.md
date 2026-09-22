---
title: Tutorial zu einem Shader für Farbkorrektur
brief: In diesem Tutorial erstellst du in Defold einen Nachbearbeitungseffekt für den gesamten Bildschirm.
---

# Tutorial zur Farbkorrektur {#grading-tutorial}

In diesem Tutorial erstellen wir einen Nachbearbeitungseffekt zur Farbkorrektur (color grading) für den gesamten Bildschirm. Die zugrunde liegende Rendertechnik lässt sich vielseitig für verschiedene Nachbearbeitungseffekte wie Unschärfe, Nachzieheffekte, Leuchten, Farbanpassungen und andere verwenden.

Wir gehen davon aus, dass du dich im Defold-Editor zurechtfindest und grundlegende Kenntnisse über GL-Shader und die Rendering-Pipeline von Defold hast. Wenn du dich in diese Themen einlesen möchtest, sieh dir [unser Shader-Handbuch](/manuals/shader/) und das [Render-Handbuch](/manuals/render/) an.

## Renderziele {#render-targets}

Mit dem Standard-Render-Skript (render script) wird jede visuelle Komponente (component), etwa ein Sprite, eine Kachelkarte (tile map), ein Partikeleffekt oder eine GUI, direkt in den *Bildpuffer (frame buffer)* der Grafikkarte gerendert. Die Hardware sorgt dann dafür, dass die Grafik auf dem Bildschirm erscheint. Das eigentliche Zeichnen der Pixel einer Komponente übernimmt ein GL-*Shader-Programm (shader program)*. Defold enthält für jeden Komponententyp ein Standard-Shader-Programm, das die Pixeldaten unverändert auf den Bildschirm zeichnet. Normalerweise ist genau dieses Verhalten erwünscht: Deine Bilder sollen so auf dem Bildschirm erscheinen, wie sie ursprünglich gestaltet wurden.

Du kannst das Shader-Programm einer Komponente durch eines ersetzen, das die Pixeldaten verändert oder völlig neue Pixelfarben programmgesteuert erzeugt. Im [Shadertoy-Tutorial](/tutorials/shadertoy) erfährst du, wie das geht.

Nehmen wir nun an, du möchtest dein gesamtes Spiel in Schwarz-Weiß rendern. Eine mögliche Lösung besteht darin, das jeweilige Shader-Programm für jeden Komponententyp so zu ändern, dass jeder Shader die Pixelfarben entsättigt. Derzeit enthält Defold 6 integrierte Materialien und 6 Paare aus Vertex- und Fragment-Shader-Programmen. Das ist also mit einigem Aufwand verbunden. Außerdem müssen alle späteren Änderungen oder zusätzlichen Effekte in jedem Shader-Programm vorgenommen werden.

Ein wesentlich flexiblerer Ansatz besteht darin, das Rendering in zwei getrennten Schritten durchzuführen:

![Renderziel](images/grading/render_target.png)

1. Zeichne alle Komponenten wie gewohnt, aber in einen Puffer außerhalb des Bildschirms statt in den üblichen Bildpuffer. Dazu zeichnest du in ein sogenanntes *Renderziel (render target)*.
2. Zeichne ein quadratisches Polygon in den Bildpuffer und verwende die im Renderziel gespeicherten Pixeldaten als Texturquelle für das Polygon. Achte außerdem darauf, dass das quadratische Polygon so gestreckt wird, dass es den gesamten Bildschirm bedeckt.

Mit dieser Methode können wir die entstandenen Bilddaten auslesen und verändern, bevor sie auf dem Bildschirm erscheinen. Indem wir Schritt 2 oben um Shader-Programme ergänzen, können wir leicht Effekte für den gesamten Bildschirm erzielen. Sehen wir uns an, wie wir das in Defold einrichten.

## Einen eigenen Renderer einrichten {#setting-up-a-custom-renderer}

Wir müssen das integrierte Render-Skript ändern und die neue Renderfunktion hinzufügen. Das Standard-Render-Skript ist ein guter Ausgangspunkt. Kopiere es daher zunächst:

1. Kopiere */builtins/render/default.render_script*: Klicke in der Ansicht *Asset* mit der rechten Maustaste auf *default.render_script* und wähle <kbd>Copy</kbd>. Klicke dann mit der rechten Maustaste auf *main* und wähle <kbd>Paste</kbd>. Klicke mit der rechten Maustaste auf die Kopie, wähle <kbd>Rename...</kbd> und gib ihr einen passenden Namen, etwa „grade.render_script“.
2. Erstelle eine neue Renderdatei namens */main/grade.render*, indem du in der Ansicht *Asset* mit der rechten Maustaste auf *main* klickst und <kbd>New ▸ Render</kbd> auswählst.
3. Öffne *grade.render* und setze ihre Eigenschaft *Script* auf „/main/grade.render_script“.

   ![grade.render](images/grading/grade_render.png)

4. Öffne *game.project* und setze *Render* auf „/main/grade.render“.

   ![game.project](images/grading/game_project.png)

Das Spiel ist jetzt so eingerichtet, dass es eine neue Rendering-Pipeline verwendet, die wir ändern können. Um zu prüfen, ob die Engine unsere Kopie des Render-Skripts verwendet, starte dein Spiel, nimm am Render-Skript eine Änderung mit sichtbarem Ergebnis vor und lade das Skript anschließend neu. Du kannst beispielsweise das Zeichnen von Kacheln und Sprites deaktivieren und dann <kbd>⌘ + R</kbd> drücken, um das „defekte“ Render-Skript per Hot Reload in das laufende Spiel zu laden:

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Kommentiere das Zeichnen des Prädikats „tile“ aus, das alle Sprites und Kacheln umfasst. Diese Codezeile findest du ungefähr bei Zeile 33 in der Render-Skript-Datei.

Wenn die Sprites und Kacheln bei diesem einfachen Test verschwinden, weißt du, dass das Spiel dein Render-Skript ausführt. Wenn alles wie erwartet funktioniert, kannst du die Änderung am Render-Skript rückgängig machen.

## In ein Renderziel außerhalb des Bildschirms zeichnen {#drawing-to-an-off-screen-target}

Ändern wir nun das Render-Skript so, dass es in das Renderziel außerhalb des Bildschirms statt in den Bildpuffer zeichnet. Zuerst müssen wir das Renderziel erstellen:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 1)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 1)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Lege die Farbpufferparameter für das Renderziel fest. Wir verwenden die Zielauflösung des Spiels.
2. Erstelle das Renderziel mit den Farbpufferparametern.

Jetzt müssen wir nur noch den ursprünglichen Rendercode mit Aufrufen von `render.set_render_target()` umschließen:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Aktiviere das Renderziel. Von nun an zeichnet jeder Aufruf von `render.draw()` in die Puffer unseres Renderziels außerhalb des Bildschirms.
2. Der gesamte ursprüngliche Zeichencode in `update()` bleibt unverändert, abgesehen vom Ansichtsbereich (viewport), der auf die Auflösung des Renderziels gesetzt wird.
3. An dieser Stelle wurde die gesamte Grafik des Spiels in das Renderziel gezeichnet. Jetzt ist es also an der Zeit, es durch den Wechsel zum Standard-Renderziel zu deaktivieren.

Mehr müssen wir nicht tun. Wenn du das Spiel jetzt ausführst, zeichnet es alles in das Renderziel. Da wir aber nichts mehr in den Bildpuffer zeichnen, sehen wir nur einen schwarzen Bildschirm.

## Etwas, das den Bildschirm füllt {#something-to-fill-the-screen-with}

Um die Pixel im Farbpuffer des Renderziels auf den Bildschirm zu zeichnen, brauchen wir etwas, das wir mit den Pixeldaten texturieren können. Dazu verwenden wir ein flaches, quadratisches 3D-Modell.

1. Öffne *`main.collection`* und erstelle ein neues Spielobjekt (game object) namens „`grade`“.
2. Füge dem Spielobjekt „`grade`“ eine Modellkomponente (Model) hinzu.
3. Setze die Eigenschaft *Mesh* der Modellkomponente auf die Datei *`quad.gltf`*, die du unter `builtins/assets/meshes` findest.

Lass das Spielobjekt unskaliert am Ursprung. Wenn wir das Quad später rendern, projizieren wir es so, dass es den gesamten Bildschirm ausfüllt. Zuerst brauchen wir aber ein Material und Shader-Programme für das Quad:

1. Erstelle ein neues Material namens *`grade.material`*, indem du mit der rechten Maustaste auf *main* in der Ansicht *Asset* klickst und <kbd>New ▸ Material</kbd> auswählst.
2. Erstelle ein Vertex-Shader-Programm namens *`grade.vp`* und ein Fragment-Shader-Programm namens *`grade.fp`*, indem du mit der rechten Maustaste auf *main* in der Ansicht *Asset* klickst und <kbd>New ▸ Vertex program</kbd> sowie <kbd>New ▸ Fragment program</kbd> auswählst.
3. Öffne *grade.material* und setze die Eigenschaften *Vertex program* und *Fragment program* auf die neuen Shader-Programmdateien.
4. Füge eine *Vertex constant* namens „`view_proj`“ vom Typ `CONSTANT_TYPE_VIEWPROJ` hinzu. Das ist die kombinierte Ansichts- und Projektionsmatrix, die im Vertex-Programm für die Vertices des Quads verwendet wird.
5. Füge einen *Sampler* namens „`original`“ hinzu. Mit ihm werden Pixel aus dem Farbpuffer des Renderziels außerhalb des Bildschirms ausgelesen.
6. Füge ein *Tag* namens „`grade`“ hinzu. Wir erstellen im Render-Skript ein neues *Render-Prädikat (render predicate)*, das diesem Tag entspricht, um das Quad zu zeichnen.

   ![grade.material](images/grading/grade_material.png)

7. Öffne *`main.collection`*, wähle die Modellkomponente im Spielobjekt „`grade`“ aus und setze ihre Eigenschaft *Material* auf „`/main/grade.material`“.

   ![Modelleigenschaften](images/grading/model_properties.png)

8. Das Vertex-Shader-Programm kann so bleiben, wie es aus der Grundvorlage erstellt wurde:

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. Im Fragment-Shader-Programm führen wir eine einfache Farbänderung durch, anstatt `gl_FragColor` direkt auf den ausgelesenen Farbwert zu setzen. Damit wollen wir vor allem sicherstellen, dass bisher alles wie erwartet funktioniert:

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturate the color sampled from the original texture
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Jetzt ist das Quad-Modell mit seinem Material und seinen Shadern eingerichtet. Wir müssen es nur noch in den Bildpuffer des Bildschirms zeichnen.

## Mit dem Puffer außerhalb des Bildschirms texturieren {#texturing-with-the-off-screen-buffer}

Wir müssen dem Render-Skript ein Render-Prädikat hinzufügen, damit wir das Quad-Modell zeichnen können. Öffne *`grade.render_script`* und bearbeite die Funktion `init()`:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Füge ein neues Prädikat hinzu, das dem Tag „grade“ entspricht, das wir in *`grade.material`* festgelegt haben.

Nachdem der Farbpuffer des Renderziels in `update()` gefüllt wurde, richten wir eine Ansicht und eine Projektion ein, mit denen das Quad-Modell den gesamten Bildschirm ausfüllt. Anschließend verwenden wir den Farbpuffer des Renderziels als Textur des Quads:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Leere den Bildpuffer. Beachte, dass der vorherige Aufruf von `render.clear()` das Renderziel beeinflusst, nicht den Bildpuffer des Bildschirms.
2. Passe den Ansichtsbereich an die Fenstergröße an.
3. Setze die Ansicht auf die Einheitsmatrix. Das bedeutet, dass die Kamera am Ursprung liegt und gerade entlang der Z-Achse blickt. Setze auch die Projektion auf die Einheitsmatrix, wodurch das Quad flach über den gesamten Bildschirm projiziert wird.
4. Setze den Texturplatz 0 auf den Farbpuffer des Renderziels. In unserem *`grade.material`* befindet sich der Sampler „original“ auf Platz 0, daher liest der Fragment-Shader aus dem Renderziel.
5. Zeichne das erstellte Prädikat, das auf alle Materialien mit dem Tag „grade“ passt. Das Quad-Modell verwendet *`grade.material`*, das dieses Tag setzt, daher wird das Quad gezeichnet.
6. Deaktiviere nach dem Zeichnen den Texturplatz 0, da wir mit dem Zeichnen über diesen Platz fertig sind.

Starten wir nun das Spiel und sehen uns das Ergebnis an:

![Entsättigtes Spiel](images/grading/desaturated_game.png)

## Farbkorrektur {#color-grading}

Farben werden durch drei Komponentenwerte ausgedrückt, wobei jede Komponente den Anteil von Rot, Grün oder Blau in einer Farbe angibt. Das gesamte Farbspektrum von Schwarz über Rot, Grün, Blau, Gelb und Pink bis Weiß lässt sich in einem Würfel darstellen:

![Farbwürfel](images/grading/color_cube.png)

Jede Farbe, die auf dem Bildschirm dargestellt werden kann, ist in diesem Farbwürfel enthalten. Die Grundidee der Farbkorrektur besteht darin, einen solchen Farbwürfel mit veränderten Farben als dreidimensionale *Nachschlagetabelle (lookup table)* zu verwenden.

Für jedes Pixel:

1. Ermittle die Position seiner Farbe im Farbwürfel anhand der Rot-, Grün- und Blauwerte.
2. *Lies aus*, welche Farbe der farbkorrigierte Würfel an dieser Position gespeichert hat.
3. Zeichne das Pixel in der ausgelesenen Farbe statt in der ursprünglichen Farbe.

Das können wir in unserem Fragment-Shader tun:

1. Lies den Farbwert jedes Pixels im Puffer außerhalb des Bildschirms aus.
2. Schlage die Farbposition des ausgelesenen Pixels in einem farbkorrigierten Farbwürfel nach.
3. Setze die Ausgabefarbe des Fragments auf den nachgeschlagenen Wert.

![Farbkorrektur mit Renderziel](images/grading/render_target_grading.png)

## Die Nachschlagetabelle darstellen {#representing-the-lookup-table}

Open GL ES 2.0 unterstützt keine 3D-Texturen, daher müssen wir einen anderen Weg finden, den 3D-Farbwürfel darzustellen. Ein gängiges Verfahren besteht darin, den Würfel entlang der Z-Achse (Blau) in Scheiben zu schneiden und diese in einem zweidimensionalen Raster nebeneinander anzuordnen. Jede der 16 Scheiben enthält ein Raster aus 16 × 16 Pixeln. Wir speichern es in einer Textur, aus der wir im Fragment-Shader mit einem Sampler lesen können:

![Nachschlagetextur](images/grading/lut.png)

Die entstandene Textur enthält 16 Zellen, eine für jede Intensität von Blau. Innerhalb jeder Zelle liegen 16 Rottöne entlang der X-Achse und 16 Grüntöne entlang der Y-Achse. Die Textur stellt den gesamten RGB-Farbraum mit 16 Millionen Farben in nur 4096 Farben dar, also mit gerade einmal 4 Bit Farbtiefe. Nach den meisten Maßstäben ist das dürftig, aber dank einer Funktion der GL-Grafikhardware können wir wieder eine sehr hohe Farbgenauigkeit erreichen. Sehen wir uns an, wie das geht.

## Farben nachschlagen {#looking-up-colors}

Um eine Farbe nachzuschlagen, prüfen wir die Blaukomponente und ermitteln, aus welcher Zelle die Rot- und Grünwerte stammen sollen. Die Formel, mit der wir die Zelle mit dem passenden Rot-Grün-Farbsatz finden, ist einfach:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Hier ist `B` der Wert der Blaukomponente zwischen 0 und 1 und `N` die Gesamtzahl der Zellen. In unserem Fall liegt die Zellnummer im Bereich `0`--`15`, wobei Zelle `0` alle Farben mit der Blaukomponente `0` und Zelle `15` alle Farben mit der Blaukomponente `1` enthält.

Der RGB-Wert `(0.63, 0.83, 0.4)` liegt beispielsweise in der Zelle, die alle Farben mit einem Blauwert von `0.4` enthält, also in Zelle 6. Mit diesem Wissen lassen sich die endgültigen Texturkoordinaten anhand der Grün- und Rotwerte leicht ermitteln:

![Nachschlagetabelle](images/grading/lut_lookup.png)

Beachte, dass wir die Rot- und Grünwerte `(0, 0)` als Position in der *Mitte* des Pixels unten links und die Werte `(1.0, 1.0)` als Position in der *Mitte* des Pixels oben rechts behandeln müssen.

::: sidenote
Wir lesen von der Mitte des Pixels unten links bis zur Mitte des Pixels oben rechts, weil keine Pixel außerhalb der aktuellen Zelle den ausgelesenen Wert beeinflussen sollen. Siehe dazu die Erklärung zur Filterung weiter unten.
:::

Wenn wir die Textur an diesen bestimmten Koordinaten abtasten, stellen wir fest, dass wir genau zwischen 4 Pixeln landen. Welchen Farbwert wird GL uns also für diesen Punkt liefern?

![Filterung der Nachschlagetabelle](images/grading/lut_filtering.png)

Die Antwort hängt davon ab, wie wir die *Filterung* des Samplers im Material festgelegt haben.

- Wenn die Sampler-Filterung auf `NEAREST` gesetzt ist, gibt GL den Farbwert des nächstgelegenen Pixels zurück; dabei wird der Positionswert abgerundet. Im obigen Fall gibt GL den Farbwert an der Position `(0.60, 0.80)` zurück. Für unsere Nachschlagetextur mit 4 Bit bedeutet das, dass wir die Farbwerte auf insgesamt nur 4096 Farben quantisieren.

- Wenn die Sampler-Filterung auf `LINEAR` gesetzt ist, gibt GL den *interpolierten* Farbwert zurück. GL mischt eine Farbe anhand der Abstände zu den Pixeln um die Abtastposition. Im obigen Fall gibt GL eine Farbe zurück, die sich zu jeweils 25 % aus den 4 Pixeln um den Abtastpunkt zusammensetzt.

Mit linearer Filterung beseitigen wir also die Farbquantisierung und erzielen mit einer recht kleinen Nachschlagetabelle eine sehr gute Farbgenauigkeit.

## Das Nachschlagen implementieren {#implementing-the-lookup}

Implementieren wir das Nachschlagen in der Textur im Fragment-Shader:

1. Öffne *`grade.material`*.
2. Füge einen zweiten Sampler namens „`lut`“ hinzu, kurz für lookup table, also Nachschlagetabelle.
3. Setze die Eigenschaft *`Filter min`* auf `FILTER_MODE_MIN_LINEAR` und die Eigenschaft *`Filter mag`* auf `FILTER_MODE_MAG_LINEAR`.

    ![Sampler der Nachschlagetabelle](images/grading/material_lut_sampler.png)

4. Lade die folgende Textur der Nachschlagetabelle (*`lut16.png`*) herunter und füge sie deinem Projekt hinzu.

    ![Nachschlagetabelle mit 16 Farben](images/grading/lut16.png)

5. Öffne *`main.collection`* und setze die Textureigenschaft *`lut`* auf die heruntergeladene Nachschlagetextur.

    ![Nachschlagetabelle des Quad-Modells](images/grading/quad_lut.png)

6. Öffne schließlich *`grade.fp`*, damit wir die Unterstützung für das Nachschlagen von Farben hinzufügen können:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Deklariere den Sampler `lut`.
    2. Konstanten für den maximalen Farbwert (15, da wir bei 0 beginnen), die Anzahl der Farben pro Kanal sowie Breite und Höhe der Nachschlagetextur.
    3. Lies eine Pixelfarbe (namens `px`) aus der ursprünglichen Textur aus, also dem Farbpuffer des Renderziels außerhalb des Bildschirms.
    4. Berechne anhand des Blaukanalwerts von `px`, aus welcher Zelle die Farbe gelesen werden soll.
    5. Berechne Versätze um ein halbes Pixel, damit wir aus den Pixelmitten lesen.
    6. Berechne den X- und Y-Versatz auf der Textur anhand der Rot- und Grünwerte von `px`.
    7. Berechne die endgültige Abtastposition auf der Nachschlagetextur.
    8. Lies die resultierende Farbe aus der Nachschlagetextur aus.
    9. Setze die Farbe auf der Textur des Quads auf die resultierende Farbe.

Derzeit gibt die Textur der Nachschlagetabelle lediglich dieselben Farbwerte zurück, die wir nachschlagen. Das bedeutet, dass das Spiel mit seiner ursprünglichen Farbgebung gerendert werden sollte:

![Spielwelt mit ursprünglicher Farbgebung](images/grading/world_original.png)

Bisher sieht es so aus, als hätten wir alles richtig gemacht. Unter der Oberfläche lauert jedoch ein Problem. Sieh dir an, was passiert, wenn wir ein Sprite mit einer Testtextur mit Farbverläufen hinzufügen:

![Streifenbildung im Blauverlauf](images/grading/blue_banding.png)

Der blaue Farbverlauf zeigt eine wirklich unschöne Streifenbildung. Woran liegt das?

## Den Blaukanal interpolieren {#interpolating-the-blue-channel}

Die Streifenbildung im Blaukanal entsteht, weil GL beim Auslesen der Farbe aus der Textur keine Interpolation des Blaukanals durchführen kann. Wir wählen anhand des Blauwerts vorab eine bestimmte Zelle zum Auslesen aus, und dabei bleibt es. Wenn der Blaukanal beispielsweise einen beliebigen Wert im Bereich `0.400`--`0.466` enthält, spielt der genaue Wert keine Rolle: Wir lesen die endgültige Farbe immer aus Zelle 6 aus, in der der Blaukanal auf `0.400` gesetzt ist.

Um eine bessere Auflösung des Blaukanals zu erhalten, können wir die Interpolation selbst implementieren. Liegt der Blauwert zwischen den Werten zweier benachbarter Zellen, können wir beide Zellen auslesen und anschließend die Farben mischen. Wenn der Blauwert beispielsweise `0.420` ist, sollten wir Zelle 6 *und* Zelle 7 auslesen und anschließend die Farben mischen.

Wir sollten also aus zwei Zellen lesen:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

und:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Anschließend lesen wir Farbwerte aus beiden Zellen aus und interpolieren die Farben linear nach folgender Formel:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Hier ist `color`~low~ die aus der niedrigeren (linken) Zelle ausgelesene Farbe und `color`~high~ die aus der höheren (rechten) Zelle ausgelesene Farbe. Die GLSL-Funktion `mix()` führt diese lineare Interpolation für uns aus.

Der Wert `C~frac~` oben ist der Nachkommaanteil des Blaukanalwerts, nachdem dieser auf den Farbbereich `0`--`15` skaliert wurde:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Auch hierfür gibt es eine GLSL-Funktion, die den Nachkommaanteil eines Werts liefert. Sie heißt `frac()`. Die endgültige Implementierung im Fragment-Shader (*`grade.fp`*) ist recht unkompliziert:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Berechne die beiden benachbarten Zellen, aus denen gelesen werden soll.
2. Berechne zwei getrennte Nachschlagepositionen, eine für jede Zelle.
3. Lies die beiden Farben an den Positionen in den Zellen aus.
3. Mische die Farben linear entsprechend dem Nachkommaanteil von `cell`, dem skalierten Blauwert.

Wenn wir das Spiel erneut mit der Testtextur ausführen, erhalten wir nun deutlich bessere Ergebnisse. Die Streifenbildung im Blaukanal ist verschwunden:

![Blauverlauf ohne Streifenbildung](images/grading/blue_no_banding.png)

## Die Nachschlagetextur farbkorrigieren {#grading-the-lookup-texture}

Gut, das war viel Arbeit, um etwas zu zeichnen, das genauso aussieht wie die ursprüngliche Spielwelt. Aber dieser Aufbau ermöglicht uns etwas wirklich Tolles. Jetzt wird es spannend!

1. Erstelle eine Bildschirmaufnahme des Spiels in seiner unveränderten Form.
2. Öffne die Bildschirmaufnahme in deinem bevorzugten Bildbearbeitungsprogramm.
3. Wende beliebig viele Farbanpassungen an, etwa Helligkeit, Kontrast, Farbkurven, Weißabgleich, Belichtung und weitere.

![Spielwelt in Affinity](images/grading/world_graded_affinity.png)

4. Wende dieselben Farbanpassungen auf die Texturdatei der Nachschlagetabelle (*`lut16.png`*) an.
5. Speichere die farblich angepasste Texturdatei der Nachschlagetabelle.
6. Ersetze die in deinem Defold-Projekt verwendete Textur *`lut16.png`* durch die farblich angepasste Version.
7. Starte das Spiel!

![Farbkorrigierte Spielwelt](images/grading/world_graded.png)

Juhu!
