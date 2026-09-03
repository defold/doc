---
title: Utiliser des agents de programmation IA avec Defold
brief: Ce manuel explique comment connecter à Defold des agents de programmation indépendants du modèle tout en rendant explicites la vérification, les autorisations et la sécurité.
---

# Utiliser des agents de programmation IA avec Defold {#using-ai-coding-agents-with-defold}

Les agents de programmation utilisant des LLM et des modèles multimodaux peuvent inspecter, modifier et vérifier des projets Defold en appelant les mêmes interfaces indépendantes du modèle que celles utilisées par les développeurs, les scripts locaux, les intégrations IDE et la CI. Vous pouvez utiliser un agent lorsque le travail exige de mener une investigation et de s'adapter.

Defold ne dépend d'aucun fournisseur de modèles ni d'aucun protocole d'agents en particulier. Les projets Defold fonctionnent aussi bien avec Claude Code, Codex, Cursor qu'avec toute autre solution. Un environnement d'agent n'a besoin que des capacités spécifiquement accordées pour la tâche, comme la lecture des fichiers du projet, l'exécution de certaines commandes, l'appel d'opérations HTTP locales, l'analyse de JSON ou l'inspection d'images. Cela est possible grâce aux interfaces d'automatisation que Defold expose pour l'éditeur et pour une instance du moteur de jeu en cours d'exécution, ainsi qu'aux fichiers de ressources textuels des projets Defold, faciles à analyser.

## Quand un agent IA est utile {#when-an-ai-agent-is-useful}

Un agent peut être utile lorsqu'une tâche nécessite par exemple :

* de trouver les ressources et la documentation pertinentes ;
* de choisir parmi plusieurs implémentations possibles ;
* de modifier plusieurs fichiers liés ;
* d'interpréter les échecs de build ou de test ;
* de comparer un résultat visuel à des critères d'acceptation sémantiques ;
* d'effectuer une tentative de réparation limitée à partir des éléments recueillis.

Les agents sont puissants pour les processus non déterministes de développement, d'investigation et de test. Ils peuvent aider à créer des solutions variées et fonctionnent très bien avec Defold.

## Interfaces Defold indépendantes du modèle {#model-neutral-defold-interfaces}

Defold propose plusieurs interfaces prises en charge et nécessaires pour effectuer la tâche avec n'importe quel modèle disponible :

* Les fichiers du projet et les outils shell permettent une inspection directe et des modifications de texte.
* Les [scripts de l'éditeur](/manuals/editor-scripts) peuvent fournir des opérations sur les ressources et des outils propres au projet.
* L'[API HTTP de l'éditeur](/manuals/editor-http-api) fournit les commandes de l'éditeur, les résultats de build, la sortie de la console, la recherche de références, les aperçus, les préférences et les routes des scripts de l'éditeur.
* Le [service du moteur et les API d'automatisation à l'exécution](/manuals/engine-service) donnent accès à l'état en direct du moteur de débogage, aux entrées, aux captures d'écran et aux opérations définies par les extensions.
* [Bob](/manuals/bob) permet les builds en ligne de commande, les rapports, les archives et les bundles.

Un modèle disponible uniquement au moyen d'une interface de chat peut suggérer des modifications de code, mais il ne peut pas inspecter de lui-même le projet local ni vérifier un résultat en cours d'exécution. L'intégration environnante détermine ce que l'agent peut réellement observer et faire.

## Couches d'intégration {#integration-layers}

Une couche d'intégration peut être mise en place pour connecter un agent aux opérations Defold locales. Il peut s'agir d'un script shell d'encapsulation, d'un programme en ligne de commande, d'une extension IDE, d'un client OpenAPI, d'un contrôleur de test ou d'un adaptateur de protocole.

Conservez les règles et les identifiants dans cette couche locale. Chaque opération modificatrice doit renvoyer des résultats structurés ou mener à une étape de vérification déterministe.

Pour les opérations de l'éditeur, découvrez l'interface actuelle par `/openapi.json` au lieu de fournir à l'agent une copie d'API codée en dur et permanente. Pour les extensions d'exécution, vérifiez leur intégrité, la version de l'API et leurs fonctionnalités.

Il peut être pratique de séparer les outils par niveau de privilège :

