---
title: Android platformu için Defold ile geliştirme
brief: Bu kılavuz, Defold uygulamalarının Android cihazlar için nasıl derleneceğini ve cihazlarda nasıl çalıştırılacağını açıklar
---

# Android için geliştirme {#android-development}

Android cihazlarda kendi uygulamalarınızı serbestçe çalıştırabilirsiniz. Oyununuzun bir sürümünü derleyip bir Android cihaza kopyalamak çok kolaydır. Bu kılavuz, oyununuzu Android için paketleme adımlarını açıklar. Geliştirme sırasında oyununuzu [geliştirme uygulaması](/manuals/dev-app) üzerinden çalıştırmak genellikle tercih edilir; çünkü bu uygulama, içerik ve kodu doğrudan cihazınızda çalışma sırasında yeniden yüklemenize (hot reload) olanak tanır.

## Android ve Google Play imzalama süreci {#android-and-google-play-signing-process}

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

### Google Play indirme boyutunu tahmin etme {#estimating-the-google-play-download-size}

Google Play, oyunculara *`.aab`* dosyasını göndermez. Her cihaz yapılandırması için optimize edilmiş APK dosyaları oluşturur; bu nedenle oyuncunun indirdiği dosya, *`.aab`* dosyasından veya evrensel *`.apk`* dosyasından daha küçüktür. Dağıtım paketi oluşturulurken tahmini indirme boyutunu almak için Bundle iletişim kutusundaki *Estimate download size* onay kutusunu işaretleyin. Tahmin hem APK hem de AAB dağıtım paketi biçimleriyle çalışır.

![İndirme boyutunu tahmin etme](images/android/sign_bundle.png)

Tahmin konsola yazdırılır:

```
Estimated Play Store download size: 18.2 MB - 25.0 MB (arm64-v8a: 25.0 MB, armeabi-v7a: 18.2 MB - 18.9 MB)
```

Ayrıca dağıtım paketinin çıktı klasörüne `download_size.json` adıyla kaydedilir. Dosya, tüm cihaz yapılandırmaları için bayt cinsinden en düşük ve en yüksek indirme boyutlarını ve her CPU mimarisi için aynı aralığı içerir:

```json
{
  "min" : 18208826,
  "max" : 25009450,
  "abis" : {
    "arm64-v8a" : { "min" : 25009448, "max" : 25009450 },
    "armeabi-v7a" : { "min" : 18208826, "max" : 18908828 }
  }
}
```

