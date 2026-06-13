---
title: Efectos de partículas en Defold
brief: Este manual explica cómo funciona el componente Particle FX y cómo editarlo para crear efectos visuales de partículas.
---

# Particle FX

Los efectos de partículas se usan para mejorar visualmente los juegos. Puedes usarlos para crear explosiones, salpicaduras de sangre, estelas, clima o cualquier otro efecto.

![Editor ParticleFX](images/particlefx/editor.png)

Los efectos de partículas consisten en varios emisores y modificadores opcionales:

Emitter
: Un emisor es una forma posicionada que emite partículas distribuidas uniformemente sobre la forma. El emisor contiene propiedades que controlan la generación de partículas, así como la imagen o animación, el tiempo de vida, el color, la forma y la velocidad de cada partícula.

Modifier
: Un modificador afecta la velocidad de las partículas generadas para hacer que aceleren o reduzcan la velocidad en una dirección determinada, se muevan radialmente o giren alrededor de un punto. Los modificadores pueden afectar las partículas de todos los emisores o de un emisor particular.

## Crear un efecto

Selecciona <kbd>New... ▸ Particle FX</kbd> desde el menú contextual en el navegador *Assets*. Nombra el nuevo archivo de efecto de partículas. El editor abrirá el archivo usando el [Scene Editor](/manuals/editor/#the-scene-editor).

El panel *Outline* muestra el emisor predeterminado. Selecciona el emisor para mostrar sus propiedades en el panel *Properties* debajo.

![Partículas predeterminadas](images/particlefx/default.png)

Para añadir un nuevo emisor al efecto, haz <kbd>click derecho</kbd> en la raíz de *Outline* y selecciona <kbd>Add Emitter ▸ [type]</kbd> desde el menú contextual. Ten en cuenta que puedes cambiar el tipo del emisor en las propiedades del emisor.

Para añadir un nuevo modificador, haz <kbd>click derecho</kbd> en la ubicación del modificador en *Outline* (la raíz del efecto o un emisor particular) y selecciona <kbd>Add Modifier</kbd>; luego selecciona el tipo de modificador.

![Añadir modificador](images/particlefx/add_modifier.png)

![Seleccionar modificador añadido](images/particlefx/add_modifier_select.png)

Un modificador que está en la raíz del efecto (no como hijo de un emisor) afecta a todas las partículas del efecto.

Un modificador añadido como hijo de un emisor afecta solo a ese emisor.

## Previsualizar un efecto

* Selecciona <kbd>View ▸ Play</kbd> desde el menú para previsualizar el efecto. Puede que necesites alejar la cámara para ver el efecto correctamente.
* Selecciona <kbd>View ▸ Play</kbd> otra vez para pausar el efecto.
* Selecciona <kbd>View ▸ Stop</kbd> para detener el efecto. Reproducirlo de nuevo lo reinicia desde su estado inicial.

Al editar un emisor o un modificador, el resultado se ve inmediatamente en el editor, incluso con el efecto pausado:

![Editar partículas](images/particlefx/rotate.gif)

## Propiedades del emisor

Id
: Identificador del emisor (se usa al definir constantes de render para emisores específicos).

Position/Rotation
: Transformación del emisor relativa al componente ParticleFX.

Play Mode
: Controla cómo se reproduce el emisor:
  - `Once` detiene el emisor después de alcanzar su duración.
  - `Loop` reinicia el emisor después de alcanzar su duración.

Size Mode
: Controla cómo se dimensionarán las animaciones flipbook:
  - `Auto` conserva el tamaño de cada frame de animación flipbook según la imagen de origen.
  - `Manual` define el tamaño de partícula según la propiedad de tamaño.

Emission Space
: En qué espacio geométrico existirán las partículas generadas:
  - `World` mueve las partículas de forma independiente del emisor.
  - `Emitter` mueve las partículas relativas al emisor.

Duration
: El número de segundos durante los que el emisor debe emitir partículas.

Start Delay
: El número de segundos que el emisor debe esperar antes de emitir partículas.

Start Offset
: El número de segundos dentro de la simulación de partículas en que debe comenzar el emisor o, en otras palabras, durante cuánto tiempo el emisor debe precalentar el efecto.

Image
: El archivo de imagen (Tile source o Atlas) que se usará para texturizar y animar las partículas.

Animation
: La animación del archivo *Image* que se usará en las partículas.

Material
: El material que se usará para sombrear las partículas.

Blend Mode
: Los modos de mezcla disponibles son `Alpha`, `Add` y `Multiply`.

Max Particle Count
: Cuántas partículas originadas desde este emisor pueden existir al mismo tiempo.

Emitter Type
: La forma del emisor
  - `Circle` emite partículas desde una ubicación aleatoria dentro de un círculo. Las partículas se dirigen hacia afuera desde el centro. El diámetro del círculo se define con *Emitter Size X*.

  - `2D Cone` emite partículas desde una ubicación aleatoria dentro de un cono plano (un triángulo). Las partículas se dirigen hacia afuera por la parte superior del cono. *Emitter Size X* define el ancho de la parte superior y *Y* define la altura.

  - `Box` emite partículas desde una ubicación aleatoria dentro de una caja. Las partículas se dirigen hacia arriba a lo largo del eje Y local de la caja. *Emitter Size X*, *Y* y *Z* definen el ancho, la altura y la profundidad respectivamente. Para un rectángulo 2D, mantén el tamaño Z en cero.

  - `Sphere` emite partículas desde una ubicación aleatoria dentro de una esfera. Las partículas se dirigen hacia afuera desde el centro. El diámetro de la esfera se define con *Emitter Size X*.

  - `Cone` emite partículas desde una ubicación aleatoria dentro de un cono 3D. Las partículas se dirigen hacia afuera a través del disco superior del cono. *Emitter Size X* define el diámetro del disco superior y *Y* define la altura del cono.

  ![tipos de emisor](images/particlefx/emitter_types.png)

Particle Orientation
: Cómo se orientan las partículas emitidas:
  - `Default` establece la orientación en la orientación unidad.
  - `Initial Direction` conserva la orientación inicial de las partículas emitidas.
  - `Movement Direction` ajusta la orientación de las partículas según su velocidad.

Inherit Velocity
: Un valor de escala que indica cuánta velocidad del emisor deben heredar las partículas. Este valor solo está disponible cuando *Space* se define como `World`. La velocidad del emisor se estima en cada frame.

Stretch With Velocity
: Marca esta opción para escalar cualquier estiramiento de partícula en la dirección del movimiento.

### Modos de mezcla
:[blend-modes](../shared/blend-modes.md)

## Propiedades animables del emisor

Estas propiedades tienen dos campos: un valor y una dispersión. La dispersión es una variación que se aplica aleatoriamente a cada partícula generada. Por ejemplo, si el valor es 50 y la dispersión es 3, cada partícula generada recibirá un valor entre 47 y 53 (50 +/- 3).

![Propiedad](images/particlefx/property.png)

Al marcar el botón de clave, el valor de la propiedad se controla mediante una curva a lo largo de la duración del emisor. Para restablecer una propiedad con claves, desmarca el botón de clave.

![Propiedad con clave](images/particlefx/key.png)

El *Curve Editor* (disponible entre las pestañas de la vista inferior) se usa para modificar la curva. Las propiedades con claves no pueden editarse en la vista *Properties*, solo en el *Curve Editor*. Haz <kbd>click y arrastra</kbd> los puntos y tangentes para modificar la forma de la curva. Haz <kbd>doble click</kbd> en la curva para añadir puntos de control. Para eliminar un punto de control, haz <kbd>doble click</kbd> sobre él.

![Curve Editor de ParticleFX](images/particlefx/curve_editor.png)

Para ajustar automáticamente el zoom del Curve Editor y mostrar todas las curvas, presiona <kbd>F</kbd>.

Las siguientes propiedades pueden animarse con claves durante el tiempo de reproducción del emisor:

Spawn Rate
: El número de partículas que se emiten por segundo.

Emitter Size X/Y/Z
: Las dimensiones de la forma del emisor; consulta *Emitter Type* arriba.

Particle Life Time
: El tiempo de vida de cada partícula generada, en segundos.

Initial Speed
: La velocidad inicial de cada partícula generada.

Initial Size
: El tamaño inicial de cada partícula generada. Si defines *Size Mode* como `Automatic` y usas una animación flipbook como fuente de imagen, esta propiedad se ignora.

Initial Red/Green/Blue/Alpha
: Los valores iniciales de tinte de los componentes de color para las partículas.

Initial Rotation
: Los valores iniciales de rotación (en grados) para las partículas.

Initial Stretch X/Y
: Los valores iniciales de estiramiento (en unidades) para las partículas.

Initial Angular Velocity
: La velocidad angular inicial (en grados/segundo) de cada partícula generada.

Las siguientes propiedades pueden animarse con claves durante el tiempo de vida de las partículas:

Life Scale
: El valor de escala a lo largo de la vida de cada partícula.

Life Red/Green/Blue/Alpha
: El valor de tinte del componente de color a lo largo de la vida de cada partícula.

Life Rotation
: El valor de rotación (en grados) a lo largo de la vida de cada partícula.

Life Stretch X/Y
: El valor de estiramiento (en unidades) a lo largo de la vida de cada partícula.

Life Angular Velocity
: La velocidad angular (en grados/segundo) a lo largo de la vida de cada partícula.

## Modificadores

Hay cuatro tipos de modificadores disponibles que afectan la velocidad de las partículas:

`Acceleration`
: Aceleración en una dirección general.

`Drag`
: Reduce la aceleración de las partículas proporcionalmente a la velocidad de la partícula.

`Radial`
: Atrae o repele partículas hacia/desde una posición.

`Vortex`
: Afecta a las partículas en una dirección circular o espiral alrededor de su posición.

  ![modificadores](images/particlefx/modifiers.png)

## Propiedades del modificador

Position/Rotation
: La transformación del modificador relativa a su padre.

Magnitude
: La cantidad de efecto que el modificador tiene sobre las partículas.

Max Distance
: La distancia máxima dentro de la cual las partículas se ven afectadas por este modificador. Solo se usa para Radial y Vortex.

## Controlar un efecto de partículas

Para iniciar y detener un efecto de partículas desde un script:

```lua
-- iniciar el componente de efecto de partículas "particles" en el objeto de juego actual
particlefx.play("#particles")

-- detener el componente de efecto de partículas "particles" en el objeto de juego actual
particlefx.stop("#particles")
```

Para iniciar y detener un efecto de partículas desde un script de GUI, consulta el [manual de Particle FX de GUI](/manuals/gui-particlefx#controlling-the-effect) para obtener más información.

::: sidenote
Un efecto de partículas continuará emitiendo partículas aunque se elimine el objeto de juego al que pertenecía el componente de efecto de partículas.
:::
Consulta la [documentación de referencia de Particle FX](/ref/particlefx) para obtener más información.

## Constantes de material

El material predeterminado de efecto de partículas tiene las siguientes constantes, que pueden cambiarse con `particlefx.set_constant()` y restablecerse con `particlefx.reset_constant()` (consulta el [manual de Material para más detalles](/manuals/material/#vertex-and-fragment-constants)):

`tint`
: El tinte de color del efecto de partículas (`vector4`). El vector4 se usa para representar el tinte con x, y, z y w, que corresponden a los tintes rojo, verde, azul y alfa. Consulta la [referencia de la API para ver un ejemplo](/ref/particlefx/#particlefx.set_constant:url-constant-value).


## Configuración del proyecto

El archivo *game.project* tiene algunas [opciones de configuración del proyecto](/manuals/project-settings#particle-fx) relacionadas con las partículas.
