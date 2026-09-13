---
title: Defold motoru ve düzenleyicisi hakkında sık sorulan sorular
brief: Defold oyun motoru, düzenleyicisi ve platformu hakkında sık sorulan sorular.
---

# Sık sorulan sorular

## Genel sorular

#### Q: Defold gerçekten ücretsiz mi?

A: Evet, Defold motoru ve düzenleyicisi tüm işlevleriyle tamamen ücretsizdir. Gizli maliyet, ücret veya telif ücreti yoktur. Tamamen ücretsizdir.


#### Q: Defold Foundation Defold'u neden ücretsiz dağıtıyor?

A: [Defold Foundation](/foundation) kuruluşunun amaçlarından biri, Defold yazılımının dünyanın her yerindeki geliştiricilere sunulmasını ve kaynak kodunun ücretsiz olarak erişilebilir olmasını sağlamaktır.


#### Q: Defold'u ne kadar süre destekleyeceksiniz?

A: Defold'a güçlü bir bağlılık duyuyoruz. [Defold Foundation](/foundation), Defold'un sorumlu sahibi olarak uzun yıllar varlığını sürdürmesi güvence altına alınacak şekilde kurulmuştur. Varlığını sürdürecektir.


#### Q: Profesyonel geliştirme için Defold'a güvenebilir miyim?

A: Kesinlikle. Defold'u kullanan profesyonel oyun geliştiricilerinin ve oyun stüdyolarının sayısı giderek artıyor. Defold ile oluşturulmuş oyun örnekleri için [oyun vitrinine](/showcase) göz atın.


#### Q: Ne tür kullanıcı takibi yapıyorsunuz?

A: Hizmetlerimizi ve ürünümüzü iyileştirmek için web sitelerimizden ve Defold düzenleyicisinden anonim kullanım verileri kaydediyoruz. Oluşturduğunuz oyunlarda kullanıcı takibi yoktur (kendiniz bir analiz hizmeti eklemediğiniz sürece). Bu konuda daha fazla bilgiyi [Gizlilik Politikamızda](/privacy-policy) bulabilirsiniz.


#### Q: Defold'u kim yaptı?

A: Defold, Ragnar Svensson ve Christian Murray tarafından oluşturuldu. Motor, düzenleyici ve sunucular üzerinde çalışmaya 2009'da başladılar. King ve Defold 2013'te bir ortaklık başlattı, King ise 2014'te Defold'u satın aldı. Hikâyenin tamamını [buradan](/about) okuyabilirsiniz.


## Oyun geliştirme soruları

#### Q: Defold'da 3B oyunlar yapabilir miyim?

A: Kesinlikle! Motor, tam donanımlı bir 3B motordur. Ancak araç seti 2B için hazırlanmıştır, bu nedenle pek çok zahmetli işi kendiniz yapmanız gerekir. Daha iyi 3B desteği planlanmaktadır.


## Programlama dili soruları

#### Q: Defold'da hangi programlama diliyle çalışırım?

