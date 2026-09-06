---
title: Використання залежностей Gradle у збірках для Android
brief: Цей посібник пояснює, як використовувати Gradle для розв’язання залежностей у збірках для Android.
---

# Gradle для Android {#gradle-for-android}

На відміну від типового процесу збирання застосунків Android, Defold не використовує [Gradle](https://gradle.org/) для всього процесу збирання. Натомість під час локального збирання Defold безпосередньо використовує засоби командного рядка Android, зокрема `aapt2` і `bundletool`, і залучає Gradle лише для розв’язання залежностей на сервері збирання.


## Розв’язання залежностей {#resolving-dependencies}

Нативні розширення можуть містити файл `build.gradle` у папці `manifests/android`, щоб указати залежності розширення. Приклад:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Сервер збирання збере файли `build.gradle` з усіх розширень і використає їх, щоб розв’язати всі залежності та включити їх під час збирання нативного коду.

Приклади:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
