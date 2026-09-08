---
title: Débogage du code natif dans Defold
brief: Ce manuel explique comment déboguer du code natif dans Defold.
---

# Débogage du code natif {#debugging-native-code}

Defold est rigoureusement testé et ne devrait que très rarement planter dans des circonstances normales. Il est toutefois impossible de garantir qu'il ne plantera jamais, en particulier si votre jeu utilise des extensions natives. Si vous rencontrez des plantages ou du code natif qui ne se comporte pas comme prévu, plusieurs approches sont possibles :

* Utiliser un débogueur pour parcourir le code pas à pas
* Utiliser le débogage par affichage
* Analyser un journal de plantage
* Symboliquer une pile d'appels


## Utiliser un débogueur {#use-a-debugger}

L'approche la plus courante consiste à exécuter le code avec un débogueur (`debugger`). Il vous permet de parcourir le code pas à pas, de définir des points d'arrêt (`breakpoints`) et arrête l'exécution en cas de plantage.

Plusieurs débogueurs sont disponibles pour chaque plateforme.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Chaque outil permet de déboguer certaines plateformes :

* Visual studio - Windows + plateformes prenant en charge gdbserver (p. ex. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + plateformes prenant en charge gdbserver
* Xcode -  macOS, iOS ([en savoir plus](/manuals/debugging-native-code-ios))
* Android Studio - Android ([en savoir plus](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


## Utiliser le débogage par affichage {#use-print-debugging}

La manière la plus simple de déboguer votre code natif est d'utiliser le [débogage par affichage](http://en.wikipedia.org/wiki/Debugging#Techniques). Utilisez les fonctions de l'[espace de noms (namespace) `dmLog`](/ref/stable/dmLog/) pour surveiller des variables ou indiquer le déroulement de l'exécution. Toutes les fonctions de journalisation affichent leurs messages dans la vue *Console* de l'éditeur et dans le [journal du jeu](/manuals/debugging-game-and-system-logs).


## Analyser un journal de plantage {#analyze-a-crash-log}

Le moteur Defold enregistre un fichier `_crash` en cas de plantage brutal. Ce fichier contient des informations sur le système et sur le plantage. La [sortie du journal du jeu](/manuals/debugging-game-and-system-logs) indique l'emplacement du fichier de plantage (qui varie selon le système d'exploitation, l'appareil et l'application).

Vous pouvez utiliser le [module crash](https://www.defold.com/ref/crash/) pour lire ce fichier lors de la session suivante. Il est recommandé de lire le fichier, de rassembler les informations, de les afficher dans la console et de les envoyer à un [service d'analyse](/tags/stars/analytics/) qui prend en charge la collecte des journaux de plantage.

::: important
Sous Windows, un fichier `_crash.dmp` est également généré. Ce fichier est utile pour déboguer un plantage.
:::

### Récupérer le journal de plantage d'un appareil {#getting-the-crash-log-from-a-device}

Si un plantage se produit sur un appareil mobile, vous pouvez télécharger le fichier de plantage sur votre ordinateur et l'analyser localement.

#### Android {#android}

Si l'application [autorise le débogage](/manuals/project-settings/#android), vous pouvez récupérer le journal de plantage à l'aide de l'[outil Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) et de la commande `adb shell` :

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS {#ios}

Dans iTunes, vous pouvez afficher ou télécharger le conteneur d'une application.

Dans la fenêtre `Xcode -> Devices`, vous pouvez également sélectionner les journaux de plantage


## Symboliquer une pile d'appels {#symbolicate-a-callstack}

Si vous récupérez une pile d'appels à partir d'un fichier `_crash` ou d'un [fichier journal](/manuals/debugging-game-and-system-logs), vous pouvez la symboliquer. Cela consiste à convertir chaque adresse de la pile d'appels en un nom de fichier et un numéro de ligne, ce qui aide à trouver la cause du problème.

Il est important d'utiliser le moteur correspondant à la pile d'appels, sinon vous risquez fort de déboguer les mauvais éléments ! Utilisez l'option [`--with-symbols`](https://www.defold.com/manuals/bob/) lors de la création d'un bundle avec [bob](https://www.defold.com/manuals/bob/), ou cochez la case « Generate debug symbols » dans la boîte de dialogue de création de bundles de l'éditeur :

* iOS - le dossier `dmengine.dSYM.zip` dans `build/arm64-ios` contient les symboles de débogage des builds iOS.
* macOS - le dossier `dmengine.dSYM.zip` dans `build/x86_64-macos` contient les symboles de débogage des builds macOS.
* Android - le dossier de sortie du bundle `projecttitle.apk.symbols/lib/` contient les symboles de débogage des architectures cibles.
* Linux - l'exécutable contient les symboles de débogage.
* Windows - le fichier `dmengine.pdb` dans `build/x86_64-win32` contient les symboles de débogage des builds Windows.
* HTML5 - le répertoire `<project_name>_symbols` situé à côté du bundle HTML5 contient `<project_name>_wasm.js.symbols` et, lorsque l'architecture `wasm_pthread-web` est sélectionnée, `<project_name>_pthread_wasm.js.symbols`.

::: important
Il est très important de conserver les symboles de débogage pour chaque version publique de votre jeu et de savoir à quelle version ils correspondent. Vous ne pourrez déboguer aucun plantage natif sans les symboles de débogage ! Vous devriez également conserver une version `unstripped` du moteur, dont les symboles n'ont pas été supprimés. Cela permet d'obtenir la meilleure symbolication possible de la pile d'appels.
:::


### Importer des symboles dans Google Play {#uploading-symbols-to-google-play}
Vous pouvez [importer les symboles de débogage dans Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) afin que les piles d'appels des plantages enregistrés dans Google Play soient symboliquées. Créez une archive ZIP du contenu du dossier de sortie du bundle `projecttitle.apk.symbols/lib/`. Ce dossier comprend un ou plusieurs sous-dossiers portant des noms d'architectures tels que `arm64-v8a`, `armeabi-v7a` et `x86_64`.


### Symboliquer une pile d'appels Android {#symbolicate-an-android-callstack}

1. Récupérez le moteur dans votre dossier de build

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Décompressez-le dans un dossier :

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Repérez l'adresse dans la pile d'appels

	Par exemple, dans une pile d'appels non symboliquée, elle pourrait se présenter ainsi

	`#00 pc 00257224 libmy_game_name.so`

	Où *`00257224`* est l'adresse

4. Résolvez l'adresse

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Remarque : si vous disposez d'une trace de pile provenant des [journaux Android](/manuals/debugging-game-and-system-logs), vous pouvez peut-être la symboliquer avec [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Symboliquer une pile d'appels iOS {#symbolicate-an-ios-callstack}

1. Si vous utilisez des extensions natives, le serveur peut vous fournir les symboles (.dSYM) (passez `--with-symbols` à bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Si vous n'utilisez pas d'extensions natives, téléchargez les symboles du moteur standard :

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Symboliquez à l'aide de l'adresse de chargement

	Pour une raison inconnue, utiliser simplement l'adresse de la pile d'appels ne fonctionne pas (c'est-à-dire avec l'adresse de chargement 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Neither does specifying the load address directly

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Adding the load address to the address works:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
