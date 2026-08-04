---
title: Automatiser l'éditeur Defold avec HTTP
brief: Ce manuel explique comment les outils externes peuvent découvrir et utiliser l'API HTTP locale d'un projet ouvert dans l'éditeur Defold.
---

# Automatiser l'éditeur Defold {#automating-the-defold-editor}

L'éditeur Defold ouvre un serveur spécial pour les actions automatisées. L'API HTTP contrôle le projet ouvert. Utilisez-la pour les commandes de l'éditeur, les builds, les ressources du projet, les aperçus, les préférences, la sortie de la console, la recherche dans la documentation ou les intégrations de scripts de l'éditeur. Pour inspecter ou contrôler le jeu en cours d'exécution, utilisez plutôt le [service du moteur ou une API d'automatisation à l'exécution](/manuals/engine-service).

::: important
L'API HTTP de l'éditeur est expérimentale et peut changer entre les versions de Defold. Le document `/openapi.json` généré par l'éditeur en cours d'exécution constitue la source de vérité pour les opérations et les schémas disponibles.
:::

## Démarrer l'éditeur depuis un outil externe {#starting-the-editor-from-an-external-tool}

Un outil externe a besoin du fichier exécutable de l'éditeur et du chemin absolu vers le fichier `game.project` du projet.

