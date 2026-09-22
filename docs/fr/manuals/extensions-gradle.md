---
title: Utilisation des dépendances Gradle dans les builds Android
brief: Ce manuel explique comment utiliser Gradle pour résoudre les dépendances des builds Android.
---

# Gradle pour Android {#gradle-for-android}

Contrairement à la manière dont les applications Android sont généralement compilées, Defold n'utilise pas [Gradle](https://gradle.org/) pour l'ensemble du processus de build. Defold utilise directement les outils Android en ligne de commande tels que `aapt2` et `bundletool` lors du build local et ne fait appel à Gradle que pour résoudre les dépendances sur le serveur de build.


## Résolution des dépendances {#resolving-dependencies}

Les extensions natives peuvent inclure un fichier `build.gradle` dans le dossier `manifests/android` pour définir les dépendances de l'extension. Exemple :

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Le serveur de build rassemble les fichiers `build.gradle` de toutes les extensions et les utilise pour résoudre l'ensemble des dépendances et les inclure lors de la compilation du code natif.

Exemples :

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)