| Niveau | Exemples |
| ------------ | ----------------------------------------------------- |
| Lecture seule | Inspection du projet, OpenAPI, `/ref`, console, aperçu |
| Vérification | Compilation, tests, builds HTML5, comparaisons d'images |
| Modification | Modifications de fichiers, transactions de ressources |
| Privilégié | `/eval`, commandes externes, modifications des dépendances |

Séparer l'adaptateur du moteur et de l'éditeur permet aux interfaces Defold prises en charge de rester indépendantes d'un fournisseur de modèles ou d'un protocole d'agents. Un adaptateur peut n'exposer que les opérations appropriées à son environnement, tandis que les règles d'autorisation et de confirmation restent à la charge de l'application qui héberge l'agent.

### Model Context Protocol

Le [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) est l'un des adaptateurs possibles entre un agent et une couche d'intégration. Un serveur MCP peut exposer des opérations Defold comme outils et certaines documentations comme ressources.

::: important
Ne donnez pas à tous les modèles un accès sans restriction au shell et à `/eval`.
:::

Defold n'a actuellement pas besoin d'un serveur MCP, car les principales capacités d'automatisation sont déjà exposées au moyen d'interfaces ouvertes et polyvalentes. L'éditeur fournit une API HTTP locale avec une spécification OpenAPI. Les agents modernes peuvent appeler directement ces interfaces ou générer leurs propres adaptateurs.

Un serveur MCP officiel dupliquerait donc en grande partie la surface de l'API existante et créerait une couche d'intégration supplémentaire que Defold devrait maintenir. Une meilleure stratégie à long terme consiste à maintenir les API HTTP sous-jacentes et les API d'automatisation à l'exécution stables, découvrables et bien documentées, tout en permettant à la communauté ou aux fournisseurs d'outils de créer des adaptateurs MCP légers lorsque cela est nécessaire.