Les versions de Defold installées peuvent être localisées grâce à `installations.json`, comme décrit dans le [manuel de l'éditeur](/manuals/editor/#editor-installation-metadata). Son champ `launcherPath` contient le fichier exécutable à démarrer. Transmettez le chemin de `game.project` comme premier argument positionnel pour ouvrir directement ce projet.

L'argument facultatif `--port` ou `-p` sélectionne le port du serveur de l'éditeur. Si vous l'omettez, Defold choisit un port disponible, ce qui est généralement préférable lorsque plusieurs projets peuvent être ouverts.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

L'éditeur est une application graphique pour ordinateur. Démarrez-la dans une session utilisateur interactive ayant accès à l'affichage. Utilisez [Bob](/manuals/bob) lorsqu'aucune session graphique n'est disponible, par exemple dans une CI headless, ou pour une automatisation limitée à la compilation et pour créer des bundles autonomes.

Après avoir démarré l'éditeur, attendez que le projet soit ouvert et que `.internal/editor.port` existe. Interrogez ensuite `/openapi.json` jusqu'à ce qu'il renvoie un document valide. Ne supposez pas que la création du processus signifie que le projet est prêt.

## Localiser le serveur de l'éditeur {#locating-the-editor-server}

L'éditeur démarre un serveur HTTP local tant qu'un projet est ouvert. Sélectionnez <kbd>Help ▸ Open Editor Server</kbd> pour ouvrir sa page d'accueil dans le navigateur par défaut :

![Page d'accueil du serveur local de l'éditeur](images/automation/editor_server.png)

Le port sélectionné est écrit dans le projet à l'emplacement suivant :

```text
.internal/editor.port
```

À partir de maintenant, les exemples et commandes de ce manuel utiliseront les variables shell suivantes :

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

Le fichier du port appartient à la session actuelle de l'éditeur. Relisez-le après avoir redémarré l'éditeur.

::: important
Le serveur de l'éditeur est une interface locale de contrôle fiable. Ne l'exposez pas au moyen d'une adresse publique, d'une redirection de port ou d'un tunnel non fiable.
:::

## Découvrir les opérations grâce à OpenAPI {#discovering-operations-through-openapi}

Les seules informations de démarrage propres à Defold dont un outil externe doit avoir besoin sont le port de l'éditeur et le document OpenAPI :

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

Le document OpenAPI 3.0.3 renvoyé décrit les opérations prises en charge par la version de l'éditeur en cours d'exécution, notamment les chemins, les méthodes, les paramètres, les noms de commandes, les formats des requêtes, les réponses, les codes d'état et les exigences d'authentification.

Listez les chemins documentés :

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Listez les commandes disponibles de l'éditeur :

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

Une intégration qui tient compte de la version doit vérifier chaque opération requise et configurer les requêtes à partir du schéma renvoyé. Nous déconseillons de maintenir une copie prétendument exhaustive des noms de points de terminaison ou de commandes, car elle peut devenir obsolète.

Les routes définies par le projet apparaissent également dans `/openapi.json` lorsque leurs scripts de l'éditeur fournissent une description d'opération OpenAPI.

## Exécuter des commandes de l'éditeur {#executing-editor-commands}

Les commandes de l'éditeur sont appelées au moyen de :

```text
POST /command/{command}
```

Par exemple, la commande actuelle `build` compile et exécute le projet :

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

Un build réussi renvoie un résultat structuré :

```json
{
  "success": true,
  "issues": []
}
```

Un échec du build renvoie l'état HTTP `422` avec des problèmes tels que :

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Les champs disponibles dépendent de l'erreur. Utilisez le chemin de la ressource et la plage du code source lorsqu'ils sont présents, mais gérez également les problèmes qui ne contiennent qu'un message.

Les commandes couramment utiles, lorsqu'elles sont répertoriées par l'éditeur en cours d'exécution, comprennent :

`build`
: Compiler et exécuter le projet.

`clean-build`
: Vider le cache de build, puis compiler et exécuter. Ne l'utilisez que lorsqu'un build ordinaire se comporte de manière incohérente ou semble ignorer des modifications.

`build-html5`
: Compiler le projet pour HTML5 et rendre la sortie disponible par l'intermédiaire du serveur de l'éditeur.

`fetch-libraries`
: Télécharger et recharger les dépendances du projet.

`hot-reload`
: Recharger les ressources modifiées dans un jeu en cours d'exécution.

`reload-extensions`
: Recharger les scripts de l'éditeur.

`debugger-start`, `debugger-stop` et les commandes pas à pas du débogueur
: Contrôler une session de débogage et le projet en cours d'exécution.

Les noms exacts et leur disponibilité dépendent de la version et de l'état actuel de l'éditeur ; découvrez-les dans `/openapi.json`.

Les commandes qui agissent sur les ressources du projet synchronisent les modifications de fichiers externes avant leur exécution.

### Réponses aux commandes et travail asynchrone {#command-responses-and-asynchronous-work}

L'opération de commande documente les codes de réponse dans le schéma OpenAPI actuel.

| État | Signification |
| --- | --- |
| `200` | La commande est terminée et a renvoyé un résultat |
| `202` | La commande a été acceptée et se poursuit de manière asynchrone |
| `403` | La commande n'est pas active dans l'état actuel de l'éditeur |
| `404` | La commande n'est pas disponible |
| `422` | Le build ou la validation a échoué |
| `500` | Une erreur interne de l'éditeur s'est produite |

Une réponse HTTP `202` ne prouve pas que le résultat demandé existe. Attendez la sortie, la ressource, le marqueur de console ou l'URL servie qui convient, et imposez un délai d'expiration.

### Build HTML5 {#building-html5}

Si le document OpenAPI actuel répertorie `build-html5`, appelez cette commande au moyen de l'opération correspondante :

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

La commande s'exécute de manière asynchrone et renvoie normalement l'état HTTP `202`. Une fois le build terminé, l'éditeur le sert à l'adresse suivante :

```text
http://127.0.0.1:<editor-port>/html5/
```

Attendez que l'URL soit disponible avant de lancer les tests dans le navigateur. Consultez [Tests HTML5 dans un navigateur](/manuals/automated-testing/#browser-tests-for-html5) pour plus de détails.

## Rechercher dans la documentation de l'API {#searching-api-documentation}

Lorsqu'elle est présente dans `/openapi.json`, l'opération `/ref` recherche dans la documentation de l'API incluse avec la version de l'éditeur en cours d'exécution. Elle fournit les noms et les signatures qui correspondent à cette version.

Par exemple, pour rechercher une fonction, utilisez :

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtrez par environnement et par langage :

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Les paramètres de recherche sont les suivants :

`environment`
: `editor`, `runtime` ou des valeurs séparées par des virgules.

`language`
: `Lua`, `C`, `C++` ou des valeurs séparées par des virgules.

`q`
: Une expression insensible à la casse. Les espaces représentent un ET, tandis que `|` représente un OU.

Il existe également des ressources de documentation condensées : l'[index de documentation pour LLM](https://defold.com/llms.txt) renvoie vers les manuels officiels, les espaces de noms de l'API et des exemples, tandis que la [documentation LLM complète](https://defold.com/llms-full.txt) fournit la documentation complète pour la recherche hors ligne et l'indexation locale.

Les agents IA doivent toutefois préférer des recherches ciblées au téléchargement d'une référence complète lorsqu'une seule API ou un seul message est nécessaire, afin d'économiser des tokens et de disposer d'un contexte mieux préparé et plus clair pour une tâche donnée.

## Lire la sortie de la console {#reading-console-output}

Lisez la console de l'éditeur au format JSON :

```sh
curl -sS "$BASE_URL/console" | jq
```

La réponse contient le texte de la console dans `lines` et les régions sémantiques dans `regions`, notamment les erreurs, les résultats d'évaluation et les références de ressources.

Pour suivre en continu la sortie de la console, utilisez :

```sh
curl -N "$BASE_URL/console/stream"
```

Le flux inclut les lignes déjà présentes dans la console, puis reste ouvert pour les nouvelles sorties. Fermez-le après avoir reçu un marqueur de fin ou une erreur, détecté l'arrêt du processus, ou atteint un délai d'expiration ou une limite de lignes.

Pour l'encadrement des résultats de test et la classification des échecs, consultez [Tests et vérification automatisés](/manuals/automated-testing/#structured-test-results).

## Générer des aperçus de scènes {#rendering-scene-previews}

L'éditeur Defold (depuis la version 1.13.1) peut générer une « capture d'écran » PNG d'une ressource de scène prise en charge au moyen de la commande `/preview/{path}` :

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Cette commande génère la collection principale du projet ouvert à partir du modèle Basic 3D, dans une vue initiale par défaut :

![Aperçu de la collection principale généré par l'éditeur](images/automation/main-preview.png)

Vous pouvez utiliser cette génération pour obtenir des aperçus des ressources qui emploient l'éditeur de scène visuel. Par exemple, il est possible de générer de la même manière l'aperçu d'un composant de modèle, ce qui permet de vérifier son apparence ou l'exactitude du shader :

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Aperçu du modèle de cube généré par l'éditeur](images/automation/cube-preview.png)

Le chemin situé après `/preview/` ne commence pas par une barre oblique. Les dimensions facultatives utilisent par défaut la taille d'affichage du projet et doivent être comprises entre `1` et `4096`.

| État | Signification |
| --- | --- |
| `200` | L'aperçu a été généré |
| `400` | Les dimensions ne sont pas valides |
| `404` | La ressource n'a pas été trouvée |
| `422` | La ressource n'est pas chargée ou ne prend pas en charge les aperçus de scène |

Les aperçus peuvent être très utiles pour l'analyse visuelle du projet : vérification de la disposition des niveaux et des interfaces graphiques, de la configuration des shaders et de l'éclairage, des régressions visuelles ou création de miniatures pour la documentation.

::: important
Un aperçu de l'éditeur n'est pas une capture d'écran du jeu en cours d'exécution. Il ne vérifie pas les objets créés dynamiquement, le post-traitement à l'exécution ni le rendu propre à une plateforme. Utilisez une [capture d'écran à l'exécution](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) lorsque ces éléments sont nécessaires.
:::

## Exécuter du code Lua dans l'éditeur {#executing-editor-lua}

L'opération authentifiée `POST /eval` exécute du code Lua dans l'environnement des extensions de l'éditeur. Le token bearer propre à la session est stocké dans :

```text
.internal/editor.token
```

Lisez le token et exécutez le code :

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

La sortie imprimée et les valeurs de retour sont renvoyées sous forme de texte. Les réponses courantes sont :

| État | Signification |
| --- | --- |
| `200` | Le code a été exécuté |
| `401` | Le token bearer est absent ou non valide |
| `422` | Le code Lua n'a pas pu être analysé ou exécuté |
| `503` | L'environnement des extensions de l'éditeur n'est pas prêt |

Un client peut réessayer après une erreur `503`, mais il doit limiter le nombre de tentatives. Corrigez le code avant de répéter une requête qui a renvoyé `422`.

Le code évalué peut utiliser l'[API de l'éditeur](https://defold.com/ref/editor-lua/) et l'environnement des scripts de l'éditeur. Il ne peut pas utiliser les API d'exécution du jeu telles que `go.*` pour manipuler un jeu en cours d'exécution. Utilisez un test d'exécution, le débogueur, un test dans un navigateur ou une [API d'automatisation à l'exécution](/manuals/engine-service/#automation-bridge-extension) pour le gameplay.

### Modifier les ressources et les fichiers {#modifying-resources-and-files}

De nombreuses ressources source de Defold utilisent des formats texte et peuvent être modifiées avec n'importe quel éditeur de texte. Pour modifier les ressources structurées d'un projet Defold, préférez les transactions de l'éditeur.

| Modification | Méthode recommandée |
| --- | --- |
| Lua, shader, JSON ou autre format texte connu | Modification directe du fichier |
| Texte non enregistré dans un onglet ouvert de l'éditeur | `editor.get()` et `editor.transact()` |
| Collection, objet de jeu, interface graphique, atlas ou autre ressource structurée | Transaction de l'éditeur |
| Contenu généré à plusieurs reprises | Générateur autonome |
| Opération de projet reproductible | Commande de l'éditeur ou point de terminaison HTTP personnalisé |
| Transformation réservée à la CI | Script autonome exécuté avant Bob |

Inspectez une ressource avant de la modifier :

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Vérifiez `editor.can_get()`, `editor.can_set()` et les autres fonctions `editor.can_*()` avant d'effectuer une transaction.

Utilisez `editor.execute()` dans le code Lua de l'éditeur pour exécuter un outil de formatage, un validateur ou un générateur :

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Lorsque la commande ne modifie pas les ressources du projet, définissez `reload_resources = false` pour éviter un rechargement inutile.

::: important
Ne modifiez pas les fichiers dans `.internal/` ni le contenu généré dans `build/`.
:::

## Préférences {#preferences}

Les préférences de l'éditeur peuvent être lues et écrites au moyen du chemin documenté dans OpenAPI, actuellement `/prefs/{path}`.

Vous pouvez par exemple lire la taille configurée de la police du code :

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Ou la définir, par exemple, sur 16 :

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

L'éditeur valide la valeur par rapport à son schéma de préférences. Un chemin ou une valeur non valide renvoie l'état HTTP `400`.

Les préférences sont des paramètres persistants propres à l'utilisateur ou au projet et à l'utilisateur ; il ne s'agit pas de la configuration du projet stockée dans `game.project`. Si l'automatisation doit modifier temporairement une préférence, enregistrez sa valeur précédente et restaurez-la ensuite.

## Routes définies par le projet {#project-defined-routes}

Les scripts de l'éditeur peuvent définir des routes supplémentaires avec [`get_http_server_routes()`](/manuals/editor-scripts/#http-server). Une table d'opération OpenAPI facultative expose une route dans le même document `/openapi.json` que les opérations intégrées.

Les routes définies par le projet peuvent assurer la génération de contenu, la validation, les rapports, les contrôles de localisation, l'analyse des ressources, les tests propres au projet ou une interface plus restreinte pour un IDE ou un contrôleur externe.

Une bonne route doit effectuer une opération au nom explicite, valider son entrée, renvoyer un résultat structuré, être idempotente lorsque cela est possible et limiter les travaux coûteux.

Les routes définies par le projet ne sont pas automatiquement protégées par le token `/eval`. Ajoutez une authentification propre au projet et des contrôles de sécurité lorsqu'une route effectue des opérations sensibles.

## Hooks de cycle de vie {#lifecycle-hooks}

Les hooks sont des fonctions qui peuvent être exécutées avant et après les builds, avant et après la création de bundles, et lorsqu'un processus de jeu démarre ou se termine. Un projet peut contenir un fichier `hooks.editor_script` à sa racine. Seul ce fichier de hooks racine reçoit ces événements, ce qui donne au projet un emplacement unique pour définir leur ordre.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Une erreur déclenchée dans `on_build_started()` arrête le build de l'éditeur. Les hooks de cycle de vie ne s'exécutent que dans l'éditeur ; placez la logique partagée de validation et de génération dans des scripts autonomes pouvant également être appelés depuis la CI.

## Sécurité et compatibilité {#security-and-compatibility}

Considérez l'ensemble du serveur de l'éditeur comme une interface locale fiable :

* N'exposez pas publiquement l'accès au port.
* Protégez `.internal/editor.token` ; il autorise `/eval` pour la session actuelle.
* N'accordez pas à des tiers un accès sans restriction à `/eval`.
* Conservez le token dans la couche d'intégration locale plutôt que dans les prompts, les rapports ou les journaux.
* N'oubliez pas que les routes définies par le projet n'héritent pas de l'authentification `/eval`.
* Utilisez un `/openapi.json` à jour.
* Utilisez des attentes limitées pour les commandes automatiques asynchrones et pour le démarrage de l'éditeur.

## Serveur du moteur {#engine-server}

Le serveur de l'éditeur appartient au processus de l'éditeur. Un jeu en cours d'exécution utilise un autre port et assume d'autres responsabilités, décrites dans le [manuel du service du moteur et de l'API HTTP d'exécution](/manuals/engine-service).
