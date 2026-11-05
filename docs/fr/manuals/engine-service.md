---
title: Le service du moteur et les API HTTP d'exécution
brief: Ce manuel décrit le service HTTP de développement d'un moteur Defold de débogage en cours d'exécution et explique comment les extensions d'exécution ou les outils externes peuvent l'utiliser.
---

# Le service du moteur et les API HTTP d'exécution {#the-engine-service-and-runtime-http-apis}

L'exécution d'un projet en mode Debug crée un processus pour une instance d'exécution donnée du moteur avec votre jeu et un service spécial du moteur accessible pour l'infrastructure de développement et de profilage, la logique et les messages d'exécution, l'état du moteur et les extensions.

Le service du moteur est un service HTTP de développement appartenant à un moteur de débogage ou sans interface graphique en cours d'exécution (`dmengine` ou `dmengine_headless`).

Il est distinct du [serveur de l'éditeur](/manuals/editor-http-api), qui appartient à l'éditeur Defold et contrôle le projet ouvert.

Les deux services utilisent des ports différents. Un outil qui se connecte au port de l'éditeur ne peut pas y appeler les routes des extensions d'exécution, et inversement : un outil qui se connecte au service du moteur ne peut pas appeler les opérations de l'éditeur.

Le service du moteur fait partie de l'infrastructure de débogage, de développement et de profilage. Les instances Release du moteur ne créent pas ce service.

## Disponibilité et découverte du port {#availability-and-port-discovery}

Lorsque l'éditeur démarre un moteur de débogage, il demande un port de service attribué dynamiquement. Le moteur indique le port sélectionné dans la *Console* et dans son journal lorsqu'il est exécuté depuis une CLI :

![Informations sur le port du service du moteur dans un build de débogage Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Le moteur consigne également l'URL complète de découverte OpenAPI avec son adresse réelle et le port attribué :

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Ces lignes apparaissent dans la console de l'éditeur lorsque le jeu a été lancé depuis celui-ci. Un contrôleur local simple peut les analyser, mais une intégration réutilisable devrait laisser l'éditeur, ou l'outil qui l'encapsule, suivre l'instance du moteur et le port enregistré. Cela évite de confondre un ancien port avec celui d'un processus nouvellement démarré ou réutilisé.

Le moteur annonce également les cibles de développement au moyen de la découverte de services sur les plateformes prises en charge. Ce mécanisme est principalement utilisé par les outils Defold et ne devrait pas être remplacé par un port codé en dur de manière permanente.

Le serveur est accessible sur localhost (`127.0.0.1`) au port indiqué :

![Accès au serveur du moteur](images/automation/engine-server.png)

## Découvrir les opérations via OpenAPI {#discovering-operations-through-openapi}

`GET /openapi.json` renvoie un document OpenAPI 3.0.3 décrivant l'API HTTP d'exécution. Utilisez le port du service du moteur indiqué dans le journal. Pour un moteur local, remplacez `<port>` ci-dessous par ce port :

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

Le document décrit les chemins, méthodes, paramètres, corps de requête et réponses fournis par les gestionnaires actuellement enregistrés, y compris les extensions natives qui fournissent des métadonnées OpenAPI. Son objet `paths` change lorsque des gestionnaires sont ajoutés ou supprimés. Les routes du profileur et des extensions dépendent de la plateforme, de la configuration et des extensions enregistrées du moteur en cours d'exécution ; récupérez donc le document depuis l'instance que vous utilisez.

Les gestionnaires enregistrés sans métadonnées OpenAPI restent accessibles mais n'apparaissent pas dans le document. Une route documentée peut aussi signaler qu'une fonctionnalité est indisponible ; examinez ses descriptions de réponse et tout point de terminaison de capacités avant d'utiliser des opérations dépendant de la plateforme.

L'éditeur possède son propre [document OpenAPI](/manuals/editor-http-api/#discovering-operations-through-openapi) sur le port de l'éditeur. Utilisez le document du moteur pour les opérations d'exécution.


## Points de terminaison intégrés {#built-in-endpoints}

Le moteur de débogage actuel enregistre un petit ensemble de routes principales.

| Point de terminaison | Objectif |
| --- | --- |
| `GET /openapi.json` | Découvrir les opérations HTTP d’exécution actuellement enregistrées qui fournissent des métadonnées OpenAPI |
| `GET /ping` | Vérifier que le service du moteur répond |
| `GET /info` | Lire la version du moteur, la plateforme, l'identifiant du build et les informations du service de journalisation |
| `GET /state` | Lire l'état de la connexion de développement utilisée par les outils Defold |
| `POST /post/<socket>/<message-type>` | Envoyer un message Defold encodé en Protobuf à un socket nommé du moteur |

Par exemple :

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

La route `/post` est utilisée par des opérations de développement telles que le rechargement à chaud, le redémarrage, le redimensionnement et le contrôle du processus. Son corps est un message Protobuf binaire du type indiqué dans la route ; il ne s'agit pas d'une API de messages JSON. La taille du message Protobuf sérialisé ne peut pas dépasser 1024 octets ; sinon, une réponse `400 Too large message` est renvoyée.

Ces routes font partie de l'infrastructure de développement. D'autres routes de profilage et d'inspection des ressources existent dans l'implémentation du moteur.

## Points de terminaison d'enregistrement {#recording-endpoints}

Les moteurs de débogage pour ordinateur exposent également l'enregistrement MP4 natif via les routes suivantes. Elles sont omises des builds de publication, sans interface graphique, mobiles et web, ainsi que lorsque **Exclude Record** est activé dans le [manifeste d'application](/manuals/app-manifest/#exclude-record).

| Point de terminaison | Objectif |
| --- | --- |
| `GET /recording/capabilities` | Découvrir la prise en charge vidéo/audio, les exigences du backend et l'`instance_id` du service d'enregistrement |
| `GET /recording/status` | Lire l'opération courante, la progression asynchrone et les informations du fichier finalisé |
| `POST /recording/start` | Demander un enregistrement et recevoir son `operation_id` |
| `POST /recording/stop` | Demander l'arrêt et la finalisation de l'opération indiquée |
| `GET /recording/files/{id}` | Télécharger un MP4 finalisé |
| `DELETE /recording/files/{id}` | Supprimer un fichier terminé conservé par le service |

Découvrez ces routes via `/openapi.json`, puis consultez `/recording/capabilities` pour connaître la prise en charge sur la plateforme courante. Les opérations qui modifient l'enregistrement nécessitent l'en-tête `X-Recording-Instance`, et l'arrêt exige aussi l'`operation_id` accepté. Le démarrage et l'arrêt sont asynchrones ; attendez la finalisation avant de télécharger le fichier. Consultez le [manuel d'enregistrement](/manuals/recording/#recording-through-http) pour le flux de travail complet.

Le service HTTP partage l'enregistreur avec Lua. Les démarrages HTTP activent l'audio de l'application par défaut lorsqu'il est pris en charge ; les démarrages Lua enregistrent uniquement la vidéo par défaut. Seuls les enregistrements démarrés via HTTP possèdent un reçu `file` téléchargeable. Avant le téléchargement, attendez `pending: false`, `finalized: true` et `file.state: "complete"`, puis [vérifiez la taille et le SHA-256 du fichier](/manuals/recording/#download-and-release-the-file). Consultez le [partage de l'enregistreur](/manuals/recording/#sharing-the-recorder-with-http-clients) pour combiner des clients Lua et HTTP.

## Point de terminaison des traces GPU Metal {#metal-gpu-trace-endpoint}

Sur macOS, les moteurs de débogage exposent `/profiler/gputrace` pour capturer des traces GPU Metal. La route n'apparaît dans `/openapi.json` que sur macOS. La capture nécessite l'adaptateur Metal natif et `METAL_CAPTURE_ENABLED=1` dans l'environnement de lancement du moteur. Une demande renvoie HTTP 501 avec `error.code: "gputrace_unsupported"` si la capture est indisponible.

| Point de terminaison | Objectif |
| --- | --- |
| `POST /profiler/gputrace` | Planifier une capture vers un chemin absolu `.gputrace` accessible en écriture ; `frames` vaut `1` par défaut et peut être compris entre `1` et `10000`. |
| `GET /profiler/gputrace` | Lire l'état, le chemin et les nombres d'images de la capture courante ou la plus récente. |
| `DELETE /profiler/gputrace` | Annuler une capture en attente ou terminer une capture active après l'image actuellement rendue ; conserver la trace sur le disque. |

Les demandes acceptées renvoient HTTP 200 avec `ok: true` et un objet `data`. La capture progresse de manière asynchrone : interrogez `GET` jusqu'à ce que `data.state` soit `complete`, `canceled` ou `failed`. Les échecs de démarrage natif sont signalés dans `data.error`. La trace est écrite sur l'hôte du moteur. Consultez le [guide de capture de traces GPU Metal](/manuals/profiling/#metal-gpu-trace-capture) pour les commandes de lancement, la découverte de la prise en charge, les exemples de capture et l'ouverture du résultat dans Xcode.


## Routes d'exécution définies par des extensions {#extension-defined-runtime-routes}

Dans les builds de débogage, le SDK des extensions natives peut donner accès au serveur web du moteur. Une extension peut enregistrer sur ce serveur un préfixe de route et exposer des opérations qui dépendent des données d'exécution.

C'est utile pour les outils de développement, car une extension peut partager le service existant du moteur au lieu d'ouvrir un autre serveur HTTP.

Une API d'automatisation à l'exécution définie par une extension devrait :

* utiliser un préfixe de route distinct et versionné ;
* exposer les fonctionnalités prises en charge ;
* renvoyer des erreurs structurées ;
* gérer explicitement les fonctionnalités indisponibles de la plateforme ou du moteur ;
* limiter les opérations au développement et aux tests ;
* indiquer dans sa documentation si elle est omise des builds Release.

### Publier les opérations des extensions dans OpenAPI {#publishing-extension-operations-in-openapi}

Dans le callback d'initialisation de l'application d'une extension native, obtenez le serveur avec `dmEngine::GetWebServer(app_params)` et n'enregistrez des gestionnaires que si le handle renvoyé n'est pas nul. Consultez le [cycle de vie des extensions](/manuals/extensions/#extension-lifecycle) pour configurer le callback.

La surcharge à quatre arguments de `dmWebServer::AddHandler()` accepte un objet Paths OpenAPI 3.0.3 sous forme de chaîne JSON. Les clés de premier niveau de l'objet sont les chemins des routes. Chaque chemin doit commencer par le préfixe enregistré et ne pas être déjà documenté par un autre gestionnaire. Utilisez des schémas en ligne, ou des références à des chemins du document résultant.

Par exemple, cet utilitaire enregistre un callback et la description de son point de terminaison d'état :

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Passez un callback qui implémente `GET /example/v1/status` et renvoie la réponse `text/plain` documentée. Le callback reste responsable de la vérification des chemins et méthodes des requêtes ainsi que de la production des réponses. Vérifiez le résultat de l'enregistrement : des métadonnées non valides ou conflictuelles renvoient `dmWebServer::RESULT_ERROR_INVAL`.

Le serveur conserve le pointeur JSON sans copier la chaîne. Gardez son stockage inchangé et valide jusqu'à la suppression du gestionnaire avec `dmWebServer::RemoveHandler()` ou jusqu'à la destruction du serveur. Le tableau `static const char` de l'exemple satisfait cette exigence. La suppression du gestionnaire supprime également ses chemins des réponses `/openapi.json` suivantes.

La surcharge à trois arguments `dmWebServer::AddHandler(server, prefix, &params)` reste prise en charge. Elle équivaut à passer `0` comme quatrième argument : le gestionnaire est enregistré sans métadonnées OpenAPI et omis de la découverte.


## Extension Automation Bridge {#automation-bridge-extension}

L'extension officielle [Automation Bridge](https://github.com/defold/extension-automation-bridge) de Defold est une extension native réservée au débogage et fondée sur le service du moteur. Elle enregistre une API d'automatisation à l'exécution versionnée sous :

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Son API d'exécution fournit notamment l'inspection de scènes et de nœuds, les entrées, des informations sur l'écran, les captures d'écran, l'enregistrement, des informations sur le cycle de vie et une synchronisation facultative définie par l'application. Voici quelques-unes de ses opérations :

| Opération | Action |
| --- | --- |
| `GET  /automation-bridge/v1/health` | rapport d'état, fonctionnalités et compatibilité de l'API |
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

La séparation entre `project` et `game` rend explicite la limite entre les processus. Les opérations de l'éditeur restent sur son serveur, tandis que les observations et les actions sur le jeu en cours d'exécution restent sur le service du moteur.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limites et sécurité {#limitations-and-security}

Le service du moteur et les routes définies par les extensions sont des outils de développement et devraient être traités comme tels.

::: important
Utilisez le document `/openapi.json` du moteur en cours d'exécution pour la découverte dans Defold 1.14.1 et versions ultérieures. Les moteurs précédents ne fournissent pas ce point de terminaison. Pour les gestionnaires enregistrés sans métadonnées OpenAPI, consultez la documentation de l'API versionnée de l'extension.
:::

Les scripts d'exécution, la physique, les entrées, les objets créés dynamiquement et le rendu propre à une plateforme nécessitent un moteur en cours d'exécution et devraient être vérifiés par des [tests d'exécution automatisés](/manuals/automated-testing).

* Ne publiez pas le service par l'intermédiaire d'un routeur, d'une interface publique ou d'un tunnel non fiable.
* Ne supposez pas que les routes du service du moteur nécessitent une authentification.
* Les routes d'exécution peuvent varier en fonction de la version de l'extension, de la plateforme, du backend graphique et des fonctionnalités du moteur.
* Utilisez une négociation de version ou de fonctionnalités pour les API à jour définies par les extensions.
