---
title: Defold terim sözlüğü
brief: Bu kılavuz, Defold ile çalışırken karşılaşacağınız her şeyi kısa açıklamalarla listeler.
---

# Defold terim sözlüğü

Bu sözlük, Defold'da karşılaşacağınız her şeyin kısa bir açıklamasını verir. Çoğu maddede daha ayrıntılı belgelere giden bir bağlantı bulabilirsiniz.

## Animasyon kümesi

![Animasyon kümesi](images/icons/animationset.png){.left} Animasyon kümesi (animation set) kaynağı, animasyonların okunacağı glTF dosyalarının veya diğer .animationset dosyalarının bir listesini içerir. Birden fazla model arasında animasyon kümelerinin bir bölümünü paylaşıyorsanız bir .animationset dosyasını diğerine eklemek kullanışlıdır. Ayrıntılar için [model animasyonu kılavuzuna](/manuals/model-animation/) bakın.

## Atlas

![Atlas](images/icons/atlas.png){.left} Atlas, performans ve bellek kullanımı nedeniyle daha büyük bir sayfada birleştirilen ayrı görüntülerden oluşan bir kümedir. Atlaslar, sabit görüntüler veya kare dizisi animasyonu (flip-book animation) oluşturan görüntü dizileri içerebilir. Çeşitli bileşenler (component), grafik kaynaklarını paylaşmak için atlasları kullanır. Daha fazla bilgi için [atlas belgelerine](/manuals/atlas) bakın.

## Builtins

![Builtins](images/icons/builtins.png){.left} builtins proje klasörü, kullanışlı varsayılan kaynaklar içeren salt okunur bir klasördür. Burada varsayılan işleyiciyi (renderer), işleme betiğini (render script), materyalleri ve daha fazlasını bulabilirsiniz. Bu kaynaklardan herhangi birinde özel değişiklikler yapmanız gerekiyorsa kaynağı projenize kopyalayın ve uygun gördüğünüz şekilde düzenleyin.

## Kamera

![Kamera](images/icons/camera.png){.left} Kamera bileşeni (camera), oyun dünyasının hangi bölümünün görünür olacağını ve nasıl izdüşürüleceğini belirlemeye yardımcı olur. Yaygın bir kullanım, oyuncunun oyun nesnesine (game object) bir kamera eklemek veya bir yumuşatma algoritmasıyla oyuncuyu takip eden kameraya sahip ayrı bir oyun nesnesi kullanmaktır. Daha fazla bilgi için [kamera belgelerine](/manuals/camera) bakın.

## Çarpışma nesnesi

![Çarpışma nesnesi](images/icons/collision-object.png){.left} Çarpışma nesneleri (collision object), oyun nesnelerine fiziksel özellikler (uzamsal şekil, ağırlık, sürtünme ve geri sekme katsayısı gibi) ekleyen bileşenlerdir. Bu özellikler, çarpışma nesnesinin diğer çarpışma nesneleriyle nasıl çarpışacağını belirler. En yaygın çarpışma nesnesi türleri kinematik nesneler, dinamik nesneler ve tetikleyicilerdir. Kinematik nesne ayrıntılı çarpışma bilgileri sağlar ve çarpışmaya tepkiyi sizin uygulamanız gerekir; dinamik nesne ise Newton'un fizik yasalarına uyacak şekilde fizik motoru tarafından otomatik olarak simüle edilir. Tetikleyiciler, diğer şekillerin tetikleyiciye girip girmediğini veya tetikleyiciden çıkıp çıkmadığını algılayan basit şekillerdir. Bunun nasıl çalıştığına ilişkin ayrıntılar için [fizik belgelerine](/manuals/physics) bakın.

## Bileşen

Bileşenler, oyun nesnelerine grafik, animasyon, kodlanmış davranış ve ses gibi belirli bir görünüm ve/veya işlevsellik kazandırmak için kullanılır. Kendi başlarına var olamazlar; oyun nesnelerinin içinde bulunmaları gerekir. Defold'da birçok bileşen türü bulunur. Bileşenlerin açıklaması için [yapı taşları kılavuzuna](/manuals/building-blocks) bakın.

## Koleksiyon

![Koleksiyon](images/icons/collection.png){.left} Koleksiyonlar (collection), Defold'un oyun nesnesi hiyerarşilerinin yeniden kullanılabildiği şablonlar oluşturma mekanizmasıdır; diğer motorlarda bunlara "prefab" denir. Koleksiyonlar, oyun nesnelerini ve diğer koleksiyonları barındıran ağaç yapılarıdır. Bir koleksiyon her zaman dosyada saklanır ve düzenleyicide elle yerleştirilerek statik biçimde ya da çalışma sırasında oluşturularak dinamik biçimde oyuna eklenir. Koleksiyonların açıklaması için [yapı taşları kılavuzuna](/manuals/building-blocks) bakın.

