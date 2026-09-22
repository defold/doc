---
title: Filtrage des textures
brief: Ce manuel décrit les options disponibles pour le filtrage des textures lors du rendu graphique.
---

# Filtrage et échantillonnage des textures {#texture-filtering-and-sampling}

Le filtrage des textures détermine le résultat visuel lorsqu'un _texel_ (un pixel d'une texture) n'est pas parfaitement aligné avec un pixel de l'écran. C'est le cas lorsque vous déplacez de moins d'un pixel un élément graphique qui contient la texture. Les méthodes de filtrage suivantes sont disponibles :

Plus proche voisin
: Le texel le plus proche est choisi pour colorer le pixel de l'écran. Choisissez cette méthode d'échantillonnage si vous souhaitez une correspondance parfaite, pixel pour pixel, entre vos textures et ce que vous voyez à l'écran. Avec le filtrage au plus proche voisin, tout passe d'un pixel à l'autre lors des déplacements. Cela peut donner une impression de saccades si le sprite se déplace lentement.

Linéaire
: La valeur du texel est moyennée avec celles de ses voisins avant de colorer le pixel de l'écran. Cela produit un aspect fluide lors des mouvements lents et continus, car un sprite empiète sur les pixels avant de les colorer entièrement. Il est donc possible de déplacer un sprite de moins d'un pixel entier.

Le choix du filtrage à utiliser est enregistré dans le fichier des [paramètres du projet](/manuals/project-settings/#graphics). Deux paramètres sont disponibles :

default_texture_min_filter
: Le filtrage de réduction s'applique dès que le texel est plus petit que le pixel de l'écran.

default_texture_mag_filter
: Le filtrage d'agrandissement s'applique dès que le texel est plus grand que le pixel de l'écran.

Les deux paramètres acceptent les valeurs `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` ou `linear_mipmap_linear`. Par exemple :

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Si vous ne spécifiez rien, les deux sont définis sur `linear` par défaut.

Notez que le paramètre de *game.project* est utilisé par les échantillonneurs par défaut. Si vous spécifiez des échantillonneurs dans un matériau personnalisé, vous pouvez définir la méthode de filtrage pour chacun d'entre eux. Consultez le [manuel sur les matériaux](/manuals/material/) pour plus de détails.
