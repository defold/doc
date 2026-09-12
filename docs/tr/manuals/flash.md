---
title: Flash kullanıcıları için Defold
brief: Bu kılavuz, Defold'u Flash oyunu geliştiricileri için bir alternatif olarak tanıtır. Flash ile oyun geliştirmede kullanılan bazı temel kavramları ele alır ve bunlara karşılık gelen Defold araçlarını ve yöntemlerini açıklar.
---

# Flash kullanıcıları için Defold

Bu kılavuz, Defold'u Flash oyunu geliştiricileri için bir alternatif olarak tanıtır. Flash ile oyun geliştirmede kullanılan bazı temel kavramları ele alır ve bunlara karşılık gelen Defold araçlarını ve yöntemlerini açıklar.

## Giriş

Flash'ın başlıca avantajlarından bazıları erişilebilirliği ve kullanmaya başlamanın kolaylığıydı. Yeni kullanıcılar programı hızla öğrenebilir ve az zaman ayırarak temel oyunlar oluşturmaya başlayabilirdi. Defold, oyun tasarımına özel bir araç kümesi sunarak benzer bir avantaj sağlar; aynı zamanda deneyimli geliştiricilerin daha karmaşık gereksinimler için gelişmiş çözümler oluşturmasına olanak tanır (örneğin geliştiricilerin varsayılan işleme betiğini (render script) düzenlemesine izin vererek).

Flash oyunları ActionScript ile (en son sürümü 3.0) programlanırken Defold betikleri Lua ile yazılır. Bu kılavuzda Lua ile ActionScript 3.0 ayrıntılı olarak karşılaştırılmayacaktır. [Defold kılavuzu](/manuals/lua), Defold'da Lua programlamaya iyi bir giriş sunar ve çevrimiçi olarak ücretsiz erişilebilen, son derece yararlı [Programming in Lua](https://www.lua.org/pil/) kitabının ilk baskısına başvurur.

Jesse Warden'ın bir makalesi, iyi bir başlangıç noktası olabilecek [ActionScript ve Lua'nın temel bir karşılaştırmasını](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html) sunar. Ancak Defold ile Flash'ın yapıları arasında, dil düzeyinde görülenden daha derin farklar olduğunu unutmayın. ActionScript ve Flash, sınıfları ve kalıtımıyla klasik anlamda nesne yönelimlidir. Defold'da sınıflar da kalıtım da yoktur. Görsel ve işitsel gösterimi, davranışı ve verileri barındırabilen *oyun nesnesi* (game object) kavramı vardır. Oyun nesneleri üzerindeki işlemler, Defold API'lerinde bulunan *işlevlerle* gerçekleştirilir. Ayrıca Defold, nesneler arasında iletişim kurmak için *iletilerin* (message) kullanılmasını teşvik eder. İletiler, yöntem çağrılarından daha yüksek düzeyli bir yapıdır ve yöntem çağrısı olarak kullanılmak üzere tasarlanmamıştır. Bu farklar önemlidir ve bunlara alışmak biraz zaman alır; ancak bu kılavuzda ayrıntılı olarak ele alınmayacaktır.

Bunun yerine bu kılavuz, Flash ile oyun geliştirmenin bazı temel kavramlarını inceler ve bunların Defold'daki en yakın karşılıklarını ana hatlarıyla açıklar. Flash'tan Defold'a geçişe hızlı bir başlangıç yapabilmeniz için benzerlikler ve farklar, sık karşılaşılan sorunlarla birlikte ele alınır.

## Film klipleri ve oyun nesneleri

Film klipleri (movie clip), Flash ile oyun geliştirmenin temel öğelerinden biridir. Her biri kendine özgü bir zaman çizelgesi içeren sembollerdir. Defold'daki en yakın karşılıkları oyun nesnesidir.

![oyun nesnesi ve film klibi](images/flash/go_movieclip.png)

