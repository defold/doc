---
title: Die Rendering-Pipeline in Defold
brief: Dieses Handbuch erklärt, wie Defolds Rendering-Pipeline funktioniert und wie du sie programmieren kannst.
---

# Rendering {#render}

Jedes Objekt, das die Engine auf dem Bildschirm anzeigt – Sprites, Modelle, Kacheln, Partikel oder GUI-Knoten (GUI nodes) –, wird von einem Renderer gezeichnet. Das Herzstück des Renderers ist ein Render-Skript (render script), das die Rendering-Pipeline steuert. Standardmäßig wird jedes 2D-Objekt mit der richtigen Bitmap, der angegebenen Farbmischung und in der richtigen Z-Tiefe gezeichnet---du musst dich also möglicherweise über die Reihenfolge und einfache Farbmischung hinaus nie mit dem Rendering befassen. Für die meisten 2D-Spiele funktioniert die Standard-Pipeline gut, aber dein Spiel kann besondere Anforderungen haben. In diesem Fall kannst du mit Defold eine maßgeschneiderte Rendering-Pipeline schreiben.

### Rendering-Pipeline - Was, wann und wo? {#render-pipeline-what-when-and-where}

Die Rendering-Pipeline steuert, was gerendert wird, wann es gerendert wird und auch wo es gerendert wird. Was gerendert wird, bestimmen [Render-Prädikate](#render-predicates) (render predicates). Wann ein Prädikat gerendert wird, wird im [Render-Skript](#the-render-script) festgelegt, und wo ein Prädikat gerendert wird, bestimmen [Ansicht und Projektion](#default-view-projection). Die Rendering-Pipeline kann außerdem Grafik, die von einem Render-Prädikat gezeichnet wird und außerhalb eines festgelegten Begrenzungsquaders oder Sichtvolumens liegt, aussondern. Dieser Vorgang heißt Aussondern von Geometrie außerhalb des Sichtvolumens (Frustum Culling).


## Das Standard-Rendering {#the-default-render}

Die Renderdatei enthält eine Referenz auf das aktuelle Render-Skript sowie benutzerdefinierte Materialien, die im Render-Skript verfügbar sein sollen (zur Verwendung mit [`render.enable_material()`](/ref/render/#render.enable_material))

Das Herzstück der Rendering-Pipeline ist das _Render-Skript_. Es ist ein Lua-Skript mit den Funktionen `init()`, `update()` und `on_message()` und dient hauptsächlich dazu, mit der zugrunde liegenden Grafik-API zu interagieren. Das Render-Skript nimmt im Lebenszyklus deines Spiels einen besonderen Platz ein. Einzelheiten findest du in der [Dokumentation zum Anwendungslebenszyklus](/manuals/application-lifecycle).

Im Ordner „Builtins“ deiner Projekte findest du die standardmäßige Render-Ressource ("default.render") und das standardmäßige Render-Skript ("default.render_script").

![Integriertes Rendering](images/render/builtin.png)

So richtest du einen benutzerdefinierten Renderer ein:

1. Kopiere die Dateien "default.render" und "default.render_script" an eine Stelle in deiner Projekthierarchie. Du kannst natürlich ein Render-Skript von Grund auf neu erstellen. Es empfiehlt sich aber, mit einer Kopie des Standardskripts zu beginnen, besonders wenn du mit Defold und/oder Grafikprogrammierung noch nicht vertraut bist.

2. Bearbeite deine Kopie der Datei "default.render" und ändere die Eigenschaft *Script* so, dass sie auf deine Kopie des Render-Skripts verweist.

3. Ändere die Eigenschaft *Render* (unter *bootstrap*) in der Einstellungsdatei *game.project* so, dass sie auf deine Kopie der Datei "default.render" verweist.


## Render-Prädikate {#render-predicates}

Um die Zeichenreihenfolge von Objekten steuern zu können, erstellst du Render-_Prädikate_. Ein Prädikat legt anhand einer Auswahl von Material-_Tags_ fest, was gezeichnet werden soll.

Jedem Objekt, das auf den Bildschirm gezeichnet wird, ist ein Material zugewiesen. Es steuert, wie das Objekt auf den Bildschirm gezeichnet werden soll. Im Material gibst du ein oder mehrere _Tags_ an, die mit dem Material verknüpft werden sollen.

In deinem Render-Skript kannst du dann ein *Render-Prädikat* erstellen und angeben, welche Tags zu diesem Prädikat gehören sollen. Wenn du die Engine anweist, das Prädikat zu zeichnen, wird jedes Objekt gezeichnet, dessen Material alle für das Prädikat angegebenen Tags enthält.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


Eine ausführliche Beschreibung der Funktionsweise von Materialien findest du in der [Materialdokumentation](/manuals/material).


## Standardansicht und -projektion {#default-view-projection}

Das standardmäßige Render-Skript ist so konfiguriert, dass es eine für 2D-Spiele geeignete orthografische Projektion verwendet. Es bietet drei verschiedene orthografische Projektionen: `Stretch` (Standard), `Fixed Fit` und `Fixed`. Als Alternative zu den orthografischen Projektionen im standardmäßigen Render-Skript kannst du auch die Projektionsmatrix verwenden, die eine Kamerakomponente (camera component) bereitstellt.

### Gestreckte Projektion {#stretch-projection}

Die gestreckte Projektion zeichnet immer einen Bereich deines Spiels, der den in *game.project* festgelegten Abmessungen entspricht, auch wenn die Fenstergröße geändert wird. Ändert sich das Seitenverhältnis, werden die Spielinhalte entweder vertikal oder horizontal gestreckt:

![Gestreckte Projektion](images/render/stretch_projection.png)

*Gestreckte Projektion mit ursprünglicher Fenstergröße*

![Gestreckte Projektion nach Größenänderung](images/render/stretch_projection_resized.png)

*Gestreckte Projektion mit horizontal gestrecktem Fenster*

Die gestreckte Projektion ist die Standardprojektion. Wenn du zu einer anderen Projektion gewechselt hast und wieder zurückwechseln möchtest, sendest du dazu eine Nachricht an das Render-Skript:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Fest eingepasste Projektion {#fixed-fit-projection}

Wie die gestreckte Projektion zeigt die fest eingepasste Projektion immer einen Spielbereich, der den in *game.project* festgelegten Abmessungen entspricht. Wenn jedoch die Fenstergröße und damit das Seitenverhältnis geändert werden, behalten die Spielinhalte ihr ursprüngliches Seitenverhältnis bei, und vertikal oder horizontal werden zusätzliche Spielinhalte angezeigt:

![Fest eingepasste Projektion](images/render/fixed_fit_projection.png)

*Fest eingepasste Projektion mit ursprünglicher Fenstergröße*

![Fest eingepasste Projektion nach Größenänderung](images/render/fixed_fit_projection_resized.png)

*Fest eingepasste Projektion mit horizontal gestrecktem Fenster*

![Fest eingepasste Projektion bei kleinerem Fenster](images/render/fixed_fit_projection_resized_smaller.png)

*Fest eingepasste Projektion mit einem auf 50 % der ursprünglichen Größe verkleinerten Fenster*

Du aktivierst die fest eingepasste Projektion, indem du eine Nachricht an das Render-Skript sendest:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Feste Projektion {#fixed-projection}

Die feste Projektion behält das ursprüngliche Seitenverhältnis bei und rendert deine Spielinhalte mit einer festen Zoomstufe. Wenn die Zoomstufe auf einen anderen Wert als 100 % eingestellt ist, zeigt sie also mehr oder weniger als den Spielbereich, der durch die Abmessungen in *game.project* definiert ist:

![Feste Projektion](images/render/fixed_projection_zoom_2_0.png)

*Feste Projektion mit Zoomstufe 2*

![Feste Projektion](images/render/fixed_projection_zoom_0_5.png)

*Feste Projektion mit Zoomstufe 0,5*

![Feste Projektion](images/render/fixed_projection_zoom_2_0_resized.png)

*Feste Projektion mit Zoomstufe 2 und einem auf 50 % der ursprünglichen Größe verkleinerten Fenster*

Du aktivierst die feste Projektion, indem du eine Nachricht an das Render-Skript sendest:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Kameraprojektion {#camera-projection}

Wenn du das standardmäßige Render-Skript verwendest und im Projekt aktivierte [Kamerakomponenten](/manuals/camera) vorhanden sind, haben diese Vorrang vor allen anderen im Render-Skript eingestellten Ansichten und Projektionen. Mehr zur Arbeit mit Kamerakomponenten in Render-Skripten findest du in der [Kameradokumentation](/manuals/camera).

Orthografische Kameras unterstützen einen `Orthographic Mode`, der steuert, wie sich die Kamera an das Fenster anpasst:
- `Fixed` verwendet den Wert `Orthographic Zoom` der Kamera.
- `Auto Fit` (einpassen) hält den gesamten Entwurfsbereich sichtbar.
- `Auto Cover` (ausfüllen) füllt das Fenster aus und kann Inhalte beschneiden.

Du kannst die Modi im Editor oder zur Laufzeit über die Kamera-API wechseln:

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Geometrie außerhalb des Sichtvolumens aussondern {#frustum-culling}

Mit der Render-API in Defold kannst du Geometrie außerhalb des Sichtvolumens aussondern. Wenn dieses Aussondern aktiviert ist, wird jede Grafik ignoriert, die außerhalb eines festgelegten Begrenzungsquaders oder Sichtvolumens liegt. In einer großen Spielwelt, von der jeweils nur ein Teil sichtbar ist, kann das Aussondern von Geometrie außerhalb des Sichtvolumens die Datenmenge, die zum Rendern an die GPU gesendet werden muss, erheblich verringern. Dadurch steigt die Leistung und auf Mobilgeräten wird der Akku geschont. Üblicherweise werden die Ansicht und die Projektion der Kamera verwendet, um den Begrenzungsquader zu erstellen. Das standardmäßige Render-Skript verwendet die Ansicht und die Projektion (von der Kamera), um ein Sichtvolumen zu berechnen.

Aktiviere das Aussondern von Geometrie außerhalb des Sichtvolumens für einen Zeichenaufruf (draw call), indem du eine kombinierte Ansichts- und Projektionsmatrix in der Option `frustum` an `render.draw()` übergibst:

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Beim Rendern mit einer Kamerakomponente kann `render.set_camera()` die kombinierte Ansichts- und Projektionsmatrix der Kamera automatisch für nachfolgende Zeichenaufrufe verwenden:

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

Bei beiden Methoden werden Partikeleffekt-Emitter anhand ihrer Begrenzungen ausgesondert.

Das Aussondern von Geometrie außerhalb des Sichtvolumens ist in der Engine für jeden Komponententyp einzeln implementiert. Aktueller Stand:

| Komponente  | Unterstützt |
|-------------|-----------|
| Sprite      | JA        |
| Modell      | JA        |
| Mesh        | JA (1)    |
| Beschriftung | JA       |
| Spine       | JA        |
| Partikeleffekt | JA     |
| Kachelkarte (tile map) | JA |
| Rive        | NEIN      |

1 = Der Begrenzungsquader des Meshes muss von dir festgelegt werden. [Mehr erfahren](/manuals/mesh/#frustum-culling).


::: sidenote
Ab Defold 1.13.0 verwenden die Primitive von Komponenten (components) eine Vertex-Reihenfolge gegen den Uhrzeigersinn, wobei die Normale des Primitivs zur Kamera zeigt. Sprites, GUI-Knoten, Kachelkarten (Kachelraster) und Partikeleffekte verwenden dieselbe Reihenfolge wie andere Komponententypen. Deshalb können für alle Komponenten dieselben Einstellungen zum Aussondern von Flächen verwendet werden.

Dies kann Projekte betreffen, die das Aussondern von Flächen für andere Komponenten als Modelle einstellen. Wenn eine Komponente unerwartet ausgesondert wird, stelle sicher, dass mit `render.set_cull_face(graphics.FACE_TYPE_BACK)` die Rückseiten ausgewählt sind, oder entferne den Aufruf von `render.set_cull_face()`, um den Standardmodus `graphics.FACE_TYPE_BACK` zu verwenden.
:::

## Koordinatensysteme {#coordinate-systems}

Beim Rendern von Komponenten ist üblicherweise auch davon die Rede, in welchem Koordinatensystem sie gerendert werden. In den meisten Spielen werden einige Komponenten im Weltkoordinatensystem und andere im Bildschirmkoordinatensystem gezeichnet.

GUI-Komponenten und ihre Knoten werden normalerweise im Bildschirmkoordinatensystem gezeichnet. Die untere linke Ecke des Bildschirms hat dabei die Koordinate (0,0), die obere rechte Ecke die Koordinate (Bildschirmbreite, Bildschirmhöhe). Das Bildschirmkoordinatensystem wird niemals durch eine Kamera versetzt oder auf andere Weise verschoben. Dadurch werden die GUI-Knoten unabhängig davon, wie die Welt gerendert wird, immer auf dem Bildschirm gezeichnet.

Sprites, Kachelkarten und andere Komponenten von Spielobjekten (game objects) in deiner Spielwelt werden normalerweise im Weltkoordinatensystem gezeichnet. Wenn du dein Render-Skript nicht änderst und keine Kamerakomponente verwendest, um die Ansicht und Projektion zu ändern, entspricht dieses Koordinatensystem dem Bildschirmkoordinatensystem. Sobald du jedoch eine Kamera hinzufügst und sie bewegst oder die Ansicht und Projektion änderst, weichen die beiden Koordinatensysteme voneinander ab. Wenn sich die Kamera bewegt, wird die untere linke Ecke des Bildschirms gegenüber (0, 0) versetzt, sodass andere Teile der Welt gerendert werden. Wenn sich die Projektion ändert, werden die Koordinaten sowohl verschoben (also gegenüber 0, 0 versetzt) als auch durch einen Skalierungsfaktor verändert.


## Das Render-Skript {#the-render-script}

Im Folgenden siehst du den Code für ein benutzerdefiniertes Render-Skript, das eine leicht abgewandelte Version des integrierten Skripts ist.

init()
: Die Funktion `init()` richtet die Prädikate, die Ansicht und die Löschfarbe ein. Diese Variablen werden beim eigentlichen Rendern verwendet.

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: Die Funktion `update()` wird einmal pro Frame aufgerufen. Ihre Aufgabe ist es, das eigentliche Zeichnen durch Aufrufe der zugrunde liegenden OpenGL-ES-APIs (OpenGL Embedded Systems API) auszuführen. Um genau zu verstehen, was in der Funktion `update()` passiert, musst du die Funktionsweise von OpenGL verstehen. Es gibt viele hilfreiche Informationsquellen zu OpenGL ES. Die offizielle Website ist ein guter Ausgangspunkt. Du findest sie unter https://www.khronos.org/opengles/

  Dieses Beispiel enthält die zum Zeichnen von 3D-Modellen notwendige Einrichtung. Die Funktion `init()` hat ein Prädikat `self.predicates.model` definiert. An anderer Stelle wurde ein Material mit dem Tag "model" erstellt. Außerdem gibt es einige Modellkomponenten, die dieses Material verwenden:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Bisher ist dies ein einfaches und geradliniges Render-Skript. Es zeichnet in jedem Frame auf dieselbe Weise. Manchmal ist es jedoch wünschenswert, einen Zustand im Render-Skript zu speichern und abhängig davon unterschiedliche Operationen auszuführen. Es kann auch wünschenswert sein, aus anderen Teilen des Spielcodes mit dem Render-Skript zu kommunizieren.

on_message()
: Ein Render-Skript kann eine Funktion `on_message()` definieren und Nachrichten aus anderen Teilen deines Spiels oder deiner Anwendung empfangen. Ein häufiger Fall, in dem eine externe Komponente Informationen an das Render-Skript sendet, ist die _Kamera_. Eine Kamerakomponente, die den Kamerafokus erhalten hat, sendet in jedem Frame automatisch ihre Ansicht und Projektion an das Render-Skript. Diese Nachricht heißt `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Jedes Skript oder GUI-Skript kann jedoch über den speziellen Socket `@render` Nachrichten an das Render-Skript senden:

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Render-Ressourcen {#render-resources}
Um bestimmte Engine-Ressourcen an das Render-Skript zu übergeben, kannst du sie der Tabelle `Render Resources` in der dem Projekt zugewiesenen `.render`-Datei hinzufügen:

![Render-Ressourcen](images/render/render_resources.png)

So verwendest du diese Ressourcen in einem Render-Skript:

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Defold unterstützt derzeit nur `Materials` und `Render Targets` als referenzierte Render-Ressourcen. Im Laufe der Zeit wird dieses System jedoch weitere Ressourcentypen unterstützen.
:::

### Renderziele mit Multisampling {#multisampled-render-targets}

Renderziele (render targets) unterstützen Multisample-Kantenglättung (MSAA). Sie glättet Geometriekanten in einem Renderdurchlauf außerhalb der Bildschirmausgabe. Die Anzahl der Samples des Renderziels ist unabhängig von [Display ▸ Samples](/manuals/project-settings/#samples), das die Kantenglättung für das Fenster steuert.

Stelle für eine `.render_target`-Ressource im Editor **Sample Count** auf `1`, `2`, `4`, `8` oder `16` ein. Ein Wert von `1` deaktiviert Multisampling. Füge die Ressource in deiner `.render`-Datei zur Tabelle **Render Resources** hinzu und verwende ihren zugewiesenen Namen mit `render.set_render_target()`, wie im obigen Beispiel.

Alternativ kannst du in der Funktion `init()` deines Render-Skripts ein Renderziel erstellen. Füge `sample_count` neben den angehängten Puffern in die äußere Parametertabelle ein:

```lua
self.offscreen = render.render_target({
    sample_count = 4,
    [graphics.BUFFER_TYPE_COLOR0_BIT] = {
        format = graphics.TEXTURE_FORMAT_RGBA,
        width = 1024,
        height = 1024,
        min_filter = graphics.TEXTURE_FILTER_LINEAR,
        mag_filter = graphics.TEXTURE_FILTER_LINEAR,
        u_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
        v_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
    },
})
self.scene_predicate = render.predicate({"scene"})
self.present_predicate = render.predicate({"present"})
```

Dieses Beispiel verwendet ein Renderziel, das nur Farbpuffer enthält. Alle angehängten Farb-, Tiefen- und Stencil-Puffer eines Renderziels teilen sich dessen Sample-Anzahl. Füge einen Tiefenpuffer hinzu und aktiviere den üblichen Tiefentest-Zustand, wenn der Durchlauf einen Tiefentest erfordert.

Gib für den folgenden Ausschnitt aus `update()` den Materialien der Szene das Tag `scene` und dem Material eines bildschirmfüllenden Vierecks das Tag `present`. Das Material des Vierecks muss Textureinheit `0` abtasten. Lege für jeden Durchlauf die passende Ansicht und Projektion fest:

```lua
render.set_render_target(self.offscreen)
render.set_viewport(0, 0, 1024, 1024)
render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = vmath.vector4(0, 0, 0, 1)})
-- Set the scene view and projection here.
render.draw(self.scene_predicate)

render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.set_viewport(0, 0, render.get_window_width(), render.get_window_height())
-- Set the full-screen quad view and projection here.
render.enable_texture(0, self.offscreen, graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.present_predicate)
render.disable_texture(0)
```

Der Wechsel zu einem anderen Renderziel beendet den Durchlauf und führt die Multisamples seiner angehängten Farbpuffer automatisch zusammen. `render.enable_texture()` bindet die daraus entstandene Farbtextur, sodass das Viereck einen gewöhnlichen Textur-Sampler verwendet. Ein separater Befehl zum Zusammenführen ist nicht erforderlich.

Die angeforderte Sample-Anzahl ist standardmäßig `1` und muss eine positive ganze Zahl sein. Grafik-Backends reduzieren nicht unterstützte Anforderungen auf eine unterstützte Anzahl, die eine Zweierpotenz ist. Falls nötig, fallen sie auf `1` zurück und protokollieren eine Warnung, wenn sich die Anzahl ändert. Höhere Sample-Anzahlen erhöhen den Speicherbedarf der angehängten Puffer.

Wenn du eine Renderziel-Ressource verwendest, prüfe ihre tatsächliche Sample-Anzahl aus einem Spielobjekt-Skript `.script` mit `resource.get_render_target_info()`. Zum Beispiel, nachdem du `/render/offscreen.render_target` zu **Render Resources** hinzugefügt hast:

```lua
function init(self)
    local info = resource.get_render_target_info("/render/offscreen.render_targetc")
    print("Render target sample count:", info.sample_count)
end
```

Verwende diese tatsächliche Anzahl, wenn du die Unterstützung auf einem Gerät prüfst, anstatt anzunehmen, dass die angeforderte Anzahl verfügbar war. Die vollständigen Parameter- und Ergebnistabellen findest du unter [`render.render_target()`](/ref/beta/render/#render.render_target:parameters) und [`resource.get_render_target_info()`](/ref/beta/resource/#resource.get_render_target_info:path).

## Textur-Handles {#texture-handles}

Texturen werden in Defold intern durch ein Handle dargestellt. Dies entspricht im Wesentlichen einer Zahl, die ein Texturobjekt überall in der Engine eindeutig identifizieren soll. Du kannst also die Spielobjektwelt mit der Rendering-Welt verbinden, indem du diese Handles zwischen dem Render-System und einem Spielobjekt-Skript übergibst. Beispielsweise kann ein Skript, das einem Spielobjekt zugewiesen ist, eine dynamische Textur erstellen und sie an den Renderer senden, damit sie als globale Textur in einem Zeichenbefehl verwendet wird.

In einer `.script`-Datei:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

In einer `.render_script`-Datei:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
Derzeit lässt sich nicht ändern, auf welche Textur eine Ressource verweist. Solche direkten Handles kannst du nur im Render-Skript verwenden.
:::

## Unterstützte Grafik-APIs {#supported-graphics-apis}
Die Render-Skript-API von Defold übersetzt Renderoperationen in die folgenden Grafik-APIs:

:[Graphics API](../shared/graphics-api.md)


## Systemnachrichten {#system-messages}

`"set_view_projection"`
: Diese Nachricht wird von Kamerakomponenten gesendet, die den Kamerafokus erhalten haben.

`"window_resized"`
: Die Engine sendet diese Nachricht, wenn sich die Fenstergröße ändert. Du kannst auf diese Nachricht reagieren, um das Rendering bei einer Änderung der Größe des Zielfensters anzupassen. Auf Desktopgeräten bedeutet dies, dass die Größe des eigentlichen Spielfensters geändert wurde. Auf Mobilgeräten wird diese Nachricht bei jeder Änderung der Ausrichtung gesendet.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: Zeichnet eine Debug-Linie. Verwende diese Nachricht, um `ray_casts`, Vektoren und mehr zu visualisieren. Die Linien werden mit dem Aufruf `render.draw_debug3d()` gezeichnet.

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Zeichnet Debug-Text. Verwende diese Nachricht, um Debug-Informationen auszugeben. Der Text wird mit der integrierten Schriftart `always_on_top.font` gezeichnet. Die Systemschrift hat ein Material mit dem Tag `debug_text` und wird im standardmäßigen Render-Skript zusammen mit anderem Text gerendert.

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

Der visuelle Profiler, den du über die Nachricht `"toggle_profile"` an den Socket `@system` aufrufen kannst, ist nicht Teil des per Skript steuerbaren Renderers. Er wird getrennt von deinem Render-Skript gezeichnet.


## Zeichenaufrufe und Bündelung von Zeichenoperationen {#draw-calls-and-batching}

Ein Zeichenaufruf bezeichnet den Vorgang, die GPU so einzurichten, dass sie ein Objekt mit einer Textur und einem Material sowie optionalen zusätzlichen Einstellungen auf den Bildschirm zeichnet. Dieser Vorgang ist normalerweise ressourcenintensiv, daher wird empfohlen, die Anzahl der Zeichenaufrufe möglichst gering zu halten. Mit dem [integrierten Profiler](/manuals/profiling/) kannst du die Anzahl der Zeichenaufrufe und die zum Rendern benötigte Zeit messen.

Defold versucht, Renderoperationen nach den unten beschriebenen Regeln zu bündeln (Batching), um die Anzahl der Zeichenaufrufe zu verringern. Die Regeln unterscheiden sich zwischen GUI-Komponenten und allen anderen Komponententypen.


### Bündelungsregeln für Komponenten außerhalb der GUI {#batch-rules-for-non-gui-components}

Jeder Aufruf von `render.draw()` steuert, wie passende Einträge mit Sortierung im Weltkoordinatensystem geordnet werden. Der Standard ist `render.SORT_BACK_TO_FRONT`; verwende `render.SORT_FRONT_TO_BACK` zum Rendern von nah nach fern oder `render.SORT_NONE`, um die Einfügereihenfolge beizubehalten:

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

Die gewählte Reihenfolge bestimmt, welche Einträge nebeneinander liegen, und kann dadurch die Bündelung beeinflussen. In dieser sortierten Liste wird jedes Objekt mit dem vorherigen Objekt zu demselben Zeichenaufruf zusammengefasst, wenn die folgenden Bedingungen erfüllt sind:

* Es gehört zum selben Sammlungs-Proxy (collection proxy)
* Es hat denselben Komponententyp (Sprite, Partikeleffekt, Kachelkarte usw.)
* Es verwendet dieselbe Textur (Atlas oder Kachelquelle)
* Es hat dasselbe Material
* Es hat dieselben Shader-Konstanten (wie die Einfärbung)

Wenn also zwei Sprite-Komponenten im selben Sammlungs-Proxy nach der gewählten Sortierung nebeneinander liegen und dieselbe Textur, dasselbe Material und dieselben Konstanten verwenden, werden sie zu demselben Zeichenaufruf zusammengefasst.


### Bündelungsregeln für GUI-Komponenten {#batch-rules-for-gui-components}

Die Knoten einer GUI-Komponente werden in der Knotenliste von oben nach unten gerendert. Jeder Knoten in der Liste wird mit dem vorherigen Knoten zu demselben Zeichenaufruf zusammengefasst, wenn die folgenden Bedingungen erfüllt sind:

* Er hat denselben Typ (Box, Text, Kreissektor usw.)
* Er verwendet dieselbe Textur (Atlas oder Kachelquelle)
* Er hat denselben Mischmodus.
* Er hat dieselbe Schriftart (nur bei Textknoten)
* Er hat dieselben Stencil-Einstellungen

::: sidenote
Knoten werden pro Komponente gerendert. Das bedeutet, dass Knoten aus verschiedenen GUI-Komponenten nicht gebündelt werden.
:::

Die Möglichkeit, Knoten in Hierarchien anzuordnen, erleichtert es, sie zu überschaubaren Einheiten zusammenzufassen. Hierarchien können jedoch das gebündelte Rendern unterbrechen, wenn du unterschiedliche Knotentypen mischst. Mit GUI-Ebenen kannst du GUI-Knoten wirkungsvoller bündeln und dabei die Knotenhierarchien beibehalten. Mehr über GUI-Ebenen und ihren Einfluss auf Zeichenaufrufe erfährst du im [GUI-Handbuch](/manuals/gui#layers-and-draw-calls).
