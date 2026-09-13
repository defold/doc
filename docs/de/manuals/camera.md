---
title: Handbuch zur Kamerakomponente
brief: Dieses Handbuch beschreibt die Funktionen der Kamerakomponente von Defold.
---

# Kameras {#cameras}

Eine Kamera in Defold ist eine Komponente (component), die den Ansichtsbereich (viewport) und die Projektion der Spielwelt ändert. Die Kamerakomponente definiert eine grundlegende perspektivische oder orthografische Kamera, die dem Render-Skript eine Ansichts- und eine Projektionsmatrix bereitstellt.

Eine perspektivische Kamera wird üblicherweise für 3D-Spiele verwendet. Dabei hängen die Ansicht der Kamera sowie die Größe und Perspektive der Objekte von einem Sichtpyramidenstumpf und dem Abstand und Blickwinkel der Kamera zu den Objekten im Spiel ab.

Bei 2D-Spielen ist es oft erwünscht, die Szene mit einer orthografischen Projektion zu rendern. Das bedeutet, dass die Ansicht der Kamera nicht mehr durch einen Sichtpyramidenstumpf, sondern durch einen Quader bestimmt wird. Eine orthografische Projektion ist insofern unrealistisch, als sie die Größe der Objekte nicht abhängig von ihrer Entfernung verändert. Ein 1000 Einheiten entferntes Objekt wird in derselben Größe gerendert wie ein Objekt direkt vor der Kamera.

![Projektionen](images/camera/projections.png)


## Eine Kamera erstellen {#creating-a-camera}

Um eine Kamera zu erstellen, klicke <kbd>mit der rechten Maustaste</kbd> auf ein Spielobjekt (game object) und wähle <kbd>Add Component ▸ Camera</kbd>. Alternativ kannst du in deiner Projekthierarchie eine Komponentendatei erstellen und sie dem Spielobjekt hinzufügen.

![Kamerakomponente erstellen](images/camera/create.png)

Die Kamerakomponente hat die folgenden Eigenschaften, die das *Sichtvolumen* der Kamera definieren:

![Kameraeinstellungen](images/camera/settings.png)

Id
: Der Bezeichner der Komponente

Aspect Ratio
: (**Nur perspektivische Kamera**) - Das Verhältnis zwischen Breite und Höhe des Sichtvolumens. 1.0 bedeutet, dass du von einer quadratischen Ansicht ausgehst. 1.33 eignet sich für eine 4:3-Ansicht wie 1024 × 768. 1.78 eignet sich für eine 16:9-Ansicht. Diese Einstellung wird ignoriert, wenn *Auto Aspect Ratio* aktiviert ist.

Fov
: (**Nur perspektivische Kamera**) - Der *vertikale* Sichtwinkel der Kamera, angegeben im _Bogenmaß_. Je größer der Sichtwinkel, desto mehr sieht die Kamera.

Near Z
: Der Z-Wert der nahen Begrenzungsebene.

Far Z
: Der Z-Wert der fernen Begrenzungsebene.

Auto Aspect Ratio
: (**Nur perspektivische Kamera**) - Aktiviere diese Einstellung, damit die Kamera das Seitenverhältnis automatisch berechnet.

Orthographic Projection
: Aktiviere diese Einstellung, um die Kamera auf eine orthografische Projektion umzustellen (siehe unten).

Orthographic Zoom
: (**Nur orthografische Kamera**) - Ein von dir steuerbarer Zoom-Multiplikator (> 1 = vergrößern, < 1 = verkleinern). Im Modus `Fixed` ist er der effektive Zoom. In den Modi `Auto Fit` und `Auto Cover` wird er mit dem automatisch berechneten Zoom multipliziert. Dadurch kannst du zusätzlichen Zoom anwenden, ohne die automatische Größenanpassung zu deaktivieren.

Orthographic Mode
: (**Nur orthografische Kamera**) - Steuert, wie die orthografische Kamera den Zoom anhand der Fenstergröße und deiner Entwurfsauflösung (der Werte in `game.project` → `display.width/height`) bestimmt.
  - `Fixed` (konstanter Zoom): Verwendet den aktuellen Wert von `Orthographic Zoom` unverändert.
  - `Auto Fit` (einpassen): Berechnet den Zoom automatisch so, dass der gesamte Entwurfsbereich in das Fenster passt, und multipliziert ihn anschließend mit `Orthographic Zoom`. An den Seiten oder oben und unten können zusätzliche Inhalte sichtbar sein.
  - `Auto Cover` (ausfüllen): Berechnet den Zoom automatisch so, dass der Entwurfsbereich das gesamte Fenster ausfüllt, und multipliziert ihn anschließend mit `Orthographic Zoom`. An den Seiten oder oben und unten können Inhalte abgeschnitten werden.
  Nur verfügbar, wenn `Orthographic Projection` aktiviert ist.


