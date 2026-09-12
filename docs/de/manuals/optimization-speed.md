---
title: Laufzeitleistung eines Defold-Spiels optimieren
brief: Dieses Handbuch beschreibt, wie du ein Defold-Spiel so optimierst, dass es mit einer stabil hohen Bildrate läuft.
---

# Ausführungsgeschwindigkeit optimieren {#optimizing-runtime-speed}
Bevor du versuchst, ein Spiel für eine stabil hohe Bildrate (Bilder pro Sekunde, FPS) zu optimieren, musst du wissen, wo die Engpässe liegen. Was beansprucht in einem Frame deines Spiels tatsächlich die meiste Zeit? Ist es das Rendering? Ist es deine Spiellogik? Ist es der Szenengraph (scene graph)? Um das herauszufinden, empfiehlt sich die Verwendung der integrierten Profiling-Werkzeuge. Verwende den [Bildschirm- oder Web-Profiler](/manuals/profiling/), um die Leistung deines Spiels zu messen und dann zu entscheiden, ob und was du optimieren solltest. Sobald du besser verstehst, was Zeit beansprucht, kannst du die Probleme angehen.

## Ausführungszeit von Skripten verringern {#reduce-script-execution-time}
Du musst die Ausführungszeit von Skripten verringern, wenn der Profiler hohe Werte für den Messbereich `Script` anzeigt. Als allgemeine Faustregel solltest du natürlich versuchen, in jedem Frame möglichst wenig Code auszuführen. Viel Code in `update()` und `on_input()` in jedem Frame auszuführen, wirkt sich wahrscheinlich auf die Leistung deines Spiels aus, insbesondere auf weniger leistungsfähigen Geräten. Hier sind einige Richtlinien:

### Reaktive Codemuster verwenden {#use-reactive-code-patterns}
Frage Änderungen nicht wiederholt ab, wenn du einen Callback erhalten kannst. Animiere nichts manuell und führe keine Aufgabe selbst aus, die du der Engine überlassen kannst (z. B. `go.animate)()` statt einer manuellen Animation).

### Automatische Speicherbereinigung reduzieren {#reduce-garbage-collection}
Wenn du in jedem Frame viele kurzlebige Objekte wie Lua-Tabellen erstellst, löst das irgendwann die automatische Speicherbereinigung (Garbage Collection) von Lua aus. Das kann sich als kurze Ruckler oder Spitzen in der Frame-Dauer bemerkbar machen. Verwende Tabellen nach Möglichkeit wieder und versuche wirklich, Lua-Tabellen möglichst nicht innerhalb von Schleifen und ähnlichen Konstrukten zu erstellen.

### Hashwerte von Nachrichten- und Aktionsbezeichnern vorab berechnen {#prehash-message-and-action-ids}
Wenn du viele Nachrichten verarbeitest oder viele Eingabeereignisse behandeln musst, empfiehlt es sich, die Hashwerte der Zeichenfolgen vorab zu berechnen. Betrachte diesen Code:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

Im obigen Beispiel würde der Hashwert der Zeichenfolge jedes Mal neu berechnet, wenn eine Nachricht empfangen wird. Du kannst das verbessern, indem du die Hashwerte der Zeichenfolgen einmal berechnest und sie dann bei der Verarbeitung von Nachrichten verwendest:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### URLs bevorzugen und zwischenspeichern {#prefer-and-cache-urls}
Beim Übermitteln von Nachrichten oder beim anderweitigen Adressieren eines Spielobjekts (game object) oder einer Komponente (component) kannst du einen Bezeichner als Zeichenfolge oder Hashwert oder eine URL angeben. Wenn du eine Zeichenfolge oder einen Hashwert verwendest, wird diese Angabe intern in eine URL umgewandelt. Deshalb empfiehlt es sich, häufig verwendete URLs zwischenzuspeichern, um die bestmögliche Leistung aus dem System herauszuholen. Betrachte Folgendes:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