A: Defold projenizdeki oyun mantığı öncelikle Lua diliyle yazılır (özellikle Lua 5.1/LuaJIT; ayrıntılar için [Lua kılavuzuna](/manuals/lua) bakın). Lua, hızlı ve çok güçlü, hafif bir dinamik dildir. Defold, Lua kodu üreten kaynak koddan kaynak koda derleyicileri (transpiler) destekler. Böyle bir derleyici eklentisi kurulduğunda, statik olarak denetlenen Lua yazmak için [Teal](https://github.com/defold/extension-teal) gibi alternatif diller kullanabilirsiniz. Ayrıca [Defold motorunu yeni işlevlerle genişletmek](/manuals/extensions/) için yerel kod (native code; platforma bağlı olarak C/C++, Objective-C, Java ve JavaScript) kullanabilirsiniz. [Özel materyaller (material)](/manuals/material/) oluştururken köşe ve parça gölgelendiricileri (vertex shader ve fragment shader) yazmak için OpenGL ES SL gölgelendirici dili kullanılır.


#### Q: Oyun mantığını yazmak için C++ kullanabilir miyim?

A: Defold'daki C++ desteği esas olarak üçüncü taraf yazılım geliştirme kitleriyle (SDK) veya platforma özgü API'lerle iletişim kuran yerel kod eklentileri (native extension) yazmak için vardır. [dmSDK](https://defold.com/ref/stable/dmGameObject/) (yerel kod eklentilerinde kullanılan Defold C++ API'si), isteyen bir geliştiricinin tüm oyun mantığını C++ ile yazabilmesini sağlayacak şekilde zamanla daha fazla işlevle genişletilecektir. Lua, oyun mantığı için kullanılan ana dil olmaya devam edecek, ancak genişletilen C++ API'siyle oyun mantığını C++ kullanarak yazmak da mümkün olacaktır. C++ API'sini genişletme çalışmaları esas olarak mevcut özel başlık dosyalarını herkese açık bölüme taşımayı ve API'leri genel kullanıma uygun hâle getirmeyi kapsar.


#### Q: Defold ile TypeScript kullanabilir miyim?

A: TypeScript resmî olarak desteklenmez. Topluluk, TypeScript yazmak ve doğrudan VSCode içinden Lua koduna dönüştürmek için [ts-defold](https://ts-defold.dev/) araç setini geliştirmeye devam ediyor.


#### Q: Defold ile Haxe kullanabilir miyim?

A: Haxe resmî olarak desteklenmez. Topluluk, Haxe yazmak ve Lua koduna dönüştürmek için [hxdefold](https://github.com/hxdefold/hxdefold) projesini geliştirmeye devam ediyor.


#### Q: Defold ile C# kullanabilir miyim?

A: Defold Foundation, C# desteğini ekledi ve bir kütüphane bağımlılığı olarak kullanıma sundu. C#, yaygın olarak benimsenmiş bir programlama dilidir ve C# diline büyük yatırım yapmış stüdyoların ve geliştiricilerin Defold'a geçişine yardımcı olacaktır.


#### Q: C# desteği eklenmesinin Defold'u olumsuz etkileyeceğinden endişeleniyorum. Endişelenmeli miyim?

Defold, ana betik dili olarak Lua'dan UZAKLAŞMIYOR. C# desteği, eklentiler için yeni bir dil olarak ekleniyor. Projenizde C# eklentilerini kullanmayı seçmediğiniz sürece motoru etkilemeyecektir.

C# desteğinin bazı maliyetleri (yürütülebilir dosya boyutu, çalışma zamanı performansı vb.) olacaktır, ancak buna her geliştirici veya stüdyo kendisi karar verecektir.

C# dilinin kendisine gelince, eklenti sistemi zaten birçok dili (C/C++/Java/Objective-C/Zig) desteklediğinden bu nispeten küçük bir değişikliktir. C# bağlamaları üretilerek SDK'lerin birbiriyle uyumu korunacaktır. Böylece bağlamalar en az çabayla güncel tutulacaktır.

Defold Foundation daha önce Defold'a C# desteği eklenmesine karşıydı, ancak çeşitli nedenlerle görüşünü değiştirdi:

* Stüdyolar ve geliştiriciler C# desteği istemeye devam ediyor.
* C# desteğinin kapsamı yalnızca eklentilerle sınırlı tutuldu (yani az çaba gerektiriyor).
* Çekirdek motor etkilenmeyecek.
* C# API'leri üretilirse en az çabayla birbiriyle uyumlu tutulabilir.
* C# desteği, NativeAOT ile DotNet 9 üzerine kurulacak; böylece mevcut derleme hattının bağlayabileceği statik kütüphaneler üretilecek (diğer tüm Defold eklentileri gibi).


## Platform soruları

#### Q: Defold hangi platformlarda çalışır?

A: Düzenleyici/araçlar ve motorun çalışma zamanı ortamı için aşağıdaki platformlar desteklenir:

  | Sistem             | Sürüm              | Mimariler          | Desteklenen        |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Düzenleyici ve motor |
  | Windows            | Vista              | `x86-32`, `x86-64` | Düzenleyici ve motor |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Düzenleyici        |
  | Linux (2)          | Herhangi biri      | `x86-64`, `arm-64` | Motor              |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Motor              |
  | Android            | 5.0 (API düzeyi 21) | `arm-32`, `arm-64` | Motor              |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | Motor        |

  (1 Düzenleyici, 64 bit Ubuntu için derlenir ve test edilir. Diğer dağıtımlarda da çalışması beklenir, ancak bunu garanti etmiyoruz.)

  (2 Grafik sürücüleri güncel olduğu sürece motorun çalışma zamanı ortamının çoğu 64 bit Linux dağıtımında çalışması beklenir; grafik API'leri hakkında daha fazla bilgi için aşağıya bakın)


#### Q: Defold ile hangi hedef platformlar için oyun geliştirebilirim?

A: Tek tıklamayla PS4™, PS5™, Nintendo Switch, iOS (64 bit), Android (32 bit ve 64 bit) ve HTML5 için; ayrıca macOS (x86-64 ve arm64), Windows (32 bit ve 64 bit) ve Linux (x86-64 ve arm64) için yayımlayabilirsiniz. Gerçekten de tek bir kod tabanı birden çok platformu destekler.


#### Q: Defold hangi işleme API'sini kullanır?

A: Geliştirici olarak, [tamamen betiklerle yönetilebilen bir işleme hattı](/manuals/render/) kullanan tek bir işleme (rendering) API'siyle ilgilenmeniz yeterlidir. Defold'un işleme betiği API'si, işleme işlemlerini aşağıdaki grafik API'lerine dönüştürür:

:[Graphics API](../shared/graphics-api.md)

#### Q: Hangi sürümü çalıştırdığımı öğrenmenin bir yolu var mı?

A: Evet, Help menüsündeki "About" seçeneğini seçin. Açılır pencere, Defold beta sürümünü ve daha da önemlisi, ilgili sürümün SHA1 değerini açıkça gösterir. Çalışma sırasında sürümü sorgulamak için [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info) işlevini kullanın.

[http://d.defold.com/beta](http://d.defold.com/beta) adresinden indirilebilen en son beta sürümünü, [http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json) adresini açarak kontrol edebilirsiniz (aynı dosya kararlı sürümler için de vardır: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)).


#### Q: Oyunun çalışma sırasında hangi platformda çalıştığını öğrenmenin bir yolu var mı?

A: Evet, [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info) işlevine göz atın.


## Düzenleyici soruları
:[Editor FAQ](../shared/editor-faq.md)


## Linux soruları {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Android soruları
:[Android FAQ](../shared/android-faq.md)


## HTML5 soruları
:[HTML5 FAQ](../shared/html5-faq.md)


## iOS soruları
:[iOS FAQ](../shared/ios-faq.md)


## Windows soruları
:[Windows FAQ](../shared/windows-faq.md)


## Konsol soruları
:[Consoles FAQ](../shared/consoles-faq.md)


## Oyun yayımlama

#### Q: Oyunumu App Store'da yayımlamaya çalışıyorum. IDFA sorusunu nasıl yanıtlamalıyım?

A: Uygulamayı gönderirken Apple, IDFA'nın üç geçerli kullanım durumu için üç onay kutusu sunar:

  1. Serve ads within the app
  2. Install attribution from ads
  3. User action attribution from ads

  1 numaralı seçeneği işaretlerseniz uygulamayı inceleyen kişi uygulamada reklam gösterilip gösterilmediğini kontrol eder. Oyununuz reklam göstermiyorsa reddedilebilir. Defold'un kendisi reklam tanımlayıcısını kullanmaz.


#### Q: Oyunumdan nasıl gelir elde edebilirim?

A: Defold, uygulama içi satın almaları ve çeşitli reklam çözümlerini destekler. Kullanılabilir gelir elde etme seçeneklerinin güncel listesi için [Asset Portal'daki Monetization kategorisine](https://defold.com/tags/stars/monetization/) bakın.


## Defold kullanırken karşılaşılan hatalar

#### Q: Oyunu başlatamıyorum ve derleme hatası da yok. Sorun ne?

A: Proje derleme süreci, daha önce karşılaşıp düzelttiğiniz derleme hatalarının ardından, nadiren de olsa dosyaları yeniden derleyemeyebilir. Menüden *Project > Rebuild And Launch* seçeneğini seçerek tam bir yeniden derlemeyi zorlayın.



## Oyun içeriği

#### Q: Defold, yeniden kullanılabilir nesne tanımları olan prefabları destekliyor mu?

A: Evet, destekliyor. Bunlara [koleksiyon (collection)](/manuals/building-blocks/#collections) denir. Koleksiyonlar, karmaşık oyun nesnesi (game object) hiyerarşileri oluşturmanızı ve bunları, düzenleyicide veya çalışma sırasında (koleksiyon içeriği oluşturarak) örneklerini oluşturabileceğiniz ayrı yapı taşları olarak saklamanızı sağlar. Grafik kullanıcı arayüzü (GUI) düğümleri için GUI şablonları desteklenir.


#### Q: Bir oyun nesnesini başka bir oyun nesnesine alt nesne olarak ekleyemiyorum, neden?

A: Büyük olasılıkla oyun nesnesi dosyasında bir alt nesne eklemeye çalışıyorsunuz ve bu mümkün değildir. Bu yalnızca koleksiyon dosyasında yapılabilir. Bunun nedenini anlamak için üst-alt nesne hiyerarşilerinin yalnızca bir _sahne grafı (scene graph)_ dönüşüm hiyerarşisi olduğunu hatırlamanız gerekir. Bir sahneye (koleksiyona) yerleştirilmemiş (veya çalışma sırasında oluşturulmamış) bir oyun nesnesi, sahne grafının parçası değildir ve bu nedenle sahne grafı hiyerarşisinin de parçası olamaz. Oyun nesnesinin üst nesnesinin tanımlayıcısını [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id) işlevini kullanarak alabilirsiniz.


#### Q: Neden bir oyun nesnesinin tüm alt nesnelerine topluca ileti gönderemiyorum?

A: Üst-alt nesne ilişkileri yalnızca sahne grafındaki dönüşüm ilişkilerini ifade eder ve nesne yönelimli programlamadaki nesne gruplarıyla karıştırılmamalıdır. Oyun verilerinize ve oyununuzun durumu değiştikçe bu verileri en iyi nasıl dönüştürebileceğinize odaklanırsanız, birçok nesneye sürekli durum verisi içeren iletiler gönderme ihtiyacınız muhtemelen azalacaktır. Veri hiyerarşilerine ihtiyaç duyduğunuz durumlarda bunları Lua'da kolayca oluşturabilir ve yönetebilirsiniz.


#### Q: Sprite bileşenlerimin kenarlarında neden görüntü kusurları oluşuyor?

A: Bu, bir atlastaki komşu piksellerin kenar piksellerinin sprite bileşeninize atanan görüntüye taştığı, "kenar taşması (edge bleeding)" adı verilen bir görüntü kusurudur. Çözüm, atlas görüntülerinizin kenarlarını aynı piksellerden oluşan ek satır ve sütunlarla doldurmaktır. Neyse ki Defold'un atlas düzenleyicisi bunu otomatik olarak yapabilir. Atlasınızı açın ve *Extrude Borders* değerini 1 olarak ayarlayın.


#### Q: Sprite bileşenlerime renk çarpanı uygulayabilir veya onları saydam yapabilir miyim, yoksa bunun için kendi gölgelendiricimi mi yazmam gerekir?

A: Tüm sprite bileşenleri için varsayılan olarak kullanılan yerleşik sprite gölgelendiricisinde "tint" adlı bir sabit tanımlıdır:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: Bir sprite bileşeninin z koordinatını 100 olarak ayarlarsam çizilmiyor. Neden?

A: Bir oyun nesnesinin Z konumu işleme sırasını belirler. Düşük değerler yüksek değerlerden önce çizilir. Varsayılan işleme betiğinde derinliği -1 ile 1 arasında olan oyun nesneleri çizilir; bu aralığın altında veya üstünde kalanlar çizilmez. İşleme betiği hakkında daha fazla bilgiyi resmî [İşleme belgelerinde](/manuals/render) bulabilirsiniz. GUI düğümlerinde Z değeri yok sayılır ve işleme sırasını hiçbir şekilde etkilemez. Bunun yerine düğümler listelendikleri sırayla ve alt düğüm hiyerarşilerine (ve katmanlara) göre işlenir. GUI işlemesi ve katmanları kullanarak çizim çağrılarını optimize etme hakkında daha fazla bilgiyi resmî [GUI belgelerinde](/manuals/gui) bulabilirsiniz.


#### Q: Görünüm izdüşümünün Z aralığını -100 ile 100 olarak değiştirmek performansı etkiler mi?

A: Hayır. Tek etkisi hassasiyet üzerindedir. Z arabelleği logaritmiktir; 0'a yakın z değerleri için çok yüksek, 0'dan uzak değerler içinse daha düşük çözünürlük sunar. Örneğin, 24 bitlik bir arabellekle 10,0 ve 10,000005 değerleri ayırt edilebilirken 10000 ve 10005 ayırt edilemez.


#### Q: Açıların gösteriminde neden tutarlılık yok?

A: Aslında tutarlılık var. Düzenleyicide ve oyun API'lerinde açılar her yerde derece cinsinden ifade edilir. Matematik kütüphaneleri radyan kullanır. Şu anda radyan/s cinsinden ifade edilen `angular_velocity` fizik özelliği bu kuralın dışındadır. Bunun değişmesi beklenmektedir.


#### Q: Yalnızca renk içeren (dokusu olmayan) bir GUI kutu düğümü oluşturduğumda nasıl işlenir?

A: Bu, yalnızca köşeleri renklendirilmiş bir şekildir. Yine de piksel doldurma hızı açısından bir maliyeti olacağını unutmayın.


#### Q: Varlıkları çalışma sırasında değiştirirsem motor bunları otomatik olarak bellekten kaldırır mı?

A: Tüm kaynaklar (resource) için motor içinde başvuru sayımı yapılır. Başvuru sayısı sıfıra iner inmez kaynak serbest bırakılır.


#### Q: Bir oyun nesnesine bağlı ses bileşeni kullanmadan ses oynatmak mümkün mü?

A: Her şey bileşen (component) temellidir. Birden fazla ses içeren, görsel bileşeni olmayan bir oyun nesnesi oluşturabilir ve sesleri denetleyen bu nesneye iletiler göndererek ses oynatabilirsiniz.


#### Q: Bir ses bileşeniyle ilişkili ses dosyasını çalışma sırasında değiştirmek mümkün mü?

A: Genel olarak tüm kaynaklar statik olarak bildirilir; bunun avantajı, kaynak yönetiminin ek bir çaba gerektirmeden sağlanmasıdır. Bir bileşene atanan kaynağı değiştirmek için [kaynak özelliklerini](/manuals/script-properties/#resource-properties) kullanabilirsiniz.


#### Q: Fizik çarpışma şeklinin özelliklerine erişmenin bir yolu var mı?

A: Evet, fizik API'sine, özellikle de [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) ve [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table) işlevlerine göz atın. 


#### Q: Sahnemdeki çarpışma nesnelerini çizdirmenin hızlı bir yolu var mı? (Box2D'nin hata ayıklama çizimi gibi)

A: Evet, *game.project* dosyasında *physics.debug* bayrağını ayarlayın. (Resmî [Proje ayarları belgelerine](/manuals/project-settings/#debug) bakın)


#### Q: Çok sayıda temas/çarpışma olmasının performans maliyetleri nelerdir?

A: Defold arka planda Box2D'nin değiştirilmiş bir sürümünü çalıştırır ve performans maliyetinin oldukça benzer olması beklenir. [Profil çıkarıcıyı](/manuals/debugging) açarak motorun fizik için ne kadar zaman harcadığını her zaman görebilirsiniz. Kullandığınız çarpışma nesnelerinin türünü de göz önünde bulundurmalısınız. Örneğin, statik nesnelerin performans maliyeti daha düşüktür. Daha fazla ayrıntı için resmî Defold [Fizik belgelerine](/manuals/physics) bakın.


#### Q: Çok sayıda parçacık efekti bileşeni olmasının performansa etkisi nedir?

A: Bu, efektlerin oynatılıp oynatılmadığına bağlıdır. Oynatılmayan bir ParticleFx'in performans maliyeti sıfırdır. Oynatılan bir ParticleFx'in performans etkisi yapılandırmasına bağlı olduğundan profil çıkarıcı kullanılarak değerlendirilmelidir. Çoğu başka şeyde olduğu gibi bellek, *game.project* dosyasında max_count olarak tanımlanan ParticleFx sayısı için önceden ayrılır.


#### Q: Bir koleksiyon vekili aracılığıyla yüklenen koleksiyondaki bir oyun nesnesine nasıl girdi alırım?

A: Koleksiyon vekili (collection proxy) aracılığıyla yüklenen her koleksiyonun kendi girdi yığını vardır. Girdi, ana koleksiyonun girdi yığınından vekil bileşeni aracılığıyla koleksiyondaki nesnelere yönlendirilir. Bu, yüklenen koleksiyondaki oyun nesnesinin girdi odağını almasının yeterli olmadığı; vekil bileşenini _barındıran_ oyun nesnesinin de girdi odağını alması gerektiği anlamına gelir. Ayrıntılar için [Girdi belgelerine](/manuals/input) bakın.


#### Q: Dize türünde betik özellikleri kullanabilir miyim?

A: Hayır. Defold, [hash](/ref/builtins#hash) türünde özellikleri destekler. Bunlar türleri, durum tanımlayıcılarını veya her türlü anahtarı belirtmek için kullanılabilir. Karma değerleri oyun nesnesi tanımlayıcılarını (yollarını) saklamak için de kullanılabilir; ancak düzenleyici ilgili URL'leri içeren bir açılır listeyi sizin için otomatik olarak doldurduğundan [url](/ref/msg#msg.url) özellikleri genellikle daha uygundur. Ayrıntılar için [Betik özellikleri belgelerine](/manuals/script-properties) bakın.


#### Q: Bir matrisin ([`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) veya benzeri bir işlevle oluşturulan) tek tek hücrelerine nasıl erişirim?

A: Hücrelere `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` vb. kullanarak erişebilirsiniz


#### Q: [gui.clone()](/ref/gui/#gui.clone:node) veya [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) kullanırken `Not enough resources to clone the node` hatasını alıyorum

A: GUI bileşeninin `Max Nodes` değerini artırın. Bu değeri, Outline görünümünde bileşenin kökünü seçtiğinizde Properties panelinde bulabilirsiniz.


## Forum

#### Q: Çalışmalarımı tanıttığım bir konu açabilir miyim?

A: Elbette! Bunun için özel bir ["Work for hire" kategorimiz](https://forum.defold.com/c/work-for-hire) var. Topluluğa yarar sağlayan her şeyi her zaman destekleriz; hizmetlerinizi ücret karşılığında olsun ya da olmasın topluluğa sunmanız buna iyi bir örnektir.


#### Q: Bir konu açıp çalışmalarımı ekledim; daha fazlasını ekleyebilir miyim?

A: "Work for hire" konularının üst sıralara taşınmasını azaltmak için kendi konunuza 14 günde birden fazla gönderi yazamazsınız (konudaki bir yoruma doğrudan yanıt vermeniz dışında; bu durumda yanıt verebilirsiniz). 14 günlük süre içinde konunuza başka çalışmalar eklemek istiyorsanız mevcut gönderilerinizi düzenleyerek yeni içeriği eklemeniz gerekir.


#### Q: İş ilanı yayımlamak için Work for Hire kategorisini kullanabilir miyim?

A: Tabii, dilediğiniz gibi kullanın! Hem hizmet sunmak hem de hizmet talep etmek için kullanılabilir; örneğin, "2B piksel sanatçısı arayan programcı; zenginim ve iyi ücret ödeyeceğim".
