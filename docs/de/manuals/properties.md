---
title: Eigenschaften in Defold
brief: Dieses Handbuch erklärt, welche Arten von Eigenschaften es in Defold gibt und wie sie verwendet und animiert werden.
---

# Eigenschaften {#properties}

Defold stellt Eigenschaften (properties) für Spielobjekte (game objects), Komponenten (components) und GUI-Knoten (GUI nodes) bereit, die gelesen, gesetzt und animiert werden können. Es gibt die folgenden Arten von Eigenschaften:

* Systemdefinierte Transformationen von Spielobjekten (Position, Drehung und Skalierung) und komponentenspezifische Eigenschaften (zum Beispiel die Größe eines Sprites in Pixeln oder die Masse eines Kollisionsobjekts (collision object))
* Benutzerdefinierte Eigenschaften von Skriptkomponenten, die in Lua-Skripten definiert werden (Einzelheiten findest du in der [Dokumentation zu Skripteigenschaften](/manuals/script-properties))
* Eigenschaften von GUI-Knoten
* Shader-Konstanten, die in Shadern und Materialdateien definiert werden (Einzelheiten findest du in der [Dokumentation zu Materialien](/manuals/material))

Numerische Eigenschaften zeigen einen Ziehgriff an, wenn du den Mauszeiger über ihr Eingabefeld bewegst. Du kannst ihren Wert erhöhen oder verringern, indem du den Griff nach rechts oder links beziehungsweise nach oben oder unten ziehst.

Je nachdem, wo eine Eigenschaft vorkommt, greifst du über eine allgemeine Funktion oder eine eigenschaftsspezifische Funktion auf sie zu. Viele Eigenschaften können automatisch animiert werden. Es wird dringend empfohlen, Eigenschaften über das integrierte System zu animieren, statt sie selbst (innerhalb einer `update()`-Funktion) zu verändern. Das ist sowohl aus Leistungsgründen als auch wegen der bequemeren Handhabung sinnvoll.

Zusammengesetzte Eigenschaften vom Typ `vector3`, `vector4` oder `quaternion` stellen auch ihre Teilkomponenten (`x`, `y`, `z` und `w`) bereit. Du kannst die Teilkomponenten einzeln ansprechen, indem du an den Namen einen Punkt (`.`) und den Namen der Teilkomponente anhängst. So setzt du zum Beispiel die x-Komponente der Position eines Spielobjekts:

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

Die Funktionen `go.get()`, `go.set()` und `go.animate()` nehmen als ersten Parameter eine Referenz und als zweiten einen Eigenschaftsbezeichner entgegen. Die Referenz bezeichnet das Spielobjekt oder die Komponente und kann eine Zeichenfolge, ein Hashwert oder eine URL sein. URLs werden im [Handbuch zur Adressierung](/manuals/addressing) ausführlich erklärt. Der Eigenschaftsbezeichner ist eine Zeichenfolge oder ein Hashwert, der die Eigenschaft benennt:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

