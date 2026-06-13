---
title: Manual de materiales de Defold
brief: Este manual explica cómo trabajar con materiales, constantes de shader y samplers.
---

# Materiales

Los materiales se usan para expresar cómo se debe renderizar un componente gráfico (un sprite, tilemap, fuente, nodo GUI, modelo, etc.).

Un material contiene _tags_, información que se usa en el pipeline de renderizado para seleccionar los objetos que se van a renderizar. También contiene referencias a _programas de shader_ que se compilan mediante el driver gráfico disponible, se suben al hardware gráfico y se ejecutan cuando el componente se renderiza en cada frame.

* Para obtener más información sobre el pipeline de render, consulta la [documentación de Render](/manuals/render).
* Para una explicación detallada de los programas de shader, consulta la [documentación de Shader](/manuals/shader).

## Crear un material

Para crear un material, haz <kbd>click derecho</kbd> en una carpeta objetivo en el explorador *Assets* y selecciona <kbd>New... ▸ Material</kbd>. (También puedes seleccionar <kbd>File ▸ New...</kbd> desde el menú y después seleccionar <kbd>Material</kbd>). Nombra el nuevo archivo de material y presiona <kbd>Ok</kbd>.

![Archivo de material](images/materials/material_file.png)

El nuevo material se abrirá en el *Material Editor*.

![Editor de material](images/materials/material.png)

El archivo de material contiene la siguiente información:

Name
: La identidad del material. Este nombre se usa para listar el material en el recurso *Render* e incluirlo en la build. El nombre también se usa en la función de la API de render `render.enable_material()`. El nombre debe ser único.

Vertex Program
: El archivo del programa de vertex shader (*`.vp`*) que se usará al renderizar con el material. El programa de vertex shader se ejecuta en la GPU para cada vértice primitivo de un componente. Calcula la posición en pantalla de cada vértice y también puede generar variables "varying" que se interpolan y se entregan como entrada al programa de fragment shader.

Fragment Program
: El archivo del programa de fragment shader (*`.fp`*) que se usará al renderizar con el material. El programa se ejecuta en la GPU para cada fragmento (pixel) de una primitiva y su propósito es decidir el color de cada fragmento. Normalmente esto se hace mediante búsquedas en texturas y cálculos basados en variables de entrada (variables varying o constantes).

Vertex Constants
: Uniforms que se pasarán al programa de vertex shader. Consulta abajo una lista de constantes disponibles.

Fragment Constants
: Uniforms que se pasarán al programa de fragment shader. Consulta abajo una lista de constantes disponibles.

Samplers
: Opcionalmente puedes configurar samplers específicos en el archivo de materiales. Agrega un sampler, nómbralo según el nombre usado en el programa de shader y configura los ajustes de wrap y filtro como prefieras.

