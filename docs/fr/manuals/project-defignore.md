---
title: Fichiers ignorés dans un projet Defold
brief: Ce manuel décrit comment ignorer des fichiers et des dossiers dans Defold.
---

# Ignorer des fichiers {#ignoring-files}

Vous pouvez configurer l'éditeur Defold et ses outils pour qu'ils ignorent des fichiers et des dossiers dans un projet. Cela peut être utile si le projet contient des fichiers dont les extensions entrent en conflit avec celles utilisées par Defold. C'est notamment le cas des fichiers du langage Go, dont l'extension `.go` est aussi celle que l'éditeur utilise pour les fichiers d'objets de jeu (game objects).

## Le fichier `.defignore` {#the-defignore-file}
Les fichiers et dossiers à exclure sont définis dans un fichier nommé `.defignore` à la racine du projet. Ce fichier doit énumérer les fichiers et dossiers à exclure, à raison d'un par ligne. Exemple :

```
/path/to/file.png
/otherpath
```

Cela exclura le fichier `/path/to/file.png` ainsi que tout le contenu du chemin `/otherpath`.

## Le fichier `.defunload` {#the-defunload-file}

Pour certains projets volumineux contenant plusieurs modules indépendants, vous pouvez souhaiter exclure certaines parties du chargement afin de réduire l'utilisation de la mémoire et les temps de chargement dans l'éditeur. Pour ce faire, vous pouvez énumérer les chemins à exclure du chargement dans un fichier `.defunload` situé dans le répertoire du projet.

En termes simples, le fichier `.defunload` vous permet de masquer des parties du projet dans l'éditeur sans que les références aux ressources masquées provoquent une erreur de build.

Les motifs du fichier `.defunload` suivent les mêmes règles que ceux du fichier `.defignore`. Les collections et les objets de jeu non chargés se comporteront comme s'ils étaient vides lorsqu'ils seront référencés par des ressources chargées. Les autres ressources correspondant aux motifs de `.defunload` resteront dans un état non chargé et ne pourront pas être consultées dans l'éditeur. Cependant, si une ressource chargée en dépend, les ressources non chargées et leurs dépendances seront chargées automatiquement.

Par exemple, si un sprite dépend d'images dans un atlas, nous devons charger l'atlas, sinon l'absence de l'image sera signalée comme une erreur. Dans ce cas, une notification avertira l'utilisateur de la situation et indiquera quelle ressource non chargée a été référencée et depuis quel endroit.

L'éditeur empêchera l'utilisateur d'ajouter des références à des ressources `.defunloaded` depuis des ressources chargées. Cette situation ne se produit donc que lorsque les ressources sont lues depuis le disque.

Contrairement au fichier `.defignore`, vous devez redémarrer l'éditeur après avoir modifié le fichier `.defunload` pour que les changements prennent effet.
