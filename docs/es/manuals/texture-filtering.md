---
title: Filtrado de texturas
brief: Este manual describe las opciones disponibles para el filtrado de texturas al renderizar gráficos.
---

# Filtrado y muestreo de texturas

El filtrado de texturas decide el resultado visual en los casos en que un _texel_ (un píxel en una textura) no está perfectamente alineado con un píxel de la pantalla. Esto ocurre cuando mueves un elemento gráfico que contiene la textura menos de un píxel. Están disponibles los siguientes métodos de filtrado:

Nearest
: Se elegirá el texel más cercano para colorear el píxel de la pantalla. Este método de muestreo debe elegirse si quieres un mapeo perfecto uno a uno de píxeles entre tus texturas y lo que ves en pantalla. Con el filtrado nearest, todo saltará de píxel en píxel al moverse. Esto puede verse tembloroso si el sprite se mueve lentamente.

Linear
: El texel se promediará con sus vecinos antes de colorear el píxel de la pantalla. Esto produce una apariencia suave para movimientos lentos y continuos, ya que un sprite se mezclará con los píxeles antes de colorearlos por completo; por lo tanto, es posible mover un sprite menos de un píxel entero.

La configuración del filtrado que se debe usar se almacena en el archivo de [configuración del proyecto](/manuals/project-settings/#graphics). Hay dos ajustes:

default_texture_min_filter
: El filtrado de minificación se aplica cuando el texel es más pequeño que el píxel de la pantalla.

default_texture_mag_filter
: El filtrado de magnificación se aplica cuando el texel es más grande que el píxel de la pantalla.

Ambos ajustes aceptan los valores `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` o `linear_mipmap_linear`. Por ejemplo:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Si no especificas nada, ambos se establecen en `linear` de forma predeterminada.

Ten en cuenta que la configuración en *game.project* se usa en los samplers predeterminados. Si especificas samplers en un material personalizado, puedes definir el método de filtrado de forma específica para cada sampler. Consulta el [manual de materiales](/manuals/material/) para más detalles.
