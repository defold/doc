---
title: Profilage dans Defold
brief: Ce manuel explique les outils de profilage disponibles dans Defold.
---

# Profilage {#profiling}

Defold comprend des outils de profilage intégrés au moteur et à la chaîne de build. Ils aident à détecter les problèmes de performances, de mémoire et d'utilisation des ressources. Plusieurs outils peuvent exploiter les données de profilage recueillies à l'exécution :

* Le profileur de base et le profileur visuel intégré au jeu sont disponibles sur toutes les plateformes.
* Le [profileur Remotery](https://github.com/Celtoys/Remotery) et le profileur web interactif d'images sont disponibles sur les plateformes de bureau et mobiles.
* Les builds de débogage macOS utilisant Metal peuvent enregistrer des [traces GPU](#metal-gpu-trace-capture) pour les inspecter dans Xcode.
* Les builds HTML5 peuvent publier les zones de mesure de Defold dans l'API Web Performance du navigateur.

Le paramètre **Profiler** de l'[App Manifest](/manuals/app-manifest/#profiler) détermine si le code du profileur est lié au build. **Debug Only** est la valeur par défaut, **None** l'exclut et **Always** l'inclut dans les builds de débogage comme dans ceux de publication. Les paramètres `profiler` de *game.project* contrôlent le comportement à l'exécution, mais ne réintègrent pas dans un build le code du profileur qui en a été exclu. En particulier, **Track CPU** contrôle l'échantillonnage de l'utilisation du CPU ; ce paramètre est indépendant du choix effectué dans l'App Manifest.

## Le profileur visuel à l'exécution {#the-runtime-visual-profiler}

Les builds qui incluent la prise en charge du profileur disposent d'un profileur visuel qui affiche des informations en temps réel, en surimpression sur l'application en cours d'exécution :

```lua
function on_reload(self)
    -- Toggle the visual profiler on hot reload.
    profiler.enable_ui(true)
end
```

![Profileur visuel](images/profiling/visual_profiler.png)

Le profileur visuel fournit plusieurs fonctions permettant de modifier la manière dont il présente ses données :

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Consultez la [référence de l'API du profileur](/ref/profiler/) pour en savoir plus sur les fonctions du profileur.

## Le profileur web {#the-web-profiler}
Lorsqu'un build de bureau ou mobile incluant la prise en charge du profileur est en cours d'exécution, vous pouvez accéder aux profileurs interactifs d'images et de ressources dans un navigateur.

### Profileur d'images Remotery {#remotery-frame-profiler}
Le profileur d'images vous permet d'échantillonner votre jeu en cours d'exécution et d'analyser chaque image en détail. Pour accéder au profileur :

1. Démarrez un build de débogage de votre jeu sur votre appareil cible.
2. Sélectionnez le menu <kbd> Debug ▸ Open Web Profiler</kbd>.

Le profileur d'images est divisé en plusieurs sections qui offrent chacune une vue différente du jeu en cours d'exécution. Appuyez sur le bouton Pause dans le coin supérieur droit pour interrompre temporairement la mise à jour des vues du profileur.

![Profileur web](images/profiling/webprofiler_page.png)

::: sidenote
Lorsque vous utilisez plusieurs cibles simultanément, vous pouvez passer manuellement de l'une à l'autre en modifiant le champ Connection Address en haut de la page pour qu'il corresponde à l'URL du profileur Remotery affichée dans la console au démarrage de la cible :

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: La vue Sample Timeline affiche les données capturées pour chaque image dans le moteur, avec une chronologie horizontale par thread. Main est le thread principal, où s'exécutent toute la logique du jeu et la majeure partie du code du moteur. Remotery correspond au profileur lui-même et Sound au thread de mixage et de lecture audio. Vous pouvez zoomer et dézoomer (avec la molette de la souris) et sélectionner chaque image pour en afficher les détails dans la vue Frame Data.

  ![Chronologie des échantillons](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: La vue Frame Data est un tableau qui détaille toutes les données de l'image actuellement sélectionnée. Vous pouvez y voir combien de millisecondes sont consacrées à chaque zone de mesure du moteur.

  ![Données de l'image](images/profiling/webprofiler_frame_data.png)


Global Properties
: La vue Global Properties affiche un tableau de compteurs. Ils permettent par exemple de suivre facilement le nombre d'appels de dessin ou le nombre de composants (components) d'un certain type.

  ![Propriétés globales](images/profiling/webprofiler_global_properties.png)

::: sidenote
La valeur LuaMem correspond à la quantité de mémoire, en kilo-octets, utilisée par la machine virtuelle Lua, telle qu'elle est indiquée par le ramasse-miettes de Lua. Memory correspond à la quantité de mémoire, en kilo-octets, utilisée par le moteur.
:::

::: important
Le [paramètre Max Sample Count](/manuals/project-settings/#max-sample-count) limite le nombre d'échantillons de profilage enregistrés par thread et par image. Si le profileur signale que la limite a été dépassée, vérifiez d'abord si le code de profilage des extensions natives comporte une paire de début/fin de zone de mesure dont l'un des éléments manque. N'augmentez la limite que si une image contient légitimement plus de zones de mesure que la limite configurée.
:::

### Profileur de ressources {#resource-profiler}
Le profileur de ressources vous permet d'inspecter votre jeu en cours d'exécution et d'analyser en détail l'utilisation des ressources. Pour accéder au profileur :

1. Démarrez un build de débogage de votre jeu sur votre appareil cible.
2. Ouvrez l'[adresse du service du moteur](/manuals/engine-service/#availability-and-port-discovery) dans un navigateur : `http://<address>:<port>/`. Utilisez l'adresse et le port indiqués dans la console par le moteur en cours d'exécution.

Le profileur de ressources est divisé en deux sections : l'une affiche une vue hiérarchique des collections, des objets de jeu (game objects) et des composants actuellement instanciés dans votre jeu, et l'autre affiche toutes les ressources actuellement chargées.

![Profileur de ressources](images/profiling/webprofiler_resources_page.png)

Vue des collections
: La vue des collections affiche une liste hiérarchique de tous les objets de jeu et composants actuellement instanciés dans le jeu, ainsi que les collections dont ils proviennent. C'est un outil très utile pour examiner et comprendre ce qui est instancié dans votre jeu à un instant donné et d'où proviennent les objets.

Vue des ressources
: La vue des ressources affiche toutes les ressources actuellement chargées en mémoire, leur taille et le nombre de références à chacune d'elles. Elle est utile pour optimiser l'utilisation de la mémoire de votre application lorsque vous devez comprendre ce qui est chargé en mémoire à un instant donné.

#### Durées de chargement des ressources {#resource-loading-times}

Vous pouvez aussi inspecter le temps de chargement de chaque ressource. Activez [Resource → Profile](/manuals/project-settings/#profile) dans *game.project* avant de lancer le jeu. Dans la vue texte, ce paramètre est :

```ini
[resource]
profile = 1
```

Le paramètre est désactivé par défaut. Redémarrez le jeu après l'avoir activé pour mesurer les chargements de démarrage. Chaque chargement terminé ou échoué écrit une entrée de journal de niveau INFO avec le chemin de la ressource, la durée totale et les durées des étapes de préchargement, lecture, création, post-création, mise en file d'attente et attente. Les accès au cache ne produisent pas de nouveaux enregistrements de chargement.

Dans le profileur de ressources, cliquez sur **Capture**, puis sur **Show load times** pour afficher les colonnes de durée. **Capture** rafraîchit la vue des mesures conservées ; cela n'active pas le profilage et ne mesure pas rétroactivement les chargements précédents.

| Colonne | Signification |
| --- | --- |
| **Load (ms)** | Durée totale écoulée pour le chargement initial, y compris les dépendances, le travail après création, la mise en file d'attente et l'attente. |
| **Preload (ms)** | Temps passé à préparer la ressource dans son callback de préchargement. |
| **Read (ms)** | Temps passé à lire les données de la ressource. |
| **Create (ms)** | Temps passé à créer la ressource d'exécution dans son callback de création. |

Afficher les durées de chargement trie la table par durée totale, les ressources les plus lentes en premier. Cliquez sur l'en-tête d'une colonne de durée pour trier selon cette étape ; cliquez à nouveau pour inverser l'ordre. Les barres de la colonne **Load** montrent chaque total par rapport à la ressource visible la plus lente. Cliquez sur **Hide load times** pour masquer à nouveau les colonnes.

Les durées de chargement et de callback incluent les travaux des dépendances imbriquées. N'additionnez pas les totaux des ressources pour calculer le temps de démarrage, car un même travail peut apparaître dans les mesures de plusieurs ressources. Les colonnes **Preload**, **Read** et **Create** ne couvrent pas non plus toute la durée totale ; le journal fournit les étapes supplémentaires.

Un tiret cadratin (`—`) signifie qu'aucune mesure terminée n'est disponible, par exemple parce que le profilage était désactivé ou que le chargement initial n'est pas terminé. Une valeur nulle mesurée est affichée comme `0.000`. Les mesures décrivent le chargement initial : les accès au cache et les rechargements à chaud ne les modifient pas, et décharger une ressource supprime sa mesure conservée.

## Capture de traces GPU Metal {#metal-gpu-trace-capture}

Le [service HTTP du moteur](/manuals/engine-service/#metal-gpu-trace-endpoint) peut capturer les commandes GPU Metal dans un document *.gputrace* sur macOS. Ouvrez la trace terminée dans Xcode pour inspecter les images capturées. Cette fonctionnalité est intégrée au moteur de débogage.

### Lancer et vérifier la prise en charge {#launch-and-check-support}

Créez un [bundle Debug](/manuals/bundling/#release-vs-debug) macOS incluant le backend graphique Metal natif. Si vous utilisez un manifeste d'application, sélectionnez une option **Graphics (macOS)** qui inclut Metal ; consultez [Backends graphiques](/manuals/app-manifest/#graphics).

Lancez l'exécutable du bundle depuis un terminal avec `METAL_CAPTURE_ENABLED=1` et sélectionnez l'adaptateur Metal. Remplacez le chemin du bundle et le nom de l'exécutable dans cet exemple :

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

La variable d'environnement doit être définie au démarrage du moteur. La définir uniquement dans le terminal utilisé pour les requêtes HTTP n'active pas la capture dans un moteur déjà en cours d'exécution.

Dans un second terminal, utilisez le [port du service du moteur affiché dans le journal](/manuals/engine-service/#availability-and-port-discovery). Les exemples suivants utilisent `curl` et `jq` :

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

La route n'est enregistrée que sur macOS. Une entrée `null` dans le document OpenAPI signifie que ce moteur ne l'expose pas. Même si la route est présente, la prise en charge de la capture dépend de l'adaptateur graphique et de l'environnement de lancement. `GET /profiler/gputrace` renvoie HTTP 501 avec `error.code: "gputrace_unsupported"` lorsque la capture Metal est indisponible. Vérifiez que le moteur utilise Metal et qu'il a été lancé avec `METAL_CAPTURE_ENABLED=1` avant de continuer. Une demande prise en charge renvoie HTTP 200 avec l'état de capture.

### Capturer et inspecter les images {#capture-and-inspect-frames}

Choisissez un chemin de sortie absolu accessible en écriture et se terminant par `.gputrace`, avec un répertoire parent existant et aucune trace déjà présente à cet emplacement. Le chemin se trouve sur l'ordinateur qui exécute le moteur. Pour un moteur local, cet exemple crée un nouveau répertoire temporaire et demande une image :

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` est facultatif, vaut `1` par défaut et accepte les entiers de `1` à `10000`. La capture commence avant l'image rendue suivante et s'arrête après la soumission du nombre demandé d'images complètes. Laissez le jeu effectuer son rendu pendant l'attente. Une seule capture peut être en attente ou active ; une autre demande de démarrage renvoie HTTP 409 avec `error.code: "gputrace_active"`.

`POST` renvoie HTTP 200 avec `ok: true` et `data.state: "pending"` lorsque la capture est planifiée. La fin de la capture est signalée par les requêtes d'état suivantes. Répétez la requête d'état jusqu'à ce que `data.state` devienne `complete`, `canceled` ou `failed` :

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Signification |
| --- | --- |
| `idle` | Aucune capture n'a été planifiée. |
| `pending` | La capture attend le début du rendu. |
| `capturing` | La capture est active ; `data.frames_captured` indique les images terminées. |
| `complete` | La capture est terminée et la trace peut être ouverte. |
| `canceled` | Une capture en attente a été annulée avant son démarrage. |
| `failed` | La capture n'a pas pu démarrer ; consultez `data.error` pour l'erreur native. |

`GET` décrit la capture courante ou la plus récente. Vérifiez que `data.path` correspond au chemin demandé. Une capture échouée renvoie toujours HTTP 200 avec `ok: true` ; inspectez `data.state` et `data.error` pour déterminer le résultat. Pour un client automatisé, interrogez périodiquement l'état avec un délai entre les requêtes et un délai d'expiration.

Une fois l'état `complete`, ouvrez la trace dans Xcode sur le Mac du moteur :

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

Le point de terminaison HTTP renvoie l'état ; la trace est enregistrée à `data.path` sur l'hôte du moteur. Pour un moteur distant, récupérez le document terminé depuis cet hôte avant de l'ouvrir localement.

### Annuler ou arrêter une capture {#cancel-or-stop-a-capture}

Pour annuler une capture en attente ou terminer plus tôt une capture active :

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Une capture en attente passe à `canceled`. Pour une capture active, `data.stop_requested` devient `true`, et la capture se termine après la soumission de l'image actuellement rendue. Continuez à interroger `GET` jusqu'à un état terminal. `DELETE` conserve toute trace déjà écrite sur le disque. Si aucune capture n'est en attente ou active, la réponse est HTTP 409 avec `error.code: "gputrace_inactive"`.


## Chronologie des performances dans le navigateur en HTML5 {#html5-browser-performance-timeline}

HTML5 utilise l'API Web Performance à la place de Remotery pour sa chronologie dans le navigateur. Pour enregistrer les zones de mesure de Defold :

1. Assurez-vous que le mode de profilage sélectionné dans l'App Manifest inclut la prise en charge du profileur dans la variante de build que vous exécutez.
2. Activez **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) dans *game.project*.
3. Lancez le build HTML5 et ouvrez les outils de développement du navigateur.
4. Enregistrez une session dans le panneau **Performance** du navigateur et inspectez les zones de mesure de Defold dans la chronologie obtenue.

Cette chronologie du navigateur est distincte à la fois du profileur visuel intégré au jeu et du profileur web interactif Remotery.


## Rapports de build {#build-reports}
Lors de la création du bundle de votre jeu, une option vous permet de créer un rapport de build. Ce rapport est très utile pour connaître la taille de toutes les ressources qui font partie du bundle de votre jeu. Il suffit de cocher la case *Generate build report* lors de la création du bundle du jeu.

![Rapport de build](images/profiling/build_report.png)

L'outil de build produit un fichier nommé `report.html` à côté du bundle du jeu. Ouvrez ce fichier dans un navigateur web pour examiner le rapport :

![Rapport de build](images/profiling/build_report_html.png)

La section *Overview* fournit une vue d'ensemble de la répartition de la taille du projet par type de ressource.

*Resources* affiche une liste détaillée de ressources que vous pouvez trier par taille, taux de compression, chiffrement, type et nom de répertoire. Utilisez le champ « search » pour filtrer les entrées de ressources affichées.

La section *Structure* affiche les tailles en fonction de l'organisation des ressources dans l'arborescence des fichiers du projet. Les entrées sont colorées du vert (léger) au bleu (lourd) selon la taille relative du fichier et du contenu du répertoire.


## Outils externes {#external-tools}
En plus des outils intégrés, il existe un large choix d'outils de traçage et de profilage gratuits et de qualité. En voici une sélection :

ProFi (Lua)
: Nous ne fournissons pas de profileur Lua intégré, mais il existe des bibliothèques externes assez faciles à utiliser. Pour trouver où vos scripts passent du temps, insérez vous-même des mesures de temps dans votre code ou utilisez une bibliothèque de profilage Lua comme [ProFi](https://github.com/jgrahamc/ProFi).

  Notez que les profileurs écrits uniquement en Lua ajoutent un surcoût assez important à chaque hook qu'ils installent. Pour cette raison, il convient d'interpréter avec prudence les mesures de temps obtenues avec un tel outil. Les mesures fondées sur le comptage sont toutefois suffisamment précises.

Instruments (macOS et iOS)
: Cet outil d'analyse et de visualisation des performances fait partie de Xcode. Il vous permet de tracer et d'inspecter le comportement d'une ou plusieurs applications ou processus, d'examiner des fonctionnalités propres à l'appareil (comme le Wi-Fi et le Bluetooth) et bien plus encore.

  ![Instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Fait partie du paquet « Additional Tools for Xcode » que vous pouvez télécharger auprès d'Apple (sélectionnez <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> dans le menu de Xcode).

  Cet outil vous permet d'inspecter une application Defold en cours d'exécution et de voir comment elle utilise OpenGL. Vous pouvez tracer les appels de fonctions OpenGL, définir des points d'arrêt sur les fonctions OpenGL, examiner les ressources de l'application (textures, programmes, shaders, etc.), consulter le contenu des tampons et vérifier d'autres aspects de l'état d'OpenGL.

  ![Profileur OpenGL](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Cet ensemble d'outils de profilage capture en temps réel les données d'utilisation du CPU, de la mémoire et du réseau de votre jeu. Vous pouvez tracer les méthodes par échantillonnage pendant l'exécution du code, capturer des vidages du tas, afficher les allocations de mémoire et inspecter les détails des fichiers transmis sur le réseau. Pour utiliser cet outil, vous devez définir `android:debuggable="true"` dans `AndroidManifest.xml`.

  ![Profileur Android](images/profiling/android_profiler.png)

  Remarque : depuis Android Studio 4.1, il est également possible d'[exécuter les outils de profilage sans démarrer Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Cet ensemble d'outils vous permet d'inspecter, de modifier et de rejouer les appels d'une application à un pilote graphique. Pour l'utiliser, vous devez définir `android:debuggable="true"` dans `AndroidManifest.xml`.

  ![Débogueur d'API graphique](images/profiling/gapid.png)
