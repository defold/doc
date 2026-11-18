---
title: Godot kullanıcıları için Defold
brief: Bu kılavuz, Godot'tan bildiğiniz kavramları Defold'daki karşılıklarıyla karşılaştırır ve ilgili araçları ve API'leri nasıl kullanacağınızı gösterir.
---

# Godot kullanıcıları için Defold {#defold-for-godot-users}

Godot deneyiminiz varsa Defold'da oyun geliştirmek için gerekenlerin çoğunu zaten biliyorsunuz. Bu kılavuz, bu deneyimden nerede yararlanabileceğinizi ve sık yapılan hatalardan kaçınmak için iki motor arasındaki hangi farkları bilmeniz gerektiğini açıklar. Karşılaştırmada Godot 4.7 kullanılmıştır.

## Giriş {#introduction}

Defold, 2B ve 3B oyunlar geliştirmek için kullanabileceğiniz ücretsiz, platformlar arası bir oyun motorudur. Düzenleyicisi Windows, Linux ve macOS'ta çalışır. Motorun ve düzenleyicinin tüm kaynak kodu [GitHub](https://github.com/defold/defold/) üzerinde bulunur. Defold'u kendiniz derleyebilir veya işletim sisteminize uygun sürümü indirebilirsiniz.

İlk bakışta Defold, Godot'a çok benzer. Her iki motorda da oyununuzu yeniden kullanılabilir parçalardan oluşturur, davranışları betiklerle eklersiniz. Godot, belirli işlere özgü çok sayıda düğüm sunar. Defold'da ise daha az sayıda, daha genel amaçlı bileşen (component) vardır. Oynanış davranışını bu bileşenlerle birlikte çalışan Lua betikleri ve modülleri belirler. Örneğin Defold'da oyuncu karakteri, bir sprite veya model, bir çarpışma nesnesi ve bir betik içeren bir oyun nesnesi (game object) olabilir.

Defold, çalışma zamanı ortamını küçük tutmaya ve kaynakları verimli kullanmaya odaklanır. Bu, özellikle web ve mobil oyunlar için avantaj sağlar. Motorun bazı kapasite sınırları önceden belirlenir. Böylece gerekli bellek baştan ayrılabilir.

Godot'a kıyasla daha az hazır oynanış ve kullanıcı arayüzü öğesi bulabilirsiniz. Aynı sonuçları elde etmek için Defold bileşenlerini birleştirebilir veya genişletebilirsiniz. Defold, motorun çekirdeğini olabildiğince küçük tutar. Kullanmadığınız özellikleri çıkararak motoru daha da küçültebilir, yerel kod eklentileri (Native Extensions) ve Lua modülleriyle genişletebilirsiniz. [Defold Asset Portal](https://defold.com/assets/) üzerinde yüzlerce modül, kütüphane ve eklenti bulunur. Bunlarla örneğin karmaşık arayüzler oluşturabilir, gelişmiş işleme (rendering) hatları kurabilir veya geliştirme sırasında yaptığınız bazı işleri kolaylaştırabilirsiniz.

Defold'un özellikleri hakkında daha fazla bilgiyi [ürün sayfasında](https://defold.com/product/) bulabilirsiniz.

## Kurulum {#installation}

