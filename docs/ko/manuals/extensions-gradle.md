---
title: Android 빌드에서 Gradle 종속성 사용하기
brief: 이 매뉴얼은 Android 빌드에서 Gradle을 사용해 종속성을 해결하는 방법을 설명합니다.
---

# Android용 Gradle

Android 어플리케이션을 일반적으로 빌드하는 방식과 달리, Defold는 전체 빌드 과정에 [Gradle](https://gradle.org/)을 사용하지 않습니다. 대신 Defold는 로컬 빌드에서 `aapt2` 및 `bundletool` 같은 Android 커맨드 라인 도구를 직접 사용하며, 빌드 서버에서 종속성을 해결할 때만 Gradle을 활용합니다.


## 종속성 해결

네이티브 익스텐션은 익스텐션 종속성을 지정하기 위해 `manifests/android` 폴더에 `build.gradle` 파일을 포함할 수 있습니다. 예:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

빌드 서버는 모든 익스텐션에서 `build.gradle` 파일을 수집하고, 이를 사용해 모든 종속성을 해결한 뒤 네이티브 코드를 빌드할 때 포함합니다.

예:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
