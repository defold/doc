---
title: Defold'da yerel kodda hata ayıklama
brief: Bu kılavuz, Defold'da yerel kodda nasıl hata ayıklanacağını açıklar.
---

# Yerel kodda hata ayıklama

Defold kapsamlı biçimde test edilmiştir ve normal koşullarda çok nadiren çökmesi beklenir. Ancak özellikle oyununuz yerel kod eklentileri (native extensions) kullanıyorsa, hiçbir zaman çökmeyeceğini garanti etmek mümkün değildir. Çökmelerle veya beklediğiniz gibi davranmayan yerel kodla (native code) ilgili sorunlarla karşılaşırsanız başvurabileceğiniz birkaç farklı yöntem vardır:

* Kodda adım adım ilerlemek için bir hata ayıklayıcı kullanın
* Çıktı yazdırarak hata ayıklayın
* Bir çökme günlüğünü inceleyin
* Bir çağrı yığınına sembol çözümlemesi uygulayın


## Hata ayıklayıcı kullanma

En yaygın yöntem, kodu bir hata ayıklayıcı (`debugger`) aracılığıyla çalıştırmaktır. Kodda adım adım ilerlemenizi ve kesme noktaları (`breakpoints`) belirlemenizi sağlar; bir çökme yaşanırsa yürütmeyi durdurur.

Her platform için çeşitli hata ayıklayıcılar vardır.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Her araç belirli platformlarda hata ayıklayabilir:

* Visual studio - Windows + gdbserver destekleyen platformlar (ör. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + gdbserver destekleyen platformlar
* Xcode -  macOS, iOS ([daha fazla bilgi](/manuals/debugging-native-code-ios))
* Android Studio - Android ([daha fazla bilgi](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (lldb aracılığıyla)


## Çıktı yazdırarak hata ayıklama

Yerel kodunuzda hata ayıklamanın en basit yolu, [çıktı yazdırarak hata ayıklama (print debugging)](http://en.wikipedia.org/wiki/Debugging#Techniques) yöntemini kullanmaktır. Değişkenleri izlemek veya yürütme akışını belirtmek için [`dmLog` ad alanındaki](/ref/stable/dmLog/) işlevleri kullanın. Günlük işlevlerinden herhangi biri kullanıldığında, düzenleyicideki *Console* görünümüne ve [oyun günlüğüne](/manuals/debugging-game-and-system-logs) çıktı yazdırılır.


## Çökme günlüğünü inceleme

Defold motoru, kurtarılamayan bir çökme yaşarsa bir `_crash` dosyası kaydeder. Çökme dosyası, çökmeyle ilgili bilgilerin yanı sıra sistemle ilgili bilgileri de içerir. [Oyun günlüğü çıktısı](/manuals/debugging-game-and-system-logs), çökme dosyasının konumunu belirtir (bu konum işletim sistemine, cihaza ve uygulamaya göre değişir).

Bu dosyayı bir sonraki oturumda okumak için [crash modülünü](https://www.defold.com/ref/crash/) kullanabilirsiniz. Dosyayı okumanız, bilgileri toplamanız, konsola yazdırmanız ve çökme günlüklerinin toplanmasını destekleyen bir [analiz hizmetine](/tags/stars/analytics/) göndermeniz önerilir.

::: important
Windows'ta ayrıca bir `_crash.dmp` dosyası oluşturulur. Bu dosya, bir çökmeye yol açan hatayı ayıklarken yararlıdır.
:::

### Bir cihazdan çökme günlüğünü alma

Bir mobil cihazda çökme yaşanırsa, çökme dosyasını kendi bilgisayarınıza indirip yerel olarak ayrıştırmayı seçebilirsiniz.

#### Android

Uygulamada [hata ayıklama etkinse](/manuals/project-settings/#android), [Android Debug Bridge (ADB) aracını](https://developer.android.com/studio/command-line/adb.html) ve `adb shell` komutunu kullanarak çökme günlüğünü alabilirsiniz:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

iTunes'ta bir uygulamanın kapsayıcısını (container) görüntüleyebilir/indirebilirsiniz.

`Xcode -> Devices` penceresinde çökme günlüklerini de seçebilirsiniz


## Çağrı yığınına sembol çözümlemesi uygulama {#symbolicate-a-callstack}

Bir `_crash` dosyasından veya bir [günlük dosyasından](/manuals/debugging-game-and-system-logs) çağrı yığını (callstack) elde ederseniz, buna sembol çözümlemesi (symbolication) uygulayabilirsiniz. Bu işlem, çağrı yığınındaki her adresi bir dosya adına ve satır numarasına dönüştürür; böylece sorunun asıl nedenini bulmanıza yardımcı olur.

Çağrı yığınını doğru motorla eşleştirmeniz önemlidir; aksi takdirde büyük olasılıkla yanlış yerlerde hata ayıklamaya çalışırsınız! [`--with-symbols`](https://www.defold.com/manuals/bob/) seçeneğini [bob](https://www.defold.com/manuals/bob/) ile paketleme yaparken kullanın veya düzenleyicideki paketleme iletişim kutusunda "Generate debug symbols" onay kutusunu işaretleyin:

* iOS - `dmengine.dSYM.zip` klasörü, `build/arm64-ios` içinde bulunur ve iOS derlemelerinin hata ayıklama sembollerini içerir.
* macOS - `dmengine.dSYM.zip` klasörü, `build/x86_64-macos` içinde bulunur ve macOS derlemelerinin hata ayıklama sembollerini içerir.
* Android - `projecttitle.apk.symbols/lib/` dağıtım paketi çıktı klasörü, hedef mimarilerin hata ayıklama sembollerini içerir.
* Linux - yürütülebilir dosya, hata ayıklama sembollerini içerir.
* Windows - `dmengine.pdb` dosyası, `build/x86_64-win32` içinde bulunur ve Windows derlemelerinin hata ayıklama sembollerini içerir.
* HTML5 - HTML5 dağıtım paketinin yanındaki `<project_name>_symbols` dizini, `<project_name>_wasm.js.symbols` dosyasını ve `wasm_pthread-web` mimarisi seçildiğinde `<project_name>_pthread_wasm.js.symbols` dosyasını içerir.

::: important
Oyununuzun herkese açık olarak yayımladığınız her sürümü için hata ayıklama sembollerini bir yerde saklamanız ve bu sembollerin hangi sürüme ait olduğunu bilmeniz çok önemlidir. Hata ayıklama sembolleri olmadan yerel kodda meydana gelen hiçbir çökmenin hatasını ayıklayamazsınız! Ayrıca motorun sembolleri çıkarılmamış (`unstripped`) bir sürümünü saklamanız önerilir. Böylece çağrı yığınının sembol çözümlemesi en iyi biçimde yapılabilir.
:::


### Sembolleri Google Play'e yükleme
Google Play'de kaydedilen çökmelerde sembolleri çözümlenmiş çağrı yığınlarının gösterilmesi için [hata ayıklama sembollerini Google Play'e yükleyebilirsiniz](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems). `projecttitle.apk.symbols/lib/` dağıtım paketi çıktı klasörünün içeriğini zip arşivi olarak sıkıştırın. Bu klasör, `arm64-v8a`, `armeabi-v7a` ve `x86_64` gibi mimari adlarını taşıyan bir veya daha fazla alt klasör içerir.


### Android çağrı yığınına sembol çözümlemesi uygulama

1. Motoru derleme klasörünüzden alın

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Zip arşivini bir klasöre çıkarın:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Çağrı yığınındaki adresi bulun

	Örneğin, sembolleri çözümlenmemiş çağrı yığınında şöyle görünebilir

	`#00 pc 00257224 libmy_game_name.so`

	Burada adres *`00257224`* değeridir

4. Adresi çözümleyin

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Not: [Android günlüklerinden](/manuals/debugging-game-and-system-logs) bir yığın izi (stack trace) elde ederseniz, [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) kullanarak buna sembol çözümlemesi uygulamanız mümkün olabilir

### iOS çağrı yığınına sembol çözümlemesi uygulama

1. Yerel kod eklentileri kullanıyorsanız, sunucu sizin için sembolleri (.dSYM) sağlayabilir (bob.jar aracına `--with-symbols` seçeneğini geçirin)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Yerel kod eklentileri kullanmıyorsanız, standart motorun sembollerini indirin:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Yükleme adresini kullanarak sembol çözümlemesi uygulayın

	Bilinmeyen bir nedenle, yalnızca çağrı yığınındaki adresi girmek işe yaramaz (yani yükleme adresi 0x0 olduğunda)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Yükleme adresini doğrudan belirtmek de işe yaramaz

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Adrese yükleme adresini eklemek işe yarar:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
