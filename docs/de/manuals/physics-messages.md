---
title: Kollisionsnachrichten in Defold
brief: Wenn zwei Objekte kollidieren, ruft die Engine den Ereignis-Callback auf oder sendet Nachrichten an alle betreffenden Empfänger.
---

# Kollisionsnachrichten {#collision-messages}

Wenn zwei Objekte kollidieren, sendet die Engine ein Ereignis an den Ereignis-Callback oder Nachrichten an beide Objekte.

## Ereignisfilterung {#event-filtering}

Die Arten der erzeugten Ereignisse lassen sich über die Optionen für jedes Objekt steuern:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Diese sind standardmäßig alle `true`.
Wenn zwei Kollisionsobjekte (collision objects) miteinander interagieren, prüft die Engine anhand dieser Kontrollkästchen, ob sie dir eine Nachricht senden soll.

Am Beispiel der Kontrollkästchen "Generate Contact Events":

Bei Verwendung von `physics.set_event_listener()`:

| Komponente (component) A | Komponente B | Nachricht senden |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Ja           |
| ❌          | ✅︎          | Ja           |
| ✅︎          | ❌          | Ja           |
| ❌          | ❌          | Nein         |

Bei Verwendung des standardmäßigen Nachrichtenhandlers:

| Komponente A | Komponente B | Nachricht(en) senden |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Ja (A,B) + (B,A)  |
| ❌          | ✅︎          | Ja (B,A)          |
| ✅︎          | ❌          | Ja (A,B)          |
| ❌          | ❌          | Nein              |

## Kollisionsreaktion {#collision-response}

Die Nachricht `"collision_response"` wird gesendet, wenn eines der kollidierenden Objekte vom Typ "dynamic", "kinematic" oder "static" ist. Dabei sind die folgenden Felder gesetzt:

`other_id`
: der Bezeichner der Instanz, mit der das Kollisionsobjekt kollidiert ist (`hash`)

`other_position`
: die Weltposition der Instanz, mit der das Kollisionsobjekt kollidiert ist (`vector3`)

`other_group`
: die Kollisionsgruppe des anderen Kollisionsobjekts (`hash`)

`own_group`
: die Kollisionsgruppe des Kollisionsobjekts (`hash`)

Die Nachricht `collision_response` eignet sich nur zum Auflösen von Kollisionen, bei denen du keine Einzelheiten zur tatsächlichen Überschneidung der Objekte benötigst, zum Beispiel wenn du erkennen möchtest, ob ein Geschoss einen Gegner trifft. Für jedes kollidierende Objektpaar wird pro Frame nur eine dieser Nachrichten gesendet.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Kontaktpunktreaktion {#contact-point-response}

Die Nachricht `"contact_point_response"` wird gesendet, wenn eines der kollidierenden Objekte vom Typ "dynamic" oder "kinematic" und das andere vom Typ "dynamic", "kinematic" oder "static" ist. Dabei sind die folgenden Felder gesetzt:

`position`
: die Weltposition des Kontaktpunkts (`vector3`).

`normal`
: die Normale des Kontaktpunkts in Weltkoordinaten, die vom anderen Objekt zum aktuellen Objekt zeigt (`vector3`).

`relative_velocity`
: die relative Geschwindigkeit des Kollisionsobjekts aus Sicht des anderen Objekts (`vector3`).

`distance`
: die Eindringtiefe zwischen den Objekten -- nicht negativ (`number`).

`applied_impulse`
: der Impuls, der sich aus dem Kontakt ergeben hat (`number`).

`life_time`
: (*wird derzeit nicht verwendet!*) die Lebensdauer des Kontakts (`number`).

`mass`
: die Masse des aktuellen Kollisionsobjekts in kg (`number`).

`other_mass`
: die Masse des anderen Kollisionsobjekts in kg (`number`).

`other_id`
: der Bezeichner der Instanz, mit der das Kollisionsobjekt in Kontakt steht (`hash`).

`other_position`
: die Weltposition des anderen Kollisionsobjekts (`vector3`).

`other_group`
: die Kollisionsgruppe des anderen Kollisionsobjekts (`hash`).

`own_group`
: die Kollisionsgruppe des Kollisionsobjekts (`hash`).

Für ein Spiel oder eine Anwendung, in der du Objekte exakt voneinander trennen musst, liefert dir die Nachricht `"contact_point_response"` alle benötigten Informationen. Beachte jedoch, dass für ein bestimmtes kollidierendes Objektpaar je nach Art der Kollision mehrere Nachrichten vom Typ `"contact_point_response"` pro Frame empfangen werden können. Weitere Informationen findest du unter [Kollisionen auflösen](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Triggerreaktion {#trigger-response}

Die Nachricht `"trigger_response"` wird gesendet, wenn eines der kollidierenden Objekte vom Typ "trigger" ist. Die Nachricht wird einmal gesendet, wenn die Kollision erstmals erkannt wird, und ein weiteres Mal, wenn die Objekte nicht mehr kollidieren. Sie enthält die folgenden Felder:

`other_id`
: der Bezeichner der Instanz, mit der das Kollisionsobjekt kollidiert ist (`hash`).

`enter`
: `true`, wenn die Interaktion ein Eintritt in den Trigger war, und `false`, wenn es ein Austritt war. (`boolean`).

`other_group`
: die Kollisionsgruppe des anderen Kollisionsobjekts (`hash`).

`own_group`
: die Kollisionsgruppe des Kollisionsobjekts (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
