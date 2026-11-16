## Bonjour le monde {#hello-world}

Voici une manière rapide de réaliser quelque chose dans Defold : suivez ces étapes, puis revenez lire la suite du manuel.

1. Sélectionnez un projet vide dans `Templates`, donnez-lui un nom dans `Title`, choisissez son emplacement et créez-le en cliquant sur `Create New Project`. Il s’ouvrira dans l’éditeur Defold.
![Bonjour le monde, étape 1](../manuals/images/unity/helloworld_1.png)
2. À gauche, dans le panneau `Assets`, ouvrez le dossier `main` et double-cliquez sur `main.collection` pour l’ouvrir.
3. À droite, dans le panneau `Outline`, faites un clic droit sur `Collection` et sélectionnez `Add Game Object`.
![Bonjour le monde, étape 2](../manuals/images/unity/helloworld_2.png)
4. Faites un clic droit sur l’objet de jeu (game object) `go` créé et sélectionnez `Add Component`, puis `Label`.
![Bonjour le monde, étape 3](../manuals/images/unity/helloworld_3.png)
5. En dessous, à gauche, dans le panneau `Properties`, saisissez du texte dans la propriété `Text`.
6. Dans la vue principale de la scène, au centre, faites glisser l’étiquette pour la placer aux environs de `(480,320,0)`, ou modifiez sa position dans `Properties` : `Position`.
![Bonjour le monde, étape 4](../manuals/images/unity/helloworld_4.png)
7. Après avoir modifié la position de l’étiquette, enregistrez le projet en cliquant sur `File` -> `Save All` ou avec le raccourci <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> sur Mac).
8. Générez un build de votre projet en cliquant sur `Project` -> `Build` ou avec le raccourci <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> sur Mac).
![Bonjour le monde, étape 5](../manuals/images/unity/helloworld_5.png)

Vous venez de générer le build de votre premier projet dans Defold et devriez voir votre texte dans la fenêtre. Les concepts d’objet de jeu et de composant (component) devraient vous être familiers. Les collections, la hiérarchie, les propriétés et la raison pour laquelle nous avons dû déplacer légèrement l’étiquette vers le haut et la droite sont expliquées ci-dessous.
