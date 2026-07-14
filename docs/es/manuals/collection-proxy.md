---
title: Manual del proxy de colección
brief: Este manual explica cómo crear dinámicamente nuevos mundos de juego y cambiar entre ellos.
---

# Proxy de colección

El componente proxy de colección (collection proxy) se usa para cargar y descargar dinámicamente nuevos "mundos" de juego basados en el contenido de un archivo de colección. Se puede usar para implementar el cambio entre niveles del juego, pantallas GUI, carga y descarga de "escenas" narrativas durante un nivel, carga/descarga de mini-juegos y más.

Defold organiza todos los objetos de juego en colecciones. Una colección puede contener objetos de juego y otras colecciones (es decir, sub-colecciones). Los proxies de colección te permiten dividir tu contenido en colecciones separadas y luego gestionar dinámicamente la carga y descarga de esas colecciones mediante scripts.

Los proxies de colección son distintos de los [componentes factory de colección](/manuals/collection-factory/). Una factory de colección instancia el contenido de una colección en el mundo de juego actual. Los proxies de colección crean un nuevo mundo de juego en runtime y, por lo tanto, tienen casos de uso distintos.

## Crear un componente proxy de colección

1. Agrega un componente proxy de colección a un objeto de juego haciendo <kbd>click derecho</kbd> en un objeto de juego y seleccionando <kbd>Add Component ▸ Collection Proxy</kbd> en el menú contextual.

2. Define la propiedad *Collection* para que referencie una colección que quieras cargar dinámicamente en el runtime más adelante. La referencia es estática y asegura que todo el contenido de la colección referenciada termine en el juego final.

![agregar componente proxy](images/collection-proxy/create_proxy.png)

(Puedes excluir el contenido de la build y descargarlo con código en su lugar marcando la casilla *Exclude* y usando la [funcionalidad Live update](/manuals/live-update/).)

## Bootstrap

