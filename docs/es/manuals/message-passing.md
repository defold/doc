---
title: Paso de mensajes en Defold
brief: El paso de mensajes es el mecanismo que usa Defold para permitir que objetos débilmente acoplados se comuniquen. Este manual describe este mecanismo en profundidad.
---

# Paso de mensajes

El paso de mensajes es un mecanismo para que los objetos de juego de Defold se comuniquen entre sí. Este manual asume que tienes una comprensión básica del [mecanismo de direccionamiento](/manuals/addressing) de Defold y de los [bloques de construcción básicos](/manuals/building-blocks).

Defold no usa orientación a objetos en el sentido de definir tu aplicación configurando jerarquías de clases con herencia y funciones miembro en tus objetos (como Java, C++ o C#). En su lugar, Defold extiende Lua con un diseño orientado a objetos simple y potente, donde el estado del objeto se mantiene internamente en componentes script y es accesible a través de la referencia `self`. Además, los objetos pueden estar totalmente desacoplados mediante el paso de mensajes asíncrono como medio de comunicación entre objetos.


## Ejemplos de uso

Veamos primero algunos ejemplos de uso sencillos. Supón que estás creando un juego que consta de:

1. Una colección bootstrap principal que contiene un objeto de juego con un componente GUI (la GUI consta de un minimapa y un contador de puntuación). También hay una colección con el id "level".
2. La colección llamada "level" contiene dos objetos de juego: un personaje héroe del jugador y un enemigo.

![Estructura de paso de mensajes](images/message_passing/message_passing_structure.png)

::: sidenote
El contenido de este ejemplo se encuentra en dos archivos separados. Hay un archivo para la colección bootstrap principal y otro para la colección con el id "level". Sin embargo, los nombres de archivo _no importan_ en Defold. Lo que importa es la identidad que asignas a las instancias.
:::

El juego contiene algunas mecánicas sencillas que requieren comunicación entre los objetos:

![Paso de mensajes](images/message_passing/message_passing.png)

① El héroe golpea al enemigo
: Como parte de esta mecánica, se envía un mensaje `"punch"` desde el componente script "hero" al componente script "enemy". Como ambos objetos están en el mismo lugar de la jerarquía de colecciones, se prefiere el direccionamiento relativo:

  ```lua
  -- Envía "punch" desde el script "hero" al script "enemy"
  msg.post("enemy#controller", "punch")
  ```

  Solo hay un tipo de golpe en el juego, así que el mensaje no necesita contener más información que su nombre, "punch".

  En el componente script del enemigo, creas una función para recibir el mensaje:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  En este caso, el código solo comprueba el nombre del mensaje (enviado como una cadena con hash en el parámetro `message_id`). Al código no le importan los datos del mensaje ni el remitente; *cualquiera* que envíe el mensaje "punch" infligirá daño al pobre enemigo.

② El héroe gana puntuación
: Cada vez que el jugador derrota a un enemigo, la puntuación del jugador aumenta. También se envía un mensaje `"update_score"` desde el componente script del objeto de juego "hero" al componente "gui" del objeto de juego "interface".

  ```lua
  -- Enemigo derrotado. Aumenta el contador de puntuación en 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  En este caso no es posible escribir una dirección relativa porque "interface" está en la raíz de la jerarquía de nomenclatura y "hero" no. El mensaje se envía al componente GUI que tiene un script adjunto, por lo que puede reaccionar al mensaje como corresponda. Los mensajes se pueden enviar libremente entre scripts, scripts GUI y render scripts.

  El mensaje `"update_score"` está acoplado a datos de puntuación. Los datos se pasan como una tabla Lua en el parámetro `message`:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- define el contador de puntuación con la nueva puntuación
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Posición del enemigo en el minimapa
: El jugador tiene un minimapa en pantalla que ayuda a localizar y seguir a los enemigos. Cada enemigo es responsable de señalizar su posición enviando un mensaje `"update_minimap"` al componente "gui" del objeto de juego "interface":

  ```lua
  -- Envía la posición actual para actualizar el minimapa de la interfaz
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  El código del script GUI necesita seguir la posición de cada enemigo y, si el mismo enemigo envía una nueva posición, se debe reemplazar la anterior. El remitente del mensaje (pasado en el parámetro `sender`) se puede usar como clave en una tabla Lua con posiciones:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- actualiza la posición en el mapa
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- define el contador de puntuación con la nueva puntuación
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- actualiza el minimapa con nuevas posiciones
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Enviar mensajes

La mecánica de enviar un mensaje es, como hemos visto arriba, muy sencilla. Llamas a la función `msg.post()`, que envía tu mensaje a la cola de mensajes. Luego, en cada frame, el motor recorre la cola y entrega cada mensaje a su dirección objetivo. Para algunos mensajes del sistema (como `"enable"`, `"disable"`, `"set_parent"`, etc.), el código del motor maneja el mensaje. El motor también produce algunos mensajes del sistema (como `"collision_response"` en colisiones de físicas) que se entregan a tus objetos. Para mensajes de usuario enviados a componentes script, el motor simplemente llama a una función especial de Defold Lua llamada `on_message()`.

Puedes enviar mensajes arbitrarios a cualquier objeto o componente existente, y depende del código del lado del destinatario responder al mensaje. Si envías un mensaje a un componente script y el código del script ignora el mensaje, no pasa nada. La responsabilidad de tratar los mensajes recae por completo en el receptor.

El motor verificará la dirección objetivo del mensaje. Si intentas enviar un mensaje a un destinatario desconocido, Defold señalará un error en la consola:

```lua
-- Intenta enviar a un objeto que no existe
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

La firma completa de la llamada `msg.post()` es:

`msg.post(receiver, message_id, [message])`

receiver
: El id del componente u objeto de juego objetivo. Ten en cuenta que si apuntas a un objeto de juego, el mensaje se difundirá a todos los componentes del objeto de juego.

message_id
: Una cadena o cadena con hash con el nombre del mensaje.

[message]
: Una tabla Lua opcional con pares clave-valor de datos del mensaje. En la tabla Lua del mensaje se puede incluir casi cualquier tipo de datos. Puedes pasar números, strings, booleanos, URL, hashes y tablas anidadas. No puedes pasar funciones.

  ```lua
  -- Envía datos de tabla que contienen una tabla anidada
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Hay un límite estricto para el tamaño de la tabla del parámetro `message`. Este límite se establece en 2 kilobytes. Actualmente no hay una forma trivial de averiguar el tamaño exacto de memoria que consume una tabla, pero puedes usar `collectgarbage("count")` antes y después de insertar la tabla para monitorear el uso de memoria.
:::

### Atajos

Defold proporciona dos atajos útiles que puedes usar para enviar mensajes sin especificar una URL completa:

:[Shorthands](../shared/url-shorthands.md)


## Recibir mensajes

Recibir mensajes consiste en asegurarse de que el componente script objetivo contenga una función llamada `on_message()`. La función acepta cuatro parámetros:

`function on_message(self, message_id, message, sender)`

`self`
: Una referencia al propio componente script.

`message_id`
: Contiene el nombre del mensaje. El nombre está almacenado como _hash_.

`message`
: Contiene los datos del mensaje. Esto es una tabla Lua. Si no hay datos, la tabla está vacía.

`sender`
: Contiene la URL completa del remitente.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Mensajes entre mundos de juego

Si usas un componente proxy de colección para cargar un nuevo mundo de juego en el runtime, querrás pasar mensajes entre los mundos de juego. Supón que has cargado una colección mediante un proxy y que la colección tiene su propiedad *Name* definida como "level":

![Nombre de colección](images/message_passing/collection_name.png)

Tan pronto como la colección se haya cargado, iniciado y habilitado, puedes enviar mensajes a cualquier componente u objeto del nuevo mundo especificando el nombre del mundo de juego en el campo "socket" de la dirección del destinatario:

```lua
-- Envía un mensaje al jugador en el nuevo mundo de juego
msg.post("level:/player#controller", "wake_up")
```
Puedes encontrar una descripción más detallada de cómo funcionan los proxies en la documentación de [proxies de colección](/manuals/collection-proxy).

## Cadenas de mensajes

Cuando un mensaje que se ha enviado finalmente se despacha, se llama al `on_message()` de los destinatarios. Es bastante común que el código de reacción envíe nuevos mensajes, que se agregan a la cola de mensajes.

Cuando el motor comienza el despacho, recorrerá la cola de mensajes y llamará a la función `on_message()` de cada destinatario de mensaje, y continuará hasta que la cola de mensajes esté vacía. Si la pasada de despacho agrega nuevos mensajes a la cola, hará otra pasada. Sin embargo, hay un límite estricto en cuántas veces el motor intenta vaciar la cola, lo que en la práctica limita la longitud de las cadenas de mensajes que puedes esperar que se despachen por completo dentro de un frame. Puedes probar fácilmente cuántas pasadas de despacho realiza el motor entre cada `update()` con el siguiente script:

```lua
function init(self)
    -- Iniciamos una cadena de mensajes larga durante init del objeto
    -- y la mantenemos ejecutándose durante varios pasos de update().
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

Ejecutar este script imprimirá algo como lo siguiente:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Vemos que esta versión específica del motor Defold realiza 10 pasadas de despacho en la cola de mensajes entre `init()` y la primera llamada a `update()`. Luego realiza 75 pasadas durante cada bucle de actualización posterior.