Tags
: Los tags asociados al material. Los tags se representan en el motor como una _bitmask_ que [`render.predicate()`](/ref/render#render.predicate) usa para recopilar componentes que deben dibujarse juntos. Consulta la [documentación de Render](/manuals/render) para saber cómo hacerlo. El número máximo de tags que puedes usar en un proyecto es 32.

## Atributos

Los atributos de shader (también llamados vertex streams o atributos de vértice) son un mecanismo que indica cómo la GPU recupera vértices de la memoria para renderizar geometría. El vertex shader especifica un conjunto de streams mediante la palabra clave `attribute` y, en la mayoría de los casos, Defold produce y vincula los datos automáticamente internamente a partir de los nombres de los streams. Sin embargo, en algunos casos puede que quieras pasar más datos por vértice para lograr un efecto específico que el motor no produce. Un atributo de vértice se puede configurar con los siguientes campos:

Name
: El nombre del atributo. Igual que con las constantes de shader, la configuración del atributo solo se usará si coincide con un atributo especificado en el vertex program.

Semantic type
: Un tipo semántico indica el significado semántico de *qué* es el atributo y/o *cómo* debe mostrarse en el editor. Por ejemplo, especificar un atributo con `SEMANTIC_TYPE_COLOR` mostrará un selector de color en el editor, aunque los datos se seguirán pasando tal cual desde el motor al shader.

  - `SEMANTIC_TYPE_NONE` El tipo semántico predeterminado. No tiene ningún otro efecto sobre el atributo aparte de pasar los datos de material del atributo directamente al buffer de vértices (predeterminado)
  - `SEMANTIC_TYPE_POSITION` Produce datos de posición por vértice para el atributo. Se puede usar junto con el espacio de coordenadas para indicar al motor cómo se calcularán las posiciones
  - `SEMANTIC_TYPE_TEXCOORD` Produce coordenadas de textura por vértice para el atributo
  - `SEMANTIC_TYPE_PAGE_INDEX` Produce índices de página por vértice para el atributo
  - `SEMANTIC_TYPE_COLOR` Afecta a cómo el editor interpreta el atributo. Si un atributo se configura con una semántica de color, se mostrará un widget selector de color en el inspector
  - `SEMANTIC_TYPE_NORMAL` Produce datos de normales por vértice para el atributo
  - `SEMANTIC_TYPE_TANGENT` Produce datos de tangentes por vértice para el atributo
  - `SEMANTIC_TYPE_WORLD_MATRIX` Produce datos de matriz de mundo por vértice para el atributo
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Produce datos de matriz normal por vértice para el atributo
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Produce una matriz 3x3 de transformación de textura por vértice para el atributo. Para los componentes de partículas, el motor proporciona una matriz que transforma coordenadas al espacio del atlas para la propiedad de imagen del componente. Para los componentes sprite, el motor proporciona una matriz para cada imagen que usa el componente (cuando se usa multi-texturing). Para los componentes de modelo, se proporciona una matriz identidad.

Data type
: El tipo de dato de los datos subyacentes del atributo.

  - `TYPE_BYTE` Valores byte con signo de 8 bits
  - `TYPE_UNSIGNED_BYTE` Valores byte sin signo de 8 bits
  - `TYPE_SHORT` Valores short con signo de 16 bits
  - `TYPE_UNSIGNED_SHORT` Valores short sin signo de 16 bits
  - `TYPE_INT` Valores enteros con signo
  - `TYPE_UNSIGNED_INT` Valores enteros sin signo
  - `TYPE_FLOAT` Valores de punto flotante (predeterminado)

Normalize
: Si es true, el driver de la GPU normalizará los valores del atributo. Esto puede ser útil cuando no necesitas precisión completa, pero quieres calcular algo sin conocer los límites específicos. Por ejemplo, un vector de color normalmente solo necesita valores byte de 0..255, aunque se siga tratando como un valor 0..1 en el shader.

Coordinate space
: Algunos tipos semánticos admiten suministrar datos en distintos espacios de coordenadas. Para implementar un efecto de billboarding con sprites, normalmente quieres un atributo de posición en espacio local y una posición completamente transformada en espacio del mundo para lograr el batching más eficiente.

Vector type
: El tipo de vector del atributo.

  - `VECTOR_TYPE_SCALAR` Valor escalar único
  - `VECTOR_TYPE_VEC2` Vector 2D
  - `VECTOR_TYPE_VEC3` Vector 3D
  - `VECTOR_TYPE_VEC4` Vector 4D (predeterminado)
  - `VECTOR_TYPE_MAT2` Matriz 2D
  - `VECTOR_TYPE_MAT3` Matriz 3D
  - `VECTOR_TYPE_MAT4` Matriz 4D

Step function
: Especifica cómo se deben presentar los datos del atributo a la función de vértices. Esto solo es relevante para instancing.

  - `Vertex` Una vez por vértice; por ejemplo, un atributo de posición normalmente se entregará a la función de vértices una vez por vértice de la malla (predeterminado)
  - `Instance` Una vez por instancia; por ejemplo, un atributo de matriz de mundo normalmente se entregará a la función de vértices una vez por instancia

Value
: El valor del atributo. Los valores de atributo se pueden sobrescribir por componente, pero si no se hace, esto actuará como el valor predeterminado del atributo de vértice. Nota: para los atributos *default* (posición, coordenadas de textura e índices de página), el valor se ignorará.

::: sidenote
Los atributos personalizados también se pueden usar para reducir el uso de memoria tanto en CPU como en GPU reconfigurando los streams para que usen un tipo de dato más pequeño o una cantidad distinta de elementos.
:::

### Semántica predeterminada de atributos

El sistema de materiales asignará automáticamente un tipo semántico predeterminado según el nombre del atributo en tiempo de ejecución para un conjunto específico de nombres:

  - `position` - tipo semántico: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - tipo semántico: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - tipo semántico: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - tipo semántico: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - tipo semántico: `SEMANTIC_TYPE_COLOR`
  - `normal` - tipo semántico: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - tipo semántico: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - tipo semántico: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - tipo semántico: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - tipo semántico: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Si tienes entradas para estos atributos en el material, el tipo semántico predeterminado se sobrescribirá con lo que hayas configurado en el editor de materiales.

### Definir datos de atributos de vértice personalizados

Al igual que con las constantes de shader definidas por el usuario, también puedes actualizar atributos de vértice en runtime llamando a `go.get`, `go.set` y `go.animate`:

![Atributo de material personalizado](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

Sin embargo, hay algunas consideraciones al actualizar los atributos de vértice: que un componente pueda usar o no el valor depende del tipo semántico del atributo. Por ejemplo, un componente sprite admite `SEMANTIC_TYPE_POSITION`, así que si actualizas un atributo que tiene este tipo semántico, el componente ignorará el valor sobrescrito porque el tipo semántico indica que los datos siempre deben producirse a partir de la posición del sprite.

En los casos en que un atributo de vértice sea un escalar o un tipo de vector distinto de `Vec4`, aún puedes definir los datos usando `go.set`:

```lua
-- Los dos últimos componentes del vec4 no se usarán!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

Lo mismo ocurre con los atributos de matriz: si el atributo es un tipo de matriz distinto de `Mat4`, aún puedes definir los datos usando `go.set`.

### Ejemplos de uso de atributos de vértice personalizados

Usar un atributo de transformación de textura para convertir coordenadas UV al espacio del atlas:

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extrae la posición de la transformación
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extrae la escala de la transformación
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // Convierte a UV locales (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Como alternativa, si las coordenadas UV ya están en el rango 0..1,
  // puedes transformarlas directamente al espacio del atlas multiplicando la transformación:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Pasa el valor al fragment shader
  var_texcoord0 = localUV;

  // ... resto del vertex shader
}
```

### Instancing

Instancing es una técnica usada para dibujar eficientemente varias copias del mismo objeto en una escena. En vez de crear una copia separada del objeto cada vez que se usa, instancing permite que el motor gráfico cree un solo objeto y lo reutilice muchas veces. Por ejemplo, en un juego con un bosque grande, en vez de crear un modelo de árbol separado para cada árbol, instancing te permite crear un modelo de árbol y colocarlo cientos o miles de veces con posiciones y escalas distintas. Ahora el bosque se puede renderizar con una sola draw call en vez de draw calls individuales para cada árbol.

::: sidenote
Instancing actualmente solo está disponible para componentes Model.
:::

Instancing se habilita automáticamente cuando es posible. Defold depende mucho de aplicar batching al estado de dibujo tanto como sea posible; para que instancing funcione, se deben cumplir algunos requisitos:

- Se debe usar el mismo material para todas las instancias. Instancing seguirá funcionando si se ha definido un material personalizado mediante `render.enable_material`
- El material debe estar configurado para usar el espacio de vértices 'local'
- El material debe tener al menos un atributo de vértice que se repita por instancia
- Los valores de constantes deben ser iguales para todas las instancias. En su lugar, los valores de constantes se pueden poner en atributos de vértice personalizados o en algún otro método subyacente (por ejemplo, una textura)
- Los recursos de shader, como texturas o buffers de almacenamiento, deben ser iguales para todas las instancias

Configurar un atributo de vértice para que se repita por instancia requiere que `Step function` esté definido como `Instance`. Esto se hace automáticamente para ciertos tipos semánticos según el nombre (consulta la tabla `Default attribute semantics` anterior), pero también se puede definir manualmente en el editor de materiales configurando `Step function` como `Instance`.

Como ejemplo simple, la siguiente escena tiene cuatro objetos de juego, cada uno con un componente de modelo:

![Configuración de instancing](images/materials/instancing-setup.png)

El material está configurado de la siguiente manera, con un único atributo de vértice personalizado que se repite por instancia:

![Material de instancing](images/materials/instancing-material.png)

El vertex shader tiene varios atributos por instancia especificados:

```glsl
// Atributos por vértice
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Atributos por instancia
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

Ten en cuenta que `mtx_world` y `mtx_normal` se configurarán para usar la step function `Instance` de forma predeterminada. Esto se puede cambiar en el editor de materiales agregando una entrada para ellos y configurando `Step function` como `Vertex`, lo que hará que el atributo se repita por vértice en vez de por instancia.

Para verificar que instancing funciona en este caso, puedes mirar el profiler web. En este caso, como lo único que cambia entre las instancias de la caja son los atributos por instancia, se puede renderizar con una sola draw call:

![Draw calls de instancing](images/materials/instancing-draw-calls.png)

#### Compatibilidad hacia atrás

En adaptadores gráficos basados en OpenGL, instancing requiere al menos OpenGL 3.1 para escritorio y OpenGL ES 3.0 para móviles. Esto significa que los dispositivos muy antiguos que usan OpenGL ES2 o versiones anteriores de OpenGL podrían no admitir instancing. En este caso, el renderizado seguirá funcionando por defecto sin ningún cuidado especial por parte del desarrollador, pero puede no ser tan eficiente como si se usara instancing real. Actualmente no hay forma de detectar si instancing está soportado o no, pero esta funcionalidad se agregará en el futuro para que se pueda usar un material menos costoso, o para omitir por completo elementos como follaje u objetos decorativos que normalmente serían buenos candidatos para instancing.

## Constantes de vertex y fragment shader

Las constantes de shader, o "uniforms", son valores que se pasan desde el motor a los programas de vertex shader y fragment shader. Para usar una constante, la defines en el archivo de material como una propiedad *Vertex Constant* o una propiedad *Fragment Constant*. Las variables `uniform` correspondientes deben definirse en el programa de shader. Las siguientes constantes se pueden definir en un material:

`CONSTANT_TYPE_WORLD`
: La matriz de mundo. Se usa para transformar vértices al espacio del mundo. Para algunos tipos de componentes, los vértices ya están en espacio del mundo cuando llegan al vertex program (debido al batching). En esos casos, multiplicar por la matriz de mundo en el shader producirá resultados incorrectos.

`CONSTANT_TYPE_VIEW`
: La matriz de vista. Se usa para transformar vértices al espacio de vista (cámara).

`CONSTANT_TYPE_PROJECTION`
: La matriz de proyección. Se usa para transformar vértices al espacio de pantalla.

`CONSTANT_TYPE_VIEWPROJ`
: Una matriz con las matrices de vista y proyección ya multiplicadas.

`CONSTANT_TYPE_WORLDVIEW`
: Una matriz con las matrices de mundo y vista ya multiplicadas.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Una matriz con las matrices de mundo, vista y proyección ya multiplicadas.

`CONSTANT_TYPE_NORMAL`
: Una matriz para calcular la orientación de normales. La transformación de mundo puede incluir escalado no uniforme, lo que rompe la ortogonalidad de la transformación mundo-vista combinada. La matriz normal se usa para evitar problemas con la dirección al transformar normales. (La matriz normal es la inversa transpuesta de la matriz mundo-vista).

`CONSTANT_TYPE_USER`
: Una constante vector4 que puedes usar para cualquier dato personalizado que quieras pasar a tus programas de shader. Puedes definir el valor inicial de la constante en la definición de la constante, pero es mutable mediante las funciones [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). También puedes recuperar el valor con [go.get()](/ref/stable/go/#go.get). Cambiar una constante de material de una sola instancia de componente [rompe el batching de render y producirá draw calls adicionales](/manuals/render/#draw-calls-and-batching).

Ejemplo:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Una constante matrix4 que puedes usar para cualquier dato personalizado que quieras pasar a tus programas de shader. Puedes definir el valor inicial de la constante en la definición de la constante, pero es mutable mediante las funciones [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). También puedes recuperar el valor con [go.get()](/ref/stable/go/#go.get). Cambiar una constante de material de una sola instancia de componente [rompe el batching de render y producirá draw calls adicionales](/manuals/render/#draw-calls-and-batching).

Ejemplo:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

::: sidenote
Para que una constante de material de tipo `CONSTANT_TYPE_USER` o `CONSTANT_TYPE_MATRIX4` esté disponible mediante `go.get()` y `go.set()`, debe usarse en el programa de shader. Si la constante se define en el material pero no se usa en el programa, se eliminará del material y no estará disponible en tiempo de ejecución.
:::

## Samplers

Los samplers se usan para muestrear la información de color de una textura (un tile source o atlas). La información de color se puede usar después para cálculos en el programa de shader.

Los componentes sprite, tilemap, GUI y de efectos de partículas reciben automáticamente un `sampler2D` definido. El primer `sampler2D` declarado en el programa de shader se vincula automáticamente a la imagen referenciada en el componente gráfico. Por lo tanto, actualmente no es necesario especificar samplers en el archivo de materiales para esos componentes. Además, esos tipos de componentes actualmente solo admiten una única textura. (Si necesitas varias texturas en un shader, puedes usar [`render.enable_texture()`](/ref/render/#render.enable_texture) y definir samplers de textura manualmente desde tu script de render).

![Sampler de sprite](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Puedes especificar los ajustes de sampler de un componente agregando el sampler por nombre en el archivo de materiales. Si no configuras el sampler en el archivo de materiales, se usa la configuración global de *graphics* del proyecto.

![Ajustes de sampler](images/materials/my_sampler.png)

Para los componentes de modelo, debes especificar tus samplers en el archivo de material con los ajustes que quieras. El editor permitirá entonces definir texturas para cualquier componente de modelo que use el material:

![Samplers de modelo](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Modelo](images/materials/model.png)

## Ajustes de sampler

Name
: El nombre del sampler. Este nombre debe coincidir con el `sampler2D` declarado en el fragment shader.

Wrap U/W
: El modo wrap para los ejes U y V:

  - `WRAP_MODE_REPEAT` repetirá los datos de textura fuera del rango [0,1].
  - `WRAP_MODE_MIRRORED_REPEAT` repetirá los datos de textura fuera del rango [0,1], pero cada segunda repetición estará espejada.
  - `WRAP_MODE_CLAMP_TO_EDGE` definirá los datos de textura para valores mayores que 1.0 como 1.0, y cualquier valor menor que 0.0 se definirá como 0.0, es decir, los pixeles del borde se repetirán hasta el borde.

Filter Min/Mag
: El filtrado para magnificación y minificación. El filtrado nearest requiere menos computación que la interpolación lineal, pero puede producir artefactos de aliasing. La interpolación lineal suele proporcionar resultados más suaves:

  - `Default` usa la opción de filtro predeterminada especificada en el archivo `game.project` bajo `Graphics` como `Default Texture Min Filter` y `Default Texture Mag Filter`.
  - `FILTER_MODE_NEAREST` usa el texel con coordenadas más cercanas al centro del pixel.
  - `FILTER_MODE_LINEAR` define un promedio lineal ponderado del arreglo 2x2 de texels que están más cerca del centro del pixel.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` elige el valor del texel más cercano dentro de un mipmap individual.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` selecciona el texel más cercano en las dos opciones de mipmap más cercanas y después interpola linealmente entre estos dos valores.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` interpola linealmente dentro de un mipmap individual.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` usa interpolación lineal para calcular el valor en cada uno de dos mapas y después interpola linealmente entre estos dos valores.

Max Anisotropy
: El filtrado anisotrópico es una técnica de filtrado avanzada que toma varias muestras y mezcla los resultados. Este ajuste controla el nivel de anisotropía para los samplers de textura. Si el filtrado anisotrópico no está soportado por la GPU, el parámetro no tendrá efecto y se definirá en 1 por defecto.

## Buffers de constantes

Cuando el pipeline de renderizado dibuja, toma valores de constantes de un buffer de constantes del sistema predeterminado. Puedes crear un buffer de constantes personalizado para sobrescribir las constantes predeterminadas y, en su lugar, definir programáticamente uniforms de programas de shader en el script de render:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Crea un nuevo buffer de constantes
2. Define la constante `tint` como rojo brillante
3. Dibuja el predicado usando nuestro buffer de constantes personalizado

Ten en cuenta que los elementos constantes del buffer se referencian como una tabla Lua común, pero no puedes iterar sobre el buffer con `pairs()` o `ipairs()`.
