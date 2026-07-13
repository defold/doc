---
title: Tutorial de shader de grading
brief: En este tutorial crearás un post effect de pantalla completa en Defold.
---

# Tutorial de grading

En este tutorial vamos a crear un post effect de color grading a pantalla completa. El método básico de renderizado usado se puede aplicar ampliamente a varios tipos de post effects como blur, trails, glow, ajustes de color, etc.

Se asume que sabes moverte por el editor Defold y que tienes una comprensión básica de shaders GL y del rendering pipeline de Defold. Si necesitas leer sobre estos temas, consulta [nuestro manual de Shader](/manuals/shader/) y el [manual de Render](/manuals/render/).

## Render targets

Con el render script predeterminado, cada componente visual (sprite, tilemap, efecto de partículas, GUI, etc.) se renderiza directamente al *frame buffer* de la tarjeta gráfica. El hardware hace entonces que los gráficos aparezcan en la pantalla. El dibujo real de los pixels de un componente lo realiza un *shader program* GL. Defold incluye un shader program predeterminado para cada tipo de componente, que dibuja los datos de pixel en la pantalla sin modificarlos. Normalmente, este es el comportamiento que quieres---tus imágenes deberían aparecer en pantalla tal como fueron concebidas originalmente.

Puedes reemplazar el shader program de un componente por uno que modifique los datos de pixel, o que cree colores de pixel completamente nuevos de forma programática. El [tutorial Shadertoy](/tutorials/shadertoy) te enseña cómo hacerlo.

Ahora supongamos que quieres renderizar todo tu juego en blanco y negro. Una solución posible es modificar el shader program individual para cada tipo de componente de modo que cada shader desature los colores de pixel. Actualmente, Defold incluye 6 materiales integrados y 6 pares de programas de vertex y fragment shader, así que requerirá bastante trabajo. Además, cualquier cambio posterior o agregado de efectos debe hacerse en cada shader program.

Un enfoque mucho más flexible es hacer el renderizado en dos pasos separados:

![Render target](images/grading/render_target.png)

1. Dibuja todos los componentes como de costumbre, pero dibújalos en un buffer fuera de pantalla en lugar del frame buffer habitual. Esto se hace dibujando a algo llamado *render target*.
2. Dibuja un polígono cuadrado al frame buffer y usa los datos de pixel almacenados en el render target como fuente de textura del polígono. Asegúrate también de que el polígono cuadrado se estire para cubrir toda la pantalla.

Con este método, podemos leer los datos visuales resultantes y modificarlos antes de que lleguen a la pantalla. Al agregar shader programs al paso 2 anterior, podemos lograr fácilmente efectos de pantalla completa. Veamos cómo configurar esto en Defold.

## Configurar un renderer personalizado

Necesitamos modificar el render script integrado y agregar la nueva funcionalidad de renderizado. El render script predeterminado es un buen punto de partida, así que empieza copiándolo:

1. Copia */builtins/render/default.render_script*: en la vista *Asset*, haz click derecho en *default.render_script*, selecciona <kbd>Copy</kbd>, luego haz click derecho en *main* y selecciona <kbd>Paste</kbd>. Haz click derecho en la copia y selecciona <kbd>Rename...</kbd> y dale un nombre adecuado, como "grade.render_script".
2. Crea un nuevo archivo render llamado */main/grade.render* haciendo click derecho en *main* en la vista *Asset* y seleccionando <kbd>New ▸ Render</kbd>.
3. Abre *grade.render* y define su propiedad *Script* como "/main/grade.render_script".

   ![grade.render](images/grading/grade_render.png)

4. Abre *game.project* y define *Render* como "/main/grade.render".

   ![game.project](images/grading/game_project.png)

Ahora el juego está configurado para ejecutarse con un nuevo render pipeline que podemos modificar. Para probar que el motor usa nuestra copia del render script, ejecuta el juego, luego haz una modificación en el render script que dé un resultado visual y recarga el script. Por ejemplo, puedes deshabilitar el dibujo de tiles y sprites, luego presionar <kbd>⌘ + R</kbd> para hacer hot-reload del render script "roto" en el juego en ejecución:

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Comenta el dibujo del predicado "tile", que incluye todos los sprites y tiles. Esta línea de código se puede encontrar alrededor de la línea 33 en el archivo de render script.

Si los sprites y tiles desaparecen con esta prueba simple, sabes que el juego ejecuta tu render script. Si todo funciona como se espera, puedes deshacer el cambio al render script.

## Dibujar a un target fuera de pantalla

Ahora, modifiquemos el render script para que dibuje al render target fuera de pantalla en lugar del frame buffer. Primero necesitamos crear el render target:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 0)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 0)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Configura parámetros de buffer de color para el render target. Usamos la resolución objetivo del juego.
2. Crea el render target con los parámetros de buffer de color.

