Les composants (components) servent à donner une apparence et/ou des fonctionnalités spécifiques aux objets de jeu (game objects). Les composants doivent être contenus dans des objets de jeu et sont affectés par la position, la rotation et l'échelle de l'objet de jeu qui les contient :

![Composants](../shared/images/components.png)

De nombreux composants possèdent des propriétés propres à leur type qui peuvent être manipulées, et des fonctions propres à chaque type de composant permettent d'interagir avec eux à l'exécution :

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

Les composants sont ajoutés soit directement dans un objet de jeu, soit sous forme de référence à un fichier de composant :

Faites un <kbd>clic droit</kbd> sur l'objet de jeu dans la vue *Outline* et sélectionnez <kbd>Add Component</kbd> (ajout direct) ou <kbd>Add Component File</kbd> (ajout par référence à un fichier).

Dans la plupart des cas, il est préférable de créer les composants directement dans l'objet de jeu, mais les types de composants suivants doivent être créés dans des fichiers de ressources distincts avant d'être ajoutés par référence à un objet de jeu :

* Script
* GUI
* Particle FX
* Tile Map
