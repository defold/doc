---
title: Extensions natives - Bonnes pratiques
brief: Ce manuel décrit les bonnes pratiques pour développer des extensions natives.
---

# Bonnes pratiques {#best-practices}

Écrire du code multiplateforme peut être difficile, mais certaines méthodes permettent de faciliter à la fois son développement et sa maintenance.


## Structure du projet {#project-structure}

Lorsque vous créez une extension, quelques choix facilitent son développement et sa maintenance.

### API Lua {#lua-api}

Il ne devrait y avoir qu'une seule API Lua et une seule implémentation de celle-ci. Il est ainsi beaucoup plus facile d'obtenir le même comportement sur toutes les plateformes.

Si la plateforme concernée ne doit pas prendre en charge l'extension, il est recommandé de ne tout simplement pas enregistrer de module Lua. Vous pouvez ainsi détecter sa prise en charge en vérifiant si sa valeur est `nil` :

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Structure des dossiers {#folder-structure}

La structure de dossiers suivante est fréquemment utilisée pour les extensions :

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Notez que les fichiers `myextension.mm` et `myextension_android.cpp` ne sont nécessaires que si vous effectuez des appels natifs propres à la plateforme concernée.

#### Dossiers des plateformes {#platform-folders}

À certains endroits, l'architecture de la plateforme sert de nom de dossier pour déterminer les fichiers à utiliser lors de la compilation de l'application ou de la création de son bundle. Ces noms prennent la forme suivante :

    <architecture>-<platform>

La liste actuelle est la suivante :

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Par exemple, placez les bibliothèques propres à une plateforme dans :

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Écriture de code natif {#writing-native-code}

Dans le code source de Defold, C++ est utilisé avec beaucoup de parcimonie et la majeure partie du code ressemble beaucoup à du C. Il n'y a pratiquement aucun modèle, à l'exception de quelques classes de conteneurs, car les modèles augmentent les temps de compilation ainsi que la taille de l'exécutable.

### Version de C++ {#c-version}

Pour compiler le cœur du moteur, nous utilisons C++11, mais nous utilisons C++14 sur Windows. Les builds pour consoles nécessitent désormais généralement C++14 ou une version ultérieure.

Pour les extensions natives, nous n'imposons pas de version de C++ et utilisons la version par défaut de la chaîne d'outils de la plateforme.

Le code source de Defold évite les fonctionnalités et les versions les plus récentes de C++. C'est principalement parce que les nouvelles fonctionnalités ne sont pas nécessaires pour développer un moteur de jeu, mais aussi parce que suivre les dernières fonctionnalités de C++ prend du temps et que les maîtriser réellement demande beaucoup de temps précieux.

Cette approche présente aussi l'avantage, pour les développeurs d'extensions, que Defold conserve une ABI stable. Il faut également souligner que les fonctionnalités les plus récentes de C++ peuvent empêcher la compilation du code sur différentes plateformes, car leur prise en charge varie.

### Aucune exception C++ {#no-c-exceptions}

Defold n'utilise aucune exception dans le moteur. Les moteurs de jeu évitent généralement les exceptions, car les données sont (pour la plupart) connues à l'avance, pendant le développement. Supprimer la prise en charge des exceptions C++ réduit la taille de l'exécutable et améliore les performances à l'exécution.

### Bibliothèques standard de modèles - STL {#standard-template-libraries-stl}

Comme le moteur Defold n'utilise aucun code de la STL, à l'exception de quelques algorithmes et fonctions mathématiques (`std::sort`, `std::upper_bound`, etc.), l'utilisation de la STL dans votre extension peut fonctionner.

Gardez toutefois à l'esprit que des incompatibilités d'ABI peuvent poser problème lorsque vous utilisez votre extension avec d'autres extensions ou des bibliothèques tierces.

Éviter les bibliothèques STL (qui font un usage intensif des modèles) réduit aussi nos temps de build et, surtout, la taille de l'exécutable.

#### Chaînes de caractères {#strings}

Dans le moteur Defold, `const char*` est utilisé à la place de `std::string`. L'utilisation de `std::string` est un piège courant lorsque vous combinez différentes versions de C++ ou de compilateurs, car elle peut entraîner une incompatibilité d'ABI. L'utilisation de `const char*` et de quelques fonctions utilitaires permet de l'éviter.

### Masquer les fonctions {#make-functions-hidden}

Utilisez si possible le mot-clé `static` pour les fonctions locales à votre unité de compilation. Cela permet au compilateur d'effectuer certaines optimisations, qui peuvent à la fois améliorer les performances et réduire la taille de l'exécutable.

## Bibliothèques tierces {#3rd-party-libraries}

Lorsque vous choisissez une bibliothèque tierce à utiliser (quel que soit le langage), tenez compte des points suivants :

* Fonctionnalités - Résout-elle votre problème précis ?
* Performances - Entraîne-t-elle un coût en performances à l'exécution ?
* Taille de la bibliothèque - De combien la taille de l'exécutable final augmentera-t-elle ? Est-ce acceptable ?
* Dépendances - Nécessite-t-elle des bibliothèques supplémentaires ?
* Maintenance - Dans quel état se trouve la bibliothèque ? A-t-elle beaucoup de problèmes ouverts ? Est-elle toujours maintenue ?
* Licence - Autorise-t-elle son utilisation dans ce projet ?


## Dépendances à code source ouvert {#open-source-dependencies}

Assurez-vous toujours d'avoir accès à vos dépendances. Par exemple, si vous dépendez d'un projet sur GitHub, rien n'empêche la suppression de son dépôt ou un changement soudain d'orientation ou de propriétaire. Vous pouvez limiter ce risque en créant un fork du dépôt et en utilisant votre fork à la place du projet d'origine.

N'oubliez pas que le code de la bibliothèque sera injecté dans votre jeu. Assurez-vous donc qu'elle fait ce qu'elle est censée faire, et rien de plus !