Bei GUI-Knoten wird der Knoten als erster Parameter an eine eigenschaftsspezifische Funktion oder an die allgemeinen Funktionen `gui.get()` und `gui.set()` übergeben:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Eigenschaften von Spielobjekten und Komponenten {#game-object-and-component-properties}

Alle Spielobjekte und einige Komponententypen haben Eigenschaften, die zur Laufzeit gelesen und verändert werden können. Lies diese Werte mit [`go.get()`](/ref/go#go.get) und schreibe sie mit [`go.set()`](/ref/go#go.set). Je nach Datentyp des Eigenschaftswerts kannst du die Werte mit [`go.animate()`](/ref/go#go.animate) animieren. Ein kleiner Teil der Eigenschaften kann nur gelesen werden.

`get`{.mark}
: Kann mit [`go.get()`](/ref/go#go.get) gelesen werden.

`get+set`{.mark}
: Kann mit [`go.get()`](/ref/go#go.get) gelesen und mit [`go.set()`](/ref/go#go.set) geschrieben werden. Numerische Werte können mit [`go.animate()`](/ref/go#go.animate) animiert werden.

*Eigenschaften von Spielobjekten*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | Die lokale Position des Spielobjekts. | `vector3`      | `get+set`{.mark} |
| *rotation* | Die lokale Drehung des Spielobjekts, ausgedrückt als `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Die lokale Drehung des Spielobjekts als Euler-Winkel. | `vector3` | `get+set`{.mark} |
| *scale*    | Die lokale nicht gleichmäßige Skalierung des Spielobjekts, ausgedrückt als Vektor, dessen Komponenten jeweils einen Multiplikator entlang einer Achse enthalten. Um die Größe in X und Y zu verdoppeln, ohne Z zu verändern, verwende `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | Die lokale nicht gleichmäßige Skalierung des Spielobjekts entlang der X- und Y-Achse. Verwende diese Eigenschaft oder `go.set_scale_xy()`, wenn keine Skalierung in Z beabsichtigt ist. | `vector3` | `get+set`{.mark} |

::: sidenote
Es gibt auch spezifische Funktionen für die Transformation des Spielobjekts: `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` und `go.set_scale_xy()`.
:::

*Eigenschaften von Sprite-Komponenten*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | Die unskalierte Größe des Sprites---seine Größe aus dem Quellatlas. | `vector3` | `get`{.mark} |
| *image* | Der Hashwert des Texturpfads des Sprites. | `hash` | `get`{.mark}|
| *scale* | Die nicht gleichmäßige Skalierung des Sprites. | `vector3` | `get+set`{.mark}|
| *scale.xy* | Die nicht gleichmäßige Skalierung des Sprites entlang der X- und Y-Achse. | `vector3` | `get+set`{.mark}|
| *material* | Das vom Sprite verwendete Material. | `hash` | `get+set`{.mark}|
| *cursor* | Die Position (im Bereich 0--1) des Wiedergabezeigers. | `number` | `get+set`{.mark}|
| *playback_rate* | Die Bildrate (Bilder pro Sekunde, FPS) der Flipbook-Animation. | `number` | `get+set`{.mark}|

*Eigenschaften von Kollisionsobjekt-Komponenten*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | Die Masse des Kollisionsobjekts. | `number` | `get`{.mark} |
| *linear_velocity* | Die aktuelle lineare Geschwindigkeit des Kollisionsobjekts. | `vector3` | `get`{.mark} |
| *angular_velocity* | Die aktuelle Winkelgeschwindigkeit des Kollisionsobjekts. | `vector3` | `get`{.mark} |
| *linear_damping* | Die lineare Dämpfung des Kollisionsobjekts. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Die Winkeldämpfung des Kollisionsobjekts. | `vector3` | `get+set`{.mark} |

*Eigenschaften von Modellkomponenten (3D)*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | Die aktuelle Animation.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Die Hashwerte der Texturpfade des Modells. | `hash` | `get+set`{.mark}|
| *cursor*  | Die Position (im Bereich 0--1) des Wiedergabezeigers. | `number`   | `get+set`{.mark} |
| *playback_rate* | Die Wiedergabegeschwindigkeit der Animation. Ein Multiplikator für die Wiedergabegeschwindigkeit der Animation. | `number` | `get+set`{.mark} |
| *material* | Das vom Modell verwendete Material. | `hash` | `get+set`{.mark}|

*Eigenschaften von Beschriftungskomponenten*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *text* | Der Textinhalt der Beschriftung (label). Verfügbar seit Defold 1.13.2. | `string` | `get+set`{.mark} |
| *scale* | Die Skalierung der Beschriftung. | `vector3` | `get+set`{.mark} |
| *scale.xy* | Die Skalierung der Beschriftung entlang der X- und Y-Achse. | `vector3` | `get+set`{.mark}|
| *color*     | Die Farbe der Beschriftung. | `vector4` | `get+set`{.mark} |
| *outline* | Die Konturfarbe der Beschriftung. | `vector4` | `get+set`{.mark} |
| *shadow* | Die Schattenfarbe der Beschriftung. | `vector4` | `get+set`{.mark} |
| *size* | Die Größe der Beschriftung. Die Größe begrenzt den Text, wenn der Zeilenumbruch aktiviert ist. | `vector3` | `get+set`{.mark} |
| *material* | Das von der Beschriftung verwendete Material. | `hash` | `get+set`{.mark}|
| *font* | Die von der Beschriftung verwendete Schriftart. | `hash` | `get+set`{.mark}|


## Eigenschaften von GUI-Knoten {#gui-node-properties}

GUI-Knoten haben eigenschaftsspezifische Getter- und Setter-Funktionen wie `gui.get_position()` und `gui.set_position()`. Die unten aufgeführten integrierten Eigenschaften können alternativ mit `gui.get(node, property)` und `gui.set(node, property, value)` gelesen und geschrieben werden. Andere Knotenwerte benötigen möglicherweise weiterhin ihre eigenen Funktionen. Materialkonstanten von GUI-Knoten verwenden ebenfalls die allgemeinen Funktionen. Um eine Komponente einer Vektoreigenschaft anzusprechen, hänge ihren Namen an, zum Beispiel `gui.set(node, "color.x", 1)`.

Die allgemeinen und die eigenschaftsspezifischen Funktionen verwenden nicht immer dieselben Datentypen. `gui.get()` gibt einen `vector4` für die vollständigen Eigenschaften `position`, `scale`, `size` und `euler` zurück, während die entsprechenden eigenschaftsspezifischen Funktionen einen `vector3` zurückgeben. `gui.set()` akzeptiert für diese Eigenschaften sowohl einen `vector3` als auch einen `vector4`. Die allgemeine Eigenschaft `rotation` verwendet ein Quaternion; verwende `euler`, wenn du die Drehung in Grad setzt.

* `position` (oder `gui.PROP_POSITION`)
* `rotation` (oder `gui.PROP_ROTATION`)
* `euler` (oder `gui.PROP_EULER`)
* `scale` (oder `gui.PROP_SCALE`)
* `color` (oder `gui.PROP_COLOR`)
* `outline` (oder `gui.PROP_OUTLINE`)
* `shadow` (oder `gui.PROP_SHADOW`)
* `size` (oder `gui.PROP_SIZE`)
* `fill_angle` (oder `gui.PROP_FILL_ANGLE`)
* `inner_radius` (oder `gui.PROP_INNER_RADIUS`)
* `leading` (oder `gui.PROP_LEADING`)
* `tracking` (oder `gui.PROP_TRACKING`)
* `slice9` (oder `gui.PROP_SLICE9`)

Beachte, dass alle Farbwerte in einem `vector4` kodiert sind, dessen Komponenten den RGBA-Werten entsprechen:

`x`
: Der rote Farbanteil

`y`
: Der grüne Farbanteil

`z`
: Der blaue Farbanteil

`w`
: Der Alpha-Anteil

*Eigenschaften von GUI-Knoten*

| Eigenschaft   | Beschreibung                            | Typ            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | Die Flächenfarbe des Knotens.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | Die Konturfarbe des Knotens.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | Die Position des Knotens. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | Die Drehung des Knotens. Der Getter gibt ein Quaternion zurück; der Setter akzeptiert ein Quaternion oder Euler-Winkel als Vektor. | `quaternion`, `vector3` oder `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | Die Drehung des Knotens, ausgedrückt als Euler-Winkel in Grad. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | Die Skalierung des Knotens, ausgedrückt als Multiplikator entlang jeder Achse. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | Die Schattenfarbe des Knotens. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | Die unskalierte Größe des Knotens. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | Der Füllwinkel eines Kreissektor-Knotens (pie node), ausgedrückt in Grad gegen den Uhrzeigersinn. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | Der innere Radius eines Kreissektor-Knotens. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | Der Skalierungsfaktor für den Zeilenabstand eines Textknotens. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | Der Skalierungsfaktor für den Zeichenabstand eines Textknotens. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | Die Randabstände eines Knotens mit Neun-Segment-Skalierung (9-slice). | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
