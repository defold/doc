---
title: Manual de programas compute de Defold
brief: Este manual explica cómo trabajar con programas compute, constantes de shader y samplers.
---

# Programas compute

::: sidenote
La compatibilidad con compute shaders en Defold está actualmente en *technical preview*.
Esto significa que todavía faltan algunas funcionalidades y que la API podría cambiar en el futuro.
:::

Los compute shaders son una herramienta potente para realizar cálculos de propósito general en la GPU. Permiten aprovechar la capacidad de procesamiento paralelo de la GPU para tareas como simulaciones físicas, procesamiento de imágenes y más. Un compute shader opera sobre datos almacenados en buffers o texturas, y realiza operaciones en paralelo en muchos hilos de la GPU. Este paralelismo es lo que hace que los compute shaders sean tan potentes para cálculos intensivos.

* Para obtener más información sobre el pipeline de render, consulta la [documentación de render](/manuals/render).
* Para ver una explicación detallada de los programas de shader, consulta la [documentación de shaders](/manuals/shader).

## ¿Qué puedo hacer con compute shaders?

Como los compute shaders están pensados para usarse en cálculos genéricos, no hay realmente un límite para lo que puedes hacer con ellos. Estos son algunos ejemplos de para qué se suelen usar los compute shaders:

Procesamiento de imágenes
  - Filtrado de imágenes: aplica desenfoques, detección de bordes, filtros de nitidez, etc.
  - Gradación de color: ajusta el espacio de color de una imagen.

Física
  - Sistemas de partículas: simula grandes cantidades de partículas para efectos como humo, fuego y dinámica de fluidos.
  - Física de cuerpos blandos: simula objetos deformables como tela y gelatina.
  - Culling: occlusion culling, frustum culling.

Generación procedural
  - Generación de terreno: crea terreno detallado usando funciones de ruido.
  - Vegetación y follaje: crea plantas y árboles generados proceduralmente.

Efectos de renderizado
  - Iluminación global: simula iluminación realista aproximando cómo rebota la luz en una escena.
  - Voxelización: crea una cuadrícula de vóxeles 3D a partir de datos de malla.

## ¿Cómo funcionan los compute shaders?

A alto nivel, los compute shaders funcionan dividiendo una tarea en muchas tareas más pequeñas que se pueden ejecutar simultáneamente. Esto se logra mediante los conceptos de `work groups` e `invocations`:

Work Groups
: El compute shader opera sobre una cuadrícula de `work groups`. Cada work group contiene un número fijo de invocations (o hilos). El tamaño de los work groups y el número de invocations se definen en el código del shader.

Invocations
: Cada invocation (o hilo) ejecuta el programa del compute shader. Las invocations dentro de un work group pueden compartir datos mediante memoria compartida, lo que permite una comunicación y sincronización eficientes entre ellas.

La GPU ejecuta el compute shader lanzando muchas invocations en paralelo en múltiples work groups, lo que proporciona una capacidad de cálculo significativa para las tareas adecuadas.

## Crear un programa compute

Para crear un programa compute, haz <kbd>click derecho</kbd> en una carpeta objetivo en el navegador *Assets* y selecciona <kbd>New... ▸ Compute</kbd>. (También puedes seleccionar <kbd>File ▸ New...</kbd> en el menú y luego seleccionar <kbd>Compute</kbd>). Pon un nombre al nuevo archivo compute y presiona <kbd>Ok</kbd>.

![Archivo compute](images/compute/compute_file.png)

El nuevo compute se abrirá en el *Compute Editor*.

![Editor compute](images/compute/compute.png)

El archivo compute contiene la siguiente información:

Compute Program
: El archivo de programa del compute shader (*`.cp`*) que se usará. El shader opera sobre "elementos de trabajo abstractos", lo que significa que no hay una definición fija de los tipos de datos de entrada y salida. Corresponde al programador definir qué debe producir el compute shader.

Constants
: Uniforms que se pasarán al programa del compute shader. Consulta abajo una lista de las constantes disponibles.

Samplers
: Puedes configurar samplers específicos opcionalmente en el archivo de materiales. Agrega un sampler, nómbralo de acuerdo con el nombre usado en el programa de shader y define los ajustes de wrap y filtrado como prefieras.


## Usar el programa compute en Defold

