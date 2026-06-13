---
title: Manual del componente factory
brief: Este manual explica cómo usar componentes factory para generar objetos de juego dinámicamente en tiempo de ejecución.
---

# Componentes factory

Los componentes factory se usan para generar dinámicamente objetos de juego desde un conjunto de objetos en un juego en ejecución.

Cuando agregas un componente factory a un objeto de juego, especificas en la propiedad *Prototype* qué archivo de objeto de juego debe usar la factory como prototipo (también conocido como "prefabs" o "blueprints" en otros motores) para todos los objetos de juego nuevos que crea.

![Componente factory](images/factory/factory_collection.png)

![Componente factory](images/factory/factory_component.png)

Para activar la creación de un objeto de juego, llama a `factory.create()`:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Objeto de juego generado](images/factory/factory_spawned.png)

`factory.create()` toma 5 parámetros:

`url`
: El id del componente factory que debe generar un nuevo objeto de juego.

`[position]`
: (opcional) La posición en el mundo del nuevo objeto de juego. Debe ser un `vector3`. Si no especificas una posición, el objeto de juego se genera en la posición del objeto de juego que llama a `factory.create()`.

`[rotation]`
: (opcional) La rotación en el mundo del nuevo objeto de juego. Debe ser un `quat`.

`[properties]`
: (opcional) Una tabla Lua con cualquier valor de propiedad de script con el que iniciar el objeto de juego. Consulta el [manual de propiedades de script](/manuals/script-properties) para obtener información sobre las propiedades de script.

`[scale]`
: (opcional) La escala del objeto de juego generado. La escala puede expresarse como un `number` (mayor que 0) que especifica un escalado uniforme a lo largo de todos los ejes. También puedes proporcionar un `vector3` donde cada componente especifica el escalado a lo largo del eje correspondiente.

Por ejemplo:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Genera sin rotación pero con escala doble.
-- Define la propiedad score de la estrella en 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Define la propiedad de script "score" del objeto de juego de la estrella.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. La propiedad de script "score" se define con un valor predeterminado.
2. Referencia la propiedad de script "score" como un valor almacenado en "self".

![Objeto de juego generado con propiedad y escalado](images/factory/factory_spawned2.png)

::: sidenote
Actualmente Defold no admite el escalado no uniforme de formas de colisión. Si proporcionas un valor de escala no uniforme, por ejemplo `vmath.vector3(1.0, 2.0, 1.0)`, el sprite se escalará correctamente, pero las formas de colisión no.
:::


## Direccionamiento de objetos creados por factory

El mecanismo de direccionamiento de Defold permite acceder a cada objeto y componente en un juego en ejecución. El [manual de direccionamiento](/manuals/addressing/) entra en bastante detalle sobre cómo funciona el sistema. Es posible usar el mismo mecanismo de direccionamiento para objetos de juego generados y sus componentes. Muy a menudo basta con usar el id del objeto generado, por ejemplo al enviar un mensaje:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
El paso de mensajes al propio objeto de juego en vez de a un componente específico enviará de hecho el mensaje a todos los componentes. Normalmente esto no es un problema, pero conviene tenerlo en cuenta si el objeto tiene muchos componentes.
:::

Pero ¿qué ocurre si necesitas acceder a un componente específico en un objeto de juego generado, por ejemplo para desactivar un objeto de colisión o cambiar la imagen de un sprite? La solución es construir una URL a partir del id del objeto de juego y el id del componente.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Seguimiento de objetos generados y objetos padre

Cuando llamas a `factory.create()` obtienes el id del nuevo objeto de juego, lo que te permite guardar el id para usarlo como referencia en el futuro. Un uso común es generar objetos y agregar sus ids a una tabla para poder eliminarlos todos más adelante, por ejemplo al restablecer la disposición de un nivel:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Genera una moneda y guárdala en la tabla "coins".
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

Y luego más adelante:

```lua
-- spawner.script
-- Elimina todas las monedas generadas.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- o alternativamente
go.delete(self.spawned_coins)
```

También es común que quieras que el objeto generado conozca el objeto de juego que lo generó. Un caso sería algún tipo de objeto autónomo que solo puede generarse de a uno por vez. El objeto generado entonces necesita informar al generador cuando se elimina o se inactiva para que pueda generarse otro:

```lua
-- spawner.script
-- Genera un drone y define su padre como la URL de este componente de script
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

Y la lógica del objeto generado:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- Estoy muerto.
    msg.post(self.parent, "drone_dead")
end
```

## Carga dinámica de recursos de factory

Al marcar la casilla *Load Dynamically* en las propiedades de la factory, el motor pospone la carga de los recursos asociados con la factory.

![Cargar dinámicamente](images/factory/load_dynamically.png)

Con la casilla desmarcada, el motor carga los recursos del prototipo cuando se carga el componente factory, de modo que estén listos inmediatamente para generar objetos.

Con la casilla marcada, tienes dos opciones de uso:

Carga síncrona
: Llama a [`factory.create()`](/ref/factory/#factory.create) cuando quieras generar objetos. Esto cargará los recursos de forma síncrona, lo que puede causar una pausa breve, y luego generará nuevas instancias.

  ```lua
  function init(self)
      -- No se carga ningún recurso de factory cuando se carga
      -- la colección padre de la factory. Llamar a create sin
      -- haber llamado a load creará los recursos de forma síncrona.
      self.go_id = factory.create("#factory")
  end

  function final(self)
      -- Elimina objetos de juego. Reducirá el contador de referencia de los recursos.
      -- En este caso los recursos se eliminan porque el componente factory
      -- no mantiene ninguna referencia.
      go.delete(self.go_id)

      -- Llamar a unload no hará nada porque factory no mantiene referencias
      factory.unload("#factory")
  end
  ```

Carga asíncrona
: Llama a [`factory.load()`](/ref/factory/#factory.load) para cargar explícitamente los recursos de forma asíncrona. Cuando los recursos estén listos para generar objetos, se recibe un callback.

  ```lua
  function load_complete(self, url, result)
      -- La carga terminó, los recursos están listos para generar objetos
      self.go_id = factory.create(url)
  end

  function init(self)
      -- No se carga ningún recurso de factory cuando se carga
      -- la colección padre de la factory. Llamar a load cargará los recursos.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Elimina el objeto de juego. Reducirá el contador de referencia de los recursos.
      -- En este caso los recursos no se eliminan porque el componente factory
      -- todavía mantiene una referencia.
      go.delete(self.go_id)

      -- Llamar a unload reducirá el contador de referencia de los recursos
      -- mantenidos por el componente factory, lo que hará que se destruyan.
      factory.unload("#factory")
  end
  ```

## Prototipo dinámico

Es posible cambiar qué *Prototype* puede crear una factory marcando la casilla *Dynamic Prototype* en las propiedades de la factory.

![Prototipo dinámico](images/factory/dynamic_prototype.png)

Cuando la opción *Dynamic Prototype* está marcada, el componente factory puede cambiar de prototipo usando la función `factory.set_prototype()`. Ejemplo:

```lua
factory.unload("#factory") -- descarga los recursos anteriores
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Cuando la opción *Dynamic Prototype* está definida, el recuento de componentes de la colección no se puede optimizar, y la colección propietaria usará los recuentos de componentes predeterminados del archivo *game.project*.
:::


## Límites de instancias

La configuración de proyecto *max_instances* en *Collection related settings* limita el número total de instancias de objetos de juego que pueden existir en un mundo (la main.collection cargada al inicio o cualquier mundo cargado mediante un proxy de colección). Todos los objetos de juego que existen en el mundo se cuentan contra ese límite y no importa si se colocaron manualmente en el editor o si se generaron en tiempo de ejecución mediante un script.

![Máximo de instancias](images/factory/factory_max_instances.png)

Si defines *max_instances* en 1024 y tienes 24 objetos de juego colocados manualmente en tu colección principal, puedes generar 1000 objetos de juego adicionales. En cuanto elimines un objeto de juego, podrás generar otra instancia.

## Pooling de objetos de juego

Puede parecer una buena idea guardar objetos de juego generados en un pool y reutilizarlos. Sin embargo, el motor ya hace pooling de objetos internamente, por lo que la sobrecarga adicional solo hará que todo sea más lento. Es más rápido y más limpio eliminar objetos de juego y generar otros nuevos.
