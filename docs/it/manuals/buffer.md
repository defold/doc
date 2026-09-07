---
title: Manuale dei buffer
brief: Questo manuale spiega come funzionano le risorse Buffer in Defold.
---

# Buffer

La risorsa Buffer serve a descrivere uno o più flussi di valori, ad esempio posizioni o colori. Ogni flusso ha un nome, un tipo di dati, un numero di componenti e i dati stessi. Esempio:

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

L'esempio precedente descrive un flusso di posizioni in tre dimensioni, rappresentate da numeri in virgola mobile a 32 bit. I file Buffer sono in formato JSON e hanno estensione `.buffer`.

Le risorse Buffer vengono in genere create con strumenti esterni o script, ad esempio durante l'esportazione da strumenti di modellazione come Blender. 

Una risorsa Buffer può essere usata come input per un [componente Mesh](/manuals/mesh). Le risorse Buffer possono anche essere create durante l'esecuzione con `buffer.create()` e le [funzioni API correlate](/ref/stable/buffer/#buffer.create:element_count-declaration). 