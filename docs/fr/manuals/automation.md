---
title: L'automatisation dans Defold
brief: Ce manuel présente les interfaces d'automatisation de Defold et explique comment choisir entre les flux de travail de l'éditeur, de l'exécution, de la ligne de commande, des tests et des agents.
---

# L'automatisation dans Defold {#automation-in-defold}

Ce manuel offre une vue d'ensemble et renvoie vers les manuels distincts consacrés à chaque sujet.

Defold prend en charge l'automatisation à plusieurs niveaux. Le choix d'une interface adaptée à la tâche est l'un des aspects les plus importants d'une automatisation efficace. Le tableau ci-dessous peut vous aider à choisir l'interface la plus simple pour une action donnée :

| Couche | Objectif |
| --- | --- |
| [Scripts de l'éditeur](/manuals/editor-scripts) | Commandes personnalisées, flux de travail ou intégrations de l'éditeur pour accélérer les tests et le développement, par exemple la création de niveaux ou de ressources |
| [Scripts d'interface utilisateur de l'éditeur](/manuals/editor-scripts-ui/) | Outils visuels, fenêtres contextuelles, configurateurs ou interfaces utilisateur personnalisés utilisant les scripts de l'éditeur |
| [API HTTP de l'éditeur](/manuals/editor-http-api) | Contrôle du projet de jeu ouvert dans l'éditeur Defold par des opérations OpenAPI, des ressources de projet, des builds, des commandes de l'éditeur, des aperçus, des préférences, la sortie de la console ou des scripts de l'éditeur pour des opérations personnalisées, des outils externes, des intégrations IDE et des contrôleurs de test |
| [CLI Bob](/manuals/bob) | Compilation d'un projet, création d'archives de données ou de bundles autonomes depuis la ligne de commande, rapports, CI |
| [Hooks de cycle de vie](/manuals/editor-http-api#lifecycle-hooks) | Validation ou génération avant et après les builds de l'éditeur ou la création de bundles |
| [Service HTTP du moteur](/manuals/engine-service) | Inspection du moteur de jeu Defold en cours d'exécution (`dmengine`), services de développement, profilage, messages d'exécution, API d'automatisation à l'exécution définies par des extensions, interrogation par des outils externes, envoi de commandes à un build de débogage en cours d'exécution |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | Extension Defold officielle qui fournit des points de terminaison supplémentaires pour automatiser le moteur à l'exécution |
| [Tests automatisés](/manuals/automated-testing) | Test de la logique du jeu, des messages, des composants, des entrées, de la physique et du comportement du moteur, inspection de scènes, retour visuel par exemple au moyen de l'[aperçu de l'éditeur](/manuals/editor-http-api/#rendering-scene-previews), entrées injectées, état en direct de l'application, [collections de test en cours d'exécution](/manuals/automated-testing/#tests-in-a-running-collection) |
| Scripts shell ou exécuteurs de tâches | Génération, formatage, validation et tâches reproductibles, opérations ordinaires sur les fichiers |
| Outils externes d'automatisation propres à une plateforme et aux navigateurs web | Outils de test pour ordinateur, tests d'interaction HTML5, captures d'écran, intégrations web |
| Agents de programmation IA et modèles multimodaux | Tâches pour lesquelles une approche déterministe est difficile ou impossible à mettre en œuvre, analyse sémantique de scènes, d'interfaces graphiques ou de captures d'écran à l'exécution |

La distinction la plus importante est celle entre l'éditeur Defold et un jeu en cours d'exécution. Il s'agit de processus distincts, avec des serveurs HTTP distincts.

## Automatisation déterministe ou agents IA {#deterministic-automation-or-ai-agents}

Préférez une solution déterministe lorsque la séquence des opérations est déjà connue, par exemple pour un validateur de niveau, un outil de formatage, une tâche de build ou un test de régression. Ces solutions doivent normalement avoir des entrées, des sorties, des délais d'expiration et des codes de sortie stables. Elles conviennent aux hooks et aux tests automatisés qui peuvent être exécutés de manière fiable dans un environnement CI. Une solution déterministe est également préférable pour la création procédurale de ressources de vos projets, par exemple un outil qui convertit des objets glTF en modèles avec un matériau donné, qui peuple un niveau d'arbres, etc. Ces procédures peuvent être facilement créées pour chaque projet avec les scripts de l'éditeur et leur interface utilisateur. Pour en savoir plus, consultez [le manuel](/manuals/editor-scripts-ui).

Un agent peut être utile lorsqu'une tâche nécessite une investigation ou une analyse multimodale (par exemple visuelle) : localiser les ressources pertinentes, choisir une implémentation, modifier plusieurs fichiers, interpréter des erreurs et progresser par itérations vers des critères d'acceptation définis. L'agent doit néanmoins appeler des interfaces déterministes et exploiter les mêmes éléments de preuve qu'un script local ou qu'un exécuteur CI. Consultez le manuel sur l'[utilisation d'agents de programmation IA avec Defold](/manuals/ai-agents).

## La boucle d'automatisation {#the-automation-loop}

Un processus d'automatisation fiable forme une boucle fermée :

1. Inspecter : lire les fichiers du projet, la description actuelle de l'interface et la documentation pertinente.
2. Modifier : utiliser des transactions de l'éditeur, des scripts de l'éditeur ou des outils de fichiers et de shell.
3. Vérifier : compiler, exécuter des tests ciblés et recueillir des journaux, des rapports, des états ou des images.
4. Évaluer : comparer les éléments recueillis aux critères d'acceptation, puis terminer ou recommencer.

![Boucle d'automatisation : inspecter, modifier, vérifier et évaluer](images/automation/automation_loop.png)

La vérification doit fournir des éléments de preuve provenant de l'environnement réel. Les éléments appropriés comprennent :

* le résultat positif d'un build ;
* une suite de tests explicitement terminée ;
* l'état attendu du jeu en cours d'exécution ;
* un bundle généré ou un rapport de build ;
* une comparaison d'images déterministe ;
* une capture d'écran satisfaisant des critères visuels définis.

Définissez le résultat attendu avant d'effectuer les modifications. Définissez également un délai d'expiration et un nombre maximal de tentatives de réparation. Un processus sans supervision ne doit pas se poursuivre indéfiniment s'il ne peut pas satisfaire aux critères d'acceptation.

## Étapes suivantes {#next-steps}

Vous trouverez davantage de détails sur des sujets précis concernant les flux de travail d'automatisation dans les manuels suivants :

* [Automatiser les tâches de l'éditeur Defold avec l'API HTTP](/manuals/editor-http-api)
* [Le service du moteur et l'API HTTP d'exécution](/manuals/engine-service)
* [Tests et vérification automatisés](/manuals/automated-testing)
* [Utiliser des agents de programmation IA avec Defold](/manuals/ai-agents)
