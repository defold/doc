---
title: Débogage sur Android
brief: Ce manuel décrit comment déboguer un build avec Android Studio.
---

# Débogage sur Android {#debugging-on-android}

Nous décrivons ici comment déboguer un build avec [Android Studio](https://developer.android.com/studio/), l'IDE officiel du système d'exploitation Android de Google.


## Android Studio {#android-studio}

* Préparez le bundle en définissant l'option `android.debuggable` dans *game.project*

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Créez le bundle de l'application en mode débogage dans le dossier de votre choix.

	![Création du bundle Android](images/extensions/debugging/android/bundle_android.png)

* Lancez [Android Studio](https://developer.android.com/studio/)

* Choisissez `Profile or debug APK`

	![Débogage de l'APK](images/extensions/debugging/android/android_profile_or_debug.png)

* Choisissez le bundle APK que vous venez de créer

	![Sélection de l'APK](images/extensions/debugging/android/android_select_apk.png)

* Sélectionnez le fichier `.so` principal et assurez-vous qu'il contient les symboles de débogage

	![Sélection du fichier .so](images/extensions/debugging/android/android_missing_symbols.png)

* Si ce n'est pas le cas, chargez un fichier `.so` dont les symboles n'ont pas été supprimés. (Sa taille est d'environ 20 Mo.)

* Les correspondances de chemins vous permettent d'associer les différents chemins de l'environnement où l'exécutable a été compilé (dans le cloud) à un dossier réel sur votre disque local.

* Sélectionnez le fichier .so, puis ajoutez une correspondance vers votre disque local

	![Correspondance de chemins 1](images/extensions/debugging/android/path_mappings_android.png)

	![Correspondance de chemins 2](images/extensions/debugging/android/path_mappings_android2.png)

* Si vous avez accès au code source du moteur, ajoutez également une correspondance de chemins vers celui-ci.

* Assurez-vous d'extraire la version que vous déboguez actuellement

	defold$ git checkout 1.2.148

* Appuyez sur `Apply changes`

* Vous devriez maintenant voir le code source associé dans votre projet

	![Correspondances du code source](images/extensions/debugging/android/source_mappings_android.png)

* Ajoutez un point d'arrêt

	![Point d'arrêt](images/extensions/debugging/android/breakpoint_android.png)

* Appuyez sur `Run` -> `Debug "Appname"` et appelez le code dans lequel vous souhaitez interrompre l'exécution

	![Point d'arrêt](images/extensions/debugging/android/callstack_variables_android.png)

* Vous pouvez maintenant parcourir la pile d'appels et inspecter les variables


## Remarques {#notes}

### Dossier de tâche de l'extension native {#native-extension-job-folder}

Actuellement, ce flux de travail est un peu contraignant pour le développement. En effet, le nom du dossier de tâche
est aléatoire à chaque build, ce qui invalide la correspondance de chemins à chaque build.

Il convient cependant bien à une session de débogage.

Les correspondances de chemins sont enregistrées dans le fichier `.iml` du projet Android Studio.

Il est possible d'obtenir le dossier de tâche à partir de l'exécutable

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

Le dossier de tâche porte un nom comme `job1298751322870374150`, avec un nombre aléatoire à chaque fois.

