---
title: Gradle-Abhängigkeiten in Android-Builds verwenden
brief: Dieses Handbuch erklärt, wie du Gradle zum Auflösen von Abhängigkeiten in Android-Builds verwendest.
---

# Gradle für Android {#gradle-for-android}

Anders als beim üblichen Erstellen von Android-Anwendungen verwendet Defold [Gradle](https://gradle.org/) nicht für den gesamten Build-Vorgang. Stattdessen verwendet Defold beim lokalen Build direkt Android-Kommandozeilenwerkzeuge wie `aapt2` und `bundletool` und setzt Gradle nur zum Auflösen von Abhängigkeiten auf dem Build-Server ein.


## Abhängigkeiten auflösen {#resolving-dependencies}

Native Erweiterungen (native extensions) können eine Datei `build.gradle` im Ordner `manifests/android` enthalten, um die Abhängigkeiten der Erweiterung anzugeben. Beispiel:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Der Build-Server sammelt die Dateien `build.gradle` aus allen Erweiterungen und verwendet sie, um alle Abhängigkeiten aufzulösen und sie beim Erstellen des nativen Codes einzubeziehen.

Beispiele:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
