---
title: Extensions natives - manifestes d'extension
brief: Ce manuel décrit le manifeste d'extension et ses relations avec le manifeste d'application et le manifeste du moteur.
---

# Fichiers manifestes d'extension, d'application et du moteur {#extension-application-and-engine-manifest-files}

Le manifeste d'extension est un fichier de configuration contenant les options et les définitions de macros utilisées lors de la compilation d'une extension donnée. Cette configuration est combinée à une configuration au niveau de l'application et à une configuration de base pour le moteur Defold lui-même.

## Manifeste d'application {#app-manifest}

Le manifeste d'application (extension de fichier `.appmanifest`) est une configuration au niveau de l'application qui détermine comment compiler votre jeu sur les serveurs de build. Le manifeste d'application vous permet de supprimer les parties du moteur que vous n'utilisez pas. Si vous n'avez pas besoin d'un moteur physique, vous pouvez le supprimer de l'exécutable pour réduire sa taille. Découvrez comment exclure les fonctionnalités inutilisées [dans le manuel du manifeste d'application](/manuals/app-manifest).

## Manifeste du moteur {#engine-manifest}

Le moteur Defold possède un manifeste de build (`build.yml`) inclus dans chaque version du moteur et du SDK Defold. Le manifeste détermine les versions de SDK à utiliser, les compilateurs, éditeurs de liens et autres outils à exécuter, ainsi que les options de compilation et d'édition de liens à transmettre par défaut à ces outils. Le manifeste se trouve dans share/extender/build_input.yml [sur GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Manifeste d'extension {#extension-manifest}

Le manifeste d'extension (`ext.manifest`), quant à lui, est un fichier de configuration propre à une extension. Il détermine comment le code source de l'extension est compilé et lié, et quelles bibliothèques supplémentaires inclure. 

Les trois types de fichiers manifestes partagent la même syntaxe afin de pouvoir être fusionnés et de contrôler entièrement la compilation des extensions et du jeu.

Pour chaque extension compilée, les manifestes sont combinés comme suit :

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Cela vous permet de redéfinir le comportement par défaut du moteur ainsi que celui de chaque extension. Pour l'étape finale d'édition de liens, nous fusionnons le manifeste d'application avec le manifeste Defold :

	manifest = merge(game.appmanifest, build.yml)


### Le fichier ext.manifest {#the-extmanifest-file}

Outre le nom de l'extension, le fichier manifeste peut contenir des options de compilation et d'édition de liens, des bibliothèques et des frameworks propres à chaque plateforme. Si le fichier *ext.manifest* ne contient pas de segment "platforms", ou si une plateforme ne figure pas dans la liste, le build pour la plateforme cible de votre bundle sera tout de même effectué, mais sans aucune option supplémentaire.

Voici un exemple :

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    arm64_sim-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Clés autorisées {#allowed-keys}

Les clés autorisées pour les options de compilation propres à chaque plateforme sont :

* `frameworks` - Frameworks Apple à inclure lors de la compilation (iOS et macOS)
* `weakFrameworks` - Frameworks Apple à inclure de manière facultative lors de la compilation (iOS et macOS)
* `flags` - Options à transmettre au compilateur
* `linkFlags` - Options à transmettre à l'éditeur de liens
* `libs` - Bibliothèques supplémentaires à inclure lors de l'édition de liens
* `defines` - Macros à définir lors de la compilation
* `aaptExtraPackages` - Nom de paquet supplémentaire à générer (Android)
* `aaptExcludePackages` - Expression régulière (ou noms exacts) des paquets à exclure (Android)
* `aaptExcludeResourceDirs` - Expression régulière (ou noms exacts) des répertoires de ressources à exclure (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Ces options servent à supprimer des éléments précédemment définis dans le contexte de la plateforme.

Nous appliquons un filtre fondé sur une liste d'autorisation à tous les mots-clés. Cela évite les manipulations de chemins non autorisées et l'accès à des fichiers situés en dehors du dossier des fichiers envoyés pour le build.
