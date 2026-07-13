---
title: Componente Light en Defold
brief: Este manual explica cómo usar luces ambientales, direccionales, puntuales y focales, y cómo acceder a los datos de iluminación en los shaders.
---

# Componente Light

El componente Light representa una fuente de luz en una colección. Actualmente, Defold admite cuatro tipos de recursos de luz:

- Luz ambiental (`.ambient_light`)
- Luz direccional (`.directional_light`)
- Luz puntual (`.point_light`)
- Luz focal (`.spot_light`)

Los recursos de luz se añaden a los objetos de juego como cualquier otro recurso de componente. Puedes crear componentes Light directamente dentro de un objeto de juego, o crear un recurso de luz en el navegador *Assets* y después añadirlo como componente a un objeto de juego en la vista *Outline*.

Defold no aplica iluminación automáticamente a todos los materiales. El motor recopila las luces y las pone a disposición de los shaders mediante el buffer de luces incorporado. El shader del material decide cómo usar los datos de iluminación.

Los ejemplos siguientes usan la misma escena para mostrar cómo afectan los distintos tipos de luz al resultado final:

![Escena sin luces](images/light/no_light.png)

## Propiedades de las luces

Todos los colores de las luces son valores RGB. Los recursos de luz no usan el canal alfa.

### Luz ambiental

Las luces ambientales añaden una iluminación constante a la escena. No se ven afectadas por la posición, la rotación ni la escala del objeto de juego. Se pueden usar, por ejemplo, como iluminación general de fondo o para hacer que los objetos parezcan no estar iluminados.

El componente de luz ambiental se representa en el editor con un icono de flechas orientadas hacia el centro. El color del icono es el mismo que el de su propiedad `color`.

![Luz ambiental con menor intensidad](images/light/ambient_light_less_intensity.png)

Propiedades:

`color`
: El color RGB de la luz ambiental.

`intensity`
: Multiplica el color de la luz ambiental.

![Luz ambiental con mayor intensidad](images/light/ambient_light_full_intensity.png)

Las luces ambientales se acumulan en un único color ambiental `light_info.xyz` en el buffer de luces del shader. No ocupan entradas en el array `lights[]`. Varios componentes de luz ambiental en la escena producen un único color de salida que combina todos ellos.

### Luz direccional

Las luces direccionales representan la luz que procede de una dirección, como la luz solar. No usan la posición ni la escala del objeto de juego, pero la dirección de la luz se obtiene aplicando la rotación del objeto de juego en el espacio del mundo a la dirección frontal local `(0, 0, -1)`.

El componente de luz direccional se representa en el editor con un icono de sol coloreado y una flecha 3D que indica su dirección.

![Luz direccional](images/light/directional_light.png)

Propiedades:

`color`
: El color RGB de la luz direccional.

`intensity`
: Multiplica el color de la luz direccional.


Las luces direccionales suelen combinarse con una luz ambiental para evitar que las superficies orientadas en dirección opuesta a la luz direccional queden completamente oscuras.

![Luz direccional y ambiental](images/light/directional_and_ambient_light.png)

### Luz puntual

Las luces puntuales emiten luz hacia el exterior desde la posición del objeto de juego en el espacio del mundo. La posición de la luz puntual procede de la posición del objeto de juego en el espacio del mundo.

El componente de luz puntual se representa en el editor con un punto que emite rayos a su alrededor; su color representa su propiedad `color` y un círculo representa el `range`.

![Luz puntual](images/light/point_light.png)

Propiedades:

`color`
: El color RGB de la luz puntual.

`intensity`
: Multiplica el color de la luz puntual.

`range`
: El radio de la luz en unidades del mundo.

El rango efectivo se multiplica por el menor valor absoluto de los ejes de la escala del objeto de juego en el espacio del mundo.

![Rango de la luz puntual](images/light/point_light_range.png)

Cambiar el color de la luz tiñe la contribución de la luz puntual, mientras que el rango controla hasta dónde llega la luz desde la fuente.

![Rango de la luz puntual con color verde](images/light/point_ight_range_green_color.png)

### Luz focal