Flash film kliplerinin aksine, Defold oyun nesnelerinin zaman çizelgeleri yoktur. Bunun yerine bir oyun nesnesi birden çok bileşenden (component) oluşur. Bileşenler arasında sprite bileşenleri, sesler ve betikler---ve daha birçok tür bulunur (kullanılabilir bileşenler hakkında daha fazla ayrıntı için [yapı taşları belgelerine](/manuals/building-blocks) ve ilgili yazılara bakın). Aşağıdaki ekran görüntüsündeki oyun nesnesi bir sprite ve bir betikten oluşur. Betik bileşeni, oyun nesnelerinin yaşam döngüsü boyunca davranışlarını ve görünümlerini denetlemek için kullanılır:

![betik bileşeni](images/flash/script_component.png)

Film klipleri başka film klipleri içerebilirken oyun nesneleri başka oyun nesnelerini *içeremez*. Ancak oyun nesneleri diğer oyun nesnelerine *alt nesne olarak bağlanabilir*; böylece birlikte taşınabilen, ölçeklenebilen veya döndürülebilen hiyerarşiler oluşturulur.

## Flash—elle film klibi oluşturma

Flash'ta film klibi örneklerini kütüphaneden zaman çizelgesine sürükleyerek sahnenize elle ekleyebilirsiniz. Aşağıdaki ekran görüntüsü bunu gösterir; her Flash logosu, `logo` film klibinin bir örneğidir:

![elle oluşturulan film klipleri](images/flash/manual_movie_clips.png)

## Defold—elle oyun nesnesi oluşturma

Daha önce belirtildiği gibi, Defold'da zaman çizelgesi kavramı yoktur. Bunun yerine oyun nesneleri koleksiyonlarda (collection) düzenlenir. Koleksiyonlar, oyun nesnelerini ve diğer koleksiyonları tutan kapsayıcılardır (veya yeniden kullanılabilir nesne tanımları olan prefablardır). En temel düzeyde bir oyun yalnızca tek bir koleksiyondan oluşabilir. Defold oyunları daha çok, başlangıç koleksiyonu (bootstrap collection) `main` içine elle eklenen veya [koleksiyon vekilleri (collection proxy)](/manuals/collection-proxy) aracılığıyla dinamik olarak yüklenen birden çok koleksiyon kullanır. Bu "bölüm" veya "ekran" yükleme kavramının Flash'ta doğrudan bir karşılığı yoktur.

Aşağıdaki örnekte `main` koleksiyonu, `logo` oyun nesnesinin (solda *Assets* tarayıcı penceresinde görülüyor) üç örneğini (sağda *Outline* penceresinde listeleniyor) içerir:

![elle oluşturulan oyun nesneleri](images/flash/manual_game_objects.png)

## Flash—elle oluşturulan film kliplerine başvurma

Flash'ta elle oluşturulan film kliplerine başvurmak için elle tanımlanmış bir örnek adı kullanılması gerekir:

![Flash örnek adı](images/flash/flash_instance_name.png)

## Defold—oyun nesnesi tanımlayıcısı

Defold'da tüm oyun nesnelerine ve bileşenlere bir adres aracılığıyla başvurulur. Çoğu durumda yalnızca basit bir ad veya kısa gösterim yeterlidir. Örneğin:

- `"."` geçerli oyun nesnesini adresler.
- `"#"` geçerli bileşeni (betiği) adresler.
- `"logo"` tanımlayıcısı `logo` olan oyun nesnesini adresler.
- `"#script"` geçerli oyun nesnesindeki, tanımlayıcısı `script` olan bileşeni adresler.
- `"logo#script"` tanımlayıcısı `script` olan bileşeni, tanımlayıcısı `logo` olan oyun nesnesi içinde adresler.

Elle yerleştirilen oyun nesnelerinin adresi, atanan *Id* özelliğiyle belirlenir (ekran görüntüsünün sağ alt köşesine bakın). Tanımlayıcının, üzerinde çalıştığınız geçerli koleksiyon dosyasında benzersiz olması gerekir. Düzenleyici sizin için otomatik olarak bir tanımlayıcı ayarlar; ancak oluşturduğunuz her oyun nesnesi örneği için bunu değiştirebilirsiniz.