## Die Kamera verwenden {#using-the-camera}

Alle Kameras werden innerhalb eines Frames automatisch aktiviert und aktualisiert. Das Lua-Modul `camera` ist in allen Skriptkontexten verfügbar. Seit Defold 1.8.1 musst du eine Kamera nicht mehr ausdrücklich aktivieren, indem du eine Nachricht vom Typ `acquire_camera_focus` an die Kamerakomponente sendest. Die alten Nachrichten zum Anfordern und Freigeben des Kamerafokus sind weiterhin verfügbar. Es wird jedoch empfohlen, stattdessen die Nachrichten `enable` und `disable` zu verwenden, wie bei jeder anderen Komponente, die du aktivieren oder deaktivieren möchtest:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Mit `camera.get_cameras()` kannst du alle aktuell verfügbaren Kameras auflisten:

```lua
-- Note: The render calls are only available in a render script.
--       The camera.get_cameras() function can be used anywhere,
--       but render.set_camera can only be used in a render script.

for k,v in pairs(camera.get_cameras()) do
    -- the camera table contains the URLs of all cameras
    render.set_camera(v)
    -- do rendering here - anything rendered here that uses materials with
    -- view and projection matrices specified, will use matrices from the camera.
end
-- to disable a camera, pass in nil (or no arguments at all) to render.set_camera.
-- after this call, all render calls will use the view and projection matrices
-- that are specified on the render context (render.set_view and render.set_projection)
render.set_camera()
```

