---
title: Importar y editar assets
brief: Este manual explica cómo importar y editar assets.
---

# Importar y editar assets {#importing-and-editing-assets}

Un proyecto de juego normalmente consta de una gran cantidad de assets externos producidos en varios programas especializados para crear gráficos, modelos 3D, archivos de sonido, animaciones y otros recursos. Defold está diseñado para un flujo de trabajo donde trabajas en tus herramientas externas y luego importas los assets a Defold cuando están finalizados.


## Importar assets {#importing-assets}

Defold necesita que todos los assets usados en tu proyecto estén ubicados en algún lugar de la jerarquía del proyecto. Por lo tanto, necesitas importar todos los assets antes de poder usarlos. Para importar assets, simplemente arrastra los archivos desde el sistema de archivos de tu computadora y suéltalos en un lugar apropiado en el panel *Assets* del editor Defold.

![Importando archivos](images/graphics/import.png)

::: sidenote
Usa imágenes PNG o JPEG para atlas y tile sources. La compatibilidad con PNG incluye imágenes RGB, RGBA y de color indexado (paleta). También puedes importar [texturas fuente KTX2](/manuals/importing-graphics/#ktx2-textures) para usarlas como texturas de modelos.
:::


## Usar assets {#using-assets}

Cuando los assets se importan a Defold, pueden ser usados por los distintos tipos de componente soportados por Defold:

* Las imágenes se pueden usar para crear muchos tipos de componentes visuales usados con frecuencia en juegos 2D. Lee más sobre [cómo importar y usar gráficos 2D aquí](/manuals/importing-graphics).
* Los sonidos pueden ser usados por el [componente Sound](/manuals/sound) para reproducir sonidos.
* Las fuentes son usadas por el [componente Label](/manuals/label) y por los [nodos de texto](/manuals/gui-text) en una GUI.
* Los modelos glTF (*.gltf* y *.glb*) pueden usarse con el [componente Model](/manuals/model) para mostrar modelos 3D con animaciones. Expande estos archivos en el panel *Assets* para explorar sus mallas, materiales generados e imágenes integradas. Puedes usar las imágenes integradas directamente; incluye las imágenes y los buffers referenciados externamente como archivos separados del proyecto. También se admite [geometría comprimida con Draco y Meshopt](/manuals/importing-models/#compressed-geometry), que se decodifica durante la importación/build. Al seleccionar una escena o malla en un componente Model, el editor puede ofrecer completar sus asignaciones de materiales y texturas. Elige <kbd>Auto Fill</kbd> para aplicarlas y reemplazar las existentes, o <kbd>Keep Current</kbd> para conservar las tuyas. Lee más sobre [cómo importar y usar modelos 3D aquí](/manuals/importing-models).


## Editar assets externos {#editing-external-assets}

Defold no proporciona herramientas de edición para imágenes, archivos de sonido, modelos o animaciones. Estos assets deben crearse fuera de Defold con herramientas especializadas e importarse a Defold. Defold detecta automáticamente los cambios en cualquier asset entre los archivos de tu proyecto y actualiza la vista del editor en consecuencia.


## Editar assets de Defold {#editing-defold-assets}

El editor guarda todos los assets de Defold en archivos basados en texto que son aptos para merge. También son fáciles de crear y modificar con scripts simples. Consulta [este hilo del foro](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) para más información. Ten en cuenta, sin embargo, que no publicamos los detalles de nuestro formato de archivo porque cambian de vez en cuando. También puedes usar [Editor Scripts](/manuals/editor-scripts/) para conectarte a ciertos eventos del ciclo de vida en el editor y ejecutar scripts que generen o modifiquen assets.

Se debe tener especial cuidado al trabajar con archivos de assets de Defold mediante un editor de texto o una herramienta externa. Si introduces errores, estos pueden impedir que el archivo se abra en el editor Defold.

Algunas herramientas externas como [Tiled](/assets/tiled/) y [Tilesetter](https://www.tilesetter.org/beta) se pueden usar para generar assets de Defold automáticamente.