## Koleksiyon fabrikası

![Koleksiyon fabrikası](images/icons/collection-factory.png){.left} Koleksiyon fabrikası (collection factory) bileşeni, çalışan bir oyunda oyun nesnesi hiyerarşilerini dinamik olarak oluşturmak için kullanılır. Ayrıntılar için [koleksiyon fabrikası kılavuzuna](/manuals/collection-factory) bakın.

## Koleksiyon vekili

![Koleksiyon](images/icons/collection.png){.left} Koleksiyon vekili (collection proxy), uygulama veya oyun çalışırken koleksiyonları anında yüklemek ve etkinleştirmek için kullanılır. Koleksiyon vekillerinin en yaygın kullanım amacı, bölümleri oynanacakları sırada yüklemektir. Ayrıntılar için [koleksiyon vekili belgelerine](/manuals/collection-proxy) bakın.

## Küp haritası

![Küp haritası](images/icons/cubemap.png){.left} Küp haritası (cubemap), bir küpün yüzlerine eşlenen 6 farklı dokudan oluşan özel bir doku türüdür. Gök kutularını (skybox) ve çeşitli yansıma ve aydınlatma haritalarını işlemek (rendering), yani görüntülerini oluşturmak için kullanışlıdır.

## Hata ayıklama

Bir noktada oyununuz beklenmedik şekilde davranacak ve sorunun ne olduğunu bulmanız gerekecektir. Hata ayıklamayı (debugging) öğrenmek bir sanattır; neyse ki Defold, size yardımcı olacak yerleşik bir hata ayıklayıcıyla gelir. Daha fazla bilgi için [hata ayıklama kılavuzuna](/manuals/debugging) bakın.

## Ekran profilleri

![Ekran profilleri](images/icons/display-profiles.png){.left} Ekran profilleri (display profiles) kaynak dosyası, yönelime, en boy oranına veya cihaz modeline bağlı GUI yerleşimlerini belirtmek için kullanılır. Kullanıcı arayüzünüzü her türlü cihaza uyarlamanıza yardımcı olur. [Yerleşimler kılavuzunda](/manuals/gui-layouts) daha fazla bilgi bulabilirsiniz.

## Fabrika

![Fabrika](images/icons/factory.png){.left} Bazı durumlarda gereken tüm oyun nesnelerini bir koleksiyona elle yerleştiremezsiniz; oyun nesnelerini dinamik olarak, çalışma sırasında oluşturmanız gerekir. Örneğin oyuncu mermi ateşleyebilir ve oyuncu tetiğe her bastığında her merminin dinamik olarak oluşturulup fırlatılması gerekir. Oyun nesnelerini dinamik olarak (önceden bellek ayrılmış bir nesne havuzundan) oluşturmak için fabrika (factory) bileşeni kullanırsınız. Ayrıntılar için [fabrika kılavuzuna](/manuals/factory) bakın.

## Yazı tipi

![Yazı tipi dosyası](images/icons/font.png){.left} Yazı tipi (font) kaynağı, bir TrueType veya OpenType yazı tipi dosyasından oluşturulur. Yazı tipi kaynağı, yazı tipinin hangi boyutta işleneceğini ve işlenen yazı tipinde hangi tür süslemelerin (dış çizgi ve gölge) bulunacağını belirtir. Yazı tipleri, GUI ve etiket bileşenleri tarafından kullanılır. Ayrıntılar için [yazı tipi kılavuzuna](/manuals/font/) bakın.

## Parça gölgelendiricisi

![Parça gölgelendiricisi](images/icons/fragment-shader.png){.left} Bu, bir çokgen ekrana çizilirken çokgendeki her piksel (parça) için grafik işlemcisinde çalıştırılan bir programdır. Parça gölgelendiricisinin (fragment shader) amacı, sonuçta oluşan her parçanın rengini belirlemektir. Bu işlem, hesaplamayla, dokudan bir veya daha fazla değer okumayla ya da değer okuma ve hesaplamanın birleşimiyle yapılır. Daha fazla bilgi için [gölgelendirici kılavuzuna](/manuals/shader) bakın.

## Oyun kumandaları

![Oyun kumandaları](images/icons/gamepad.png){.left} Oyun kumandaları (gamepads) kaynak dosyası, belirli bir oyun kumandası cihazından gelen girdinin belirli bir platformdaki oyun kumandası girdi tetikleyicileriyle nasıl eşleneceğini tanımlar. Ayrıntılar için [girdi kılavuzuna](/manuals/input) bakın.

