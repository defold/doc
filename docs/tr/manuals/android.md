---
title: Android platformu için Defold ile geliştirme
brief: Bu kılavuz, Defold uygulamalarının Android cihazlar için nasıl derleneceğini ve cihazlarda nasıl çalıştırılacağını açıklar
---

# Android için geliştirme

Android cihazlarda kendi uygulamalarınızı serbestçe çalıştırabilirsiniz. Oyununuzun bir sürümünü derleyip bir Android cihaza kopyalamak çok kolaydır. Bu kılavuz, oyununuzu Android için paketleme adımlarını açıklar. Geliştirme sırasında oyununuzu [geliştirme uygulaması](/manuals/dev-app) üzerinden çalıştırmak genellikle tercih edilir; çünkü bu uygulama, içerik ve kodu doğrudan cihazınızda çalışma sırasında yeniden yüklemenize (hot reload) olanak tanır.

## Android ve Google Play imzalama süreci

Android, tüm APK dosyalarının bir cihaza kurulmadan veya güncellenmeden önce bir sertifikayla dijital olarak imzalanmasını gerektirir. Android App Bundle (AAB) biçimini kullanıyorsanız Play Console'a yüklemeden önce yalnızca uygulama paketinizi imzalamanız gerekir; geri kalanını [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) halleder. Bununla birlikte, uygulamanızı Google Play'e veya diğer uygulama mağazalarına yüklemek ve herhangi bir mağazanın dışında dağıtmak için elle de imzalayabilirsiniz.

Defold düzenleyicisinden veya [komut satırı aracından](/manuals/bob) bir Android uygulaması dağıtım paketi (bundle) oluştururken uygulamanızın imzalanmasında kullanılacak bir anahtar deposu (keystore; sertifikanızı ve anahtarınızı içerir) ve anahtar deposu parolası sağlayabilirsiniz. Bunları sağlamazsanız Defold bir hata ayıklama anahtar deposu oluşturur ve uygulamanın dağıtım paketini imzalarken bunu kullanır.

::: important
Uygulamanız bir hata ayıklama anahtar deposuyla imzalandıysa onu Google Play'e **asla** yüklememelisiniz. Her zaman kendinizin oluşturduğu, bu amaca ayrılmış bir anahtar deposu kullanın.
:::

## Anahtar deposu oluşturma {#creating-a-keystore}