1. [İndirme sayfasından](https://defold.com/download/) işletim sisteminize uygun Defold sürümünü indirin.
2. Arşivi çıkarın ve düzenleyiciyi başlatın.

Ayrı bir merkez uygulaması veya dışa aktarma şablonları kurmadan ilk projenizi oluşturup çalıştırabilirsiniz. Platforma özgü yönergeler için [Kurulum kılavuzuna](/manuals/install/) bakın.

Defold'u doğrudan düzenleyiciden güncelleyebilirsiniz. Mevcut bir projeyi güncellerken sürüm notlarını okuyun ve oyunu hedef platformlarında test edin.

## Karşılama ekranı {#welcome-screen}

Defold açıldığında karşılama ekranından son projelerinizi açabilir veya yeni bir proje oluşturabilirsiniz. Bu ekran Godot'un proje yöneticisine benzer bir işlev görür.

![Godot proje yöneticisi ve Defold karşılama ekranı](images/godot/godot_1.png)

Defold'da yeni bir projeye şu seçeneklerden biriyle başlayabilirsiniz:

- **Templates** altında boş veya belirli bir platforma yönelik temel proje şablonları bulunur.
- **Tutorials** altında size adım adım yol gösteren başlangıç projeleri bulunur.
- **Samples** altında çalıştırıp inceleyebileceğiniz örnekler ve başlangıç paketleri bulunur.

![Godot proje yöneticisi ve Defold karşılama ekranı](images/godot/godot_2.png)

Defold'daki Samples bölümü, Godot Asset Store'daki başlangıç paketleri ve örnekler gibi, kendi projenizde temel alabileceğiniz projeler ve örnekler içerir.

![Godot proje yöneticisi ve Defold karşılama ekranı](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Defold düzenleyicisine genel bakış {#defold-editor-overview}

Ana bölmelerin adları ve konumları farklı olsa da işlevleri tanıdık gelecektir. Karşılaştırmayı kolaylaştırmak için Godot düzenleyicisindeki bölmeleri Defold'un varsayılan görünümüne göre yerleştirdik.

![Godot düzenleyicisine genel bakış](images/godot/godot_4.png)
![Defold düzenleyicisine genel bakış](images/godot/godot_5.png)

| Godot | Defold | Defold düzenleyicisindeki işlevi |
|---|---|---|
| FileSystem bölmesi | Assets | Projedeki dosya ve klasörleri yönetirsiniz. Buradaki yapı, diskteki proje dizininizle bire bir aynıdır. |
| 2B/3B görünüm ve kaynak düzenleyicileri | Ana düzenleyici | Açtığınız kaynağa (koleksiyon, GUI, atlas, betik vb.) göre değişir. İki bölmeye ayrılabilir. |
| Scene bölmesi | Outline | Geçerli kaynağın yapısını gösterir. Çalışma sırasında kullanılan genel bir sahne ağacı değildir. |
| Inspector | Properties | Seçili nesne, bileşen veya kaynağın özelliklerini gösterir. |
| Output ve Debugger | Tools | Console, Build Errors ve Search Results bölmelerini ve hata ayıklayıcıyı içerir. |
| Sürüm kontrolü tümleştirmesi | Changed Files | Projede Git kullanılıyorsa dosyalardaki değişiklikleri gösterir. |

Defold'un 3B düzenleyicisinde sağ üst köşede bir araç çubuğu da bulunur. Ayrıntılar için [Sahne düzenleme kılavuzuna](/manuals/scene-editing/#toolbar-overview) bakın.

### 2B ve 3B sahne yönelimi {#2d-and-3d-scene-orientation}

:[2B ve 3B sahne yönelimi](../shared/2d-and-3d-scene-orientation.md)

### Bölmeler {#panes}

Defold'daki bölmeleri ayrı pencerelere ayıramazsınız. Kenarlarını sürükleyerek boyutlarını değiştirebilir, `F6`, `F7` ve `F8` tuşlarıyla veya `View` menüsünden bölmeleri gösterip gizleyebilirsiniz.

![Bölmelerin görünürlüğü](images/editor/editor_panes.png)

### Koordinatlar {#coordinates}

2B bir projede varsayılan işleme betiğini kullanıyorsanız ve Defold koleksiyonunuzda kamera bileşeni yoksa `(0, 0)` koordinatları oyun penceresinin sol alt köşesine karşılık gelir. Pozitif Y **yukarıyı**, pozitif X sağı gösterir.

Godot'ta alışılmış 2B ekran koordinatlarında pozitif Y **aşağıyı** gösterir. Konumları veya hareket kodunu aktarırken bu farkı göz önünde bulundurun.

![Defold ve Godot'un 2B koordinatları arasındaki fark](images/godot/godot_6.png)

Godot'un 3B koordinat sisteminde pozitif Y, Defold'daki gibi yukarıyı gösterir. Defold, 2B ve 3B oyunlar için ortak bir 3B koordinat sistemi kullanır. Tipik bir 2B projede XY düzlemi ve ortografik izdüşüm kullanılır. Gerekirse kamerayı farklı yapılandırabilirsiniz.

![Defold ve Godot'un 3B koordinat sistemlerindeki benzerlik](images/godot/godot_7.png)

Ayrıntılar için [Defold düzenleyicisine genel bakış kılavuzuna](/manuals/editor/) bakın.

---

## Temel kavramlar {#key-concepts}

Godot'ta düğümleri bir araya getirerek **sahneler** oluşturursunuz. Defold'da bileşenlerle, oyun nesneleriyle ve oyun nesnelerinden oluşan koleksiyonlarla (collection) çalışırsınız.

Örneğin Godot'ta oyuncuyu bir `Node2D` düğümü ve onun altına eklediğiniz bir `Sprite2D` düğümüyle oluşturabilir, kök düğüme bir betik bağlayabilirsiniz. Ardından oyuncuyu ilk sahnenize (`Scene`) eklersiniz.
Defold'da aynı oyuncuyu `Sprite` ve `Script` bileşenleri içeren bir oyun nesnesi olarak oluşturup bir koleksiyona eklersiniz.

![Godot'taki bir düğüm yapısı ile Defold oyun nesneleri ve bileşenlerinin karşılaştırması](images/godot/key_concepts.png)

Bu kavramlar [Yapı taşları kılavuzunda](/manuals/building-blocks/) ayrıntılı olarak açıklanır.

### Oyun nesneleri {#game-objects}

Defold'da **oyun nesnesi**, bileşenler için bir *kapsayıcıdır* ve şunları sağlar:

- **Kimlik**
- **Dönüşüm** (konum, dönme, ölçek)

Bir oyun nesnesi, Godot'taki `Node2D` veya `Node3D` düğümüne benzer bir işlev görebilir. Defold'da ayrı bir 2B oyun nesnesi türü yoktur. 2B oyunlardakiler dahil tüm oyun nesneleri 3B dönüşüm kullanır.

Defold'da bir oyun nesnesini başka bir oyun nesnesinin altına bağlayabilirsiniz. Böylece alt nesne, üst nesnenin dönüşümünü devralır. Bu ilişkileri koleksiyonda düzenleyebilir veya çalışma sırasında değiştirebilirsiniz. Bir nesnenin üst nesnesini değiştirmek adresini etkilemez.

Bir koleksiyonda oyun nesnesini doğrudan `.collection` dosyasında **gömülü** olarak tanımlayabilir veya yeniden kullanılabilir bir `.go` prototipine başvuru olarak ekleyebilirsiniz. Gömülü nesnenin tanımını düzenlediğinizde bu koleksiyon değişir. Bağımsız olarak tanımlanmış diğer nesneler etkilenmez. Bir `.go` prototipini düzenlediğinizde, ona başvuran örnekler güncellenir. Örneğe özgü geçersiz kılmalar varsa bunlar korunur. Gömülü nesneler de dahil olmak üzere birden çok nesne aynı bileşen kaynağına başvurabilir. Kaynağı düzenlerseniz onu kullanan diğer nesneler de etkilenebilir. Bir koleksiyonu yeniden kullanıyorsanız gömülü nesnelerinde yaptığınız değişiklikler bu koleksiyona başvurulan her yerde görünür.

### Bileşenler {#components}

Bileşenler, oyun nesnelerine görünüm, fizik işlevleri, ses veya davranış gibi özellikler kazandıran yapı taşlarıdır.

Oyun nesnesine bir görüntü göstermek için `Sprite`, ses çalmak için `Sound`, Lua kodu çalıştırmak için de `Script` bileşeni ekleyin.

Bileşenler oyun nesnelerine aittir ve alt bileşen içeremez. Bir hiyerarşi oluşturmak için oyun nesneleri arasında koleksiyon içinde üst-alt ilişkileri kurun.

Godot'ta olduğu gibi bir bileşene betik ekleyerek davranışını değiştiremezsiniz. Bileşeni Properties bölmesinden ayarlayabilir, GDExtension'a benzer şekilde yerel kod eklentileriyle yeni özel bileşenler oluşturabilirsiniz. Defold'un desteklediği özel bileşenlere örnek olarak resmî [Rive](https://github.com/defold/extension-rive) ve [Spine](https://github.com/defold/extension-spine) bileşenleri ile topluluğun geliştirdiği [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) ve [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation) verilebilir.

Defold'da betik, herhangi bir oyun nesnesine eklenebilen ayrı bir bileşendir. Bir oyun nesnesine, betikler de dahil olmak üzere birden çok bileşen ekleyebilirsiniz.

Bileşenler kendi aralarında hiyerarşi oluşturmaz ve özel betiklerden bağımsızdır. Bu yapı sayesinde Defold, veri odaklı tasarımdan yararlanarak bileşenleri belleğe verimli biçimde yerleştirir.

| Godot düğümü | Defold bileşeni | Açıklama |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Bir atlastan (birden çok görüntü içeren doku) veya karo kaynağından alınan 2B dokuları ve kare dizisi animasyonlarını çizer. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` ve bunların 3B karşılıkları | [Çarpışma nesnesi](/manuals/physics-objects/) | Fizik etkileşimlerini ve tetikleyicileri yönetir. Çarpışma şekillerini ayrı alt düğümler olarak eklemek yerine doğrudan bu bileşenin içinde tanımlarsınız. Tür olarak statik, dinamik, kinematik veya tetikleyici seçebilirsiniz. |
| Bir düğüme bağlı `.gd` betiği | Script | Oyun mantığını çalıştıran, girdiyi işleyen ve diğer bileşenler ile oyun nesnelerini denetleyen Lua kodu içerir. |
| `TileMapLayer` | [Karo haritası](/manuals/tilemap/) | Karo kaynağını ve karo haritası katmanlarını kullanarak ızgara tabanlı bir harita çizer. |
| `Label` | [GUI metin düğümü](/manuals/gui-text/) | Arayüz metinleri için GUI metin düğümü, oyun dünyasındaki metinler için [etiket bileşeni](/manuals/label/) kullanın. |
| `AudioStreamPlayer` | [Ses](/manuals/sound/) | Ses çalar. Speed, Pan ve Gain özelliklerini ayarlayabilirsiniz. |
| `Camera2D` / `Camera3D` | [Kamera](/manuals/camera/) | Ortografik ve perspektif izdüşümü destekler. |
| `Control` hiyerarşisi / `CanvasLayer` | [GUI](/manuals/gui/) | Defold'da GUI bileşeni kendi düğüm hiyerarşisini (örneğin Box, Text, Pie) içerir. GUI davranışı için ayrı bir `.gui_script` kullanılır. |
| `MeshInstance3D` | [Model](/manuals/model/) veya [Örgü](/manuals/mesh/) | Model bileşeni içe aktarılan 3B içeriği, örgü bileşeni ise bir arabellekten alınan özel geometriyi destekler. |
| `CPUParticles2D` / `GPUParticles2D` ve bunların 3B karşılıkları | [ParticleFX](/manuals/particlefx/) | Defold'un parçacık düzenleyicisinde yapılandırdığınız 2B veya 3B parçacıkları yayar. |
| `PackedScene.instantiate()` | Fabrika / Koleksiyon fabrikası | Defold'da hangi oyun nesnelerinin veya koleksiyonların çalışma sırasında oluşturulabileceğini ayrı bileşenlerle tanımlarsınız. |

### Koleksiyonlar ve dünyalar {#collections-and-worlds}

Bir **koleksiyon**, oyun nesnelerini, bunların bileşenlerini ve aralarındaki üst-alt ilişkilerini tanımlar. Bir grup nesneyi yeniden kullanmak için bir koleksiyonu başka bir koleksiyona ekleyebilirsiniz. Bu, Godot'ta sahneleri iç içe kullanmaya benzer. Defold, Godot'taki gibi genel amaçlı sahne kalıtımı sunmaz. Bunun yerine prototipleri ve koleksiyonları yeniden kullanabilir, örnekleri özellikler veya betikler aracılığıyla özelleştirebilirsiniz.

Koleksiyon dosyasının kendisi çalışma sırasında bir nesneye dönüşmez. Üzerinde yöntem çağırabileceğiniz bir koleksiyon nesnesi veya koleksiyonun kendisine karşılık gelen bir kök düğüm yoktur. Dosya, Defold'un çalışma sırasında oyun nesnelerini, bileşenleri ve bunların hiyerarşisini oluştururken kullandığı tanımları içerir.

Defold, oyunu başlatırken `game.project` dosyasını okur. İlk olarak **Bootstrap ▸ Main Collection** ayarında belirtilen koleksiyonu yükler. Böylece başlangıçtaki oyun dünyası oluşturulur. İç içe koleksiyonlardaki nesneler de aynı dünyanın parçası olur.

**Koleksiyon fabrikası (Collection Factory)**, fabrikayı içeren **mevcut** dünyada bir grup oyun nesnesini ve bileşenlerini oluşturur.

**Koleksiyon vekili (Collection Proxy)** ise ayrı bir koleksiyon yükler. Böylece kendi adres alanı ve fizik simülasyonu olan **yeni bir dünya** oluşur. Örneğin bir düşmanın mevcut bölümün geometrisiyle etkileşime girmesini istiyorsanız onu aynı dünyada oluşturmanız gerekir. Bütünüyle yeni bir bölümü, gerekirse eşzamansız olarak yüklemek farklı bir işlemdir. Her ikisi de aşağıda açıklanmıştır.

Godot, hem örnek oluşturmak hem de sahne değiştirmek için `PackedScene` kullanır. `SceneTree` ile sahne değiştirmek, koleksiyon vekiliyle ayrı bir dünya yüklemeye benzer.

İki motordaki kavramları şöyle karşılaştırabiliriz:

| Godot | Defold | Açıklama |
|---|---|---|
| Alt düğümleri olan `Node3D` | Bileşenleri olan oyun nesnesi | Bileşenler nesnenin işlevlerini ve davranışını belirler. Oyun nesnesi dönüşüm ve kimlik sağlar. |
| `Node2D` / `Node3D` dönüşümü | Oyun nesnesinin dönüşümü | Her oyun nesnesinde yerleşik olarak bulunur. |
| Sahne / `PackedScene` | Oyun nesnesi prototipi (`.go`) veya koleksiyon (`.collection`) | Prototip tek bir nesneyi, koleksiyon ise bir grup nesneyi ve bunların hiyerarşisini tanımlar. |
| `PackedScene.instantiate()` | Fabrika veya koleksiyon fabrikası | Mevcut dünyada bir oyun nesnesi veya nesne grubu oluşturur ve nesnelerin tanımlayıcılarını döndürür. |
| `SceneTree` + `PackedScene.instantiate()` ile sahne değiştirme | Koleksiyon vekili | Yeni, ayrı bir dünya yükleyip oluşturur ve bu dünyada oyun nesneleri oluşturur. |

---

## Kod yazma {#code-writing}

Defold düzenleyicisi tüm metin dosyaları ve betikler için yerleşik bir metin düzenleyicisi sunar. Kod yazarken otomatik tamamlama ve biçimlendirmeden yararlanabilir, Structure görünümünde verileri ve işlevleri görebilirsiniz. Ayrıntılar için [Yerleşik kod düzenleyicisini kullanma bölümüne](/manuals/writing-code/#using-the-built-in-code-editor) bakın.

Defold'un tüm metin tabanlı dosyalarını ve betiklerini harici bir düzenleyicide de açabilirsiniz. Defold, VS Code gibi harici araçlarla tümleştirmeyi ve bu araçlardan Defold ile çalışmayı kolaylaştıran özellikler sunar. Ayrıntıları [Harici kod düzenleyicisi kullanma bölümünde](/manuals/writing-code/#using-an-external-code-editor) bulabilirsiniz.

### Lua ve betikler {#lua-and-scripts}

Defold'da oynanış betiklerini Lua ile yazarsınız. Lua size GDScript'i anımsatabilir ancak aralarında önemli farklar vardır. Defold, Lua'nın statik tür denetimli bir lehçesi olan Teal'i de destekler. GDExtension'a benzer biçimde, hedef platforma göre C, C++, C#, Objective-C, Java veya JavaScript ile yazılmış yerel kod eklentileri de kullanabilirsiniz. Bu eklentileri ileride ayrıca ele alacağız.

Defold'da başlıca şu Lua dosyalarıyla çalışırsınız:

| Dosya | Amacı |
|---|---|
| `.script` | Oyun mantığını ve davranışını tanımlar. Diğer oyun nesnelerini ve bileşenleri denetlemek için `go`, `factory`, `sprite`, `tilemap` veya `physics` gibi API'leri kullanır. |
| `.gui_script` | GUI'ye özgüdür. Arayüzün davranışını `gui` API'siyle tanımlar. |
| `.render_script` | `render` API'siyle görüntünün işlenmesini yönetir. |
| `.lua` | `require()` ile yüklenen, yeniden kullanılabilir Lua modülleridir. Kod kütüphaneleri veya yardımcı betikler gibi düşünebilirsiniz. |

Lua tabloları veri, işlev veya ikisini birden içerebilir. Kodunuzu düzenlemek için GDScript'in sınıf hiyerarşisini yeniden kurmanız gerekmez. Yeniden kullanacağınız mantığı modüllere yerleştirin ve ilgili davranıştan sorumlu betikten çağırın.

Defold'un betik ortamı Lua 5.1 ile uyumludur. Dil farkları ve platforma özgü ayrıntılar için [Defold'da Lua kılavuzuna](/manuals/lua/) bakın.

### Uygulama yaşam döngüsü {#application-lifecycle}

Bir Defold oyunu genel olarak başlangıç aşamasıyla başlar ve sonlandırma aşamasıyla biter. Bu iki aşama arasında her karede çalışan güncelleme döngüsü dönüşümleri ve bileşenleri günceller, kodu çalıştırır ve iletileri işler.

![Defold'da uygulama yaşam döngüsü](images/application_lifecycle/application_lifecycle.png)

Godot dahil diğer birçok oyun motorunda olduğu gibi, Defold betiklerinde de uygulamanın yaşam döngüsü boyunca çağrılan Lua geri çağırım işlevleri vardır. İsimleri farklı olsa da görevleri tanıdık gelecektir.

| Godot | Defold | Açıklama |
|---|---|---|
| `_ready()` | `init(self)` | Örneğin verilerini hazırlayın ve gerekiyorsa girdi odağını alın. |
| `_process(delta)` | `update(self, dt)` | Her karede bir kez güncelleyin. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | Etkinleştirildiğinde sabit zaman adımlarıyla güncelleyin. |
| `_input(event)` | `on_input(self, action_id, action)` | Nesnenin girdi dinleyicilerine iletilen girdiyi işleyin. |
| Sinyal geri çağırımı | `on_message(self, message_id, message, sender)` | Betiklerden veya motor bileşenlerinden gelen iletileri alın. |
| `_exit_tree()` | `final(self)` | Betik örneği sonlandırılırken temizlik işlemlerini yapın. |

Godot, alt düğümlerin `_ready()` yöntemlerini üst düğümünkinden önce çağırır. Defold ise oyun nesneleri ve bileşenler için belirli bir başlatma veya güncelleme sırası garanti etmez. Nesneler arasında eşgüdüm sağlarken bir nesnenin `init()` işlevinin önce çalışacağına güvenmek yerine iletileri kullanın.

`fixed_update()` kullanacaksanız `game.project` dosyasında **Engine ▸ Fixed Update Frequency** değerini 60 gibi pozitif bir sayıya ayarlayın ve **Physics ▸ Use Fixed Timestep** seçeneğini etkinleştirin.

Defold, kamerayı ayarlamak gibi normal güncellemelerden sonra, görüntü işlenmeden önce yapılacak işler için `late_update(self, dt)` işlevini de sunar. Gerekirse bunun ardından dönüşümler son bir kez güncellenebilir.

Bir bileşeni devre dışı bırakmakla silmek ayrı işlemlerdir.

Aşamaların sırasını ve her betik türünde kullanabileceğiniz geri çağırımları [Uygulama yaşam döngüsü kılavuzunda](/manuals/application-lifecycle/) bulabilirsiniz.

### Örneğe özgü veriler ve yerel veriler {#instance-data-vs-local-data}

Her betik bileşeni örneği, geri çağırımlarda kendine ait bir `self` değeri alır. `self.health` veya `self.target` gibi örneğe özgü durum bilgilerini burada saklayabilirsiniz. Aynı oyun nesnesindeki iki betik bileşeninin bile `self` değerleri ayrıdır. `self` bir Lua tablosu değildir. Alanlarına tablo alanları gibi erişilebilen bir userdata değeri olduğu için `pairs(self)` gibi işlemler çalışmaz. Godot'ta örnek değişkenleri (`var`) benzer bir amaca hizmet eder.

Godot, her `.gd` dosyasını bir sınıf tanımı olarak ele alır. Bir `.gd` dosyasını 10 düşmana bağladığınızda sınıftan 10 ayrı nesne oluşturur. Dosyanın en üst düzeyinde var ile bildirdiğiniz değişkenlerin her nesnede ayrı birer kopyası olur.

Defold, betik kaynağını yüklediğinde `.script` dosyasını bir Lua kod bloğu olarak çalıştırır. Her betik bileşeni örneği `init(self)` ve `update(self, dt)` gibi yaşam döngüsü geri çağırımlarında kendine ait `self` değerini alır.

Buna karşılık bir Defold `.script` dosyasının en üst düzeyinde tanımlanan yerel değişken, o betiğin **tüm örnekleri** arasında paylaşılır. Godot'taki statik değişkenler (`static var`), Defold'daki dosya kapsamlı yerel değişkenlere karşılık gelir.

![Defold'da örneğe özgü veriler ile yerel veriler arasındaki fark](images/lua/self_local.png)

Yukarıdaki örnekte bir örneğin `self.has_shield` değerini `true` olarak değiştirmek diğer örnekleri etkilemez. Buna karşılık `color` yerel değişkeni bu betik dosyasını kullanan örnekler arasında paylaşılır. Değerini değiştirmek tüm bu örnekleri etkileyebilir.

### Özellikler {#properties}

Örneğe ait düzenlenebilir bir **özellik** tanımlamak için `go.property()` kullanın. Bu özelliğe `self` üzerinden erişirsiniz. Godot'taki `@export` gibi, bu işlem değeri düzenleyicide görünür kılar. Defold'da bu özellikleri `Properties` bölmesinde bulabilirsiniz.

![Defold düzenleyicisinde özellikler](images/script-properties/properties.png)

Karşılaştırmak için Godot'ta bir `Node3D` düğümüne bağlı **GDScript** betiğine bakın:

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

Defold'da betik bileşeni olarak eklenen **Lua** kodu şöyledir:

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Lua özelliğine `self.speed` üzerinden erişirsiniz. Nesneyi oluştururken de bu özelliğe değer verebilirsiniz. Defold'da dönüşümler 2B'de bile `vector3` kullandığından Z koordinatı da belirtirsiniz.

Desteklenen özellik türleri için [Betik özellikleri kılavuzuna](/manuals/script-properties/), daha fazla örnek için [Betikler kılavuzuna](/manuals/script/) bakın.

---

## İletiler ve adresleme {#messages-and-addressing}

Godot'ta bir nesne, sinyal aracılığıyla kendisine bağlı dinleyicilere bir olayı bildirebilir. Defold betiklerinde iletişim için genellikle bir oyun nesnesinin veya bileşenin adresine ileti (message) gönderirsiniz.

Defold'da herhangi bir betikten `msg.post()` işleviyle ileti gönderebilir, gelen iletileri betiğin `on_message()` geri çağırımında alıp işleyebilirsiniz.

![Defold'da iletiler](images/message_passing/messages_overview.png)

Örneğin oyuncu, puandaki değişikliği ekrandaki göstergeye (HUD) bildirebilir.

Godot'ta `Player` (`Node2D`), `player.gd` betiğini kullanır. Aynı üst düğüme bağlı `GUI` (`CanvasLayer`) ise `gui.gd` betiğini kullanır ve `ScoreText` adlı bir Label düğümü içerir.

![Godot'ta sinyal örneğinin düğüm yapısı](images/godot/godot_signals.png)

Defold'da `player` oyun nesnesine `player.script` eklenmiştir. `hud` oyun nesnesinde `gui` bileşeni vardır. Bu bileşen `score` adlı bir metin düğümü içerir ve `hud.gui_script` betiğini kullanır.

![Defold'da ileti örneğinin nesne ve bileşenleri](images/godot/defold_messages.png)

### İleti gönderme {#sending-messages}

Godot'ta Player ve GUI aynı üst düğüme bağlıdır. Player, `score_changed` sinyalini GUI betiğindeki bir yönteme bağlar. Bu yöntem de Label düğümünü günceller.

**GDScript**, `player.gd`:

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

Godot'ta `Player`, `score_changed` adında bir sinyal tanımlar. `_ready()` sırasında bu sinyali GUI betiğinin `set_score()` yöntemine bağlar. `collect()` her çağrıldığında puan artar ve sinyal yeni değeri dinleyicilere bildirir.

Defold'da girdi eşlemelerinde **Space** tuşunu `collect` eylemine bağlayın. `player`, `init()` içinde puanının başlangıç değerini ayarlar ve girdi olaylarını almak için girdi odağı ister. `collect(self)` çağrıldığında puanı bir artırır ve `/hud#gui` adresine `score_changed` iletisini gönderir. İletinin veri tablosu yeni puanı içerir.

**Lua**, `player.script`:

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

Godot'tan farklı olarak Defold'da oyuncunun GUI'ye önceden bir sinyal bağlaması gerekmez. İletiyi alıcının adresine göndermesi yeterlidir. Defold'un göreli adresleme özelliğini bu şekilde kullanarak yeniden kullanılabilir işlevler ve betikler yazabilirsiniz.

### İletileri alma ve işleme {#receiving-and-handling-messages}

Ardından GUI, değeri alır ve puanı gösteren metni günceller.

`GUI` (`CanvasLayer`) düğümüne bağlı **GDScript** betiği `gui.gd`:

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

GUI betiği, sinyalin ilettiği değeri `set_score()` yoluyla alır. Ardından alt düğümü olan `ScoreText` etiketini günceller. Player, etikete doğrudan erişmez ve onu kendisi değiştirmez.

Defold'da GUI betiği önce `gui.get_node()` ile puanı gösteren metin düğümünü alır. GUI bileşeni bir ileti aldığında `on_message()` iletinin tanımlayıcısını denetler. Tanımlayıcı `score_changed` ise betik `message.value` değerini okur ve `gui.set_text()` ile metni günceller.

GUI bileşenine atanmış **Lua** betiği `hud.gui_script`:

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

Defold'da iletinin adresi, puanı gösteren metin düğümünü değil, GUI **bileşenini** belirtir. İletiyi nasıl kullanacağına ve hangi metin düğümünü güncelleyeceğine alıcı GUI betiği karar verir.

İki ekran görüntüsünde de başlangıç metni `Score: 0` olarak görünür. Örnek betikler, puan değiştiğinde metnin tamamını yeni sayısal değerle değiştirir.

`msg.post()` alıcıyı hemen çağırmaz. İletiyi daha sonra dağıtılmak üzere kuyruğa ekler ve alıcı betikten bir sonuç döndürmez. İletiler çoğu zaman aynı karede dağıtılır ancak dağıtım turu sayısı sınırlıdır. Uzun bir ileti zinciri sonraki kareye sarkabilir. Yanıt vermesi gereken alıcı, `on_message()` işlevine iletilen gönderen URL'sini kullanarak ilk gönderene başka bir ileti gönderebilir. Ayrıntılar için [İleti zincirleri bölümüne](/manuals/message-passing/#message-chains) bakın.

Birden çok dinleyiciyle iletişimde de fark vardır. Godot'ta bir sinyali birden çok yönteme bağlayabilirsiniz. Sinyal yayıldığında bağlı dinleyicilerin tümü bilgilendirilir. Defold'da ise bir ileti belirli bir adrese gönderilir. Birden çok alıcıyı bilgilendirmek için her birine ayrı bir ileti gönderebilir veya oyununuzda bir abonelik sistemi kurabilirsiniz.

### Bir nesneyi bulma ve Defold'da adresleme {#finding-an-object-addressing-in-defold}

Başka bir betik örneğini temsil eden bir Lua nesnesi döndüren genel amaçlı bir `get_node()` karşılığı yoktur. Bunun yerine `go.get_position()`, `go.set()` veya `msg.post()` gibi bir motor API'sine bir tanımlayıcı veya **URL** verirsiniz.

Defold'da bir URL üç bölümden oluşur:

```lua
socket:/path#component
```

- **Soket (socket)**, başlangıçtaki ana koleksiyonun dünyası veya koleksiyon vekiliyle yüklenmiş bir dünya gibi, bir oyun dünyasını belirtir.
- **Yol (path)**, o dünya içindeki bir oyun nesnesini belirtir.
- **Bileşen (component)**, o nesnenin bir bileşenini belirtir.

Tam URL kullanabilir veya bazı bölümleri atlayarak göreli bir adres oluşturabilirsiniz. Örneğin bir betik, aynı oyun nesnesindeki bir bileşene yalnızca bileşen bölümünü yazarak ulaşabilir. Sık kullanılan biçimler şunlardır:

| Adres | Anlamı |
|---|---|
| `"#sprite"` | Geçerli oyun nesnesindeki sprite bileşeni. |
| `"/player#controller"` | Geçerli dünyadaki player nesnesinin controller bileşeni. |
| `"level:/player#controller"` | Yüklenmiş olan level adlı dünyadaki player nesnesinin controller bileşeni. |
| `"."` | Geçerli oyun nesnesinin (`Game Object`) kısa gösterimi. Bu adrese gönderilen ileti nesnenin bileşenlerine iletilir. |
| `"#"` | Geçerli betik (`Script`) bileşeninin kısa gösterimi. |

İç içe koleksiyonlar nesne yollarına ön ek ekleyebilir. Ancak dönüşümlerin aktarımı için kurulan üst-alt ilişkisi nesnenin adresini değiştirmez.

Çalışma sırasında oluşturduğunuz nesnelere daha sonra erişmek için `factory.create()` veya `collectionfactory.create()` tarafından döndürülen tanımlayıcıları kodunuzda saklayın.

Godot'ta oynanışla ilgili sorgular veya `call_group()` için kullanılan grupların Defold'da yerleşik bir karşılığı yoktur. Bu amaçla kendi nesne kaydınızı tutmanız veya iletileri yönlendirmeniz gerekir.

Defold'da çarpışma nesnelerinin fizik grupları, çarpışmaları filtreler. Bir grubun hangi gruplarla çarpışabileceğini maske belirler. Bu grupların ileti sistemiyle ilişkisi yoktur.

[Adresleme](/manuals/addressing/) ve [İleti aktarımı](/manuals/message-passing/) kılavuzlarını erkenden okuyun. İlk projenizde karşılaşacağınız pek çok sorunun yanıtını bu kılavuzlarda bulabilirsiniz.

---

## Autoload ve paylaşılan durum {#autoloads-and-shared-state}

Defold'un ileti sistemiyle haberleşmeye ek olarak, Lua modüllerindeki işlevleri doğrudan çağırabilirsiniz.

Godot'ta veri paylaşmak için **Autoload** kullanıyorsanız Defold'da aynı işi bir Lua modülüyle yapabilirsiniz. Örneğin modülü `modules/game_state.lua` adıyla kaydedin ve `require "modules.game_state"` ile yükleyin.

`game_state.gd` dosyasının `GameState` adıyla Autoload olarak kaydedildiği **GDScript** örneği:

```gdscript
extends Node
var score: int = 0
```

**Lua** karşılığı, `modules/game_state.lua`:

```lua
local M = { score = 0 }
return M
```

Artık başka bir betik de paylaşılan veriyi kullanabilir.

**GDScript**:

```gdscript
func add_point():
    GameState.score += 1
```

**Lua**:

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

`require()` işlevi modülü önbelleğe alır. Böylece modülü yükleyen betikler, modülün döndürdüğü tabloyu paylaşır. Oyun nesnesi, GUI ve işleme betikleri aynı Lua durumunu paylaşır. Koleksiyon vekiliyle yüklenen dünyayı bellekten kaldırmak modülün verilerini sıfırlamaz. Yeni bir oyuna başlarken bu verileri kodunuzda sıfırlayabilirsiniz.

Defold'da bir Lua modülü oyun nesnesi değildir ve yaşam döngüsü, ileti veya girdi geri çağırımlarını almaz. Godot'ta Autoload ile her karede kod çalıştırıyor, ses çalıyor veya bölüm geçişlerini yönetiyorsanız bu davranışı koleksiyondaki bir nesnenin betiğine yerleştirin. Yaşam döngüsü geri çağırımlarını işlemek için bir modülde işlev tanımlayıp onu betiğinizden de çağırabilirsiniz.

`my_module` Lua modülü:

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Lua betiği:
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Örneğe özgü veriler için modül, her çağrıldığında yeni bir tablo oluşturan bir işlev döndürebilir. Dönen tabloyu `self` üzerinde saklayabilirsiniz. Ayrıntılar ve çalışma sırasında yeniden yüklemeyle ilgili noktalar için [Modüller kılavuzuna](/manuals/modules/) bakın.

---

## Nesneleri oluşturma ve bölümleri yükleme {#spawning-objects-and-loading-levels}

### Fabrikalar {#factories}

Defold'da tek bir oyun nesnesi oluşturmak için bir **fabrika (Factory)** bileşeni ekleyin ve **Prototype** özelliğini kullanacağınız `.go` dosyasına ayarlayın.

Bir koleksiyon için benzer şekilde bir **koleksiyon fabrikası (Collection Factory)** ekleyin ve kullanacağınız `.collection` dosyasını belirtin. Fabrika bir grup nesne oluştururken aralarındaki üst-alt ilişkilerini korur.

Örneğin Godot'ta aşağıdaki `Node2D` düğümü sahnemizin koordinat başlangıcında bulunur. Düğüme bağlı betik mermi örnekleri oluşturur.

**GDScript**:

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

Defold'da bir oyun nesnesine `bullet_factory` tanımlayıcılı fabrika bileşenini ekledik. Fabrikanın `Prototype` özelliğinin işaret ettiği oyun nesnesini `factory.create()` işleviyle oluşturabiliriz.

![Defold'da fabrika bileşeninin yapılandırılması](images/godot/defold_factory.png)

Ekran görüntüsünde fabrika `init()` içinde çağrılır. Aşağıdaki yardımcı işlev, nesnenin oluşturulacağı konumu nasıl belirteceğinizi ve tanımlayıcısını nasıl döndüreceğinizi gösterir.

**Lua**:

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

Defold işlevi, üzerinde yöntem çağırabileceğiniz bir nesne yerine bir nesne **tanımlayıcısı** döndürür. Bu tanımlayıcıyı `go` işlevlerine verebilirsiniz. Oluşturulan nesnede `controller` adlı bir betik bileşeni varsa `msg.url(nil, id, "controller")` ile bileşenin URL'sini oluşturabilirsiniz.

Koleksiyon fabrikası, prototipteki nesne tanımlayıcılarını yeni oluşturulan nesnelerin tanımlayıcılarıyla eşleyen bir tablo döndürür. Oluşturulan nesneleri daha sonra silmek için bu tabloyu saklayın.

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

Godot'taki `queue_free()` işlevinin aksine `go.delete(id)` varsayılan olarak alt nesneleri silmez. Bir nesneyi ve o anda alt hiyerarşisinde bulunan tüm nesneleri silmek için `go.delete(id, true)` kullanın. Fabrikanın döndürdüğü tabloyu `go.delete(ids)` işlevine verdiğinizde yalnızca listelenen nesneler silinir. Sonradan bunların altına bağlanan diğer nesneler silinmez. Bilinen bir kök nesneyi özyinelemeli olarak silerseniz o anda ona bağlı tüm alt nesneler de silinir. Ayrıntılar için [`go.delete()` başvuru belgesine](/ref/go/#go.delete) bakın.

Defold, oyun nesneleri ve bileşenleri için önceden yer ayırır. Bir sınıra ulaşıldığı için nesne oluşturulamıyorsa `game.project` dosyasında **Collection ▸ Max Instances** ayarını ve ilgili bileşen sınırlarını kontrol edin. Tüm sınırları artırmak bellek kullanımını da artırır.

Özellikler, dönüşümler ve dinamik yükleme için [Fabrika](/manuals/factory/) ve [Koleksiyon fabrikası](/manuals/collection-factory/) kılavuzlarına bakın.

### Koleksiyon vekilleri {#collection-proxies}

Defold'da bir koleksiyonu, örneğin bir oyun bölümünü yüklemek için bölümler arasında varlığını sürdüren bir nesneye **Collection Proxy** bileşeni ekleyin. **Collection** özelliğini ilgili `.collection` dosyasına ayarlayın.

![Defold'da koleksiyon vekilinin yapılandırılması](images/godot/defold_proxy.png)

`msg.post()` ile `"load"` veya `"async_load"` iletisini gönderin. Yükleme bittiğinde vekil `"proxy_loaded"` iletisiyle yanıt verir. Ardından on_message işlevinin `sender` parametresiyle gelen adrese `"init"` ve `"enable"` iletilerini göndererek yüklenen dünyayı başlatıp etkinleştirebilirsiniz.

Böylece hangi dünyaların yüklü ve çalışır durumda olduğunu siz belirlersiniz. Godot'taki sahne değişiminin aksine mevcut sahne kendiliğinden değiştirilmez. Başka bir koleksiyonu bellekten kaldırmak için vekiline `"unload"` gönderin. Vekil, dünyayı bellekten kaldırmadan önce otomatik olarak devre dışı bırakıp sonlandırır ve ardından `"proxy_unloaded"` iletisiyle yanıt verir. Bu aşamaları ayrı ayrı yönetmek istiyorsanız `"disable"` ve `"final"` iletilerini kendiniz de gönderebilirsiniz.

Farklı koleksiyon vekillerinin yüklediği dünyalardaki çarpışma nesneleri, iki dünya aynı anda yüklenmiş ve ekranda görünür olsa bile birbirleriyle çarpışmaz. Ancak bu dünyalardaki oyun nesneleri ve bileşenler, hedef soketi içeren URL'lerle birbirlerine ileti gönderebilir.

Bölüm geçişlerini uygulamadan önce [Koleksiyon vekili kılavuzunu](/manuals/collection-proxy/) okuyun. Kılavuzda bir dünyayı yükleme, bellekten kaldırma, girdiyi iletme ve yüklenmiş dünyanın güncelleme hızını denetleme konuları açıklanır.

## Proje kaynakları ve varlıkları {#project-resources-and-assets}

Defold projesi `game.project` dosyasını, betikleri ve kaynakları içeren bir klasördür. **Assets** bölmesi bu klasör yapısını yansıtır. Defold kaynak tanımlarının çoğu metin dosyası olduğundan sürüm kontrolüyle değişiklikleri inceleyebilirsiniz.

Oyunu derlediğinizde veya dağıtım için paketlediğinizde Defold, kaynakları çalışma zamanı biçimlerine dönüştürür. Ana koleksiyon, fabrikalar ve koleksiyon vekilleri üzerinden başvurulan kaynaklar bir bağımlılık ağacı oluşturur. Proje klasörüne koyduğunuz bir dosyaya başvuru yoksa bu dosya pakete eklenmez.

Godot'taki özel `Resource` sınıflarının ve `.tres` dosyalarının Defold'da tek bir genel amaçlı karşılığı yoktur. Motorun kullandığı içerik için Defold kaynak türlerini, kendi oyun verileriniz için Lua tablolarını veya veri dosyalarını kullanın. [`resource` API'si](/ref/resource/) desteklenen kaynakları çalışma sırasında oluşturmanıza veya değiştirmenize olanak tanır.

Normal bir fabrikanın kaynakları fabrikayla birlikte yüklenir. Yüklemeyi ertelemek için **Load Dynamically** seçeneğini etkinleştirin. Ardından `factory.load()` veya `collectionfactory.load()` ile kaynakları eşzamansız olarak yükleyip kullanıma hazır hale getirebilirsiniz. Koleksiyon vekilinin içeriği ise yüklenmesini istediğinizde yüklenir.

İçeriği daha sonra dağıtım paketinden yüklemek ile daha sonra indirmek ayrı işlemlerdir. Defold'un [Live Update](/manuals/live-update/) özelliğiyle içeriği ilk dağıtım paketinin dışında tutabilir ve ayrı olarak sunabilirsiniz.

Ayrıntılar için [Kaynak yönetimi kılavuzuna](/manuals/resource/) bakın.

---

## Girdi {#input}

Godot'taki `InputMap`, Defold'da `.input_binding` dosyasına karşılık gelir. Bir aygıt girdisini (klavye, oyun kumandası, fare, dokunma veya metin) bir eylem adına bağlayabilirsiniz. Eşleme dosyasını `game.project` içinde **Input ▸ Game Binding** ayarından seçin.

![Girdi eşlemeleri](images/input/defold_input.png)

Defold'da girdiyi alacak oyun nesnesinin **girdi odağını alması** gerekir. Böylece nesne girdi yığınına eklenir. Artık nesnenin betik ve GUI bileşenleri `on_input()` geri çağırımlarını alabilir.

Ekran görüntüsünde boşluk tuşu `collect` eylemine bağlanmıştır. Aşağıdaki ayrı örnekte ise `fire` adlı bir eylem kullanılır. Onu da girdi eşlemelerinize eklemeniz gerekir.

**GDScript**:

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua**:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

`action` tablosu, girdi türüne göre `pressed`, `released` ve `value` gibi değerler içerir.

Girdi, odağı en son alan dinleyiciden başlayarak yığın boyunca ilerler. Örneğin bir menü tıklamayı işlediğinde eylemi tüketmek ve alttaki dinleyicilere geçmesini önlemek için `on_input()` işlevinden `true` döndürün.

Bir koleksiyon vekiliyle yüklenen dünyada, hem vekili taşıyan nesnenin hem de o dünyadaki dinleyicilerin girdi odağını alması gerekir. Bölüm değişince daha önce çalışan bir betiğe girdi gelmemesinin yaygın bir nedeni bu adımlardan birinin atlanmasıdır.

Ayrıntılar için [Girdi](/manuals/input/), [Fare ve dokunma](/manuals/input-mouse-and-touch/) ve [Oyun kumandaları](/manuals/input-gamepads/) kılavuzlarına bakın.

---

## Fizik ve çarpışmalar {#physics-and-collisions}

Defold'daki **çarpışma nesnesi (Collision Object)**, Godot'taki fizik gövdelerine karşılık gelir. Fizik ayarlarını **ve** çarpışma şekillerini tek bileşende birleştirir. Defold'da `game.project` dosyasından 2B veya 3B fiziği seçebilirsiniz. Ayrıca App Manifest ile kullanılacak fizik motoru sürümünü seçebilir veya fiziği tamamen devre dışı bırakabilirsiniz.

Defold dört çarpışma nesnesi türü sunar:

| Godot | Defold türü | Açıklama |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Hareket etmez. Dinamik nesneler onunla etkileşir. |
| `RigidBody2D` / `3D` | `Dynamic` | Fizik motoru hareketi simüle eder ve çarpışmaları çözer. |
| `CharacterBody2D` / `3D` | `Kinematic` | Fizik motoru çarpışmalarla ilgili tüm verileri sağlar. Tepkiyi ve çarpışma çözümünü kodunuz belirler. |
| `Area2D` | `Trigger` | Fiziksel tepki üretmeden yalnızca giriş ve çıkış olaylarını bildirir. |

Defold'daki kinematik bir nesne, `move_and_slide()` kullanan bir `CharacterBody2D` ile tam olarak aynı davranmaz. Defold temasları algılar ve tüm verileri çarpışma yanıtı iletisinde size verir. Hareketi ve temasa verilecek tepkiyi ise betiğiniz belirler. Bir karakter denetleyicisi oluştururken [Çarpışmaları çözme kılavuzuna](/manuals/physics-resolving-collisions/) bakın.

Gruplar ve maskeler, numaralı çarpışma katmanları yerine adlar kullanır. Çarpışmanın kaydedilmesi için **her iki nesnenin maskesinde de diğer nesnenin grubu bulunmalıdır**.

![Defold'da çarpışma grupları ve maskeleri](images/physics/collision_groups.png)

Bu ekran görüntüsünde `danger` adlı oyun nesnesi `player` grubunu, `player` adlı nesne ise `danger` grubunu kullanır. Grup adlarının nesne tanımlayıcılarıyla eşleşmesi gerekmez. Buradaki maskeler iki grubun birbiriyle etkileşmesine izin verir.

Varsayılan olarak çarpışma nesneleri, ait oldukları oyun nesnelerinin betiklerine ileti gönderir. `"collision_response"`, `"contact_point_response"` veya `"trigger_response"` iletilerini `on_message()` içinde işleyin. Tetikleyici iletilerindeki `enter` alanı girişi çıkıştan ayırır. Nesneler temas halinde kaldığı sürece çarpışma ve temas iletileri yinelenebilir. Her iletinin yeni bir vuruş anlamına geldiğini varsaymayın.

Fizik olaylarını bir [çarpışma olayı dinleyicisiyle](/manuals/physics-events/) de işleyebilirsiniz. Dinleyici kullanmak varsayılan fizik iletisi dağıtımının yerini alır ve bu iletiler artık gönderilmez. İki yöntemden hangisini kullanacağınızı buna göre seçin.

Basit geometrik şekillerden karmaşık şekillere kadar çeşitli çarpışma şekilleri kullanabilirsiniz. Ayrıntılar için [Çarpışma şekilleri kılavuzuna](/manuals/physics-shapes) bakın.

![Örgü çarpışma şekli](images/physics/mesh.png)

Ayrıntılar ve ilgili API'ler için [Fiziğe genel bakış](/manuals/physics/), [Çarpışma nesneleri](/manuals/physics-objects/), [Çarpışma iletileri](/manuals/physics-messages/) ve [Işın sorguları](/manuals/physics-ray-casts/) kılavuzlarına bakın.

---

## GUI

Defold'da arayüzü bir `.gui` dosyasından oluşturulan **GUI bileşeni** içinde tasarlarsınız. Burada kutu, metin ve daire dilimi gibi GUI düğümlerini yerleştirebilirsiniz. Godot'ta bir `CanvasLayer` düğümüne bağlı betik gibi, bu bileşeni de ona özel bir `.gui_script` yönetir.

Bu düğümler GUI'ye aittir. Oyun nesnesinin dönüşüm hiyerarşisinin parçası değildir. Varsayılan olarak GUI, oyunun üzerine çizilir ve oyun kamerasıyla veya GUI bileşenini taşıyan nesneyle birlikte hareket etmez.

Düğümleri denetlemek için GUI bileşenine bir `.gui_script` atayın. Bu betikte `gui.get_node()`, `gui.set_text()` ve diğer `gui` işlevlerini kullanabilirsiniz. `gui` API'si yalnızca GUI betiklerinde, `go` API'si ise yalnızca oyun nesnesi betiklerinde kullanılabilir. Yukarıdaki puan örneğinde olduğu gibi bu iki betik arasında iletilerle haberleşin.

Şablonlar sayesinde başka bir GUI'nin düğüm hiyerarşisini yeniden kullanabilirsiniz. Bu, Godot'ta bir düğümü yeniden kullanmaya benzer.

Defold, Godot'taki Button veya yerleşim için kullanılan Container türleri gibi hazır arayüz denetimleri yerine, arayüzü oluşturacağınız basit düğümler sunar. Örneğin düğme oluşturmak için bir kutu ve bir metin düğümünü bir araya getirin. Girdiyi GUI betiğinde işleyin ve işaretçinin düğmenin üzerinde olup olmadığını `gui.pick_node()` ile denetleyin.

Defold, GUI'de Godot'un `CanvasLayer` katmanlarına benzer şekilde **Layers** kullanımını da destekler. Defold'da katmanları sayılarla değil adlarla tanımlarsınız. Çizim sırasını katmanların "Layers" listesindeki sırası belirler.

Sabitleme noktaları, dayanak noktaları, uyarlama modları ve [GUI yerleşimleri](/manuals/gui-layouts/) arayüzü farklı ekranlara uyarlamanıza yardımcı olur. Bunlar Godot'un yerleşim Container düğümlerine benzer ancak görevleri bire bir aynı değildir.

Daha büyük veya karmaşık bir arayüz için kendi yerleşim ve denetim kodunuzu ekleyebilir veya [Druid](https://defold.com/assets/druid/) gibi bir topluluk kütüphanesi kullanabilirsiniz.

Ayrıntılar için [GUI](/manuals/gui/) ve [GUI betiği](/manuals/gui-script/) kılavuzlarına bakın.

## Animasyon {#animation}

Defold'da `AnimationPlayer` düğümünün tek bir karşılığı yerine farklı animasyon araçları vardır:

- **Kare dizisi animasyonu**, sprite bileşenlerinde ve GUI kutularında görüntü dizilerini oynatır.
- **Model animasyonu**, içe aktarılan iskelet animasyonlarını 3B modellerde oynatır.
- **Özellik animasyonu**, `go.animate()` veya `gui.animate()` ile özelliğin başlangıç ve bitiş değerleri arasındaki ara değerleri hesaplar.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** ve **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** eklentiler aracılığıyla kullanabileceğiniz diğer animasyon biçimleridir.

### Ara geçişler (Tween) ve Defold'da özellik animasyonları {#tweens-defold-property-animations}

Godot'taki basit bir ara geçiş animasyonu (Tween), Defold'da bir özellik animasyonuna karşılık gelir. Bu iki örnek de bir nesneyi yarım saniyede `X = 200` konumuna taşır.

Bir `Node2D` düğümündeki **GDScript** betiği:

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

Bir oyun nesnesi betiğindeki **Lua** kodu:

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Birden çok özelliği değiştiren, ses çalan veya oynanış olaylarını tetikleyen bir dizi oluşturmak için adımları Lua'da yönetin. Defold'da henüz animasyon için özel bir zaman çizelgesi düzenleyicisi yoktur. Tools bölmesindeki Curve Editor, ParticleFX parçacıklarının yaşam süresi boyunca özelliklerinin nasıl değiştiğini belirleyen eğrileri düzenlemek için kullanılır.

[Animasyon](/manuals/animation/), [Özellik animasyonu](/manuals/property-animation/), [Kare dizisi animasyonu](/manuals/flipbook-animation/) ve [Model animasyonu](/manuals/model-animation/) kılavuzlarına bakın. Genel bakış kılavuzunda Spine ve Rive eklentilerinin bağlantılarını da bulabilirsiniz.

## Karo haritaları {#tilemaps}

Defold'un `Tilemap` bileşeni, karoların ızgara biçiminde dizildiği bir **karo kaynağı** kullanır. Yerleşik karo haritası düzenleyicisinde katmanlara karolar çizebilir, çalışma sırasında bunları `tilemap` API'siyle değiştirebilirsiniz.

Defold'un yerleşik karo haritası dikdörtgen bir ızgara kullanır. Godot'un arazi kümelerini ve otomatik karo yerleştirme kurallarını henüz doğrudan Defold'a aktaramazsınız. Gereken davranışı kodla sağlayabilir veya [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) ya da [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold) gibi Defold'a dışa aktarımı destekleyen bir harita aracı kullanabilirsiniz.

[Karo haritası kılavuzuna](/manuals/tilemap/) bakın.

---

## İşleme hattı {#rendering-pipeline}

Defold'da özel bir `.render` dosyası, bir `.render_script` ve gölgelendiricilerle işleme hattının tamamını betikle denetleyebilirsiniz. Ayrıca çoğu oyunda kullanabileceğiniz varsayılan bir işleme hattı da bulunur.

Defold'un varsayılan işleme betiği yaygın 2B ve 3B içerikleri işler. Özel bir `.render_script` ile çizim geçişlerini, işleme hedeflerini ve diğer işleme işlemlerini yönetebilirsiniz. Betik, materyal etiketlerinden yararlanan işleme yüklemleriyle bileşen gruplarını seçer. Defold, fiziksel tabanlı işleme (PBR) için yerleşik destek sunar. Ayrıca topluluğun geliştirdiği çok sayıda özel işleme hattı ve gölgelendirici vardır.


Defold, köşe ve parça aşamaları ayrı dosyalarda olan GLSL gölgelendiricileri kullanır. Godot'un ise motora özgü yerleşik öğeler içeren, GLSL benzeri bir gölgelendirme dili vardır. Bu nedenle Godot'tan veya Shadertoy gibi diğer kaynaklardan aldığınız gölgelendiricileri uyarlamanız gerekebilir. Defold'un gereksinimleri için [Gölgelendiriciler kılavuzuna](/manuals/shader/) bakın.

Defold'da **materyaller**, köşe ve parça programlarını (gölgelendiricileri), dokuları, gölgelendirici sabitlerini ve öznitelikleri bir araya getirir. `builtins` klasöründeki varsayılan materyalleri başlangıç noktası olarak kullanabilirsiniz.

Varsayılan davranışı değiştirmek istediğinizde [İşleme](/manuals/render/), [Materyaller](/manuals/material/) ve [Gölgelendiriciler](/manuals/shader/) kılavuzlarına bakın.

### Çizim sırası ve katmanlar {#draw-order-and-layers}

Godot'un tamsayı değerli `z_index` özelliğinin Defold'da doğrudan bir karşılığı yoktur. Z ekseninin derinlikle ilişkisi işleme düzenine bağlıdır. Z boyunca hareket etmek her zaman derinliği değiştirmek anlamına gelmez. Defold temelde bir 3B motordur. Bu yüzden Godot'taki gibi 2B sıralamaya ayrılmış bir tamsayı yerine uzaydaki gerçek Z koordinatını kullanır.

Defold'un **varsayılan** ortografik düzeninde yalnızca Z konumu -1.0 ile 1.0 arasında olan nesneler çizilir. Katmanlara 0.1 veya 0.2 gibi ondalık değerler verebilirsiniz. İşleme betiğine bir ileti göndererek bu aralığı değiştirebilirsiniz. Basit varsayılan düzende Defold bu aralıktaki oyun nesnelerinin veya sprite bileşenlerinin gerçek Z konumunu kullanarak çizim sırasını belirler. Z değeri yüksek nesneler düşük olanların üzerine çizilir. Bu yönüyle Godot'taki `z_index` kullanımına benzer. Perspektif kameraya geçer veya `.render_script` dosyasını değiştirirseniz bu davranış değişebilir.

Defold'da GUI düğümleri dünyanın Z koordinatını dikkate almaz. Varsayılan olarak GUI bileşenleri, dünyadaki sprite bileşenlerinden sonra ayrı bir geçişte çizilir. Bu nedenle bir GUI düğümünün Z konumunu değiştirmek çizim sırasını etkilemez. GUI çizim sırasını, Outline bölmesindeki düğümlerin yukarıdan aşağıya sırası ve GUI katmanları (`Layers`) belirler. Katmanlar toplu çizim yapabilmek için düğüm sırasına göre önceliklidir. Bu bakımdan Godot'un `CanvasLayer` katmanlarına benzerler.

### Kameralar ve koordinatlar {#cameras-and-coordinates}

Bir oyun nesnesine `Camera` bileşeni ekleyin. Kamerayı hareket ettirmek için bu nesneyi hareket ettirin. Tipik bir 2B görünüm için ortografik, 3B için perspektif izdüşüm kullanabilirsiniz.

Varsayılan işleme betiği otomatik olarak en son etkinleştirilen kamerayı kullanır. Hiç kamera yoksa varsayılan görünüm 2B ortografiktir. Tek kamera varsa o kullanılır. Bu düzenle başlayabilir ve oyununuz ihtiyaç duyduğunda işleme davranışını özelleştirebilirsiniz.

Kamera, dünya koordinatlarının ekrana nasıl yansıtıldığını belirler. Oyun dünyasında işaretçi girdisini işlerken işaretçi koordinatlarını doğrudan dünya konumu olarak kabul etmeyin. [Kamera API'sinin](/ref/camera/) dönüştürme işlevlerini kullanın. İşaretçinin hangi GUI düğümünün üzerinde olduğunu denetlerken ise varsayılan olarak GUI koordinatları kullanılır.

İzdüşüm, yakınlaştırma ve koordinat dönüşümleri için [Kamera kılavuzuna](/manuals/camera/) bakın.

---

## Oyunu dışa aktarma {#exporting-a-game}

Defold'da dışa aktarmaya **dağıtım paketi oluşturma (bundling)** denir. **Project ▸ Bundle** seçeneğini seçin, hedef platformu belirleyin ve paket seçeneklerini ayarlayın. Düzenleyici tüm derleme araçlarını sunduğu için Godot'un dışa aktarma şablonları gibi ayrı bir kurulum gerekmez.

`game.project` dosyası ana koleksiyon, girdi eşlemeleri ve ekran boyutu dahil proje ve platform ayarlarını içerir. Hedef platformun imzalama ve mağaza gereksinimlerini de karşılamanız gerekebilir. Yerel kod eklentileri içeren projelerde, bulut derleme hizmeti üzerinden özel bir motor derlemek için ağ bağlantısı gerekir. İsterseniz derleme hizmetini yerel olarak da kurabilirsiniz.

Dağıtım paketinin boyutu varlıklara, eklentilere ve derleme ayarlarına bağlıdır. Oyunun hangi kaynakları içerdiğini görmek için bir `Build Report` oluşturun.

[Dağıtım paketi oluşturma](/manuals/bundling/), [Proje ayarları](/manuals/project-settings/) ve [HTML5](/manuals/html5/) kılavuzlarına bakın. Özellikle oyununuz gölgelendiriciler, yerel kod eklentileri veya platform hizmetleri kullanıyorsa paketi hedef platformunuzda erkenden test edin.

## Kütüphaneler ve eklentiler {#libraries-and-extensions}

Defold projelerine paylaşılan betikler ve kaynaklar içeren **kütüphane bağımlılıkları (Library Dependencies)** ekleyebilirsiniz. Kütüphanelerin arşiv URL'lerini `game.project` dosyasına ekleyin, ardından kütüphaneleri indirin. Kütüphane bulmak için önerilen kaynaklardan biri Defold [Asset Portal](https://defold.com/assets/) sayfasıdır. **Asset Store** düzenleyici eklentisiyle de Godot'taki gibi doğrudan Defold düzenleyicisinden varlık arayıp indirebilirsiniz.

Düzenleyiciyi özelleştirmek için **düzenleyici betikleri ve kullanıcı arayüzü (Editor Scripts and UI)** ile komutlar ekleyebilir, işleri otomatikleştirebilir ve özel düzenleyici arayüzleri oluşturabilirsiniz. Örneğin bölüm düzenleme, kaynak oluşturma veya otomatik karo yerleştirme işlemlerini hızlandırabilirsiniz. Bu araçlar Godot'un `EditorPlugin` ve `@tool` özellikleriyle bazı amaçları paylaşır ancak Defold'un kendi `editor` API'sini ve yaşam döngüsünü kullanır.

Motoru Lua'nın sunduklarının ötesine taşımak için **yerel kod eklentileri (Native Extensions)** ile yerel kodu betiklerden çağrılabilir hale getirebilir, yeni bileşenler ekleyebilir veya platform hizmetleriyle tümleştirme sağlayabilirsiniz. Bu eklentiler farklı bir API ve derleme süreci kullanmakla birlikte GDExtension'a benzer bir işlev görür.

[Kütüphaneler](/manuals/libraries/), [Düzenleyici betikleri](/manuals/editor-scripts/) ve [Yerel kod eklentileri](/manuals/extensions/) kılavuzlarına bakın.

## Çalışma sırasında yeniden yükleme {#hot-reload}

Defold'da oyun çalışırken kaynakları yeniden yükleyebilirsiniz (hot reload). Oyunu derleyip çalıştırın, desteklenen bir kaynağı düzenleyip kaydedin ve güncellemek için **File ▸ Hot Reload** seçeneğini seçin. Bu özellik, hedef olarak seçtiğiniz bir cihazda çalışan hata ayıklama derlemesiyle de kullanılabilir.

Bir betiği yeniden yüklemek `init()` işlevini tekrar çağırmaz. Örneğin mevcut verileri korunur. Bu nedenle betikte değiştirdiğiniz bir başlangıç değeri `self` üzerinde kendiliğinden görünmez. Mevcut durumu uyarlamak için `on_reload(self)` kullanın. Baştan başlamak istiyorsanız oyunu yeniden derleyin. Yeni bir tablo döndüren bir Lua modülünü yeniden yüklemek, diğer betiklerin eski tabloya tuttuğu başvuruları değiştirmez. Ayrıntılar için [Modüller kılavuzuna](/manuals/modules/) bakın.

[Çalışma sırasında yeniden yükleme kılavuzunu](/manuals/hot-reload/) okuyun.

## Kesme noktaları ve hata ayıklama {#breakpoints-and-debugging}

Düzenleyicinin yerleşik hata ayıklayıcısında kesme noktaları koyabilir, kodu adım adım çalıştırabilir ve değerleri inceleyebilirsiniz. Çalışma sırasındaki çıktılar için Console, derleme sorunları için Build Errors bölmesini kullanın. Profil çıkarıcı kare süresini, bellek kullanımını ve görüntü işleme işlemlerini incelemenize yardımcı olur. Derleme raporları ise paket boyutuna hangi kaynakların ne kadar katkıda bulunduğunu gösterir.

[Oyun mantığında hata ayıklama](/manuals/debugging-game-logic/) ve [Profil çıkarma](/manuals/profiling/) kılavuzlarına bakın.

## Otomatik iş akışları {#automated-workflows}

Defold, iş akışlarını otomatikleştirmek ve yapay zekâ destekli geliştirme için çeşitli arayüzler sunar. Düzenleyici betikleriyle yinelenen görevleri otomatikleştirebilirsiniz. Düzenleyicinin OpenAPI ile belgelenen HTTP API'si, harici araçların ve yapay zekâ ajanlarının projeleri incelemesine, komutları çalıştırmasına ve derleme başlatmasına olanak verir. Motorun HTTP hizmeti ve Automation Bridge eklentisi ile çalışan oyunu inceleyebilir, girdileri simüle edebilir ve ekran görüntüleri alabilirsiniz. Codex, Claude Code ve Cursor gibi kodlama ajanları bu araçları birlikte kullanarak bir projeyi değiştirme, oyunu derleme, davranışını test etme ve sorunları düzeltme döngüsünü yineleyebilir.

Ayrıntılar için [Otomasyon](/manuals/automation/), [Düzenleyici HTTP API'si](/manuals/editor-http-api/), [Motor hizmeti](/manuals/engine-service/) ve [Otomatik test](/manuals/automated-testing/) kılavuzlarına bakın.

---

## Sık yapılan hatalar {#common-pitfalls}

### Koleksiyonu kök düğüm olarak görmek {#treating-a-collection-as-a-root-node}

Defold koleksiyonu oyun nesnelerini ve aralarındaki ilişkileri tanımlar ancak çalışma sırasında bir kök nesneye dönüşmez. Bir bölümdeki nesneler arasında eşgüdüm sağlamak için kendine ait betiği olan bir oyun nesnesi ekleyin. [Koleksiyonlar ve dünyalar](#collections-and-worlds) bölümüne bakın.

### Bir hiyerarşiyi silmek {#deleting-a-hierarchy}

Godot'ta `queue_free()` düğümün altındaki tüm düğümleri de siler. Defold'da `go.delete(id)` ile silerken özyinelemeli silme istemezseniz alt oyun nesneleri yerinde kalır. Örnek ve koleksiyon fabrikasıyla oluşturulan nesnelerin nasıl temizleneceği için [Fabrikalar](#factories) bölümüne bakın.

### Sahne kalıtımı beklemek {#expecting-scene-inheritance}

Defold, Godot'taki sahne kalıtımı iş akışını sunmaz. Bu yüzden türetilmiş bir sahnenin yapısını aynı şekilde serbestçe değiştiremezsiniz. Prototipleri ve koleksiyonları yeniden kullanabilir, örnekleri özellikler veya betikler aracılığıyla özelleştirebilirsiniz. [Koleksiyonlar ve dünyalar](#collections-and-worlds) bölümüne bakın.

### Nesne başvurusu üzerinden başka bir betiği çağırmak {#calling-another-script-through-an-object-reference}

Defold'da bir oyun nesnesinin tanımlayıcısı başka bir betik örneğinin işlevlerine genel erişim sağlamaz. Bileşenler arasında iletişim için iletileri kullanın veya ortak işlevleri bir Lua modülüne yerleştirin. [İletiler ve adresleme](#messages-and-addressing) ve [Autoload ve paylaşılan durum](#autoloads-and-shared-state) bölümlerine bakın.

### Örneğin durumunu dosya kapsamlı bir yerel değişkende tutmak {#keeping-instance-state-in-a-top-level-local}

Bir betik dosyasının en üst düzeyinde tanımlanan yerel değişken, dosyayı kullanan tüm örnekler arasında paylaşılır. Değişkeni bir örnek için değiştirmek bu yüzden diğerlerini de etkileyebilir. Örneğe özgü durumu [Örneğe özgü veriler ve yerel veriler](#instance-data-vs-local-data) bölümünde açıklandığı gibi `self` üzerinde saklayın.

### Girdinin otomatik olarak etkinleştiğini varsaymak {#assuming-input-is-enabled-automatically}

Defold'da bileşenlerin girdi alabilmesi için oyun nesnesinin önce girdi odağını alması gerekir. Koleksiyon vekiliyle yüklenen bir dünyada vekili taşıyan nesnenin de odağa ihtiyacı vardır. Eşlemeler, odak ve girdi yığınının işleyişi için [Girdi](#input) bölümüne bakın.

### Kinematik bir nesnenin kendiliğinden kaymasını beklemek {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold kinematik çarpışma nesnelerinin temaslarını algılar ancak Godot'taki `move_and_slide()` davranışını kendisi sağlamaz. Hareketi ve çarpışmaya verilecek tepkiyi betiğinizin yönetmesi gerekir. [Fizik ve çarpışmalar](#physics-and-collisions) bölümüne bakın.

### Yalnızca tek bir çarpışma maskesi ayarlamak {#configuring-only-one-collision-mask}

Yalnızca bir nesne diğeriyle etkileşime girecek şekilde yapılandırılmışsa çarpışma kaydedilmez. Her nesnenin maskesi diğerinin grubunu içermelidir. [Fizik ve çarpışmalar](#physics-and-collisions) bölümüne bakın.

### 2B koordinatları olduğu gibi kopyalamak {#copying-2d-coordinates-unchanged}

Godot'ta ve tipik bir 2B Defold projesinde Y eksenleri zıt yönlere bakar. Bu yüzden kopyalanan hareket kodu nesneleri yanlış yöne hareket ettirebilir. Kamera kullanıldığında ekran ve dünya konumları da birbirinden farklıdır. [Koordinatlar](#coordinates) ve [Kameralar ve koordinatlar](#cameras-and-coordinates) bölümlerine bakın.

### GUI düğümlerini dünya Z koordinatına göre sıralamak {#using-world-z-to-sort-gui-nodes}

Defold'da bir GUI düğümünün Z konumu çizim sırasını belirlemez. [Çizim sırası ve katmanlar](#draw-order-and-layers) bölümünde açıklandığı gibi GUI düğümlerinin sırasını ve katmanlarını kullanın.

### Çalışma sırasında yeniden yüklemenin nesneyi baştan başlatmasını beklemek {#expecting-hot-reload-to-restart-the-object}

Çalışan oyunda bir betiği yeniden yüklemek `init()` işlevini yeniden çalıştırmaz. Bu yüzden örnek önceki değerlerini koruyabilir. Durumu ve modüllerin yeniden yüklenmesini yönetmek için [Çalışma sırasında yeniden yükleme](#hot-reload) bölümüne bakın.

### Bir bölümü bellekten kaldırmanın paylaşılan durumu sıfırlamasını beklemek {#expecting-a-level-unload-to-clear-shared-state}

Godot'taki Autoload durumu da önbelleğe alınmış bir Lua modülünün durumu da bölüm değişimlerinde korunabilir. Bu nedenle gerektiğinde paylaşılan verileri kodunuzda sıfırlayın. Bir Lua modülü, Autoload düğümünden farklı olarak geri çağırımları kendiliğinden almaz. [Autoload ve paylaşılan durum](#autoloads-and-shared-state) bölümüne bakın.

## Buradan sonra nereye geçmeli? {#where-to-go-from-here}

Başlangıçta size yol gösterecek ve Defold'u daha yakından tanımanıza yardımcı olacak kılavuzları, örnekleri, öğreticileri, videoları ve kursları [Defold Learn Hub](https://defold.com/learn/) üzerinde bulabilirsiniz. Şu kaynaklarla başlamanızı öneririz:

- [Yapı taşları](/manuals/building-blocks/)
- [Adresleme](/manuals/addressing/)
- [İleti aktarımı](/manuals/message-passing/)
- [Defold örnekleri](/examples/)
- [Öğreticiler](/tutorials/)
- [API başvuru belgeleri](/ref/go/)

Takılırsanız [Defold Forum](https://forum.defold.com/) veya [Discord](https://defold.com/discord/) üzerinden soru sorabilirsiniz. Küçük bir örnek proje paylaşmanız ve Godot'taki hangi davranışı elde etmek istediğinizi açıklamanız, başkalarının size yardımcı olmasını kolaylaştırır.