Das Skriptmodul `camera` bietet mehrere Funktionen, mit denen du die Kamera verändern kannst. Hier sind einige davon aufgeführt. Alle verfügbaren Funktionen findest du in der [API-Dokumentation](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- get aspect ratio
camera.get_far_z(camera) -- get far z
camera.get_fov(camera) -- get field of view
camera.get_orthographic_mode(camera) -- get orthographic mode (one of camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- get the user-controlled zoom multiplier
camera.get_orthographic_auto_zoom(camera) -- get the automatically calculated zoom
camera.set_aspect_ratio(camera, ratio) -- set aspect ratio
camera.set_far_z(camera, far_z) -- set far z
camera.set_near_z(camera, near_z) -- set near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- set orthographic mode
... And so forth
```

Eine Kamera wird durch eine URL identifiziert. Diese enthält den vollständigen Szenenpfad der Komponente, einschließlich der Sammlung (collection), des zugehörigen Spielobjekts und des Komponentenbezeichners. In diesem Beispiel verwendest du die URL `/go#camera`, um die Kamerakomponente innerhalb derselben Sammlung zu identifizieren, und `main:/go#camera`, wenn du aus einer anderen Sammlung oder aus dem Render-Skript auf die Kamera zugreifst.

![Kamerakomponente erstellen](images/camera/create.png)

```lua
-- Accessing a camera from a script in the same collection:
camera.get_fov("/go#camera")

-- Accessing a camera from a script in a different collection:
camera.get_fov("main:/go#camera")

-- Accessing a camera from the render script:
render.set_camera("main:/go#camera")
```

In jedem Frame sendet die Kamerakomponente, die aktuell den Kamerafokus hat, eine Nachricht vom Typ `set_view_projection` an den Socket `@render`:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Die von der Kamerakomponente gesendete Nachricht enthält eine Ansichtsmatrix und eine Projektionsmatrix.

Die Kamerakomponente stellt dem Render-Skript je nach Eigenschaft *Orthographic Projection* der Kamera eine perspektivische oder eine orthografische Projektionsmatrix bereit. Die Projektionsmatrix berücksichtigt außerdem die festgelegte nahe und ferne Begrenzungsebene, den Sichtwinkel und das Seitenverhältnis der Kamera.

Die von der Kamera bereitgestellte Ansichtsmatrix definiert die Position und Ausrichtung der Kamera. Eine Kamera mit *Orthographic Projection* zentriert die Ansicht auf die Position des Spielobjekts, dem sie zugeordnet ist. Bei einer Kamera mit *Perspective Projection* befindet sich die untere linke Ecke der Ansicht an der Position des Spielobjekts, dem sie zugeordnet ist.


### Render-Skript {#render-script}

Wenn du das Standard-Render-Skript verwendest, legt Defold automatisch die zuletzt aktivierte Kamera als Kamera für das Rendering fest. Vor dieser Änderung musste ein Skript im Projekt ausdrücklich die Nachricht `use_camera_projection` an den Renderer senden, um ihm mitzuteilen, dass die Ansicht und Projektion der Kamerakomponenten verwendet werden sollen. Das ist nicht mehr erforderlich, bleibt aber aus Gründen der Abwärtskompatibilität weiterhin möglich.

Alternativ kannst du in einem Render-Skript eine bestimmte Kamera festlegen, die für das Rendering verwendet werden soll. Das kann nützlich sein, wenn du genauer steuern musst, welche Kamera für das Rendering verwendet wird, beispielsweise in einem Mehrspielerspiel.

```lua
-- render.set_camera will automatically use the view and projection matrices
-- for any rendering happening until render.set_camera() is called.
render.set_camera("main:/my_go#camera")
```

Mit der Funktion `get_enabled` aus der [Kamera-API](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera) kannst du prüfen, ob eine Kamera aktiv ist:

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- camera is enabled, use it for rendering!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Um die Funktion `set_camera` zusammen mit dem Aussondern von Geometrie außerhalb des Sichtvolumens (Frustum Culling) zu verwenden, musst du dies als Option an die Funktion übergeben:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Die Kamera verschieben {#panning-the-camera}

Du verschiebst die Kamera in der Spielwelt, indem du das Spielobjekt bewegst, dem die Kamerakomponente zugeordnet ist. Die Kamerakomponente sendet automatisch eine aktualisierte Ansichtsmatrix anhand der aktuellen Position der Kamera auf der x- und y-Achse.

### Den Kamerazoom ändern {#zooming-the-camera}

Bei einer perspektivischen Kamera kannst du die Ansicht vergrößern und verkleinern, indem du das Spielobjekt, dem die Kamera zugeordnet ist, entlang der z-Achse bewegst. Die Kamerakomponente sendet automatisch eine aktualisierte Ansichtsmatrix anhand der aktuellen z-Position der Kamera.

Bei einer orthografischen Kamera kannst du die Ansicht vergrößern und verkleinern, indem du die Eigenschaft *Orthographic Zoom* der Kamera im Editor oder zur Laufzeit änderst:

```lua
-- In Fixed mode, this is the effective zoom.
go.set("#camera", "orthographic_zoom", 2)
```

In den Modi `Auto Fit` und `Auto Cover` wird *Orthographic Zoom* zusätzlich auf den automatisch berechneten Zoom angewendet und nicht ignoriert. Setze beispielsweise im Editor *Orthographic Mode* auf `Auto Fit` und *Orthographic Zoom* auf `1.25`, um den Entwurfsbereich in das Fenster einzupassen und die Ansicht anschließend um weitere 25 % zu vergrößern. Die entsprechende Konfiguration zur Laufzeit lautet:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` gibt in den Modi `Auto Fit` und `Auto Cover` den Zoom zurück, der anhand der aktuellen Fenster- und Projektabmessungen berechnet wird. Im Modus `Fixed` gibt die Funktion `1.0` zurück. Derselbe Wert ist über die nur lesbare Komponenteneigenschaft `orthographic_auto_zoom` verfügbar:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Bei einer orthografischen Kamera kannst du außerdem über die Einstellung `Orthographic Mode` oder per Skript ändern, wie der Zoom bestimmt wird:

```lua
-- get current mode (one of camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- switch to auto-fit (contain) to always keep the full design area visible
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- switch to auto-cover to ensure the design area covers the window
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- switch to fixed mode to use orthographic_zoom without automatic sizing
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Adaptiver Zoom {#adaptive-zoom}

Das Konzept hinter adaptivem Zoom besteht darin, den Zoomwert der Kamera anzupassen, wenn sich die Auflösung der Anzeige gegenüber der ursprünglich in *game.project* festgelegten Auflösung ändert.

Zwei gängige Ansätze für adaptiven Zoom sind:

1. Maximaler Zoom - Berechne einen Zoomwert, bei dem der von der ursprünglichen Auflösung in *game.project* abgedeckte Inhalt den Bildschirm ausfüllt und über dessen Grenzen hinausreicht. Dabei können Inhalte an den Seiten oder oben und unten verdeckt werden.
2. Minimaler Zoom - Berechne einen Zoomwert, bei dem der von der ursprünglichen Auflösung in *game.project* abgedeckte Inhalt vollständig innerhalb der Bildschirmgrenzen liegt. Dabei können zusätzliche Inhalte an den Seiten oder oben und unten sichtbar werden.

Beispiel:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: ensure that the initial design dimensions will fill and expand beyond the screen bounds
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: ensure that the initial design dimensions will shrink and be contained within the screen bounds
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Ein vollständiges Beispiel für adaptiven Zoom findest du in [diesem Beispielprojekt](https://github.com/defold/sample-adaptive-zoom).

Hinweis: Mit einer orthografischen Kamera kannst du jetzt ohne eigenen Code erreichen, dass der Entwurfsbereich eingepasst wird oder das Fenster ausfüllt. Setze dazu `Orthographic Mode` auf `Auto Fit` (einpassen) oder `Auto Cover` (ausfüllen). In diesen Modi wird der aus der Fenstergröße und der Entwurfsauflösung berechnete Zoom mit `Orthographic Zoom` multipliziert.


### Einem Spielobjekt folgen {#following-a-game-object}

Du kannst die Kamera einem Spielobjekt folgen lassen, indem du das Spielobjekt mit der Kamerakomponente dem zu verfolgenden Spielobjekt unterordnest:

![Einem Spielobjekt folgen](images/camera/follow.png)

Alternativ kannst du in jedem Frame die Position des Spielobjekts mit der Kamerakomponente aktualisieren, während sich das zu verfolgende Spielobjekt bewegt.

### Zwischen Bildschirm- und Weltkoordinaten umrechnen {#converting-mouse-to-world-coordinates}

Wenn eine Kamera verschoben, ihr Zoom verändert oder ihre Projektion geändert wurde, stimmen Eingabekoordinaten nicht mehr direkt mit Weltkoordinaten überein. Verwende die Umrechnungsfunktionen der Kamera mit `action.screen_x` und `action.screen_y`. Wenn du die optionale Kamera-URL weglässt, wird die zuletzt aktivierte Kamera verwendet.

Bei einer orthografischen Kamera gibt [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]) für ein Bildschirmpixel den Punkt auf der nahen Begrenzungsebene der Kamera im Weltkoordinatensystem zurück:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Bei einer perspektivischen Kamera nimmt [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]) einen `vector3` entgegen, dessen Z-Komponente die von der Kameraebene aus gemessene Ansichtstiefe in Welteinheiten angibt:

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) führt die umgekehrte Umrechnung durch. Die Funktion gibt X und Y in Bildschirmpixeln sowie Z nach derselben Konvention für die Ansichtstiefe zurück. Ihr Ergebnis kann daher wieder an `camera.screen_to_world()` übergeben werden:

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Auf der [Beispielseite](https://defold.com/examples/render/screen_to_world/) kannst du die Koordinatenumrechnung in Aktion sehen. Außerdem gibt es ein [Beispielprojekt](https://github.com/defold/sample-screen-to-world-coordinates/), das dieselben APIs zeigt.

::: sidenote
Die [in diesem Handbuch erwähnten Kameralösungen von Drittanbietern](/manuals/camera/#third-party-camera-solutions) bieten Funktionen für die Umrechnung in und aus Bildschirmkoordinaten.
:::

## Änderungen zur Laufzeit {#runtime-manipulation}
Du kannst Kameras zur Laufzeit über verschiedene Nachrichten und Eigenschaften verändern (Hinweise zur Verwendung findest du in der [API-Dokumentation](/ref/camera/)).

Eine Kamera hat verschiedene Eigenschaften, auf die du mit `go.get()` und `go.set()` zugreifen kannst:

`fov`
: Der Sichtwinkel der Kamera (`number`).

`near_z`
: Der nahe Z-Wert der Kamera (`number`).

`far_z`
: Der ferne Z-Wert der Kamera (`number`).

`orthographic_zoom`
: Der von dir steuerbare Zoom-Multiplikator der orthografischen Kamera. In den Modi `Auto Fit` und `Auto Cover` wird er mit `orthographic_auto_zoom` multipliziert. (`number`).

`orthographic_auto_zoom`
: Der berechnete orthografische Zoom für die Modi `Auto Fit` und `Auto Cover` oder `1.0` im Modus `Fixed`. NUR LESBAR. (`number`).

`aspect_ratio`
: Das Verhältnis zwischen Breite und Höhe des Sichtvolumens. Wird bei der Berechnung der Projektion einer perspektivischen Kamera verwendet. (`number`).

`view`
: Die berechnete Ansichtsmatrix der Kamera. NUR LESBAR. (`matrix4`).

`projection`
: Die berechnete Projektionsmatrix der Kamera. NUR LESBAR. (`matrix4`).


## Kameralösungen von Drittanbietern {#third-party-camera-solutions}

Es gibt Kameralösungen aus der Community, die gängige Funktionen wie Bildschirmwackeln, das Verfolgen von Spielobjekten, die Umrechnung von Bildschirm- in Weltkoordinaten und vieles mehr bereitstellen. Du kannst sie aus dem Defold Asset Portal herunterladen:

- [Orthographic camera](https://defold.com/assets/orthographic/) (nur 2D) von Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D und 3D) von Klayton Kowalski.