Las luces focales emiten luz en forma de cono desde la posición del objeto de juego en el espacio del mundo. La dirección se obtiene aplicando la rotación del objeto de juego en el espacio del mundo a `(0, 0, -1)`.

El componente de luz focal se representa en el editor con un icono de lámpara coloreado y líneas guía que muestran los conos exterior e interior.

![Luz focal](images/light/spot_light.png)

Propiedades:

`color`
: El color RGB de la luz focal.

`intensity`
: Multiplica el color de la luz focal.

`range`
: El radio de la luz en unidades del mundo.

`inner_cone_angle`
: El ángulo del cono interior, en grados, en el editor. Los píxeles dentro de este cono reciben toda la contribución de la luz focal.

`outer_cone_angle`
: El ángulo del cono exterior, en grados, en el editor. La luz se desvanece entre los conos interior y exterior.

El rango efectivo se multiplica por el menor valor absoluto de los ejes de la escala del objeto de juego en el espacio del mundo. Los ángulos de los conos se editan en grados y se convierten a radianes en el recurso de luz compilado.

![Gizmos de la luz focal](images/light/spot_light_gizmos.png)

## Validación

El pipeline de build valida y normaliza los datos de los recursos de luz:

- `color` debe contener exactamente tres números.
- `intensity` se limita a `0` o un valor superior.
- `range` se limita a `0` o un valor superior para las luces puntuales y focales.
- Los ángulos de los conos de las luces focales se limitan a `0..180` grados.
- `inner_cone_angle` se limita para que nunca supere `outer_cone_angle`.

## Límite del proyecto

La configuración del proyecto `light.max_count` controla el número máximo de componentes Light. El valor predeterminado es `64`.

Las luces ambientales no consumen entradas del array `lights[]` del shader, pero siguen siendo componentes Light y cuentan para `light.max_count`. Las luces direccionales, puntuales y focales consumen entradas de `lights[]` mientras están activas.

Si el número de componentes Light supera `light.max_count`, el motor informará de un error de buffer de componentes lleno.

## Buffer de luces en los shaders

Un shader puede acceder a las luces activas declarando un bloque uniform llamado `LightBuffer` con el layout incorporado. El motor detecta este bloque y vincula automáticamente los datos de las luces para los materiales y programas de cómputo que lo usan.

![Shader del buffer de luces](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: posición en el espacio del mundo, w: sin usar
    vec4 color;           // rgb: color, a: sin usar
    vec4 direction_range; // xyz: dirección normalizada en el espacio del mundo, w: rango
    vec4 params;          // x: tipo, y: intensidad, z: cono interior, w: cono exterior
};

uniform LightBuffer
{
    // xyz: color ambiental acumulado, w: número de luces no ambientales activas
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

El tipo de luz se almacena en `lights[i].params.x`:

| Tipo | Valor |
|------|-------|
| Direccional | `0` |
| Puntual | `1` |
| Focal | `2` |

El shader puede declarar un array `lights[]` más pequeño que `light.max_count`, pero no uno más grande. Limita siempre los bucles de luces al tamaño declarado del array:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Direccional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Puntual
        {
            result += light_color;
        }
        else if (type == 2) // Focal
        {
            result += light_color;
        }
    }

    return result;
}
```

El ejemplo anterior muestra el patrón de acceso al buffer. Un shader de luz puntual o focal real también debe calcular el vector desde el punto sombreado hasta `lights[i].position.xyz`, aplicar la atenuación por distancia mediante `lights[i].direction_range.w` y, para las luces focales, usar `lights[i].params.z` y `lights[i].params.w` como ángulos de los conos en radianes.

## Función auxiliar de iluminación incorporada

Defold incluye una función auxiliar para shaders en `/builtins/materials/lighting.glsl`. Define `MAX_LIGHT_COUNT`, proporciona los varyings que espera la función auxiliar y después inclúyela desde tu fragment shader:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

La función auxiliar define las constantes `LIGHT_DIRECTIONAL`, `LIGHT_POINT` y `LIGHT_SPOT`, expone `ambient_light()` y proporciona funciones de difusión Lambert para las luces del buffer.

## Véase también

- [Manual de shaders](/manuals/shader)
- [Manual de materiales](/manuals/material)
- [Manual de render](/manuals/render)
