---
title: La conception de Defold
brief: La philosophie qui sous-tend la conception de Defold
---

# La conception de Defold {#the-design-of-defold}

Defold a été créé avec les objectifs suivants :

- Être une plateforme de production complète, professionnelle et clé en main pour les équipes de développement de jeux.
- Être simple et clair, en apportant des solutions explicites aux problèmes courants d'architecture et de flux de travail dans le développement de jeux.
- Être une plateforme de développement extrêmement rapide, idéale pour le développement itératif de jeux.
- Offrir de hautes performances à l'exécution.
- Être véritablement multiplateforme.

L'éditeur et le moteur sont conçus avec soin pour atteindre ces objectifs. Certains de nos choix de conception diffèrent de ce à quoi vous êtes peut-être habitué si vous avez déjà utilisé d'autres plateformes, par exemple :

- Nous exigeons une déclaration statique de l'arborescence des ressources et de tous les noms. Cela vous demande un certain effort initial, mais facilite considérablement le processus de développement à long terme.
- Nous encourageons l'échange de messages entre des entités simples et encapsulées.
- Il n'y a pas d'héritage orienté objet.
- Nos API sont asynchrones.
- Le pipeline de rendu est piloté par le code et entièrement personnalisable.
- Tous nos fichiers de ressources utilisent des formats de texte brut simples, dont la structure est optimisée pour les fusions Git ainsi que pour l'importation et le traitement avec des outils externes.
- Les ressources peuvent être modifiées et rechargées à chaud dans un jeu en cours d'exécution, ce qui permet des itérations et des expérimentations extrêmement rapides.
