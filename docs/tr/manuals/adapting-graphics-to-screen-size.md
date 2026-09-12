---
title: Grafikleri farklı ekran boyutlarına uyarlama
brief: Bu kılavuz, oyununuzu ve grafiklerinizi farklı ekran boyutlarına nasıl uyarlayacağınızı açıklar.
---

# Giriş

Oyununuzu ve grafiklerinizi farklı ekran boyutlarına uyarlarken dikkate almanız gereken birkaç nokta vardır:

* Bu, düşük çözünürlüklü, piksel düzeyinde tam hizalı (pixel-perfect) grafiklere sahip retro bir oyun mu, yoksa HD kalitesinde grafiklere sahip modern bir oyun mu?
* Oyun, farklı ekran boyutlarında tam ekran oynandığında nasıl davranmalı?
  * Oyuncu, yüksek çözünürlüklü bir ekranda oyun içeriğinin daha büyük bir bölümünü mü görmeli, yoksa grafikler her zaman aynı içeriği gösterecek şekilde yakınlaştırmayı uyarlamalı mı?
* Oyun, *game.project* dosyasında ayarladığınızdan farklı en boy oranlarını nasıl ele almalı?
  * Oyuncu, oyun içeriğinin daha büyük bir bölümünü mü görmeli? Belki siyah şeritler mi olmalı? Ya da GUI öğeleri yeniden mi boyutlandırılmalı?
* Ne tür menülere ve ekranda gösterilen GUI bileşenlerine (GUI component) ihtiyacınız var ve bunlar farklı ekran boyutlarına ve ekran yönelimlerine nasıl uyarlanmalı?
  * Yönelim değiştiğinde menüler ve diğer GUI bileşenleri yerleşimlerini değiştirmeli mi, yoksa yönelimden bağımsız olarak aynı yerleşimi korumalı mı?

Bu kılavuz, bu konuların bazılarını ele alır ve önerilen uygulamaları sunar.


## İçeriğinizin işlenme biçimini değiştirme