In allen drei Fällen würde die Position eines Spielobjekts mit dem Bezeichner `enemy` abgerufen. Im ersten und zweiten Fall würde der Bezeichner (Zeichenfolge oder Hashwert) vor der Verwendung in eine URL umgewandelt. Daraus ergibt sich, dass es für die bestmögliche Leistung besser ist, URLs zwischenzuspeichern und die zwischengespeicherte Version zu verwenden:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## Zeit zum Rendern eines Frames verringern {#reduce-time-it-takes-to-render-a-frame}
Du musst die Zeit zum Rendern eines Frames verringern, wenn der Profiler hohe Werte in den Messbereichen `Render` und `Render Script` anzeigt. Wenn du diese Zeit verringern möchtest, solltest du mehrere Dinge berücksichtigen:

* Zeichenaufrufe (draw calls) reduzieren - Lies mehr über das Reduzieren von Zeichenaufrufen in [diesem Forumsbeitrag](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Mehrfaches Zeichnen derselben Pixel (Overdraw) reduzieren
* Shader-Komplexität verringern - Informiere dich über GLSL-Optimierungen in [diesem Khronos-Artikel](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). Du kannst auch die von Defold verwendeten Standard-Shader (unter `builtins/materials`) ändern und eine geringere Genauigkeit wählen, wenn der Shader kein `highp` benötigt. Crosskompilierte GLSL-ES-Shader verwenden standardmäßig `mediump` für Gleitkommawerte und `highp` für Ganzzahlen. Diese Standardwerte lassen sich in den Projekteinstellungen unter Shader ändern. Explizite Qualifizierer für einzelne Variablen haben Vorrang. Siehe die [Dokumentation zur Shader-Genauigkeit](/manuals/shader/#precision).

## Komplexität des Szenengraphen verringern {#reduce-scene-graph-complexity}
Du musst die Komplexität des Szenengraphen verringern, wenn der Profiler hohe Werte im Messbereich `GameObject` und insbesondere für den Messwert `UpdateTransform` anzeigt. Mögliche Maßnahmen:

* Aussondern von Geometrie (Culling) - Deaktiviere Spielobjekte (und ihre Komponenten), wenn sie gerade nicht sichtbar sind. Wie du das feststellst, hängt stark von der Art des Spiels ab. Bei einem 2D-Spiel kann es so einfach sein, immer alle Spielobjekte außerhalb eines rechteckigen Bereichs zu deaktivieren. Du kannst das mit einem Physik-Trigger erkennen oder deine Objekte in Gruppen aufteilen. Sobald du weißt, welche Objekte du deaktivieren oder aktivieren möchtest, sendest du dazu eine Nachricht `disable` oder `enable` an jedes Spielobjekt.

## Aussondern von Geometrie außerhalb des Sichtvolumens {#frustum-culling}
Das Render-Skript kann Komponenten von Spielobjekten, die sich außerhalb einer festgelegten Begrenzungsbox (Sichtvolumen, frustum) befinden, automatisch vom Rendering ausschließen. Erfahre mehr über das Aussondern von Geometrie außerhalb des Sichtvolumens (Frustum Culling) im [Handbuch zur Rendering-Pipeline](/manuals/render/#frustum-culling).

# Plattformspezifische Optimierungen {#platform-specific-optimizations}

## Android Device Performance Framework
Das Android Dynamic Performance Framework ist eine Sammlung von APIs, mit denen Spiele direkter mit den Systemen für Energie- und Temperaturverwaltung von Android-Geräten interagieren können. Damit lässt sich das dynamische Verhalten auf Android-Systemen überwachen und die Spielleistung auf einem dauerhaft tragbaren Niveau optimieren, ohne dass Geräte überhitzen. Verwende die [Erweiterung Android Dynamic Performance Framework](https://defold.com/extension-adpf/), um die Leistung deines Defold-Spiels auf Android-Geräten zu überwachen und zu optimieren.
