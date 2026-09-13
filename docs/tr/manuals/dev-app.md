---
title: Geliştirme uygulamasını cihazda çalıştırma
brief: Bu kılavuz, cihazda yinelemeli geliştirme yapmak için geliştirme uygulamasının cihazınıza nasıl kurulacağını açıklar.
---

# Mobil geliştirme uygulaması

Geliştirme uygulamasına (development app) Wi-Fi üzerinden içerik gönderebilirsiniz. Değişikliklerinizi test etmek istediğiniz her seferde paketleme ve kurulum yapmanız gerekmediği için bu, geliştirme döngülerinin süresini büyük ölçüde kısaltır. Geliştirme uygulamasını cihazlarınıza kurun, uygulamayı başlatın ve ardından düzenleyicide cihazı derleme hedefi olarak seçin.

## Geliştirme uygulamasını kurma

Debug modunda paketlenen herhangi bir iOS veya Android uygulaması, geliştirme uygulaması olarak kullanılabilir. Aslında önerilen çözüm budur; çünkü geliştirme uygulaması doğru proje ayarlarına sahip olur ve üzerinde çalıştığınız projeyle aynı [yerel kod eklentilerini (native extensions)](/manuals/extensions/) kullanır. 

Projenizin Debug çeşidini hiçbir içerik olmadan paketleyebilirsiniz. Uygulamanızın yerel kod eklentileri içeren ve bu kılavuzda anlatılan yinelemeli geliştirmeye uygun bir sürümünü oluşturmak için bu seçeneği kullanın.

![İçeriksiz dağıtım paketi](images/dev-app/contentless-bundle.png)

### iOS üzerinde kurma

iOS için dağıtım paketi oluşturmak üzere [iOS kılavuzundaki yönergeleri](/manuals/ios/#creating-an-ios-application-bundle) izleyin. Derleme çeşidi olarak Debug seçtiğinizden emin olun!

### Android üzerinde kurma

Android için dağıtım paketi oluşturmak üzere [Android kılavuzundaki yönergeleri](https://defold.com/manuals/android/#creating-an-android-application-bundle) izleyin.

## Oyununuzu başlatma

Oyununuzu cihazınızda başlatmak için geliştirme uygulaması ile düzenleyicinin aynı Wi-Fi ağı üzerinden veya USB kullanarak birbirine bağlanabilmesi gerekir (aşağıya bakın).

1. Düzenleyicinin açık ve çalışır durumda olduğundan emin olun.
2. Cihazda geliştirme uygulamasını başlatın.
3. Düzenleyicide <kbd>Project ▸ Targets</kbd> altında cihazınızı seçin.
4. Oyunu çalıştırmak için <kbd>Project ▸ Build</kbd> seçeneğini seçin. Oyun içeriği ağ üzerinden cihaza aktarıldığı için oyunun başlaması biraz zaman alabilir.
5. Oyun çalışırken her zamanki gibi [çalışma sırasında yeniden yükleme (hot reload)](/manuals/hot-reload/) özelliğini kullanabilirsiniz.

### Windows'ta USB kullanarak bir iOS cihazına bağlanma

Windows'ta, bir iOS cihazında çalışan geliştirme uygulamasına USB üzerinden bağlanırken önce [iTunes'u kurmanız](https://www.apple.com/lae/itunes/download/) gerekir. iTunes kurulduktan sonra iOS cihazınızda Settings menüsünden [Personal Hotspot seçeneğini etkinleştirmeniz](https://support.apple.com/en-us/HT204023) de gerekir. "Trust This Computer?" yazan bir uyarı görürseniz Trust seçeneğine dokunun. Geliştirme uygulaması çalışırken cihazın artık <kbd>Project ▸ Targets</kbd> altında görünmesi gerekir.

### Linux'ta USB kullanarak bir iOS cihazına bağlanma

Linux'ta USB kullanarak bağlandığınızda cihazınızdaki Settings menüsünden Personal Hotspot seçeneğini etkinleştirmeniz gerekir. "Trust This Computer?" yazan bir uyarı görürseniz Trust seçeneğine dokunun. Geliştirme uygulaması çalışırken cihazın artık <kbd>Project ▸ Targets</kbd> altında görünmesi gerekir.

### macOS'ta USB kullanarak bir iOS cihazına bağlanma

Yeni iOS sürümlerinde, macOS'ta USB kullanarak bağlandığınızda cihaz, kendisiyle bilgisayar arasında otomatik olarak yeni bir Ethernet arayüzü açar. Geliştirme uygulaması çalışırken cihazın <kbd>Project ▸ Targets</kbd> altında görünmesi gerekir.

Eski iOS sürümlerinde, macOS'ta USB kullanarak bağlandığınızda cihazınızdaki Settings menüsünden Personal Hotspot seçeneğini etkinleştirmeniz gerekir. "Trust This Computer?" yazan bir uyarı görürseniz Trust seçeneğine dokunun. Geliştirme uygulaması çalışırken cihazın artık <kbd>Project ▸ Targets</kbd> altında görünmesi gerekir.

### macOS'ta USB kullanarak bir Android cihazına bağlanma

macOS'ta, cihaz USB Tethering Mode durumundayken Android cihazında çalışan geliştirme uygulamasına USB üzerinden bağlanabilirsiniz. macOS'ta [HoRNDIS](https://joshuawise.com/horndis#available_versions) gibi üçüncü taraf bir sürücü kurmanız gerekir. HoRNDIS kurulduktan sonra Security & Privacy ayarları üzerinden çalışmasına izin vermeniz de gerekir. USB Tethering etkinleştirildiğinde, geliştirme uygulaması çalışırken cihaz <kbd>Project ▸ Targets</kbd> altında görünür.

### Windows veya Linux'ta USB kullanarak bir Android cihazına bağlanma

Windows ve Linux'ta, cihaz USB Tethering Mode durumundayken Android cihazında çalışan geliştirme uygulamasına USB üzerinden bağlanabilirsiniz. USB Tethering etkinleştirildiğinde, geliştirme uygulaması çalışırken cihaz <kbd>Project ▸ Targets</kbd> altında görünür.

## Sorun giderme

Uygulama indirilemiyor
: Cihazınızın UDID değerinin, uygulamayı imzalamak için kullanılan mobil sağlama profilinde bulunduğundan emin olun.

Cihazınız Targets menüsünde görünmüyor
: Cihazınızın bilgisayarınızla aynı Wi-Fi ağına bağlı olduğundan emin olun. Geliştirme uygulamasının Debug modunda derlendiğinden emin olun.

Oyun başlamıyor ve sürümlerin uyuşmadığını belirten bir ileti gösteriliyor
: Bu durum, düzenleyiciyi en son sürüme yükselttiğinizde ortaya çıkar. Yeni bir sürüm derleyip kurmanız gerekir.