## Oyun nesnesi

![Oyun nesnesi](images/icons/game-object.png){.left} Oyun nesneleri, oyununuzun çalışması sırasında ayrı yaşam sürelerine sahip basit nesnelerdir. Oyun nesneleri kapsayıcılardır ve genellikle ses veya sprite bileşeni gibi görsel ya da işitsel bileşenler içerir. Betik bileşenleri aracılığıyla davranış da kazanabilirler. Oyun nesnelerini düzenleyicide oluşturup koleksiyonlara yerleştirebilir veya fabrikalarla çalışma sırasında dinamik olarak oluşturabilirsiniz. Oyun nesnelerinin açıklaması için [yapı taşları kılavuzuna](/manuals/building-blocks) bakın.

## GUI

![GUI bileşeni](images/icons/gui.png){.left} GUI bileşeni, kullanıcı arayüzlerini oluşturmak için kullanılan öğeleri içerir: metinler ve renkli ve/veya dokulu bloklar. Öğeler hiyerarşik yapılarda düzenlenebilir, betiklerle yönetilebilir ve animasyonla canlandırılabilir. GUI bileşenleri genellikle oyun içi bilgi göstergeleri, menü sistemleri ve ekran bildirimleri oluşturmak için kullanılır. GUI bileşenleri, GUI davranışını tanımlayan ve kullanıcının onunla etkileşimini yöneten GUI betikleriyle kontrol edilir. [GUI belgelerinde](/manuals/gui) daha fazla bilgi bulabilirsiniz.

## GUI betiği

![GUI betiği](images/icons/script.png){.left} GUI betikleri (GUI script), GUI bileşenlerinin davranışını kontrol etmek için kullanılır. GUI animasyonlarını ve kullanıcının GUI ile nasıl etkileşim kurduğunu kontrol ederler. Lua betiklerinin Defold'da nasıl kullanıldığına ilişkin ayrıntılar için [Defold'da Lua kılavuzuna](/manuals/lua) bakın.

## Çalışma sırasında yeniden yükleme

Defold düzenleyicisi, masaüstünde ve cihazda zaten çalışmakta olan bir oyunun içeriğini güncellemenizi sağlar. Çalışma sırasında yeniden yükleme (hot reload) adı verilen bu özellik son derece güçlüdür ve geliştirme iş akışını büyük ölçüde iyileştirebilir. Daha fazla bilgi için [çalışma sırasında yeniden yükleme kılavuzuna](/manuals/hot-reload) bakın.

## Girdi eşlemesi

![Girdi eşlemesi](images/icons/input-binding.png){.left} Girdi eşlemesi (input binding) dosyaları, oyunun donanım girdisini (fare, klavye, dokunmatik ekran ve oyun kumandası) nasıl yorumlayacağını tanımlar. Dosya, donanım girdisini "jump" ve "move_forward" gibi üst düzey girdi _eylemlerine_ bağlar. Girdiyi dinleyen betik bileşenlerinde, belirli bir girdi karşısında oyunun veya uygulamanın gerçekleştirmesi gereken eylemleri kodlayabilirsiniz. Ayrıntılar için [girdi belgelerine](/manuals/input) bakın.

## Etiket

![Etiket](images/icons/label.png){.left} Etiket (label) bileşeni, herhangi bir oyun nesnesine metin içeriği eklemenizi sağlar. Belirli bir yazı tipiyle yazılmış bir metni, oyun uzayında ekrana işler. Daha fazla bilgi için [etiket kılavuzuna](/manuals/label) bakın.

## Kütüphane

![Oyun nesnesi](images/icons/builtins.png){.left} Defold, güçlü bir kütüphane (library) mekanizmasıyla projeler arasında veri paylaşmanızı sağlar. Bunu kullanarak kendiniz veya tüm ekibiniz için bütün projelerinizden erişilebilen ortak kütüphaneler oluşturabilirsiniz. Kütüphane mekanizması hakkında daha fazla bilgiyi [kütüphaneler belgelerinde](/manuals/libraries) bulabilirsiniz.

## Lua dili

Lua programlama dili, Defold'da oyun mantığı oluşturmak için kullanılır. Lua güçlü, verimli ve çok küçük bir betik dilidir. Yordamsal programlamayı, nesne yönelimli programlamayı, fonksiyonel programlamayı, veri odaklı programlamayı ve veri tanımlamayı destekler. Dil hakkında daha fazla bilgiyi https://www.lua.org/ adresindeki resmî Lua ana sayfasında ve [Defold'da Lua kılavuzunda](/manuals/lua) bulabilirsiniz.

