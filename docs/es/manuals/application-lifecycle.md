---
title: Manual del ciclo de vida de las aplicaciones Defold
brief: Este manual detalla el ciclo de vida de los juegos y aplicaciones Defold.
---

# Ciclo de vida de la aplicación

El ciclo de vida de una aplicación o juego Defold es, a grandes rasgos, simple. El motor avanza por tres etapas de ejecución: inicialización, el bucle de actualización (donde las apps y los juegos pasan la mayor parte de su tiempo) y finalización.

::: sidenote
El manual se refiere a versiones de Defold desde la 1.12.0. En la versión 1.12.0 se introdujeron cambios relacionados con el ciclo de vida y la nueva función `late_update()`.
:::

![Visión general del ciclo de vida](images/application_lifecycle/application_lifecycle.png)

En muchos casos solo es necesario entender de forma básica el funcionamiento interno de Defold. Sin embargo, puedes encontrarte con casos límite donde el orden exacto en que Defold realiza sus tareas se vuelve vital. Este documento describe cómo el motor ejecuta una aplicación de principio a fin.

La aplicación comienza inicializando todo lo necesario para ejecutar el motor. Carga la colección principal y llama a [`init()`](/ref/go#init) en todos los componentes cargados que tienen una función Lua `init()` (componentes script y componentes GUI con scripts GUI). Esto te permite realizar una inicialización personalizada.

Luego la aplicación entra en el bucle de actualización, donde pasará la mayor parte de su vida útil. En cada frame, se actualizan los objetos de juego y los componentes que contienen. Se llama a cualquier función [`update()`](/ref/go#update) de scripts y scripts GUI. Durante el bucle de actualización, los mensajes se despachan a sus destinatarios, se reproducen sonidos y se renderizan todos los gráficos.

En algún momento, el ciclo de vida de la aplicación llegará a su fin. Antes de que la aplicación salga, el motor abandona el bucle de actualización y entra en una etapa de finalización. Prepara todos los objetos de juego cargados para su eliminación. Se llama a las funciones [`final()`](/ref/go#final) de todos los componentes de objetos, lo que permite hacer limpieza personalizada. Luego se eliminan los objetos y se descarga la colección principal.

Los pasos incluidos en la pasada de ["dispatch messages"](#dispatching-messages) se muestran en un diagrama separado al final de este manual para mayor claridad y se marcan en los diagramas con un pequeño icono de "sobre con una flecha" 📩.

## Inicialización

Aquí es donde empieza tu juego y es el primer paso del juego en ejecución. Se puede separar en 3 fases:

![Inicialización](images/application_lifecycle/initialization.png)

### Preinicialización

Durante la fase `Preinitialization`, el motor realiza muchos pasos antes de que se cargue la colección principal (bootstrap). Se configuran el profiler de memoria, sockets, gráficos, HID (dispositivos de input), sonido, físicas y mucho más. La configuración de la aplicación (*game.project*) también se carga y se configura.

![Preinicialización](images/application_lifecycle/pre_init.png)

El primer punto de entrada controlable por el usuario, al final de la inicialización del motor, es la llamada a la función `init()` del script de render actual.

Luego se carga e inicializa la colección principal.

### Inicialización de colección

Durante la fase `Collection Init`, todos los objetos de juego de la colección aplican sus transformaciones: traslación (cambio de posición), rotación y escala, a sus hijos. Luego se llama a todas las funciones `init()` existentes de los componentes.

![Inicialización de colección](images/application_lifecycle/collection_init.png)

::: sidenote
El orden en que se llaman las funciones `init()` de los componentes de objetos de juego no está especificado. No debes asumir que el motor inicializa los objetos que pertenecen a la misma colección en un orden determinado.
:::

### Post Update en la inicialización

Luego el motor realiza una pasada completa de `Post Update`: la misma pasada que se realiza después de cada paso de `Update Loop` más adelante. Se realiza al final de la inicialización porque tu código `init()` puede enviar nuevos mensajes, indicar a las factories que generen nuevos objetos, marcar objetos para eliminación y realizar otras acciones.

![Post Update](images/application_lifecycle/post_init.png)

Esta pasada realiza la entrega de mensajes, la generación real de objetos de juego desde factories y la eliminación de objetos. Ten en cuenta que la pasada `Post Update` incluye una secuencia de "dispatch messages" que no solo entrega los mensajes en cola, sino que también procesa mensajes enviados a proxies de colección. Cualquier actualización posterior de proxy (enable, disable, init, final, carga y marcado para descarga) se realiza durante esos pasos.

Es completamente posible cargar un [proxy de colección](/manuals/collection-proxy) durante `init()`, asegurarse de que todos los objetos que contiene se inicialicen y luego descargar la colección a través del proxy, todo esto antes de que se llame al primer `update()` de un componente; es decir, antes de que el motor haya salido de la etapa de inicialización y haya entrado en el bucle de actualización:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- La colección del proxy se descarga antes de llegar a este código.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- Las funciones init() y final() de los objetos de la colección
        -- del proxy se llaman antes de llegar al update() de este objeto
    end
end
```

## Bucle de actualización

El `Update Loop` ejecuta una secuencia específica una vez por frame. Esta secuencia se puede definir mediante 5 fases principales:

![Bucle de actualización](images/application_lifecycle/update_loop.png)

1. Input (procesamiento y manejo)
2. Update (incluye actualizaciones Fixed, Regular, Late y de componentes del motor)
3. Render Update
4. Post Update (descarga de proxies de colección, generación y eliminación de objetos de juego)
5. Frame Render (se renderizan los gráficos finales)

### Fase de Input

El input se lee desde los dispositivos disponibles, se mapea contra [input bindings](/manuals/input) y luego se despacha. Cualquier objeto de juego que haya adquirido el foco de input recibe input enviado a las funciones `on_input()` de todos sus componentes. Un objeto de juego con un componente script y un componente GUI con un script GUI recibirá input en las funciones `on_input()` de ambos componentes, siempre que estén definidas y hayan adquirido el foco de input.

![Fase de Input](images/application_lifecycle/input_phase.png)

Cualquier objeto de juego que haya adquirido el foco de input y contenga componentes de proxy de colección despacha input a los componentes dentro de la colección del proxy. Este proceso continúa recursivamente hacia abajo por proxies de colección habilitados dentro de proxies de colección habilitados.

### Fase de Update

La fase `Update` es parte del `Update Loop`. Se inicia una vez para la colección raíz y luego se ejecuta recursivamente para cada proxy de colección habilitado.

Dentro de una colección, Defold procesa callbacks por tipo de componente: itera sobre todas las instancias de un tipo de componente que implementa la etapa relevante, llama al callback Lua para cada instancia, vacía los mensajes y luego avanza al siguiente tipo de componente.

El orden de alto nivel de las etapas de callbacks Lua de componentes *script* es:

1. `fixed_update()`: se llama de 0 a N veces por frame (si se usa fixed timestep)
2. `update()`: se llama 1 vez por frame
3. `late_update()`: se llama 1 vez por frame

![Fase de Update](images/application_lifecycle/update_phase.png)

Se recorre cada componente de objeto de juego en la colección principal. Si alguno de estos componentes tiene un script con una función `fixed_update()`/`update()`/`late_update()`, entonces se llama a esa función. Si el componente es un proxy de colección, cada componente de la colección del proxy se actualiza recursivamente con todos los pasos de la fase `Update`.

::: sidenote
El orden en que se llaman las funciones `update()` de los componentes de objetos de juego no está especificado. No debes asumir que el motor actualiza los objetos que pertenecen a la misma colección en un orden determinado. Lo mismo aplica a `fixed_update()` y `late_update()` (desde 1.12.0).
:::

#### Físicas

Para los componentes de objeto de colisión, los mensajes de físicas (colisiones, triggers, respuestas de ray cast, etc.) se despachan por todo el objeto de juego que los contiene hacia todos los componentes que contienen un script con la función `on_message()`.

Si se usa un [fixed timestep](/manuals/physics/#physics-updates) para la simulación de físicas, también puede haber una llamada a la función `fixed_update()` en todos los componentes script. Esta función es útil en juegos basados en físicas cuando quieres manipular objetos físicos a intervalos regulares para lograr una simulación de físicas estable.

#### Transformaciones

Antes de **cada** actualización por tipo de componente, varias veces durante el `Update Loop` si es necesario, se actualizan las transformaciones, aplicando cualquier movimiento, rotación y escala de objeto de juego a cada componente de objeto de juego y a cualquier componente de objeto de juego hijo.

Hay una actualización final adicional de transformaciones al final del `Update Loop`, si es necesaria.

#### Fase de actualización del motor (sin fixed updates)

Las tablas siguientes describen las pasadas de actualización a *nivel del motor*. Omiten deliberadamente el orden exacto de prioridad interna de los componentes (que es un detalle de implementación del motor), pero reflejan las garantías de orden relevantes para scripting:

- `fixed_update()` se ejecuta antes de `update()`
- `late_update()` se ejecuta después de `update()`
- los mensajes enviados se vacían entre actualizaciones por tipo de componente, y también entre las etapas de callbacks de script

Cuando `Use Fixed Timestep` es `false` y/o Fixed Update Frequency es `0`, al comienzo de la fase se prepara `dt` y luego el flujo es el que se presenta en la tabla siguiente:

:::sidenote
Ten en cuenta que después de la actualización de **cada** tipo de componente, se despachan todos los mensajes; esto no está marcado en la tabla siguiente para mantenerla clara.
:::

| Paso | Fase del motor | Callback Lua | Comentario |
|-|-|-|-|
| 1 | **Update** | `update()` | Se llama una vez por frame para cada tipo de componente que implementa Update en el orden de prioridad interno. Además, las animaciones de propiedades de objetos de juego iniciadas con `go.animate()` se actualizan aquí como un tipo de componente separado. Los componentes de **físicas** se actualizan aquí. Para cada proxy de colección habilitado, toda la fase `Update` se llama recursivamente desde el paso 1. |
| 2 | **Late Update** | `late_update()` | Se llama una vez por frame para cada tipo de componente que implementa Late Update en el orden de prioridad interno. |
| 3 | **Transforms** | | Se realiza una actualización final adicional de transformaciones al final para cada componente si es necesario. |

#### Fase de actualización del motor con Fixed Timestep

Cuando `Use Fixed Timestep` es `true` y Fixed Update Frequency no es cero, al comienzo de la fase se preparan `dt` (delta time), `fixed_dt` y `num_fixed_steps` (`0..N`), es decir, cuántas veces se llamará a fixed update, determinado por el tiempo desde la última actualización para asegurar que haya una cantidad fija de actualizaciones.

:::sidenote
Ten en cuenta que después de la actualización de **cada** tipo de componente, se despachan todos los mensajes; esto no está marcado en la tabla siguiente para mantenerla clara.
:::

Luego entra en un bucle:

| Paso | Fase del motor | Callback Lua | Comentario |
|-|-|-|-|
| 1 | **Fixed Update** | `fixed_update()` | Se llama `0..N` veces por frame, según el tiempo, para cada tipo de componente que implementa Fixed Update en el orden de prioridad interno. Incluye los pasos Fixed Update de los componentes de *físicas*. |
| 2 | **Update** | `update()` | Se llama una vez por frame para cada tipo de componente que implementa Update en el orden de prioridad interno. Además, las animaciones de propiedades de objetos de juego iniciadas con `go.animate()` se actualizan aquí como un tipo de componente separado. Para cada proxy de colección habilitado, la fase `Update` se llama recursivamente desde el paso 1. |
| 3 | **Late Update** | `late_update()` | Se llama una vez por frame para cada tipo de componente que implementa Late Update en el orden de prioridad interno. |
| 4 | **Transforms** | | Se realiza una actualización final adicional de transformaciones al final para cada componente si es necesario. |

Si alguna vez necesitas más detalles sobre cómo funciona Defold internamente durante la fase Update, vale la pena leer el código de [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Fase de Render Update

El bloque de render update despacha primero todos los mensajes enviados al socket `@render` (por ejemplo, mensajes `set_view_projection` de componentes de cámara, mensajes `set_clear_color`, etc.). Luego se llama a `update()` del script de render.

![Fase de Render Update](images/application_lifecycle/render_update_phase.png)

### Fase de Post Update

Después de las actualizaciones, se ejecuta una secuencia post update. Descarga de memoria los proxies de colección marcados para descarga (esto ocurre durante la secuencia "dispatch messages"). Cualquier objeto de juego marcado para eliminación llamará a las funciones `final()` de todos sus componentes, si las hay. El código en las funciones `final()` suele enviar nuevos mensajes a la cola, por lo que la pasada "dispatch messages" se ejecuta después.

![Fase de Post Update](images/application_lifecycle/post_update_phase.png)

Cualquier componente factory al que se le haya indicado que genere un objeto de juego lo hará a continuación. Finalmente, los objetos de juego marcados para eliminación se eliminan realmente.

### Fase de renderizado

El último paso del bucle de actualización implica despachar mensajes de `@system` (mensajes `exit`, `reboot`, alternar el profiler, iniciar y detener captura de video, etc.).

![Fase de renderizado](images/application_lifecycle/render_phase.png)

Luego se renderizan los gráficos, junto con cualquier renderizado del profiler visual (consulta la [documentación de depuración](/manuals/debugging)). Después del renderizado de gráficos, se realiza una captura de video.

#### Frecuencia de frames y time step de colección

El número de actualizaciones de frame por segundo (que equivale al número de ejecuciones del bucle de actualización por segundo) se puede establecer en la configuración del proyecto, o programáticamente enviando un mensaje `set_update_frequency` al socket `@system`. Además, es posible establecer el _time step_ de los proxies de colección de forma individual enviando un mensaje `set_time_step` al proxy. Cambiar el time step de una colección no afecta la frecuencia de frames. Sí afecta el time step de actualización de físicas, así como la variable `dt` pasada a `update().` Ten en cuenta también que modificar el time step no cambia la cantidad de veces que se llamará a `update()` en cada frame: siempre es exactamente una vez.

(Consulta el [manual de proxy de colección](/manuals/collection-proxy) y [`set_time_step`](/ref/collectionproxy#set-time-step) para más detalles)

#### Throttling del motor

Defold 1.12.0 introdujo una API de throttling del motor que puede omitir por completo las actualizaciones y el renderizado del motor, mientras sigue detectando input. Cualquier input despierta el motor de nuevo, y el motor puede volver a entrar en throttling después de un tiempo de espera.

Consulta la API `sys.set_engine_throttle()` para ver detalles y ejemplos de uso.

## Finalización

Cuando la aplicación sale, primero termina la última secuencia del bucle de actualización, que descargará cualquier proxy de colección: finaliza y elimina todos los objetos de juego en cada colección del proxy.

Cuando esto termina, el motor entra en una secuencia de finalización que maneja la colección principal y sus objetos:

![Finalización](images/application_lifecycle/finalization.png)

Primero se llama a las funciones `final()` de los componentes. Luego sigue un despacho posterior de mensajes. Finalmente, se eliminan todos los objetos de juego y se descarga la colección principal.

Luego el motor continúa con el cierre interno de subsistemas: se elimina la configuración del proyecto, se apaga el profiler de memoria, y así sucesivamente.

La aplicación ahora está completamente apagada.

<a id="dispatching-messages"></a>

## Despacho de mensajes

**Dispatching Messages** es una pasada especial que se realiza después de la actualización de **cada** tipo de componente; por ejemplo, actualización de sprites, actualización de scripts y cualquier otra acción que pueda enviar mensajes. Durante su ejecución, se despachan todos los mensajes enviados que se hayan acumulado en una cola. Se marcan en los diagramas con pequeños iconos de "sobre con una flecha" 📩.

![Despacho de mensajes](images/application_lifecycle/dispatch_messages.png)

Después de despachar todos los **mensajes de usuario** llamando a `on_message()` para cada componente, los mensajes especiales de Defold se manejan en el orden siguiente (como también se presenta en el diagrama), para cada proxy de colección:

1. Mensajes `load`: para cargar proxies de colección marcados para carga; envían de vuelta el mensaje `proxy_loaded`.
2. Mensajes `unload`: para descargar proxies de colección marcados para descarga; envían de vuelta el mensaje `proxy_unloaded`.
3. Mensajes `init`: disparan la fase `Collection Init` para todos los proxies de colección que se inicializarán.
4. Mensajes `final`: disparan `final()` en todos los componentes del proxy marcado para finalización.
5. Mensajes `enable`: habilitan el proxy de colección, por lo que el `Update Loop` se realizará para él en el siguiente frame; esto dispara implícitamente `init()` para cada componente de la colección.
6. Mensajes `disable`: deshabilitan el proxy de colección, por lo que el `Update Loop` **no** se realizará para él en el siguiente frame; deja de ejecutar por completo el `Update Loop` para ese proxy.

Como el código `on_message()` de cualquier componente receptor puede enviar mensajes adicionales, el despachador de mensajes seguirá despachando mensajes enviados recursivamente hasta que la cola de mensajes quede vacía. Sin embargo, hay un límite para la cantidad de pasadas por la cola de mensajes que realiza el despachador de mensajes. Consulta [cadenas de mensajes](/manuals/message-passing) para más detalles.
