---
title: Développement avec Defold pour la plateforme HTML5
brief: Ce manuel décrit le processus de création d'un jeu HTML5, ainsi que les problèmes connus et les limitations.
---

# Développement HTML5 {#html5-development}

Defold permet de créer des builds de jeux pour la plateforme HTML5 à partir du menu habituel de création de bundles, comme pour les autres plateformes. De plus, le jeu obtenu est intégré à une page HTML classique dont vous pouvez personnaliser l'apparence grâce à un système de modèles simple.

Le fichier *game.project* contient les paramètres propres à HTML5 :

![Paramètres du projet](images/html5/html5_project_settings.png)

## Taille du tas {#heap-size}

La prise en charge de HTML5 dans Defold repose sur Emscripten (voir http://en.wikipedia.org/wiki/Emscripten). En résumé, il crée un espace mémoire isolé pour le tas dans lequel l'application s'exécute. Par défaut, le moteur alloue une quantité généreuse de mémoire (256 Mo). Cela devrait être largement suffisant pour un jeu classique. Dans le cadre de vos optimisations, vous pouvez choisir d'utiliser une valeur plus petite. Pour cela, suivez ces étapes :

1. Définissez *heap_size* à la valeur souhaitée. Elle doit être exprimée en mégaoctets.
2. Créez votre bundle HTML5 (voir ci-dessous)

## Tester un build HTML5 {#testing-html5-build}

Pour être testé, un build HTML5 nécessite un serveur HTTP. Defold en crée un pour vous si vous sélectionnez <kbd>Project ▸ Build HTML5</kbd>.

![Créer un build HTML5](images/html5/html5_build_launch.png)

Pour tester votre bundle, il vous suffit de l'envoyer sur votre serveur HTTP distant ou de créer un serveur local, par exemple avec Python dans le dossier du bundle.
Python 2 :

```sh
python -m SimpleHTTPServer
```

Python 3 :

```sh
python -m http.server
```

ou

```sh
python3 -m http.server
```

::: important
Vous ne pouvez pas tester le bundle HTML5 en ouvrant le fichier `index.html` dans un navigateur. Cela nécessite un serveur HTTP.
:::

::: important
Si l'erreur `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` apparaît dans la console, vous devez vous assurer que votre serveur utilise le type MIME `application/wasm` pour les fichiers `.wasm`.
:::

## Créer un bundle HTML5 {#creating-html5-bundle}

Créer du contenu HTML5 avec Defold est simple et suit la même procédure que pour toutes les autres plateformes prises en charge : sélectionnez <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd> dans le menu :

![Créer un bundle HTML5](images/html5/html5_bundle.png)

Les bundles HTML5 prennent en charge deux architectures WebAssembly :

* `wasm-web` - le moteur WebAssembly classique, sans threads.
* `wasm_pthread-web` - un moteur WebAssembly qui peut utiliser des threads.

Vous pouvez inclure l'une des architectures ou les deux. Lorsque les deux sont incluses, le chargeur sélectionne `wasm_pthread-web` si le navigateur et l'environnement d'hébergement le prennent en charge, et utilise `wasm-web` dans le cas contraire. Consultez le [manuel de Bob](/manuals/bob/#usage) pour connaître les noms canoniques des cibles.

::: important
Le moteur avec threads nécessite `SharedArrayBuffer` dans une page sécurisée et [isolée des autres origines](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated). Servez le bundle en HTTPS (ou sur localhost) et configurez le serveur avec des en-têtes d'isolation entre origines compatibles, généralement :

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Les ressources provenant d'autres origines et chargées par la page doivent également utiliser des en-têtes CORS ou Cross-Origin-Resource-Policy compatibles. Un bundle contenant uniquement `wasm_pthread-web` ne peut pas s'exécuter si ces exigences ne sont pas respectées ; incluez `wasm-web` comme solution de repli si le jeu peut être hébergé sur un site qui ne prend pas en charge l'isolation entre origines.
:::

Les bundles HTML5 de Defold nécessitent un navigateur moderne prenant en charge WebAssembly. Internet Explorer 11 n'est pas pris en charge.

Lorsque vous cliquez sur le bouton <kbd>Create bundle</kbd>, vous êtes invité à sélectionner un dossier dans lequel créer votre application. Une fois l'exportation terminée, vous y trouverez tous les fichiers nécessaires à l'exécution de l'application.

## Version du contexte WebGL {#webgl-context-version}

Sélectionnez le contexte graphique demandé avec [`graphics.webgl_version_hint`](/manuals/project-settings/#webgl-version-hint). Sa valeur par défaut est WebGL 2 ; demandez WebGL 1 pour tester ou cibler ce contexte dans les navigateurs prenant en charge les deux versions.

## Vérification des téléchargements {#download-verification}

Le chargeur HTML5 vérifie par défaut la taille des fichiers du moteur et de l'archive téléchargés. En cas d'échec d'une vérification, les téléchargements sont réessayés avant que le chargeur ne signale une erreur :

* Les erreurs réseau, les statuts HTTP d'échec et les écarts de taille lors du téléchargement du JavaScript ou du WebAssembly du moteur utilisent la limite de tentatives de `html5.retry_count`.
* La vérification des fichiers de l'archive possède sa propre limite de tentatives pour les écarts de taille ou de SHA-1. Chaque nouvelle vérification télécharge à nouveau les morceaux du fichier, avec les tentatives réseau habituelles disponibles pour chaque téléchargement.

Le paramètre `html5.retry_time` contrôle le délai entre les tentatives dans les deux cas.

Si votre serveur, proxy ou CDN réécrit volontairement les fichiers servis et modifie leur taille, désactivez la vérification de taille dans *game.project* :

```ini
[html5]
verify_downloaded_file_size = 0
```

Désactiver **Verify Downloaded File Size** laisse active toute vérification SHA-1 incluse dans le bundle. Consultez les [paramètres du projet HTML5](/manuals/project-settings/#verify-downloaded-file-size).

## Problèmes connus et limitations {#known-issues-and-limitations}

* Rechargement à chaud - Le rechargement à chaud ne fonctionne pas dans les builds HTML5. Les applications Defold doivent exécuter leur propre serveur web miniature pour recevoir les mises à jour de l'éditeur, ce qui n'est pas possible dans un build HTML5.
* Chrome
  * Lenteur des builds de débogage - Dans les builds de débogage pour HTML5, nous vérifions tous les appels graphiques WebGL afin de détecter les erreurs. Cette vérification est malheureusement très lente lors des tests dans Chrome. Vous pouvez la désactiver en définissant le champ *Engine Arguments* de *game.project* à `--verify-graphics-calls=false`.
* Prise en charge des manettes - [Consultez la documentation sur les manettes](/manuals/input-gamepads/#gamepads-in-html5) pour connaître les particularités de HTML5 et les mesures que vous pourriez devoir prendre.

## Personnaliser un bundle HTML5 {#customizing-html5-bundle}

Lorsque vous générez une version HTML5 de votre jeu, Defold fournit une page web par défaut. Elle référence des ressources de style et de script qui déterminent la présentation de votre jeu.

À chaque exportation de l'application, ce contenu est entièrement recréé. Si vous souhaitez personnaliser l'un de ces éléments, vous devez modifier les paramètres de votre projet. Pour cela, ouvrez *game.project* dans l'éditeur Defold et faites défiler jusqu'à la section *html5* :

![Section HTML5](images/html5/html5_section.png)

Vous trouverez plus d'informations sur chaque option dans le [manuel des paramètres du projet](/manuals/project-settings/#html5).

::: important
Vous ne pouvez pas modifier les fichiers du modèle HTML/CSS par défaut dans le dossier `builtins`. Pour appliquer vos modifications, copiez-collez le fichier nécessaire depuis `builtins` et sélectionnez ce fichier dans *game.project*.
:::

::: important
Le canevas ne doit avoir ni bordure ni marge intérieure. Sinon, les coordonnées des entrées de la souris seront incorrectes.
:::

Dans *game.project*, vous pouvez désactiver le bouton `Fullscreen` et le lien `Made with Defold`.
Defold fournit un thème sombre et un thème clair pour `index.html`. Le thème clair est défini par défaut, mais vous pouvez le changer en modifiant le fichier `Custom CSS`. Vous pouvez également choisir parmi quatre modes de mise à l'échelle prédéfinis dans le champ `Scale Mode`.

::: important
Les calculs de tous les modes de mise à l'échelle tiennent compte de la résolution actuelle de l'écran en DPI si vous activez l'option `High Dpi` dans *game.project* (section `Display`)
:::

### Modes Downscale Fit et Fit {#downscale-fit-and-fit}

Avec le mode `Fit`, la taille du canevas est modifiée pour afficher tout le canevas du jeu à l'écran en conservant ses proportions d'origine. La seule différence avec `Downscale Fit` est que la taille ne change que si la zone intérieure de la page web est plus petite que le canevas d'origine du jeu ; le canevas n'est pas agrandi lorsque la page web est plus grande que le canevas d'origine.

![Section HTML5](images/html5/html5_fit.png)

### Mode Stretch {#stretch}

Avec le mode `Stretch`, la taille du canevas est modifiée pour remplir entièrement la zone intérieure de la page web.

![Section HTML5](images/html5/html5_stretch.png)

### Mode No Scale {#no-scale}
Avec le mode `No Scale`, la taille du canevas est exactement celle que vous avez définie dans la section `[display]` du fichier *game.project*.

![Section HTML5](images/html5/html5_no_scale.png)

## Jetons {#tokens}

Nous utilisons le [langage de modèles Mustache](https://mustache.github.io/mustache.5.html) pour créer le fichier `index.html`. Lorsque vous créez un build ou un bundle, les fichiers HTML et CSS passent par un compilateur capable de remplacer certains jetons par des valeurs qui dépendent des paramètres de votre projet. Ces jetons sont toujours entourés d'accolades doubles ou triples (`{{TOKEN}}` ou `{{{TOKEN}}}`), selon que les séquences de caractères doivent être échappées ou non. Cette fonctionnalité peut être utile si vous modifiez fréquemment les paramètres de votre projet ou si vous prévoyez de réutiliser ce contenu dans d'autres projets.

::: sidenote
Vous trouverez plus d'informations sur le langage de modèles Mustache dans son [manuel](https://mustache.github.io/mustache.5.html).
:::

Toute valeur de *game.project* peut servir de jeton. Par exemple, si vous souhaitez utiliser la valeur `Width` de la section `Display` :

![Section Display](images/html5/html5_display.png)

Ouvrez *game.project* sous forme de texte et vérifiez `[section_name]` ainsi que le nom du champ que vous souhaitez utiliser. Vous pouvez ensuite l'utiliser comme jeton : `{{section_name.field}}` ou `{{{section_name.field}}}`.

![Section Display](images/html5/html5_game_project.png)

Par exemple, en JavaScript dans le modèle HTML :

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Nous proposons également les jetons personnalisés suivants :

DEFOLD_SPLASH_IMAGE
: Insère le nom du fichier de l'image de démarrage, ou `false` si `html5.splash_image` est vide dans *game.project*


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: Le nom du projet sans les symboles non autorisés

DEFOLD_ARCHIVE_LOCATION_PREFIX
: Le préfixe de chemin d'archive résolu utilisé par le chargeur, d'après `html5.archive_location_prefix`.

DEFOLD_ARCHIVE_LOCATION_SUFFIX
: Le suffixe résolu ajouté aux URL de l'archive, d'après `html5.archive_location_suffix`.

DEFOLD_HAS_ARCHIVE_ORIGIN
: `true` lorsque le préfixe de l'archive précise une origine HTTP ou HTTPS, y compris une URL relative au protocole comme `//cdn.example.com/archive`. Vaut `false` pour les préfixes d'archive relatifs. Disponible depuis Defold 1.13.2.

DEFOLD_ARCHIVE_ORIGIN
: L'origine de l'archive, incluant le schéma, l'hôte et le port facultatif, ou une chaîne vide si aucune origine n'est précisée. Un préfixe relatif au protocole produit une origine relative au protocole. Utilisée pour l'indication de préconnexion et disponible depuis Defold 1.13.2.

DEFOLD_HAS_WASM_ENGINE
: `true` si le bundle inclut un moteur WebAssembly, soit `wasm-web`, soit `wasm_pthread-web`.

DEFOLD_HAS_WASM_PTHREAD_ENGINE
: `true` si le bundle inclut `wasm_pthread-web`. Utilisez cette valeur pour éviter de précharger la mauvaise variante du moteur lorsque le chargeur choisit l'architecture à l'exécution.


DEFOLD_CUSTOM_CSS_INLINE
: C'est ici que nous insérons directement le contenu du fichier CSS indiqué dans les paramètres de votre *game.project*.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
Il est important que ce bloc intégré apparaisse avant le chargement du script principal de l'application. Comme il contient des balises HTML, cette macro doit être entourée d'accolades triples `{{{TOKEN}}}` pour empêcher l'échappement des séquences de caractères.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Ce jeton vaut `true` si `html5.scale_mode` vaut `Downscale Fit`.

DEFOLD_SCALE_MODE_IS_FIT
: Ce jeton vaut `true` si `html5.scale_mode` vaut `Fit`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Ce jeton vaut `true` si `html5.scale_mode` vaut `No Scale`.

DEFOLD_SCALE_MODE_IS_STRETCH
: Ce jeton vaut `true` si `html5.scale_mode` vaut `Stretch`.

DEFOLD_HEAP_SIZE
: La taille du tas indiquée dans *game.project* par `html5.heap_size`, convertie en octets.

DEFOLD_ENGINE_ARGUMENTS
: Les arguments du moteur indiqués dans *game.project* par `html5.engine_arguments`, séparés par le symbole `,`.

build-timestamp
: L'horodatage du build actuel, en secondes.


## Paramètres supplémentaires {#extra-parameters}

Si vous créez un modèle personnalisé, vous pouvez modifier les paramètres du chargeur du moteur en affectant des valeurs à l'objet global `CUSTOM_PARAMETERS`. Le modèle intégré fournit un bloc `<script id="engine-setup">` volontairement vide pour ces personnalisations.
::: important
Conservez le bloc `engine-setup` après le script qui charge `dmloader.js` et avant le bloc `engine-start` qui appelle `EngineLoader.load()`.
:::
Par exemple :

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` peut notamment contenir les champs suivants :

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## Opérations sur les fichiers en HTML5 {#file-operations-in-html5}

Les builds HTML5 prennent en charge les opérations sur les fichiers telles que `sys.save()`, `sys.load()` et `io.open()`, mais leur traitement interne diffère de celui des autres plateformes. Lorsque JavaScript s'exécute dans un navigateur, il n'existe pas de véritable notion de système de fichiers et l'accès aux fichiers locaux est bloqué pour des raisons de sécurité. Emscripten (et donc Defold) utilise à la place [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), une base de données intégrée au navigateur qui stocke les données de manière persistante, pour créer un système de fichiers virtuel dans le navigateur. La différence importante par rapport à l'accès au système de fichiers sur les autres plateformes est qu'un léger délai peut s'écouler entre l'écriture dans un fichier et l'enregistrement effectif de la modification dans la base de données. La console de développement du navigateur permet généralement d'inspecter le contenu d'IndexedDB.


## Transmettre des arguments à un jeu HTML5 {#passing-arguments-to-an-html5-game}

Il est parfois nécessaire de fournir des arguments supplémentaires à un jeu avant ou pendant son démarrage. Il peut s'agir, par exemple, d'un identifiant d'utilisateur, d'un jeton de session ou du niveau à charger au démarrage du jeu. Vous pouvez procéder de plusieurs façons, dont certaines sont décrites ici.

### Arguments du moteur {#engine-arguments}

Vous pouvez spécifier des arguments supplémentaires pour le moteur lors de sa configuration et de son chargement. Ces arguments supplémentaires peuvent être récupérés à l'exécution avec `sys.get_config_string()`. Affectez les arguments directement à `CUSTOM_PARAMETERS.engine_arguments` dans le bloc `engine-setup` de `index.html` :


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

L'affectation d'un nouveau tableau remplace tous les arguments du moteur configurés dans *game.project*. Pour conserver ces arguments et en ajouter un autre, utilisez plutôt `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")`.

Vous pouvez également ajouter `--config=example.foo1=bar1, --config=example.foo2=bar2` au champ *Engine Arguments* de la section HTML5 de *game.project*. Les valeurs séparées par des virgules sont ajoutées à `CUSTOM_PARAMETERS.engine_arguments` dans le fichier `dmloader.js` généré.

À l'exécution, vous récupérez les valeurs ainsi :

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Arguments de requête dans l'URL {#query-arguments-in-the-url}

Vous pouvez transmettre des arguments dans les paramètres de requête de l'URL de la page et les lire à l'exécution :

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Une fonction utilitaire complète pour récupérer tous les paramètres de requête sous forme de table Lua :

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Optimisations {#optimizations}
Les jeux HTML5 ont généralement des exigences strictes concernant la taille du téléchargement initial, le temps de démarrage et l'utilisation de la mémoire, afin de garantir un chargement rapide et un bon fonctionnement sur les appareils peu puissants et les connexions Internet lentes. Pour optimiser un jeu HTML5, il est recommandé de vous concentrer sur les points suivants :

* [Utilisation de la mémoire](/manuals/optimization-memory)
* [Taille du moteur](/manuals/optimization-size)
* [Taille du jeu](/manuals/optimization-size)

## FAQ {#faq}
:[HTML5 FAQ](../shared/html5-faq.md)
