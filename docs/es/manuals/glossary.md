---
title: Glosario de Defold
brief: Este manual enumera todo lo que encuentras al trabajar en Defold con una breve descripción.
---

# Glosario de Defold

Este glosario da una breve descripción de todas las cosas que encuentras en Defold. En la mayoría de los casos, encontrarás un enlace a documentación más detallada.

## Conjunto de animaciones (Animation set)

![Conjunto de animaciones](images/icons/animationset.png){.left} Un recurso animation set contiene una lista de archivos glTF u otros archivos .animationset desde los que leer animaciones. Agregar un archivo .animationset a otro resulta práctico si compartes conjuntos parciales de animaciones entre varios modelos. Consulta el [manual de animación de modelos](/manuals/model-animation/) para más detalles.

## Atlas

![Atlas](images/icons/atlas.png){.left} Un atlas es un conjunto de imágenes separadas que se compilan en una hoja más grande por motivos de rendimiento y memoria. Pueden contener imágenes fijas o series animadas de imágenes flipbook. Los atlas se usan en varios componentes para compartir recursos gráficos. Consulta la [documentación de Atlas](/manuals/atlas) para más información.

## Builtins

![Builtins](images/icons/builtins.png){.left} La carpeta de proyecto builtins es una carpeta de solo lectura que contiene recursos predeterminados útiles. Aquí encuentras el renderer predeterminado, el render script, materiales y más. Si necesitas modificaciones personalizadas en cualquiera de estos recursos, simplemente cópialos en tu proyecto y edítalos como prefieras.

## Cámara (Camera)

![Cámara](images/icons/camera.png){.left} El componente camera ayuda a decidir qué parte del mundo de juego debe ser visible y cómo debe proyectarse. Un caso de uso común es adjuntar una cámara al objeto de juego del jugador, o tener un objeto de juego separado con una cámara que sigue al jugador con algún algoritmo de suavizado. Consulta la [documentación de Camera](/manuals/camera) para más información.

## Objeto de colisión (Collision object)

![Objeto de colisión](images/icons/collision-object.png){.left} Los objetos de colisión son componentes que extienden los objetos de juego con propiedades físicas (como forma espacial, peso, fricción y restitución). Estas propiedades gobiernan cómo debe colisionar el objeto de colisión con otros objetos de colisión. Los tipos más comunes de objetos de colisión son objetos cinemáticos, objetos dinámicos y triggers. Un objeto cinemático da información detallada de colisión a la que debes responder manualmente; un objeto dinámico es simulado automáticamente por el motor de físicas para obedecer las leyes newtonianas de la física. Los triggers son formas simples que detectan si otras formas han entrado o salido del trigger. Consulta la [documentación de físicas](/manuals/physics) para más detalles sobre cómo funciona.

## Componente (Component)

Los componentes se usan para dar una representación específica y/o funcionalidad a los objetos de juego, como gráficos, animación, comportamiento programado y sonido. No tienen vida propia, sino que deben estar contenidos dentro de objetos de juego. Hay muchos tipos de componentes disponibles en Defold. Consulta [el manual de bloques de construcción](/manuals/building-blocks) para una descripción de los componentes.

## Colección (Collection)

![Colección](images/icons/collection.png){.left} Las colecciones son el mecanismo de Defold para crear plantillas, o lo que en otros motores se llama "prefabs", donde se pueden reutilizar jerarquías de objetos de juego. Las colecciones son estructuras de árbol que contienen objetos de juego y otras colecciones. Una colección siempre se almacena en un archivo y se introduce en el juego de forma estática al colocarla manualmente en el editor, o de forma dinámica mediante generación. Consulta [el manual de bloques de construcción](/manuals/building-blocks) para una descripción de las colecciones.

## Factory de colección (Collection factory)

![Factory de colección](images/icons/collection-factory.png){.left} Un componente factory de colección se usa para generar dinámicamente jerarquías de objetos de juego en un juego en ejecución. Consulta el [manual de factory de colección](/manuals/collection-factory) para más detalles.

## Proxy de colección (Collection proxy)

![Colección](images/icons/collection.png){.left} Un proxy de colección se usa para cargar y habilitar colecciones al vuelo mientras una app o juego se está ejecutando. El caso de uso más común para los proxies de colección es cargar niveles cuando van a jugarse. Consulta la [documentación de proxy de colección](/manuals/collection-proxy) para más detalles.

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} Un cubemap es un tipo especial de textura que consiste en 6 texturas diferentes que se mapean en los lados de un cubo. Esto es útil para renderizar skyboxes y distintos tipos de mapas de reflexión e iluminación.