Defold işleme betiği (render script), grafiklerden görüntü oluşturmayı sağlayan işleme (rendering) hattının tamamı üzerinde tam denetim sağlar. İşleme betiği, çizim sırasının yanı sıra nelerin nasıl çizileceğine de karar verir. İşleme betiğinin varsayılan davranışı, pencere yeniden boyutlandırılsa veya gerçek ekran çözünürlüğü bu boyutlarla eşleşmese de her zaman *game.project* dosyasındaki genişlik ve yüksekliğin tanımladığı aynı piksel alanını çizmektir. Bunun sonucunda en boy oranı değişirse içerik esnetilir, pencere boyutu değişirse içerik yakınlaştırılır veya uzaklaştırılır. Bazı oyunlarda bu kabul edilebilir; ancak ekran çözünürlüğü veya en boy oranı farklı olduğunda büyük olasılıkla oyun içeriğinin daha fazla veya daha az bir bölümünü göstermek ya da en azından en boy oranını değiştirmeden içeriği yakınlaştırmak istersiniz. Varsayılan esnetme davranışı kolayca değiştirilebilir; bunun nasıl yapılacağı hakkında daha fazla bilgiyi [İşleme kılavuzunda](https://www.defold.com/manuals/render/#default-view-projection) bulabilirsiniz.


## Retro/8 bit grafikler

Retro/8 bit grafikler genellikle eski oyun konsollarının veya bilgisayarların düşük çözünürlüğünü ve sınırlı renk paletini içeren grafik tarzını taklit eden oyunları ifade eder. Örneğin Nintendo Entertainment System (NES) 256x240, Commodore 64 320x200 ve Gameboy 160x144 ekran çözünürlüğüne sahipti; bunların tümü modern ekranların boyutunun yalnızca küçük bir bölümüdür. Bu grafik tarzını ve ekran çözünürlüğünü taklit eden oyunların modern, yüksek çözünürlüklü bir ekranda oynanabilmesi için grafiklerin birkaç kat büyütülmesi veya yakınlaştırılması gerekir. Bunu yapmanın basit bir yolu, tüm grafiklerinizi taklit etmek istediğiniz düşük çözünürlükte ve tarzda çizmek ve işlenirken grafikleri yakınlaştırmaktır. Defold'da işleme betiğini kullanarak ve [Sabit izdüşümü](/manuals/render/#fixed-projection) uygun bir yakınlaştırma değerine ayarlayarak bunu kolayca yapabilirsiniz.

Bu karo kümesini (tileset) ve oyuncu karakterini ([kaynak](https://ansimuz.itch.io/grotto-escape-game-art-pack)) alıp 320x200 çözünürlüklü, 8 bitlik retro bir oyun için kullanalım:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

*game.project* dosyasında 320x200 ayarlayıp oyunu başlattığınızda görünüm şöyle olur:

![](images/screen_size/retro-original_320x200.png)

Pencere, modern ve yüksek çözünürlüklü bir ekranda gerçekten çok küçüktür! Pencere boyutunu dört katına, 1280x800 değerine çıkarmak, onu modern bir ekran için daha uygun hale getirir:

![](images/screen_size/retro-original_1280x800.png)

Pencere boyutu artık daha makul olduğuna göre grafikler için de bir şey yapmamız gerekiyor. Grafikler o kadar küçük ki oyunda neler olduğunu görmek çok zor. Sabit ve yakınlaştırılmış bir izdüşüm ayarlamak için işleme betiğini kullanabiliriz:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
Aynı sonuç, bir oyun nesnesine (game object) [kamera bileşeni](/manuals/camera/) ekleyip *Orthographic Projection* seçeneğini işaretleyerek ve *Orthographic Zoom* değerini 4.0 olarak ayarlayarak da elde edilebilir:

![](images/screen_size/retro-camera_zoom.png)
:::

Bu, aşağıdaki sonucu verir:

![](images/screen_size/retro-zoomed_1280x800.png)

Bu daha iyi. Hem pencerenin hem de grafiklerin boyutu uygun, ancak daha yakından baktığımızda belirgin bir sorun var:

![](images/screen_size/retro-zoomed_linear.png)

Grafikler bulanık görünüyor! Bunun nedeni, yakınlaştırılmış grafiklerin GPU tarafından işlenirken dokudan örneklenme biçimidir. *game.project* dosyasının *Graphics* bölümündeki varsayılan ayar *linear* değeridir:

![](images/screen_size/retro-settings_linear.png)

Bunu *nearest* olarak değiştirmek, istediğimiz sonucu verir:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

Artık retro oyunumuz için keskin, *piksel düzeyinde tam hizalı* grafiklerimiz var. *game.project* dosyasında sprite bileşenleri için alt pikselleri devre dışı bırakmak gibi dikkate alınması gereken başka noktalar da vardır:

![](images/screen_size/retro-subpixels.png)

*Subpixels* seçeneği devre dışı bırakıldığında sprite bileşenleri hiçbir zaman yarım piksel konumlarında işlenmez ve her zaman en yakın tam piksele hizalanır.

## Yüksek çözünürlüklü grafikler

Yüksek çözünürlüklü grafiklerle çalışırken proje ve içerik kurulumuna retro/8 bit grafiklerden farklı yaklaşmamız gerekir. Bit eşlem grafiklerde içeriğinizi, yüksek çözünürlüklü bir ekranda 1:1 ölçekte gösterildiğinde iyi görünecek şekilde oluşturmanız gerekir.

Retro/8 bit grafiklerde olduğu gibi işleme betiğini değiştirmeniz gerekir. Bu durumda grafiklerin, özgün en boy oranını korurken ekran boyutuyla birlikte ölçeklenmesini istersiniz:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

Bu, ekranın her zaman *game.project* dosyasında belirtilen miktarda içeriği gösterecek şekilde yeniden boyutlandırılmasını sağlar; en boy oranının farklı olup olmamasına bağlı olarak üstte ve altta ya da yanlarda ek içerik de gösterilebilir.

*game.project* dosyasındaki genişlik ve yüksekliği, oyun içeriğinizi ölçeklemeden göstermenize olanak tanıyan bir boyuta ayarlamanız önerilir.

### Yüksek DPI ayarı ve retina ekranlar

Yüksek çözünürlüklü retina ekranları da desteklemek isterseniz bunu *game.project* dosyasının Display bölümünde etkinleştirebilirsiniz:

![](images/screen_size/highdpi-enabled.png)

Bu, destekleyen ekranlarda yüksek DPI değerine sahip bir arka arabellek oluşturur. Oyun, Width ve Height ayarlarında belirtilen çözünürlüğün iki katında işlenir; bu ayarlar, betiklerde ve özelliklerde kullanılan mantıksal çözünürlüğü belirtmeye devam eder. Bu, tüm ölçülerin aynı kalacağı ve 1x ölçekte işlenen içeriğin aynı görüneceği anlamına gelir. Ancak yüksek çözünürlüklü görüntüleri içe aktarıp 0.5x ölçeğine küçültürseniz ekranda yüksek DPI değerinde görüntülenirler.


## Uyarlanabilir bir GUI oluşturma

GUI bileşenlerini oluşturma sistemi, temel yapı taşları olan [düğümler (node)](/manuals/gui/#node-types) üzerine kuruludur. Fazlasıyla basit görünse de düğmelerden karmaşık menülere ve açılır pencerelere kadar her şeyi oluşturmak için kullanılabilir. Oluşturduğunuz GUI'ler, ekran boyutu ve yönelim değişikliklerine otomatik olarak uyarlanacak şekilde yapılandırılabilir. Örneğin *düğümleri* ekranın üstüne, altına veya yanlarına sabitleyebilirsiniz; düğümler boyutlarını koruyabilir veya esneyebilir. *Düğümler* arasındaki ilişki, boyutları ve görünümleri de ekran boyutu veya yönelimi değiştiğinde değişecek şekilde yapılandırılabilir.

### *Düğüm* özellikleri

Bir GUI'deki her *düğümün* bir dayanak noktası (pivot), yatay ve dikey sabitleme noktaları (anchor) ve bir uyarlama modu (adjust mode) vardır.

* Dayanak noktası, düğümün merkez noktasını tanımlar.
* Sabitleme modu, sahnenin veya üst düğümün sınırları fiziksel ekran boyutuna sığacak şekilde esnetildiğinde düğümün dikey ve yatay konumunun nasıl değişeceğini denetler.
* Uyarlama modu ayarı, sahnenin veya üst düğümün sınırları fiziksel ekran boyutuna sığacak şekilde uyarlandığında düğüme ne olacağını denetler.

Bu özellikler hakkında daha fazla bilgiyi [GUI kılavuzunda](/manuals/gui/#node-properties) bulabilirsiniz.

### Yerleşimler

Defold, mobil cihazlarda ekran yönelimi değişikliklerine otomatik olarak uyarlanan GUI'leri destekler. Bu özelliği kullanarak farklı ekran boyutlarının yönelimine ve en boy oranına uyarlanabilen bir GUI tasarlayabilirsiniz. Belirli cihaz modelleriyle eşleşen yerleşimler oluşturmak da mümkündür. Bu sistem hakkında daha fazla bilgiyi [GUI yerleşimleri kılavuzunda](/manuals/gui-layouts/) bulabilirsiniz.


## Farklı ekran boyutlarını test etme

*Debug* menüsü, belirli bir cihaz modelinin çözünürlüğünü veya özel bir çözünürlüğü benzetmek için bir seçenek içerir. Uygulama çalışırken <kbd>Debug->Simulate Resolution</kbd> seçeneğini seçip listeden cihaz modellerinden birini seçebilirsiniz. Çalışan uygulamanın penceresi yeniden boyutlandırılır ve oyununuzun farklı bir çözünürlükte veya farklı bir en boy oranıyla nasıl göründüğünü görebilirsiniz.

![](images/screen_size/simulate-resolution.png)
