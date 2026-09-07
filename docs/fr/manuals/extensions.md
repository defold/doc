---
title: Écrire des extensions natives pour Defold
brief: Ce manuel explique comment écrire une extension native pour le moteur de jeu Defold et la compiler à l'aide des services de build dans le cloud, sans aucune configuration préalable.
---

# Extensions natives {#native-extensions}

Si vous avez besoin d'interactions personnalisées de bas niveau avec des logiciels ou du matériel externes et que Lua ne suffit pas, le SDK Defold vous permet d'écrire des extensions du moteur en C, C++, C#, Objective-C, Java ou JavaScript, selon la plateforme cible. Les cas d'utilisation courants des extensions natives sont les suivants :

- Interaction avec du matériel spécifique, par exemple la caméra d'un téléphone mobile.
- Interaction avec des API externes de bas niveau, par exemple les API de réseaux publicitaires qui ne permettent pas d'interagir au moyen d'API réseau utilisables avec Luasocket.
- Calculs et traitement de données à hautes performances.

::: sidenote
La prise en charge de C# est expérimentale et s'adresse aux extensions natives, pas aux composants script (script components) Defold. Elle utilise .NET 9 NativeAOT pour produire une bibliothèque statique ; ajoutez des fichiers source `.cs` au dossier `src` d'une extension et le service de build génère le fichier de projet. La prise en charge des cibles dépend des capacités actuelles de NativeAOT et du service de build. Consultez l'[exemple officiel des langages pour les extensions natives](https://github.com/defold/example-languages) pour connaître le flux de travail actuel et la configuration testée.
:::

## Le serveur de build {#the-build-server}

Defold vous permet de commencer à utiliser les extensions natives sans aucune configuration, grâce à une solution de build dans le cloud. Toute extension native développée et ajoutée à un projet de jeu, directement ou par l'intermédiaire d'un [projet bibliothèque](/manuals/libraries/), fait partie du contenu ordinaire du projet. Il n'est pas nécessaire de compiler des versions spéciales du moteur et de les distribuer aux membres de l'équipe, car cela se fait automatiquement : tout membre de l'équipe qui compile et exécute le projet obtient un exécutable du moteur propre au projet, intégrant toutes les extensions natives.

![Build dans le cloud](images/extensions/cloud_build.png)

