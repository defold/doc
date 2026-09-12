---
title: Android'de hata ayıklama
brief: Bu kılavuz, Android Studio kullanarak bir derleme çıktısında nasıl hata ayıklanacağını açıklar.
---

# Android'de hata ayıklama

Burada, Google'ın Android işletim sistemi için resmî tümleşik geliştirme ortamı (IDE) olan [Android Studio](https://developer.android.com/studio/) ile bir derleme çıktısında nasıl hata ayıklanacağını açıklıyoruz.


## Android Studio

* *game.project* dosyasındaki `android.debuggable` seçeneğini ayarlayarak dağıtım paketini (bundle) hazırlayın

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Uygulamayı hata ayıklama modunda, seçtiğiniz bir klasöre paketleyin.

	![Android için paketleme](images/extensions/debugging/android/bundle_android.png)

* [Android Studio](https://developer.android.com/studio/) uygulamasını başlatın

* `Profile or debug APK` seçeneğini seçin

	![APK hata ayıklama](images/extensions/debugging/android/android_profile_or_debug.png)

* Az önce oluşturduğunuz APK dağıtım paketini seçin

	![APK seçimi](images/extensions/debugging/android/android_select_apk.png)

* Ana `.so` dosyasını seçin ve hata ayıklama sembolleri içerdiğinden emin olun

	![.so dosyası seçimi](images/extensions/debugging/android/android_missing_symbols.png)

* İçermiyorsa sembolleri ayıklanmamış bir `.so` dosyası yükleyin. (Boyutu yaklaşık 20mb'dir)

* Yol eşlemeleri (path mappings), yürütülebilir dosyanın derlendiği yerdeki (buluttaki) yolları yerel diskinizdeki gerçek bir klasöre yeniden eşlemenizi sağlar.

* .so dosyasını seçin, ardından yerel diskinize bir eşleme ekleyin

	![Yol eşlemesi 1](images/extensions/debugging/android/path_mappings_android.png)

	![Yol eşlemesi 2](images/extensions/debugging/android/path_mappings_android2.png)

* Motorun kaynak koduna erişiminiz varsa ona da bir yol eşlemesi ekleyin.

* Şu anda hata ayıkladığınız sürüme geçtiğinizden emin olun

	defold$ git checkout 1.2.148

* `Apply changes` düğmesine basın

* Artık projenizde eşlenen kaynak kodu görmeniz gerekir

	![Kaynak kod eşlemeleri](images/extensions/debugging/android/source_mappings_android.png)

* Bir kesme noktası (breakpoint) ekleyin

	![Kesme noktası](images/extensions/debugging/android/breakpoint_android.png)

* `Run` -> `Debug "Appname"` seçeneğine basın ve yürütmeyi durdurmak istediğiniz kodu çağırın

	![Kesme noktası](images/extensions/debugging/android/callstack_variables_android.png)

* Artık çağrı yığınında (call stack) adım adım ilerleyebilir ve değişkenleri inceleyebilirsiniz


## Notlar

### Yerel kod eklentisinin iş klasörü

Şu anda yerel kod eklentisi (native extension) geliştirme iş akışı biraz zahmetlidir. Bunun nedeni, iş klasörünün adının
her derlemede rastgele belirlenmesi ve yol eşlemesinin her derlemede geçersiz hale gelmesidir.

Ancak tek bir hata ayıklama oturumu için sorunsuz çalışır.

Yol eşlemeleri, Android Studio projesindeki `.iml` proje dosyasında saklanır.

İş klasörünü yürütülebilir dosyadan öğrenmek mümkündür

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

İş klasörü, her seferinde rastgele bir sayıyla `job1298751322870374150` biçiminde adlandırılır.