## Depuración (Debugging)

En algún momento tu juego se comportará de una manera inesperada y necesitarás averiguar qué está mal. Aprender a depurar es un arte y, por suerte, Defold incluye un depurador integrado para ayudarte. Consulta el [manual de depuración](/manuals/debugging) para más información.

## Perfiles de visualización (Display profiles)

![Perfiles de visualización](images/icons/display-profiles.png){.left} El archivo de recurso display profiles se usa para especificar layouts de GUI según la orientación, la relación de aspecto o el modelo del dispositivo. Ayuda a adaptar tu interfaz a cualquier tipo de dispositivo. Lee más en el [manual de layouts](/manuals/gui-layouts).

## Factory

![Factory](images/icons/factory.png){.left} En algunas situaciones no puedes colocar manualmente todos los objetos de juego necesarios en una colección; tienes que crear los objetos de juego dinámicamente, al vuelo. Por ejemplo, un jugador podría disparar balas y cada disparo debería generarse dinámicamente y lanzarse cada vez que el jugador presiona el gatillo. Para crear objetos de juego dinámicamente (desde un pool preasignado de objetos), usas un componente factory. Consulta el [manual de factory](/manuals/factory) para más detalles.

## Fuente (Font)

![Archivo de fuente](images/icons/font.png){.left} Un recurso Font se construye a partir de un archivo de fuente TrueType u OpenType. Font especifica con qué tamaño se debe renderizar la fuente y qué tipo de decoración (contorno y sombra) debe tener la fuente renderizada. Las fuentes se usan en componentes GUI y Label. Consulta el [manual de Font](/manuals/font/) para más detalles.

## Shader de fragmentos (Fragment shader)

![Fragment shader](images/icons/fragment-shader.png){.left} Este es un programa que se ejecuta en el procesador gráfico para cada píxel (fragmento) de un polígono cuando se dibuja en la pantalla. El propósito del fragment shader es decidir el color de cada fragmento resultante. Esto se hace mediante cálculo, consultas de textura (una o varias) o una combinación de consultas y cálculos. Consulta el [manual de shaders](/manuals/shader) para más información.

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} Un archivo de recurso gamepads define cómo se mapea el input de un dispositivo gamepad específico a triggers de input de gamepad en una plataforma determinada. Consulta el [manual de input](/manuals/input) para más detalles.

## Objeto de juego (Game object)

![Objeto de juego](images/icons/game-object.png){.left} Los objetos de juego son objetos simples que tienen un tiempo de vida separado durante la ejecución de tu juego. Los objetos de juego son contenedores y normalmente están equipados con componentes visuales o audibles, como un sonido o un sprite. También pueden equiparse con comportamiento mediante componentes script. Creas objetos de juego y los colocas en colecciones en el editor, o los generas dinámicamente en tiempo de ejecución con factories. Consulta [el manual de bloques de construcción](/manuals/building-blocks) para una descripción de los objetos de juego.

## GUI

![Componente GUI](images/icons/gui.png){.left} Un componente GUI contiene elementos usados para construir interfaces de usuario: texto y bloques con color y/o textura. Los elementos pueden organizarse en estructuras jerárquicas, programarse con scripts y animarse. Los componentes GUI se usan normalmente para crear interfaces superpuestas, sistemas de menús y notificaciones en pantalla. Los componentes GUI se controlan con scripts GUI que definen el comportamiento de la GUI y controlan la interacción del usuario con ella. Lee más en la [documentación de GUI](/manuals/gui).

## Script GUI (GUI script)

![Script GUI](images/icons/script.png){.left} Los scripts GUI se usan para controlar el comportamiento de los componentes GUI. Controlan las animaciones de GUI y cómo interactúa el usuario con la GUI. Consulta el [manual de Lua en Defold](/manuals/lua) para más detalles sobre cómo se usan los scripts Lua en Defold.

## Recarga en caliente (Hot reload)

El editor Defold te permite actualizar contenido en un juego que ya se está ejecutando, en escritorio y dispositivo. Esta funcionalidad es extremadamente potente y puede mejorar mucho el flujo de trabajo de desarrollo. Consulta el [manual de hot reload](/manuals/hot-reload) para más información.

