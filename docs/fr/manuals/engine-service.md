---
title: Le service du moteur et les API HTTP d'exécution
brief: Ce manuel décrit le service HTTP de développement d'un moteur Defold de débogage en cours d'exécution et explique comment les extensions d'exécution ou les outils externes peuvent l'utiliser.
---

# Le service du moteur et les API HTTP d'exécution {#the-engine-service-and-runtime-http-apis}

L'exécution d'un projet en mode Debug crée un processus pour une instance d'exécution donnée du moteur avec votre jeu et un service spécial du moteur accessible pour l'infrastructure de développement et de profilage, la logique et les messages d'exécution, l'état du moteur et les extensions.

Le service du moteur est un service HTTP de développement appartenant à un moteur de débogage en cours d'exécution (`dmengine`).

Il est distinct du [serveur de l'éditeur](/manuals/editor-http-api), qui appartient à l'éditeur Defold et contrôle le projet ouvert.

Les deux services utilisent des ports différents. Un outil qui se connecte au port de l'éditeur ne peut pas y appeler les routes des extensions d'exécution, et inversement : un outil qui se connecte au service du moteur ne peut pas appeler les opérations de l'éditeur.

Le service du moteur fait partie de l'infrastructure de débogage, de développement et de profilage. Les instances Release du moteur ne créent pas ce service.

## Disponibilité et découverte du port {#availability-and-port-discovery}

Lorsque l'éditeur démarre un moteur de débogage, il demande un port de service attribué dynamiquement. Le moteur indique le port sélectionné dans la `Console` (et dans son journal s'il est exécuté depuis une CLI) :

![Informations sur le port du service du moteur dans un build de débogage Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Cette ligne apparaît dans la console de l'éditeur lorsque le jeu a été lancé depuis celui-ci. Un contrôleur local simple peut l'analyser, mais une intégration réutilisable doit laisser l'éditeur ou son wrapper suivre l'instance du moteur et le port enregistré. Cela évite de confondre un ancien port avec celui d'un processus nouvellement démarré ou réutilisé.

Le moteur annonce également les cibles de développement par la découverte de services sur les plateformes prises en charge. Ce mécanisme est principalement utilisé par les outils Defold et ne doit pas être remplacé par un port codé en dur de manière permanente.

Le serveur est accessible sur localhost (`127.0.0.1`) au port indiqué :

![Accès au serveur du moteur](images/automation/engine-server.png)

## Points de terminaison intégrés {#built-in-endpoints}

Le moteur de débogage actuel enregistre un petit ensemble de routes principales.

| Point de terminaison | Objectif |
| --- | --- |
| `GET /ping` | Vérifier que le service du moteur répond |
| `GET /info` | Lire la version du moteur, la plateforme, l'identifiant du build et les informations du service de journalisation |
| `GET /state` | Lire l'état de la connexion de développement utilisé par les outils Defold |
| `POST /post/<socket>/<message-type>` | Envoyer un message Defold encodé en Protobuf à un socket nommé du moteur |

Par exemple :

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

La route `/post` est utilisée par des opérations de développement telles que le rechargement à chaud, le redémarrage, le redimensionnement et le contrôle du processus. Son corps est un message Protobuf binaire du type indiqué dans la route ; il ne s'agit pas d'une API de messages JSON. La taille du message Protobuf sérialisé ne peut pas dépasser 1024 octets ; sinon, une réponse `400 Too large message` est renvoyée.

Ces routes font partie de l'infrastructure de développement. D'autres routes de profilage et d'inspection des ressources existent dans l'implémentation du moteur.

## Routes d'exécution définies par des extensions {#extension-defined-runtime-routes}

Dans les builds de débogage, le SDK des extensions natives peut donner accès au serveur web du moteur. Une extension peut enregistrer sur ce serveur un préfixe de route et exposer des opérations qui dépendent des données d'exécution.

C'est utile pour les outils de développement, car une extension peut partager le service existant du moteur au lieu d'ouvrir un autre serveur HTTP.

Une API d'automatisation à l'exécution définie par une extension doit :

* utiliser un préfixe de route distinct et versionné ;
* exposer les fonctionnalités prises en charge ;
* renvoyer des erreurs structurées ;
* gérer explicitement les fonctionnalités indisponibles de la plateforme ou du moteur ;
* limiter les opérations au développement et aux tests ;
* indiquer dans sa documentation si elle est omise des builds Release.

## Extension Automation Bridge {#automation-bridge-extension}

L'[Automation Bridge](https://github.com/defold/extension-automation-bridge) officielle de Defold est une extension native réservée au débogage et fondée sur le service du moteur. Elle enregistre une API d'automatisation à l'exécution versionnée sous :

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Son API d'exécution fournit notamment l'inspection de scènes et de nœuds, les entrées, des informations sur l'écran, les captures d'écran, l'enregistrement, des informations sur le cycle de vie et une synchronisation facultative définie par l'application. Voici quelques-unes de ses opérations :

| Opération | Action |
| --- | --- |
| `GET  /automation-bridge/v1/health` | rapport d'intégrité, fonctionnalités et compatibilité de l'API |
| `POST /automation-bridge/v1/input/click` | interactions avec les entrées à l'exécution |
| `GET  /automation-bridge/v1/screenshot` | captures d'écran à l'exécution |

Consultez la [documentation de l'API native](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) de l'extension et la [documentation des utilitaires Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) pour la version installée dans le projet.

Automation Bridge n'expose ni son API HTTP ni son module Lua dans les builds Release.

### Clients de l'éditeur et d'exécution {#editor-and-runtime-clients}

Les utilitaires Python d'Automation Bridge illustrent l'architecture à deux clients. La fonction `editor.open_project()` renvoie un client de projet de l'éditeur, tandis que `project.build_and_run()` renvoie un client distinct pour le moteur.

| Client | Objectif |
| --- | --- |
| Projet | API HTTP de l'éditeur, commandes, débogueur, console, préférences, référence, aperçus, build et découverte du port |
| Jeu — service du moteur | Scène, entrées, captures d'écran, état d'exécution et synchronisation |

La séparation entre `project` et `game` rend explicite la limite entre les processus. Les opérations de l'éditeur restent sur son serveur, tandis que les observations et les actions sur le jeu en direct restent sur le service du moteur.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limites et sécurité {#limitations-and-security}

Le service du moteur et les routes définies par les extensions sont des outils de développement et doivent être traités comme tels.

::: important
Le service du moteur ne publie actuellement pas de document OpenAPI. Les intégrations doivent se limiter aux comportements documentés ou à l'API versionnée d'une extension.
:::

Les scripts d'exécution, la physique, les entrées, les objets créés dynamiquement et le rendu propre à une plateforme nécessitent un moteur en cours d'exécution et doivent être vérifiés par des [tests d'exécution automatisés](/manuals/automated-testing).

* Ne publiez pas le service par l'intermédiaire d'un routeur, d'une interface publique ou d'un tunnel non fiable.
* Ne supposez pas que les routes du service du moteur nécessitent une authentification.
* Les routes d'exécution peuvent varier en fonction de la version de l'extension, de la plateforme, du backend graphique et des fonctionnalités du moteur.
* Utilisez une négociation de version ou de fonctionnalités pour les API à jour définies par les extensions.
