---
title: Handbuch zu Eigenschaftsanimationen in Defold
brief: Dieses Handbuch beschreibt, wie du Eigenschaftsanimationen in Defold verwendest.
---

# Eigenschaftsanimation {#property-animation}

Alle numerischen Eigenschaften (`numbers`, `vector3`, `vector4` und Quaternionen) sowie Shader-Konstanten können mit dem integrierten Animationssystem über die Funktion `go.animate()` animiert werden. Die Engine interpoliert die Eigenschaften automatisch für dich entsprechend den angegebenen Wiedergabemodi und Easing-Funktionen. Du kannst auch eigene Easing-Funktionen angeben.

  ![Eigenschaftsanimation](images/animation/property_animation.png)
  ![Wiederholte Sprungbewegung](images/animation/bounce.gif)

## Eigenschaftsanimation {#property-animation-1}

Um eine Eigenschaft eines Spielobjekts (game object) oder einer Komponente (component) zu animieren, verwende die Funktion `go.animate()`. Für Eigenschaften von GUI-Knoten (GUI nodes) lautet die entsprechende Funktion `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Um alle Animationen einer bestimmten Eigenschaft anzuhalten, rufe `go.cancel_animations()` oder bei GUI-Knoten `gui.cancel_animations()` auf:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

Wenn du die Animation einer zusammengesetzten Eigenschaft wie `position` abbrichst, werden auch alle Animationen ihrer einzelnen Komponenten (`position.x`, `position.y` und `position.z`) abgebrochen.

Das [Handbuch zu Eigenschaften](/manuals/properties) enthält alle verfügbaren Eigenschaften von Spielobjekten, Komponenten und GUI-Knoten.

## Eigenschaftsanimation bei GUI-Knoten {#gui-node-property-animation}

Fast alle Eigenschaften von GUI-Knoten lassen sich animieren. Du kannst zum Beispiel einen Knoten unsichtbar machen, indem du seine Eigenschaft `color` auf vollständige Transparenz setzt, und ihn anschließend einblenden, indem du die Farbe zu Weiß animierst (also ohne Einfärbung).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Callbacks bei Abschluss {#completion-callbacks}

Die Funktionen zur Eigenschaftsanimation `go.animate()` und `gui.animate()` unterstützen als letztes Argument eine optionale Lua-Callback-Funktion. Diese Funktion wird aufgerufen, wenn die Animation bis zum Ende abgespielt wurde. Bei wiederholten Animationen wird die Funktion nie aufgerufen, ebenso wenig, wenn eine Animation manuell über `go.cancel_animations()` oder `gui.cancel_animations()` abgebrochen wird. Mit dem Callback kannst du beim Abschluss einer Animation Ereignisse auslösen oder mehrere Animationen miteinander verketten.

## Easing

Easing legt fest, wie sich der animierte Wert mit der Zeit ändert. Die folgenden Bilder zeigen die Funktionen, die über die Zeit angewendet werden, um das Easing zu erzeugen.

Die folgenden Easing-Werte sind für `go.animate()` gültig:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

Die folgenden Easing-Werte sind für `gui.animate()` gültig:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Lineare Interpolation](images/properties/easing_linear.png)
![Back-Kurve (In)](images/properties/easing_inback.png)
![Back-Kurve (Out)](images/properties/easing_outback.png)
![Back-Kurve (In-out)](images/properties/easing_inoutback.png)
![Back-Kurve (Out-in)](images/properties/easing_outinback.png)
![Bounce-Kurve (In)](images/properties/easing_inbounce.png)
![Bounce-Kurve (Out)](images/properties/easing_outbounce.png)
![Bounce-Kurve (In-out)](images/properties/easing_inoutbounce.png)
![Bounce-Kurve (Out-in)](images/properties/easing_outinbounce.png)
![Elastische Kurve (In)](images/properties/easing_inelastic.png)
![Elastische Kurve (Out)](images/properties/easing_outelastic.png)
![Elastische Kurve (In-out)](images/properties/easing_inoutelastic.png)
![Elastische Kurve (Out-in)](images/properties/easing_outinelastic.png)
![Sinuskurve (In)](images/properties/easing_insine.png)
![Sinuskurve (Out)](images/properties/easing_outsine.png)
![Sinuskurve (In-out)](images/properties/easing_inoutsine.png)
![Sinuskurve (Out-in)](images/properties/easing_outinsine.png)
![Exponentialkurve (In)](images/properties/easing_inexpo.png)
![Exponentialkurve (Out)](images/properties/easing_outexpo.png)
![Exponentialkurve (In-out)](images/properties/easing_inoutexpo.png)
![Exponentialkurve (Out-in)](images/properties/easing_outinexpo.png)
![Kreiskurve (In)](images/properties/easing_incirc.png)
![Kreiskurve (Out)](images/properties/easing_outcirc.png)
![Kreiskurve (In-out)](images/properties/easing_inoutcirc.png)
![Kreiskurve (Out-in)](images/properties/easing_outincirc.png)
![Quadratische Kurve (In)](images/properties/easing_inquad.png)
![Quadratische Kurve (Out)](images/properties/easing_outquad.png)
![Quadratische Kurve (In-out)](images/properties/easing_inoutquad.png)
![Quadratische Kurve (Out-in)](images/properties/easing_outinquad.png)
![Kubische Kurve (In)](images/properties/easing_incubic.png)
![Kubische Kurve (Out)](images/properties/easing_outcubic.png)
![Kubische Kurve (In-out)](images/properties/easing_inoutcubic.png)
![Kubische Kurve (Out-in)](images/properties/easing_outincubic.png)
![Quartische Kurve (In)](images/properties/easing_inquart.png)
![Quartische Kurve (Out)](images/properties/easing_outquart.png)
![Quartische Kurve (In-out)](images/properties/easing_inoutquart.png)
![Quartische Kurve (In-out)](images/properties/easing_outinquart.png)
![Quintische Kurve (In)](images/properties/easing_inquint.png)
![Quintische Kurve (Out)](images/properties/easing_outquint.png)
![Quintische Kurve (In-out)](images/properties/easing_inoutquint.png)
![Quintische Kurve (Out-in)](images/properties/easing_outinquint.png)

## Eigenes Easing {#custom-easing}

Du kannst eigene Easing-Kurven erstellen, indem du einen `vector` mit einer Reihe von Werten definierst und diesen Vektor anstelle einer der oben aufgeführten vordefinierten Easing-Konstanten übergibst. Die Vektorwerte beschreiben eine Kurve vom Startwert (`0`) zum Zielwert (`1`). Die Laufzeitumgebung liest Werte aus dem Vektor aus und interpoliert linear, um Werte zwischen den im Vektor angegebenen Punkten zu berechnen.

Der folgende Vektor zum Beispiel:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

ergibt diese Kurve:

![Eigene Kurve](images/animation/custom_curve.png)

Das folgende Beispiel lässt die y-Position eines Spielobjekts entsprechend einer Rechteckkurve zwischen der aktuellen Position und 200 springen:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Rechteckkurve](images/animation/square_curve.png)
