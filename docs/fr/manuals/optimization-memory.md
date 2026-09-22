---
title: Optimiser l'utilisation de la mémoire d'un jeu Defold
brief: Ce manuel décrit comment optimiser l'utilisation de la mémoire d'un jeu Defold.
---

# Optimiser l'utilisation de la mémoire {#optimizing-memory-usage}

## Compression des textures {#texture-compression}
L'utilisation de la compression des textures réduit la taille des ressources dans l'archive de votre jeu, et les textures compressées peuvent également réduire la quantité de mémoire GPU nécessaire.

## Chargement dynamique {#dynamic-loading}
Dans la plupart des jeux, une partie au moins du contenu est utilisée peu fréquemment. Du point de vue de l'utilisation de la mémoire, il est peu judicieux de conserver ce contenu chargé en mémoire en permanence ; il vaut mieux le charger et le décharger selon les besoins. Il s'agit évidemment d'un compromis entre garder un contenu immédiatement accessible, au prix d'une consommation de mémoire à l'exécution, et le charger au prix d'un temps de chargement.

Defold propose plusieurs façons de charger du contenu dynamiquement :

* [Proxys de collection (collection proxy)](/manuals/collection-proxy/)
* [Factories de collection dynamiques](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Factories dynamiques](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Optimiser les compteurs de composants {#optimize-component-counters}
Defold alloue la mémoire des composants (components) et des ressources une seule fois, lors de la création d'une collection, afin de réduire la fragmentation de la mémoire. La quantité de mémoire allouée dépend de la configuration des différents compteurs de composants dans *game.project*. Utilisez le [profileur](/manuals/profiling/) pour mesurer précisément l'utilisation des composants et des ressources et configurez votre jeu avec des valeurs maximales plus proches du nombre réel de composants et de ressources. Cela réduira la quantité de mémoire utilisée par votre jeu (consultez les informations sur les [optimisations du nombre maximal de composants](/manuals/project-settings/#component-max-count-optimizations)).

## Optimiser le nombre de nœuds de l'interface graphique {#optimize-gui-node-count}
Optimisez le nombre de nœuds de l'interface graphique en limitant le nombre maximal de nœuds dans le fichier GUI au strict nécessaire. Le champ `Current Nodes` des [propriétés du composant GUI](https://defold.com/manuals/gui/#gui-properties) indique le nombre de nœuds utilisés par le composant GUI.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)


