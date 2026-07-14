---
title: Optimizar el tamaño de un juego Defold
brief: Este manual describe cómo optimizar el tamaño de un juego Defold.
---

# Optimizar el tamaño del juego

El tamaño de tu juego puede ser un factor crítico de éxito para plataformas como web y móviles, mientras que tiene menos importancia en escritorio y consolas, donde el espacio en disco es barato y suele ser abundante.

### iOS y Android
Apple y Google han definido límites de tamaño de aplicación al descargar a través de redes móviles (a diferencia de descargar por Wifi). Para Android este límite es de 200 MB para apps publicadas con [app bundles](https://developer.android.com/guide/app-bundle#size_restrictions). En iOS, los usuarios recibirán una advertencia si la aplicación supera los 200 MB, pero podrán continuar con la descarga.

::: sidenote
Según un estudio de 2017, se demostró que "por cada aumento de 6 MB en el tamaño de un APK, vemos una disminución del 1% en la tasa de conversión de instalaciones". ([fuente](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki y muchas otras plataformas de juegos web recomiendan que la descarga inicial no supere los 5 MB.

Facebook recomienda que un Facebook Instant Game arranque en menos de 5 segundos y, preferiblemente, en menos de 3 segundos. Lo que esto significa para el tamaño real de la aplicación no está definido con claridad, pero hablamos de tamaños en el rango de hasta 20 MB.

Los anuncios jugables suelen estar limitados a entre 2 y 5 MB, según la red publicitaria.

## Estrategias de optimización de tamaño
Puedes optimizar el tamaño de la aplicación de dos formas: reduciendo el tamaño del motor o reduciendo el tamaño de los assets del juego.

Para comprender mejor qué compone el tamaño de tu aplicación, puedes [generar un reporte de build](/manuals/bundling/#build-reports) al crear el bundle. Es bastante común que los sonidos y los gráficos ocupen la mayor parte del tamaño de cualquier juego.

::: important
Defold creará un árbol de dependencias al crear la build y el bundle de tu aplicación. El sistema de build empezará desde la colección bootstrap especificada en el archivo *game.project* e inspeccionará cada colección, objeto de juego y componente referenciados para crear una lista de los assets que están en uso. Solo esos assets se incluirán en el bundle final de la aplicación. Todo lo que no esté referenciado directamente se excluirá. Aunque es bueno saber que los assets no usados no se incluirán, como desarrollador aún debes considerar qué entra en la aplicación final, el tamaño de los assets individuales y el tamaño total del bundle de la aplicación.
:::

## Optimizar el tamaño del motor
Una forma rápida de reducir el tamaño del motor es eliminar funcionalidades del motor que no usas. Esto se hace en el [archivo de manifiesto de la aplicación](https://defold.com/manuals/app-manifest/), donde es posible eliminar componentes del motor que no necesitas. Ejemplos:

* Physics - Si tu juego no usa físicas de Box2D o Bullet3D, se recomienda encarecidamente eliminar los motores de físicas
* LiveUpdate - Si tu juego no usa LiveUpdate, se puede eliminar
* Image loaded - Si tu juego no carga y decodifica imágenes manualmente usando `image.load()`
* BasisU - Si tu juego tiene pocas texturas, compara el tamaño de build sin BasisU (eliminado mediante el manifiesto de la aplicación) y sin compresión de texturas frente a una build con BasisU y texturas comprimidas. Para juegos con texturas limitadas, puede ser más beneficioso reducir el tamaño del binario y omitir la compresión de texturas. Además, no usar el transcodificador puede reducir la cantidad de memoria necesaria para ejecutar tu juego.

## Optimizar el tamaño de los assets
Las mayores mejoras en optimización de tamaño de assets suelen conseguirse reduciendo el tamaño de sonidos y texturas.

### Optimizar sonidos
Defold admite estos formatos:
* .wav
* .ogg
* .opus

Defold admite archivos Wave PCM de 8 y 16 bits. Ogg Vorbis y Ogg Opus usan sus respectivos formatos comprimidos en lugar de exigir una profundidad de bits PCM. El decodificador Opus no se incluye de forma predeterminada; activa **Include Sound Decoder: Opus** en el [manifiesto de la aplicación](/manuals/app-manifest/#sound) antes de usar recursos `.opus`.
Nuestros decodificadores de sonido aumentarán o reducirán las frecuencias de muestreo de sonido según sea necesario para el dispositivo de sonido actual.

Los sonidos más cortos, como los efectos de sonido, suelen comprimirse más, mientras que los archivos de música tienen menos compresión.
Defold no realiza compresión, por lo que el desarrollador tendrá que encargarse de ello específicamente para cada formato de audio.

Puedes editar los sonidos en un software externo de edición de sonido (o desde la línea de comando usando, por ejemplo, [ffmpeg](https://ffmpeg.org)) para reducir la calidad o convertir entre formatos. Considera también convertir los sonidos de estéreo a mono para reducir aún más el tamaño del contenido.

### Optimizar texturas
Tienes varias opciones para optimizar las texturas usadas por tu juego, pero lo primero es revisar el tamaño de las imágenes que se agregan a un atlas o se usan como tilesource. Nunca debes usar imágenes de mayor tamaño que el necesario en tu juego. Importar imágenes grandes y escalarlas hacia abajo hasta el tamaño apropiado desperdicia memoria de textura y debe evitarse. Empieza ajustando el tamaño de las imágenes con software externo de edición de imágenes al tamaño real necesario en tu juego. Para elementos como imágenes de fondo, también puede estar bien usar una imagen pequeña y escalarla hacia arriba hasta el tamaño deseado. Una vez que tengas las imágenes en el tamaño correcto y agregadas a atlas o usadas en tilesources, también debes considerar el tamaño de los propios atlas. El tamaño máximo de atlas que se puede usar varía entre plataformas y hardware gráfico.

::: sidenote
[Esta publicación del foro](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) sugiere varios consejos sobre cómo redimensionar múltiples imágenes usando scripts o software de terceros.
:::

* Tamaño máximo de textura en HTML5 reportado al [proyecto Web3D Survey](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Tamaño máximo de textura en iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* El tamaño máximo de textura en Android varía mucho, pero en general todos los dispositivos razonablemente nuevos admiten al menos 4096x4096.

Si un atlas es demasiado grande, debes dividirlo en varios atlas más pequeños, usar atlas multipágina o escalar todo el atlas con un perfil de textura. El sistema de perfiles de textura de Defold te permite no solo escalar atlas completos, sino también aplicar algoritmos de compresión para reducir el tamaño del atlas en disco. Puedes [leer más sobre perfiles de textura en el manual](/manuals/texture-profiles/). Si no sabes qué usar, intenta empezar con estos ajustes como punto de partida para futuras personalizaciones:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Puedes leer más sobre cómo optimizar y administrar texturas en [esta publicación del foro](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Optimizar fuentes
El tamaño de tus fuentes será menor si especificas qué símbolos vas a usar y los defines en [Characters](/manuals/font/#properties), en lugar de usar la casilla All Chars.

### Excluir contenido para descargarlo bajo demanda
Otra forma de reducir el tamaño inicial de la aplicación es excluir partes del contenido del juego del bundle de la aplicación y descargarlas bajo demanda. Defold proporciona un sistema llamado Live Update para excluir contenido y descargarlo bajo demanda.

El contenido excluido puede ser cualquier cosa, desde niveles completos hasta personajes desbloqueables, skins, armas o vehículos. Si tu juego tiene mucho contenido, organiza el proceso de carga para que la colección bootstrap y la colección del primer nivel incluyan los recursos mínimos necesarios para ese nivel. Esto se logra usando proxies de colección o factories con la casilla "Exclude" activada. Divide los recursos según el progreso del jugador. Este enfoque asegura una carga eficiente de recursos y mantiene bajo el uso inicial de memoria. Aprende más en el [manual de Live Update](/manuals/live-update/).

## Optimizaciones de tamaño específicas de Android
Las builds de Android deben admitir arquitecturas de CPU de 32 y 64 bits. Cuando [creas un bundle para Android](/manuals/android), puedes especificar qué arquitecturas de CPU incluir:

![Signing Android bundle](images/android/sign_bundle.png)

Google Play admite [múltiples APK](https://developer.android.com/google/play/publishing/multiple-apks) por release de un juego, lo que significa que puedes reducir el tamaño de la aplicación generando dos APK, uno por arquitectura de CPU, y subiendo ambos a Google Play.

También puedes usar una combinación de [APK Expansion Files](https://developer.android.com/google/play/expansion-files) y [contenido de Live Update](/manuals/live-update) gracias a la [extensión APKX en el Asset Portal](https://defold.com/assets/apkx/).
