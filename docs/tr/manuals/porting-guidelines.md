---
title: Platformlara taşıma ve yayımlama yönergeleri
brief: Bu kılavuz, bir oyunu yeni bir platforma taşırken veya ilk kez yayımlarken dikkat edilmesi gereken bazı noktaları ele alır.
---

# Platformlara taşıma ve yayımlama yönergeleri

Bu sayfa, bir oyunu yayımlarken veya yeni bir platforma taşırken (porting) dikkat edilmesi gereken noktalar için yararlı bir kılavuz ve kontrol listesi sunar.

Bir Defold oyununu yeni bir platforma taşımak veya ilk kez yayımlamak genellikle basit bir süreçtir. Teoride ilgili bölümlerin *game.project* dosyasında yapılandırıldığından emin olmak yeterlidir; ancak her platformdan en iyi şekilde yararlanmak için oyunu o platformun özelliklerine uyarlamanız önerilir.


## Girdi
Oyunu platformun girdi (input) yöntemlerine uyarladığınızdan emin olun. Platform destekliyorsa [oyun kumandası (gamepad)](/manuals/input-gamepads) desteği eklemeyi değerlendirin! Ayrıca oyunun bir duraklatma menüsünü desteklediğinden emin olun - bir oyun kumandasının bağlantısı aniden kesilirse oyunun duraklatılması gerekir!

## Yerelleştirme
Oyundaki tüm metinleri çevirin. Avrupa ve Amerika kıtalarında yayımlamak için en azından EFIGS dillerine (İngilizce, Fransızca, İtalyanca, Almanca ve İspanyolca) çevirmeyi değerlendirin. Oyun içinde (duraklatma menüsünden) farklı diller arasında kolayca geçiş yapılabildiğinden emin olun.

