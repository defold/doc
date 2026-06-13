---
title: Eventos de colisión en Defold
brief: El manejo de eventos de colisión puede centralizarse usando `physics.set_event_listener()` para dirigir todos los mensajes de colisión e interacción a una única función especificada.
---

# Manejo de eventos de físicas en Defold

Defold ofrece manejo centralizado de eventos de físicas mediante la función `physics.set_event_listener()`. Esta función te permite definir un listener personalizado para manejar todos los eventos de interacción de físicas en un solo lugar, lo que simplifica tu código y mejora la eficiencia.

## Definir el listener del mundo de físicas

En Defold, cada proxy de colección crea su propio mundo de físicas separado. Por lo tanto, cuando trabajas con varios proxies de colección, es esencial gestionar los distintos mundos de físicas asociados con cada uno. Para asegurar que los eventos de físicas se manejen correctamente en cada mundo, debes definir un listener de mundo de físicas específicamente para el mundo de cada proxy de colección.

Esta configuración significa que el listener de eventos de físicas debe definirse desde el contexto de la colección que representa el proxy. Al hacerlo, asocias el listener directamente con el mundo de físicas correspondiente, lo que permite que procese los eventos de físicas con precisión.

Este es un ejemplo de cómo definir un listener de mundo de físicas dentro de un proxy de colección:

```lua
function init(self)
    -- Asumiendo que este script está adjunto a un objeto de juego dentro de la colección cargada por el proxy
    -- Definir el listener de mundo de físicas para el mundo de físicas de este proxy de colección
    physics.set_event_listener(physics_world_listener)
end
```

Al implementar este método, aseguras que cada mundo de físicas generado por un proxy de colección tenga su listener dedicado. Esto es fundamental para manejar eventos de físicas de manera eficaz en proyectos que usan varios proxies de colección.

::: important
Si se define un listener, los [mensajes de físicas](/manuals/physics-messages) ya no se enviarán para el mundo de físicas donde está definido este listener.
:::

## Estructura de datos de eventos

Cada evento de físicas proporciona una tabla `data` que contiene información específica relevante para el evento.

1. **Evento de punto de contacto (`contact_point_event`):**
Este evento informa de un punto de contacto entre dos objetos de colisión. Es útil para un manejo detallado de colisiones, como calcular fuerzas de impacto o respuestas de colisión personalizadas.

   - `applied_impulse`: El impulso resultante del contacto.
   - `distance`: La distancia de penetración entre los objetos.
   - `a` y `b`: Objetos que representan las entidades que colisionan, cada uno con:
     - `position`: Posición en el mundo del punto de contacto (`vector3`).
     - `instance_position`: Posición en el mundo de la instancia del objeto de juego (`vector3`).
     - `id`: ID de instancia (`hash`).
     - `group`: Grupo de colisión (`hash`).
     - `relative_velocity`: Velocidad relativa al otro objeto (`vector3`).
     - `mass`: Masa en kilogramos (`number`).
     - `normal`: Normal de contacto, apuntando desde el otro objeto (`vector3`).

2. **Evento de colisión (`collision_event`):**
Este evento indica que ha ocurrido una colisión entre dos objetos. Es un evento más general que el evento de punto de contacto, ideal para detectar colisiones sin necesitar información detallada sobre los puntos de contacto.

   - `a` y `b`: Objetos que representan las entidades que colisionan, cada uno con:
     - `position`: Posición en el mundo (`vector3`).
     - `id`: ID de instancia (`hash`).
     - `group`: Grupo de colisión (`hash`).

3. **Evento de trigger (`trigger_event`):**
Este evento se envía cuando un objeto interactúa con un objeto trigger. Es útil para crear áreas en tu juego que hacen que ocurra algo cuando un objeto entra o sale.

   - `enter`: Indica si la interacción fue una entrada (`true`) o una salida (`false`).
   - `a` y `b`: Objetos involucrados en el evento de trigger, cada uno con:
     - `id`: ID de instancia (`hash`).
     - `group`: Grupo de colisión (`hash`).

4. **Respuesta de ray cast (`ray_cast_response`):**
Este evento se envía como respuesta a un ray cast y proporciona información sobre el objeto impactado por el rayo.

   - `group`: Grupo de colisión del objeto impactado (`hash`).
   - `request_id`: Identificador de la solicitud de ray cast (`number`).
   - `position`: Posición del impacto (`vector3`).
   - `fraction`: La fracción de la longitud del rayo en la que ocurrió el impacto (`number`).
   - `normal`: Normal en la posición del impacto (`vector3`).
   - `id`: ID de instancia del objeto impactado (`hash`).

5. **Ray cast sin impacto (`ray_cast_missed`):**
Este evento se envía cuando un ray cast no impacta ningún objeto.

   - `request_id`: Identificador de la solicitud de ray cast que no impactó (`number`).

## Ejemplo de uso

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Manejar datos detallados del punto de contacto
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Manejar datos generales de colisión
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Manejar datos de interacción de trigger
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Manejar datos de impacto de ray cast
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Manejar datos de ray cast sin impacto
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Limitaciones

El listener se llama de forma síncrona en el momento en que ocurre el evento. Esto sucede en medio de un timestep, lo que significa que el mundo de físicas está bloqueado. Por eso no es posible usar funciones que puedan afectar las simulaciones del mundo de físicas, por ejemplo `physics.create_joint()`.

Este es un pequeño ejemplo de cómo evitar estas limitaciones:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- rellenar el mensaje de la misma forma en que se deberían pasar los argumentos a `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- enviar el mensaje al propio objeto
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- desempaquetar el mensaje con argumentos de función
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
