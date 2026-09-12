---
title: Plattformspiel-Tutorial für Defold
brief: In diesem Artikel gehst du die Implementierung eines einfachen kachelbasierten 2D-Plattformspiels in Defold durch. Du lernst die Mechaniken für die Bewegung nach links und rechts, das Springen und das Fallen kennen.
---

# Plattformspiel {#platformer}

In diesem Artikel gehen wir die Implementierung eines einfachen kachelbasierten 2D-Plattformspiels in Defold durch. Wir lernen die Mechaniken für die Bewegung nach links und rechts, das Springen und das Fallen kennen.

Es gibt viele verschiedene Möglichkeiten, ein Plattformspiel zu erstellen. Rodrigo Monteiro hat [hier](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/) eine ausführliche Analyse zu diesem Thema und weiteren Aspekten geschrieben.

Wir empfehlen dir sehr, sie zu lesen, wenn du noch keine Erfahrung mit der Entwicklung von Plattformspielen hast, denn sie enthält viele wertvolle Informationen. Wir werden einige der beschriebenen Methoden und ihre Implementierung in Defold etwas genauer betrachten. Alles sollte sich jedoch leicht auf andere Plattformen und Sprachen übertragen lassen (in Defold verwenden wir Lua).

Wir gehen davon aus, dass du dich ein wenig mit Vektorrechnung (linearer Algebra) auskennst. Falls nicht, solltest du dich damit beschäftigen, denn sie ist für die Spieleentwicklung unglaublich nützlich. David Rosen von Wolfire hat [hier](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/) eine sehr gute Artikelreihe dazu geschrieben.

Wenn du Defold bereits verwendest, kannst du ein neues Projekt auf Grundlage der Projektvorlage _Platformer_ erstellen und damit experimentieren, während du diesen Artikel liest.

::: sidenote
Einige Leser haben darauf hingewiesen, dass unsere vorgeschlagene Methode mit der Standardimplementierung von Box2D nicht möglich ist. Wir haben ein paar Änderungen an Box2D vorgenommen, damit sie funktioniert:

Kollisionen zwischen kinematischen und statischen Objekten werden ignoriert. Ändere die Prüfungen in `b2Body::ShouldCollide` und `b2ContactManager::Collide`.

Außerdem wird der Kontaktabstand (in Box2D als separation bezeichnet) nicht an die Callback-Funktion übergeben.
Füge `b2ManifoldPoint` ein Abstandsfeld hinzu und stelle sicher, dass es in den Funktionen `b2Collide*` aktualisiert wird.
:::

## Kollisionserkennung {#collision-detection}