![oyun nesnesi tanımlayıcısı](images/flash/game_object_id.png)

::: sidenote
Bir oyun nesnesinin tanımlayıcısını, betik bileşeninde şu kodu çalıştırarak bulabilirsiniz: `print(go.get_id())`. Bu kod, geçerli oyun nesnesinin tanımlayıcısını konsola yazdırır.
:::

Adresleme modeli ve ileti aktarımı, Defold ile oyun geliştirmenin temel kavramlarıdır. [Adresleme kılavuzu](/manuals/addressing) ve [ileti aktarımı kılavuzu](/manuals/message-passing) bunları ayrıntılı olarak açıklar.

## Flash—dinamik olarak film klibi oluşturma

Flash'ta dinamik olarak film klibi oluşturmak için önce ActionScript Linkage ayarının yapılması gerekir:

![ActionScript Linkage](images/flash/actionscript_linkage.png)

Bu işlem bir sınıf (bu örnekte `Logo`) oluşturur ve ardından bu sınıfın yeni örneklerinin oluşturulmasına olanak tanır. `Logo` sınıfının bir örneğini Stage'e eklemek için aşağıdaki kod kullanılabilir:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold—fabrikalarla oyun nesnesi oluşturma

Defold'da oyun nesnelerinin dinamik olarak oluşturulması *fabrikalar* (factory) aracılığıyla gerçekleştirilir. Fabrikalar, belirli bir oyun nesnesinin kopyalarını çalışma sırasında oluşturmak için kullanılan bileşenlerdir. Bu örnekte, prototip olarak `logo` oyun nesnesini kullanan bir fabrika oluşturulmuştur:

![logo fabrikası](images/flash/logo_factory.png)

Fabrikaların, tüm bileşenler gibi, kullanılabilmeleri için önce bir oyun nesnesine eklenmesi gerektiğini unutmayın. Bu örnekte, fabrika bileşenimizi tutmak için `factories` adlı bir oyun nesnesi oluşturduk:

![fabrika bileşeni](images/flash/factory_component.png)

`logo` oyun nesnesinin bir örneğini oluşturmak için çağrılacak işlev şudur:

```lua
local logo_id = factory.create("factories#logo_factory")
```

