---
title: Propiedades de componentes script
brief: Este manual explica cómo agregar propiedades personalizadas a componentes script y acceder a ellas desde el editor y scripts en tiempo de ejecución.
---

# Propiedades de script

Las propiedades de script ofrecen una forma simple y potente de definir y exponer propiedades personalizadas para una instancia específica de un objeto de juego. Las propiedades de script pueden editarse en instancias específicas directamente en el editor y sus valores pueden usarse en código para modificar el comportamiento de un objeto de juego. Hay muchos casos en los que las propiedades de script son muy útiles:

* Cuando quieres sobrescribir valores para instancias específicas en el editor y así aumentar la reutilización del script.
* Cuando quieres generar un objeto de juego con valores iniciales.
* Cuando quieres animar los valores de una propiedad.
* Cuando quieres acceder a datos de estado de un script desde otro. (Ten en cuenta que si accedes frecuentemente a propiedades entre objetos, puede ser mejor mover los datos a un almacenamiento compartido.)

Los casos de uso comunes son definir la salud o la velocidad de una IA enemiga específica, el color de tinte de un objeto pickup, el atlas de un sprite, o qué mensaje debe enviar un objeto botón cuando se presione, y/o adónde enviarlo.

## Definir una propiedad de script

Las propiedades de script se agregan a un componente script definiéndolas con la función especial `go.property()`. La función debe usarse en el nivel superior, fuera de cualquier función de ciclo de vida como `init()` y `update()`. El valor predeterminado proporcionado para la propiedad determina el tipo de la propiedad: `number`, `boolean`, `string`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` y `resource` (ver más abajo).

::: important
Ten en cuenta que la conversión inversa del valor hash funciona solo en la build Debug para facilitar la depuración. En la build Release, el valor de string inverso no existe, por lo que usar `tostring()` en un valor `hash` para extraer el string no tiene sentido.
:::


```lua
-- can.script
-- Define las propiedades de script para health y un objetivo de ataque
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- almacena la posición inicial del objetivo.
  -- self.target es una URL que referencia otro objeto.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- reduce la propiedad health
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

Entonces, cualquier instancia de componente script creada a partir de este script puede definir los valores de las propiedades.

![Componente con propiedades](images/script-properties/component.png)

Selecciona el componente script en la vista *Outline* del editor y las propiedades aparecerán en la vista *Properties*, lo que permite editarlas:

![Properties](images/script-properties/properties.png)

Cualquier propiedad sobrescrita con un nuevo valor específico de la instancia se marca en azul. Haz click en el botón de restablecer junto al nombre de la propiedad para revertir el valor al predeterminado (tal como se definió en el script).


::: important
Las propiedades de script se analizan al crear la build del proyecto. Las expresiones de valor no se evalúan. Esto significa que algo como `go.property("hp", 3+6)` no funcionará, mientras que `go.property("hp", 9)` sí.
:::

### Propiedades de texto {#text-properties}

Desde Defold 1.13.2, un valor predeterminado de tipo string define una propiedad de texto. Las propiedades de texto admiten UTF-8 y caracteres de salto de línea, y se editan en un campo multilínea en el editor:

```lua
go.property("greeting", "Hello!\nWelcome, José!")

function init(self)
    go.set("#label", "text", self.greeting)
end
```

Selecciona un componente script en un objeto de juego o colección para sobrescribir sus propiedades de texto, igual que las demás propiedades de script. No se permiten caracteres NUL incrustados en los valores predeterminados ni en los valores que los sobrescriben.

Otros scripts pueden leer y escribir una propiedad de texto mediante la URL del componente script. Por ejemplo, coloca el script anterior y un label en un objeto de juego llamado `speaker` en la colección, con los ids de componente `script` y `label`. Actualízalos desde `init()` de otro script:

```lua
function init(self)
    local greeting = go.get("/speaker#script", "greeting")
    go.set("/speaker#script", "greeting", greeting .. "\nEnjoy the game!")
    go.set("/speaker#label", "text", go.get("/speaker#script", "greeting"))
end
```

Cambiar la propiedad de script no actualiza automáticamente el label; la última línea copia explícitamente el nuevo valor a la propiedad `text` del label.

## Acceder a propiedades de script

Cualquier propiedad de script definida está disponible como un miembro almacenado en `self`, la referencia de la instancia del script:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Lee y escribe la propiedad
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Las propiedades de script definidas por el usuario también se pueden leer con `go.get()` y escribir con `go.set()`. Las propiedades numéricas, incluidos los vectores y cuaterniones, se pueden animar con `go.animate()`. Las propiedades de texto se pueden leer y escribir, pero no se pueden animar:

```lua
-- another.script

-- aumenta "my_property" en "myobject#script" en 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- anima "my_property" en "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Objetos creados con factory

Si usas una factory para crear el objeto de juego, es posible definir propiedades de script en el momento de la creación:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accede a propiedades de script de un objeto creado por factory
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Cuando generas una jerarquía de objetos de juego mediante `collectionfactory.create()`, necesitas emparejar los ids de objeto con tablas de propiedades. Los pares se agrupan en una tabla y se pasan a la función `create()`:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Los valores de propiedades proporcionados mediante `factory.create()` y `collectionfactory.create()` sobrescribirán cualquier valor definido en el archivo de prototipo, así como los valores predeterminados del script.

Si varios componentes script adjuntos a un objeto de juego definen la misma propiedad, cada componente se inicializará con el valor proporcionado a `factory.create()` o `collectionfactory.create()`.


## Propiedades de recursos {#resource-properties}

Las propiedades de recursos se definen igual que las propiedades de script para los tipos de datos básicos:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Cuando se define una propiedad de recurso, aparece en la vista *Properties* como cualquier otra propiedad de script, pero como un campo de exploración de archivo/recurso:

![Propiedades de recursos](images/script-properties/resource-properties.png)

Puedes acceder a las propiedades de recursos y usarlas mediante `go.get()` o a través de la referencia de instancia de script `self`, y modificarlas con `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
