---
title: Использование Gradle-зависимостей в Android-сборках
brief: В этом руководстве объясняется, как использовать Gradle для разрешения зависимостей в Android-сборках.
---

# Gradle для Android

В отличие от того, как обычно собираются Android-приложения, Defold не использует [Gradle](https://gradle.org/) для всего процесса сборки. Вместо этого Defold использует Android command line tools, такие как `aapt2` и `bundletool`, напрямую при локальной сборке и задействует Gradle только при разрешении зависимостей на сервере сборки.


## Разрешение зависимостей

Native extension может включать файл `build.gradle` в папке `manifests/android`, чтобы указывать зависимости расширения. Пример:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Сервер сборки соберет файлы `build.gradle` из всех расширений и использует их, чтобы разрешить все зависимости и включить их при сборке нативного кода.

Примеры:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/build.gradle)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
