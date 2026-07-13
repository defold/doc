---
title: Defold para usuarios de Unity
brief: Esta guía te ayuda a cambiar rápidamente a Defold si tienes experiencia previa con Unity. Cubre algunos de los conceptos clave usados en Unity y explica las herramientas y métodos correspondientes en Defold.
---

# Defold para usuarios de Unity

Si tienes experiencia previa con Unity, esta guía te ayuda a ser productivo rápidamente en Defold. Se centra en lo esencial y te dirige a los manuales oficiales de Defold cuando se necesitan detalles más profundos.

## Introducción

Defold es un motor de videojuegos 3D completamente gratuito y realmente multiplataforma, con un editor para Windows, Linux y macOS. El código fuente completo está disponible en [Github](https://github.com/defold/defold/).

Defold se centra en el rendimiento, incluso en dispositivos de gama baja. Usa un modelo de componentes pequeño donde muchas interacciones de la lógica del juego se gestionan mediante código y paso de mensajes.

Defold es mucho más pequeño que Unity. El tamaño del motor con un proyecto vacío está entre 1 y 3 MB en todas las plataformas. Puedes eliminar partes adicionales del motor y mover parte del contenido del juego a [Live Update](/manuals/live-update) para descargarlo por separado más tarde. En la [página Why Defold](https://defold.com/why/) se describe una comparación de tamaño y otras razones para elegir Defold.

Para personalizar Defold según tus necesidades, puedes escribir o usar elementos existentes:

1. Pipeline de renderizado completamente programable mediante scripts (script de render + materiales/shaders), con varios backends para elegir (OpenGL, Vulkan, etc.).
2. Código y componentes como Native Extensions (C++/C#).
3. Editor Scripts y widgets de interfaz para personalizar el editor.
3. Una build modificada del motor y del editor, ya que el código fuente completo y un pipeline de build están disponibles.

También recomendamos ver un video de Game From Scratch sobre [Defold para desarrolladores de Unity](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Instalación

1. Descarga Defold para tu sistema operativo.
2. Descomprímelo y ejecútalo.

Eso es todo. No hay hub, ni SDK adicional, ni toolchains ni bundles de plataforma que instalar. Por eso decimos que Defold tiene configuración cero.

Si necesitas más detalles, lee este breve [manual de instalación](/manuals/install/).

### Versiones

Defold se actualiza con frecuencia y no tiene una rama “LTS”. Recomendamos usar siempre la versión más nueva. Se publican versiones nuevas con regularidad, normalmente cada mes, con unas dos semanas de beta pública. Puedes actualizar Defold directamente desde el editor.

---

## Pantalla de bienvenida

Defold te recibe con una pantalla de bienvenida similar a Unity Hub, donde puedes abrir proyectos recientes:

![Welcome screen comparison](images/unity/unity_defold_start.png)

O iniciar uno nuevo desde:
- `Templates` - proyectos vacíos básicos para configurar más rápido una plataforma o género específico,
- `Tutorials` - recorridos guiados de aprendizaje que te ayudan a dar tus primeros pasos,
- `Samples` - casos de uso y ejemplos oficiales o aportados por la comunidad,

![Welcome Templates comparison](images/unity/unity_defold_templates.png)

Cuando crees tu primer proyecto y/o lo abras, se abrirá en el editor Defold.

## Hello World

Esta es una forma rápida de hacer algo en Defold: sigue los pasos y luego vuelve para leer el resto del manual.

1. Selecciona un proyecto vacío desde `Templates`, asígnale un nombre en `Title`, elige la ubicación y créalo haciendo click en `Create New Project`. Se abrirá en el editor Defold.
![Hello World Step 1](images/unity/helloworld_1.png)
2. En el lado izquierdo, en el panel `Assets`, abre la carpeta `main` y haz doble click en `main.collection` para abrirla.
3. En el lado derecho, en el panel `Outline`, haz click derecho en `Collection` y selecciona `Add Game Object`.
![Hello World Step 2](images/unity/helloworld_2.png)
4. Haz click derecho en el objeto de juego `go` creado, selecciona `Add Component` y luego `Label`.
![Hello World Step 3](images/unity/helloworld_3.png)
5. Abajo a la izquierda, en el panel `Properties`, escribe algo en la propiedad `Text`.
6. En la vista principal central de la escena, arrastra, mueve y suelta la label para colocarla alrededor de `(480,320,0)`, o cambia su posición en `Properties`: `Position`.
![Hello World Step 4](images/unity/helloworld_4.png)
7. Después de cambiar la posición de la label, guarda el proyecto haciendo click en `File` -> `Save All` o con el atajo <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> en Mac).
8. Crea la build del proyecto haciendo click en `Project` -> `Build` o con el atajo <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> en Mac).
![Hello World Step 5](images/unity/helloworld_5.png)

Acabas de crear la build de tu primer proyecto en Defold y deberías ver tu texto en la ventana. Los conceptos de objeto de juego y componente deberían resultarte familiares. Las colecciones, Outline, Properties y por qué tuvimos que mover la label un poco hacia arriba a la derecha se explican más abajo.

---

## Visión general del editor Defold

Presentaremos el editor Defold desde la perspectiva de lo que un usuario de Unity podría querer saber al principio, pero te recomendamos revisar después el [manual completo de visión general del editor](/manuals/editor).

### Comparación de editores

La primera diferencia que notarás entre Unity y Defold es el layout predeterminado del editor. Mostramos un Unity Editor con un layout ligeramente modificado para coincidir con el layout predeterminado de Defold. Están colocados uno junto al otro para facilitar la comparación visual de los paneles principales, ya que probablemente reconocerás con más facilidad las pestañas de Unity.

![Editor Comparison](images/unity/defold_unity_editor.png)

De forma predeterminada, el editor Defold se abre en una vista previa ortográfica 2D. Si vas a trabajar en un proyecto 3D, o simplemente quieres una experiencia más cercana a Unity, recomendamos cambiar de 2D a 3D desmarcando el toggle `2D` en la barra de herramientas y cambiar la proyección de la cámara a perspectiva marcando el toggle `Perspective`:

![Defold Toolbar](images/unity/defold_2d.png)

También puedes ajustar `Grid Settings` en la barra de herramientas para usar el plano `Y`, como en Unity:

![Defold 3D settings](images/unity/defold_3d.png)

### Visión general de los paneles de Defold

El editor Defold se divide en 6 paneles principales.

![Editor 2](images/editor/editor_overview.png)

A continuación se muestra una comparación de los nombres en Defold y las diferencias funcionales:

| Defold | Unity | Diferencias |
|---|---|---|
| 1. Assets | Project (Assets Browser) | En Defold, el panel Assets está acoplado a la izquierda. Defold no crea ningún archivo `meta`. |
| 2. Main Editor | Scene View | El editor Defold es sensible al contexto (editores diferentes para tipos de archivo diferentes), mientras que Unity usa ventanas especializadas separadas (por ejemplo, Animator, Shader Graph). Defold también tiene un editor de código integrado. |
| 3. Outline | Hierarchy | Defold refleja solo el archivo abierto actualmente o el elemento seleccionado (objeto de juego o componente), no una jerarquía global. |
| 4. Properties | Inspector | Defold muestra solo las propiedades de la **selección actual** en Outline, no las de todos los componentes del objeto de juego. |
| 5. Tools | Console | Defold ofrece herramientas en pestañas como Console, Curve Editor, Build Errors, Search Results, Breakpoints y Debugger. |
| 6. Changed Files | Unity Version Control (Plastic) | En Defold, cuando Git está integrado en tu proyecto, los archivos modificados se muestran aquí. Aun así, puedes usar Git externamente. |

Otros nombres útiles relacionados con el editor:

| Defold | Unity | Diferencias |
|---|---|---|
| Game Build | Game Preview | Muestra el juego en ejecución construido con el motor. Defold puede ejecutar varias instancias del juego desde el editor, de forma similar a Unity 6+ Multiplayer Play Mode. En Defold, el juego siempre se ejecuta en una ventana separada, no acoplada. Defold también puede ejecutar el juego en un dispositivo externo (por ejemplo, un teléfono móvil), de forma similar a Unity Remote. |
| Tabs | Tabs | Defold permite edición lado a lado en dos paneles dentro de la vista Main Editor. Las pestañas y paneles están acoplados dentro de una única ventana del editor; la visibilidad de los paneles se puede alternar (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>) y los tamaños de los paneles se pueden ajustar. |
| Toolbar | Toolbar / Scene View Options | Solo en versiones más recientes de Unity, las herramientas de transformación se han movido a la vista Scene, de forma similar a Defold. |
| Console | Console | La Console de Defold no se puede desacoplar. Los errores de build en Defold aparecen en una pestaña separada `Build Errors`. |
| Build Errors | Compilation Errors in Console | Los scripts Lua se interpretan, así que no hay errores de compilación. Sin embargo, tu proyecto se construye, y algunos errores pueden aparecer durante la build. Defold también usa un Lua Language Server para el análisis estático de scripts. |
| Search Results | Search / Project Search | El filtrado por tipos y etiquetas no está presente en Defold. |
| Curve Editor | Unity Curve Editor | El Curve Editor de Defold permite editar curvas solo para propiedades de efectos de partículas. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | El Debugger está completamente integrado en Defold desde el inicio. Hay una pestaña adicional para rastrear, habilitar y deshabilitar breakpoints. |

---

## Conceptos clave

Si generalizas lo suficiente, los conceptos clave detrás de la mayoría de los motores de videojuegos son muy similares. Están pensados para ayudar a los desarrolladores a construir juegos con más facilidad, como ensamblando bloques, mientras gestionan por sí mismos las tareas complejas y relacionadas con plataformas.

### Bloques de construcción

Defold funciona con solo unos pocos bloques de construcción básicos:

![Building blocks](images/unity/blocks.png)

Para más detalles, consulta el manual completo sobre los [bloques de construcción de Defold](/manuals/building-blocks/).

### Objetos de juego
Defold usa **objetos de juego (Game Objects)**, de forma similar a Unity. En ambos motores, los objetos de juego son contenedores de datos con un ID, y todos tienen transformaciones: posición, rotación y escala, pero en Defold la transformación está integrada en lugar de ser un componente separado.

Puedes crear relaciones padre-hijo entre objetos de juego. En Defold, esto solo puede hacerse en el editor dentro de una colección (Collection, explicada más abajo) o dinámicamente mediante script. Los objetos de juego no pueden contener otros objetos de juego como objetos anidados de la misma forma que en Unity.

### Componentes
En ambos motores, los objetos de juego se pueden extender con **componentes (Components)**. Defold proporciona un conjunto mínimo de componentes esenciales. Hay menos distinción entre 2D y 3D que en Unity (por ejemplo, colliders), así que hay menos componentes en total, y quizá eches de menos algunos de Unity.

#### Componentes de comportamiento

En Unity, "component" normalmente significa un `MonoBehaviour` que está adjunto a un `GameObject`. Puedes crear los tuyos heredando de `MonoBehaviour` o usar componentes integrados como Light, elementos de física, etc.

En Defold, Component se refiere exclusivamente a lo que sería el equivalente a los componentes integrados en Unity. Defold no trata un script como un MonoBehaviour y no requiere ninguna "marca" explícita para adjuntarlo a un objeto de juego, aparte de crear eventos/callbacks de escucha.

El comportamiento personalizado de la lógica del juego normalmente no se añade como muchos componentes script separados en el mismo objeto de juego. En su lugar, suele implementarse en módulos Lua y usarse desde un `.script` anfitrión, o gestionarse mediante un script de sistema más grande que controla muchos objetos. La sección sobre escritura de código más abajo lo cubre con más detalle.

Lee más sobre los [componentes de Defold aquí](/manuals/components/).

La tabla siguiente presenta componentes similares de Unity para una consulta rápida, con enlaces al manual de cada componente de Defold:

| Defold | Unity | Diferencias |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | En Defold, solo puedes cambiar el tinte (propiedad de color) mediante código. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold tiene un Tilemap Editor integrado que admite cuadrículas cuadradas (pero hay una extensión para, por ejemplo, [Hexagon](https://github.com/selimanac/defold-hexagon/)) y no tiene reglas integradas de autotiling. Herramientas como [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) o [Sprite Fusion](https://defold.com/assets/spritefusion/) tienen opciones de exportación a Defold. |
| [Label](/manuals/label/) | Text / TextMeshPro | Defold tiene una [extensión RichText](https://defold.com/assets/richtext/) para formato enriquecido (similar a TextMeshPro). |
| [Sound](/manuals/sound/) | AudioSource | Defold solo tiene una fuente de sonido global (no espacial). Hay una [extensión FMOD](https://github.com/defold/extension-fmod) oficial para Defold. |
| [Factory](/manuals/factory/) | Prefab Instantiate() | En Defold, una Factory es un componente con un prototipo específico (prefab). |
| [Collection Factory](/manuals/collection-factory/) | - (Sin equivalente directo de componente) | Un componente Collection Factory en Defold puede generar varios objetos de juego con relaciones padre-hijo a la vez. |
| [Collision Object](/manuals/physics-objects) | Rigidbody + Collider | En Defold, los objetos de física y las formas de colisión se combinan en un único componente. |
| [Collision Shapes](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | En Defold, las formas (caja, esfera, cápsula) se configuran dentro del componente Collision Object. Ambos admiten formas de colisión desde tilemaps y datos de convex hull. |
| [Camera](/manuals/camera/) | Camera | En Unity, la cámara tiene más ajustes integrados de renderizado y postprocesamiento, mientras que Defold delega esto al usuario para un control personalizado mediante el script de render. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defold GUI es un componente potente para construir interfaces completas y plantillas. Unity no tiene un componente único de interfaz equivalente, sino varios frameworks de interfaz. Defold también tiene una extensión para [Extension](https://github.com/britzl/extension-imgui). |
| [GUI Script](/manuals/gui-script/) | Unity UI / uGUI scripts | Defold GUI se puede controlar mediante GUI scripts usando la API dedicada `gui`. |
| [Model](/manuals/model/) | MeshRenderer + Material | En Defold, un componente Model agrupa un archivo de modelo 3D, texturas y un material con shaders. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | En Defold, Mesh es un componente para gestionar un conjunto de vértices mediante código. Es similar a un Model de Defold, pero todavía más bajo nivel. |
| [ParticleFX](/manuals/particlefx/) | Particle System | El editor de partículas de Defold admite efectos de partículas 2D/3D con muchas propiedades, y permite animarlas en el tiempo usando curvas en Curve Editor. No tiene Trails ni Collisions. |
| [Script](/manuals/script/) | Script | Más abajo se explican más detalles sobre las diferencias de programación. |

#### Extensiones y componentes personalizados

Defold también tiene componentes oficiales [Spine](/extension-spine/) y [Rive](/extension-rive/) disponibles mediante extensiones.

También puedes crear tus propios [componentes personalizados](https://github.com/defold/extension-simpledata) usando Native Extensions, como por ejemplo este [Object Interpolation Component](https://github.com/indiesoftby/defold-object-interpolation) creado por la comunidad.

Algunos componentes de Unity no tienen equivalente listo para usar en Defold, por ejemplo: Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth o Animator. Sin embargo, toda esta funcionalidad se puede implementar en scripts, y ya hay soluciones disponibles; por ejemplo, distintos pipelines de iluminación, el componente Mesh para generar meshes arbitrarios (incluido terreno) o [Hyper Trails](https://defold.com/assets/hypertrails/) para efectos de rastro personalizables. Defold también puede añadir nuevos componentes integrados en el futuro, como luces.

### Recursos

Algunos componentes requieren **recursos (Resources)**, de forma similar a Unity; por ejemplo, los sprites y modelos necesitan texturas. Algunos se comparan en la tabla siguiente:

| Defold | Unity | Diferencias |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold también tiene una [extensión para Texture Packer](https://defold.com/extension-texturepacker/). |
| [Tile source](/manuals/tilesource/) | Tile Palette + Asset | En Defold, un tile source puede usarse como textura para tilemaps, pero también para sprites o partículas. |
| [Font](/manuals/font/) | Font | Lo usa el componente Label de Defold o los nodos de texto en GUI, de forma similar a Text/TextMeshPro en Unity. |
| [Material](/manuals/material/) | Material | En Defold, los shaders se denominan: vertex program y fragment program. |

### Colección vs escena

En Defold, los objetos de juego y componentes pueden colocarse en archivos separados, como los prefabs de Unity, o definirse en un archivo **Collection** que los combina.

Una colección (Collection) en Defold es esencialmente un archivo de texto con una descripción estática de la escena. **No** es un objeto en tiempo de ejecución. Solo define qué objetos de juego deben instanciarse en el juego y cómo deben establecerse las relaciones padre-hijo entre esos objetos.

#### Mundos de juego

Las escenas de Unity comparten de forma predeterminada el mismo estado global del juego y la misma simulación de físicas, efectivamente el mismo *mundo* (*world*). En Defold tienes dos opciones:
1. Instanciar objetos de juego desde un único archivo de objeto de juego mediante una `Factory`, o desde un archivo de colección mediante una `Collection Factory`, en un *mundo* dado que ya ha sido instanciado, como prefabs.
2. Crear un *mundo* de juego separado en tiempo de ejecución, con sus propios objetos de juego, mundo de físicas, operaciones del motor y namespace de direccionamiento mediante una colección cargada en bootstrap o mediante un componente `Collection Proxy`.

Las fábricas y los componentes Proxy también se explican más abajo.
Lee más sobre las colecciones en el [manual de bloques de construcción](/manuals/building-blocks/#collections).

---

## Recursos y assets del proyecto

Unity y Defold almacenan el contenido del juego en el directorio del proyecto, pero difieren en cómo se rastrean y preparan los assets.

### Assets

Unity mantiene los assets en `Assets/` y genera archivos `.meta`. Defold no tiene archivos meta. El proyecto en Defold es solo tu estructura de carpetas, exactamente como en disco, y el panel `Assets` siempre la refleja.

### Formatos de recursos

Unity importa y convierte assets a otros formatos entre bastidores. En Defold, trabajas directamente con recursos fuente (`.png`, `.gltf`, `.wav`, `.ogg`, etc.) y los asignas a `Components`.

Unity puede usar una sola imagen como Sprite. En Defold, las imágenes pueden usarse directamente para Models/Meshes, pero Sprites/GUI/Tilemaps/Particles requieren un atlas (texturas empaquetadas) o un tilesource (tiles basados en cuadrícula).

La mayoría de los recursos de Defold se almacenan como texto, lo que resulta amigable para el control de versiones.

### Caché de biblioteca

Unity genera una carpeta `Library/` para los assets importados. Defold no tiene un directorio así; los assets se procesan durante las builds, con salidas en caché dentro de la carpeta de build (y cachés de build locales/remotas opcionales).

---

## Escritura de código

El equivalente en Defold a los scripts `MonoBehaviour` es un componente Script, pero hay algunas diferencias que conviene conocer.

### Lua

Los scripts de Defold se escriben en [Lua](https://www.lua.org/), un lenguaje dinámico y multiparadigma.

Hay varios tipos de scripts Lua: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` y módulos `*.lua`.

### Teal

Defold admite el uso de transpiladores que emiten código Lua, como [Teal](https://teal-language.org/), un dialecto de Lua con tipado estático, pero esta funcionalidad es más limitada y requiere configuración adicional. Los detalles están disponibles en el [repositorio de la extensión Teal](https://github.com/defold/extension-teal).

### C++/C# Native Extensions

En Defold, las Native Extensions pueden escribirse en varios otros lenguajes: C, C++, C#, Objective-C, Java o JS, según la plataforma objetivo. Si te sientes muy cómodo con C#, técnicamente es posible estructurar la mayor parte de la lógica del juego en una extensión C# y llamarla desde un pequeño script bootstrap en Lua, aunque esto requiere conocimientos avanzados de API y no se recomienda para principiantes.

Lee más sobre extensiones en el [manual de Native Extensions de Defold](/manuals/extensions/).


### De MonoBehaviours a módulos Lua

Unity tiene un modelo de scripting abierto. Como `MonoBehaviour` es la forma principal de añadir comportamiento en el editor, muchos proyectos de Unity empiezan con un script de estilo controlador por cada GameObject importante: `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager`, etc.

Defold es más específico sobre su arquitectura predeterminada. Un objeto de juego puede tener un `.script`, pero rara vez necesitas crear un script para cada objeto de juego, porque un único script en Defold puede controlar cientos o miles de otros objetos y sus componentes, incluso sin que tengan scripts propios, gracias al potente direccionamiento y paso de mensajes de Defold. Crear scripts que correspondan a cada objeto de juego rara vez es necesario y puede llevar a una complejidad contraproducente.

Para comportamientos reutilizables de la lógica del juego, los desarrolladores de Unity suelen acercarse a la composición: scripts `MonoBehaviour` más pequeños como `Health.cs`, `Attack.cs` o `EnemyFinder.cs` adjuntos al mismo GameObject. En Defold, normalmente mantienes un único `.script` adjunto como anfitrión o coordinador y colocas la lógica reutilizable en módulos Lua normales.

En Unity, esta composición podría verse así:

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

En Defold, las mismas responsabilidades suelen dividirse entre un script adjunto y módulos reutilizables:

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

El `.script` adjunto se convierte en el anfitrión o coordinador. Los módulos Lua contienen lógica reutilizable, de forma similar a como los scripts `MonoBehaviour` pequeños suelen contener una responsabilidad en Unity.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

La diferencia importante no es que Defold impida una arquitectura modular, sino dónde ocurre la composición y cómo se comunica el código de juego:

| Unity | Defold |
|---|---|
| Adjuntar varios scripts `MonoBehaviour` en el Inspector | Adjuntar un `.script` y componer módulos Lua en código |
| Usar `GetComponent<T>()` o campos serializados para conectar comportamientos | Guardar instancias de módulos en `self` y usar direcciones/mensajes entre objetos |
| Cada componente puede tener sus propios métodos de ciclo de vida | El script anfitrión enruta `init()`, `update()`, `on_message()`, `final()`, etc. |
| Son posibles muchos estilos arquitectónicos | La composición explícita en código y orientada a mensajes es la práctica común |

Esto puede resultar extraño al principio, sobre todo si estás acostumbrado a configurar comportamiento añadiendo componentes en el Inspector. En Defold, muchas cosas que quizá configurarías visualmente en Unity pueden crearse, conectarse, habilitarse, deshabilitarse o actualizarse mediante código. El sistema de mensajes de Defold ayuda a desacoplar la lógica: el remitente envía datos a una dirección y el receptor decide qué hacer con ellos.

Aunque este enfoque se recomienda, no se impone, y puedes escribir tus scripts como prefieras, incluyendo adjuntar varios scripts por objeto de juego o acercarte a un estilo de programación orientado a objetos. Incluso hay librerías que te ayudan con esto ([defold-oop](https://github.com/xiyoo0812/defold-oop) o [lua-class](https://github.com/d954mas/lua-class)).

Para muchos objetos del mismo tipo, como balas, enemigos, partículas, tiles o elementos interactivos simples, a menudo es mejor controlarlos desde un script de sistema o gestor en lugar de dar a cada objeto un script separado. Usa scripts por objeto cuando un objeto tenga su propio estado y comportamiento significativos. Usa módulos cuando quieras lógica reutilizable. Usa scripts de sistema cuando un script pueda controlar muchos objetos con eficiencia.

Puedes encontrar [aquí](https://defold.com/examples/factory/spawn_manager/) un ejemplo que muestra cómo utilizar propiedades de script, factories, direccionamiento y mensajes de Defold para controlar múltiples unidades.

Buenos manuales sobre escritura de código:
- [Manual de Script](/manuals/script/)
- [Escribir código](/manuals/writing-code/)
- [Depuración](/manuals/debugging/)


### Editor de código integrado

El editor Defold incluye un editor de código integrado con autocompletado, resaltado de sintaxis, consulta rápida de documentación, linting y un debugger integrado.

![Defold Code Editor](/images/editor/code-editor.png)

### VS Code y otros editores

Puedes seguir usando tu propio editor externo si lo prefieres. Todos los componentes de Defold y archivos relacionados están basados en texto, así que puedes editarlos con cualquier editor de texto, pero debes seguir el formato y la estructura de elementos adecuados, ya que están basados en Protobuf.

Si estás acostumbrado a VS Code y quieres usarlo para escribir el código de tu juego, recomendamos instalar [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) o [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) desde Visual Studio Marketplace.

También puedes configurar las preferencias del editor Defold para abrir archivos de texto de forma predeterminada en VS Code (o cualquier otro editor externo). Consulta [Editor Preferences](/manuals/editor-preferences/) para más detalles.

### Shaders - GLSL

Defold usa GLSL (OpenGL Shading Language) para shaders: `Vertex Programs` y `Fragment Programs`, de forma similar a Unity. Aunque Defold no ofrece un Shader Graph como Unity (lo que puede ser una desventaja), puedes crear shaders equivalentes escribiendo código.

Lee más sobre shaders en el [manual de Shaders](/manuals/shader).

#### Materiales

Defold usa un concepto de `Material` que conecta shaders `.fp` y `.vp`, samplers (texturas) y otras cosas como Vertex Attributes o Constants.

Lee más sobre materiales en el [manual de Materials](/manuals/material).

---

## Sistema de mensajes

En Defold, los objetos no mantienen referencias directas entre sí. No hay `GetComponent`, ni llamadas de métodos entre scripts de objetos distintos, ni acceso global a la escena como en Unity.

En su lugar, los scripts se comunican mediante paso de mensajes: envías mensajes a otros scripts, en lugar de llamar métodos o acceder a componentes directamente. Lo que esos objetos hagan con los mensajes depende de ellos.

Esto puede resultar desconocido al principio, pero fomenta un acoplamiento débil y reduce las interdependencias fuertes.


### Enviar un mensaje

En Unity, la comunicación suele verse así:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Así, los objetos pueden referenciarse directamente entre sí y llamar métodos en otros scripts. Todo existe en un único espacio de escena compartido.

En Defold envías un mensaje de un script a otro script (u otro componente):

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

Y puedes gestionar esos mensajes en script:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Ignora `#` y `hash` por ahora; llegaremos a eso más adelante. El resto debería ser sencillo. Puedes enviar un mensaje a cualquier componente (incluso al mismo script) de cualquier objeto de juego instanciado.

#### Componentes que no son scripts

A veces envías mensajes, por ejemplo, a componentes `Sprite` o `Collision`, para habilitarlos o deshabilitarlos. A veces `Components` envían mensajes a tu script, por ejemplo cuando ocurre una colisión, para que puedas gestionarla. Defold usa internamente el mismo sistema de mensajes para eventos del motor y comunicación de la lógica del juego.

El sistema de mensajes es algo similar a SendMessage o a los sistemas de eventos de Unity, aunque el direccionamiento y las convenciones difieren.

Puedes leer más detalles en el [manual de paso de mensajes](/manuals/message-passing/).

### Direccionamiento

Los objetos y componentes en Defold se identifican mediante direcciones, conocidas como URL.

Cada objeto y componente instanciado tiene su propia dirección única, y no necesitas recorrer un gráfico de la escena para encontrarlos. Esto hace que el direccionamiento sea explícito y directo.

Una URL simple en Defold podría verse así:
```lua
"/player"
```

Esto es *conceptualmente* similar a:
```c#
GameObject.Find("player")
```

Ahora es momento de explicar por qué se usaron `"/"` o `"#"` en las direcciones.

Una URL de Defold (similar a una [URL](https://en.wikipedia.org/wiki/URL)) consta de tres partes:

```yaml
socket: /path #fragment
```

o, descrito más según la nomenclatura de Defold:

```yaml
collection: /gameobject #component
```
Los espacios se añaden en las descripciones anteriores solo para separar visualmente esas 3 partes.

Dicho de forma simple:
1. `collection:` identifica el contexto de colección, con `:` al final.
2. `/path` identifica el objeto de juego, con `/` antes del ID.
3. `#fragment` identifica el componente específico en ese objeto (como un script, sprite o componente de colisión), con `#` antes del ID.

#### Dirección estática

Esos identificadores se determinan cuando se crea cada elemento y nunca cambian, aunque alteres las relaciones padre-hijo. Puedes configurarlos en la propiedad `Id` de los archivos, o los obtienes en tiempo de ejecución desde llamadas a `factory.create` o `collectionfactory.create` al instanciar.

#### Direccionamiento relativo

No siempre necesitas usar una URL completa.

Si envías mensajes dentro de la misma colección (el mismo *world*), puedes omitir la parte socket:

```yaml
/gameobject #component
```
Si envías a un componente dentro del mismo objeto de juego, también puedes omitir la parte del objeto de juego:

```yaml
#component
```

Dos atajos útiles son:
- `#` para enviar a este componente *Script*
- `.` para enviar a todos los componentes de este *objeto de juego*

El direccionamiento relativo y los atajos te permiten escribir URLs reutilizables en distintos contextos y objetos de juego sin especificar rutas completas.

### Mensajes a GUI y render

Como Defold separa el mundo de GUI del mundo de los objetos de juego, también puedes enviar mensajes desde tus `.scripts` de objeto de juego a `.gui_scripts`.

También puedes enviar mensajes a namespaces especiales del sistema usando un identificador que comienza con `@`. Por ejemplo, se puede direccionar el sistema de render mediante `@render`: y puedes usar esto para controlar ciertas funcionalidades de renderizado integradas, como cambiar la proyección en el script de render predeterminado:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Puedes encontrar más detalles en el [manual de direccionamiento](/manuals/addressing/).

---

## Prefabs e instancias

Unity puede instanciar cualquier cosa en la Scene de forma estática o dinámica, y Defold puede hacer lo mismo. En Unity tomas un Prefab y llamas a `Instantiate(prefab)`. En Defold tienes 3 componentes para instanciar contenido:

- `Factory` - instancia un **único objeto de juego** desde un prototipo dado: un archivo `*.go` (prefab).
- `Collection Factory` - instancia un **conjunto de objetos de juego** con relaciones padre-hijo desde un prototipo dado: un archivo `*.collection`.
- `Collection Proxy` - **carga** e instancia un nuevo *mundo* desde un archivo `*.collection`.

### Factory

Una vez que tienes un componente `Factory` definido con su propiedad `Prototype` establecida en el archivo de objeto de juego adecuado, generar una instancia es tan simple como llamar en código:

```lua
factory.create("#my_factory")
```

Esto usa la dirección del componente; en este caso, una ruta relativa usando el identificador `"#my_factory"`.

Devuelve el identificador de la instancia recién creada, así que si necesitas usarlo más tarde, vale la pena guardarlo en una variable:

```lua
local new_instance_id = factory.create("#my_factory")
```

Recuerda que en Defold no necesitas hacer pooling de objetos manualmente: el propio motor hace pooling internamente por ti.

Consulta más detalles en el [manual de Factory](/manuals/factory/).

### Collection Factory

La diferencia entre los componentes `Factory` y `Collection Factory` es que Collection Factory puede generar **varios** objetos de juego a la vez, y definir durante la creación las relaciones padre-hijo tal como están definidas en el archivo `*.collection`.

Esta distinción no existe en Unity; no tiene un concepto dedicado que coincida con Collection Factory de Defold. La analogía más cercana es simplemente un Prefab anidado que contiene una jerarquía de objetos.

Devuelve una **tabla** con los ids de todas las instancias generadas:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Consulta más detalles en el [manual de Collection Factory](/manuals/collection-factory/).

#### Propiedades personalizadas de instancias

Al llamar a `factory.create()` o `collectionfactory.create()`, también puedes especificar parámetros opcionales como posición, rotación, escala y propiedades de script, para controlar exactamente cómo y dónde aparece la instancia, y cómo se comporta, por ejemplo:

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

El orden de los argumentos opcionales es primero las propiedades y después la escala. Usa un `vector3` con Z definido explícitamente como `1.0` al escalar solo los ejes X e Y de un objeto 2D; una escala numérica se aplica uniformemente a los tres ejes.

#### Carga dinámica

En los componentes `Factory` y `Collection Factory` puedes marcar un Prototype para carga dinámica de recursos, de modo que sus assets pesados solo se carguen en memoria cuando se necesiten y se descarguen cuando ya no se usen.

Consulta más detalles en el [manual de gestión de recursos](/manuals/resource/).

### Collection Proxy

El `Collection Proxy` se refiere a un archivo `*.collection` específico, pero en lugar de inyectar los objetos en el *mundo actual* (como hacen las fábricas), **carga e instancia un nuevo mundo de juego**. Esto es algo similar a cargar una escena completa en Unity, pero con una separación más estricta.

En Unity podrías cargar una escena aditiva así:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

En Defold cargas la nueva colección simplemente enviando un mensaje al componente `Collection Proxy`:

```lua
msg.post("#myproxy", "load")
```

1. Cuando envías al proxy un mensaje `"load"` (o `"async_load"` para carga asíncrona), el motor asigna un nuevo mundo, instancia allí todo lo que hay en esa colección y lo mantiene aislado.
2. Una vez cargado, el proxy devuelve un mensaje `"proxy_loaded"` que indica que el mundo está listo.
3. Luego normalmente envías mensajes `"init"` y `"enable"` para que los objetos de ese nuevo mundo comiencen su ciclo de vida normal.

Para comunicarte entre los mundos cargados, tienes que usar mensajes explícitos con URLs que incluyan el nombre del mundo (`collection:`, la primera parte de la URL).

Este aislamiento puede ser una gran ventaja al implementar transiciones de nivel, minijuegos o sistemas modulares grandes, porque evita interacciones no intencionadas y también permite controlar por separado el momento de actualización si es necesario (por ejemplo, para pausa o cámara lenta).

Si alguna vez has usado varias escenas en Unity y necesitabas que se comportaran de forma independiente, piensa en un `Collection Proxy` como una forma de llevar ese concepto directamente a Defold.

Consulta más detalles en el [manual de Collection Proxy](/manuals/collection-proxy/).

---

## Ciclo de vida de la aplicación

Conoces un conjunto de eventos de ciclo de vida de Unity: `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` u `OnApplicationQuit`.

Defold también tiene un ciclo de vida de aplicación bien definido, pero los conceptos y la terminología difieren. Defold expone las etapas del ciclo de vida mediante un conjunto de callbacks Lua predefinidos que el motor llama durante la inicialización, cada fotograma y la finalización.

Aquí hay una comparación:

| Defold | Unity | Comentario |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold tiene un único punto de entrada y callback de inicialización: init(). Se llama en cada componente al crearse. |
| `on_input` | Input Methods | Defold recibe input cuando [el foco de input está establecido para el script](/manuals/input/#input-focus). Se procesa primero en el bucle de actualización. |
| `fixed_update()` | `FixedUpdate()` | Se llama a un timestep fijo. Para habilitarlo en Defold, tienes que establecer `Use Fixed Timestep`; [detalles](https://defold.com/manuals/project-settings/#use-fixed-timestep). Desde 1.12.0 se ejecuta antes de `update()`. |
| `update()` | `Update()` | Se llama una vez por fotograma con delta time. |
| `late_update()` | `LateUpdate()` | Se llama después de `update()`, justo antes de renderizar el fotograma. Disponible desde 1.12.0. |
| `on_message` | Message Receiver | Callback central de Defold para recibir mensajes. Se procesa cuando hay cualquier mensaje en una cola. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold llama a los callbacks `final()` de cada componente cuando su objeto de juego se destruye en tiempo de ejecución (usando `go.delete()`) o cuando el mundo/colección se descarga, y durante la terminación de la aplicación para todos los objetos restantes. |

::: sidenote
Recuerda que Defold no garantiza ningún orden de ejecución entre componentes cuando varios se inicializan, actualizan o eliminan a la vez. Se recomienda un diseño desacoplado.

### Inicialización

Piensa en `init()` de Defold como la combinación de elementos de `Awake()`, `Start()` y `OnEnable()` de Unity en un único punto de entrada donde el motor ya ha configurado todo y puedes preparar con seguridad el estado de tu componente.

### ¿Cuándo se gestionan los mensajes?

Como ya puedes enviar mensajes en `init()`, los mensajes se despachan primero justo después de la inicialización.

Luego los mensajes se gestionan después de cada bucle interno de procesamiento, cada vez que hay algo en una cola, por lo que `on_message()` puede llamarse, por ejemplo, incluso varias veces en un bucle de actualización.

### Bucle de actualización

Cada fotograma, Defold ejecuta una secuencia de operaciones: gestionar input, despachar mensajes, activar actualizaciones de scripts y GUI, aplicar físicas, transformaciones y, al final, renderizar gráficos.

### Finalización

En Defold, la limpieza siempre está ligada a la eliminación o descarga del mundo, y tu único punto de salida por componente es `final()`.

Una diferencia sutil respecto al modelo de Unity es que no hay distinción entre que un componente se deshabilite y que toda la aplicación se cierre.

### Renderizado

El script de render (`*.render_script`) forma parte del pipeline de renderizado, que también participa en el ciclo de vida con sus propios callbacks `init()`, `update()` y `on_message()`, pero operan en el hilo de render y están separados de la lógica de scripts de objetos de juego y GUI.

Para más detalles, lee el [manual de ciclo de vida de la aplicación](/manuals/application-lifecycle/).

---

## GUI

La GUI de Defold es un framework completo y dedicado para interfaces de usuario: menús, overlays, diálogos y otros elementos, similar a UI Toolkit o uGUI con Canvas.

GUI es un componente, y está separada de los objetos de juego y las colecciones. En lugar de Game Objects, trabajas con nodos GUI organizados en una jerarquía y controlados por un GUI script.

### Nodos GUI

Cuando abres un archivo de componente `*.gui` en Defold, se te presenta un lienzo donde colocas nodos GUI (`"GUI nodes"`). Estos son los bloques de construcción de la GUI. Puedes añadir nodos GUI de tipo:

- Box (forma rectangular con una textura)
- Text (con cualquier fuente)
- Pie (elemento radial de relleno en forma de porción circular con una textura)
- ParticleFX
- Template (otro archivo `.gui` completo anidado, como un prefab de GUI)
- y nodo Spine, al usar la extensión Spine.

### GUI Script

El componente GUI tiene una propiedad especial para GUI scripts: asignas un archivo `*.gui_script` por componente, y esto permite modificar el comportamiento del componente, así que es muy similar a los scripts normales, excepto que no usa el namespace `go.*` (que es para scripts de objetos de juego). En su lugar, usa una API especial del namespace `gui.*` que solo funciona dentro de GUI scripts (`*.gui_script`). Puedes pensarlo como una Scene separada, comparable a Unity UI (uGUI) con Canvas.

### Renderizado de GUI

Los elementos GUI se renderizan independientemente de la cámara del juego, normalmente en espacio de pantalla (screen-space), pero este comportamiento puede cambiarse en pipelines de renderizado personalizados.

Para más detalles, lee el [manual de GUI](/manuals/gui/).

## ¿Dónde están las Sorting Layers?

Esta es una confusión muy común al migrar desde Unity.

Los componentes GUI tienen `Layers` y esto funciona casi igual que las "Sorting Layers" en Unity, pero para otros componentes, como `Sprites`, `Tilemaps`, `Models`, etc., no hay un equivalente directo.

En su lugar, normalmente combinas:
- Orden fino mediante el eje Z al usar una cámara predeterminada, o profundidad al usar un componente Camera.
- Orden general mediante el script de render usando predicados de render, para seleccionar qué dibujar según etiquetas de material.

Pero no deberías imitar las Sorting Layers de Unity con muchas etiquetas, porque en Defold las etiquetas son un mecanismo a nivel de render. Usarlas en exceso puede romper el batching y aumentar la sobrecarga de dibujo.

---

## ¿A dónde ir desde aquí?

- [Ejemplos de Defold](/examples)
- [Tutoriales](/tutorials)
- [Manuales](/manuals)
- [Referencias de API](/ref/go)
- [FAQ](/faq/faq)

Si tienes preguntas o te atascas, el [foro de Defold](//forum.defold.com) o [Discord](https://defold.com/discord/) son excelentes lugares para pedir ayuda.
