---
title: Importación de modelos
brief: Este manual explica cómo importar modelos 3D usados por el componente Model.
---

# Importación de modelos 3D
Defold admite modelos, esqueletos y animaciones en el formato glTF 2.0 (GL Transmission Format). Usa archivos *.gltf* o *.glb* para los modelos 3D. glTF es un formato moderno diseñado para transferir y cargar datos 3D en motores de videojuegos y aplicaciones en tiempo real.

Puedes usar herramientas como Maya, 3ds Max, SketchUp y Blender para crear modelos 3D o convertirlos a glTF.

Blender es un programa potente y popular de modelado, animación y renderizado 3D. Funciona en Windows, macOS y Linux y está disponible de forma gratuita en [https://www.blender.org](https://www.blender.org).

![Modelo en Blender](images/model/blender_gltf.png)

## Importación a Defold
Para importar un modelo, arrastra y suelta el archivo *.gltf* o *.glb* en el panel *Assets* del editor Defold.

glTF puede almacenarse de dos maneras comunes:

* *.glb* es un único archivo binario. Contiene los datos del modelo y también puede contener imágenes de textura empaquetadas. Esto es cómodo cuando quieres mover o almacenar un modelo como un solo archivo.
* *.gltf* es un archivo JSON basado en texto. Normalmente hace referencia a un archivo *.bin* separado para los datos de la malla y a imágenes de textura separadas, como *.png* o *.jpg*. Cuando uses esta variante, agrega todos los archivos referenciados al proyecto y mantén intactas sus rutas relativas.

Si el modelo debe usar una textura en Defold, importa la imagen de textura como un asset separado. Incluso cuando el archivo glTF/GLB de origen contiene imágenes incrustadas, las texturas deben asignarse al componente Model mediante las propiedades de textura del material del componente.

![Assets de modelo importados](images/model/assets_gltf.png)

## Uso de un modelo
Una vez que hayas importado el modelo, úsalo en un [componente Model](/manuals/model):

1. Crea un archivo Model desde el panel *Assets* con <kbd>New... ▸ Model</kbd>, o agrega un componente Model directamente a un objeto de juego con <kbd>Add Component ▸ Model</kbd>.
2. Define la propiedad *Mesh* con el archivo *.gltf* o *.glb* importado que contiene la malla.
3. Para un modelo animado, define la propiedad *Skeleton* con el archivo *.gltf* o *.glb* que contiene el esqueleto. A menudo es el mismo archivo usado para *Mesh* cuando la malla, el esqueleto y las animaciones se exportan juntos.
4. Crea un archivo *Animation Set* para las animaciones y asígnalo a la propiedad *Animations*. Define *Default Animation* si quieres que una animación se inicie automáticamente.
5. Define la propiedad *Material* con un material adecuado para el modelo. Los archivos integrados *model.material*, *model_instances.material*, *model_skinned.material* y *model_skinned_instances.material* son puntos de partida útiles.
6. Define las propiedades de textura del material, como *Texture*, con los archivos de imagen de textura importados. Si el material usa varias texturas, asigna cada textura en el campo de textura de material correspondiente.


## Exportación a glTF
El archivo *.gltf* o *.glb* exportado contiene todos los vértices, aristas y caras que componen el modelo, así como las _coordenadas UV_ (qué parte de la imagen de textura se asigna a cierta parte de la malla) si las has definido, los huesos del esqueleto y los datos de animación.

* Puedes encontrar una descripción detallada de las mallas poligonales en http://en.wikipedia.org/wiki/Polygon_mesh.

* Las coordenadas UV y el mapeado UV se describen en http://en.wikipedia.org/wiki/UV_mapping.

Defold impone algunas limitaciones a los datos de animación exportados:

* Actualmente Defold solo admite animaciones horneadas. Las animaciones deben tener matrices para cada hueso animado en cada keyframe, y no posición, rotación y escala como claves separadas.

* Las animaciones también se interpolan linealmente. Si usas una interpolación de curvas más avanzada, las animaciones deben prehornearse desde el exportador.

### Requisitos
Cuando exportes un modelo, ten en cuenta que el soporte de glTF puede variar entre herramientas y motores. Usa glTF 2.0, asegúrate de que el modelo tenga coordenadas UV correctas si usa texturas e importa las imágenes de textura por separado cuando deban asignarse a un componente Model.

Aunque nuestra intención es admitir completamente el formato glTF, todavía no hemos llegado a ese punto.
Si falta alguna funcionalidad, crea una solicitud de funcionalidad para ella en [nuestro repositorio](https://github.com/defold/defold/issues).

### Exportación de una textura
Si aún no tienes una textura para tu modelo, puedes usar Blender para generarla. Debes hacerlo antes de eliminar materiales adicionales del modelo. Empieza seleccionando la malla y todos sus vértices:

![Seleccionar todo](images/model/blender_select_all_vertices.png)

Cuando todos los vértices estén seleccionados, desenvuelve la malla para obtener el layout UV:

![Desenvolver malla](images/model/blender_unwrap_mesh.png)

Luego puedes exportar el layout UV a una imagen que pueda usarse como textura:

![Exportar layout UV](images/model/blender_export_uv_layout.png)

![Resultado de exportar layout UV](images/model/blender_export_uv_layout_result.png)

### Exportación con Blender
Exporta tu modelo desde Blender con <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Exportación con Blender](images/model/export_gltf.png)

Selecciona el objeto o los objetos antes de exportar y activa *Selected Objects* si solo quieres exportar la selección.

Elige una de las opciones de *Format*:

* *glTF Binary (.glb)* crea un archivo. Usa esta opción cuando quieras que el modelo sea fácil de mover o almacenar como un único asset.
* *glTF Separate (.gltf + .bin + textures)* crea archivos separados para la descripción del modelo, los datos binarios y las texturas. Usa esta opción cuando quieras editar imágenes de textura o asignarlas por separado en Defold.

Si el modelo contiene animaciones, activa la exportación de animaciones y asegúrate de que las animaciones estén horneadas. Si el modelo usa texturas, asegúrate de que la malla tenga un UV unwrap y de que las imágenes de textura se exporten en un formato que Defold pueda importar, como PNG o JPEG.

![Exportación con Blender](images/model/export_settings.png)
