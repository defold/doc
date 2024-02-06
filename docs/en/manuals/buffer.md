---
title: Buffer manual
brief: This manual explains how Buffer resources work in Defold.
---

# Buffer

The Buffer resource is used to describe one or more streams of values, for instance positions or colours. Each stream has a name, data type, count and the data itself. Example:

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

The above example describes a stream of positions in three dimensions, represented as 32-bit floating point numbers. The format of a Buffer file is JSON, with file extension `.buffer`.

Buffer resources are typically created using external tools or scripts, for instance when exporting from modeling tools such as Blender. 

A Buffer resource can be used as input to a [Mesh component](/manuals/mesh). Buffers resources can also be created at runtime using the `buffer.create()` and [related API functions](/ref/stable/buffer/#buffer.create:element_count-declaration). 