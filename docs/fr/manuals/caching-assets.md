---
title: Mise en cache des ressources
brief: Ce manuel explique comment utiliser le cache des ressources pour accélérer les builds.
---

# Mise en cache des ressources {#caching-assets}

Les jeux créés avec Defold se compilent généralement en quelques secondes, mais le nombre de ressources augmente à mesure que le projet s'agrandit. La compilation des polices et la compression des textures peuvent prendre beaucoup de temps dans un projet volumineux, et le cache des ressources permet d'accélérer les builds en ne recompilant que les ressources modifiées et en utilisant les ressources déjà compilées du cache pour celles qui n'ont pas changé.

Defold utilise un cache à trois niveaux :

1. Cache du projet
2. Cache local
3. Cache distant


## Cache du projet {#project-cache}

Par défaut, Defold met en cache les ressources compilées dans le dossier `build/default` d'un projet Defold. Le cache du projet accélère les builds suivants, car seules les ressources modifiées doivent être recompilées, tandis que celles qui n'ont pas changé sont récupérées dans le cache du projet. Ce cache est toujours activé et est utilisé à la fois par l'éditeur et les outils en ligne de commande.

Vous pouvez supprimer le cache du projet manuellement en effaçant les fichiers dans `build/default` ou en exécutant la commande `clean` de l'[outil de build en ligne de commande Bob](/manuals/bob).


## Cache local {#local-cache}

Le cache local est un deuxième cache facultatif dans lequel les ressources compilées sont stockées à un emplacement externe au projet, sur la même machine ou sur un lecteur réseau. Grâce à cet emplacement externe, le contenu du cache est conservé après un nettoyage du cache du projet. Il peut aussi être partagé par plusieurs développeurs travaillant sur le même projet. Ce cache n'est actuellement disponible que pour les builds effectués avec les outils en ligne de commande. Il est activé à l'aide de l'option `resource-cache-local` :

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

L'accès aux ressources compilées du cache local repose sur une somme de contrôle calculée qui tient compte de la version du moteur Defold, des noms et du contenu des ressources sources, ainsi que des options de build du projet. Cela garantit que les ressources mises en cache sont uniques et que le cache peut être partagé entre plusieurs versions de Defold.

::: sidenote
Les fichiers du cache local sont conservés indéfiniment. Il appartient au développeur de supprimer manuellement les fichiers anciens ou inutilisés.
:::


## Cache distant {#remote-cache}

Le cache distant est un troisième cache facultatif dans lequel les ressources compilées sont stockées sur un serveur et accessibles par des requêtes HTTP. Ce cache n'est actuellement disponible que pour les builds effectués avec les outils en ligne de commande. Il est activé à l'aide de l'option `resource-cache-remote` :

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Comme pour le cache local, l'accès à toutes les ressources du cache distant repose sur une somme de contrôle calculée. L'accès aux ressources mises en cache utilise les méthodes de requête HTTP GET, PUT et HEAD. Defold ne fournit pas de serveur de cache distant. Il appartient à chaque développeur de le mettre en place. Vous pouvez consulter [un exemple de serveur Python simple ici](https://github.com/britzl/httpserver-python).
