---
title: Mostrar imágenes 2D
brief: Este manual describe cómo mostrar imágenes y animaciones 2D usando el componente Sprite.
---

# Sprites

Un componente Sprite es una imagen simple o una animación flipbook que se muestra en pantalla.

![sprite](images/graphics/sprite.png)

El componente Sprite puede usar un [Atlas](/manuals/atlas) o un [Tile Source](/manuals/tilesource) para sus gráficos.

## Propiedades del sprite

Además de las propiedades *Id*, *Position* y *Rotation*, existen las siguientes propiedades específicas del componente:

*Image*
: Si el shader tiene un solo sampler, este campo se llama `Image`. De lo contrario, cada slot toma el nombre del sampler de textura en el material.
Cada slot especifica el recurso de Atlas o Tile Source que se usará para el sprite en ese sampler de textura.

*Default Animation*
: La animación que se usará para el sprite. La información de la animación se toma del primer Atlas o Tile Source.

*Material*
: El material que se usará para renderizar el sprite.

*Blend Mode*
: El modo de mezcla que se usará al renderizar el sprite.

*Size Mode*
: Si se establece en `Automatic`, el editor definirá un tamaño para el sprite. Si se establece en `Manual`, puedes definir el tamaño tú mismo.

*Slice 9*
: Configura esta opción para preservar el tamaño en píxeles de la textura del sprite alrededor de los bordes cuando se redimensiona el sprite.

:[Slice-9](../shared/slice-9-texturing.md)

### Modos de mezcla
:[blend-modes](../shared/blend-modes.md)

## Manipulación en runtime

Puedes manipular sprites en runtime mediante distintas funciones y propiedades (consulta la [documentación de la API para su uso](/ref/sprite/)). Funciones:

* `sprite.play_flipbook()` - Reproduce una animación en un componente Sprite.
* `sprite.set_hflip()` y `sprite.set_vflip()` - Define el volteo horizontal y vertical en la animación de un sprite.

Un sprite también tiene varias propiedades que se pueden manipular con `go.get()` y `go.set()`:

`cursor`
: El cursor normalizado de la animación (`number`).

`image`
: La imagen del sprite (`hash`). Puedes cambiarla con una propiedad de recurso de Atlas o Tile Source y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/sprite/#image).

`material`
: El material del sprite (`hash`). Puedes cambiarlo con una propiedad de recurso de material y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/sprite/#material).

`playback_rate`
: La velocidad de reproducción de la animación (`number`).

`scale`
: La escala no uniforme del sprite (`vector3`).

`size`
: El tamaño del sprite (`vector3`). Solo se puede cambiar si la propiedad `Size Mode` del sprite está establecida en `Manual`.

## Constantes de material

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: El tinte de color del sprite (`vector4`). El `vector4` se usa para representar el tinte con `x`, `y`, `z` y `w` correspondientes al tinte rojo, verde, azul y alfa.

## Atributos de material

Un sprite puede sobrescribir atributos de vértice del material asignado actualmente; estos se pasarán al vertex shader desde el componente (consulta el [manual de Material para más detalles](/manuals/material/#attributes)).

Los atributos especificados en el material aparecerán como propiedades normales en el inspector y se pueden definir en componentes Sprite individuales. Si alguno de los atributos se sobrescribe, aparecerá como una propiedad sobrescrita y se almacenará en el archivo de sprite en disco:

![sprite-attributes](../images/graphics/sprite-attributes.png)

## Configuración del proyecto

El archivo *game.project* tiene algunas [opciones de configuración del proyecto](/manuals/project-settings#sprite) relacionadas con los sprites.

## Sprites con múltiples texturas {#multi-textured-sprites}

Cuando un sprite usa múltiples texturas, hay algunas cosas que conviene tener en cuenta.

### Animaciones

Los datos de animación (fps, nombres de frames) se toman actualmente de la primera textura. A esta la llamaremos la "animación guía".

Los ids de imagen de la animación guía se usan para buscar las imágenes en otra textura.
Por eso es importante asegurarte de que los ids de frame coincidan entre texturas.

Por ejemplo, si tu `diffuse.atlas` tiene una animación `run` así:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Entonces los ids de frame serían `run/hero_run_color_1`, lo que probablemente no se encontraría, por ejemplo, en un `normal.atlas`:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Por eso usamos `Rename patterns` en el [atlas](/manuals/material/) para renombrarlos.
Define `_color=` y `_normal=` en los atlas correspondientes, y obtendrás nombres de frame como estos en ambos atlas:

```
run/hero_run_1
run/hero_run_2
...
```

### UVs

Las UV se toman de la primera textura. Como solo hay un conjunto de vértices, no podemos garantizar una buena coincidencia si las texturas secundarias tienen más coordenadas UV o una forma diferente.

Es importante tener esto en cuenta, así que asegúrate de que las imágenes tengan formas suficientemente similares; de lo contrario, podrías experimentar sangrado de textura.

Las dimensiones de las imágenes en cada textura pueden ser diferentes.
