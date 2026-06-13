---
title: Mallas 3D en Defold
brief: Este manual describe cómo crear mallas 3D en tiempo de ejecución en tu juego.
---

# Componente Mesh

Defold es, en esencia, un motor 3D. Incluso cuando trabajas solo con material 2D, todo el renderizado se realiza en 3D, pero se proyecta ortográficamente en la pantalla. Defold te permite usar contenido 3D completo al agregar y crear mallas 3D en tiempo de ejecución en tus colecciones. Puedes crear juegos estrictamente en 3D solo con assets 3D, o puedes mezclar contenido 3D y 2D como prefieras.

## Crear un componente Mesh

Los componentes Mesh se crean igual que cualquier otro componente de objeto de juego. Puedes hacerlo de dos formas:

- Crea un *archivo Mesh* con <kbd>click derecho</kbd> en una ubicación del explorador *Assets* y selecciona <kbd>New... ▸ Mesh</kbd>.
- Crea el componente incrustado directamente en un objeto de juego con <kbd>click derecho</kbd> en un objeto de juego en la vista *Outline* y selecciona <kbd>Add Component ▸ Mesh</kbd>.

![Mesh en objeto de juego](images/mesh/mesh.png)

Una vez creada la malla, debes especificar varias propiedades:

### Propiedades de Mesh

Aparte de las propiedades *Id*, *Position* y *Rotation*, existen las siguientes propiedades específicas del componente:

*Material*
: El material que se usará para renderizar la malla.

*Vertices*
: Un archivo de buffer que describe los datos de la malla por stream.

*Primitive Type*
: Lines, Triangles o Triangle Strip.

*Position Stream*
: Esta propiedad debe ser el nombre del stream *position*. El stream se proporciona automáticamente como entrada al vertex shader.

*Normal Stream*
: Esta propiedad debe ser el nombre del stream *normal*. El stream se proporciona automáticamente como entrada al vertex shader.

*tex0*
: Define esta propiedad con la textura que se usará para la malla.

## Manipulación en el editor

Con el componente Mesh en su lugar, puedes editar y manipular libremente el componente y/o el objeto de juego que lo encapsula con las herramientas habituales de *Scene Editor* para mover, rotar y escalar la malla a tu gusto.

## Manipulación en tiempo de ejecución

Puedes manipular mallas en tiempo de ejecución usando buffers de Defold. Ejemplo de creación de un cubo a partir de triangle strips:

```Lua

-- cubo
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- crea un buffer con un stream position
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- obtiene el stream position y escribe los vértices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- define el buffer con los vértices en la malla
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Consulta la [publicación de anuncio en el foro](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137) para obtener más información sobre cómo usar el componente Mesh, incluidos proyectos de ejemplo y fragmentos de código.

## Culling de frustum

Los componentes Mesh no se descartan automáticamente debido a su naturaleza dinámica y al hecho de que no es posible saber con certeza cómo están codificados los datos posicionales. Para descartar una malla, el cuadro delimitador alineado a los ejes de la malla debe establecerse como metadatos en el buffer usando 6 floats (AABB min/max):

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Constantes del material

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: El tinte de color de la malla (`vector4`). El `vector4` se usa para representar el tinte con x, y, z y w correspondientes al tinte rojo, verde, azul y alfa.

## Espacio local vs espacio del mundo de vértices
Si la configuración Vertex Space del material de la malla está establecida en Local Space, los datos se te proporcionarán tal cual en tu shader y tendrás que transformar los vértices/normales como de costumbre en la GPU.

Si la configuración Vertex Space del material de la malla está establecida en World Space, debes proporcionar un stream predeterminado `position` y `normal`, o puedes seleccionarlo en el menú desplegable al editar la malla. Esto es para que el motor pueda transformar los datos al espacio del mundo para batching con otros objetos.
