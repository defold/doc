---
title: Android derlemelerinde Gradle bağımlılıklarını kullanma
brief: Bu kılavuz, Android derlemelerindeki bağımlılıkları çözümlemek için Gradle'ın nasıl kullanılacağını açıklar.
---

# Android için Gradle

Android uygulamalarının derlenmesinde yaygın olan yaklaşımın aksine Defold, tüm proje derleme süreci için [Gradle](https://gradle.org/) kullanmaz. Bunun yerine yerel proje derlemesinde `aapt2` ve `bundletool` gibi Android komut satırı araçlarını doğrudan kullanır ve Gradle'dan yalnızca derleme sunucusunda bağımlılıkları çözümlerken yararlanır.


## Bağımlılıkları çözümleme

Yerel kod eklentileri (native extensions), eklentinin bağımlılıklarını belirtmek için `manifests/android` klasöründe bir `build.gradle` dosyası içerebilir. Örnek:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

Derleme sunucusu, tüm eklentilerin `build.gradle` dosyalarını toplar ve bunları kullanarak tüm bağımlılıkları çözümler ve yerel kod derlenirken bu bağımlılıkları derlemeye dahil eder.

Örnekler:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
