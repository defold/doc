---
title: FAQ de Editor y motor Defold
brief: Preguntas frecuentes sobre el motor de videojuegos, editor y plataforma Defold.
---

# Preguntas Frecuentes

## Preguntas generales

#### Q: ¿Es Defold realmente gratuito?

A: Sí, el motor y editor Defold con toda su funcionalidad es completamente libre de cargos. No hay costos, cuotas o regalías escondidas. Solo gratis.


#### Q: ¿Por qué la Defold Foundation regalaría Defold?

A: Uno de los objetivos de [Defold Foundation](/foundation) es asegurarse que el software Defold esté disponible a desarrolladores globalmente y que el código fuente esté disponible libre de cargos.


#### Q: ¿Por cuánto tiempo soportarán Defold?

A: Estamos comprometidos profundamente con Defold. La [Defold Foundation](/foundation) ha sido establecida de una forma que esté garantizada su existencia como responsable de Defold por muchos años próximos. No se va a ir a ningún lado.


#### Q: ¿Puedo confiar en Defold para desarrollo profesional?

A: Absolutamente. Defold es usado por un creciente número de desarrolladores de videojuegos profesionales y estudios de videojuegos. Revisa el [games showcase](/showcase) para ejemplos de videojuegos desarrollados usando Defold.


#### Q: ¿Qué tipo de seguimiento de usuario utilizan?

A: Registramos datos de uso de manera anónima de nuestros sitios y el editor Defold para mejorar nuestros servicios y producto. No hay seguimiento de usuario en los juegos que desarrollas (al menos que añadas un servicio de analytics por tu cuenta). Lee más en nuestra [Política de privacidad](/privacy-policy).


#### Q: ¿Quién hizo Defold?

A: Defold fue creado por Ragnar Svensson y Christian Murray. Empezaron trabajando en el motor, editor y servidores in 2009. King y Defold empezaron una asociación en 2013 y King adquirió Defold en 2014. Lee la historia completa [aquí](/about).


#### Q: ¿Puedo hacer juegos 3D en Defold?

A: ¡Absolutamente! El motor es un motor 3D completo. Sin embargo, las herramientas fueron creadas para el 2D así que tendrás que hacer un montón de trabajo pesado. Un mejor soporte 3D está en planeación.


#### Q: ¿Qué lenguaje de programación utilizo en Defold?

A: La lógica del juego en tu proyecto Defold está escrita principalmente en el lenguaje Lua (específicamente Lua 5.1/LuaJIT, refiere al [manual Lua](/manuals/lua) para más detalles). Lua es un lenguaje dinámico ligero que es rápido y poderoso. También puedes usar lenguaje nativo (C/C++, Objective-C, Java and JavaScript dependiendo de la plataforma) para extender el motor Defold con nuevas funcionalidades. Cuando crees materiales personalizados, se utiliza OpenGL ES SL shader language para escribir vértices y fragmentos
shaders.


## Preguntas de Plataforma

#### Q: ¿En qué plataformas corre Defold?

A: Las siguientes plataformas tienen soporte para el editor/herramientas y el runtime del motor:

  | System             | Version            | Architectures      | Supported            |
  | ------------------ | ------------------ | ------------------ | -------------------- |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Editor               |
  | macOS              | 10.15              | `x86-64`, `arm-64` | Engine               |
  | Windows            | Vista              | `x86-32`, `x86-64` | Editor and Engine    |
  | Ubuntu (1)         | 18.04              | `x86-64`           | Editor               |
  | Linux (2)          | Any                | `x86-64`, `arm-64` | Engine               |
  | iOS                | 11.0               | `arm-64`           | Engine               |
  | Android            | 4.4 (API level 19) | `arm-32`, `arm-64` | Engine               |
  | HTML5              |                    | `asm.js`, `wasm`   | Engine               |

  (1 El editor fue creado y probad para 64-bit Ubuntu 18.04. Debe funcionar en otras distribuciones pero no damos garantía de ello.)

  (2 El engine runtime debe correr en la mayoría de distribuciones 64-bit de Linux mientras los drivers de gráficos estén actualizados y soporten OpenGL ES 2.0.)