A diferencia de los materiales, los programas compute no se asignan a ningún componente y no forman parte del flujo normal de render. Un programa compute debe lanzarse (`dispatched`) en un script de render para hacer cualquier trabajo. Sin embargo, antes de hacer dispatch, debes asegurarte de que el script de render tenga una referencia al programa compute. Actualmente, la única forma de que un script de render conozca el programa compute es agregarlo al archivo .render que contiene la referencia a tu script de render:

![Archivo de render compute](images/compute/compute_render_file.png)

Para usar el programa compute, primero debe enlazarse al contexto de render. Esto se hace de la misma forma que con los materiales:

```lua
render.set_compute("my_compute")
-- Haz el trabajo de compute aquí; llama a render.set_compute() para desenlazar
render.set_compute()
```

Aunque las constantes compute se aplicarán automáticamente cuando se haga dispatch del programa, no hay forma de enlazar recursos de entrada o salida (texturas, buffers, etc.) a un programa compute desde el editor. En su lugar, esto debe hacerse mediante scripts de render:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Para ejecutar el programa en el espacio de trabajo que hayas elegido, debes hacer dispatch del programa:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute también acepta una tabla de opciones como último argumento
-- puedes usar esta tabla de argumentos para pasar constantes de render a la llamada de dispatch
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Escribir datos desde programas compute

Actualmente, generar cualquier tipo de salida desde un programa compute solo se puede hacer mediante `storage textures`. Una storage texture es similar a una "textura regular", excepto que admite más funcionalidad y configurabilidad. Las storage textures, como su nombre indica, se pueden usar como un buffer genérico desde el que puedes leer datos y al que puedes escribir datos desde un programa compute. Luego puedes enlazar el mismo buffer a otro programa de shader para lectura.

Para crear una storage texture en Defold, debes hacerlo desde un archivo `.script` normal. Los scripts de render no tienen esta funcionalidad, ya que las texturas dinámicas deben crearse mediante la API de `resource`, que solo está disponible en archivos `.script` normales.

```lua
-- En un archivo .script:
function init(self)
    -- Crea un recurso de textura como de costumbre, pero agrega la flag "storage"
    -- para que se pueda usar como almacenamiento de respaldo para programas compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- obtén el handle de textura del recurso
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notifica al renderer sobre la textura de respaldo para que pueda enlazarse con render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Todo junto

### Programa de shader

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// especifica los recursos de entrada
uniform vec4 color;
uniform sampler2D texture_in;

// especifica la imagen de salida
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // Este no es un shader especialmente interesante, pero demuestra
    // cómo leer desde una textura y un buffer de constantes, y escribir en una storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Escribe el valor de salida en la storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Componente script
```lua
-- En un archivo .script

-- Aquí especificamos la textura de entrada que luego enlazaremos al
-- programa compute. Podemos asignar esta textura a un componente de modelo
-- o habilitarla en el contexto de render en el script de render.
go.property("texture_in", resource.texture())

function init(self)
    -- Crea un recurso de textura como de costumbre, pero agrega la flag "storage"
    -- para que se pueda usar como almacenamiento de respaldo para programas compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notifica al renderer sobre las texturas de entrada y salida
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Script de render
```lua
-- responde al mensaje "set_backing_texture"
-- para definir la textura de respaldo para el programa compute
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- Podemos enlazar texturas a constantes con nombres específicos
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Haz dispatch del programa compute tantas veces como píxeles tengamos.
    -- Esto constituye nuestro "work group". El shader será invocado
    -- 128 x 128 x 1 veces, o una vez por píxel.
    render.dispatch_compute(128, 128, 1)
    -- cuando hayamos terminado con el programa compute, debemos desenlazarlo
    render.set_compute()
end
```

## Compatibilidad

Defold actualmente admite compute shaders en los siguientes adaptadores gráficos:

- Vulkan
- Metal (mediante MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

::: sidenote
Actualmente no hay forma de comprobar si el cliente en ejecución admite compute shaders.
Esto significa que no hay garantía de que el cliente pueda ejecutar compute shaders si el adaptador gráfico está basado en OpenGL u OpenGL ES.
Vulkan y Metal admiten compute shaders desde la versión 1.0. Para usar Vulkan, debes crear un manifest personalizado y seleccionar Vulkan como backend.
:::