::: important
Yalnızca iOS için - [Localizations](/manuals/project-settings/#localizations) ayarını `game.project` dosyasında belirttiğinizden emin olun; çünkü `sys.get_info()` bu listede bulunmayan bir dili hiçbir zaman döndürmez.
:::

Mağaza sayfasındaki metinleri çevirin; bu, satışları olumlu etkileyecektir! Bazı platformlar, mağaza sayfasındaki metinlerin oyunun sunulduğu her ülkenin diline çevrilmesini zorunlu tutar.

## Mağaza materyalleri

### Uygulama simgesi
Oyununuzun rakiplerinden ayrıştığından emin olun. Simge, potansiyel oyuncularla çoğu zaman ilk temas noktanızdır. Oyun simgeleriyle dolu bir sayfada kolayca bulunabilmelidir.

### Mağaza afişleri ve görselleri
Oyununuz için etkileyici ve heyecan verici görseller kullandığınızdan emin olun. Oyuncuların ilgisini çeken görseller oluşturmak için bir sanatçıyla çalışmaya biraz para harcamak muhtemelen buna değer.


## Oyun kayıtları

### Masaüstünde, mobilde ve web üzerinde oyun kayıtları
Oyun kayıtları ve kaydedilen diğer durum verileri, Defold API işlevi `sys.save(filename, data)` kullanılarak kaydedilebilir ve `sys.load(filename)` kullanılarak yüklenebilir. Dosyaların kaydedilebileceği, işletim sistemine özgü bir konumun yolunu almak için `sys.get_save_file(application_id, name)` işlevini kullanabilirsiniz; bu konum genellikle oturum açmış kullanıcının ev klasöründedir.

### Konsolda oyun kayıtları
Çoğu platformda `sys.get_save_file()` ve `sys.save()` kullanmak iyi sonuç verir; ancak konsollarda farklı bir yaklaşım benimsemeniz önerilir. Konsol platformları genellikle bağlı her oyun kumandasını bir kullanıcıyla ilişkilendirir; bu nedenle oyun kayıtlarının, başarımların ve diğer özelliklerin de ilgili kullanıcıyla ilişkilendirilmesi önerilir.

Oyun kumandası girdi olayları (input event), kumandanın eylemlerini konsoldaki bir kullanıcıyla ilişkilendirmek için kullanılabilecek bir kullanıcı kimliği içerir.

Konsol platformları ve bunların yerel kod eklentileri (native extension), belirli bir kullanıcıyla ilişkili verileri kaydetmek ve yüklemek için platforma özgü API işlevleri sunar. Konsolda kayıt ve yükleme yaparken bu API'leri kullanın.

Konsol platformlarının dosya işlemlerine yönelik API'leri genellikle eşzamansızdır (asynchronous). Konsolu da hedefleyen çok platformlu bir oyun geliştirirken, platformdan bağımsız olarak tüm dosya işlemleri eşzamansız olacak şekilde oyununuzu tasarlamanız önerilir. Örnek:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Derleme çıktıları

Çökmelerde hata ayıklayabilmek için yayımlanan her sürümde [hata ayıklama sembolleri oluşturduğunuzdan](/manuals/debugging-native-code/#symbolicate-a-callstack) emin olun. Bunları uygulamanın dağıtım paketiyle (bundle) birlikte saklayın.

## Uygulama optimizasyonları

Uygulamanızı performans, boyut, bellek ve pil kullanımı açısından nasıl optimize edeceğinizi öğrenmek için [Optimizasyon kılavuzunu](/manuals/optimization) okuyun.



## Performans
Her zaman hedef donanımda test edin! Oyun performansını kontrol edin ve gerekirse optimize edin. Koddaki darboğazları bulmak için [profil çıkarıcıyı (profiler)](/manuals/profiling) kullanın.


## Ekran çözünürlüğü ve yenileme hızı
Yönelimi ve ekran çözünürlüğü sabit olan platformlarda: Oyunun hedef platformun ekran çözünürlüğünde ve en boy oranında çalıştığını kontrol edin. Ekran çözünürlüğü ve en boy oranı değişken olan platformlarda: Oyunun çeşitli ekran çözünürlüklerinde ve en boy oranlarında çalıştığını kontrol edin. Görüntü oluşturmayı yöneten işleme betiğinde (render script) ve kamerada kullanılan [görünüm izdüşümünün (view projection)](/manuals/render/#default-view-projection) türünü dikkate alın.

Mobil platformlarda ya ekran yönelimini *game.project* dosyasında kilitleyin ya da oyunun hem yatay hem de dikey modda çalıştığından emin olun.

* **Ekran boyutları** - *game.project* dosyasında ayarlanan varsayılan genişlik ve yükseklikten daha büyük veya daha küçük bir ekranda her şey iyi görünüyor mu?
  * İşleme betiğinde kullanılan izdüşüm ve GUI'de kullanılan yerleşimler burada rol oynar.
* **En boy oranları** - *game.project* dosyasında ayarlanan genişlik ve yüksekliğin belirlediği varsayılan en boy oranından farklı bir en boy oranına sahip ekranda her şey iyi görünüyor mu?
  * İşleme betiğinde kullanılan izdüşüm ve GUI'de kullanılan yerleşimler burada rol oynar.
* **Yenileme hızı** - Oyun, yenileme hızı 60 Hz'den yüksek olan bir ekranda iyi çalışıyor mu?
  * vsync ve swap interval (*game.project* dosyasının Display bölümünde) 


## Cep telefonları, çentikler ve ekran içi kamera delikleri
Ön kameraya ve sensörlere yer açmak için ekranda küçük bir lens açıklığı (çentik veya ekran içi kamera deliği olarak da bilinir) kullanmak giderek yaygınlaşmıştır. Bir oyunu mobile taşırken kritik bilgilerin platformun güvenli alanı (safe area) içinde kaldığından emin olun.

Defold, Android ve iOS'ta yerleşik güvenli alan desteğine sahiptir. Hangi karşılıklı güvenli alan kenar paylarının (insets) GUI uyarlamasını etkileyeceğini belirlemek için `gui.safe_area_mode` ayarını *game.project* dosyasında yapılandırın. Varsayılan değer olan `none`, kenar paylarını yok sayar; `long`, yatay modda sol/sağ, dikey modda üst/alt kenar paylarını uygular; `short`, diğer çifti uygular; `both` ise dört kenarın tümünü uygular. Bir GUI betiği, [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode) ile kendi sahnesi için proje genelindeki modu geçersiz kılabilir. Özel GUI veya işleme (rendering) mantığı için [`window.get_safe_area()`](/ref/window/#window.get_safe_area), güvenli dikdörtgeni ve her bir kenarın payını döndürür. Yerleşik güvenli alan kenar payları olmayan platformlar, pencerenin tamamını ve sıfır kenar payı döndürür.

[Safe Area eklentisi](/extension-safearea), eski projeler veya yerleşik API'lerin sunduğunun ötesinde davranışa ihtiyaç duyan iş akışları için bir alternatif olmaya devam eder; Android ve iOS'ta standart güvenli alan yönetimi için gerekli değildir.


## Platforma özgü yönergeler

### Android
Oyununuzu güncelleyebilmek için [anahtar deponuzu (keystore)](/manuals/android/#creating-a-keystore) güvenli bir yerde sakladığınızdan emin olun.


### Konsollar
Her sürümün dağıtım paketini eksiksiz saklayın. Oyuna yama uygulamak isterseniz bu dosyalara ihtiyacınız olacaktır.


### Nintendo Switch
Platforma özgü kodu entegre edin - Nintendo Switch için kullanıcı seçimi gibi işlemlerde yardımcı olan bazı işlevleri içeren ayrı bir eklenti vardır.

Nintendo Switch için Defold, grafik arka ucu (graphics backend) olarak Vulkan kullanır - Oyunu [Vulkan grafik arka ucunu](https://github.com/defold/extension-vulkan) kullanarak test ettiğinizden emin olun.


### PlayStation®4
Platforma özgü kodu entegre edin - PlayStation®4 için kullanıcı seçimi gibi işlemlerde yardımcı olan bazı işlevleri içeren ayrı bir eklenti vardır.


### HTML5
Cep telefonlarında web oyunları oynamak giderek yaygınlaşıyor - Oyunun mobil tarayıcılarda da iyi çalışmasını sağlamaya çalışın! Web oyunlarının hızlı yüklenmesinin beklendiğini de akılda tutmak önemlidir! - Oyunu boyut açısından optimize ettiğinizden emin olun. Oyuncuları gereksiz yere kaybetmemek için genel yükleme deneyimini de göz önünde bulundurun.

2018'de tarayıcılar, bir kullanıcı etkileşimi olayı (dokunma, düğme, oyun kumandası vb.) gerçekleşene kadar oyunların ve diğer web içeriklerinin ses çalmasını engelleyen bir otomatik oynatma politikası getirdi. HTML5'e taşırken bunu dikkate almak ve sesleri ve müziği yalnızca ilk kullanıcı etkileşiminde çalmaya başlamak önemlidir. Herhangi bir kullanıcı etkileşiminden önce ses çalma girişimleri, tarayıcının geliştirici konsoluna hata olarak kaydedilir; ancak oyunu etkilemez.

Ayrıca oyun reklam gösteriyorsa çalmakta olan tüm sesleri duraklattığınızdan emin olun.
