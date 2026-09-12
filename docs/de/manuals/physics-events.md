---
title: Kollisionsereignisse in Defold
brief: Die Verarbeitung von Kollisionsereignissen lässt sich mit `physics.set_event_listener()` zentralisieren, indem alle Kollisions- und Interaktionsnachrichten an eine einzelne festgelegte Funktion geleitet werden.
---

# Verarbeitung von Physikereignissen in Defold {#defold-physics-event-handling}

Defold bietet mit der Funktion `physics.set_event_listener()` eine zentrale Verarbeitung von Physikereignissen. Mit dieser Funktion kannst du einen benutzerdefinierten Listener festlegen, der alle Ereignisse physikalischer Interaktionen an einer Stelle verarbeitet. Dadurch wird dein Code übersichtlicher und effizienter.

## Den Listener für die Physikwelt festlegen {#setting-the-physics-world-listener}

In Defold erstellt jeder Sammlungs-Proxy (collection proxy) seine eigene separate Physikwelt. Wenn du mit mehreren Sammlungs-Proxys arbeitest, musst du daher die verschiedenen Physikwelten verwalten, die ihnen jeweils zugeordnet sind. Damit Physikereignisse in jeder Welt korrekt verarbeitet werden, musst du für die Welt jedes Sammlungs-Proxys einen eigenen Listener für die Physikwelt festlegen.

Das bedeutet, dass der Listener für Physikereignisse innerhalb des Kontexts der Sammlung (collection) festgelegt werden muss, die der Proxy repräsentiert. Dadurch ordnest du den Listener direkt der entsprechenden Physikwelt zu, sodass er Physikereignisse korrekt verarbeiten kann.

Hier ist ein Beispiel dafür, wie du einen Listener für die Physikwelt innerhalb eines Sammlungs-Proxys festlegst:

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

Mit dieser Methode stellst du sicher, dass jede von einem Sammlungs-Proxy erzeugte Physikwelt ihren eigenen Listener hat. Das ist entscheidend, um Physikereignisse in Projekten mit mehreren Sammlungs-Proxys effektiv zu verarbeiten.

::: important
Wenn ein Listener festgelegt ist, werden für die Physikwelt, in der dieser Listener festgelegt ist, keine [Physiknachrichten](/manuals/physics-messages) mehr gesendet.
:::

## Datenstruktur der Ereignisse {#event-data-structure}

Der Listener wird mit `self` und einer Tabelle namens `events` aufgerufen. Die Tabelle `events` ist ein Array, das alle für den Callback gesammelten Physikereignisse enthält. Jeder Eintrag ist eine Ereignistabelle mit einem Feld namens `type`, das den Hashwert des Ereignisnamens enthält, sowie zusätzlichen Feldern, die für den jeweiligen Ereignistyp spezifisch sind.

Die Ereignistabellen enthalten die folgenden Daten:

1. **Kontaktpunktereignis (`contact_point_event`):**
Dieses Ereignis meldet einen Kontaktpunkt zwischen zwei Kollisionsobjekten (collision object). Es eignet sich für eine detaillierte Kollisionsverarbeitung, beispielsweise zur Berechnung von Aufprallkräften oder benutzerdefinierten Kollisionsreaktionen.

   - `applied_impulse`: Der aus dem Kontakt resultierende Impuls.
   - `distance`: Die Eindringtiefe zwischen den Objekten.
   - `a` und `b`: Objekte, die die kollidierenden Entitäten repräsentieren und jeweils Folgendes enthalten:
     - `position`: Weltposition des Kontaktpunkts (vector3).
     - `instance_position`: Weltposition der Instanz eines Spielobjekts (game object) (vector3).
     - `id`: Instanz-ID (hash).
     - `group`: Kollisionsgruppe (hash).
     - `relative_velocity`: Geschwindigkeit relativ zum anderen Objekt (vector3).
     - `mass`: Masse in Kilogramm (number).
     - `normal`: Kontaktnormale, die vom anderen Objekt weg zeigt (vector3).

2. **Kollisionsereignis (`collision_event`):**
Dieses Ereignis zeigt an, dass eine Kollision zwischen zwei Objekten stattgefunden hat. Es ist allgemeiner als das Kontaktpunktereignis und eignet sich ideal zum Erkennen von Kollisionen, wenn keine detaillierten Informationen zu den Kontaktpunkten benötigt werden.

   - `a` und `b`: Objekte, die die kollidierenden Entitäten repräsentieren und jeweils Folgendes enthalten:
     - `position`: Weltposition (vector3).
     - `id`: Instanz-ID (hash).
     - `group`: Kollisionsgruppe (hash).

3. **Trigger-Ereignis (`trigger_event`):** 
Dieses Ereignis wird gesendet, wenn ein Objekt mit einem Trigger-Objekt interagiert. Es eignet sich dazu, Bereiche in deinem Spiel zu erstellen, die etwas auslösen, wenn ein Objekt sie betritt oder verlässt.

   - `enter`: Gibt an, ob es sich bei der Interaktion um einen Eintritt (true) oder einen Austritt (false) handelt.
   - `a` und `b`: Am Trigger-Ereignis beteiligte Objekte, die jeweils Folgendes enthalten:
     - `id`: Instanz-ID (hash).
     - `group`: Kollisionsgruppe (hash).

4. **Antwort auf eine Strahlabfrage (`ray_cast_response`):**
Dieses Ereignis wird als Antwort auf eine Strahlabfrage (raycast) gesendet und liefert Informationen über das vom Strahl getroffene Objekt.

   - `group`: Kollisionsgruppe des getroffenen Objekts (hash).
   - `request_id`: Kennung der Strahlabfrage (number).
   - `position`: Trefferposition (vector3).
   - `fraction`: Der Anteil der Strahllänge, an dem der Treffer auftrat (number).
   - `normal`: Normale an der Trefferposition (vector3).
   - `id`: Instanz-ID des getroffenen Objekts (hash).

5. **Strahlabfrage ohne Treffer (`ray_cast_missed`):**
Dieses Ereignis wird gesendet, wenn eine Strahlabfrage kein Objekt trifft.

   - `request_id`: Kennung der Strahlabfrage, die kein Objekt getroffen hat (number).

## Anwendungsbeispiel {#example-usage}

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Einschränkungen {#limitations}

Der Listener wird synchron zum Zeitpunkt des Ereignisses aufgerufen. Das geschieht mitten in einem Zeitschritt, weshalb die Physikwelt gesperrt ist. Dadurch ist es nicht möglich, Funktionen zu verwenden, die die Simulationen der Physikwelt beeinflussen könnten, beispielsweise `physics.create_joint()`.

Hier ist ein kurzes Beispiel dafür, wie du diese Einschränkungen umgehen kannst:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
