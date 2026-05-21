---
title: Usando dependências do Gradle em builds Android
brief: Este manual explica como usar o Gradle para resolver dependências em builds Android.
---

# Gradle para Android

Ao contrário da forma como aplicações Android normalmente são compiladas, o Defold não usa o [Gradle](https://gradle.org/) em todo o processo de build. Em vez disso, o Defold usa ferramentas de linha de comando do Android, como `aapt2` e `bundletool`, diretamente no build local, e aproveita o Gradle apenas ao resolver dependências no servidor de build.


## Resolvendo dependências

Extensões nativas podem incluir um arquivo `build.gradle` na pasta `manifests/android` para especificar as dependências da extensão. Exemplo:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

O servidor de build coletará os arquivos `build.gradle` de todas as extensões e os usará para resolver todas as dependências e incluí-las ao compilar o código nativo.

Exemplos:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
