---
title: Hata ayıklama - oyun ve sistem günlükleri
brief: Bu kılavuz, oyun ve sistem günlüklerinin nasıl okunacağını açıklar.
---

# Oyun ve sistem günlüğü

Oyun günlüğü (game log), motordan, yerel kod eklentilerinden (native extension) ve oyun mantığınızdan gelen tüm çıktıları gösterir. [print()](/ref/stable/base/#print:...) ve [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) komutlarını betiklerinizden ve Lua modüllerinizden oyun günlüğünde bilgi göstermek için kullanabilirsiniz. Yerel kod eklentilerinden oyun günlüğüne yazmak için [`dmLog` ad alanındaki](/ref/stable/dmLog/) işlevleri kullanabilirsiniz. Oyun günlüğü düzenleyiciden, terminal penceresinden, platforma özgü araçlar kullanılarak veya bir günlük dosyasından okunabilir.

Sistem günlükleri (system log) işletim sistemi tarafından oluşturulur ve bir sorunun kaynağını saptamanıza yardımcı olabilecek ek bilgiler sağlayabilir. Sistem günlükleri, çökmeler için yığın izleri (stack trace) ve bellek yetersizliği uyarıları içerebilir.

::: important
Konsola/ekrana günlük çıktısı yalnızca Debug derlemelerinde bilgi gösterir. Release derlemelerinde konsol günlüğü boştur, ancak "Write Log File" proje ayarını "Always" olarak ayarlayarak Release derlemelerinde dosyaya günlük kaydetmeyi etkinleştirebilirsiniz. Ayrıntılar için aşağıya bakın.
:::

## Oyun günlüğünü düzenleyiciden okuma

Oyununuzu düzenleyiciden yerel olarak veya [mobil geliştirme uygulamasına](/manuals/dev-app) bağlı olarak çalıştırdığınızda tüm çıktılar düzenleyicinin konsol bölmesinde gösterilir:

![Düzenleyici 2](images/editor/editor2_overview.png)

## Oyun günlüğünü terminalden okuma

Bir Defold oyununu terminalden çalıştırdığınızda günlük, terminal penceresinde gösterilir. Windows ve Linux'ta oyunu başlatmak için terminale yürütülebilir dosyanın adını yazın. macOS'te motoru .app dosyasının içinden başlatmanız gerekir:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Oyun ve sistem günlüklerini platforma özgü araçlarla okuma

### HTML5

Günlükler, çoğu tarayıcının sunduğu geliştirici araçları kullanılarak okunabilir.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Oyun ve sistem günlüğünü görüntülemek için Android Debug Bridge (ADB) aracını kullanabilirsiniz.

:[Android ADB](../shared/android-adb.md)

Kurulum ve yapılandırma tamamlandıktan sonra cihazınızı USB üzerinden bağlayın, bir terminal açın ve şu komutları çalıştırın:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

Cihaz, oyunun yazdırdığı bilgilerle birlikte tüm çıktıları geçerli terminale aktarır.

Yalnızca Defold uygulamasının çıktılarını görmek istiyorsanız şu komutu kullanın:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

iOS'te oyun ve sistem günlüklerini okumak için birden fazla seçeneğiniz vardır:

1. Oyun ve sistem günlüğünü okumak için [Console aracını](https://support.apple.com/guide/console/welcome/mac) kullanabilirsiniz.
2. Cihazda çalışan bir oyuna bağlanmak için LLDB hata ayıklayıcısını kullanabilirsiniz. Bir oyunda hata ayıklamak için oyunun, hata ayıklamak istediğiniz cihazı içeren bir "Apple Developer Provisioning Profile" ile imzalanmış olması gerekir. Düzenleyiciden oyunun dağıtım paketini oluşturun ve paketleme iletişim kutusunda sağlama profilini (provisioning profile) belirtin (iOS için paketleme yalnızca macOS'te kullanılabilir).

Oyunu başlatmak ve hata ayıklayıcıyı bağlamak için [ios-deploy](https://github.com/phonegap/ios-deploy) adlı bir araca ihtiyacınız vardır. Terminalde aşağıdaki komutu çalıştırarak oyununuzu kurun ve hata ayıklayın:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

Bu işlem uygulamayı cihazınıza kurar, başlatır ve ona otomatik olarak bir LLDB hata ayıklayıcısı bağlar. LLDB'yi ilk kez kullanıyorsanız [LLDB'ye başlangıç](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html) yazısını okuyun.


## Oyun günlüğünü günlük dosyasından okuma

Dosyaya günlük kaydetmeyi denetlemek için *game.project* dosyasındaki "Write Log File" proje ayarını kullanın:

- "Never": Günlük dosyası yazılmaz.
- "Debug": Yalnızca Debug derlemeleri için günlük dosyası yazılır.
- "Always": Hem Debug hem de Release derlemeleri için günlük dosyası yazılır.

Etkinleştirildiğinde oyunun tüm çıktıları diskte "`log.txt`" adlı bir dosyaya yazılır. Oyunu cihazda çalıştırıyorsanız dosyayı şu şekilde çıkarabilirsiniz:

iOS
: Cihazınızı macOS ve Xcode kurulu bir bilgisayara bağlayın.

  Xcode'u açın ve <kbd>Window ▸ Devices and Simulators</kbd> seçeneğine gidin.

  Listeden cihazınızı, ardından *Installed Apps* listesinden ilgili uygulamayı seçin.

  Listenin altındaki dişli simgesine tıklayın ve <kbd>Download Container...</kbd> seçeneğini seçin.

  ![konteyneri indirme](images/debugging/download_container.png)

  Konteyner çıkarıldıktan sonra *Finder* içinde gösterilir. Konteynere sağ tıklayın ve <kbd>Show Package Content</kbd> seçeneğini seçin. "`log.txt`" dosyasını bulun; bu dosyanın "`AppData/Documents/`" içinde bulunması beklenir.

Android(
: "`log.txt`" dosyasının çıkarılabilmesi, işletim sistemi sürümüne ve üreticiye bağlıdır. İşte kısa ve basit bir [adım adım kılavuz](https://stackoverflow.com/a/48077004/129360).
