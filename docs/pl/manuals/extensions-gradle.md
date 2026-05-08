---
title: Korzystanie z zależności Gradle w kompilacjach Androida
brief: Ta instrukcja wyjaśnia, jak używać Gradle do rozwiązywania zależności w kompilacjach Androida.
---

# Gradle dla Androida

W przeciwieństwie do tego, jak zwykle buduje się aplikacje Android, Defold nie używa [Gradle](https://gradle.org/) do całego procesu budowania. Zamiast tego Defold używa bezpośrednio narzędzi wiersza poleceń Android, takich jak `aapt2` i `bundletool`, w lokalnym budowaniu, a Gradle wykorzystuje tylko podczas rozwiązywania zależności na serwerze budowania.


## Rozwiązywanie zależności

Rozszerzenia natywne mogą zawierać plik `build.gradle` w folderze `manifests/android`, aby określić zależności rozszerzenia. Przykład:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Serwer budowania zbierze pliki `build.gradle` ze wszystkich rozszerzeń i użyje ich do rozwiązywania wszystkich zależności oraz dołączenia ich podczas budowania kodu natywnego.

Przykłady:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