Komut satırından dağıtım paketi oluştururken rapor dosyasının yolunu `--download-size-report <path>` seçeneğiyle [Bob'a](/manuals/bob) geçirin. Bu, sürekli tümleştirmede oyununuzun indirme boyutunun zaman içindeki değişimini izlemek için yararlıdır.

Tahmin, Google Play'in dağıtım paketinizden oluşturacağı ve aynı anahtar deposuyla imzalanmış APK dosyalarından [bundletool](https://developer.android.com/tools/bundletool) kullanılarak hesaplanır. Bu dosyaları oluşturmak yaklaşık olarak *`.aab`* dosyasını oluşturmak kadar sürdüğünden tahmin varsayılan olarak kapalıdır. Tahmin başarısız olursa bir uyarı yazdırılır ve dağıtım paketi her zamanki gibi oluşturulur, ancak rapor dosyası yazılmaz.

:[Build Variants](../shared/build-variants.md)

### Android uygulaması dağıtım paketini kurma {#installing-an-android-application-bundle}

#### APK kurma {#installing-an-apk}

Bir *`.apk`* dosyası `adb` aracıyla cihazınıza veya [Google Play geliştirici konsolu](https://play.google.com/apps/publish/) üzerinden Google Play'e kopyalanabilir.

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Düzenleyiciyi kullanarak APK kurma {#installing-an-apk-using-editor}

Düzenleyicinin Bundle iletişim kutusundaki "Install on connected device" ve "Launch installed app" onay kutularını kullanarak bir *`.apk`* dosyasını kurup başlatabilirsiniz:

![APK kurma ve başlatma](images/android/install_and_launch.png)

Bu özelliğin çalışması için *ADB* kurulu olmalı ve bağlı cihazda *USB debugging* etkinleştirilmelidir. Düzenleyici ADB komut satırı aracının kurulum konumunu algılayamazsa bunu [Preferences](/manuals/editor-preferences/#tools) içinde belirtmeniz gerekir.

#### AAB kurma {#installing-an-aab}

Bir *.aab* dosyası [Google Play geliştirici konsolu](https://play.google.com/apps/publish/) üzerinden Google Play'e yüklenebilir. [Android bundletool](https://developer.android.com/studio/command-line/bundletool) kullanarak bir *.aab* dosyasından yerel olarak kurmak üzere bir *`.apk`* dosyası oluşturmak da mümkündür.

## Ekran kesikleri {#display-cutouts}

`window.get_reserved_areas()`, Android 9 (API düzeyi 28) ve sonraki sürümlerde ekran kesiklerinin dikdörtgenlerini bildirir. Güvenli bir yerleşim dikdörtgenine ihtiyaç duyduğunuzda `window.get_safe_area()` işlevini kullanın. Koordinat birimleri, desteklenmeyen platformlardaki davranış ve bildirilen alanlar değiştiğinde yerleşimi yenileme hakkında bilgi için [Ayrılmış ekran alanları](/manuals/porting-guidelines/#reserved-screen-areas) bölümüne bakın.

## R8 ile Java kodunu ve Android kaynaklarını küçültme {#shrinking-java-code-with-r8}

R8, küçültme, optimizasyon ve karartma (obfuscation) yoluyla Java kodunun boyutunu azaltır. Defold 1.14.0 veya sonraki sürümlerde, uyumlu bir Extender derleme sunucusuyla kullanıldığında eklentilerin ve Android bağımlılıklarının sağladığı yerleşimler (layout), çizilebilir kaynaklar (drawable) ve ham kaynaklar gibi kullanılmayan Android kaynaklarını da kaldırır. Oyun arşivindeki Defold oyun varlıkları R8 tarafından işlenmez.

### R8'i etkinleştirme {#enabling-r8}

*game.project* dosyasındaki **Android ▸ R8 Keep Rules** alanında `/builtins/manifests/android/dmengine.keep` dosyasını seçin. Bu, Defold'un varsayılan kurallarını doğrudan kullanır:

```ini
[android]
r8_keep_rules = /builtins/manifests/android/dmengine.keep
```

Java kodu içeren her eklentinin, çalışma sırasında ihtiyaç duyduğu sınıflar için bir `.keep` dosyası sağladığından emin olun. Eklenti kuralları, proje derlenirken seçili proje kurallarıyla birleştirilir. R8'i etkinleştirdikten sonra yayıma yönelik bir derlemeyi cihazda test edin.

**R8 Keep Rules** alanı boş bırakıldığında küçültme işlemi yapılmadan D8 kullanılır. R8 etkinleştirildiğinde, yerel kod eklentileri (native extension) olmayan bir projede bile yerel kod eklentisi derleme hizmeti kullanılır.

Android kaynaklarını küçültme işlemi de aynı **R8 Keep Rules** ayarıyla etkinleştirilir; bunun için ayrı bir proje ayarı yoktur. Eski Defold SDK'larında R8 küçültme işlemi yalnızca kodu kapsar.

### Bir eklentiye kurallar ekleme {#adding-rules-to-an-extension}

Bir eklentinin koruma kuralları, eklentinin `manifests/android` dizininde, `build.gradle` dosyasının yanında bulunur. Bir dosyanın nasıl ekleneceğini ve eklentinin Java sınıflarının nasıl korunacağını öğrenmek için [Android eklentileri için R8 koruma kuralları](/manuals/extensions/#r8-keep-rules-for-android) bölümüne bakın.

### Android kaynaklarını koruma {#keeping-android-resources}

Adlarıyla dinamik olarak aranan kaynaklar için açık koruma kuralları gerekebilir. Android kaynakları, Java sınıfları için kullanılan `.keep` kurallarından ayrı olarak `tools:keep` içeren bir XML dosyası kullanır. Örneğin bir eklenti, `/myextension/res/android/res/raw/com_example_myextension_keep.xml` dosyasını ekleyerek `dynamic_data` adlı bir ham kaynağı koruyabilir:

```xml
<resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@raw/dynamic_data" />
```

Çakışmaları önlemek için her eklentinin XML koruma dosyasına benzersiz bir dosya adı verin. `tools:keep` değeri, virgülle ayrılmış bir kaynak adı listesi kabul eder ve `*` joker karakterini destekler. Ayrıntılar için Android'in [kaynak koruma kuralları belgelerine](https://developer.android.com/topic/performance/app-optimization/customize-which-resources-to-keep) bakın. R8'i etkinleştirdikten sonra kaynakları dinamik olarak yükleyen özellikleri yayıma yönelik bir derlemede test edin.

### Karartma eşlemesini saklama {#keeping-the-obfuscation-mapping}

Derleme bir `mapping.txt` dosyası oluşturduğunda R8'in bu dosyasını saklamak için Android dağıtım paketi iletişim kutusunda **Generate debug symbols** seçeneğini etkinleştirin veya Bob'a `--with-symbols` seçeneğini geçirin. Örneğin, proje dizininden:

```sh
java -jar bob.jar --platform arm64-android --variant release \
  --archive --with-symbols --bundle-output build/android \
  resolve build bundle
```

Eşleme, oluşturulan APK veya AAB dosyasının yanına `<binary-name>.apk.symbols/mapping.txt` olarak kaydedilir. Örneğin, proje başlığı `My Game` olduğunda yukarıdaki komut `build/android/MyGame/MyGame.apk.symbols/mapping.txt` dosyasını oluşturur.

Eşleme dosyasını, oluşturulduğu sürümle birlikte saklayın. Bu dosya, yığın izlerini (stack trace) yorumlamak için karartılmış Java adlarını özgün adlarla eşler; farklı bir derlemeye ait eşleme yanlış sonuçlar verebilir.

## İzinler {#permissions}

Defold motoru, tüm motor özelliklerinin çalışabilmesi için çeşitli izinler gerektirir. İzinler, *game.project* [proje ayarları dosyasında](/manuals/project-settings/#android) belirtilen `AndroidManifest.xml` dosyasında tanımlanır. Android izinleri hakkında daha fazla bilgiyi [resmî belgelerden](https://developer.android.com/guide/topics/permissions/overview) edinebilirsiniz. Varsayılan bildirimde aşağıdaki izinler istenir:

### android.permission.INTERNET ve android.permission.ACCESS_NETWORK_STATE (Koruma düzeyi: normal) {#androidpermissioninternet-and-androidpermissionaccess_network_state-protection-level-normal}
Uygulamaların *ağ soketleri* açmasına ve ağlar hakkındaki bilgilere erişmesine izin verir. Bu izinler internet erişimi için gereklidir. ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) ve ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Koruma düzeyi: normal) {#androidpermissionwake_lock-protection-level-normal}
İşlemcinin uyumasını veya ekranın kararmasını önlemek için PowerManager WakeLocks kullanılmasına izin verir. Bu izin, bir anlık bildirim alınırken cihazın uyumasını geçici olarak önlemek için gereklidir. ([Android resmî belgeleri](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## AndroidX kullanma {#using-androidx}
AndroidX, artık bakımı yapılmayan özgün Android Support Library'ye kıyasla büyük bir iyileştirmedir. AndroidX paketleri, aynı özellikleri ve yeni kütüphaneleri sağlayarak Support Library'nin yerini tamamen alır. [Asset Portal](/assets) üzerindeki Android eklentilerinin çoğu AndroidX'i destekler. AndroidX kullanmak istemiyorsanız [uygulama bildiriminde](https://defold.com/manuals/app-manifest/) `Use Android Support Lib` seçeneğini işaretleyerek AndroidX'i açıkça devre dışı bırakıp eski Android Support Library'yi kullanabilirsiniz.

![](images/android/enable_supportlibrary.png)

## Sık sorulan sorular {#faq}
:[Android FAQ](../shared/android-faq.md)
