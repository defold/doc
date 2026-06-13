---
title: Importar y editar assets
brief: Este manual explica cómo importar y editar assets.
---

# Importar y editar assets

Un proyecto de juego normalmente consta de una gran cantidad de assets externos producidos en varios programas especializados para crear gráficos, modelos 3D, archivos de sonido, animaciones y otros recursos. Defold está diseñado para un flujo de trabajo donde trabajas en tus herramientas externas y luego importas los assets a Defold cuando están finalizados.


## Importar assets

Defold necesita que todos los assets usados en tu proyecto estén ubicados en algún lugar de la jerarquía del proyecto. Por lo tanto, necesitas importar todos los assets antes de poder usarlos. Para importar assets, simplemente arrastra los archivos desde el sistema de archivos de tu computadora y suéltalos en un lugar apropiado en el panel *Assets* del editor Defold.

![Importando archivos](images/graphics/import.png)

::: sidenote
Defold soporta imágenes en los formatos PNG y JPEG. Las imágenes PNG deben estar en formato RGBA de 32 bits. Otros formatos de imagen deben convertirse antes de poder usarse.
:::


## Usar assets

Cuando los assets se importan a Defold, pueden ser usados por los distintos tipos de componente soportados por Defold:

* Las imágenes se pueden usar para crear muchos tipos de componentes visuales usados con frecuencia en juegos 2D. Lee más sobre [cómo importar y usar gráficos 2D aquí](/manuals/importing-graphics).
* Los sonidos pueden ser usados por el [componente Sound](/manuals/sound) para reproducir sonidos.
* Las fuentes son usadas por el [componente Label](/manuals/label) y por los [nodos de texto](/manuals/gui-text) en una GUI.
* Los modelos glTF (*.gltf* y *.glb*) pueden ser usados por el [componente Model](/manuals/model) para mostrar modelos 3D con animaciones. Importa como assets separados cualquier imagen de textura que use el modelo y asígnalas en las propiedades de textura del material del componente Model. Lee más sobre [cómo importar y usar modelos 3D aquí](/manuals/importing-models).


## Editar assets externos

Defold no proporciona herramientas de edición para imágenes, archivos de sonido, modelos o animaciones. Estos assets deben crearse fuera de Defold con herramientas especializadas e importarse a Defold. Defold detecta automáticamente los cambios en cualquier asset entre los archivos de tu proyecto y actualiza la vista del editor en consecuencia.


## Editar assets de Defold

El editor guarda todos los assets de Defold en archivos basados en texto que son aptos para merge. También son fáciles de crear y modificar con scripts simples. Consulta [este hilo del foro](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) para más información. Ten en cuenta, sin embargo, que no publicamos los detalles de nuestro formato de archivo porque cambian de vez en cuando. También puedes usar [Editor Scripts](/manuals/editor-scripts/) para conectarte a ciertos eventos del ciclo de vida en el editor y ejecutar scripts que generen o modifiquen assets.

Se debe tener especial cuidado al trabajar con archivos de assets de Defold mediante un editor de texto o una herramienta externa. Si introduces errores, estos pueden impedir que el archivo se abra en el editor Defold.

Algunas herramientas externas como [Tiled](/assets/tiled/) y [Tilesetter](https://www.tilesetter.org/beta) se pueden usar para generar assets de Defold automáticamente.
