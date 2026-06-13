---
title: Usar dependencias de Gradle en builds de Android
brief: Este manual explica cómo usar Gradle para resolver dependencias en builds de Android.
---

# Gradle para Android

A diferencia de cómo se suelen crear las aplicaciones Android, Defold no usa [Gradle](https://gradle.org/) para todo el proceso de build. En su lugar, Defold usa herramientas de línea de comando de Android como `aapt2` y `bundletool` directamente en la build local y solo aprovecha Gradle al resolver dependencias en el servidor de build.


## Resolver dependencias

Las extensiones nativas pueden incluir un archivo `build.gradle` en la carpeta `manifests/android` para especificar las dependencias de la extensión. Ejemplo:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

El servidor de build recopilará los archivos `build.gradle` de todas las extensiones y los usará para resolver todas las dependencias e incluirlas al crear el código nativo.

Ejemplos:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