## Binding de input (Input binding)

![Binding de input](images/icons/input-binding.png){.left} Los archivos de binding de input definen cómo debe interpretar el juego el input de hardware (mouse, teclado, pantalla táctil y gamepad). El archivo enlaza el input de hardware a _acciones_ de input de alto nivel como "jump" y "move_forward". En componentes script que escuchan input puedes programar las acciones que el juego o app debe realizar dado cierto input. Consulta la [documentación de input](/manuals/input) para más detalles.

## Label

![Label](images/icons/label.png){.left} El componente label te permite adjuntar contenido de texto a cualquier objeto de juego. Renderiza un fragmento de texto con una fuente determinada, en pantalla, en el espacio del juego. Consulta el [manual de Label](/manuals/label) para más información.

## Biblioteca (Library)

![Objeto de juego](images/icons/builtins.png){.left} Defold te permite compartir datos entre proyectos mediante un potente mecanismo de bibliotecas. Puedes usarlo para configurar bibliotecas compartidas que sean accesibles desde todos tus proyectos, ya sea para ti o para todo el equipo. Lee más sobre el mecanismo de bibliotecas en la [documentación de bibliotecas](/manuals/libraries).

## Lenguaje Lua (Lua language)

El lenguaje de programación Lua se usa en Defold para crear lógica del juego. Lua es un lenguaje de scripting potente, eficiente y muy pequeño. Admite programación procedural, programación orientada a objetos, programación funcional, programación dirigida por datos y descripción de datos. Puedes leer más sobre el lenguaje en la página oficial de Lua en https://www.lua.org/ y en el [manual de Lua en Defold](/manuals/lua).

## Módulo Lua (Lua module)

![Módulo Lua](images/icons/lua-module.png){.left} Los módulos Lua te permiten estructurar tu proyecto y crear código de biblioteca reutilizable. Lee más sobre esto en el [manual de módulos Lua](/manuals/modules/)

## Material

![Material](images/icons/material.png){.left} Los materiales definen cómo deben renderizarse distintos objetos al especificar shaders y sus propiedades. Consulta el [manual de Material](/manuals/material) para más información.

## Mensaje (Message)

Los componentes se comunican entre sí y con otros sistemas mediante paso de mensajes. Los componentes también responden a un conjunto de mensajes predefinidos que los alteran o disparan acciones específicas. Envías mensajes para ocultar gráficos o empujar objetos físicos. El motor también usa mensajes para notificar eventos a los componentes, por ejemplo cuando las formas físicas colisionan. El mecanismo de paso de mensajes necesita un destinatario para cada mensaje enviado. Por lo tanto, todo en el juego tiene una dirección única. Para permitir la comunicación entre objetos, Defold extiende Lua con paso de mensajes. Defold también proporciona una biblioteca de funciones útiles.

Por ejemplo, el código Lua necesario para ocultar un componente sprite en un objeto de juego se ve así:

```lua
msg.post("#weapon", "disable")
```

Aquí, `"#weapon"` es la dirección del componente sprite del objeto actual. `"disable"` es un mensaje al que responden los componentes sprite. Consulta la [documentación de paso de mensajes](/manuals/message-passing) para una explicación detallada de cómo funciona el paso de mensajes.

## Modelo (Model)

![Modelo](images/icons/model.png){.left} El componente de modelo 3D puede importar assets de malla, esqueleto y animación glTF en tu juego. Consulta el [manual de Model](/manuals/model/) para más información.

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Las partículas son muy útiles para crear buenos efectos visuales, en especial en juegos. Puedes usarlas para crear niebla, humo, fuego, lluvia u hojas que caen. Defold contiene un potente editor de efectos de partículas que te permite crear y ajustar efectos mientras los ejecutas en tiempo real en tu juego. La [documentación de ParticleFX](/manuals/particlefx) te da los detalles sobre cómo funciona.

## Profiling

Un buen rendimiento es clave en los juegos, y es vital que puedas hacer profiling de rendimiento y memoria para medir tu juego e identificar cuellos de botella de rendimiento y problemas de memoria que deban corregirse. Consulta el [manual de Profiling](/manuals/profiling) para más información sobre las herramientas de profiling disponibles en Defold.

## Render

