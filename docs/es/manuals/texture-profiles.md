---
title: Perfiles de textura en Defold
brief: Defold admite procesamiento automático de texturas y compresión de datos de imagen. Este manual describe la funcionalidad disponible.
---

# Perfiles de textura {#texture-profiles}

Defold admite procesamiento automático de texturas y compresión de datos de imagen (en *Atlas*, *Tile sources*, *Cubemaps* y texturas independientes usadas para modelos, GUI, etc.).

Existen dos tipos de compresión: compresión de imagen por software y compresión de texturas por hardware.

1. La compresión por software (como PNG y JPEG) reduce el tamaño de almacenamiento de los recursos de imagen. Esto hace que el tamaño final del bundle sea menor. Sin embargo, los archivos de imagen deben descomprimirse cuando se leen en memoria, así que aunque una imagen sea pequeña en disco, puede tener una gran huella de memoria.

2. La compresión de texturas por hardware también reduce el tamaño de almacenamiento de los recursos de imagen. Pero, a diferencia de la compresión por software, reduce la huella en memoria de las texturas. Esto se debe a que el hardware gráfico puede manejar directamente texturas comprimidas sin tener que descomprimirlas primero.

El procesamiento de texturas se configura mediante un perfil de textura específico. En este archivo creas _perfiles_ que expresan qué formato(s) comprimido(s) y qué tipo deben usarse al crear bundles para una plataforma específica. Luego, los _perfiles_ se vinculan a _patrones de rutas_ coincidentes, lo que permite un control fino sobre qué archivos del proyecto deben comprimirse y exactamente cómo.

Como toda la compresión de texturas por hardware disponible es con pérdida, obtendrás artefactos en los datos de textura. Estos artefactos dependen mucho del aspecto del material fuente y del método de compresión usado. Debes probar tu material fuente y experimentar para obtener los mejores resultados. Google puede ser útil aquí.

