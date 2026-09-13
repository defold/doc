---
title: Defold'da reklam gösterme
brief: Çeşitli reklam türleri göstermek, web ve mobil oyunlardan gelir elde etmenin yaygın bir yoludur. Bu kılavuz, reklamları kullanarak oyununuzdan gelir elde etmenin çeşitli yollarını gösterir.
---

# Reklamlar

Reklamlar, web ve mobil oyunlardan gelir elde etmenin çok yaygın bir yolu haline gelmiş ve milyar dolarlık bir sektöre dönüşmüştür. Bir geliştirici olarak, oyununuzda gösterdiğiniz reklamları izleyen kişi sayısına göre ödeme alırsınız. Genellikle denklem basittir: daha fazla izleyici, daha fazla para demektir; ancak ne kadar ödeme alacağınızı başka etkenler de belirler:

* Reklam kalitesi - oyuncularınızın kendilerine uygun reklamlarla etkileşime girme ve bu reklamlara dikkat etme olasılığı daha yüksektir.
* Reklam biçimi - bant reklamlar genellikle daha az kazandırırken baştan sona izlenen tam ekran reklamlar daha fazla kazandırır.
* Reklam ağı - aldığınız ödeme tutarı reklam ağından reklam ağına değişir.

::: sidenote
CPM = Bin gösterim başına maliyet (Cost per mille). Bir reklamverenin bin gösterim için ödediği tutardır. CPM, reklam ağlarına ve reklam biçimlerine göre değişir.
:::

## Biçimler

Oyunlarda kullanılabilecek birçok farklı reklam biçimi vardır. Daha yaygın olanlardan bazıları bant reklamlar (banner ads), geçiş reklamları (interstitial ads) ve ödüllü reklamlardır (rewarded ads):

### Bant reklamlar

Bant reklamlar metin, görüntü veya video tabanlıdır ve genellikle ekranın üst veya alt kısmında, ekranın görece küçük bir bölümünü kaplar. Bant reklamların uygulamaya eklenmesi çok kolaydır ve ekranın bir bölümünü reklamlara ayırmanın kolay olduğu, tek ekranlı gündelik oyunlara çok iyi uyar. Bant reklamlar, kullanıcılar oyununuzu kesintisiz oynarken reklam görünürlüğünü en üst düzeye çıkarır.

### Geçiş reklamları

Geçiş reklamları, animasyonlar ve bazen etkileşimli *zengin medya (rich media)* içeriği barındıran, tüm ekranı kaplayan büyük reklam deneyimleridir. Geçiş reklamları genellikle bölümler veya oyun oturumları arasında gösterilir; çünkü bunlar oyun deneyimindeki doğal ara noktalardır. Geçiş reklamları genellikle bant reklamlardan daha az gösterim alır, ancak maliyetleri (CPM) bant reklamlara göre çok daha yüksektir ve bu da toplamda önemli bir reklam geliri sağlar.

### Ödüllü reklamlar

Ödüllü reklamlar (teşvikli reklamlar olarak da bilinir) isteğe bağlıdır ve bu nedenle diğer birçok reklam biçimine göre daha az rahatsız edicidir. Ödüllü reklamlar, geçiş reklamları gibi genellikle tam ekran deneyimleridir. Kullanıcı, reklamı izleme karşılığında bir ödül seçebilir; örneğin *ganimet*, oyun parası, can, süre ya da başka bir oyun içi para birimi veya avantaj. Ödüllü reklamlar genellikle en yüksek maliyete (CPM) sahiptir, ancak gösterim sayısı doğrudan kullanıcıların reklam izlemeyi kabul etme oranlarıyla ilişkilidir. Ödüllü reklamlar ancak ödüller yeterince değerliyse ve doğru zamanda sunuluyorsa yüksek performans sağlar.


## Reklam ağları

[Defold Asset Portal](/tags/stars/ads/), reklam sağlayıcılarıyla bütünleşen çeşitli varlıklar (assets) içerir:

* [AdMob](https://defold.com/assets/admob-defold/) - Google AdMob ağını kullanarak reklam gösterin.
* [AppLovin MAX](https://defold.com/extension-applovin/) - AppLovin MAX reklam uyumlulaştırmasını kullanarak reklam gösterin.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Facebook Instant Game oyununuzda reklam gösterin.
* [LevelPlay](https://defold.com/extension-levelplay/) - Unity LevelPlay reklam uyumlulaştırmasını kullanarak reklam gösterin.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Unity Ads ağını kullanarak reklam gösterin.


# Oyununuzda reklamları bütünleştirme

Oyununuzda bütünleştireceğiniz reklam ağına karar verdiğinizde, ilgili *varlığın* kurulum ve kullanım yönergelerini izlemeniz gerekir. Genellikle ilk olarak eklentiyi bir [proje bağımlılığı](/manuals/libraries/#setting-up-library-dependencies) olarak eklersiniz. Varlığı projenize ekledikten sonra bütünleştirmeye devam edebilir ve reklamları yükleyip göstermek için varlığa özgü işlevleri çağırabilirsiniz.


# Reklamlarla uygulama içi satın almaları birleştirme

Mobil oyunlarda reklamları kalıcı olarak kaldırmak için [uygulama içi satın alma](/manuals/iap) sunmak oldukça yaygındır.


## Daha fazla bilgi

Reklam gelirini optimize etmeyi öğrenebileceğiniz birçok çevrimiçi kaynak vardır:

* Google AdMob [Reklamlarla mobil oyunlardan gelir elde etme](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popüler reklam biçimleri ve bunların kullanımı](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Oyunlarda reklam sunumu: 10 uzman önerisi](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
