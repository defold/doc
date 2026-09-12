---
title: Arabellek kılavuzu
brief: Bu kılavuz, Defold'da arabellek kaynaklarının nasıl çalıştığını açıklar.
---

# Arabellek

Arabellek (Buffer) kaynağı, konum veya renk gibi değerlerden oluşan bir ya da daha fazla akışı (stream) tanımlamak için kullanılır. Her akışın bir adı, veri türü, değer sayısı ve verisi vardır. Örnek:

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

Yukarıdaki örnek, 32 bit kayan noktalı sayılarla temsil edilen üç boyutlu bir konum akışını tanımlar. Arabellek dosyasının biçimi JSON'dur ve dosya uzantısı `.buffer` şeklindedir.

Arabellek kaynakları genellikle harici araçlar veya betikler kullanılarak, örneğin Blender gibi modelleme araçlarından dışa aktarma sırasında oluşturulur. 

Bir arabellek kaynağı, bir [örgü bileşeninin (Mesh component)](/manuals/mesh) girdisi olarak kullanılabilir. Arabellek kaynakları `buffer.create()` ve [ilgili API işlevleri](/ref/stable/buffer/#buffer.create:element_count-declaration) kullanılarak çalışma sırasında da oluşturulabilir. 