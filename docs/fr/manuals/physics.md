---
title: La physique dans Defold
brief: Defold intègre des moteurs physiques pour la 2D et la 3D. Ils vous permettent de simuler les interactions de la physique newtonienne entre différents types d'objets de collision.
---

# Physique {#physics}

Defold intègre [Box2D](https://box2d.org/) pour les simulations physiques en 2D et Bullet pour la physique en 3D. Le [paramètre Physics 2D de l'App Manifest](/manuals/app-manifest/#physics-2d) permet de sélectionner **Box2D Version 3**, **Box2D (Legacy Defold version)** ou **None**. L'implémentation historique est utilisée par défaut ; Box2D 3 doit être activé explicitement. Un changement d'implémentation peut modifier les résultats de la simulation et vous obliger à ajuster les [paramètres Box2D du projet](/manuals/project-settings/#box2d) propres à chaque version.

Le flux de travail des objets de collision, centré sur la notion de composant (component), et le module `physics` décrits dans ces manuels fonctionnent avec les deux implémentations de Box2D ; sélectionner **None** supprime la physique en 2D. Defold expose également les API de plus bas niveau [`b2d`](/ref/stable/b2d/), `b2d.body`, `b2d.fixture`, `b2d.shape`, `b2d.joint`, `b2d.chain` et `b2d.world` pour accéder directement aux corps, formes, articulations, chaînes et mondes en 2D. Certaines fonctions de bas niveau ne sont pas disponibles dans les deux implémentations de Box2D ; vérifiez la documentation d'API générée de chaque fonction en fonction de l'implémentation sélectionnée dans l'App Manifest.

Les principaux concepts des moteurs physiques utilisés dans Defold sont les suivants :

* **Objets de collision** - Un objet de collision est un composant qui vous permet de donner un comportement physique à un objet de jeu (game object). Un objet de collision possède des propriétés physiques telles que le poids, le frottement et la forme. [Découvrez comment créer un objet de collision](/manuals/physics-objects).
* **Formes de collision** - Un objet de collision peut utiliser plusieurs formes primitives ou une seule forme complexe pour définir son étendue dans l'espace. [Découvrez comment ajouter des formes à un objet de collision](/manuals/physics-shapes).
* **Groupes de collision** - Tous les objets de collision doivent appartenir à un groupe prédéfini et chaque objet de collision peut spécifier une liste d'autres groupes avec lesquels il peut entrer en collision. [Découvrez comment utiliser les groupes de collision](/manuals/physics-groups).
* **Messages de collision** - Lorsque deux objets de collision entrent en collision, le moteur physique envoie des messages aux objets de jeu auxquels appartiennent les composants. [En savoir plus sur les messages de collision](/manuals/physics-messages)

En plus des objets de collision eux-mêmes, vous pouvez définir des **contraintes** sur les objets de collision, plus couramment appelées **articulations**, pour relier deux objets de collision et limiter leur comportement dans la simulation physique, ou l'influencer d'autres manières en leur appliquant des forces. [En savoir plus sur les articulations](/manuals/physics-joints).

Vous pouvez également sonder le monde physique et en lire les informations le long d'un rayon rectiligne à l'aide d'un **lancer de rayon**. [En savoir plus sur les lancers de rayons](/manuals/physics-ray-casts).


## Unités utilisées par la simulation du moteur physique {#units-used-by-the-physics-engine-simulation}

Le moteur physique simule la physique newtonienne et est conçu pour bien fonctionner avec les unités mètres, kilogrammes et secondes (MKS). De plus, le moteur physique est réglé pour bien fonctionner avec des objets mobiles dont la taille est comprise entre 0.1 et 10 mètres (les objets statiques peuvent être plus grands) et, par défaut, il considère 1 unité (pixel) comme 1 mètre. Cette conversion entre pixels et mètres est pratique pour la simulation, mais elle n'est pas très utile du point de vue de la création d'un jeu. Avec les paramètres par défaut, une forme de collision de 200 pixels serait considérée comme mesurant 200 mètres, ce qui dépasse largement la plage recommandée, du moins pour un objet mobile.

En général, il est nécessaire de mettre la simulation physique à l'échelle pour qu'elle fonctionne bien avec la taille habituelle des objets d'un jeu. L'échelle de la simulation physique peut être modifiée dans *game.project* au moyen du [paramètre d'échelle de la physique](/manuals/project-settings/#physics). Si vous réglez cette valeur sur 0.02, par exemple, 200 pixels seront considérés comme 4 mètres. Notez que la gravité (également modifiable dans *game.project*) doit être augmentée pour tenir compte du changement d'échelle.


## Mises à jour de la physique {#physics-updates}

Il est recommandé de mettre à jour le moteur physique à intervalles réguliers pour assurer la stabilité de la simulation (plutôt qu'à des intervalles potentiellement irréguliers dépendant de la fréquence d'images). Vous pouvez utiliser une mise à jour à pas fixe pour la physique en cochant le [paramètre Use Fixed Timestep](/manuals/project-settings/#physics) de la section Physics du fichier *game.project*. La fréquence de mise à jour est contrôlée par le [paramètre Fixed Update Frequency](/manuals/project-settings/#engine) de la section Engine du fichier *game.project*. Lorsque vous utilisez un pas de temps fixe pour la physique, il est également recommandé d'utiliser la fonction de cycle de vie `fixed_update(self, dt)` pour interagir avec les objets de collision de votre jeu, par exemple pour leur appliquer des forces.


## Précautions et problèmes courants {#caveats-and-common-issues}

Proxys de collection
: Les proxys de collection (collection proxy) permettent de charger plusieurs collections de premier niveau, ou *mondes de jeu (game world)*, dans le moteur. Dans ce cas, il est important de savoir que chaque collection de premier niveau constitue un monde physique distinct. Les interactions physiques ([collisions, déclencheurs](/manuals/physics-messages) et [lancers de rayons](/manuals/physics-ray-casts)) ne se produisent qu'entre des objets appartenant au même monde. Ainsi, même si les objets de collision de deux mondes se superposent visuellement, aucune interaction physique ne peut avoir lieu entre eux.

Collisions non détectées
: Si les collisions ne sont pas traitées ou détectées correctement, consultez la section sur le [débogage de la physique dans le manuel de débogage](/manuals/debugging-game-logic/#debugging-problems-with-physics).