::: sidenote
Defold, Android imzalama süreci için bir anahtar deposu kullanır. [Bu forum gönderisinde daha fazla bilgi bulabilirsiniz](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Bir anahtar deposunu [Android Studio kullanarak](https://developer.android.com/studio/publish/app-signing#generate-key) veya bir terminalden/komut isteminden oluşturabilirsiniz:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Bu işlem, bir anahtar ve sertifika içeren `mykeystore.keystore` adlı bir anahtar deposu dosyası oluşturur. Anahtara ve sertifikaya erişim `5Up3r_53cR3t` parolasıyla korunur. Anahtar ve sertifika 25 yıl (9125 gün) boyunca geçerli olur. Oluşturulan anahtar ve sertifika `myAlias` takma adıyla tanımlanır.

::: important
Anahtar deposunu ve ona ait parolayı güvenli bir yerde sakladığınızdan emin olun. Uygulamalarınızı kendiniz imzalayıp Google Play'e yüklüyorsanız ve anahtar deposu veya anahtar deposu parolası kaybolursa uygulamayı Google Play'de güncellemeniz mümkün olmaz. Google Play App Signing kullanıp uygulamalarınızı sizin için Google'ın imzalamasını sağlayarak bu durumdan kaçınabilirsiniz.
:::


## Android uygulaması dağıtım paketi oluşturma {#creating-an-android-application-bundle}

Düzenleyici, oyununuz için kolayca bağımsız bir uygulama dağıtım paketi oluşturmanızı sağlar. Paketlemeden önce *game.project* [proje ayarları dosyasında](/manuals/project-settings/#android) uygulama için kullanılacak simgeleri belirtebilir, sürüm kodunu ayarlayabilir ve benzeri işlemleri yapabilirsiniz.

Paketlemek için menüden <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> seçeneğini seçin.

Düzenleyicinin otomatik olarak rastgele hata ayıklama sertifikaları oluşturmasını istiyorsanız *Keystore* ve *Keystore password* alanlarını boş bırakın:

![Android dağıtım paketini imzalama](images/android/sign_bundle.png)

Dağıtım paketinizi belirli bir anahtar deposuyla imzalamak istiyorsanız *Keystore* ve *Keystore password* alanlarını belirtin. *Keystore* dosyasının `.keystore` uzantısına sahip olması, parolanın ise `.txt` uzantılı bir metin dosyasında saklanması beklenir. Anahtar deposundaki anahtar, anahtar deposunun kendisinden farklı bir parola kullanıyorsa *Key password* belirtmeniz de mümkündür:

![Android dağıtım paketini imzalama](images/android/sign_bundle2.png)

Defold hem APK hem de AAB dosyalarının oluşturulmasını destekler. *Bundle Format* açılır listesinden APK veya AAB seçin.

Uygulama dağıtım paketi ayarlarını yapılandırdıktan sonra <kbd>Create Bundle</kbd> düğmesine basın. Ardından, dağıtım paketinin bilgisayarınızda nerede oluşturulacağını belirtmeniz istenir.

![Android uygulama paketi dosyası](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Android uygulaması dağıtım paketini kurma

#### APK kurma

Bir *`.apk`* dosyası `adb` aracıyla cihazınıza veya [Google Play geliştirici konsolu](https://play.google.com/apps/publish/) üzerinden Google Play'e kopyalanabilir.

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Düzenleyiciyi kullanarak APK kurma

Düzenleyicinin Bundle iletişim kutusundaki "Install on connected device" ve "Launch installed app" onay kutularını kullanarak bir *`.apk`* dosyasını kurup başlatabilirsiniz:

![APK kurma ve başlatma](images/android/install_and_launch.png)

Bu özelliğin çalışması için *ADB* kurulu olmalı ve bağlı cihazda *USB debugging* etkinleştirilmelidir. Düzenleyici ADB komut satırı aracının kurulum konumunu algılayamazsa bunu [Preferences](/manuals/editor-preferences/#tools) içinde belirtmeniz gerekir.

#### AAB kurma

Bir *.aab* dosyası [Google Play geliştirici konsolu](https://play.google.com/apps/publish/) üzerinden Google Play'e yüklenebilir. [Android bundletool](https://developer.android.com/studio/command-line/bundletool) kullanarak bir *.aab* dosyasından yerel olarak kurmak üzere bir *`.apk`* dosyası oluşturmak da mümkündür.

## R8 ile Java kodunu küçültme {#shrinking-java-code-with-r8}

R8, küçültme, optimizasyon ve karartma (obfuscation) yoluyla Java kodunun boyutunu azaltır.

### R8'i etkinleştirme {#enabling-r8}

*game.project* dosyasındaki **Android ▸ R8 Keep Rules** alanında `/builtins/manifests/android/dmengine.keep` dosyasını seçin. Bu, Defold'un varsayılan kurallarını doğrudan kullanır:

```ini
[android]
r8_keep_rules = /builtins/manifests/android/dmengine.keep
```

Java kodu içeren her eklentinin, çalışma sırasında ihtiyaç duyduğu sınıflar için bir `.keep` dosyası sağladığından emin olun. Eklenti kuralları, proje derlenirken seçili proje kurallarıyla birleştirilir. R8'i etkinleştirdikten sonra yayıma yönelik bir derlemeyi cihazda test edin.

**R8 Keep Rules** alanı boş bırakıldığında küçültme işlemi yapılmadan D8 kullanılır. R8 etkinleştirildiğinde, yerel kod eklentileri (native extension) olmayan bir projede bile yerel kod eklentisi derleme hizmeti kullanılır.

### Bir eklentiye kurallar ekleme

Bir eklentinin koruma kuralları, eklentinin `manifests/android` dizininde, `build.gradle` dosyasının yanında bulunur. Bir dosyanın nasıl ekleneceğini ve eklentinin Java sınıflarının nasıl korunacağını öğrenmek için [Android eklentileri için R8 koruma kuralları](/manuals/extensions/#r8-keep-rules-for-android) bölümüne bakın.

### Karartma eşlemesini saklama

Derleme bir `mapping.txt` dosyası oluşturduğunda R8'in bu dosyasını saklamak için Android dağıtım paketi iletişim kutusunda **Generate debug symbols** seçeneğini etkinleştirin veya Bob'a `--with-symbols` seçeneğini geçirin. Örneğin, proje dizininden:

```sh
java -jar bob.jar --platform arm64-android --variant release \
  --archive --with-symbols --bundle-output build/android \
  resolve build bundle
```

Eşleme, oluşturulan APK veya AAB dosyasının yanına `<binary-name>.apk.symbols/mapping.txt` olarak kaydedilir. Örneğin, proje başlığı `My Game` olduğunda yukarıdaki komut `build/android/MyGame/MyGame.apk.symbols/mapping.txt` dosyasını oluşturur.

Eşleme dosyasını, oluşturulduğu sürümle birlikte saklayın. Bu dosya, yığın izlerini (stack trace) yorumlamak için karartılmış Java adlarını özgün adlarla eşler; farklı bir derlemeye ait eşleme yanlış sonuçlar verebilir.

## İzinler

Defold motoru, tüm motor özelliklerinin çalışabilmesi için çeşitli izinler gerektirir. İzinler, *game.project* [proje ayarları dosyasında](/manuals/project-settings/#android) belirtilen `AndroidManifest.xml` dosyasında tanımlanır. Android izinleri hakkında daha fazla bilgiyi [resmî belgelerden](https://developer.android.com/guide/topics/permissions/overview) edinebilirsiniz. Varsayılan bildirimde aşağıdaki izinler istenir:

### android.permission.INTERNET ve android.permission.ACCESS_NETWORK_STATE (Koruma düzeyi: normal)
Uygulamaların *ağ soketleri* açmasına ve ağlar hakkındaki bilgilere erişmesine izin verir. Bu izinler internet erişimi için gereklidir. ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) ve ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Koruma düzeyi: normal)
İşlemcinin uyumasını veya ekranın kararmasını önlemek için PowerManager WakeLocks kullanılmasına izin verir. Bu izin, bir anlık bildirim alınırken cihazın uyumasını geçici olarak önlemek için gereklidir. ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## AndroidX kullanma
AndroidX, artık bakımı yapılmayan özgün Android Support Library'ye kıyasla büyük bir iyileştirmedir. AndroidX paketleri, aynı özellikleri ve yeni kütüphaneleri sağlayarak Support Library'nin yerini tamamen alır. [Asset Portal](/assets) üzerindeki Android eklentilerinin çoğu AndroidX'i destekler. AndroidX kullanmak istemiyorsanız [uygulama bildiriminde](https://defold.com/manuals/app-manifest/) `Use Android Support Lib` seçeneğini işaretleyerek AndroidX'i açıkça devre dışı bırakıp eski Android Support Library'yi kullanabilirsiniz.

![](images/android/enable_supportlibrary.png)

## Sık sorulan sorular
:[Android FAQ](../shared/android-faq.md)
