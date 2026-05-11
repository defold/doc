---
title: Manual de buffer
brief: Este manual explica como os recursos de buffer funcionam no Defold.
---

# Buffer

O recurso Buffer é usado para descrever um ou mais fluxos de valores, por exemplo posições ou cores. Cada fluxo tem um nome, tipo de dado, contagem e os próprios dados. Exemplo:

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

O exemplo acima descreve um fluxo de posições em três dimensões, representadas como números de ponto flutuante de 32 bits. O formato de um arquivo Buffer é JSON, com a extensão de arquivo `.buffer`.

Recursos Buffer normalmente são criados usando ferramentas ou scripts externos, por exemplo ao exportar de ferramentas de modelagem como o Blender.

Um recurso Buffer pode ser usado como entrada para um [componente Mesh](/manuals/mesh). Recursos Buffer também podem ser criados em runtime usando `buffer.create()` e as [funções relacionadas da API](/ref/stable/buffer/#buffer.create:element_count-declaration).
