---
title: Extensions natives - SDK Defold
brief: Ce manuel décrit comment utiliser le SDK Defold lors de la création d'extensions natives.
---

# Le SDK Defold {#the-defold-sdk}

Le SDK Defold contient les fonctionnalités nécessaires pour déclarer une extension native et communiquer avec la couche native de bas niveau de la plateforme sur laquelle l'application s'exécute, ainsi qu'avec la couche Lua de haut niveau dans laquelle la logique du jeu est créée.

## Utilisation {#usage}

Les extensions C++ peuvent inclure le fichier d'en-tête agrégé `dmsdk/sdk.h` :

```cpp
#include <dmsdk/sdk.h>
```

L'en-tête agrégé contient des déclarations C++ et ne peut pas être inclus dans un fichier source C. Les fichiers source C doivent inclure les en-têtes `.h` individuels compatibles avec C dont ils ont besoin, par exemple :

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Actuellement, seule une partie de dmSDK dispose d'une interface en C pur ; tous les sous-systèmes C++ n'ont pas d'équivalent en C. Les fonctions et les types disponibles sont documentés dans la [présentation de l'API C](/ref/overview_defoldc/) et la [présentation de l'API C++](/ref/overview_defoldcpp/). Les en-têtes du SDK Defold sont fournis dans une archive distincte `defoldsdk_headers.zip` pour chaque [version de Defold publiée sur GitHub](https://github.com/defold/defold/releases). Vous pouvez utiliser ces en-têtes pour la complétion de code dans l'éditeur de votre choix.
