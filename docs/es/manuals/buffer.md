---
title: Manual de Buffer
brief: Este manual explica cómo funcionan los recursos Buffer en Defold.
---

# Buffer

El recurso Buffer se usa para describir uno o más flujos de valores, por ejemplo posiciones o colores. Cada flujo tiene un nombre, un tipo de dato, una cantidad y los datos en sí. Ejemplo:

```
[
  {
    "name": "position",
    "type": "float32",
    "count": 3,
    "data": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      1.0,
      ...
    ]
  }
]
```

El ejemplo anterior describe un flujo de posiciones en tres dimensiones, representadas como números de punto flotante de 32 bits. El formato de un archivo Buffer es JSON, con la extensión de archivo `.buffer`.

Los recursos Buffer suelen crearse usando herramientas o scripts externos, por ejemplo al exportar desde herramientas de modelado como Blender.

Un recurso Buffer puede usarse como entrada de un [componente Mesh](/manuals/mesh). Los recursos Buffer también pueden crearse en tiempo de ejecución usando `buffer.create()` y [funciones de API relacionadas](/ref/stable/buffer/#buffer.create:element_count-declaration).
