---
title: Uso delle dipendenze Gradle nelle build Android
brief: Questo manuale spiega come usare Gradle per risolvere le dipendenze nelle build Android.
---

# Gradle per Android {#gradle-for-android}

A differenza del modo in cui vengono solitamente create le build delle applicazioni Android, Defold non usa [Gradle](https://gradle.org/) per l'intero processo di build. Defold usa invece gli strumenti Android a riga di comando, come `aapt2` e `bundletool`, direttamente nella build locale e usa Gradle soltanto per risolvere le dipendenze sul server di build.


## Risoluzione delle dipendenze {#resolving-dependencies}

Le estensioni native possono includere un file `build.gradle` nella cartella `manifests/android` per specificare le dipendenze dell'estensione. Esempio:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Il server di build raccoglie i file `build.gradle` di tutte le estensioni e li usa per risolvere tutte le dipendenze e includerle durante la compilazione del codice nativo.

Esempi:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
