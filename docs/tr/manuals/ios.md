---
title: Defold ile iOS platformu için geliştirme
brief: Bu kılavuz, Defold'da iOS cihazları için oyun ve uygulama derlemeyi ve çalıştırmayı açıklar.
---

# iOS için geliştirme

::: sidenote
iOS için oyun paketleme yalnızca Defold düzenleyicisinin Mac sürümünde kullanılabilir.
:::

iOS, derlediğiniz ve telefonunuzda veya tabletinizde çalıştırmak istediğiniz _her_ uygulamanın Apple tarafından verilmiş bir sertifika ve sağlama profiliyle (provisioning profile) imzalanmasını _zorunlu kılar_. Bu kılavuz, oyununuzu iOS için paketlerken izlemeniz gereken adımları açıklar. Geliştirme sırasında oyununuzu [geliştirme uygulaması](/manuals/dev-app) üzerinden çalıştırmak genellikle tercih edilir; çünkü bu yöntem, içeriği ve kodu doğrudan cihazınızda çalışma sırasında yeniden yüklemenize (hot reload) olanak tanır.

## Apple'ın kod imzalama süreci

iOS uygulamalarının güvenliği birkaç bileşenden oluşur. [Apple'ın iOS Developer Program](https://developer.apple.com/programs/) programına kaydolarak gerekli araçlara erişebilirsiniz. Kaydolduktan sonra [Apple Developer Member Center](https://developer.apple.com/membercenter/index.action) sayfasına gidin.

![Apple Member Center](images/ios/apple_member_center.png)

*Certificates, Identifiers & Profiles* bölümü, ihtiyacınız olan tüm araçları içerir. Buradan aşağıdakileri oluşturabilir, silebilir ve düzenleyebilirsiniz:

Certificates
: Sizi geliştirici olarak tanımlayan, Apple tarafından verilmiş kriptografik sertifikalardır. Geliştirme veya üretim sertifikaları oluşturabilirsiniz. Geliştirici sertifikaları, uygulama içi satın alma mekanizması gibi belirli özellikleri yalıtılmış bir test ortamında denemenize olanak tanır. Üretim sertifikaları, App Store'a yüklenecek son uygulamayı imzalamak için kullanılır. Uygulamaları test amacıyla cihazınıza koymadan önce imzalamak için bir sertifikaya ihtiyacınız vardır.

Identifiers
: Çeşitli amaçlarla kullanılan tanımlayıcılardır. Birden çok uygulamayla kullanılabilen joker karakterli tanımlayıcılar (ör. `some.prefix.*`) kaydedebilirsiniz. App ID'ler, uygulamanın Passbook entegrasyonunu, Game Center'ı vb. etkinleştirip etkinleştirmediği gibi Application Service bilgilerini içerebilir. Bu tür App ID'ler joker karakterli tanımlayıcılar olamaz. Application Services işlevlerinin çalışması için uygulamanızın *paket tanımlayıcısı* (bundle identifier), App ID tanımlayıcısıyla eşleşmelidir.

Devices
: Her geliştirme cihazının kendi UDID değeriyle (Unique Device IDentifier, aşağıya bakın) kaydedilmesi gerekir.

Provisioning Profiles
: Sağlama profilleri, sertifikaları App ID'ler ve bir cihaz listesiyle ilişkilendirir. Hangi geliştiricinin hangi uygulamasının hangi cihazlarda bulunmasına izin verildiğini belirtir.

Defold'da oyunlarınızı ve uygulamalarınızı imzalarken geçerli bir sertifikaya ve geçerli bir sağlama profiline ihtiyacınız vardır.

::: sidenote
Member Center ana sayfasında yapabileceğiniz işlemlerin bazılarını, kuruluysa Xcode geliştirme ortamından da yapabilirsiniz.
:::

Cihaz tanımlayıcısı (UDID)
: Bir iOS cihazının UDID değerini bulmak için cihazı Wi-Fi veya kabloyla bir bilgisayara bağlayın. Xcode'u açın ve <kbd>Window ▸ Devices and Simulators</kbd> seçeneğini seçin. Cihazınızı seçtiğinizde seri numarası ve tanımlayıcısı görüntülenir.

  ![Xcode cihazları](images/ios/xcode_devices.png)

  Xcode kurulu değilse tanımlayıcıyı iTunes'da bulabilirsiniz. Cihazlar simgesine tıklayın ve cihazınızı seçin.

  ![iTunes cihazları](images/ios/itunes_devices.png)

  1. *Summary* sayfasında *Serial Number* alanını bulun.
  2. Alanın *UDID* olarak değişmesi için *Serial Number* alanına bir kez tıklayın. Art arda tıklarsanız cihazla ilgili çeşitli bilgiler gösterilir. *UDID* görünene kadar tıklamaya devam edin.
  3. Uzun UDID dizesine sağ tıklayın ve tanımlayıcıyı panoya kopyalamak için <kbd>Copy</kbd> seçeneğini seçin. Böylece cihazı Apple Developer Member Center'da kaydederken UDID alanına kolayca yapıştırabilirsiniz.

## Ücretsiz Apple geliştirici hesabıyla geliştirme

Xcode 7'den itibaren herkes Xcode'u kurup ücretsiz olarak cihaz üzerinde geliştirme yapabilir. iOS Developer Program programına kaydolmanız gerekmez. Bunun yerine Xcode, geliştirici olarak sizin için otomatik olarak bir sertifika (1 yıl geçerli) ve belirli cihazınızdaki uygulamanız için bir sağlama profili (bir hafta geçerli) oluşturur.

1. Cihazınızı bağlayın.
2. Xcode'u kurun.
3. Xcode'a yeni bir hesap ekleyin ve Apple ID'nizle giriş yapın.
4. Yeni bir proje oluşturun. En basit `Single View App` yeterlidir.
5. `Team` seçeneğini (sizin için otomatik oluşturulur) seçin ve uygulamaya bir paket tanımlayıcısı verin.

::: important
Defold projenizde aynı paket tanımlayıcısını kullanmanız gerektiğinden bu tanımlayıcıyı not edin.
:::

6. Xcode'un uygulama için bir *Provisioning Profile* ve *Signing Certificate* oluşturduğundan emin olun.

   ![](images/ios/xcode_certificates.png)

7. Uygulamayı cihazınızda derleyin. İlk seferde Xcode, Developer mode seçeneğini etkinleştirmenizi ister ve cihazı hata ayıklayıcı desteğiyle hazırlar. Bu işlem biraz zaman alabilir.
8. Uygulamanın çalıştığını doğruladıktan sonra uygulamayı diskinizde bulun. Derleme konumunu `Report Navigator` içindeki derleme raporunda görebilirsiniz.

   ![](images/ios/app_location.png)

9. Uygulamayı bulun, sağ tıklayın ve <kbd>Show Package Contents</kbd> seçeneğini seçin.

   ![](images/ios/app_contents.png)

10. `embedded.mobileprovision` dosyasını diskinizde daha sonra bulabileceğiniz bir yere kopyalayın.

   ![](images/ios/free_provisioning.png)

Bu sağlama dosyası, kod imzalama kimliğinizle birlikte Defold'da uygulamaları bir hafta boyunca imzalamak için kullanılabilir.

Sağlama dosyasının süresi dolduğunda uygulamayı Xcode'da yeniden derlemeniz ve yukarıda açıklandığı gibi yeni bir geçici sağlama dosyası almanız gerekir.

## iOS uygulama dağıtım paketi oluşturma {#creating-an-ios-application-bundle}

Kod imzalama kimliğini ve sağlama profilini edindikten sonra, düzenleyiciden oyununuz için bağımsız bir uygulama dağıtım paketi (bundle) oluşturmaya hazırsınız. Menüden <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> seçeneğini seçin.

![iOS dağıtım paketini imzalama](images/ios/sign_bundle.png)

Kod imzalama kimliğinizi seçin, mobil sağlama dosyanızı bulup seçin ve derleme çeşidini (Debug veya Release) belirleyin. İsterseniz `Sign application` onay kutusunun işaretini kaldırarak imzalama işlemini atlayabilir ve daha sonraki bir aşamada elle imzalayabilirsiniz. Cihaz dağıtım paketi yerine iOS Simulator için bir `arm64_sim-ios` dağıtım paketi oluşturmak üzere `Simulator` seçeneğini işaretleyin.

::: important
Simülatör dağıtım paketleri yalnızca Apple Silicon Mac'lerdeki iOS Simulator üzerinde çalışır. İmzalama kimliği veya sağlama profili kullanmadıklarından, `Simulator` işaretlendiğinde imzalama, kurma ve başlatma seçenekleri devre dışı bırakılır. Dağıtım paketini aşağıda açıklandığı gibi `xcrun simctl` ile kurun.
:::

*Create Bundle* düğmesine basın; ardından dağıtım paketinin bilgisayarınızda nerede oluşturulacağını belirtmeniz istenir.

![ipa iOS uygulama dağıtım paketi](images/ios/ipa_file.png){.left}

Uygulamada kullanılacak simgeyi, açılış ekranının arayüz taslağını (storyboard) ve benzeri ayarları *game.project* proje ayarları dosyasının [iOS bölümünde](/manuals/project-settings/#ios) belirtirsiniz.

### Özel Info.plist ve yerel hedef keşfi

Yerleşik iOS `Info.plist` dosyası, yayıma yönelik olmayan derlemelerde düzenleyicinin hedefleri otomatik keşfetmesi için gereken Bonjour hizmetini ve yerel ağ kullanım açıklamasını içerir. Özel bir `Info.plist`, bu yerleşik temel bildirimin yerini alır. Bir hata ayıklama derlemesinde özel bildirim kullanıyorsanız ve yerel ağ üzerinden hedef keşfine, profil çıkarmaya, çalışma sırasında yeniden yüklemeye veya günlük akışına ihtiyacınız varsa şu girdileri ekleyin:

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

Mustache koşulu, keşif girdilerinin yayıma yönelik dağıtım paketlerine dahil edilmesini önler. Kullanım açıklaması dizesi iOS tarafından kullanıcıya gösterilir ve düzenlenebilir veya yerelleştirilebilir. Koşulu yalnızca yayıma yönelik uygulamanın kendisi aynı Bonjour hizmetini ve yerel ağ işlevlerini kullanıyorsa kaldırın.

:[Build Variants](../shared/build-variants.md)

## Bağlı bir iPhone'a dağıtım paketi kurma ve başlatma

Derlenen dağıtım paketini, düzenleyicinin Bundle iletişim kutusundaki `Install on connected device` ve `Launch installed app` onay kutularını kullanarak kurabilir ve başlatabilirsiniz:

![iOS dağıtım paketini kurma ve başlatma](images/ios/install_and_launch.png)

Bu özelliğin çalışması için [ios-deploy](https://github.com/ios-control/ios-deploy) komut satırı aracının kurulu olması gerekir. Kurmanın en basit yolu Homebrew kullanmaktır:
```
$ brew install ios-deploy
```

Düzenleyici ios-deploy aracının kurulum konumunu algılayamazsa bu konumu [Preferences](/manuals/editor-preferences/#tools) bölümünde belirtmeniz gerekir. 

### Arayüz taslağı oluşturma {#creating-a-storyboard}

Arayüz taslağı dosyasını Xcode kullanarak oluşturursunuz. Xcode'u başlatın ve yeni bir proje oluşturun. iOS ve Single View App seçeneklerini seçin:

![Proje oluşturma](images/ios/xcode_create_project.png)

Next düğmesine tıklayıp projenizi yapılandırmaya devam edin. Product Name alanına bir ad girin:

![Proje ayarları](images/ios/xcode_storyboard_create_project_settings.png)

İşlemi tamamlamak için Create düğmesine tıklayın. Projeniz artık oluşturuldu; arayüz taslağını oluşturmaya geçebiliriz:

![Proje görünümü](images/ios/xcode_storyboard_project_view.png)

Bir görüntüyü projeye içe aktarmak için sürükleyip bırakın. Ardından `Assets.xcassets` öğesini seçin ve görüntüyü `Assets.xcassets` içine bırakın:

![Görüntü ekleme](images/ios/xcode_storyboard_add_image.png)

`LaunchScreen.storyboard` dosyasını açın ve artı düğmesine (<kbd>+</kbd>) tıklayın. ImageView bileşenini bulmak için iletişim kutusuna `imageview` yazın.

![Görüntü görünümü ekleme](images/ios/xcode_storyboard_add_imageview.png)

Image View bileşenini arayüz taslağına sürükleyin:

![Arayüz taslağına ekleme](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Daha önce `Assets.xcassets` içine eklediğiniz görüntüyü Image açılır listesinden seçin:

![](images/ios/xcode_storyboard_select_image.png)

Görüntüyü konumlandırın ve ihtiyaç duyduğunuz diğer ayarlamaları yapın; örneğin bir Label veya başka bir arayüz öğesi ekleyebilirsiniz. Bitirdiğinizde etkin şemayı **Any iOS Device (arm64)** (veya **Generic iOS Device**) olarak ayarlayın ve **Product ▸ Build** seçeneğini seçin. Defold, 64 bit cihazlarda iOS 15.0 ve sonraki sürümleri destekler; bu nedenle dağıtıma alma hedefini 15.0 veya daha yeni bir sürümde tutun. Derleme işleminin tamamlanmasını bekleyin.

Arayüz taslağında görüntü kullanırsanız bunlar `LaunchScreen.storyboardc` dosyanıza otomatik olarak dahil edilmez. Kaynakları dahil etmek için *game.project* dosyasındaki `Bundle Resources` alanını kullanın.
Örneğin, Defold projesinde `LaunchScreen` klasörünü ve bunun içinde `ios` klasörünü oluşturun (`ios` klasörü, bu dosyaların yalnızca iOS dağıtım paketlerine dahil edilmesi için gereklidir), ardından dosyalarınızı `LaunchScreen/ios/` içine koyun. Bu yolu `Bundle Resources` alanına ekleyin.

![](images/ios/bundle_res.png)

Son adım, derlenmiş `LaunchScreen.storyboardc` dosyasını Defold projenize kopyalamaktır. Finder'da aşağıdaki konumu açın ve `LaunchScreen.storyboardc` dosyasını Defold projenize kopyalayın:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
Forum kullanıcısı Sergey Lerg, [bu süreci gösteren bir video öğretici](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo) hazırladı.
:::

Arayüz taslağı dosyasını edindikten sonra *game.project* dosyasından ona başvurabilirsiniz.


### Simge varlık kataloğu oluşturma

Varlık kataloğu (asset catalog) kullanmak, uygulamanızın simgelerini yönetmek için Apple'ın tercih ettiği yöntemdir. Hatta App Store listelemesinde kullanılan simgeyi sağlamanın tek yolu budur. Varlık kataloğunu, arayüz taslağıyla aynı şekilde Xcode kullanarak oluşturursunuz. Xcode'u başlatın ve yeni bir proje oluşturun. iOS ve Single View App seçeneklerini seçin:

![Proje oluşturma](images/ios/xcode_create_project.png)

Next düğmesine tıklayıp projenizi yapılandırmaya devam edin. Product Name alanına bir ad girin:

![Proje ayarları](images/ios/xcode_icons_create_project_settings.png)

İşlemi tamamlamak için Create düğmesine tıklayın. Projeniz artık oluşturuldu; varlık kataloğunu oluşturmaya geçebiliriz:

![Proje görünümü](images/ios/xcode_icons_project_view.png)

Görüntüleri, desteklenen farklı simge boyutlarını temsil eden boş kutulara sürükleyip bırakın:

![Simge ekleme](images/ios/xcode_icons_add_icons.png)

::: sidenote
Notifications, Settings veya Spotlight için simge eklemeyin.
:::

Bitirdiğinizde etkin şemayı `Build -> Any iOS Device (arm64)`(veya `Generic iOS Device`) olarak ayarlayın ve <kbd>Product</kbd> -> <kbd>Build</kbd> seçeneğini seçin. Derleme işleminin tamamlanmasını bekleyin.

::: sidenote
`Any iOS Device (arm64)` veya `Generic iOS Device` için derlediğinizden emin olun; aksi halde derleme çıktınızı yüklerken `ERROR ITMS-90704` hatasını alırsınız.
:::

![Projeyi derleme](images/ios/xcode_icons_build.png)

Son adım, derlenmiş `Assets.car` dosyasını Defold projenize kopyalamaktır. Finder'da aşağıdaki konumu açın ve `Assets.car` dosyasını Defold projenize kopyalayın:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Varlık kataloğu dosyasını edindikten sonra *game.project* dosyasından kataloğa ve simgelere başvurabilirsiniz:

![game.project dosyasına simge ve varlık kataloğu ekleme](images/ios/defold_icons_game_project.png)

::: sidenote
App Store simgesine *game.project* dosyasından başvurmanız gerekmez. Simge, iTunes Connect'e yükleme sırasında `Assets.car` dosyasından otomatik olarak çıkarılır.
:::


## iOS uygulama dağıtım paketi kurma

Düzenleyici, iOS uygulama dağıtım paketi olan bir *.ipa* dosyası yazar. Dosyayı cihazınıza kurmak için aşağıdaki araçlardan birini kullanabilirsiniz:

* `Devices and Simulators` penceresi üzerinden Xcode
* [`ios-deploy`](https://github.com/ios-control/ios-deploy) komut satırı aracı
* macOS App Store'dan [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/)
* iTunes

Xcode üzerinden kullanılabilen iOS simülatörleriyle çalışmak için `xcrun simctl` komut satırı aracını da kullanabilirsiniz:

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## İhracat uygunluğu bilgileri

Oyununuzu App Store'a gönderirken oyununuzdaki şifreleme kullanımıyla ilgili ihracat uygunluğu bilgileri sağlamanız istenir. [Apple bunun neden gerekli olduğunu açıklıyor](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations):

"Uygulamanızı TestFlight'a veya App Store'a gönderdiğinizde uygulamanızı Amerika Birleşik Devletleri'ndeki bir sunucuya yüklersiniz. Uygulamanızı ABD veya Kanada dışında dağıtıyorsanız tüzel kişiliğinizin merkezinin nerede olduğuna bakılmaksızın uygulamanız ABD ihracat yasalarına tabidir. Uygulamanız şifreleme kullanıyor, şifrelemeye erişiyor, şifreleme içeriyor, uyguluyor veya bünyesine dahil ediyorsa bu, şifreleme yazılımı ihracatı olarak kabul edilir. Bu da uygulamanızın, dağıtımını yaptığınız ülkelerin ithalat uygunluğu gerekliliklerinin yanı sıra ABD ihracat uygunluğu gerekliliklerine de tabi olduğu anlamına gelir."

Defold oyun motoru, şifrelemeyi aşağıdaki amaçlarla kullanır:

* Güvenli kanallar üzerinden çağrı yapmak (ör. HTTPS ve SSL)
* Lua kodunun telif hakkını korumak (çoğaltılmasını önlemek için)

Defold motorundaki bu şifreleme kullanımları, Amerika Birleşik Devletleri ve Avrupa Birliği yasaları kapsamında ihracat uygunluğu belgesi gerekliliklerinden muaftır. Çoğu Defold projesi muaf kalır; ancak başka kriptografik yöntemlerin eklenmesi bu durumu değiştirebilir. Projenizin bu yasaların gerekliliklerini ve App Store kurallarını karşıladığından emin olmak sizin sorumluluğunuzdadır. Daha fazla bilgi için Apple'ın [İhracat uygunluğuna genel bakış](https://help.apple.com/app-store-connect/#/dev88f5c7bf9) belgesine bakın.

Projenizin muaf olduğunu düşünüyorsanız projenin `Info.plist` dosyasında [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) anahtarını `False` olarak ayarlayın. Daha fazla ayrıntı için [Uygulama bildirimleri](/manuals/extensions-manifest-merge-tool) kılavuzuna bakın.

## Sık sorulan sorular
:[iOS FAQ](../shared/ios-faq.md)
