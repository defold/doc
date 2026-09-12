---
title: Kinematische Kollisionen in Defold auflösen
brief: Dieses Handbuch erklärt, wie du kinematische Kollisionen in der Physiksimulation auflöst.
---

# Kinematische Kollisionen auflösen {#resolving-kinematic-collisions}

Wenn du kinematische Kollisionsobjekte (kinematic collision objects) verwendest, musst du Kollisionen selbst auflösen und die Objekte als Reaktion darauf bewegen. Eine naive Implementierung zum Trennen zweier kollidierender Objekte sieht so aus:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Dieser Code trennt dein kinematisches Kollisionsobjekt von anderen Physikobjekten, in die es eingedrungen ist. Die Verschiebung geht jedoch oft zu weit, sodass du in vielen Fällen ein Zittern siehst. Um das Problem besser zu verstehen, betrachte den folgenden Fall, in dem eine Spielfigur mit zwei Objekten, *A* und *B*, kollidiert ist:

![Physikalische Kollision](images/physics/collision_multi.png)

Die Physik-Engine sendet in dem Frame, in dem die Kollision auftritt, mehrere `"contact_point_response"`-Nachrichten: eine für Objekt *A* und eine für Objekt *B*. Wenn du die Figur als Reaktion auf jedes Eindringen bewegst, wie im naiven Code oben, ergibt sich folgende Trennung:

- Bewege die Figur entsprechend ihrer Eindringtiefe aus Objekt *A* heraus (der schwarze Pfeil)
- Bewege die Figur entsprechend ihrer Eindringtiefe aus Objekt *B* heraus (der schwarze Pfeil)

Die Reihenfolge ist beliebig, aber das Ergebnis ist in beiden Fällen gleich: eine Gesamtverschiebung, die der *Summe der einzelnen Eindringvektoren* entspricht:

![Naive Trennung bei einer Kollision](images/physics/separation_naive.png)

Um die Figur korrekt von den Objekten *A* und *B* zu trennen, musst du die Eindringtiefe jedes Kontaktpunkts verarbeiten und prüfen, ob vorherige Verschiebungen die Trennung bereits vollständig oder teilweise bewirkt haben.

Angenommen, die erste Kontaktpunktnachricht kommt von Objekt *A* und du bewegst die Figur um den Eindringvektor von *A* heraus:

![Trennung bei einer Kollision, Schritt 1](images/physics/separation_step1.png)

Dann ist die Figur bereits teilweise von *B* getrennt. Der schwarze Pfeil oben zeigt den noch nötigen Ausgleich für eine vollständige Trennung von Objekt *B*. Die Länge des Ausgleichsvektors lässt sich berechnen, indem du den Eindringvektor von *A* auf den Eindringvektor von *B* projizierst:

![Projektion](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

Den Ausgleichsvektor erhältst du, indem du die Länge von *B* um *l* verringerst. Um dies für eine beliebige Anzahl von Eindringungen zu berechnen, kannst du die nötige Korrektur in einem Vektor aufsummieren. Beginne mit einem Korrekturvektor der Länge null und führe für jeden Kontaktpunkt folgende Schritte aus:

1. Projiziere die aktuelle Korrektur auf den Eindringvektor des Kontakts.
2. Berechne, welcher Ausgleich des Eindringvektors noch nötig ist (gemäß der obigen Formel).
3. Bewege das Objekt um den Ausgleichsvektor.
4. Addiere den Ausgleich zur aufsummierten Korrektur.

Eine vollständige Implementierung sieht so aus:

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