Ahora solo necesitamos envolver el código de renderizado original con `render.set_render_target()` así:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Habilita el render target. Desde ahora, cada llamada a `render.draw()` dibujará en los buffers de nuestro render target fuera de pantalla.
2. Todo el código de dibujo original en `update()` se deja tal cual, salvo el viewport, que se define a la resolución del render target.
3. En este punto, todos los gráficos del juego se han dibujado al render target. Así que es momento de deshabilitarlo definiendo el render target predeterminado.

Eso es todo lo que necesitamos hacer. Si ejecutas el juego ahora, dibujará todo al render target. Pero como ahora no dibujamos nada al frame-buffer, solo veremos una pantalla negra.

## Algo con qué llenar la pantalla

Para dibujar los pixels del buffer de color del render target en la pantalla, necesitamos configurar algo que podamos texturizar con los datos de pixel. Para ese propósito vamos a usar un modelo 3D plano y cuadrático.

1. Abre *`main.collection`* y crea un nuevo objeto de juego llamado "`grade`".
2. Agrega un componente Model al objeto de juego "`grade`".
3. Define la propiedad *Mesh* del componente model como el archivo *`quad.gltf`* que se encuentra en `builtins/assets/meshes`.

Deja el objeto de juego sin escalar en el origen. Más tarde, cuando rendericemos el quad, lo proyectaremos para que llene toda la pantalla. Pero primero necesitamos un material y shader programs para el quad:

1. Crea un material nuevo y llámalo *`grade.material`* haciendo click derecho en *main* en la vista *Asset* y seleccionando <kbd>New ▸ Material</kbd>.
2. Crea un vertex shader program llamado *`grade.vp`* y un fragment shader program llamado *`grade.fp`* haciendo click derecho en *main* en la vista *Asset* y seleccionando <kbd>New ▸ Vertex program</kbd> y <kbd>New ▸ Fragment program</kbd>.
3. Abre *grade.material* y define las propiedades *Vertex program* y *Fragment program* a los nuevos archivos de shader program.
4. Agrega una *Vertex constant* llamada "`view_proj`" de tipo `CONSTANT_TYPE_VIEWPROJ`. Esta es la matriz de vista y proyección usada en el vertex program para los vértices del quad.
5. Agrega un *Sampler* llamado "`original`". Se usará para muestrear pixels desde el buffer de color del render target fuera de pantalla.
6. Agrega un *Tag* llamado "`grade`". Crearemos un nuevo *render predicate* en el render script que coincida con este tag para dibujar el quad.

   ![grade.material](images/grading/grade_material.png)

7. Abre *`main.collection`*, selecciona el componente model en el objeto de juego "`grade`" y define su propiedad *Material* como "`/main/grade.material`".

   ![model properties](images/grading/model_properties.png)

8. El vertex shader program se puede dejar como se crea desde la plantilla base:

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // las posiciones están en espacio del mundo
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. En el fragment shader program, en lugar de definir `gl_FragColor` directamente al valor de color muestreado, hagamos una manipulación de color simple. Hacemos esto principalmente para asegurarnos de que todo funcione como se espera hasta ahora:

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desatura el color muestreado desde la textura original
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Ahora tenemos el modelo quad en su lugar con su material y shaders. Solo tenemos que dibujarlo al frame buffer de la pantalla.

## Texturizar con el buffer fuera de pantalla

Necesitamos agregar un render predicate al render script para poder dibujar el modelo quad. Abre *`grade.render_script`* y edita la función `init()`:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Agrega un nuevo predicado que coincida con el tag "grade" que definimos en *`grade.material`*.

Después de que el buffer de color del render target se haya llenado en `update()`, configuramos una vista y una proyección que hacen que el modelo quad llene toda la pantalla. Luego usamos el buffer de color del render target como textura del quad:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Limpia el frame buffer. Ten en cuenta que la llamada anterior a `render.clear()` afecta al render target, no al frame buffer de la pantalla.
2. Define el viewport para que coincida con el tamaño de la ventana.
3. Define la vista a la matriz identidad. Esto significa que la cámara está en el origen mirando recto a lo largo del eje Z. También define la proyección a la matriz identidad, haciendo que el quad se proyecte plano a lo largo de toda la pantalla.
4. Define el slot de textura 0 al buffer de color del render target. Tenemos el sampler "original" en el slot 0 en nuestro *`grade.material`*, así que el fragment shader muestreará desde el render target.
5. Dibuja el predicado que creamos, que coincide con cualquier material con el tag "grade". El modelo quad usa *`grade.material`*, que define ese tag---por lo tanto, el quad se dibujará.
6. Después de dibujar, deshabilita el slot de textura 0, ya que terminamos de dibujar con él.

Ahora ejecutemos el juego y veamos el resultado:

![desaturated game](images/grading/desaturated_game.png)

