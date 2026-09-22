## Optimisation du nombre maximal de composants {#component-max-count-optimizations}
Le fichier de paramètres *game.project* contient de nombreuses valeurs qui définissent le nombre maximal d'instances d'une ressource donnée pouvant exister simultanément, souvent comptabilisées par collection chargée (également appelée monde de jeu, ou game world). Le moteur Defold utilise ces valeurs maximales pour préallouer la mémoire correspondante, afin d'éviter les allocations dynamiques et la fragmentation de la mémoire pendant l'exécution du jeu.

Les structures de données de Defold utilisées pour représenter les composants (components) et les autres ressources sont optimisées pour occuper aussi peu de mémoire que possible, mais il faut tout de même choisir ces valeurs avec soin pour éviter d'allouer plus de mémoire que nécessaire.

Pour optimiser davantage l'utilisation de la mémoire, le processus de build de Defold analyse le contenu du jeu et remplace les nombres maximaux lorsqu'il est possible de déterminer avec certitude le nombre exact d'instances :

* Si une collection ne contient aucun composant factory, le nombre exact d'instances de chaque composant et d'objet de jeu (game object) est alloué, et les valeurs maximales sont ignorées.
* Si une collection contient un composant factory, les objets créés sont analysés et le nombre maximal est utilisé pour les composants pouvant être créés par les factory ainsi que pour les objets de jeu.
* Si une collection contient un composant factory ou collection factory avec l'option "Dynamic Prototype" activée, cette collection utilise les valeurs maximales.