Puedes seleccionar qué compresión de imagen por software se aplica a los datos finales de textura (comprimidos o sin procesar) en los archivos del bundle. Defold admite los formatos de compresión [Basis Universal](https://github.com/BinomialLLC/basis_universal) y [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
La compresión es una operación intensiva en recursos y consume tiempo; puede causar tiempos de build _muy_ largos según la cantidad de imágenes de textura que se deban comprimir y también según los formatos de textura elegidos y el tipo de compresión por software.
:::

### Basis Universal {#basis-universal}

Basis Universal (o BasisU para abreviar) comprime la imagen en un formato intermedio que se transcodifica en runtime a un formato de hardware adecuado para la GPU del dispositivo actual. El formato Basis Universal es de alta calidad, pero con pérdida.
Todas las imágenes también se comprimen con LZ4 para reducir aún más el tamaño de archivo cuando se almacenan en el archivo del juego.

### ASTC {#astc}

ASTC es un formato de compresión de texturas flexible y eficiente desarrollado por ARM y estandarizado por Khronos Group. Ofrece una amplia variedad de tamaños de bloque y tasas de bits, lo que permite a los desarrolladores equilibrar de forma efectiva la calidad de imagen y el uso de memoria. ASTC admite varios tamaños de bloque, desde 4x4 hasta 12x12 texels, correspondientes a tasas de bits que van desde 8 bits por texel hasta 0.89 bits por texel. Esta flexibilidad permite un control detallado del equilibrio entre la calidad de textura y los requisitos de almacenamiento.

ASTC admite varios tamaños de bloque, desde 4x4 hasta 12x12 texels, correspondientes a tasas de bits que van desde 8 bits por texel hasta 0.89 bits por texel. Esta flexibilidad permite un control detallado del equilibrio entre la calidad de textura y los requisitos de almacenamiento. La siguiente tabla muestra los tamaños de bloque admitidos y sus tasas de bits correspondientes:

| Tamaño de bloque (ancho x alto) | Bits por pixel |
| ------------------------------- | -------------- |
| 4x4                             | 8.00           |
| 5x4                             | 6.40           |
| 5x5                             | 5.12           |
| 6x5                             | 4.27           |
| 6x6                             | 3.56           |
| 8x5                             | 3.20           |
| 8x6                             | 2.67           |
| 10x5                            | 2.56           |
| 10x6                            | 2.13           |
| 8x8                             | 2.00           |
| 10x8                            | 1.60           |
| 10x10                           | 1.28           |
| 12x10                           | 1.07           |
| 12x12                           | 0.89           |


#### Dispositivos compatibles {#supported-devices}

Aunque ASTC ofrece grandes resultados, no es compatible con todas las tarjetas gráficas. Esta es una pequeña lista de dispositivos compatibles según el proveedor:

| Proveedor de GPU   | Soporte                                                                         |
| ------------------ | ------------------------------------------------------------------------------- |
| ARM (Mali)         | Todas las GPU ARM Mali que admiten OpenGL ES 3.2 o Vulkan admiten ASTC.         |
| Qualcomm (Adreno)  | Las GPU Adreno que admiten OpenGL ES 3.2 o Vulkan admiten ASTC.                 |
| Apple              | Las GPU Apple desde el chip A8 admiten ASTC.                                    |
| NVIDIA             | El soporte de ASTC es principalmente para GPU móviles (p. ej., chips Tegra).     |
| AMD (Radeon)       | Las GPU AMD que admiten Vulkan generalmente admiten ASTC mediante software.      |
| Intel (Integrated) | ASTC es compatible con GPU Intel modernas mediante software.                     |

## Archivo de perfiles de textura {#texture-profiles-1}

Cada proyecto contiene un archivo *.texture_profiles* específico que contiene la configuración usada al comprimir texturas. De forma predeterminada, este archivo es *builtins/graphics/default.texture_profiles* y tiene una configuración que asocia cada recurso de textura con un perfil que usa RGBA sin compresión de texturas por hardware y con la compresión de archivo ZLib predeterminada.

Para agregar compresión de texturas:

- Selecciona <kbd>File ▸ New...</kbd> y elige *Texture Profiles* para crear un nuevo archivo de perfiles de textura. (Como alternativa, copia *default.texture_profiles* a una ubicación fuera de *builtins*)
- Elige un nombre y una ubicación para el nuevo archivo.
- Cambia la entrada *texture_profiles* en *game.project* para que apunte al nuevo archivo.
- Abre el archivo *.texture_profiles* y configúralo según tus requisitos.

![Nuevo archivo de perfiles](images/texture_profiles/texture_profiles_new_file.png)

![Configurar el perfil de textura](images/texture_profiles/texture_profiles_game_project.png)

Puedes activar y desactivar el uso de perfiles de textura en las preferencias del editor. Selecciona <kbd>File ▸ Preferences...</kbd>. La pestaña *General* contiene la casilla *Enable texture profiles*.

![Preferencias de perfiles de textura](images/texture_profiles/texture_profiles_preferences.png)

## Configuración de rutas {#path-settings}

La sección *Path Settings* del archivo de perfiles de textura contiene una lista de patrones de ruta y qué *perfil* usar al procesar recursos que coinciden con la ruta. Las rutas se expresan como patrones "Ant Glob" (consulta la [documentación](http://ant.apache.org/manual/dirtasks.html#patterns) para más detalles). Los patrones pueden expresarse usando los siguientes comodines:

`*`
: Coincide con cero o más caracteres. Por ejemplo, `sprite*.png` coincide con los archivos *`sprite.png`*, *`sprite1.png`* y *`sprite_with_a_long_name.png`*.

`?`
: Coincide exactamente con un carácter. Por ejemplo: `sprite?.png` coincide con los archivos *sprite1.png*, *`spriteA.png`*, pero no con *`sprite.png`* ni *`sprite_with_a_long_name.png`*.

`**`
: Coincide con un árbol completo de directorios o, cuando se usa como nombre de directorio, con cero o más directorios. Por ejemplo: `/gui/**` coincide con todos los archivos del directorio */gui* y todos sus subdirectorios.

![Rutas](images/texture_profiles/texture_profiles_paths.png)

Este ejemplo contiene dos patrones de ruta y sus perfiles correspondientes.

`/gui/**/*.atlas`
: Todos los archivos *.atlas* en el directorio *`/gui`* o cualquiera de sus subdirectorios se procesarán según el perfil "gui_atlas".

`/**/*.atlas`
: Todos los archivos *.atlas* en cualquier lugar del proyecto se procesarán según el perfil "atlas".

Ten en cuenta que la ruta más genérica se coloca al final. El algoritmo de coincidencia funciona de arriba hacia abajo. Se usará la primera ocurrencia que coincida con la ruta del recurso. Una expresión de ruta coincidente más abajo en la lista nunca anula la primera coincidencia. Si las rutas se hubieran colocado en el orden opuesto, todos los atlas se habrían procesado con el perfil "atlas", incluso los del directorio *`/gui`*.

Los recursos de textura que _no_ coincidan con ninguna ruta del archivo de perfiles se compilarán y escalarán a la potencia de 2 más cercana, pero por lo demás se dejarán intactos.

## Perfiles {#profiles}

La sección *profiles* del archivo de perfiles de textura contiene una lista de perfiles con nombre. Cada perfil contiene una o más *plataformas*, y cada plataforma se describe mediante una lista de propiedades.

![Perfiles](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Especifica una plataforma coincidente. `OS_ID_GENERIC` coincide con todas las plataformas, `OS_ID_WINDOWS` coincide con bundles objetivo de Windows, `OS_ID_IOS` coincide con bundles de iOS, y así sucesivamente. Ten en cuenta que si se especifica `OS_ID_GENERIC`, se incluirá para todas las plataformas.

::: important
Si dos [configuraciones de rutas](#path-settings) coinciden con el mismo archivo y la ruta usa perfiles diferentes con plataformas diferentes, se usarán **ambos** perfiles y se generarán **dos** texturas.
:::

*Formats*
: Uno o más formatos de textura para generar. Si se especifican varios formatos, se generan texturas para cada formato y se incluyen en el bundle. El motor selecciona texturas de un formato compatible con la plataforma en runtime.

*Mipmaps*
: Si está marcada, se generan mipmaps para la plataforma. Está desmarcada de forma predeterminada.

*Premultiply alpha*
: Si está marcada, el alpha se premultiplica en los datos de textura. Está marcada de forma predeterminada.

*Max Texture Size*
: Si se define con un valor distinto de cero, las texturas se limitan en tamaño de pixeles al número especificado. Cualquier textura que tenga un ancho o alto mayor que el valor especificado se escalará hacia abajo.

Los *Formats* agregados a un perfil tienen cada uno las siguientes propiedades:

*Format*
: El formato que se usará al codificar la textura. Consulta más abajo todos los formatos de textura disponibles.

*Compressor*
: El compresor que se usará al codificar la textura.

*Compressor Preset*
: Selecciona un preset de compresión para codificar la imagen comprimida resultante. Cada preset de compresor es único para el compresor y su configuración depende del propio compresor. Para simplificar estas opciones, los presets de compresión actuales vienen en cuatro niveles:

| Preset    | Nota                                                   |
| --------- | ------------------------------------------------------ |
| `LOW`     | Compresión más rápida. Calidad de imagen baja          |
| `MEDIUM`  | Compresión predeterminada. Mejor calidad de imagen     |
| `HIGH`    | Compresión más lenta. Tamaño de archivo menor          |
| `HIGHEST` | Compresión lenta. Tamaño de archivo mínimo             |

Ten en cuenta que el compresor `uncompressed` solo tiene un preset llamado `uncompressed`, lo que significa que no se aplicará compresión a las texturas.
Para ver la lista de compresores disponibles, consulta [Compresores](#compressors)

## Formatos de textura {#texture-formats}

Las texturas de hardware gráfico pueden procesarse como datos sin comprimir o datos comprimidos *con pérdida*, con distintos números de canales y profundidades de bits. La compresión por hardware es fija, lo que significa que la imagen resultante tendrá un tamaño fijo, independientemente del contenido de la imagen. Esto significa que la pérdida de calidad durante la compresión depende del contenido de la textura original.

Como la transcodificación de compresión Basis Universal depende de las capacidades de la GPU del dispositivo, los formatos recomendados para usar con la compresión Basis Universal son los formatos genéricos como:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` y `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

El transcodificador Basis Universal admite muchos formatos de salida, como `ASTC4x4`, `BCx`, `ETC2`, `ETC1` y `PVRTC1`.

Actualmente se admiten los siguientes formatos de compresión con pérdida:

| Formato                           | Compresión | Detalles                                                                           |
| --------------------------------- | ---------- | ---------------------------------------------------------------------------------- |
| `TEXTURE_FORMAT_RGB`              | ninguna    | Color de 3 canales. El alpha se descarta                                           |
| `TEXTURE_FORMAT_RGBA`             | ninguna    | Color de 3 canales y alpha completo.                                               |
| `TEXTURE_FORMAT_RGB_16BPP`        | ninguna    | Color de 3 canales. 5+6+5 bits.                                                    |
| `TEXTURE_FORMAT_RGBA_16BPP`       | ninguna    | Color de 3 canales y alpha completo. 4+4+4+4 bits.                                 |
| `TEXTURE_FORMAT_LUMINANCE`        | ninguna    | Escala de grises de 1 canal, sin alpha. Canales RGB multiplicados en uno. El alpha se descarta. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | ninguna    | Escala de grises de 1 canal y alpha completo. Canales RGB multiplicados en uno.    |

Para ASTC, el número de canales siempre será 4 (RGB + alpha), y el propio formato define el tamaño de la compresión de bloque.
Ten en cuenta que estos formatos solo son compatibles con un compresor ASTC; cualquier otra combinación producirá un error de build.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Compresores {#compressors}

Defold admite los siguientes compresores de textura de forma predeterminada. Los datos se descomprimen cuando el archivo de textura se carga en memoria.

| Nombre                            | Formatos                  | Nota                                                                                           |
| --------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Todos los formatos        | No se aplicará compresión. Predeterminado.                                                     |
| `BasisU`                          | Todos los formatos RGB/RGBA | Compresión Basis Universal de alta calidad, con pérdida. Un nivel de calidad menor produce un tamaño menor. |
| `ASTC`                            | Todos los formatos ASTC   | Compresión ASTC con pérdida. Un nivel de calidad menor produce un tamaño menor.                 |

::: sidenote
Defold admite compresores instalables en el pipeline de compresión de texturas. Esto hace posible implementar un algoritmo de compresión de texturas en una extensión, como WEBP o algo completamente personalizado.
:::

## Imagen de ejemplo {#example-image}

Para dar una mejor idea de la salida, aquí hay un ejemplo.
Ten en cuenta que la calidad de imagen, el tiempo de compresión y el tamaño comprimido siempre dependen de la imagen de entrada y pueden variar.

Imagen base (1024x512):
![Nuevo archivo de perfiles](images/texture_profiles/kodim03_pow2.png)

### Tiempos de compresión {#compression-times}

| Preset    | Tiempo de compresión | Tiempo relativo |
| --------- | -------------------- | --------------- |
| `LOW`     | 0m0.143s             | 0.5x            |
| `MEDIUM`  | 0m0.294s             | 1.0x            |
| `HIGH`    | 0m1.764s             | 6.0x            |
| `HIGHEST` | 0m1.109s             | 3.8x            |

### Pérdida de señal {#signal-loss}

La comparación se hace usando la herramienta `basisu` (midiendo el PSNR).
100 dB significa que no hay pérdida de señal (es decir, es igual que la imagen original).

| Preset    | Señal                                           |
| --------- | ----------------------------------------------- |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Tamaños de los archivos comprimidos {#compression-file-sizes}

El tamaño del archivo original es 1572882 bytes.

| Preset    | Tamaños de archivo | Proporción |
| --------- | ------------------ | ---------- |
| `LOW`     | 357225             | 22.71 %    |
| `MEDIUM`  | 365548             | 23.24 %    |
| `HIGH`    | 277186             | 17.62 %    |
| `HIGHEST` | 254380             | 16.17 %    |


### Calidad de imagen {#image-quality}

Estas son las imágenes resultantes (obtenidas de la codificación ASTC usando la herramienta `basisu`)

`LOW`
![preset de compresión bajo](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![preset de compresión medio](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![preset de compresión alto](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![mejor preset de compresión](images/texture_profiles/kodim03_pow2.best.png)