#### Q: ¿Para qué plataformas objetivo puedo desarrollar con Defold?

A: Con un click puedes publicar en Nintendo Switch, iOS, Android y HTML5 así como macOS, Windows y Linux. Es realmente un código base con múltiples plataformas soportadas.


#### Q: ¿De cuál API de rendering depende Defold?

A: Defold utiliza WebGL en builds HTML5, Metal en iOS y macOS y Vulkan o OpenGL ES 2.0 en las otras plataformas. Como desarrollador solo tienes que preocuparte por un render API utilizando un rendering pipeline completamente codificable.


#### Q: ¿Hay alguna forma de saber qué versión estoy corriendo?

A: Si, selecciona la opción "About" en el menú Help. El popup muestra claramente la versión beta de Defold y, más importante, el release específico SHA1. Para la versión de runtime, usa [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

La última version beta disponible para descarga desde http://d.defold.com/beta puede revisarse abriendo http://d.defold.com/beta/info.json (el mismo archivo existe para versiones estables: http://d.defold.com/stable/info.json)


#### Q: ¿Hay alguna forma de saber en que plataforma está corriendo el juego?

A: Sí, checa [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Preguntas del Editor
:[Editor FAQ](../shared/editor-faq.md)


## Preguntas de Linux
:[Linux FAQ](../shared/linux-faq.md)


## Preguntas de Android
:[Android FAQ](../shared/android-faq.md)


## Preguntas de HTML5
:[HTML5 FAQ](../shared/html5-faq.md)


## Preguntas de IOS
:[iOS FAQ](../shared/ios-faq.md)


## Preguntas de Windows
:[Windows FAQ](../shared/windows-faq.md)


## Preguntas de Consoles
:[Consoles FAQ](../shared/consoles-faq.md)


## Publicando juegos

#### Q: Estoy tratando de publicar mi videojuego en la Appstore. ¿Cómo debo responder a IDFA?

A: Cuando estés presentando, Apple tiene tres checkboxes para sus tres usos válidos por el IDFA:

  1. Entregar anuncios desde la aplicación
  2. Instalar atribución desde anuncios
  3. Acción de usuario de anuncios

  Si seleccionas la opción un, el revisor de la aplicación buscará por anuncios dentro de la app. Si tu juego no muestra anuncios, el juego puede ser rechazado. Defold no usa AD id por sí mismo.


#### Q: ¿Cómo monetizo mi juego?

A: Defold tiene soporte para compras in-app y varias soluciones de anuncios. Checa la [categoría de Monetización en el Asset Portal](https://defold.com/tags/stars/monetization/) para una lista actualizada de opciones de monetización disponibles.


## Errores usando Defold

#### Q: No puedo iniciar el juego y no hay error de build. ¿Que pasó?

A: El proceso de build puede fallar al hacer rebuild en raras ocasiones donde ha encontrado previamente errores de build que hayas reparado. Forza un rebuild completo seleccionando *Project > Rebuild And Launch* desde el menú.



## Contenido del juego

#### Q: ¿Defold soporta prefabs?

A: Si, lo hace. Son llamadas [colecciones](/manuals/building-blocks/#collections). Permiten crear jerarquías de objetos complejas y guardarlos como un bloque de construcción separado que puedes instanciaren el editor o durante la ejecución (a través de la aparición de colección). Para nodos GUI existe soporte para plantillas GUI.


#### Q: No puedo agregar un objeto de juego como hijo de otro objeto de juego, ¿por qué?

A: Probablemente sea que trataste de añadir un hijo en el archivo de objeto de juego y eso no es posible. Para entender por qué, hay que recordar que las jerarquías padre-hijo son estrictamente una jerarquía de transformación del gráfico de la escena _(scene-graph_). Un objeto de juego que no se haya colocado (o aparecido) en una escena (colección) no es parte del gráfico de la escena y no puede ser parte de la jerarquía de éste.


#### Q: ¿Por quéno puedo transmitir mensajes a todos los hijos de un objeto de juego?

A: Las relaciones padre-hijo no expresan nada más que las relaciones de transformación scene-graph y no deben ser confundidas por agregados de orientación de objeto. Si intentas enfocarte en los datos de tu juego y como transformarlo de la mejor forma posible, encontrarás menor necesidad de enviar mensajes con datos de estado a demasiados objetos al mismo tiempo. En los casos donde necesites jerarquía de datos, éstos son construidos y mantenidos fácilmente en Lua.


#### Q: ¿Por qué experimento artefactos visuales alrededor de los bordes de mis sprites?

A: Eso es un artefacto visual llamado "sangrado de borde" (edge bleeding) donde los pixeles del borde de otros pixeles cercanos en un atlas sangran en la imagen asignada a tu sprite. La solución es acomodar los bordes de tus atlas de imágenes con columnas y filas extra de pixeles idénticos. Afortunadamente esto se puede hacer automáticamente en el editor de atlas de Defold. Abre el atlas y cambia el valor de *Extrude Borders* a 1.


#### Q: ¿Puedo entintar mis sprites o hacerlos transparente, o tengo que escribir mi propio shader?

A: El shader de sprites integrado que es usado por defecto en todos los sprites tienen un "tinte" constante definido:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: Si selecciono la coordenada z de un sprite a 100 no se renderiza. ¿Por qué?

A: La posición Z de un objeto de juego controla el orden del renderizado. Los valores bajos son dibujados antes de los valores más altos. En el script de render por defecto los objetos del juego con una profundidad del rango -1 a 1 son dibujados, cualquier cosa con el número más bajo o alto no serán dibujados. Puedes leer más sobre el script de render en la [documentación de Render](/manuals/render) oficial. En nodos GUI el valor Z es ignorado y no afecta el orden del renderizado. En lugar de eso los nodos son renderizados en el orden que son enlistados y de acuerdo a las jerarquías de los hijos (y por capas). Lee más sobre el renderizado de GUI y optimización de llamadas de dibujo (draw call) utilizando capas en la [documentación de GUI](/manuals/gui) oficial.


#### Q: ¿Cambiar la proyección del rango Z a -100 hasta 100 afectaría el rendimiento?

A: No. El único efecto es precisión. El buffer Z es logarítmico y tiene una resolución muy fina de valores z cercanos a 0 y menos resolución más lejano al 0. Por instancia, con un buffer de 24 bits los valores 10.0 y 10.000005 pueden ser diferenciados mientras 10000 y 10005 no pueden.


#### Q: No hay consistencia en la representación de los ángulos. ¿Por qué?

A: De hecho, sí hay consistencia. Los ángulos están expresados en grados en todo el editor y el API del juego. Las librerías del videojuego utilizan radianes. Recientemente la convención rompe las físias de la propiedad `angular_velocity`  que son expresadas en radianes/s. Se espera un cambio.


#### Q: Cuando se crea un nodo caja (box-node) GUI con solo un color (sin textura), ¿cómo será renderizado?

A: Solo es una forma con color de vértice. Ten en cuenta que aún costará un nivel de servicio (fill-rate)


#### Q: Si cambio assets en el momento, ¿el motor los descargará al momento?

A: Todos los recursos son contados por referencia de manera interna. Tan pronto el contador de referencia llegue a cero, el recurso es liberado.


#### Q: ¿Es posible reproducir un audio sin el uso de un componente de audio adjuntado a un objeto?

A: Todo está basado por componente. Es posible crear un objeto sin cabeza con múltiples sonidos y reproducir sonidos que envien mensajes al objeto controlador de sonido.


#### Q: ¿Es posible cambiar el archivo de audio asociado con un componente de audio en ejecución?

A: En general todos los recursos están estadísticamente declarados con el beneficio que obtienes control de recursos de manera libre. Puedes usar las [propiedades de recursos](/manuals/script-properties/#resource-properties) para cambiar qué recurso es asignado al componente.


#### Q: ¿Hay una forma de accesar a las propiedades de la forma de colisión de físicas?

A: No, por el momento no es posible.


#### Q: ¿Hay alguna forma rápida de renderizar los objetos colisionadores en mi escena? (como Box2D's debugdraw)

A: Si, utiliza la bandera *physics.debug* en *game.project*. (Refiere a la [documentación de opciones del proyecto](/manuals/project-settings/#debug) oficial).


#### Q: ¿Cuáles son los costos de rendimiento por tener muchos contactos/colisiones?

A: Defold utiliza una versión modificada de Box2D en el fondo y el costo de rendimiento debe ser similar. Siempre puedes ver cuánto tiempo el motor tarda en las físicas sacando el [profiler](/manuals/debugging). También deberías considerar que tipo de colisiones usas. Objetos estáticos utilizan menos rendimiento, por ejemplo. Refiere a la [documentación de Físicas](/manuals/physics) en Defold para más detalles.


#### Q: ¿Cuál es el impacto en el rendimiento por tener muchos componentes de efectos de partículas?

A: Depende de si están reproduciéndose o no. Un ParticleFx que no esté reproduciendo no tiene costo en el rendimiento. La implicación del rendimiento por reproducir ParticleFx debe ser evaluada usando el profiler pues su impacto depende en cómo está configurado. Como lo es con muchas otras cosas la memoria está asignada en el frente por el número de ParticleFx definido como max_count en *game.project*.


#### Q: ¿Cómo recibo input a un objeto del juego dentro de una colección cargada por un proxy de colección?

A: Cada proxy de colección cargado tiene su propio input stack. El Input está enrutado desde el input stack de la colección principal por el componente de proxy a los objetos en la colección. Esto significa que no es suficiente para el objeto del juego cargado en la colección el adquirir enfoque en el input, el objeto que aún mantiene _(holds_) el componente proxy necesita adquirir el enfoque de input también. Mira la [documentación de Input](/manuals/input) para más detalles.


#### Q: ¿Puedo usar propiedades de script de tipo string?

A: No. Defold soporta propiedades de tipo [hash](/ref/builtins#hash). Éstas pueen ser usadas para indicar tipos, identificadores de estado o claves de cualquier tipo. Los Hashes también pueden ser usados para guardar id's de objeto (paths) pero propiedades de [url](/ref/msg#msg.url) son usualmente prefereidas ya que el editor automáticamente puebla un desplegable con URLs relevantes para ti. Ver la [documentación de propiedades de Script](/manuals/script-properties) para más detalles.


#### Q: ¿Cómo acceso a las células individuales de una matrix? (creadas usando [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) o similares)?

A: Accesas a las células usando `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` etc


#### Q: Estoy teniendo `Not enough resources to clone the node` cuando uso [gui.clone()](/ref/gui/#gui.clone:node) o [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

A: Incrementa el valor de `Max Nodes` del componente gui. Encontrarás este valor en el panel Properties cuando selecciones la raíz del componente en el Outline.


## El foro

#### Q: ¿Puedo postear un hilo donde anuncie mi trabajo?

A: ¡Por supuesto! Tenemos una [categoría "Work for hire"](https://forum.defold.com/c/work-for-hire) para eso. Siemprealentamos todo y eso benefica a la comunidad, y ofreciendo tus servicios a la comunidad---por remuneración o no---es un buen ejemplo.


#### Q: He creado un hilo y añadí mi trabajo-¿puedo añadir más?

A: En orden para reducir el revivir hilos de "Work for hire", no deberías postear por más de una vez cada 14 días en tu propio hilo (al menos que sea una respuesta directa a un comentario en el hilo, en ese caso puedes responder). Si deseas añadir material adicional de tu trabajo dentro de los 14 días, puedes editar posts existentes con tu contenido añadido.


#### Q: ¿Puedo usar la categoría Work for Hire para postear ofertas de trabajo?

A: Seguro, ¡dense el gusto! Puede ser usado para ofertas así como pedidos, ej. "Programador buscando 2d pixel artist; soy rico y te pagaré bien".