Die Kollisionserkennung wird benötigt, damit sich die Spielfigur nicht durch die Levelgeometrie bewegt.
Je nach deinem Spiel und seinen spezifischen Anforderungen gibt es verschiedene Möglichkeiten, dies zu lösen.
Eine der einfachsten Möglichkeiten besteht darin, diese Aufgabe nach Möglichkeit einer Physik-Engine zu überlassen.
In Defold verwenden wir für 2D-Spiele die Physik-Engine [Box2D](http://box2d.org/).
Die Standardimplementierung von Box2D bietet nicht alle benötigten Funktionen. Am Ende dieses Artikels erfährst du, wie wir sie angepasst haben.

Eine Physik-Engine speichert die Zustände der Physikobjekte zusammen mit ihren Formen, um physikalisches Verhalten zu simulieren. Während der Simulation meldet sie außerdem Kollisionen, damit das Spiel auf sie reagieren kann, sobald sie auftreten. In den meisten Physik-Engines gibt es drei Arten von Objekten: _statische_ (static), _dynamische_ (dynamic) und _kinematische_ (kinematic) Objekte (diese Namen können in anderen Physik-Engines abweichen). Es gibt noch weitere Arten von Objekten, aber die lassen wir vorerst außer Acht.

- Ein *statisches* Objekt bewegt sich niemals (z. B. die Levelgeometrie).
- Ein *dynamisches* Objekt wird von Kräften und Drehmomenten beeinflusst, die während der Simulation in Geschwindigkeiten umgewandelt werden.
- Ein *kinematisches* Objekt wird von der Anwendungslogik gesteuert, beeinflusst aber trotzdem andere dynamische Objekte.

In einem Spiel wie diesem wollen wir ein Verhalten, das dem physikalischen Verhalten in der realen Welt ähnelt. Eine reaktionsschnelle Steuerung und ausgewogene Mechaniken sind jedoch viel wichtiger. Ein Sprung, der sich gut anfühlt, muss weder physikalisch korrekt sein noch der Schwerkraft der realen Welt unterliegen. [Diese](http://hypertextbook.com/facts/2007/mariogravity.shtml) Analyse zeigt allerdings, dass die Schwerkraft in Mario-Spielen mit jeder Version näher an 9,8 m/s<sup>2</sup> heranrückt. :-)

Es ist wichtig, dass wir die volle Kontrolle über das Geschehen haben, damit wir die Mechaniken so gestalten und anpassen können, dass das gewünschte Spielerlebnis entsteht. Deshalb entscheiden wir uns dafür, die Spielfigur als kinematisches Objekt zu modellieren. So können wir die Spielfigur nach Belieben bewegen, ohne uns mit physikalischen Kräften beschäftigen zu müssen. Das bedeutet, dass wir Überschneidungen zwischen der Spielfigur und der Levelgeometrie selbst auflösen müssen (mehr dazu später), aber diesen Nachteil nehmen wir in Kauf. Wir stellen die Spielfigur in der Physikwelt durch eine Rechteckform dar.

## Bewegung {#movement}

Nachdem wir entschieden haben, die Spielfigur als kinematisches Objekt darzustellen, können wir sie durch das Setzen ihrer Position frei bewegen. Beginnen wir mit der Bewegung nach links und rechts.

Die Bewegung soll auf Beschleunigung beruhen, damit die Figur ein Gefühl von Gewicht vermittelt. Wie bei einem normalen Fahrzeug bestimmt die Beschleunigung, wie schnell die Spielfigur ihre Höchstgeschwindigkeit erreichen und die Richtung wechseln kann. Die Beschleunigung wirkt über den Zeitschritt des Frames---üblicherweise im Parameter `dt` (Delta-`t`) angegeben---und wird dann zur Geschwindigkeit addiert. Ebenso wirkt die Geschwindigkeit über den Frame, und die daraus resultierende Verschiebung wird zur Position addiert. In der Mathematik nennt man dies [Integration über die Zeit](http://en.wikipedia.org/wiki/Integral).

![Näherungsweise Integration der Geschwindigkeit](images/platformer/integration.png)

Die beiden senkrechten Linien markieren den Anfang und das Ende des Frames. Die Höhe der Linien entspricht der Geschwindigkeit, die die Spielfigur zu diesen beiden Zeitpunkten hat. Nennen wir diese Geschwindigkeiten `v0` und `v1`. `v1` ergibt sich, indem die Beschleunigung (die Steigung der Kurve) über den Zeitschritt `dt` angewendet wird:

![Gleichung der Geschwindigkeit](images/platformer/equationofvelocity.png)

Die orange Fläche entspricht der Verschiebung, die wir während des aktuellen Frames auf die Spielfigur anwenden sollen. Geometrisch können wir die Fläche wie folgt annähern:

![Gleichung der Verschiebung](images/platformer/equationoftranslation.png)

So integrieren wir die Beschleunigung und Geschwindigkeit, um die Figur in der Aktualisierungsschleife zu bewegen:

1. Bestimme die Zielgeschwindigkeit anhand der Eingabe
2. Berechne die Differenz zwischen unserer aktuellen Geschwindigkeit und der Zielgeschwindigkeit
3. Richte die Beschleunigung so aus, dass sie in Richtung der Differenz wirkt
4. Berechne die Geschwindigkeitsänderung für diesen Frame (`dv` steht für Delta-Geschwindigkeit), wie oben gezeigt:

    ```lua
    local dv = acceleration * dt
    ```

5. Prüfe, ob `dv` die beabsichtigte Geschwindigkeitsdifferenz überschreitet, und begrenze den Wert in diesem Fall
6. Speichere die aktuelle Geschwindigkeit zur späteren Verwendung (`self.velocity`, die derzeit noch die im vorherigen Frame verwendete Geschwindigkeit enthält):

    ```lua
    local v0 = self.velocity
    ```

7. Berechne die neue Geschwindigkeit, indem du die Geschwindigkeitsänderung addierst:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Berechne die Verschiebung in x-Richtung für diesen Frame durch Integration der Geschwindigkeit, wie oben gezeigt:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Wende sie auf die Spielfigur an

Wenn du dir nicht sicher bist, wie du Eingaben in Defold verarbeitest, findest du [hier](/manuals/input) eine Anleitung dazu.

Jetzt können wir die Figur nach links und rechts bewegen, und die Steuerung fühlt sich gewichtig und flüssig an. Fügen wir nun die Schwerkraft hinzu!

Schwerkraft ist ebenfalls eine Beschleunigung, wirkt aber entlang der y-Achse auf die Spielfigur. Sie wird also genauso angewendet wie die oben beschriebene Bewegungsbeschleunigung. Wenn wir die obigen Berechnungen auf Vektoren umstellen und dafür sorgen, dass wir in Schritt 3) die Schwerkraft in die y-Komponente der Beschleunigung aufnehmen, funktioniert es bereits. Vektorrechnung muss man einfach lieben! :-)

## Kollisionsreaktion {#collision-response}

Unsere Spielfigur kann sich jetzt bewegen und fallen. Es ist also an der Zeit, uns die Kollisionsreaktionen anzusehen.
Natürlich müssen wir auf der Levelgeometrie landen und uns an ihr entlangbewegen können. Wir verwenden die von der Physik-Engine bereitgestellten Kontaktpunkte, um sicherzustellen, dass wir niemals etwas überlappen.

Ein Kontaktpunkt enthält eine _Normale_ des Kontakts (sie zeigt aus dem Objekt heraus, mit dem wir kollidieren; in anderen Engines kann dies anders sein) sowie einen _Abstand_, der angibt, wie weit wir in das andere Objekt eingedrungen sind. Das ist alles, was wir brauchen, um die Spielfigur von der Levelgeometrie zu trennen.
Da wir ein Rechteck verwenden, können wir innerhalb eines Frames mehrere Kontaktpunkte erhalten. Das passiert zum Beispiel, wenn zwei Ecken des Rechtecks in den waagerechten Boden eindringen oder sich die Spielfigur in eine Ecke bewegt.

![Kontaktnormalen, die auf die Spielfigur wirken](images/platformer/collision.png)

Damit wir dieselbe Korrektur nicht mehrfach vornehmen, sammeln wir die Korrekturen in einem Vektor und stellen so sicher, dass wir nicht überkompensieren. Sonst wären wir am Ende zu weit von dem Objekt entfernt, mit dem wir kollidiert sind. Im Bild oben siehst du, dass wir derzeit zwei Kontaktpunkte haben, die durch die beiden Pfeile (Normalen) dargestellt werden. Die Eindringtiefe ist bei beiden Kontakten gleich. Würden wir sie jedes Mal ungeprüft verwenden, würden wir die Spielfigur am Ende um das Doppelte des beabsichtigten Betrags verschieben.

::: sidenote
Es ist wichtig, die gesammelten Korrekturen in jedem Frame auf den Nullvektor zurückzusetzen.
Füge dazu etwa Folgendes am Ende der Funktion `update()` ein:
`self.corrections = vmath.vector3()`
:::

Wenn es eine Callback-Funktion gibt, die für jeden Kontaktpunkt aufgerufen wird, können wir die Trennung in dieser Funktion so durchführen:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Projiziere den Korrekturvektor auf die Kontaktnormale (beim ersten Kontaktpunkt ist der Korrekturvektor der Nullvektor)
2. Berechne die Kompensation, die wir für diesen Kontaktpunkt vornehmen müssen
3. Addiere sie zum Korrekturvektor
4. Wende die Kompensation auf die Spielfigur an

Wir müssen außerdem den Anteil der Geschwindigkeit der Spielfigur aufheben, der zum Kontaktpunkt hin gerichtet ist:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Projiziere die Geschwindigkeit auf die Normale
2. Wenn die Projektion negativ ist, bedeutet das, dass ein Teil der Geschwindigkeit zum Kontaktpunkt hin gerichtet ist; entferne in diesem Fall diese Komponente

## Springen {#jumping}

Da wir jetzt auf der Levelgeometrie laufen und herunterfallen können, ist es Zeit zu springen! Sprünge in Plattformspielen lassen sich auf viele verschiedene Arten umsetzen. In diesem Spiel streben wir etwas Ähnliches wie in Super Mario Bros und Super Meat Boy an. Beim Springen wird die Spielfigur durch einen Impuls nach oben gestoßen, der im Grunde eine feste Geschwindigkeit ist.

Die Schwerkraft zieht die Figur fortlaufend wieder nach unten, wodurch eine schöne Sprungkurve entsteht. Während die Figur in der Luft ist, kann der Spieler sie weiterhin steuern. Lässt der Spieler die Sprungtaste vor dem höchsten Punkt der Sprungkurve los, wird die Aufwärtsgeschwindigkeit verringert, um den Sprung vorzeitig zu beenden.

1. Wenn die Eingabe gedrückt wird, führe Folgendes aus:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Dies sollte nur geschehen, wenn die Eingabe _gedrückt_ wird, und nicht in jedem Frame, in dem sie weiterhin _gedrückt gehalten_ wird.

2. Wenn die Eingabe losgelassen wird, führe Folgendes aus:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike hat einige schöne Diagramme der Sprungkurven in [Super Mario Bros 3](http://meyermike.com/wp/?p=175) und [Super Meat Boy](http://meyermike.com/wp/?p=160) erstellt, die einen Blick wert sind.

## Levelgeometrie {#level-geometry}

Die Levelgeometrie besteht aus den Kollisionsformen der Umgebung, mit denen die Spielfigur (und möglicherweise andere Dinge) kollidiert. In Defold gibt es zwei Möglichkeiten, diese Geometrie zu erstellen.

Du kannst separate Kollisionsformen über den von dir erstellten Levels anlegen. Diese Methode ist sehr flexibel und ermöglicht eine genaue Positionierung der Grafiken. Sie ist besonders nützlich, wenn du sanfte Schrägen möchtest.
Das Spiel [Braid](http://braid-game.com/) hat diese Methode zum Aufbau von Levels verwendet. Auch das Beispiellevel in diesem Tutorial wurde damit erstellt. So sieht es im Defold-Editor aus:

![Der Defold-Editor mit der Levelgeometrie und der in der Welt platzierten Spielfigur](images/platformer/editor.png)

Eine weitere Möglichkeit besteht darin, Levels aus Kacheln aufzubauen und den Editor die Physikformen automatisch anhand der Kachelgrafiken erzeugen zu lassen. Das bedeutet, dass die Levelgeometrie automatisch aktualisiert wird, wenn du die Levels änderst, was äußerst nützlich sein kann.

Die Physikformen der platzierten Kacheln werden automatisch zu einer einzigen Form zusammengeführt, wenn sie aneinander anschließen.
Dadurch entfallen Lücken, an denen deine Spielfigur hängen bleiben oder anstoßen könnte, wenn sie über mehrere waagerechte Kacheln gleitet. Dazu werden die Kachelpolygone beim Laden durch Kantenformen in Box2D ersetzt.

![Mehrere kachelbasierte Polygone zu einem einzigen verbunden](images/platformer/stitching.png)

Oben siehst du ein Beispiel, in dem wir fünf benachbarte Kacheln aus einem Teil der Plattformspielgrafik erstellt haben. Im Bild kannst du sehen, wie die platzierten Kacheln (oben) einer einzigen zusammengefügten Form entsprechen (graue Kontur unten).

Weitere Informationen findest du in unseren Anleitungen zu [Physik](/manuals/physics) und [Kacheln](/manuals/2dgraphics).

## Abschließende Worte {#final-words}

Wenn du mehr über die Mechaniken von Plattformspielen erfahren möchtest, findest du hier eine beeindruckend große Menge an Informationen über die Physik in [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Wenn du unser Vorlagenprojekt auf einem iOS-Gerät oder mit einer Maus ausprobierst, kann sich das Springen ziemlich unbeholfen anfühlen.
Das ist nur unser schwacher Versuch, ein Plattformspiel mit einer einzigen Berührung zu steuern. :-)

Wir haben nicht darüber gesprochen, wie wir die Animationen in diesem Spiel umgesetzt haben. Du kannst dir einen Eindruck davon verschaffen, indem du dir *player.script* unten ansiehst. Suche nach der Funktion `update_animations()`.

Wir hoffen, dass diese Informationen für dich nützlich waren!
Bitte entwickle ein großartiges Plattformspiel, damit wir es alle spielen können! <3

## Code

Hier ist der Inhalt von *player.script*:

```lua
-- player.script

-- these are the tweaks for the mechanics, feel free to change them for a different feeling
-- the acceleration to move right/left
local move_acceleration = 3500
-- acceleration factor to use when air-borne
local air_acceleration_factor = 0.8
-- max speed right/left
local max_speed = 450
-- gravity pulling the player down in pixel units
local gravity = -1000
-- take-off speed when jumping in pixel units
local jump_takeoff_speed = 550
-- time within a double tap must occur to be considered a jump (only used for mouse/touch controls)
local touch_jump_timeout = 0.2

-- prehashing ids improves performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- this lets us handle input in this script
    msg.post(".", "acquire_input_focus")

    -- initial player velocity
    self.velocity = vmath.vector3(0, 0, 0)
    -- support variable to keep track of collisions and separation
    self.correction = vmath.vector3()
    -- if the player stands on ground or not
    self.ground_contact = false
    -- movement input in the range [-1,1]
    self.move_input = 0
    -- the currently playing animation
    self.anim = nil
    -- timer that controls the jump-window when using mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- only play animations which are not already playing
    if self.anim ~= anim then
        -- tell the sprite to play the animation
        sprite.play_flipbook("#sprite", anim)
        -- remember which animation is playing
        self.anim = anim
    end
end

local function update_animations(self)
    -- make sure the player character faces the right way
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- make sure the right animation is playing
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determine the target speed based on input
    local target_speed = self.move_input * max_speed
    -- calculate the difference between our current speed and the target speed
    local speed_diff = target_speed - self.velocity.x
    -- the complete acceleration to integrate over this frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- set the acceleration to work in the direction of the difference
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- decrease the acceleration when air-borne to give a slower feel
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calculate the velocity change this frame (dv is short for delta-velocity)
    local dv = acceleration * dt
    -- check if dv exceeds the intended speed difference, clamp it in that case
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- save the current velocity for later use
    -- (self.velocity, which right now is the velocity used the previous frame)
    local v0 = self.velocity
    -- calculate the new velocity by adding the velocity change
    self.velocity = self.velocity + dv
    -- calculate the translation this frame by integrating the velocity
    local dp = (v0 + self.velocity) * dt * 0.5
    -- apply it to the player character
    go.set_position(go.get_position() + dp)

    -- update the jump timer
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- check if we received a contact point message
    if message_id == msg_contact_point_response then
        -- check that the object is something we consider an obstacle
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    -- (extend this with a counter to do things like double-jumps)
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
        -- play animation
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move towards the touch-point
        local diff = action.x - go.get_position().x
        -- only give input when far away (more than 10 pixels)
        if math.abs(diff) > 10 then
            -- slow down when less than 100 pixels away
            self.move_input = diff / 100
            -- clamp input to [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- start timing the last release to see if we are about to jump
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- jump on double tap
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
