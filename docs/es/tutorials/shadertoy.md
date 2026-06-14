---
brief: En este tutorial convertirás un shader de shadertoy.com a Defold.
layout: tutorial
locale: es
title: Tutorial de Shadertoy a Defold
---

# Tutorial Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) es un sitio que reúne shaders GL aportados por usuarios. Es un gran recurso para encontrar código de shader e inspiración. En este tutorial tomaremos un shader de Shadertoy y lo haremos funcionar en Defold. Se asume una comprensión básica de shaders. Si necesitas leer más, [el manual de Shader](/manuals/shader/) es un buen lugar para empezar.

El shader que usaremos es [Star Nest](https://www.shadertoy.com/view/XlfGRj) de Pablo Andrioli (usuario "Kali" en Shadertoy). Es un fragment shader puramente matemático y procedural de magia negra que renderiza un efecto de campo estelar realmente genial.

![Star Nest](../images/shadertoy/starnest.png)

El shader tiene solo 65 líneas de código GLSL bastante complicado, pero no te preocupes. Vamos a tratarlo como una caja negra que hace lo suyo a partir de unas pocas entradas simples. Nuestro trabajo aquí es modificar el shader para que interactúe con Defold en lugar de Shadertoy.

## Algo que texturizar

El shader Star Nest es un fragment shader puro, así que solo necesitamos algo que el shader pueda texturizar. Hay varias opciones: un sprite, un tilemap, una GUI o un modelo. Para este tutorial vamos a usar un modelo 3D simple. La razón es que podemos convertir fácilmente el renderizado del modelo en un efecto de pantalla completa---algo que necesitamos hacer si queremos realizar post processing visual, por ejemplo.

Podemos empezar desde un proyecto vacío.

1. Abre Defold y selecciona Create From *Templates*.
2. Selecciona *Empty Project*.
3. Define el *Title* y selecciona *Location* en tu disco.
4. Haz click en <kbd>Create New Project</kbd>.

![start](../images/shadertoy/empty_project.png)

Puedes usar una mesh `quad.gltf` integrada desde `builtins/assets/meshes`.

Opcionalmente, también puedes crear una mesh de plano cuadrático en Blender o cualquier otro programa de modelado 3D --- por comodidad, las 4 coordenadas de vértice están en -1 y 1 en el eje X y -1 y 1 en el eje Y. Blender tiene el eje Z hacia arriba por defecto, así que necesitas rotar la mesh 90° alrededor del eje X. También debes asegurarte de generar coordenadas UV correctas para la mesh. En Blender, entra en *Edit Mode* con la mesh seleccionada, luego selecciona <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender es software 3D gratuito y open-source que se puede descargar desde [blender.org](https://www.blender.org).
</div>

![quad in Blender](../images/shadertoy/quad_blender.png)

1. Abre tu archivo "main.collection" en Defold y crea un nuevo objeto de juego "star-nest".
2. Agrega un componente *Model* al objeto de juego "star-nest".
3. Define la propiedad *Mesh* a nuestro `quad.gltf`.
4. Necesitamos definir el material para el modelo, así que por ahora selecciona el `model.material` integrado.

El modelo debería aparecer en el editor de escena, pero se renderiza completamente negro. Esto se debe a que todavía no tiene textura definida:

![quad in Defold](../images/shadertoy/quad_default_material.png)

## Crear el material

1. Crea un nuevo archivo de material *`star-nest.material`* haciendo click con <kbd>Right Mouse Button</kbd> en la carpeta `main` del panel `Assets` y seleccionando <kbd>New</kbd>-><kbd>Material</kbd>, y nómbralo `star-nest`.

 ![material](../images/shadertoy/new_material.png)

2. De la misma manera, crea un vertex shader program `star-nest.vp` y un fragment shader program `star-nest.fp`:
3. Abre *star-nest.material*.
4. Define *Vertex Program* como `star-nest.vp`.
5. Define *Fragment Program* como `star-nest.fp`.
6. Agrega una *Vertex Constant* y llámala "`view_proj`" de tipo `Viewproj` (por "view projection").
8. Agrega un tag "tile" a *Tags*. Esto hace que el quad se incluya en el render pass cuando se dibujan sprites y tiles.

 ![material](../images/shadertoy/material.png)

### Vertex program

1. Abre el archivo de vertex shader program `star-nest.vp`. Debería contener el siguiente código:

    ```glsl
    #version 140

    // las posiciones están en espacio del mundo
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Fragment program

1. Abre el archivo de fragment shader program `star-nest.fp` y modifica el código para que el color del fragmento se defina según las coordenadas X e Y de las coordenadas UV (`var_texcoord0`). Hacemos esto para asegurarnos de que tenemos el modelo configurado correctamente:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Define la propiedad `Material` con nuestro material `star-nest` recién creado en el componente model del objeto de juego `star-nest` en `main.collection`.

Ahora el editor debería renderizar el modelo con el nuevo shader y podemos ver claramente si las coordenadas UV son correctas; la esquina inferior izquierda debería tener color negro (0, 0, 0), la esquina superior izquierda color verde (0, 1, 0), la esquina superior derecha color amarillo (1, 1, 0) y la esquina inferior derecha debería tener color rojo (1, 0, 0):

![quad in Defold](../images/shadertoy/quad_material.png)

## Cámara

Ahora podemos ejecutar nuestro proyecto (<kbd>Project</kbd>-><kbd>Build</kbd> o el atajo <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), pero veremos una pantalla negra (bueno, casi, salvo quizá un pixel diminuto en la esquina inferior izquierda). Esto ocurre porque no hay cámara, y el render script predeterminado usa un fallback simple que muestra un espacio 2D enorme, mientras que nuestro modelo está en la posición (0,0,0) con solo 1 de ancho.

Agreguemos un objeto de juego con un componente de cámara para definir lo que veremos en el juego.

1. Agrega un objeto de juego llamado `camera` con posición (0,0,1). (Es importante definir la coordenada Z en 1, para que este objeto de juego esté delante de nuestro modelo, ya que el eje Z apunta ahora, en la configuración 2D predeterminada, hacia nosotros).
2. Agrega un componente `Camera` y verás una vista previa de cámara con nuestro quad dentro. Con las propiedades predeterminadas tenemos suerte en esta configuración y no necesitamos cambiar nada; ya deberíamos ver el resultado correcto, excepto por una cosa: no necesitamos un frustum de vista de cámara tan enorme, así que podemos reducir `Far Z` a `2`.

![camera](../images/shadertoy/camera.png)

Opcionalmente, podemos cambiar el tipo de cámara definiendo `Orthographic Projection` como `true`, y luego ajustar también `Orthographic Zoom` a algo como 600, pero en este caso no tendremos una relación de aspecto automática, así que nuestro modelo no llenará la pantalla.

## El shader star nest

Ahora que todo está en su lugar, empecemos a trabajar en el código real del shader. Primero veamos el código original. Consta de algunas secciones:

![Star Nest shader code](../images/shadertoy/starnest_code.png)

Usaremos un pipeline moderno con GLSL en versión 140; para hacerlo, declararemos la versión al inicio del archivo con `#version 140`.

1. Las líneas 5--18 definen un montón de constantes. Podemos dejarlas tal cual. Son constantes GLSL simples y no dependen específicamente de Shadertoy ni de Defold.

2. Las líneas 21 y 63 contienen las coordenadas de textura de espacio de pantalla X e Y del fragmento de entrada (`in vec2 fragCoord`) y el color de fragmento de salida (`out vec4 fragColor`).

    Defold pasa coordenadas de textura desde el vertex shader al fragment shader a través de una variable interpolada como coordenadas UV (en el rango 0--1). En nuestro vertex shader esto se declara con un calificador `out`:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     En el fragment shader, el mismo valor se recibe con un calificador `in`:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Luego, en GLSL 140, declaramos una salida de fragment explícita con el calificador `out`:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Así que donde el código Shadertoy original escribe en `fragColor`, nuestro shader Defold escribe en `out_fragColor`.

3. Las líneas 23--27 configuran las dimensiones de la textura, así como la dirección de movimiento y el tiempo escalado. En Shadertoy, el shader recibe la posición de pixel mediante `fragCoord` y la resolución del viewport de la textura/viewport se pasa al shader como `uniform vec3 iResolution`. El shader calcula coordenadas estilo UV con la relación de aspecto correcta a partir de las coordenadas de fragmento y la resolución. También se aplica cierto desplazamiento de resolución para obtener un encuadre más agradable.

    En Defold, no partimos de coordenadas de pixel. En su lugar, ya recibimos coordenadas UV normalizadas desde el vertex shader a través de `var_texcoord0`. Estas coordenadas están en el rango de `0.0` a `1.0` a través del quad renderizado.

    La versión de Defold necesita alterar estos cálculos para usar las coordenadas UV de `var_texcoord0`.
    Una conversión típica se ve así:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    El valor exacto de `aspect` depende de cómo esté configurado el ejemplo. Si el efecto se renderiza en un quad de pantalla completa con un tamaño de display conocido, la relación de aspecto puede hardcodearse para el tutorial. Si el efecto necesita soportar tamaños de ventana arbitrarios, pasa la resolución como una constante de fragmento y colócala dentro de un bloque uniform GLSL 140.

    El tiempo también se configura aquí. Se pasa al shader como `uniform float iGlobalTime`. Defold (desde 1.12.3) proporciona tiempo a los shaders mediante una constante especial `Time` que usaremos.

    En Defold moderno, los uniforms no opacos se declaran dentro de bloques uniform.
    En el fragment shader lo declaramos así:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Luego, en `star-nest.material`, agregaremos una Fragment Constant llamada `time` y definiremos su tipo como `Time`.

    El valor puede usarse así:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    donde `time.x` es el tiempo desde el inicio del motor, y `time.y` es el delta time desde el frame anterior.

4. Las líneas 29--39 configuran la rotación del renderizado volumétrico, con la posición del mouse afectando la rotación. Las coordenadas del mouse se pasan al shader como `uniform vec4 iMouse`.

    Para este tutorial vamos a omitir el input del mouse.

5. Las líneas 41--62 son el núcleo del shader. Podemos dejar este código tal cual.

## El shader star nest modificado

Recorrer las secciones anteriores y hacer los cambios necesarios da como resultado el siguiente código de shader. Se limpió un poco para mejorar la legibilidad. Se indican las diferencias entre las versiones de Defold y Shadertoy:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// obtiene coordenadas y dirección
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// renderizado volumétrico
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// repetición plegada
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// la fórmula mágica
			p = abs(p) / dot(p, p) - formuparam;

			// suma absoluta del cambio promedio
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// materia oscura
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// materia oscura, no renderizar cerca
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloreado basado en distancia
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// ajuste de color
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Declaramos #version 140 al inicio del archivo para usar el pipeline GLSL moderno de Defold. Luego dejamos los defines tal cual.
2. El vertex shader pasa coordenadas UV al fragment shader mediante var_texcoord0. En GLSL 140, el fragment shader recibe este valor interpolado con el calificador in.
3. En GLSL 140, el fragment shader debe declarar una variable de salida explícita en lugar de escribir en gl_FragColor. Aquí usamos out vec4 out_fragColor.
4. La constante de material Time de Defold se expone al shader a través de un bloque uniform. En star-nest.material, agrega una Fragment Constant llamada time y define su tipo como Time.
5. Shadertoy usa mainImage(out vec4 fragColor, in vec2 fragCoord). En Defold usamos el punto de entrada normal void main(), leemos las coordenadas UV interpoladas desde var_texcoord0 y escribimos el color final en out_fragColor.
6. Para este tutorial definimos un valor estático de resolución/aspecto para el renderizado. Actualmente el modelo es cuadrado, así que podemos usar vec2 res = vec2(1.0, 1.0);. Con un modelo rectangular de tamaño 1280×720, podríamos usar en su lugar vec2 res = vec2(1.78, 1.0); y multiplicar las coordenadas UV con eso para preservar la relación de aspecto correcta.
7. El shader Shadertoy original usa iGlobalTime. En esta versión de Defold, time.x contiene el tiempo desde el inicio del motor, así que lo asignamos a una variable local iGlobalTime y lo usamos para animar el movimiento de cámara a través del campo estelar.
8. Mantenemos este tutorial simple eliminando por completo los valores iMouse. La rotación en sí se conserva, porque reduce la simetría visual en el renderizado volumétrico.
9. Finalmente, el shader escribe el color de fragmento resultante en out_fragColor.

Guarda el fragment shader program. El modelo ahora debería estar bien texturizado con un campo estelar en el editor de escena y en runtime:

![quad with starnest](../images/shadertoy/quad_starnest.png)


## Animación

La última pieza del puzzle es introducir tiempo para hacer que las estrellas se muevan. Defold (desde 1.12.3) proporciona esto automáticamente mediante una constante de fragmento de tipo `Time`.

1. Abre *star-nest.material*.
2. Agrega una *Fragment Constant* y llámala "time".
3. Define su *Type* como `Time`.

![time constant](../images/shadertoy/time_constant.png)

¡Y eso es todo! Ya manejamos este `time` en el fragment shader. ¡Terminamos!

## Ejercicios

Un ejercicio de continuación divertido es agregar al shader el input original de movimiento del mouse. Necesitarás crear una nueva Fragment Constant, esta vez de tipo `User`, y actualizarla en `on_input` en algún script que detecte movimiento del mouse usando la función `go.set()` y definiendo las coordenadas de input en la nueva constante.

¡Feliz Defolding!