Defold fournit gratuitement le serveur de build dans le cloud, sans aucune restriction d'utilisation. Le serveur est hébergé en Europe, et l'URL à laquelle le code natif est envoyé se configure dans la [fenêtre des préférences de l'éditeur](/manuals/editor-preferences/#extensions) ou au moyen de l'option de ligne de commande `--build-server` de [bob](/manuals/bob/#usage). Si vous souhaitez configurer votre propre serveur, [suivez ces instructions](/manuals/extender-local-setup).

## Organisation du projet {#project-layout}

Pour créer une nouvelle extension, créez un dossier à la racine du projet. Ce dossier contiendra tous les paramètres, le code source, les bibliothèques et les ressources associés à l'extension. Le service de build des extensions reconnaît la structure des dossiers et rassemble les fichiers source et les bibliothèques.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: Le dossier de l'extension _doit_ contenir un fichier *ext.manifest*. Ce fichier de configuration contient les options et les définitions utilisées lors du build d'une extension individuelle. La définition du format de fichier se trouve dans le [manuel du manifeste des extensions](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Ce dossier devrait contenir tous les fichiers de code source.

*include*
: Ce dossier facultatif contient les fichiers d'inclusion.

*lib*
: Ce dossier facultatif contient les bibliothèques compilées dont dépend l'extension. Les fichiers de bibliothèque devraient être placés dans des sous-dossiers nommés selon `platform` ou `architecture-platform`, en fonction des architectures prises en charge par vos bibliothèques.

  :[platforms](../shared/platforms.md)

*manifests*
: Ce dossier facultatif contient des fichiers supplémentaires utilisés lors du build ou de la création de bundles. Consultez les détails ci-dessous.

*res*
: Ce dossier facultatif contient les ressources supplémentaires dont dépend l'extension. Les fichiers de ressources devraient être placés dans des sous-dossiers nommés selon `platform` ou `architecture-platform`, comme les sous-dossiers de `lib`. Un sous-dossier `common` est également autorisé pour contenir les fichiers de ressources communs à toutes les plateformes.

### Fichiers manifeste {#manifest-files}

Le dossier facultatif *manifests* d'une extension contient des fichiers supplémentaires utilisés lors du build et de la création de bundles. Les fichiers devraient être placés dans des sous-dossiers nommés selon `platform` :

* `android` - Ce dossier accepte un fichier de manifeste partiel à fusionner avec celui de l'application principale ([comme décrit ici](/manuals/extensions-manifest-merge-tool)).
  * Le dossier peut également contenir un fichier `build.gradle` avec des dépendances qui seront [résolues par Gradle](/manuals/extensions-gradle).
  * Enfin, le dossier peut également contenir zéro ou plusieurs fichiers ProGuard (expérimental).
* `ios` - Ce dossier accepte un fichier de manifeste partiel à fusionner avec celui de l'application principale ([comme décrit ici](/manuals/extensions-manifest-merge-tool)).
  * Le dossier peut également contenir un fichier `Podfile` avec des dépendances qui seront [résolues par Cocoapods](/manuals/extensions-cocoapods).
* `osx` - Ce dossier accepte un fichier de manifeste partiel à fusionner avec celui de l'application principale ([comme décrit ici](/manuals/extensions-manifest-merge-tool)).
* `web` - Ce dossier accepte un fichier de manifeste partiel à fusionner avec celui de l'application principale ([comme décrit ici](/manuals/extensions-manifest-merge-tool)).


## Partager une extension {#sharing-an-extension}

Les extensions sont traitées comme toute autre ressource de votre projet et peuvent être partagées de la même manière. Si le dossier d'une extension native est ajouté comme dossier de bibliothèque, il peut être partagé et utilisé par d'autres comme dépendance de projet. Consultez le [manuel des projets bibliothèques](/manuals/libraries/) pour plus d'informations.


## Un exemple d'extension simple {#a-simple-example-extension}

Créons une extension très simple. Nous commençons par créer un nouveau dossier *`myextension`* à la racine, puis nous ajoutons un fichier *`ext.manifest`* contenant le nom de l'extension « `MyExtension` ». Notez que ce nom est un symbole C++ et doit correspondre au premier argument de `DM_DECLARE_EXTENSION` (voir ci-dessous).

![Manifeste](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

L'extension se compose d'un seul fichier C++, *`myextension.cpp`*, créé dans le dossier « `src` ».

![Fichier C++](images/extensions/cppfile.png)

Le fichier source de l'extension contient le code suivant :

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Notez la macro `DM_DECLARE_EXTENSION`, utilisée pour déclarer les différents points d'entrée dans le code de l'extension. Le premier argument `symbol` doit correspondre au nom indiqué dans *ext.manifest*. Dans cet exemple simple, aucun point d'entrée `update` ou `on_event` n'est nécessaire ; on passe donc `0` à la macro pour ces arguments.

Il suffit maintenant de compiler le projet (<kbd>Project ▸ Build</kbd>). Cela envoie l'extension au service de build des extensions, qui produit un moteur personnalisé intégrant la nouvelle extension. Si le service rencontre des erreurs, une boîte de dialogue affiche les erreurs de build.

Pour tester l'extension, créez un objet de jeu (game object) et ajoutez un composant script avec du code de test :

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

Et voilà ! Nous avons créé une extension native entièrement fonctionnelle.


## Cycle de vie d'une extension {#extension-lifecycle}

Comme nous l'avons vu plus haut, la macro `DM_DECLARE_EXTENSION` sert à déclarer les différents points d'entrée dans le code de l'extension :

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Ces points d'entrée vous permettent d'exécuter du code à différents moments du cycle de vie d'une extension :

* Démarrage du moteur
  * Les systèmes du moteur démarrent
  * `app_init` de l'extension
  * `init` de l'extension - Toutes les API Defold ont été initialisées. Il s'agit du moment recommandé dans le cycle de vie de l'extension pour créer les liaisons Lua vers le code de l'extension.
  * Initialisation des scripts - La fonction `init()` des fichiers de script est appelée.
* Boucle du moteur
  * Mise à jour du moteur
    * `update` de l'extension
    * Mise à jour des scripts - La fonction `update()` des fichiers de script est appelée.
  * Événements du moteur (réduction/agrandissement de la fenêtre, etc.)
    * `on_event` de l'extension
* Arrêt du moteur (ou redémarrage)
  * Finalisation des scripts - La fonction `final()` des fichiers de script est appelée.
  * `final` de l'extension
  * `app_final` de l'extension

## Identifiants de plateforme définis {#defined-platform-identifiers}

Les identifiants suivants sont définis par le service de build sur chaque plateforme correspondante :

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Journaux du serveur de build {#build-server-logs}

Les journaux du serveur de build sont disponibles lorsque le projet utilise des extensions natives. Le journal du serveur de build (`log.txt`) est téléchargé avec le moteur personnalisé lors du build du projet. Il est stocké dans le fichier `.internal/%platform%/build.zip` et également extrait dans le dossier de build de votre projet.

## Exemples d'extensions {#example-extensions}

* [Exemple d'extension de base](https://github.com/defold/template-native-extension) (l'extension de ce manuel)
* [Exemple d'extension Android](https://github.com/defold/extension-android)
* [Exemple d'extension HTML5](https://github.com/defold/extension-html5)
* [Extension de lecteur vidéo pour macOS, iOS et Android](https://github.com/defold/extension-videoplayer)
* [Extension de caméra pour macOS et iOS](https://github.com/defold/extension-camera)
* [Extension d'achats intégrés pour iOS et Android](https://github.com/defold/extension-iap)
* [Extension Firebase Analytics pour iOS et Android](https://github.com/defold/extension-firebase-analytics)

Le [portail de ressources Defold](https://www.defold.com/assets/) contient également plusieurs extensions natives.