## Lua modülü

![Lua modülü](images/icons/lua-module.png){.left} Lua modülleri, projenizi yapılandırmanızı ve yeniden kullanılabilir kütüphane kodu oluşturmanızı sağlar. [Lua modülleri kılavuzunda](/manuals/modules/) daha fazla bilgi bulabilirsiniz

## Materyal

![Materyal](images/icons/material.png){.left} Materyaller (material), gölgelendiricileri ve özelliklerini belirterek farklı nesnelerin nasıl işleneceğini tanımlar. Daha fazla bilgi için [materyal kılavuzuna](/manuals/material) bakın.

## İleti

Bileşenler, ileti aktarımı (message passing) aracılığıyla birbirleriyle ve diğer sistemlerle iletişim kurar. Bileşenler ayrıca kendilerini değiştiren veya belirli eylemleri tetikleyen önceden tanımlanmış bir ileti (message) kümesine yanıt verir. Grafikleri gizlemek veya fizik nesnelerini hafifçe itmek için iletiler gönderirsiniz. Motor da örneğin fizik şekilleri çarpıştığında, bileşenlere olayları bildirmek için iletileri kullanır. İleti aktarımı mekanizması, gönderilen her ileti için bir alıcıya ihtiyaç duyar. Bu nedenle oyundaki her şeyin benzersiz bir adresi vardır. Nesneler arasında iletişimi sağlamak için Defold, Lua'yı ileti aktarımıyla genişletir. Defold ayrıca kullanışlı işlevlerden oluşan bir kütüphane sunar.

Örneğin bir oyun nesnesindeki sprite bileşenini gizlemek için gereken Lua kodu şöyle görünür:

```lua
msg.post("#weapon", "disable")
```

Burada `"#weapon"`, geçerli nesnenin sprite bileşeninin adresidir. `"disable"` ise sprite bileşenlerinin yanıt verdiği bir iletidir. İleti aktarımının nasıl çalıştığına ilişkin ayrıntılı açıklama için [ileti aktarımı belgelerine](/manuals/message-passing) bakın.

## Model

![Model](images/icons/model.png){.left} 3B model bileşeni, glTF örgü, iskelet ve animasyon varlıklarını oyununuza içe aktarabilir. Daha fazla bilgi için [model kılavuzuna](/manuals/model/) bakın.

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Parçacıklar (particle), özellikle oyunlarda güzel görsel efektler oluşturmak için çok kullanışlıdır. Bunları sis, duman, ateş, yağmur veya düşen yapraklar oluşturmak için kullanabilirsiniz. Defold, efektleri oyununuzda gerçek zamanlı çalıştırırken oluşturmanıza ve ayarlamanıza olanak tanıyan güçlü bir parçacık efektleri düzenleyicisi içerir. [ParticleFX belgeleri](/manuals/particlefx), bunun nasıl çalıştığını ayrıntılarıyla açıklar.

## Profil çıkarma

Oyunlarda iyi performans çok önemlidir. Oyununuzu ölçmek, düzeltilmesi gereken performans darboğazlarını ve bellek sorunlarını belirlemek için performans ve bellek profili çıkarma (profiling) işlemini yapabilmeniz hayati önem taşır. Defold için sunulan profil çıkarma araçları hakkında daha fazla bilgi için [profil çıkarma kılavuzuna](/manuals/profiling) bakın.

## İşleme

![İşleme](images/icons/render.png){.left} İşleme dosyaları (render), oyun ekrana işlenirken kullanılan ayarları içerir. İşleme dosyaları, işleme için hangi işleme betiğinin ve hangi materyallerin kullanılacağını tanımlar. Daha fazla ayrıntı için [işleme kılavuzuna](/manuals/render/) bakın.

## İşleme betiği

![İşleme betiği](images/icons/script.png){.left} İşleme betiği, oyunun veya uygulamanın ekrana nasıl işleneceğini kontrol eden bir Lua betiğidir. En yaygın durumları kapsayan varsayılan bir işleme betiği bulunur; ancak özel aydınlatma modellerine ve başka efektlere ihtiyaç duyarsanız kendi betiğinizi yazabilirsiniz. İşleme hattının nasıl çalıştığına ilişkin daha fazla ayrıntı için [işleme kılavuzuna](/manuals/render/), Lua betiklerinin Defold'da nasıl kullanıldığına ilişkin ayrıntılar için [Defold'da Lua kılavuzuna](/manuals/lua) bakın.

## Betik

