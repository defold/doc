---
title: Importación de modelos
brief: Este manual explica cómo importar modelos 3D usados por el componente Model.
---

# Importación de modelos 3D {#importing-3d-models}
Defold admite modelos, esqueletos y animaciones en el formato glTF 2.0 (GL Transmission Format). Usa archivos *.gltf* o *.glb* para los modelos 3D. glTF es un formato moderno diseñado para transferir y cargar datos 3D en motores de videojuegos y aplicaciones en tiempo real.

Puedes usar herramientas como Maya, 3ds Max, SketchUp y Blender para crear modelos 3D o convertirlos a glTF.

Blender es un programa potente y popular de modelado, animación y renderizado 3D. Funciona en Windows, macOS y Linux y está disponible de forma gratuita en [https://www.blender.org](https://www.blender.org).

![Modelo en Blender](images/model/blender_gltf.png)

## Importación a Defold {#importing-to-defold}
Para importar un modelo, arrastra y suelta el archivo *.gltf* o *.glb* en el panel *Assets* del editor Defold.

glTF puede almacenarse de dos maneras comunes:

* *.glb* es un único archivo binario. Contiene los datos del modelo y también puede contener imágenes de textura empaquetadas. Esto es cómodo cuando quieres mover o almacenar un modelo como un solo archivo.
* *.gltf* es un archivo JSON de texto. Normalmente referencia un archivo *.bin* separado para los datos de malla e imágenes de textura separadas como *.png*, *.jpg* o *.ktx2*. Al usar esta variante, agrega al proyecto todos los archivos referenciados y conserva sus rutas relativas.

Las imágenes integradas pueden usarse directamente desde un archivo glTF o GLB sin extraerlas como assets independientes. Las imágenes y los buffers externos deben seguir importándose junto con el modelo, conservando sus rutas relativas.

::: sidenote
Defold conserva las posiciones y transformaciones del archivo glTF importado y no vuelve a centrar automáticamente el modelo durante la importación. La vista previa del editor y el runtime usan las transformaciones importadas de forma coherente: las mallas con skinning o vinculadas a huesos conservan sus transformaciones locales relativas al esqueleto, mientras que las mallas rígidas mantienen su posición global resultante.

Un [componente Model](/manuals/model/#model-properties) puede seleccionar una única malla con nombre de la escena importada. Dejar vacío el campo *Mesh* usa toda la escena y conserva las transformaciones descritas anteriormente. Seleccionar una malla usa su geometría local sin las transformaciones de los nodos glTF, por lo que debes colocarla con la transformación del componente Model o del objeto de juego.

Si un modelo creado con una versión anterior de Defold cambia de posición u orientación después de volver a importarlo, corrige la transformación en Blender u otra herramienta de creación y vuelve a exportar el archivo *.gltf* o *.glb*.
:::

### Geometría comprimida {#compressed-geometry}

Las fuentes *.gltf* y *.glb* pueden contener geometría comprimida con Draco o Meshopt. Las extensiones de compresión glTF admitidas son:

| Compresión | Extensión glTF |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` y `KHR_meshopt_compression` |

Exporta u optimiza tu asset glTF 2.0 usando una de estas extensiones e impórtalo siguiendo los mismos pasos que para un modelo sin comprimir. Incluye los buffers y las texturas externos y conserva sus rutas relativas. Asigna el archivo importado a la propiedad *Scene* de un componente Model como de costumbre.

Defold decodifica la geometría comprimida durante la importación y la build. El modelo resultante usa la representación geométrica normal de Defold en runtime. Esta compatibilidad no activa la compresión Draco o Meshopt en el motor en ejecución, y un archivo fuente más pequeño no garantiza un bundle de juego más pequeño.

### Explorar la escena importada {#browsing-the-imported-scene}

Expande un archivo *.gltf* o *.glb* en el panel *Assets* para explorar sus mallas, materiales generados e imágenes integradas. Al abrir la escena se muestra una vista previa con sus materiales y texturas definidos. También puedes abrir una malla individual para previsualizarla.

Los recursos expuestos dentro del archivo son de solo lectura. Para crear un recurso Model editable para una malla, copia la malla y pégala en una carpeta del proyecto. El archivo *.model* resultante sigue referenciando el archivo glTF o GLB importado. Para cambiar la geometría fuente o las imágenes integradas, edita el asset en tu herramienta de creación y expórtalo de nuevo.

Los scripts del editor pueden enumerar estos recursos con `editor.resource_children(path)`. Consulta [Recorrer los recursos del proyecto](/manuals/editor-scripts/#traversing-project-resources) para ver un ejemplo que visita recursivamente los recursos de carpetas y archivos glTF/GLB.

### Texturas KTX2 {#ktx2-textures}

Las texturas de modelos pueden usar fuentes *.ktx2*, tanto como archivos externos como imágenes integradas en un archivo *.gltf* o *.glb*. Importa los archivos externos junto con el modelo. Las imágenes KTX2 integradas aparecen bajo la escena en el panel *Assets* y pueden asignarse directamente a los campos de textura de los materiales o mediante <kbd>Auto Fill</kbd>.

Los [perfiles de textura](/manuals/texture-profiles/#ktx2-source-textures) determinan si se conserva el formato fuente KTX2 o se convierte a los formatos de salida configurados. **Keep KTX2 Format** conserva el formato de codificación de origen cuando la compresión de texturas está activada, pero el procesamiento de imágenes puede requerir volver a codificarlo. Comprueba la compatibilidad del formato en tus dispositivos objetivo y considera la posible pérdida adicional de calidad al recomprimir una textura ya comprimida. Consulta [Formatos de entrada y vistas previas de KTX2](/manuals/importing-graphics/#ktx2-textures).

## Uso de un modelo {#using-a-model}
Una vez que hayas importado el modelo, úsalo en un [componente Model](/manuals/model):

1. Crea un archivo Model desde el panel *Assets* con <kbd>New... ▸ Model</kbd>, o agrega un componente Model directamente a un objeto de juego con <kbd>Add Component ▸ Model</kbd>.
2. Establece la propiedad *Scene* con el archivo *.gltf* o *.glb* importado.
3. Cuando aparezca el diálogo *Auto Fill Model Fields?*, elige <kbd>Auto Fill</kbd> para asignar los materiales generados de la escena y las texturas referenciadas. Esto reemplaza las asignaciones existentes de materiales y texturas. Elige <kbd>Keep Current</kbd> para conservar tus asignaciones; la nueva selección de escena se aplica de todos modos.
4. Deja *Mesh* vacío para usar toda la escena o selecciona una malla con nombre para usar solo su geometría local. Cambiar la selección de malla puede mostrar el mismo diálogo: seleccionar una malla ofrece sus materiales, mientras que borrar la selección ofrece todos los materiales de la escena. <kbd>Keep Current</kbd> conserva las asignaciones mientras aplica la nueva selección de malla.
5. Para un modelo animado, establece la propiedad *Skeleton* con el archivo *.gltf* o *.glb* que contiene el esqueleto. A menudo es el mismo archivo usado para *Scene* cuando la malla, el esqueleto y las animaciones se exportan juntos.
6. Crea un archivo *Animation Set* para las animaciones y asígnalo a la propiedad *Animations*. Establece *Default Animation* si quieres que una animación comience automáticamente.

El editor ofrece completar las asignaciones cuando la fuente glTF o GLB seleccionada expone materiales. Resuelve tanto las imágenes integradas como las referencias a imágenes externas. Los materiales generados usan los shaders glTF integrados; consulta el [manual de PBR](/manuals/physically-based-rendering/#built-in-pbr-materials) para conocer la iluminación y los efectos de material admitidos.

### Asignar materiales y texturas manualmente {#assigning-materials-and-textures-manually}

Si eliges <kbd>Keep Current</kbd> o necesitas sombreado personalizado, establece cada propiedad *Material* con un material adecuado. Los materiales `gltf` integrados proporcionan sombreado PBR; también están disponibles los materiales `model` integrados y tus propios materiales. Consulta el [manual de Model](/manuals/model/#material) para conocer las variantes estáticas, con skinning y con instancias, y sus requisitos.

Asigna cada textura al campo de textura correspondiente del material. Puedes usar una imagen integrada expuesta bajo el archivo glTF o GLB en el panel *Assets*, o un asset de imagen independiente del proyecto. Para materiales con varios samplers, asocia cada textura con el sampler previsto; el [manual de PBR enumera los nombres de los samplers glTF integrados](/manuals/physically-based-rendering/#built-in-pbr-materials).


## Exportación a glTF {#exporting-to-gltf}
El archivo *.gltf* o *.glb* exportado contiene todos los vértices, aristas y caras que componen el modelo, así como las _coordenadas UV_ (qué parte de la imagen de textura se asigna a cierta parte de la malla) si las has definido, los huesos del esqueleto y los datos de animación.

* Puedes encontrar una descripción detallada de las mallas poligonales en http://en.wikipedia.org/wiki/Polygon_mesh.

* Las coordenadas UV y el mapeado UV se describen en http://en.wikipedia.org/wiki/UV_mapping.

Defold impone algunas limitaciones a los datos de animación exportados:

* Actualmente Defold solo admite animaciones horneadas. Las animaciones deben tener matrices para cada hueso animado en cada keyframe, y no posición, rotación y escala como claves separadas.

* Las animaciones también se interpolan linealmente. Si usas una interpolación de curvas más avanzada, las animaciones deben prehornearse desde el exportador.

### Requisitos {#requirements}
Al exportar un modelo, ten en cuenta que la compatibilidad con glTF puede variar entre herramientas y motores. Usa glTF 2.0 y comprueba que el modelo tenga coordenadas UV correctas si utiliza texturas. Las imágenes pueden integrarse en el archivo glTF o GLB o almacenarse como archivos independientes referenciados por la escena. Incluye todas las imágenes y los buffers externos al importar el modelo a Defold.

Aunque nuestra intención es admitir completamente el formato glTF, todavía no hemos llegado a ese punto.
Si falta alguna funcionalidad, crea una solicitud de funcionalidad para ella en [nuestro repositorio](https://github.com/defold/defold/issues).

### Exportación de una textura {#exporting-a-texture}
Si quieres crear una imagen de textura manualmente, puedes exportar el layout UV de Blender como plantilla. Comienza seleccionando la malla y todos sus vértices:

![Seleccionar todo](images/model/blender_select_all_vertices.png)

Cuando todos los vértices estén seleccionados, desenvuelve la malla para obtener el layout UV:

![Desenvolver malla](images/model/blender_unwrap_mesh.png)

Luego puedes exportar el layout UV a una imagen que pueda usarse como textura:

![Exportar layout UV](images/model/blender_export_uv_layout.png)

![Resultado de exportar layout UV](images/model/blender_export_uv_layout_result.png)

### Exportación con Blender {#exporting-using-blender}
Exporta tu modelo desde Blender con <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Exportación con Blender](images/model/export_gltf.png)

Selecciona el objeto o los objetos antes de exportar y activa *Selected Objects* si solo quieres exportar la selección.

Elige una de las opciones de *Format*:

* *glTF Binary (.glb)* crea un archivo. Usa esta opción cuando quieras que el modelo sea fácil de mover o almacenar como un único asset.
* *glTF Separate (.gltf + .bin + textures)* crea archivos separados para la descripción del modelo, los datos binarios y las texturas. Usa esta opción cuando quieras editar imágenes de textura o asignarlas por separado en Defold.

Si el modelo contiene animaciones, activa la exportación de animaciones y asegúrate de que las animaciones estén horneadas. Si el modelo usa texturas, asegúrate de que la malla tenga un UV unwrap y de que las imágenes de textura se exporten en un formato que Defold pueda importar, como PNG o JPEG.

![Exportación con Blender](images/model/export_settings.png)