URL, `factory.create()` işlevinin zorunlu bir parametresidir. Ayrıca konumu, dönmeyi, özellikleri ve ölçeği ayarlamak için isteğe bağlı parametreler ekleyebilirsiniz. Fabrika bileşeni hakkında daha fazla bilgi için [fabrika kılavuzuna](/manuals/factory) bakın. `factory.create()` çağrısının, oluşturulan oyun nesnesinin tanımlayıcısını döndürdüğünü unutmayın. Bu tanımlayıcı, daha sonra başvurmak üzere bir tabloda (dizinin Lua'daki karşılığı) saklanabilir.

## Flash—sahne

Flash'ta Timeline (aşağıdaki ekran görüntüsünün üst bölümü) ve Stage (Timeline altında görünen alan) bize tanıdıktır:

![zaman çizelgesi ve sahne](images/flash/stage.png)

Yukarıdaki film klipleri bölümünde ele alındığı gibi, Stage temelde bir Flash oyununun en üst düzey kapsayıcısıdır ve bir proje her dışa aktarıldığında oluşturulur. Stage varsayılan olarak tek bir alt nesneye, *`MainTimeline`* nesnesine sahiptir. Projede oluşturulan her film klibinin kendi zaman çizelgesi olur ve diğer semboller (film klipleri dahil) için kapsayıcı görevi görebilir.

## Defold—koleksiyonlar

Flash Stage'in Defold'daki karşılığı bir koleksiyondur. Motor başlatıldığında bir koleksiyon dosyasının içeriğine dayalı yeni bir oyun dünyası oluşturur. Bu dosyanın varsayılan adı `main.collection` olsa da, her Defold projesinin kökünde bulunan *game.project* ayar dosyasını açarak başlangıçta hangi koleksiyonun yükleneceğini değiştirebilirsiniz:

![game.project](images/flash/game_project.png)

Koleksiyonlar, düzenleyicide oyun nesnelerini ve diğer koleksiyonları düzenlemek için kullanılan kapsayıcılardır. Bir koleksiyonun içeriği, normal bir oyun nesnesi fabrikasıyla aynı şekilde çalışan [koleksiyon fabrikası (collection factory)](/manuals/collection-factory/#spawning-a-collection) kullanılarak betik aracılığıyla çalışma sırasında da oluşturulabilir. Bu, örneğin düşman grupları veya belirli bir düzende toplanabilir madeni paralar oluşturmak için yararlıdır. Aşağıdaki ekran görüntüsünde `logos` koleksiyonunun iki örneğini `main` koleksiyonuna elle yerleştirdik.

![koleksiyon](images/flash/collection.png)

Bazı durumlarda tamamen yeni bir oyun dünyası yüklemek istersiniz. [Koleksiyon vekili](/manuals/collection-proxy/) bileşeni, bir koleksiyon dosyasının içeriğine dayalı yeni bir oyun dünyası oluşturmanıza olanak tanır. Bu; yeni oyun bölümleri, mini oyunlar veya ara sahneler yükleme gibi durumlarda yararlı olur.

## Flash—zaman çizelgesi

Flash zaman çizelgesi, öncelikle çeşitli kare kare animasyon teknikleri veya şekil/hareket ara geçiş animasyonları (tween) kullanılarak animasyon oluşturmak için kullanılır. Projenin genel FPS (saniyedeki kare sayısı) ayarı, bir karenin ne kadar süreyle gösterileceğini belirler. Deneyimli kullanıcılar oyunun genel FPS değerini, hatta tek tek film kliplerinin FPS değerini değiştirebilir.

Şekil ara geçiş animasyonları, vektör grafiklerinin iki durumu arasında ara değerleme yapılmasına olanak tanır. Aşağıdaki bir kareyi üçgene dönüştüren şekil ara geçiş animasyonu örneğinin gösterdiği gibi, bunlar çoğunlukla yalnızca basit şekiller ve uygulamalar için yararlıdır:

![zaman çizelgesi](images/flash/timeline.png)

Hareket ara geçiş animasyonları, bir nesnenin boyut, konum ve dönme dahil çeşitli özelliklerine animasyon uygulanmasına olanak tanır. Aşağıdaki örnekte, listelenen tüm özellikler değiştirilmiştir.

![hareket ara geçiş animasyonu](images/flash/tween.png)

## Defold—özellik animasyonu

Defold vektör grafikleri yerine piksel görüntüleriyle çalışır; bu nedenle şekil ara geçiş animasyonunun bir karşılığı yoktur. Ancak hareket ara geçiş animasyonunun [özellik animasyonu (property animation)](/ref/go/#go.animate) biçiminde güçlü bir karşılığı vardır. Bu, betik aracılığıyla `go.animate()` işlevi kullanılarak gerçekleştirilir. `go.animate()` işlevi, kullanılabilir birçok geçiş eğrisi işlevinden (easing function) birini (özel işlevler dahil) kullanarak bir özelliği (renk, ölçek, dönme veya konum gibi) başlangıç değerinden istenen son değere geçirir. Flash'ta daha gelişmiş geçiş eğrisi işlevlerini kullanıcının uygulaması gerekirken Defold, motora yerleşik [birçok geçiş eğrisi işlevi](/manuals/property-animation/#easing) içerir.

Flash, animasyon için bir zaman çizelgesindeki grafik anahtar karelerini kullanırken Defold'da grafik animasyonunun başlıca yöntemlerinden biri, içe aktarılan görüntü dizileriyle kare dizisi animasyonu (flipbook animation) oluşturmaktır. Animasyonlar, atlas olarak bilinen bir oyun nesnesi bileşeninde düzenlenir. Bu örnekte, bir oyun karakteri için `run` adlı animasyon dizisi içeren bir atlasımız var. Animasyon dizisi, bir dizi png dosyasından oluşur:

![kare dizisi animasyonu](images/flash/flipbook.png)

## Flash—derinlik indeksi

Flash'ta görüntüleme listesi (display list), neyin hangi sırayla gösterileceğini belirler. Bir kapsayıcıdaki (Stage gibi) nesnelerin sıralaması bir indeksle yönetilir. `addChild()` yöntemi kullanılarak bir kapsayıcıya eklenen nesneler, 0'dan başlayan ve eklenen her nesneyle artan indeksin en üst konumuna otomatik olarak yerleşir. Aşağıdaki ekran görüntüsünde `logo` film klibinin üç örneğini oluşturduk:

![derinlik indeksi](images/flash/depth_index.png)

Görüntüleme listesindeki konumlar, her `logo` örneğinin yanındaki sayılarla belirtilir. Film kliplerinin x/y konumunu ayarlayan kodu dikkate almazsak yukarıdaki sonuç şöyle oluşturulabilir:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

Bir nesnenin başka bir nesnenin üstünde mi yoksa altında mı gösterileceği, görüntüleme listesi indeksindeki göreli konumlarıyla belirlenir. Örneğin iki nesnenin indeks konumlarını değiştirmek bunu açıkça gösterir:

```as
swapChildren(logo2,logo3);
```

Sonuç aşağıdaki gibi görünür (indeks konumu güncellenmiştir):

![derinlik indeksi](images/flash/depth_index_2.png)

## Defold—z konumu

Defold'da oyun nesnelerinin konumları, x, y ve z olmak üzere üç değişkenden oluşan vektörlerle temsil edilir. z konumu, bir oyun nesnesinin derinliğini belirler. Varsayılan [işleme betiğinde](/manuals/render), kullanılabilir z konumları -1 ile 1 arasındadır.

::: sidenote
z konumu -1 ile 1 aralığının dışında olan oyun nesneleri işlenmez ve bu nedenle görünmez. Bu, Defold'a yeni başlayan geliştiricilerin sık karşılaştığı bir sorundur; bir oyun nesnesi görünmesini beklediğiniz hâlde görünmüyorsa bunu aklınızda bulundurun.
:::

Flash düzenleyicisinde derinlik indekslemesi yalnızca dolaylı olarak gösterilirken (ve *Bring Forward* ile *Send Backward* gibi komutlarla değiştirilebilirken), Defold nesnelerin z konumunu doğrudan düzenleyicide ayarlamanıza olanak tanır. Aşağıdaki ekran görüntüsünde `logo3` nesnesinin en üstte gösterildiğini ve z konumunun 0.2 olduğunu görebilirsiniz. Diğer oyun nesnelerinin z konumları 0.0 ve 0.1'dir.

![z sırası](images/flash/z_order.png)

Bir veya daha fazla koleksiyonun içinde yer alan bir oyun nesnesinin z konumunun, kendi z konumuyla birlikte tüm üst nesnelerinin z konumları tarafından belirlendiğini unutmayın. Örneğin yukarıdaki `logo` oyun nesnelerinin bir `logos` koleksiyonuna yerleştirildiğini, bu koleksiyonun da `main` içine yerleştirildiğini düşünün (aşağıdaki ekran görüntüsüne bakın). `logos` koleksiyonunun z konumu 0.9 olsaydı, içindeki oyun nesnelerinin z konumları 0.9, 1.0 ve 1.1 olurdu. Dolayısıyla `logo3`, z konumu 1'den büyük olduğu için işlenmezdi.

![z sırası](images/flash/z_order_outline.png)

Bir oyun nesnesinin z konumu betikle de değiştirilebilir. Aşağıdaki kodun bir oyun nesnesinin betik bileşeninde bulunduğunu varsayın:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Flash'ta `hitTestObject` ve `hitTestPoint` ile çarpışma algılama

Flash'ta temel çarpışma algılama, `hitTestObject()` yöntemi kullanılarak gerçekleştirilir. Bu örnekte iki film klibimiz var: `bullet` ve `bullseye`. Bunlar aşağıdaki ekran görüntüsünde gösterilmiştir. Flash düzenleyicisinde semboller seçildiğinde mavi sınırlayıcı kutu görünür ve `hitTestObject()` yönteminin sonucunu bu sınırlayıcı kutular belirler.

![isabet testi](images/flash/hittest.png)

`hitTestObject()` kullanılarak çarpışma algılama şu şekilde yapılır:

```as
bullet.hitTestObject(bullseye);
```

Bu durumda sınırlayıcı kutuların kullanılması uygun olmaz; çünkü aşağıdaki senaryoda bir isabet algılanır:

![sınırlayıcı kutuyla isabet testi](images/flash/hitboundingbox.png)

`hitTestObject()` yönteminin bir alternatifi `hitTestPoint()` yöntemidir. Bu yöntem, isabet testlerinin sınırlayıcı kutu yerine nesnenin gerçek piksellerine karşı yapılmasını sağlayan bir `shapeFlag` parametresi içerir. `hitTestPoint()` kullanılarak çarpışma algılama aşağıdaki gibi yapılabilir:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Bu satır, merminin x ve y konumunu (bu senaryoda sol üst köşesi) hedefin şekline karşı kontrol eder. `hitTestPoint()` bir noktayı bir şekle karşı kontrol ettiğinden, hangi noktanın (veya noktaların!) kontrol edileceği önemli bir konudur.

## Defold—çarpışma nesneleri

Defold, çarpışmaları algılayabilen ve bir betiğin bunlara tepki vermesine olanak tanıyan bir fizik motoru içerir. Defold'da çarpışma algılama, oyun nesnelerine çarpışma nesnesi (collision object) bileşenleri atanmasıyla başlar. Aşağıdaki ekran görüntüsünde `bullet` oyun nesnesine bir çarpışma nesnesi ekledik. Çarpışma nesnesi, kırmızı saydam kutuyla gösterilir (bu kutu yalnızca düzenleyicide görünür):

![çarpışma nesnesi](images/flash/collision_object.png)

Defold, gerçekçi çarpışmaları otomatik olarak simüle edebilen Box2D fizik motorunun değiştirilmiş bir sürümünü içerir. Bu kılavuz, Flash'taki çarpışma algılamaya en çok benzedikleri için kinematik çarpışma nesnelerinin kullanıldığını varsayar. Dinamik çarpışma nesneleri hakkında daha fazla bilgiyi Defold [fizik kılavuzunda](/manuals/physics) bulabilirsiniz.

Çarpışma nesnesi aşağıdaki özellikleri içerir:

![çarpışma nesnesi özellikleri](images/flash/collision_object_properties.png)

Mermi görseline en uygun şekil olduğu için kutu kullanılmıştır. 2B çarpışmalar için kullanılan diğer şekil olan küre ise hedef için kullanılacaktır. Türün Kinematic olarak ayarlanması, çarpışmaların çözümünün yerleşik fizik motoru yerine betiğiniz tarafından yapılacağı anlamına gelir (diğer türler hakkında daha fazla bilgi için [fizik kılavuzuna](/manuals/physics) bakın). *Group* ve *Mask* özellikleri, sırasıyla nesnenin hangi çarpışma grubuna ait olduğunu ve hangi çarpışma grubuna karşı kontrol edilmesi gerektiğini belirler. Geçerli ayarlar, bir `bullet` nesnesinin yalnızca bir `target` nesnesiyle çarpışabileceği anlamına gelir. Ayarların aşağıdaki gibi değiştirildiğini düşünün:

![çarpışma grubu/maskesi](images/flash/collision_groupmask.png)

Artık mermiler hedeflerle ve diğer mermilerle çarpışabilir. Karşılaştırma için hedefe aşağıdaki gibi görünen bir çarpışma nesnesi ekledik:

![mermi çarpışma nesnesi](images/flash/collision_object_bullet.png)

*Group* özelliğinin `target`, *Mask* özelliğinin ise `bullet` olarak ayarlandığına dikkat edin.

Flash'ta çarpışma algılama yalnızca betik tarafından açıkça çağrıldığında gerçekleşir. Defold'da ise bir çarpışma nesnesi etkin kaldığı sürece çarpışma algılama arka planda sürekli gerçekleşir. Bir çarpışma olduğunda oyun nesnesinin tüm bileşenlerine (özellikle betik bileşenlerine) iletiler gönderilir. Bunlar, çarpışmayı istendiği şekilde çözmek için gereken tüm bilgileri içeren [`collision_response` ve `contact_point_response`](/manuals/physics-messages) iletileridir.

Defold'un çarpışma algılamasının avantajı, Flash'takinden daha gelişmiş olması ve çok az ayarlama ile nispeten karmaşık şekiller arasındaki çarpışmaları algılayabilmesidir. Çarpışma algılama otomatiktir; dolayısıyla farklı çarpışma gruplarındaki çeşitli nesneleri döngüyle dolaşmak ve açıkça isabet testleri yapmak gerekmez. Başlıca eksikliği, Flash'taki `shapeFlag` parametresinin bir karşılığının olmamasıdır. Ancak çoğu kullanım için temel kutu ve küre şekillerinin birleşimleri yeterlidir. Daha karmaşık senaryolarda özel şekiller kullanmak [mümkündür](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash—olay işleme

Olay (event) nesneleri ve bunlarla ilişkili dinleyiciler; çeşitli olayları (örneğin fare tıklamaları, düğmeye basılması, kliplerin yüklenmesi) algılamak ve bunlara yanıt olarak eylemleri tetiklemek için kullanılır. Kullanabileceğiniz çeşitli olaylar vardır.

## Defold—geri çağırım işlevleri ve ileti alışverişi

Flash'ın olay işleme sisteminin Defold'daki karşılığı birkaç unsurdan oluşur. Öncelikle, her betik bileşeni belirli olayları algılayan bir dizi geri çağırım işleviyle (callback function) gelir. Bunlar şunlardır:

init
:   Betik bileşeninin başlangıç işlemleri yapıldığında çağrılır. Flash'taki kurucu işlevin karşılığıdır.

final
:   Betik bileşeni yok edildiğinde (örneğin çalışma sırasında oluşturulan bir oyun nesnesi kaldırıldığında) çağrılır.

update
:   Her karede çağrılır. Flash'taki `enterFrame` karşılığıdır.

on_message
:   Betik bileşeni bir ileti aldığında çağrılır.

on_input
:   Kullanıcı girdisi (örneğin fare veya klavye), [girdi odağına (input focus)](/ref/go/#acquire_input_focus) sahip bir oyun nesnesine gönderildiğinde çağrılır; girdi odağı, nesnenin tüm girdileri aldığı ve bunlara tepki verebildiği anlamına gelir.

on_reload
:   Betik bileşeni yeniden yüklendiğinde çağrılır.

Yukarıda listelenen geri çağırım işlevlerinin tümü isteğe bağlıdır ve kullanılmıyorsa kaldırılabilir. Girdinin nasıl ayarlanacağıyla ilgili ayrıntılar için [girdi kılavuzuna](/manuals/input) bakın. Koleksiyon vekilleriyle çalışırken sık karşılaşılan bir sorun vardır; daha fazla bilgi için girdi kılavuzunun [bu bölümüne](/manuals/input/#input-dispatch-and-on_input) bakın.

Çarpışma algılama bölümünde ele alındığı gibi, çarpışma olayları ilgili oyun nesnelerine iletiler gönderilerek işlenir. Bu nesnelerin betik bileşenleri, iletiyi kendi `on_message` geri çağırım işlevlerinde alır.

## Flash—düğme sembolleri

Flash, düğmeler için özel bir sembol türü kullanır. Düğmeler, kullanıcı etkileşimi algılandığında eylemleri gerçekleştirmek için belirli olay işleyici yöntemleri (örneğin `click` ve `buttonDown`) kullanır. Düğme sembolünün "Hit" bölümündeki düğme görselinin şekli, düğmenin isabet alanını belirler.

![düğme](images/flash/button.png)

## Defold—GUI sahneleri ve betikleri

Defold, yerleşik bir düğme bileşeni içermez; ayrıca Flash'ta düğmelerin ele alınışına benzer biçimde belirli bir oyun nesnesinin şekline yapılan tıklamalar kolayca algılanamaz. Bir [GUI](/manuals/gui) bileşeni kullanmak en yaygın çözümdür; bunun nedenlerinden biri, Defold GUI bileşenlerinin konumlarının oyun içi kameradan (kullanılıyorsa) etkilenmemesidir. GUI API'si ayrıca tıklama ve dokunma olayları gibi kullanıcı girdilerinin bir GUI öğesinin sınırları içinde olup olmadığını algılayan işlevler içerir.

## Hata ayıklama

Flash'ta hata ayıklarken `trace()` komutu yardımcınızdır. Defold'daki karşılığı `print()` işlevi olup `trace()` ile aynı şekilde kullanılır:

```lua
print("Hello world!"")
```

Tek bir `print()` işlevi kullanarak birden çok değişkeni yazdırabilirsiniz:

```lua
print(score, health, ammo)
```

Tablolarla çalışırken yararlı olan `pprint()` (biçimlendirilmiş yazdırma) işlevi de vardır. Bu işlev, iç içe tablolar dahil tabloların içeriğini yazdırır. Aşağıdaki betiği inceleyin:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Bu betikte, `factions` tablosu `world` tablosunun içine yerleştirilmiştir. Normal `print()` komutu kullanıldığında tablonun gerçek içeriği yerine benzersiz tanımlayıcısı yazdırılır:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Yukarıda gösterildiği gibi `pprint()` işlevi kullanıldığında daha anlamlı sonuçlar elde edilir:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Oyununuz çarpışma algılama kullanıyorsa, aşağıdaki iletiyi göndererek fizik hata ayıklamasını açıp kapatabilirsiniz:

```lua
msg.post("@system:", "toggle_physics_debug")
```

Fizik hata ayıklaması proje ayarlarından da etkinleştirilebilir. Fizik hata ayıklamasını açmadan önce projemiz şöyle görünür:

![hata ayıklama kapalı](images/flash/no_debug.png)

Fizik hata ayıklaması açıldığında oyun nesnelerimize eklenen çarpışma nesneleri gösterilir:

![hata ayıklama açık](images/flash/with_debug.png)

Çarpışmalar gerçekleştiğinde ilgili çarpışma nesneleri aydınlanır. Ayrıca çarpışma vektörü gösterilir:

![çarpışma](images/flash/collision.png)

Son olarak, CPU ve bellek kullanımını nasıl izleyeceğiniz hakkında bilgi için [profil çıkarıcı belgelerine](/ref/profiler/) bakın. Gelişmiş hata ayıklama teknikleri hakkında daha fazla bilgi için Defold kılavuzunun [hata ayıklama bölümüne](/manuals/debugging) bakın.

## Sonraki adımlar

- [Defold örnekleri](/examples)
- [Öğreticiler](/tutorials)
- [Kılavuzlar](/manuals)
- [Başvuru](/ref/go)
- [Sık sorulan sorular](/faq/faq)

Sorularınız varsa veya bir noktada takılırsanız, [Defold forumları](//forum.defold.com) yardım istemek için harika bir yerdir.