Cuando el motor Defold se inicia, carga e instancia en el runtime todos los objetos de juego de una *colección bootstrap*. Luego inicializa y habilita los objetos de juego y sus componentes. La colección bootstrap que debe usar el motor se configura en la [configuración del proyecto](/manuals/project-settings/#main-collection). Por convención, este archivo de colección suele llamarse "main.collection".

![bootstrap](images/collection-proxy/bootstrap.png)

Para alojar los objetos de juego y sus componentes, el motor asigna la memoria necesaria para todo el "mundo de juego" en el que se instancia el contenido de la colección bootstrap. También se crea un mundo físico separado para cualquier objeto de colisión y simulación física.

Como los componentes script deben poder direccionar todos los objetos del juego, incluso desde fuera del mundo bootstrap, a ese mundo se le asigna un nombre único: la propiedad *Name* que defines en el archivo de colección:

![bootstrap](images/collection-proxy/collection_id.png)

Si la colección que se carga contiene componentes proxy de colección, las colecciones a las que hacen referencia *no* se cargan automáticamente. Debes controlar la carga de estos recursos mediante scripts.

## Cargar una colección

Para cargar dinámicamente una colección mediante un proxy, envía un mensaje llamado `"load"` al componente proxy desde un script:

```lua
-- Indica al proxy "myproxy" que empiece a cargar.
msg.post("#myproxy", "load")
```

![cargar](images/collection-proxy/proxy_load.png)

El componente proxy le indicará al motor que asigne espacio para un nuevo mundo. También se crea un mundo físico de runtime separado y se instancian todos los objetos de juego de la colección "`mylevel.collection`".

El nuevo mundo obtiene su nombre de la propiedad *Name* en el archivo de colección; en este ejemplo está definida como "`mylevel`". El nombre debe ser único. Si el *Name* definido en el archivo de colección ya se usa para un mundo cargado, el motor señalará un error de colisión de nombres:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Cuando el motor termina de cargar la colección, el componente proxy de colección envía un mensaje llamado `"proxy_loaded"` al script que envió el mensaje `"load"`. Entonces el script puede inicializar y habilitar la colección como reacción al mensaje:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- El nuevo mundo está cargado. Inicialízalo y habilítalo.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Este mensaje le indica al componente proxy de colección que empiece a cargar su colección en un nuevo mundo. El proxy devolverá un mensaje llamado `"proxy_loaded"` cuando termine.

`"async_load"`
: Este mensaje le indica al componente proxy de colección que empiece a cargar su colección en segundo plano en un nuevo mundo. El proxy devolverá un mensaje llamado `"proxy_loaded"` cuando termine.

`"init"`
: Este mensaje le indica al componente proxy de colección que todos los objetos de juego y componentes que se han instanciado deben inicializarse. En esta etapa se llaman todas las funciones `init()` de los scripts.

`"enable"`
: Este mensaje le indica al componente proxy de colección que todos los objetos de juego y componentes deben habilitarse. Por ejemplo, todos los componentes sprite empiezan a dibujarse cuando se habilitan.

## Direccionamiento hacia el nuevo mundo

La propiedad *Name* definida en las propiedades del archivo de colección se usa para direccionar objetos de juego y componentes en el mundo cargado. Por ejemplo, si creas un objeto cargador en la colección bootstrap, puede que necesites comunicarte con él desde cualquier colección cargada:

```lua
-- indica al cargador que cargue el siguiente nivel:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![cargar](images/collection-proxy/message_passing.png)

Y si necesitas comunicarte con un objeto de juego de la colección cargada desde el cargador, puedes enviar un mensaje usando la [URL completa al objeto](/manuals/addressing/#urls):

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
No es posible acceder directamente a objetos de juego de una colección cargada desde fuera de esa colección:

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Descargar un mundo

Para descargar una colección cargada, envía mensajes correspondientes a los pasos inversos de la carga:

```lua
-- descarga el nivel
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Este mensaje le indica al componente proxy de colección que deshabilite todos los objetos de juego y componentes del mundo. En esta etapa los sprites dejan de renderizarse.

`"final"`
: Este mensaje le indica al componente proxy de colección que finalice todos los objetos de juego y componentes del mundo. En esta etapa se llaman todas las funciones `final()` de los scripts.

`"unload"`
: Este mensaje le indica al proxy de colección que elimine el mundo completamente de la memoria.

Si no necesitas un control más granular, puedes enviar el mensaje `"unload"` directamente, sin deshabilitar ni finalizar primero la colección. Entonces el proxy deshabilitará y finalizará automáticamente la colección antes de descargarla.

Cuando el proxy de colección haya terminado de descargar la colección, enviará un mensaje `"proxy_unloaded"` al script que envió el mensaje `"unload"`:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, el mundo está descargado...
        ...
    end
end
```


## Paso de tiempo

Las actualizaciones de un proxy de colección pueden escalarse alterando el _time step_ (paso de tiempo). Esto significa que, aunque el juego avance a 60 FPS constantes, un proxy puede actualizarse a un ritmo mayor o menor, lo que afecta a cosas como:

* Velocidad de simulación de física
* El `dt` pasado a `update()`
* [Animaciones de propiedades de objetos de juego y GUI](https://defold.com/manuals/animation/#property-animation-1)
* [Animaciones flipbook](https://defold.com/manuals/animation/#flip-book-animation)
* [Simulaciones Particle FX](https://defold.com/manuals/particlefx/)
* Velocidad de temporizadores

También puedes establecer el modo de actualización, que te permite controlar si el escalado debe realizarse de forma discreta (lo que solo tiene sentido con un factor de escala por debajo de 1.0) o continua.

Controlas el factor de escala y el modo de escalado enviando al proxy un mensaje `set_time_step`:

```lua
-- actualiza el mundo cargado a un quinto de la velocidad.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Para ver qué ocurre al cambiar el paso de tiempo, podemos crear un objeto con el siguiente código en un componente script y ponerlo en la colección cuyo paso de tiempo estamos modificando:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Con un paso de tiempo de 0.2, obtenemos el siguiente resultado en la consola:

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` se sigue llamando 60 veces por segundo, pero el valor de `dt` cambia. Vemos que solo 1/5 (0.2) de las llamadas a `update()` tendrán un `dt` de 1/60 (correspondiente a 60 FPS); el resto es cero. Todas las simulaciones de física también se actualizarán de acuerdo con ese `dt` y avanzarán solo en uno de cada cinco frames.

::: sidenote
Puedes usar la funcionalidad de paso de tiempo de colecciones para pausar tu juego, por ejemplo mientras muestras un popup o cuando la ventana ha perdido el foco. Usa `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` para pausar y `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` para reanudar.
:::

Consulta [`set_time_step`](/ref/collectionproxy#set_time_step) para más detalles.

## Advertencias y problemas comunes

Física
: Mediante proxies de colección es posible cargar más de una colección de nivel superior, o *mundo de juego*, en el motor. Al hacerlo, es importante saber que cada colección de nivel superior es un mundo físico separado. Las interacciones físicas (colisiones, triggers, ray-casts) solo ocurren entre objetos que pertenecen al mismo mundo. Así que, aunque los objetos de colisión de dos mundos visualmente estén justo uno sobre otro, no puede haber ninguna interacción física entre ellos.

Memoria
: Cada colección cargada crea un nuevo mundo de juego con un uso de memoria relativamente grande. Si cargas decenas de colecciones simultáneamente mediante proxies, quizá quieras reconsiderar tu diseño. Para generar muchas instancias de jerarquías de objetos de juego, los [componentes factory de colección](/manuals/collection-factory) son más adecuados.

Input
: Si tienes objetos en tu colección cargada que requieren acciones de input, debes asegurarte de que el objeto de juego que contiene el proxy de colección adquiera input. Cuando el objeto de juego recibe mensajes de input, estos se propagan a los componentes de ese objeto, es decir, a los proxies de colección. Las acciones de input se envían mediante el proxy hacia la colección cargada.
