---
title: Manuel des ressources Buffer
brief: Ce manuel explique le fonctionnement des ressources Buffer dans Defold.
---

# Ressources Buffer {#buffer}

La ressource Buffer sert à décrire un ou plusieurs flux de valeurs, par exemple des positions ou des couleurs. Chaque flux possède un nom, un type de données, un nombre de composantes et les données elles-mêmes. Exemple :

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

L'exemple ci-dessus décrit un flux de positions en trois dimensions, représentées par des nombres à virgule flottante sur 32 bits. Un fichier Buffer est au format JSON et porte l'extension `.buffer`.

Les ressources Buffer sont généralement créées à l'aide d'outils ou de scripts externes, par exemple lors de l'exportation depuis des outils de modélisation tels que Blender. 

Une ressource Buffer peut servir d'entrée à un [composant (component) Mesh](/manuals/mesh). Les ressources Buffer peuvent également être créées à l'exécution avec `buffer.create()` et les [fonctions associées de l'API](/ref/stable/buffer/#buffer.create:element_count-declaration). 