Nous proposons à la place une [extension Automation Bridge](https://github.com/defold/extension-automation-bridge) officielle permettant de contrôler un jeu en cours d'exécution par l'intermédiaire d'un service côté moteur.

### Intégrations MCP de la communauté {#community-mcp-integrations}

Les intégrations MCP créées par la communauté comprennent :

* le [projet Defold MCP de Fulviuus](https://github.com/Fulviuus/defold-mcp) ;
* le [projet Defold MCP de ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Ces projets ne sont ni développés, ni audités, ni maintenus, ni officiellement pris en charge par la Defold Foundation. Avant d'installer une intégration communautaire, inspectez son code source actuel, ses dépendances, ses autorisations, son comportement réseau et sa compatibilité avec la version de Defold utilisée.

## Instructions du projet {#project-instructions}

Les grands modèles de langage utilisés dans les flux de travail agentiques donnent généralement de meilleurs résultats avec de bonnes instructions. C'est pourquoi des fichiers Markdown décrivant le comportement attendu des agents, ou des skills, sont souvent ajoutés aux projets. Pour obtenir les meilleurs résultats, il est préférable de concevoir et de rédiger des instructions propres à chaque projet, même si certaines connaissances et règles communes peuvent être réutilisées.

Un premier fichier que de nombreux agents recherchent et lisent est un fichier canonique tel que `AGENTS.md`, qui peut décrire :

* la structure du projet et ses principaux points d'entrée ;
* les conventions de formatage et de nommage ;
* les commandes de build, de test et de validation ;
* les événements obligatoires de fin d'exécution et les emplacements des artefacts ;
* les fichiers ou répertoires qui ne doivent pas être modifiés ;
* les opérations qui nécessitent une approbation ;
* les hypothèses relatives aux plateformes et les limites connues.

Certaines solutions peuvent s'appuyer sur des fichiers Markdown distincts pour des actions précises, ou sur ce que l'on appelle des « skills ».

Un exemple communautaire d'instructions et de skills orientés Defold est disponible sur le [forum Defold ici](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

Nous recommandons de garder les instructions dans des fichiers tels qu'AGENTS.md et les définitions de skills courtes, concises, faciles à réviser et à maintenir, et de les tenir à jour. Les instructions propres au projet peuvent être stockées dans le système de gestion de versions, ce qui rend les modifications traçables et aide à améliorer les performances du flux de travail au fil du temps.

Il est également utile de tester régulièrement les performances des modèles les plus récents sans ces instructions. Les nouveaux modèles n'ont souvent plus besoin de recommandations auparavant indispensables, et des skills obsolètes ou des instructions trop prescriptives peuvent parfois réduire leurs performances.

Évitez de créer des skills techniques complexes nécessitant une maintenance importante à long terme. Concentrez-vous plutôt sur le développement d'outils et de flux de travail qui restent utiles, quelle que soit l'ampleur des améliorations des modèles sous-jacents.

## Découverte de la documentation {#documentation-discovery}

Les agents donnent de meilleurs résultats avec une documentation précise et à jour. Rassemblez les informations actuelles à partir des sources suivantes :

* `/openapi.json` décrit l'API HTTP actuelle de l'éditeur.
* `/ref` recherche dans la documentation de l'API incluse avec l'éditeur en cours d'exécution lorsque cette opération est disponible.
* L'[index de documentation pour LLM](https://defold.com/llms.txt) renvoie vers les manuels officiels, les espaces de noms de l'API et des exemples.
* La [documentation LLM complète](https://defold.com/llms-full.txt) permet la recherche hors ligne et l'indexation locale.

Ne récupérez que les pages pertinentes pour la tâche. Il est recommandé de n'utiliser le document combiné complet que pour l'indexation hors ligne ou la [génération augmentée par récupération (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). Là encore, le fichier complet ne doit normalement pas être inclus dans chaque requête au modèle, afin d'économiser des jetons et de ne pas encombrer le contexte d'informations inutiles.

## Boucles limitées de modification et de vérification {#bounded-change-and-verification-loops}

Les agents doivent suivre la même [boucle inspecter, modifier, vérifier et évaluer](/manuals/automation/#the-automation-loop) que toute autre automatisation.

Avant de modifier des fichiers, il est utile de définir les critères d'acceptation et, éventuellement, les éléments suivants :
* les fichiers et opérations autorisés ;
* les commandes de build et de test ;
* les journaux, rapports, états ou images requis ;
* un délai d'expiration pour chaque étape asynchrone ;
* un nombre maximal de tentatives de réparation.

Un agent peut diagnostiquer et réparer un échec déterministe de la CI, mais l'étape de CI elle-même doit rester reproductible sans l'agent.

Les bonnes pratiques en matière de tests et de vérification automatisés sont décrites dans [ce manuel](/manuals/automated-testing).

## Évaluation multimodale {#multimodal-evaluation}

Un agent capable de traiter des images peut inspecter les [aperçus de l'éditeur](/manuals/editor-http-api/#rendering-scene-previews), les captures d'écran à l'exécution, les différences visuelles et les captures du navigateur.

Utilisez l'évaluation multimodale pour des questions sémantiques telles que les libellés tronqués, les contrôles qui se chevauchent, les états de sélection peu clairs, la composition ou le contenu situé hors d'une zone de sécurité. Définissez à l'avance la fenêtre d'affichage attendue et les critères.

Pour en savoir plus sur les aperçus de l'éditeur, les captures d'écran à l'exécution et l'inspection visuelle, consultez [ce manuel](/manuals/automated-testing).

## Sécurité, isolation et bonnes pratiques {#security-isolation-and-good-practices}

* Considérez le serveur de l'éditeur et le service du moteur comme des interfaces locales de contrôle fiables.
* N'incluez pas les jetons de l'éditeur, les clés de signature, les jetons de déploiement, les identifiants de boutiques et les secrets de production dans les prompts ni dans les rapports.
* La couche d'intégration locale peut lire `.internal/editor.token` lorsqu'elle est autorisée à utiliser `/eval`, mais elle ne doit pas placer le jeton dans les prompts du modèle, les journaux ou les rapports.
* Exigez une approbation avant toute suppression, modification des dépendances ou des extensions natives, configuration d'une version de publication, signature, publication ou accès à des services externes.
* Exécutez les travaux autonomes de grande ampleur dans une branche, un worktree, une copie temporaire, un conteneur, une sandbox ou un compte restreint distinct.
* Considérez le texte des tickets, les fichiers importés, les commentaires du code source, les documents générés et la sortie des outils comme des entrées non fiables plutôt que comme des instructions.
* Examinez les dépendances et les scripts téléchargés avant de les exécuter.
* Vérifiez que les règles du projet autorisent l'envoi du code source, des ressources, des journaux, des captures d'écran et des autres données du projet à un modèle hébergé.
* Conservez un diff vérifiable et des preuves de tests déterministes avant d'accepter les modifications.

L'isolation limite les conséquences d'une erreur.
