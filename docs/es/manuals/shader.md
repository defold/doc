---
title: Programas shader en Defold
brief: Este manual describe en detalle los vertex shaders y fragment shaders, y cómo usarlos en Defold.
---

# Shaders

Los programas shader están en el centro del renderizado de gráficos. Son programas escritos en un lenguaje similar a C llamado GLSL (GL Shading Language) que el hardware gráfico ejecuta para realizar operaciones sobre los datos 3D subyacentes (los vértices) o sobre los píxeles que terminan en pantalla (los "fragmentos"). Los shaders se usan para dibujar sprites, iluminar modelos 3D, crear efectos posteriores de pantalla completa y mucho, mucho más.

Este manual describe cómo el pipeline de renderizado de Defold se comunica con los shaders de la GPU. Para crear shaders para tu contenido, también necesitas entender el concepto de materiales, así como cómo funciona el pipeline de renderizado.

* Consulta el [manual de Render](/manuals/render) para obtener detalles sobre el pipeline de renderizado.
* Consulta el [manual de Material](/manuals/material) para obtener detalles sobre los materiales.
* Consulta el [manual de Compute](/manuals/compute) para obtener detalles sobre los programas compute.

Las especificaciones de OpenGL ES 2.0 (OpenGL for Embedded Systems) y OpenGL ES Shading Language se pueden encontrar en [Khronos OpenGL Registry](https://www.khronos.org/registry/gles/).

Ten en cuenta que en computadoras de escritorio es posible escribir shaders usando funcionalidades que no están disponibles en OpenGL ES 2.0. El driver de tu tarjeta gráfica puede compilar y ejecutar sin problemas código shader que no funcionará en dispositivos móviles.


## Conceptos

Shader de vértices (Vertex shader)
: Un vertex shader no puede crear ni eliminar vértices, solo cambiar la posición de un vértice. Los vertex shaders se usan comúnmente para transformar las posiciones de los vértices desde el espacio 3D del mundo al espacio 2D de la pantalla.

  La entrada de un vertex shader son datos de vértices (en forma de `attributes`) y constantes (`uniforms`). Las constantes comunes son las matrices necesarias para transformar y proyectar la posición de un vértice al espacio de pantalla.

  La salida del vertex shader es la posición de pantalla calculada del vértice (`gl_Position`). También es posible pasar datos del vertex shader al fragment shader mediante variables `varying`.

Shader de fragmentos (Fragment shader)
: Una vez que el vertex shader termina, el trabajo del fragment shader es decidir el color de cada fragmento (o píxel) de las primitivas resultantes.

  La entrada de un fragment shader son constantes (`uniforms`), así como cualquier variable `varying` definida por el vertex shader.

  La salida del fragment shader es el valor de color del fragmento específico (`gl_FragColor`).

Compute shader
: Un compute shader es un shader de propósito general que se puede usar para realizar cualquier tipo de trabajo en una GPU. No forma parte del pipeline gráfico; los compute shaders se ejecutan en un contexto de ejecución separado y no dependen de la entrada de ningún otro shader.

  La entrada de un compute shader son buffers de constantes (`uniforms`), imágenes de textura (`image2D`), samplers (`sampler2D`) y buffers de almacenamiento (`buffer`).

  La salida del compute shader no está definida explícitamente; no hay una salida específica que deba producirse, a diferencia de los vertex shaders y fragment shaders. Como los compute shaders son genéricos, depende del programador definir qué tipo de resultado debe producir el compute shader.

Matriz de mundo
: Las posiciones de los vértices de la forma de un modelo se almacenan en relación con el origen del modelo. Esto se llama "espacio de modelo". El mundo del juego, sin embargo, es un "espacio del mundo" donde la posición, orientación y escala de cada vértice se expresan en relación con el origen del mundo. Al mantenerlos separados, el motor de videojuegos puede mover, rotar y escalar cada modelo sin destruir los valores de vértices originales almacenados en el componente de modelo.

  Cuando un modelo se coloca en el mundo del juego, las coordenadas locales de sus vértices deben traducirse a coordenadas de mundo. Esta traducción se realiza mediante una *matriz de transformación de mundo*, que indica qué traducción (movimiento), rotación y escala deben aplicarse a los vértices de un modelo para colocarlo correctamente en el sistema de coordenadas del mundo del juego.

  ![Transformación de mundo](images/shader/world_transform.png)

Matrices de vista y proyección
: Para colocar los vértices del mundo del juego en la pantalla, las coordenadas 3D de cada matriz se traducen primero a coordenadas relativas a la cámara. Esto se hace con una _matriz de vista_. Luego, los vértices se proyectan al espacio 2D de la pantalla con una _matriz de proyección_:

  ![Proyección](images/shader/projection.png)

Atributos
: Un valor asociado a un vértice individual. Los atributos se pasan al shader desde el motor y, si quieres acceder a un atributo, solo tienes que declararlo en tu programa shader. Distintos tipos de componentes tienen distintos conjuntos de atributos:
  - Sprite tiene `position` y `texcoord0`.
  - Tilegrid tiene `position` y `texcoord0`.
  - GUI node tiene `position`, `textcoord0` y `color`.
  - ParticleFX tiene `position`, `texcoord0` y `color`.
  - Model tiene `position`, `texcoord0` y `normal`.
  - Font tiene `position`, `texcoord0`, `face_color`, `outline_color` y `shadow_color`.

Constantes
: Las constantes de shader permanecen constantes durante la llamada de dibujo de renderizado. Las constantes se agregan a las secciones *Constants* del archivo de material y luego se declaran como `uniform` en el programa shader. Los sampler uniforms se agregan a la sección *Samplers* del material y luego se declaran como `uniform` en el programa shader. Las matrices necesarias para realizar transformaciones de vértices en un vertex shader están disponibles como constantes:

  - `CONSTANT_TYPE_WORLD` es la *matriz de mundo* que transforma desde el espacio de coordenadas local de un objeto al espacio del mundo.
  - `CONSTANT_TYPE_VIEW` es la *matriz de vista* que transforma desde el espacio del mundo al espacio de cámara.
  - `CONSTANT_TYPE_PROJECTION` es la *matriz de proyección* que transforma desde la cámara al espacio de pantalla.
  - También están disponibles matrices premultiplicadas $world * view$, $view * projection$ y $world * view$.
  - `CONSTANT_TYPE_USER` es una constante de tipo `vec4` que puedes usar como quieras.

  El [manual de Material](/manuals/material) explica cómo especificar constantes.

Samplers
: Los shaders pueden declarar variables uniformes de tipo *sampler*. Los samplers se usan para leer valores desde una fuente de imagen:

  - `sampler2D` muestrea desde una textura de imagen 2D.
  - `sampler2DArray` muestrea desde una textura de arreglo de imágenes 2D. Esto se usa principalmente para atlas paginados.
  - `samplerCube` muestrea desde una textura cubemap de 6 imágenes.
  - `image2D` carga (y potencialmente almacena) datos de textura en un objeto de imagen. Esto se usa principalmente para almacenamiento en compute shaders.

  Puedes usar un sampler solo en las funciones de búsqueda de texturas de la biblioteca estándar de GLSL. El [manual de Material](/manuals/material) explica cómo especificar la configuración de samplers.

Coordenadas UV
: Una coordenada 2D se asocia con un vértice y se mapea a un punto en una textura 2D. Por lo tanto, una parte, o toda la textura, se puede pintar sobre la forma descrita por un conjunto de vértices.

  ![Coordenadas UV](images/shader/uv_map.png)

  Un mapa UV se genera normalmente en el programa de modelado 3D y se almacena en la malla. Las coordenadas de textura de cada vértice se proporcionan al vertex shader como un atributo. Luego se usa una variable `varying` para encontrar la coordenada UV de cada fragmento, interpolada a partir de los valores de los vértices.

Variables varying
: Los tipos de variables `varying` se usan para pasar información entre la etapa de vértices y la etapa de fragmentos.

  1. Una variable `varying` se define en el vertex shader para cada vértice.
  2. Durante la rasterización, este valor se interpola para cada fragmento de la primitiva que se está renderizando. La distancia del fragmento a los vértices de la forma determina el valor interpolado.
  3. La variable se establece para cada llamada al fragment shader y se puede usar para cálculos de fragmentos.

  ![Interpolación varying](images/shader/varying_vertex.png)

  Por ejemplo, definir un `varying` con un valor de color RGB `vec3` en cada esquina de un triángulo interpolará los colores a través de toda la forma. Del mismo modo, definir coordenadas de búsqueda de mapa de textura (o *coordenadas UV*) en cada vértice de un rectángulo permite que el fragment shader busque valores de color de textura para toda el área de la forma.

  ![Interpolación varying](images/shader/varying.png)

## Escribir shaders GLSL modernos

Como el motor Defold soporta varias plataformas y API gráficas, debe ser sencillo para los desarrolladores escribir shaders que funcionen en todas partes. El pipeline de assets logra esto principalmente de dos maneras (denominadas `shader pipelines` de ahora en adelante):

1. El pipeline heredado, donde los shaders se escriben en código GLSL compatible con ES2.
2. El pipeline moderno, donde los shaders se escriben en código GLSL compatible con SPIR-v.

A partir de Defold 1.9.2, se recomienda escribir shaders que utilicen el nuevo pipeline, y para lograrlo la mayoría de los shaders deben migrarse a shaders escritos al menos en la versión 140 (OpenGL 3.1). Para migrar un shader, asegúrate de cumplir estos requisitos:

### Declaración de versión
Coloca al menos #version 140 en la parte superior del shader:

```glsl
#version 140
```

Así es como se elige el pipeline de shaders en el proceso de build, por eso todavía puedes usar los shaders antiguos. Si no se encuentra ninguna declaración de versión del preprocesador, Defold volverá al pipeline heredado.

### Atributos
En vertex shaders, reemplaza la palabra clave `attribute` por `in`:

```glsl
// en lugar de:
// attribute vec4 position;
// haz:
in vec4 position;
```

Nota: Los fragment shaders (y compute shaders) no reciben entradas de vértices.

### Varyings
En vertex shaders, los varyings deben tener el prefijo `out`. En fragment shaders, los varyings pasan a ser `in`:

```glsl
// En un vertex shader, en lugar de:
// varying vec4 var_color;
// haz:
out vec4 var_color;

// En un fragment shader, en lugar de:
// varying vec4 var_color;
// haz:
in vec4 var_color;
```

### Uniforms (llamados constantes en Defold)

Los tipos uniform opacos (samplers, imágenes, atomics, SSBOs) no necesitan ninguna migración; puedes usarlos como lo haces hoy:

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

Para tipos uniform no opacos, debes colocarlos en un `uniform block`. Un uniform block es simplemente una colección de variables uniform y se declara con la palabra clave `uniform`:

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Los miembros individuales del uniform block se pueden usar tal cual
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

Todos los miembros del uniform block se exponen a materiales y componentes como constantes individuales. No se necesita migración para usar buffers de constantes de renderizado, ni `go.set` y `go.get`.

### Variables integradas

En fragment shaders, `gl_FragColor` está obsoleto a partir de la versión 140. Usa `out` en su lugar:

```glsl
// en lugar de:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// haz:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### Funciones de textura

Las funciones específicas de muestreo de texturas, como `texture2D` y `texture2DArray`, ya no existen. En su lugar, usa simplemente la función `texture`:

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// en lugar de:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// haz:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### Precisión

Definir precisión explícita para variables, entradas, salidas y demás era necesario antes para cumplir con contextos OpenGL ES. Esto ya no es necesario; ahora la precisión se define automáticamente para las plataformas que la soportan.

### Juntándolo todo

Como ejemplo final donde se aplican todas estas reglas, aquí están los shaders de sprite integrados convertidos al formato nuevo:

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// las posiciones están en espacio del mundo
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Premultiplica alfa, ya que todas las texturas de runtime ya tienen alfa premultiplicado
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## Incluir fragmentos de código en shaders

Los shaders en Defold soportan incluir código fuente desde archivos dentro del proyecto que tengan la extensión `.glsl`. Para incluir un archivo glsl desde un shader, usa el pragma `#include` con comillas dobles o corchetes. Los includes deben tener rutas relativas al proyecto o una ruta relativa al archivo que los incluye:

```glsl
// En el archivo /main/my-shader.fp

// Ruta absoluta
#include "/main/my-snippet.glsl"
// El archivo está en la misma carpeta
#include "my-snippet.glsl"
// El archivo está en una subcarpeta al mismo nivel que 'my-shader'
#include "sub-folder/my-snippet.glsl"
// El archivo está en una subcarpeta del directorio padre, es decir /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// El archivo está en el directorio padre, es decir /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

Hay algunas salvedades sobre cómo se detectan los includes:

  - Los archivos deben ser relativos al proyecto, lo que significa que solo puedes incluir archivos ubicados dentro del proyecto. Cualquier ruta absoluta debe especificarse con una `/` inicial.
  - Puedes incluir código en cualquier parte del archivo, pero no puedes incluir un archivo inline en una sentencia. Por ejemplo, `const float #include "my-float-name.glsl" = 1.0` no funcionará.

### Guardas de encabezado (header guards)

Los fragmentos de código pueden incluir otros archivos `.glsl`, lo que significa que el shader final producido puede llegar a incluir el mismo código varias veces y, dependiendo del contenido de los archivos, puedes terminar con problemas de compilación por tener los mismos símbolos declarados más de una vez. Para evitar esto, puedes usar *header guards*, un concepto común en varios lenguajes de programación. Ejemplo:

```glsl
// En my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// En math-functions.glsl
#include "pi.glsl"

// En pi.glsl
const float PI = 3.14159265359;
```

En este ejemplo, la constante `PI` se definirá dos veces, lo que causará errores de compilación al ejecutar el proyecto. En su lugar, debes proteger el contenido con header guards:

```glsl
// En pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

El código de `pi.glsl` se expandirá dos veces en `my-shader.vs`, pero como lo has envuelto en header guards, el símbolo PI solo se definirá una vez y el shader compilará correctamente.

Sin embargo, esto no siempre es estrictamente necesario, según el caso de uso. Si en cambio quieres reutilizar código localmente en una función o en otro lugar donde no necesitas que los valores estén disponibles globalmente en el código del shader, probablemente no deberías usar header guards. Ejemplo:

```glsl
// En red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// En my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## Código shader específico del editor

Cuando los shaders se renderizan en el viewport del editor Defold, está disponible una definición de preprocesador `EDITOR`. Esto te permite escribir código shader que se comporte de forma diferente cuando se ejecuta en el editor y cuando se ejecuta en el motor real del juego.

Esto es especialmente útil para:
  - Agregar visualizaciones de debug que solo deben aparecer en el editor.
  - Implementar funcionalidades específicas del editor, como modos wireframe o vistas previas de materiales.
  - Proporcionar un renderizado de respaldo para materiales que podrían no funcionar correctamente en el viewport del editor.

Usa la directiva de preprocesador `#ifdef EDITOR` para compilar condicionalmente código que solo debe ejecutarse en el editor:

```glsl
#ifdef EDITOR
    // Este código solo se ejecutará cuando el shader se renderice en el Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Color magenta para la vista previa del editor
#else
    // Este código se ejecutará cuando se ejecute en el juego
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## El proceso de renderizado

Antes de terminar en la pantalla, los datos que creas para tu juego pasan por una serie de pasos:

![Pipeline de renderizado](images/shader/pipeline.png)

Todos los componentes visuales (sprites, nodos GUI, efectos de partículas o modelos) están compuestos por vértices, puntos en el mundo 3D que describen la forma del componente. Lo bueno de esto es que es posible ver la forma desde cualquier ángulo y distancia. El trabajo del programa vertex shader es tomar un único vértice y traducirlo a una posición en el viewport para que la forma pueda terminar en pantalla. Para una forma con 4 vértices, el programa vertex shader se ejecuta 4 veces, cada una en paralelo.

![vertex shader](images/shader/vertex_shader.png)

La entrada del programa es la posición del vértice (y otros datos de atributos asociados con el vértice) y la salida es una nueva posición de vértice (`gl_Position`), así como cualquier variable `varying` que deba interpolarse para cada fragmento.

El programa vertex shader más simple solo establece la posición de la salida en un vértice cero (lo cual no es muy útil):

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Un ejemplo más completo es el vertex shader de sprite integrado:

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. Un uniform (constante) que contiene las matrices de vista y proyección multiplicadas.
2. Atributos del vértice del sprite. `position` ya está transformado a espacio del mundo. `texcoord0` contiene la coordenada UV del vértice.
3. Declara una variable de salida `varying`. Esta variable se interpolará para cada fragmento entre los valores definidos para cada vértice y se enviará al fragment shader.
4. `gl_Position` se define como la posición de salida del vértice actual en el espacio de proyección. Este valor tiene 4 componentes: `x`, `y`, `z` y `w`. El componente `w` se usa para calcular interpolación correcta en perspectiva. Este valor normalmente es 1.0 para cada vértice antes de aplicar cualquier matriz de transformación.
5. Define la coordenada UV `varying` para esta posición de vértice. Después de la rasterización se interpolará para cada fragmento y se enviará al fragment shader.




Después del vertex shading, se decide la forma en pantalla del componente: se generan y rasterizan formas primitivas, lo que significa que el hardware gráfico divide cada forma en *fragmentos*, o píxeles. Luego ejecuta el programa fragment shader, una vez por cada fragmento. Para una imagen en pantalla de 16x24 píxeles, el programa se ejecuta 384 veces, cada una en paralelo.

![fragment shader](images/shader/fragment_shader.png)

La entrada del programa es lo que envíen el pipeline de renderizado y el vertex shader, normalmente las *coordenadas UV* del fragmento, colores de tinte, etc. La salida es el color final del píxel (`gl_FragColor`).

El programa fragment shader más simple solo establece el color de cada píxel en negro (de nuevo, no es un programa muy útil):

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

De nuevo, un ejemplo más completo es el fragment shader de sprite integrado:

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. Se declara la variable `varying` de coordenadas de textura. El valor de esta variable se interpolará para cada fragmento entre los valores definidos para cada vértice de la forma.
2. Se declara una variable uniform `sampler2D`. El sampler, junto con las coordenadas de textura interpoladas, se usa para realizar la búsqueda de textura y que el sprite pueda texturizarse correctamente. Como esto es un sprite, el motor asignará este sampler a la imagen definida en la propiedad *Image* del sprite.
3. Una constante de tipo `CONSTANT_TYPE_USER` se define en el material y se declara como `uniform`. Su valor se usa para permitir el tinte de color del sprite. El valor predeterminado es blanco puro.
4. El valor de color del tinte se premultiplica con su valor alfa, ya que todas las texturas de runtime ya contienen alfa premultiplicado.
5. Muestrea la textura en la coordenada interpolada y devuelve el valor muestreado.
6. `gl_FragColor` se define como el color de salida del fragmento: el color difuso de la textura multiplicado por el valor de tinte.

El valor de fragmento resultante luego pasa por pruebas. Una prueba común es la *prueba de profundidad*, en la que el valor de profundidad del fragmento se compara con el valor del depth buffer del píxel que se está probando. Según la prueba, el fragmento puede descartarse o se escribe un valor nuevo en el depth buffer. Un uso común de esta prueba es permitir que los gráficos que están más cerca de la cámara bloqueen los gráficos más alejados.

Si la prueba concluye que el fragmento debe escribirse en el framebuffer, se *mezclará* con los datos de píxel ya presentes en el buffer. Los parámetros de blending definidos en el render script permiten combinar de varias maneras el color de origen (el valor escrito por el fragment shader) y el color de destino (el color de la imagen en el framebuffer). Un uso común del blending es habilitar el renderizado de objetos transparentes.

## Más información

- [Shadertoy](https://www.shadertoy.com) contiene una enorme cantidad de shaders aportados por usuarios. Es una gran fuente de inspiración donde puedes aprender sobre varias técnicas de shading. Muchos de los shaders mostrados en el sitio se pueden portar a Defold con muy poco trabajo. El [tutorial de Shadertoy](https://www.defold.com/tutorials/shadertoy/) repasa los pasos para convertir un shader existente a Defold.

- El [tutorial de Grading](https://www.defold.com/tutorials/grading/) muestra cómo crear un efecto de gradación de color de pantalla completa usando texturas de tabla de búsqueda de color para la gradación.

- [The Book of Shaders](https://thebookofshaders.com/00/) te enseñará cómo usar e integrar shaders en tus proyectos, mejorando su rendimiento y calidad gráfica.