![Betik](images/icons/script.png){.left}  Betik (script), oyun nesnelerinin davranışlarını tanımlayan bir program içeren bileşendir. Betiklerle oyununuzun kurallarını ve nesnelerin çeşitli etkileşimlere (hem oyuncuyla hem de diğer nesnelerle) nasıl yanıt vereceğini belirleyebilirsiniz. Tüm betikler Lua programlama dilinde yazılır. Defold ile çalışabilmek için sizin veya ekibinizdeki birinin Lua'da programlama yapmayı öğrenmesi gerekir. Lua'ya genel bir bakış ve Lua betiklerinin Defold'da nasıl kullanıldığına ilişkin ayrıntılar için [Defold'da Lua kılavuzuna](/manuals/lua) bakın.

## Ses

![Ses](images/icons/sound.png){.left} Ses bileşeni (sound), belirli bir sesi çalmaktan sorumludur. Defold, WAV, Ogg Vorbis ve Ogg Opus dosyalarını destekler. Opus desteğinin App Manifest içinde etkinleştirilmesi gerekir. Daha fazla bilgi için [ses kılavuzuna](/manuals/sound) bakın.

## Sprite

![Sprite](images/icons/sprite.png){.left} Sprite, oyun nesnelerine grafik ekleyen bir bileşendir. Karo kaynağından veya atlastan alınan bir görüntüyü gösterir. Sprite bileşenleri, kare dizisi animasyonu ve kemik animasyonu için yerleşik desteğe sahiptir. Sprite bileşenleri genellikle karakterler ve eşyalar için kullanılır.

## Doku profilleri

![Doku profilleri](images/icons/texture-profiles.png){.left} Doku profilleri (texture profiles) kaynak dosyası, paketleme sürecinde görüntü verilerini (atlaslarda, karo kaynaklarında, küp haritalarında ve modeller, GUI vb. için kullanılan bağımsız dokularda) otomatik olarak işlemek ve sıkıştırmak için kullanılır. [Doku profilleri kılavuzunda](/manuals/texture-profiles) daha fazla bilgi bulabilirsiniz.

## Karo haritası

![Karo haritası](images/icons/tilemap.png){.left} Karo haritası (tile map) bileşenleri, karo kaynağındaki görüntüleri üst üste yerleştirilmiş bir veya daha fazla ızgarada gösterir. En yaygın kullanım alanları oyun ortamlarını oluşturmaktır: zemin, duvarlar, binalar ve engeller. Bir karo haritası, belirtilen bir harmanlama moduyla üst üste hizalanmış birden fazla katmanı gösterebilir. Bu, örneğin çimenli arka plan karolarının üzerine bitki örtüsü yerleştirmek için kullanışlıdır. Bir karoda gösterilen görüntüyü dinamik olarak değiştirmek de mümkündür. Böylece örneğin yalnızca karoları yıkılmış köprüyü gösteren ve karşılık gelen fizik şeklini içeren karolarla değiştirerek bir köprüyü yıkabilir ve geçilmez hâle getirebilirsiniz. Daha fazla bilgi için [karo haritası belgelerine](/manuals/tilemap) bakın.

## Karo kaynağı

![Karo kaynağı](images/icons/tilesource.png){.left} Karo kaynağı (tile source), her biri aynı boyutta olan birden fazla küçük görüntüden oluşan bir dokuyu tanımlar. Bir karo kaynağındaki görüntü dizisinden kare dizisi animasyonları tanımlayabilirsiniz. Karo kaynakları ayrıca görüntü verilerinden çarpışma şekillerini otomatik olarak hesaplayabilir. Bu, nesnelerin çarpışabileceği ve etkileşim kurabileceği karolardan oluşan bölümler hazırlamak için çok kullanışlıdır. Karo haritası bileşenleri (ayrıca Sprite ve ParticleFX), grafik kaynaklarını paylaşmak için karo kaynaklarını kullanır. Atlasların çoğu zaman karo kaynaklarından daha uygun olduğunu unutmayın. Daha fazla bilgi için [karo haritası belgelerine](/manuals/tilemap) bakın.

## Köşe gölgelendiricisi

![Köşe gölgelendiricisi](images/icons/vertex-shader.png){.left} Köşe gölgelendiricisi (vertex shader), bir bileşenin temel çokgen şekillerinin ekran geometrisini hesaplar. Sprite, karo haritası veya model gibi her türlü görsel bileşenin şekli, bir dizi çokgen köşesi konumuyla temsil edilir. Köşe gölgelendiricisi programı, her köşeyi (dünya uzayında) işler ve temel bir şeklin her köşesinin sonuçta sahip olması gereken koordinatı hesaplar. Daha fazla bilgi için [gölgelendirici kılavuzuna](/manuals/shader) bakın.
