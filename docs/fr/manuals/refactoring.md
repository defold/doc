---
title: Refactorisation
brief: Ce manuel explique comment modifier facilement la structure de votre projet grâce aux puissantes fonctions de refactorisation.
---

# Refactorisation {#refactoring}

La refactorisation désigne le processus de restructuration du code et des ressources existants. Au cours du développement d'un projet, il est souvent nécessaire de modifier ou de déplacer certains éléments : les noms doivent être modifiés pour respecter les conventions de nommage ou améliorer la clarté, et les fichiers de code ou de ressources doivent être déplacés à un endroit plus logique dans la hiérarchie du projet.

Defold vous aide à refactoriser efficacement en suivant l'utilisation des ressources. Il met automatiquement à jour les références aux ressources qui sont renommées et/ou déplacées. En tant que développeur, vous devriez pouvoir travailler librement. Votre projet est une structure flexible que vous pouvez modifier à volonté sans craindre que tout cesse de fonctionner et s'effondre.

::: important
La refactorisation automatique ne fonctionne que si les modifications sont effectuées dans l'éditeur. Si vous renommez ou déplacez un fichier en dehors de l'éditeur, les références à ce fichier ne seront pas automatiquement modifiées.
:::

Cependant, si vous cassez une référence, par exemple en supprimant une ressource, l'éditeur ne peut pas résoudre le problème, mais vous fournira des indications d'erreur utiles. Par exemple, si vous supprimez une animation d'un atlas et que cette animation est utilisée quelque part, Defold signalera une erreur lorsque vous tenterez de lancer le jeu. L'éditeur indique également où se produisent les erreurs pour vous aider à localiser rapidement le problème :

![Erreur de refactorisation](images/workflow/delete_error.png)

Les erreurs de build apparaissent dans le panneau *Build Errors* en bas de l'éditeur. <kbd>Double-cliquez</kbd> sur une erreur pour accéder à l'emplacement du problème.