## Color grading

Los colores se expresan como valores de tres componentes donde cada componente dicta la cantidad de rojo, verde o azul de la que consta un color. El espectro completo de color desde negro, pasando por rojo, verde, azul, amarillo y rosa hasta blanco puede encajar en una forma de cubo:

![color cube](images/grading/color_cube.png)

Cualquier color que se pueda mostrar en pantalla puede encontrarse en este cubo de color. La idea básica del color grading es usar un cubo de color así, pero con colores alterados, como una *lookup table* 3D.

Para cada pixel:

1. Busca la posición de su color en el cubo de color (según los valores rojo, verde y azul).
2. *Lee* qué color tiene almacenado el cubo graded en esa ubicación.
3. Dibuja el pixel en el color leído en lugar del color original.

Podemos hacer esto en nuestro fragment shader:

1. Muestrea el valor de color para cada pixel en el buffer fuera de pantalla.
2. Busca la posición del color del pixel muestreado en un cubo de color con color grading.
3. Define el color de fragmento de salida al valor buscado.

![render target grading](images/grading/render_target_grading.png)

## Representar la lookup table

Open GL ES 2.0 no soporta texturas 3D, así que necesitamos encontrar otra forma de representar el cubo de color 3D. Una forma común de hacerlo es cortar el cubo a lo largo del eje Z (azul) y poner cada corte lado a lado en una cuadrícula bidimensional. Cada uno de los 16 cortes contiene una cuadrícula de 16⨉16 pixels. Almacenamos esto en una textura que podemos leer desde el fragment shader con un sampler:

![lookup texture](images/grading/lut.png)

La textura resultante contiene 16 celdas (una por cada intensidad de color azul) y dentro de cada celda 16 colores rojos a lo largo del eje X y 16 colores verdes a lo largo del eje Y. La textura representa todo el espacio de color RGB de 16 millones de colores en solo 4096 colores---apenas 4 bits de profundidad de color. Según la mayoría de los estándares esto es malo, pero gracias a una funcionalidad del hardware gráfico GL podemos recuperar una precisión de color muy alta. Veamos cómo.

## Buscar colores

Buscar un color consiste en comprobar el componente azul y averiguar qué celda elegir para los valores rojo y verde. La fórmula para encontrar la celda con el conjunto rojo-verde correcto es simple:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Aquí `B` es el valor del componente azul entre 0 y 1 y `N` es el número total de celdas. En nuestro caso, el número de celda estará en el rango `0`--`15`, donde la celda `0` contiene todos los colores con el componente azul en `0` y la celda `15` todos los colores con el componente azul en `1`.

Por ejemplo, el valor RGB `(0.63, 0.83, 0.4)` se encuentra en la celda que contiene todos los colores con un valor azul de `0.4`, que es la celda número 6. Sabiendo eso, la búsqueda de las coordenadas de textura finales según los valores verde y rojo es directa:

![lookup table](images/grading/lut_lookup.png)

Ten en cuenta que necesitamos tratar los valores rojo y verde `(0, 0)` como si estuvieran en el *centro* del pixel inferior izquierdo y los valores `(1.0, 1.0)` como si estuvieran en el *centro* del pixel superior derecho.

::: sidenote
La razón por la que leemos empezando en el centro del pixel inferior izquierdo y hasta el centro del pixel superior derecho es que no queremos que ningún pixel fuera de la celda actual afecte el valor muestreado. Consulta más abajo sobre filtering.
:::

Al muestrear en estas coordenadas específicas de la textura, vemos que terminamos justo entre 4 pixels. Entonces, ¿qué valor de color nos dirá GL que tiene ese punto?

![lookup table filtering](images/grading/lut_filtering.png)

La respuesta depende de cómo hayamos especificado el *filtering* del sampler en el material.

- Si el filtering del sampler es `NEAREST`, GL devolverá el valor de color del pixel más cercano (valor de posición redondeado hacia abajo). En el caso anterior, GL devolverá el valor de color en la posición `(0.60, 0.80)`. Para nuestra textura de lookup de 4 bits, significa que cuantizaremos los valores de color en solo 4096 colores en total.

- Si el filtering del sampler es `LINEAR`, GL devolverá el valor de color *interpolado*. GL mezclará un color según la distancia a los pixels alrededor de la posición de muestreo. En el caso anterior, GL devolverá un color que es 25% de cada uno de los 4 pixels alrededor del punto de muestreo.

Al usar filtering lineal eliminamos así la cuantización de color y obtenemos muy buena precisión de color a partir de una lookup table bastante pequeña.

## Implementar la búsqueda

Implementemos la búsqueda de textura en el fragment shader:

