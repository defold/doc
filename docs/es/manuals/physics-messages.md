---
title: Mensajes de colisión en Defold
brief: Cuando dos objetos colisionan, el motor llamará al callback de eventos o transmitirá mensajes.
---

# Mensajes de colisión

Cuando dos objetos colisionan, el motor enviará un evento al callback de eventos o transmitirá mensajes a ambos objetos.

## Filtrado de eventos

Los tipos de eventos generados se pueden controlar mediante los indicadores de cada objeto:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Todos son `true` de forma predeterminada.
Cuando dos objetos de colisión interactúan, se comprueba si se debe enviar un mensaje al usuario, según estas casillas.

Por ejemplo, dadas las casillas "Generate Contact Events":

Al usar `physics.set_event_listener()`:

| Componente A | Componente B | Enviar mensaje |
|--------------|--------------|----------------|
| ✅︎           | ✅︎           | Sí             |
| ❌           | ✅︎           | Sí             |
| ✅︎           | ❌           | Sí             |
| ❌           | ❌           | No             |

Al usar el manejador de mensajes predeterminado:

| Componente A | Componente B | Enviar mensaje(s) |
|--------------|--------------|-------------------|
| ✅︎           | ✅︎           | Sí (A,B) + (B,A)  |
| ❌           | ✅︎           | Sí (B,A)          |
| ✅︎           | ❌           | Sí (A,B)          |
| ❌           | ❌           | No                |

## Respuesta de colisión

El mensaje `"collision_response"` se envía cuando uno de los objetos que colisionan es de tipo "dynamic", "kinematic" o "static". Tiene definidos los siguientes campos:

`other_id`
: el id de la instancia con la que colisionó el objeto de colisión (`hash`)

`other_position`
: la posición en el mundo de la instancia con la que colisionó el objeto de colisión (`vector3`)

`other_group`
: el grupo de colisión del otro objeto de colisión (`hash`)

`own_group`
: el grupo de colisión del objeto de colisión (`hash`)

El mensaje `"collision_response"` solo es adecuado para resolver colisiones donde no necesitas detalles sobre la intersección real de los objetos, por ejemplo si quieres detectar si una bala golpea a un enemigo. Solo se envía uno de estos mensajes por cada par de objetos que colisionan en cada frame.

```Lua
function on_message(self, message_id, message, sender)
    -- comprobar el mensaje
    if message_id == hash("collision_response") then
        -- realizar una acción
        print("I collided with", message.other_id)
    end
end
```

## Respuesta de punto de contacto

El mensaje `"contact_point_response"` se envía cuando uno de los objetos que colisionan es de tipo "dynamic" o "kinematic" y el otro es de tipo "dynamic", "kinematic" o "static". Tiene definidos los siguientes campos:

`position`
: posición en el mundo del punto de contacto (`vector3`).

`normal`
: normal en el espacio del mundo del punto de contacto, que apunta desde el otro objeto hacia el objeto actual (`vector3`).

`relative_velocity`
: la velocidad relativa del objeto de colisión observada desde el otro objeto (`vector3`).

`distance`
: la distancia de penetración entre los objetos; no negativa (`number`).

`applied_impulse`
: el impulso resultante del contacto (`number`).

`life_time`
: (*no se usa actualmente*) tiempo de vida del contacto (`number`).

`mass`
: la masa del objeto de colisión actual en kg (`number`).

`other_mass`
: la masa del otro objeto de colisión en kg (`number`).

`other_id`
: el id de la instancia con la que el objeto de colisión está en contacto (`hash`).

`other_position`
: la posición en el mundo del otro objeto de colisión (`vector3`).

`other_group`
: el grupo de colisión del otro objeto de colisión (`hash`).

`own_group`
: el grupo de colisión del objeto de colisión (`hash`).

Para un juego o aplicación donde necesitas separar objetos perfectamente, el mensaje `"contact_point_response"` te da toda la información que necesitas. Sin embargo, ten en cuenta que para cualquier par de colisión dado, se pueden recibir varios mensajes `"contact_point_response"` en cada frame, según la naturaleza de la colisión. Consulta [Resolver colisiones para más información](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- comprobar el mensaje
    if message_id == hash("contact_point_response") then
        -- realizar una acción
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Respuesta de trigger

El mensaje `"trigger_response"` se envía cuando uno de los objetos que colisionan es de tipo "trigger". El mensaje se enviará una vez cuando la colisión se detecte por primera vez y otra vez cuando los objetos ya no estén colisionando. Tiene los siguientes campos:

`other_id`
: el id de la instancia con la que colisionó el objeto de colisión (`hash`).

`enter`
: `true` si la interacción fue una entrada en el trigger, `false` si fue una salida. (`boolean`).

`other_group`
: el grupo de colisión del otro objeto de colisión (`hash`).

`own_group`
: el grupo de colisión del objeto de colisión (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- comprobar el mensaje
    if message_id == hash("trigger_response") then
        if message.enter then
            -- realizar una acción para la entrada
            print("I am now inside", message.other_id)
        else
            -- realizar una acción para la salida
            print("I am now outside", message.other_id)
        end
    end
end
```