![Render](images/icons/render.png){.left} Los archivos Render contienen ajustes usados al renderizar el juego en la pantalla. Los archivos Render definen qué Render script se usa para renderizar y qué materiales se usan. Consulta el [manual de Render](/manuals/render/) para más detalles.

## Render script

![Render script](images/icons/script.png){.left} Un Render script es un script Lua que controla cómo debe renderizarse el juego o app en la pantalla. Hay un Render script predeterminado que cubre la mayoría de los casos comunes, pero puedes escribir el tuyo si necesitas modelos de iluminación personalizados y otros efectos. Consulta el [manual de Render](/manuals/render/) para más detalles sobre cómo funciona el render pipeline, y el [manual de Lua en Defold](/manuals/lua) para más detalles sobre cómo se usan los scripts Lua en Defold.

## Script

![Script](images/icons/script.png){.left} Un script es un componente que contiene un programa que define comportamientos de objetos de juego. Con scripts puedes especificar las reglas de tu juego y cómo deben responder los objetos a distintas interacciones (con el jugador y también con otros objetos). Todos los scripts se escriben en el lenguaje de programación Lua. Para poder trabajar con Defold, tú o alguien de tu equipo necesita aprender a programar en Lua. Consulta el [manual de Lua en Defold](/manuals/lua) para una visión general de Lua y detalles sobre cómo se usan los scripts Lua en Defold.

## Sonido (Sound)

![Sonido](images/icons/sound.png){.left} El componente sound es responsable de reproducir un sonido específico. Actualmente, Defold admite archivos de sonido en los formatos WAV y Ogg Vorbis. Consulta el [manual de Sound](/manuals/sound) para más información.

## Sprite

![Sprite](images/icons/sprite.png){.left} Un sprite es un componente que extiende los objetos de juego con gráficos. Muestra una imagen desde un Tile source o desde un Atlas. Los sprites tienen soporte integrado para animación flipbook y de huesos. Los sprites normalmente se usan para personajes y objetos.

## Perfiles de textura (Texture profiles)

![Perfiles de textura](images/icons/texture-profiles.png){.left} El archivo de recurso texture profiles se usa en el proceso de crear el bundle para procesar y comprimir automáticamente datos de imagen (en Atlas, Tile sources, Cubemaps y texturas independientes usadas para modelos, GUI, etc.). Lee más en el [manual de perfiles de textura](/manuals/texture-profiles).

## Tile map

![Tile map](images/icons/tilemap.png){.left} Los componentes Tile map muestran imágenes desde un tile source en una o más cuadrículas superpuestas. Se usan más comúnmente para construir entornos de juego: suelo, paredes, edificios y obstáculos. Un tile map puede mostrar varias capas alineadas una encima de otra con un modo de mezcla especificado. Esto es útil, por ejemplo, para poner follaje encima de tiles de fondo de césped. También es posible cambiar dinámicamente la imagen mostrada en un tile. Eso te permite, por ejemplo, destruir un puente y volverlo intransitable simplemente reemplazando los tiles por otros que representen el puente derrumbado y contengan la forma física correspondiente. Consulta la [documentación de Tile map](/manuals/tilemap) para más información.

## Tile source

![Tile source](images/icons/tilesource.png){.left} Un tile source describe una textura compuesta por múltiples imágenes más pequeñas, cada una con el mismo tamaño. Puedes definir animaciones flipbook a partir de una secuencia de imágenes en un tile source. Los tile sources también pueden calcular automáticamente formas de colisión a partir de datos de imagen. Esto es muy útil para crear niveles tileados con los que los objetos puedan colisionar e interactuar. Los tile sources son usados por componentes Tile map (y Sprite y ParticleFX) para compartir recursos gráficos. Ten en cuenta que los Atlas suelen encajar mejor que los tile sources. Consulta la [documentación de Tile map](/manuals/tilemap) para más información.

## Shader de vértices (Vertex shader)

![Vertex shader](images/icons/vertex-shader.png){.left} El vertex shader calcula la geometría en pantalla de las formas poligonales primitivas de un componente. Para cualquier tipo de componente visual, ya sea un sprite, tilemap o modelo, la forma se representa mediante un conjunto de posiciones de vértices de polígonos. El programa vertex shader procesa cada vértice (en espacio del mundo) y calcula la coordenada resultante que debe tener cada vértice de una primitiva. Consulta el [manual de shaders](/manuals/shader) para más información.