1. Abre *`grade.material`*.
2. Agrega un segundo sampler llamado "`lut`" (por lookup table).
3. Define la propiedad *`Filter min`* como `FILTER_MODE_MIN_LINEAR` y la propiedad *`Filter mag`* como `FILTER_MODE_MAG_LINEAR`.

    ![lookup table sampler](images/grading/material_lut_sampler.png)

4. Descarga la siguiente textura de lookup table (*`lut16.png`*) y agrégala a tu proyecto.

    ![16 colors lookup table](images/grading/lut16.png)

5. Abre *`main.collection`* y define la propiedad de textura *`lut`* con la textura de lookup descargada.

    ![quad model lookup table](images/grading/quad_lut.png)

6. Finalmente, abre *`grade.fp`* para que podamos agregar soporte para la búsqueda de color:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Declara el sampler `lut`.
    2. Constantes para el color máximo (15, ya que empezamos desde 0), número de colores por canal y ancho y alto de la textura de lookup.
    3. Muestrea un color de pixel (llamado `px`) desde la textura original (el buffer de color del render target fuera de pantalla).
    4. Calcula desde qué celda leer color según el valor del canal azul de `px`.
    5. Calcula offsets de medio pixel para leer desde los centros de pixel.
    6. Calcula el offset X e Y en la textura según los valores rojo y verde de `px`.
    7. Calcula la posición final de muestreo en la textura de lookup.
    8. Muestrea el color resultante desde la textura de lookup.
    9. Define el color en la textura del quad al color resultante.

Actualmente, la textura de lookup table solo devuelve los mismos valores de color que buscamos. Esto significa que el juego debería renderizarse con su coloración original:

![world original look](images/grading/world_original.png)

Hasta ahora parece que hicimos todo bien, pero hay un problema oculto bajo la superficie. Mira qué ocurre cuando agregamos un sprite con una textura de prueba en gradiente:

![blue banding](images/grading/blue_banding.png)

El gradiente azul muestra unas bandas realmente feas. ¿Por qué ocurre eso?

## Interpolar el canal azul

El problema con las bandas en el canal azul es que GL no puede realizar ninguna interpolación del canal azul al leer el color desde la textura. Preseleccionamos una celda particular para leer según el valor de color azul, y eso es todo. Por ejemplo, si el canal azul contiene un valor en cualquier punto del rango `0.400`--`0.466`, el valor no importa---siempre muestrearemos el color final desde la celda número 6, donde el canal azul está definido en `0.400`.

Para obtener mejor resolución en el canal azul, podemos implementar nosotros mismos la interpolación. Si el valor azul está entre el valor de dos celdas adyacentes, podemos muestrear desde ambas celdas y luego mezclar los colores. Por ejemplo, si el valor azul es `0.420`, deberíamos muestrear desde la celda número 6 *y* desde la celda número 7 y luego mezclar los colores.

Entonces, deberíamos leer desde dos celdas:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

y:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Luego muestreamos valores de color desde cada una de estas celdas e interpolamos los colores linealmente, según la fórmula:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Aquí `color`~low~ es el color muestreado desde la celda inferior (más a la izquierda) y `color`~high~ es el color muestreado desde la celda superior (más a la derecha). La función GLSL `mix()` realiza esta interpolación lineal por nosotros.

El valor `C~frac~` anterior es la parte fraccionaria del valor del canal azul escalado al rango de color `0`--`15`:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

De nuevo, hay una función GLSL que nos da la parte fraccionaria de un valor. Se llama `frac()`. La implementación final en el fragment shader (*`grade.fp`*) es bastante directa:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Calcula las dos celdas adyacentes desde las que leer.
2. Calcula dos posiciones de lookup separadas, una para cada celda.
3. Muestrea los dos colores desde las posiciones de celda.
3. Mezcla los colores linealmente según la fracción de `cell`, que es el valor de color azul escalado.

Ejecutar el juego otra vez con la textura de prueba ahora produce resultados mucho mejores. Las bandas en el canal azul desaparecieron:

![blue no banding](images/grading/blue_no_banding.png)

## Aplicar grading a la textura de lookup

Bien, fue mucho trabajo para dibujar algo que se ve exactamente como el mundo de juego original. Pero esta configuración nos permite hacer algo realmente genial. ¡Espera!

1. Toma una captura de pantalla del juego en su forma no afectada.
2. Abre la captura en tu programa favorito de manipulación de imágenes.
3. Aplica cualquier cantidad de ajustes de color (brillo, contraste, curvas de color, balance de blancos, exposición, etc., etc.).

![world in Affinity](images/grading/world_graded_affinity.png)

4. Aplica los mismos ajustes de color al archivo de textura de lookup table (*`lut16.png`*).
5. Guarda el archivo de textura de lookup table con los colores ajustados.
6. Reemplaza la textura *`lut16.png`* usada en tu proyecto Defold con la ajustada en color.
7. ¡Ejecuta el juego!

![world graded](images/grading/world_graded.png)

¡Qué alegría!
