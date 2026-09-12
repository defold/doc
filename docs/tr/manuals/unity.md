---
title: Unity kullanıcıları için Defold
brief: Bu kılavuz, Unity deneyiminiz varsa Defold'a hızla geçmenize yardımcı olur. Unity'de kullanılan bazı temel kavramları ele alır ve bunlara karşılık gelen Defold araçlarını ve yöntemlerini açıklar.
---

# Unity kullanıcıları için Defold

Unity deneyiminiz varsa bu kılavuz, Defold'da kısa sürede verimli çalışmaya başlamanıza yardımcı olur. Temel noktalara odaklanır ve daha ayrıntılı bilgi gerektiğinde sizi resmî Defold kılavuzlarına yönlendirir.

## Giriş

Defold, Windows, Linux ve macOS için bir düzenleyici sunan, tamamen ücretsiz ve gerçekten platformlar arası bir 3B oyun motorudur. Kaynak kodunun tamamı [GitHub](https://github.com/defold/defold/) üzerinde bulunur.

Defold, düşük donanımlı cihazlarda bile performansa odaklanır. Oynanış etkileşimlerinin çoğunun kod ve ileti aktarımı yoluyla yönetildiği küçük bir bileşen (component) modeli kullanır.

Defold, Unity'den çok daha küçüktür. Boş bir projeyle motor boyutu tüm platformlarda 1-3 MB arasındadır. Motorun ek bölümlerini çıkarabilir ve oyun içeriğinin bir kısmını daha sonra ayrı olarak indirmek üzere [Live Update](/manuals/live-update) kapsamına taşıyabilirsiniz. Boyut karşılaştırması ve Defold'u seçmek için diğer nedenler [Neden Defold web sayfasında](https://defold.com/why/) açıklanmıştır.

Defold'u ihtiyaçlarınıza göre özelleştirmek için aşağıdakileri kendiniz yazabilir veya mevcut olanları kullanabilirsiniz:

1. Aralarından seçim yapabileceğiniz birkaç arka uca (OpenGL, Vulkan vb.) sahip, görüntü oluşturan ve tamamen betiklerle yönetilebilen bir işleme (rendering) hattı (işleme betiği + materyaller/gölgelendiriciler).
2. Yerel kod eklentileri (Native Extensions) olarak kod ve bileşenler (C++/C#).
3. Düzenleyiciyi özelleştirmek için düzenleyici betikleri ve kullanıcı arayüzü (UI) denetimleri.
3. Kaynak kodunun tamamı ve bir derleme hattı sunulduğu için motorun ve düzenleyicinin değiştirilmiş bir derlemesi.

Ayrıca Game From Scratch'in [Unity geliştiricileri için Defold](https://www.youtube.com/watch?v=-3CzCbd4QZ0) videosuna göz atmanızı öneririz.

---

## Kurulum

1. İşletim sisteminiz için Defold'u indirin.
2. Arşivi çıkarın ve başlatın.

Hepsi bu kadar. Bir merkez uygulaması, ek SDK, araç zincirleri veya platform paketleri kurmanız gerekmez. Bu nedenle Defold'un kurulum gerektirmediğini söylüyoruz.

Daha fazla ayrıntıya ihtiyacınız varsa bu kısa [Kurulum kılavuzunu](/manuals/install/) okuyun.

### Sürümler

Defold sık güncellenir ve bir "LTS" sürüm kolu yoktur. Her zaman en yeni sürümü kullanmanızı öneririz. Yeni sürümler düzenli olarak, genellikle aylık ve yaklaşık iki haftalık herkese açık beta sürecinin ardından yayımlanır. Defold'u doğrudan düzenleyiciden güncelleyebilirsiniz.

---

## Karşılama ekranı

Defold sizi Unity Hub'a benzer bir karşılama ekranıyla karşılar; buradan son projeleri açabilirsiniz:

![Karşılama ekranlarının karşılaştırması](images/unity/unity_defold_start.png)

Veya aşağıdakilerden yeni bir proje başlatabilirsiniz:
- `Templates` - belirli bir platform veya tür için daha hızlı başlangıç yapmanızı sağlayan temel boş projeler,
- `Tutorials` - ilk adımlarınızı atmanıza yardımcı olan yönlendirmeli öğrenme turları,
- `Samples` - resmî veya topluluğun katkıda bulunduğu kullanım senaryoları ve örnekler,

![Karşılama ekranındaki şablonların karşılaştırması](images/unity/unity_defold_templates.png)

İlk projenizi oluşturduğunuzda ve/veya açtığınızda proje Defold düzenleyicisinde açılır.

## Merhaba dünya

Bu bölüm, Defold'da hızla bir şeyler ortaya çıkarmanın kısa bir yoludur. Adımları izleyin, ardından kılavuzun geri kalanını okumaya dönün.

1. `Templates` bölümünden boş bir proje seçin, `Title` alanında adlandırın, konum seçin ve `Create New Project` düğmesine tıklayarak oluşturun. Proje Defold düzenleyicisinde açılır.
![Merhaba dünya, 1. adım](images/unity/helloworld_1.png)
2. Sol taraftaki `Assets` bölmesinde `main` klasörünü açın ve `main.collection` dosyasını açmak için dosyaya çift tıklayın.
3. Sağ taraftaki `Outline` bölmesinde `Collection` öğesine sağ tıklayın ve `Add Game Object` seçeneğini seçin.
![Merhaba dünya, 2. adım](images/unity/helloworld_2.png)
4. Oluşturulan `go` oyun nesnesine sağ tıklayın ve `Add Component`, ardından `Label` seçeneğini seçin.
![Merhaba dünya, 3. adım](images/unity/helloworld_3.png)
5. Aşağıda, sol taraftaki `Properties` bölmesinde `Text` özelliğine bir şey yazın.
6. Ortadaki ana sahne görünümünde etiketi sürükleyip taşıyarak yaklaşık `(480,320,0)` konumuna bırakın veya `Properties` içindeki `Position` değerini değiştirin.
![Merhaba dünya, 4. adım](images/unity/helloworld_4.png)
7. Etiketin konumunu değiştirdikten sonra `File` -> `Save All` seçeneğine tıklayarak veya <kbd>Ctrl</kbd>+<kbd>S</kbd> (Mac'te <kbd>Cmd</kbd>+<kbd>S</kbd>) kısayolunu kullanarak projeyi kaydedin.
8. `Project` -> `Build` seçeneğine tıklayarak veya <kbd>Ctrl</kbd>+<kbd>B</kbd> (Mac'te <kbd>Cmd</kbd>+<kbd>B</kbd>) kısayolunu kullanarak projenizi derleyin.
![Merhaba dünya, 5. adım](images/unity/helloworld_5.png)

Defold'da ilk projenizi derlediniz; metninizi pencerede görmeniz gerekir. Oyun nesnesi (game object) ve bileşen kavramları size tanıdık gelmelidir. Koleksiyonlar, Outline görünümü, özellikler ve etiketi neden biraz sağ üste taşımamız gerektiği aşağıda açıklanmıştır.

---

## Defold düzenleyicisine genel bakış

Burada Defold düzenleyicisini, bir Unity kullanıcısının ilk başta bilmek isteyebileceği noktalar üzerinden tanıtacağız; ancak sonrasında [Düzenleyiciye genel bakış kılavuzunun](/manuals/editor) tamamına göz atmanızı öneririz.

### Düzenleyicilerin karşılaştırması

Unity ile Defold arasında ilk fark edeceğiniz şey varsayılan düzenleyici yerleşimidir. Burada Unity düzenleyicisini, Defold'un varsayılan yerleşimine uyacak şekilde biraz değiştirilmiş bir yerleşimle gösteriyoruz. Unity sekmelerini daha rahat tanıyabileceğiniz için ana bölmeleri görsel olarak daha kolay karşılaştırmanız amacıyla düzenleyiciler yan yana yerleştirilmiştir.

![Düzenleyicilerin karşılaştırması](images/unity/defold_unity_editor.png)

Defold düzenleyicisi varsayılan olarak 2B ortografik önizlemeyle açılır. Bir 3B proje üzerinde çalışacaksanız veya yalnızca Unity'ye daha yakın bir deneyim istiyorsanız --- araç çubuğundaki `2D` seçeneğinin işaretini kaldırarak 2B'den 3B'ye geçmenizi ve `Perspective` seçeneğini işaretleyerek kamera izdüşümünü perspektif olarak değiştirmenizi öneririz:

![Defold araç çubuğu](images/unity/defold_2d.png)

Araç çubuğundaki `Grid Settings` ayarlarını da Unity'deki gibi `Y` düzlemini kullanacak şekilde değiştirebilirsiniz:

![Defold 3B ayarları](images/unity/defold_3d.png)

### Defold bölmelerine genel bakış

Defold düzenleyicisi 6 ana bölmeye ayrılır.

![Düzenleyici 2](images/editor/editor_overview.png)

Aşağıda Defold'daki adlandırmaların ve işlevsel farkların karşılaştırması yer alır:

| Defold | Unity | Farklar |
|---|---|---|
| 1. Assets | Project (Assets Browser) | Defold'da Assets bölmesi sola sabitlenmiştir. Defold herhangi bir `meta` dosyası oluşturmaz. |
| 2. Main Editor | Scene View | Defold düzenleyicisi bağlama duyarlıdır (farklı dosya türleri için farklı düzenleyiciler kullanılır); Unity ise ayrı, belirli bir işe özel pencereler kullanır (ör. Animator, Shader Graph). Defold'da yerleşik bir kod düzenleyicisi de bulunur. |
| 3. Outline | Hierarchy | Defold, genel bir hiyerarşi yerine yalnızca o anda açık olan dosyayı veya seçili öğeyi (oyun nesnesi veya bileşen) yansıtır. |
| 4. Properties | Inspector | Defold, oyun nesnesindeki tüm bileşenlerin özelliklerini değil, yalnızca Outline içindeki **geçerli seçimin** özelliklerini gösterir. |
| 5. Tools | Console | Defold, Console, Curve Editor, Build Errors, Search Results, Breakpoints ve Debugger gibi sekmelerde araçlar sunar. |
| 6. Changed Files | Unity Version Control (Plastic) | Defold'da Git projenize tümleştirildiğinde değişen dosyalar burada gösterilir. Git'i harici olarak kullanmaya devam edebilirsiniz. |

Düzenleyiciyle ilgili diğer yararlı adlandırmalar:

| Defold | Unity | Farklar |
|---|---|---|
| Game Build | Game Preview | Motorla derlenmiş ve çalışmakta olan oyunu gösterir. Defold, Unity 6+ Multiplayer Play Mode özelliğine benzer şekilde, düzenleyiciden oyunun birden çok örneğini (instance) çalıştırabilir. Defold'da oyun her zaman ayrı bir pencerede çalışır ve düzenleyiciye sabitlenmez. Defold ayrıca Unity Remote'a benzer şekilde oyunu harici bir cihazda (ör. cep telefonu) çalıştırabilir. |
| Tabs | Tabs | Defold, Main Editor görünümündeki iki bölmede yan yana düzenlemeye izin verir. Sekmeler ve bölmeler tek bir düzenleyici penceresinin içine sabitlenmiştir; bölmelerin görünürlüğü değiştirilebilir (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>) ve boyutları ayarlanabilir. |
| Toolbar | Toolbar / Scene View Options | Dönüşüm araçları ancak daha yeni Unity sürümlerinde, Defold'dakine benzer şekilde Scene görünümüne taşınmıştır. |
| Console | Console | Defold Console ayrılarak bağımsız bir pencereye taşınamaz. Defold'daki derleme hataları ayrı bir `Build Errors` sekmesinde görünür. |
| Build Errors | Console içindeki kod derleme hataları | Lua betikleri yorumlandığı için kod derleme hatası oluşmaz. Ancak projeniz derlenir ve derleme sırasında bazı hatalar ortaya çıkabilir. Defold ayrıca betiklerin statik analizi için bir Lua Language Server kullanır. |
| Search Results | Search / Project Search | Defold'da türe ve etikete göre filtreleme bulunmaz. |
| Curve Editor | Unity Curve Editor | Defold Curve Editor yalnızca parçacık efekti özelliklerinin eğrilerini düzenlemeye izin verir. |
| [Hata ayıklayıcı](/manuals/debugging/) | Visual Studio Debugger | Hata ayıklayıcı, Defold'a en baştan tamamen tümleştirilmiştir. Kesme noktalarını izlemek, etkinleştirmek ve devre dışı bırakmak için ek bir sekme bulunur. |

---

## Temel kavramlar

Yeterince genel bakarsanız çoğu oyun motorunun temel kavramları birbirine çok benzer. Geliştiricilerin yapı taşlarını bir araya getirir gibi daha kolay oyun yapmasına yardımcı olmayı amaçlarlar ve karmaşık, platforma özgü işleri kendileri yürütürler.

### Yapı taşları

Defold yalnızca birkaç temel yapı taşıyla çalışır:

![Yapı taşları](images/unity/blocks.png)

Daha fazla ayrıntı için [Defold yapı taşları](/manuals/building-blocks/) hakkındaki kılavuzun tamamına göz atın.

### Oyun nesneleri 
Defold, Unity'ye benzer şekilde **"oyun nesneleri"** kullanır. Her iki motorda da oyun nesneleri, bir tanımlayıcıya sahip veri kapsayıcılarıdır ve hepsinin konum, dönme ve ölçekten oluşan dönüşümleri vardır; ancak Defold'da dönüşüm ayrı bir bileşen olmak yerine yerleşiktir.

Oyun nesneleri arasında üst-alt nesne ilişkileri oluşturabilirsiniz. Defold'da bu yalnızca düzenleyicide bir "koleksiyon" (collection, aşağıda açıklanmıştır) içinde veya betikte dinamik olarak yapılabilir. Oyun nesneleri, Unity'deki gibi başka oyun nesnelerini iç içe nesneler olarak barındıramaz.

### Bileşenler
Her iki motorda da oyun nesneleri **"bileşenlerle"** genişletilebilir. Defold, temel bileşenlerden oluşan küçük bir küme sunar. 2B ve 3B arasındaki ayrım Unity'dekinden daha azdır (ör. çarpıştırıcılar); bu nedenle toplam bileşen sayısı daha azdır ve Unity'deki bazı bileşenleri arayabilirsiniz.

#### Davranış bileşenleri

Unity'de "bileşen" genellikle bir `GameObject` nesnesine eklenen `MonoBehaviour` anlamına gelir. `MonoBehaviour` sınıfından türeterek kendi bileşenlerinizi oluşturabilir veya Light, bazı fizik öğeleri ve benzeri yerleşik bileşenleri kullanabilirsiniz.

Defold'da bileşen yalnızca Unity'deki yerleşik bileşenlere karşılık gelen veya benzeri öğeleri ifade eder; ancak Defold bir betiği monobehaviour olarak ele almaz ve dinleyici olayları/geri çağırımları oluşturmak dışında bir oyun nesnesine eklemek için açıkça herhangi bir "işaretleme" gerektirmez.

Özel oynanış davranışı genellikle aynı oyun nesnesine birçok ayrı betik bileşeni olarak eklenmez. Bunun yerine çoğunlukla Lua modüllerinde uygulanıp bunları barındıran tek bir `.script` tarafından kullanılır veya birçok nesneyi yöneten daha büyük bir sistem betiği tarafından ele alınır. Aşağıdaki Kod yazma bölümü bunu daha ayrıntılı açıklar.

[Defold bileşenleri hakkında buradan](/manuals/components/) daha fazla bilgi edinebilirsiniz.

Aşağıdaki tablo, hızlıca karşılaştırabilmeniz için benzer Unity bileşenlerini ve her Defold bileşeninin kılavuzuna bağlantıları sunar:

| Defold | Unity | Farklar |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | Defold'da sprite bileşeninin renk çarpanını (renk özelliği) yalnızca kod yoluyla değiştirebilirsiniz. |
| [Karo haritası](/manuals/tilemap/) | Tilemap / Grid | Defold'da kare ızgaraları destekleyen yerleşik bir karo haritası düzenleyicisi bulunur (ancak örneğin [altıgenler](https://github.com/selimanac/defold-hexagon/) için bir eklenti vardır) ve yerleşik otomatik karo yerleştirme kuralları yoktur. [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) veya [Sprite Fusion](https://defold.com/assets/spritefusion/) gibi araçlar Defold'a dışa aktarma seçenekleri sunar. |
| [Etiket](/manuals/label/) | Text / TextMeshPro | Defold 1.13.2'den itibaren etiket bileşenleri ve GUI metin düğümleri; renkler, renk geçişleri, dış çizgiler ve animasyonlu efektler için yerleşik [zengin metin işaretlemesini](/manuals/font-richtext/) destekler. Ayrı bir [RichText eklentisi](https://defold.com/assets/richtext/) de mevcuttur. |
| [Ses](/manuals/sound/) | AudioSource | Defold'da yalnızca genel bir ses kaynağı bulunur (uzamsal değildir). Defold için resmî bir [FMOD eklentisi](https://github.com/defold/extension-fmod) vardır. |
| [Fabrika](/manuals/factory/) | Prefab Instantiate() | Defold'da fabrika (factory), belirli bir prototipe (prefab; yeniden kullanılabilir nesne tanımı) sahip bir bileşendir. |
| [Koleksiyon fabrikası](/manuals/collection-factory/) | - (Doğrudan bir bileşen karşılığı yoktur) | Defold'daki bir koleksiyon fabrikası (collection factory) bileşeni, üst-alt nesne ilişkilerine sahip birden çok oyun nesnesini aynı anda oluşturabilir. |
| [Çarpışma nesnesi](/manuals/physics-objects) | Rigidbody + Collider | Defold'da fizik nesneleri ve çarpışma şekilleri tek bir bileşende birleştirilmiştir. |
| [Çarpışma şekilleri](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | Defold'da şekiller (kutu, küre, kapsül) çarpışma nesnesi bileşeninin içinde yapılandırılır. Her ikisi de karo haritalarından ve dışbükey kabuk verilerinden alınan çarpışma şekillerini destekler. |
| [Kamera](/manuals/camera/) | Camera | Unity'deki kamera daha fazla yerleşik işleme ve son işleme ayarına sahipken Defold bu ayarların işleme betiği üzerinden kullanıcı tarafından özelleştirilerek yönetilmesini sağlar. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defold GUI, eksiksiz kullanıcı arayüzleri ve şablonlar oluşturmak için güçlü bir bileşendir. Unity'de buna karşılık gelen tek bir kullanıcı arayüzü bileşeni yerine birden çok kullanıcı arayüzü çatısı bulunur. Defold'da [Eklenti](https://github.com/britzl/extension-imgui) için de bir eklenti vardır. |
| [GUI betiği](/manuals/gui-script/) | Unity UI / uGUI betikleri | Defold GUI, özel `gui` API'sini kullanan GUI betikleri üzerinden yönetilebilir. |
| [Model](/manuals/model/) | MeshRenderer + Material | Defold'da bir model bileşeni; bir 3B model dosyasını, dokuları ve gölgelendiricilere sahip bir materyali bir araya getirir. |
| [Örgü](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | Defold'da örgü (mesh), bir köşe kümesini kod yoluyla yönetmek için kullanılan bir bileşendir. Defold model bileşenine benzer, ancak daha da düşük düzeylidir. |
| [ParticleFX](/manuals/particlefx/) | Particle System | Defold'un parçacık düzenleyicisi birçok özelliğe sahip 2B/3B parçacık efektlerini destekler ve Curve Editor içindeki eğrileri kullanarak bunlara zaman içinde animasyon uygulamanızı sağlar. Trails veya Collisions özellikleri yoktur. |
| [Betik](/manuals/script/) | Script | Programlama farkları hakkında daha fazla ayrıntı aşağıda açıklanmıştır. |

#### Eklentiler ve özel bileşenler

Defold ayrıca eklentiler üzerinden sunulan resmî [Spine](/extension-spine/) ve [Rive](/extension-rive/) bileşenlerine sahiptir.

Yerel kod eklentilerini kullanarak kendi [özel bileşenlerinizi](https://github.com/defold/extension-simpledata) de oluşturabilirsiniz; örneğin topluluk tarafından oluşturulan bu [Nesne ara değerleme bileşeni](https://github.com/indiesoftby/defold-object-interpolation) gibi.

Bazı Unity bileşenlerinin Defold'da hazır bir karşılığı yoktur; örneğin Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth veya Animator. Ancak bu işlevlerin tamamı betiklerde uygulanabilir ve hâlihazırda mevcut çözümler vardır: örneğin farklı aydınlatma hatları, isteğe göre örgüler (arazi dahil) üretmek için örgü bileşeni veya özelleştirilebilir iz efektleri için [Hyper Trails](https://defold.com/assets/hypertrails/). Defold gelecekte ışıklar gibi yeni yerleşik bileşenler de ekleyebilir.

### Kaynaklar

Unity'ye benzer şekilde bazı bileşenler **"kaynaklara" (resources)** ihtiyaç duyar; örneğin sprite ve model bileşenlerinin dokulara ihtiyacı vardır. Bunlardan birkaçı aşağıdaki tabloda karşılaştırılmıştır:

| Defold | Unity | Farklar |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold'da bir [Texture Packer eklentisi](https://defold.com/extension-texturepacker/) de bulunur. |
| [Karo kaynağı](/manuals/tilesource/) | Tile Palette + Asset | Defold'da bir karo kaynağı, karo haritalarının yanı sıra sprite bileşenleri veya parçacıklar için de doku olarak kullanılabilir. |
| [Yazı tipi](/manuals/font/) | Font | Unity'deki Text/TextMeshPro'ya benzer şekilde, Defold etiket bileşeni veya GUI içindeki metin düğümleri tarafından kullanılır. |
| [Materyal](/manuals/material/) | Material | Defold'da gölgelendiriciler köşe programı ve parça programı olarak adlandırılır. |

### Koleksiyon ve sahne karşılaştırması

Defold'da oyun nesneleri ve bileşenler, Unity prefabları gibi ayrı dosyalara yerleştirilebilir veya onları bir araya getiren bir **"koleksiyon"** dosyasında tanımlanabilir.

Defold'da bir koleksiyon temelde statik bir sahne açıklaması içeren metin dosyasıdır. Bir çalışma zamanı nesnesi **değildir**. Yalnızca oyunda hangi oyun nesnelerinin örneklerinin oluşturulacağını ve bu nesneler arasındaki üst-alt nesne ilişkilerinin nasıl kurulacağını tanımlar.

#### Oyun dünyaları

Unity sahneleri varsayılan olarak aynı genel oyun durumunu ve fizik simülasyonunu, dolayısıyla aynı *dünyayı* (*oyun dünyasını*) paylaşır. Defold'da iki seçeneğiniz vardır:
1. Prefablarda olduğu gibi, tek bir oyun nesnesi dosyasından `Factory` aracılığıyla veya bir koleksiyon dosyasından `Collection Factory` aracılığıyla, örneği zaten oluşturulmuş belirli bir *dünyada* oyun nesnelerinin örneklerini oluşturmak.
2. Başlangıçta yüklenen bir koleksiyon veya bir koleksiyon vekili (collection proxy) olan `Collection Proxy` bileşeni aracılığıyla, kendi oyun nesnelerine, fizik dünyasına, motor işlemlerine ve adresleme ad alanına sahip ayrı bir oyun *dünyasını* çalışma sırasında oluşturmak.

Fabrika ve vekil bileşenleri aşağıda ayrıca açıklanmıştır.
Koleksiyonlar hakkında daha fazla bilgi için [Yapı taşları kılavuzunu](/manuals/building-blocks/#collections) okuyun.

---

## Proje kaynakları ve varlıkları

Unity ve Defold, oyun içeriğini proje dizininde saklar; ancak varlıkların (asset) nasıl izlendiği ve hazırlandığı konusunda farklılık gösterir.

### Varlıklar

Unity varlıkları `Assets/` içinde tutar ve `.meta` dosyaları oluşturur. Defold'da meta dosyaları yoktur. Defold'daki proje, diskte olduğu hâliyle klasör yapınızdan ibarettir ve `Assets` bölmesi her zaman bu yapıyı yansıtır.

### Kaynak biçimleri

Unity varlıkları içe aktarır ve arka planda başka biçimlere dönüştürür. Defold'da doğrudan kaynaklarla (`.png`, `.gltf`, `.wav`, `.ogg` vb.) çalışır ve bunları `Components` öğelerine atarsınız.

Unity tek bir görüntüyü Sprite olarak kullanabilir. Defold'da görüntüler doğrudan model/örgü bileşenlerinde kullanılabilir; ancak sprite/GUI/karo haritası/parçacık bileşenleri bir atlas (paketlenmiş dokular) veya karo kaynağı (ızgara tabanlı karolar) gerektirir.

Defold kaynaklarının çoğu metin olarak saklanır; bu da sürüm kontrolüne uygundur.

### Kütüphane önbelleği

Unity, içe aktarılan varlıklar için bir `Library/` klasörü oluşturur. Defold'da böyle bir dizin yoktur; varlıklar derleme sırasında işlenir ve çıktılar derleme klasöründe (ve isteğe bağlı yerel/uzak derleme önbelleklerinde) önbelleğe alınır.

---

## Kod yazma

`MonoBehaviour` betiklerinin Defold'daki karşılığı bir betik bileşenidir; ancak bilinmesi gereken bazı farklar vardır.

### Lua

Defold betikleri, dinamik türlere sahip ve birden çok programlama paradigmasını destekleyen [Lua](https://www.lua.org/) dilinde yazılır.

Birkaç Lua betiği türü vardır: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` ve `*.lua` modülleri.

### Teal

Defold, Lua'nın statik türlere sahip bir lehçesi olan [Teal](https://teal-language.org/) gibi Lua kodu üreten kaynak kod dönüştürücülerinin kullanımını destekler; ancak bu işlev daha sınırlıdır ve ek kurulum gerektirir. Ayrıntılar [Teal eklenti deposunda](https://github.com/defold/extension-teal) bulunur.

### C++/C# yerel kod eklentileri

Defold'da yerel kod eklentileri, hedef platforma bağlı olarak başka birkaç dilde yazılabilir: C, C++, C#, Objective-C, Java veya JS. C# diline çok hâkimseniz oyun mantığınızın çoğunu bir C# eklentisinde yapılandırıp yalnızca küçük bir Lua başlangıç betiğinden çağırmak teknik olarak mümkündür; ancak bu, ileri düzey API bilgisi gerektirir ve yeni başlayanlara önerilmez.

Eklentiler hakkında daha fazla bilgi için [Defold yerel kod eklentileri kılavuzunu](/manuals/extensions/) okuyun.


### MonoBehaviour betiklerinden Lua modüllerine

Unity açık bir betik yazma modeline sahiptir. `MonoBehaviour` düzenleyicide davranış eklemenin başlıca yolu olduğu için birçok Unity projesi, önemli her GameObject için denetleyici tarzında bir betikle başlar: `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager` vb.

Defold, varsayılan mimarisi konusunda daha belirli bir yaklaşım benimser. Bir oyun nesnesinin bir `.script` dosyası olabilir; ancak her oyun nesnesi için betik oluşturmanız nadiren gerekir. Çünkü Defold'un güçlü adresleme ve ileti aktarımı sayesinde Defold'daki tek bir betik, kendilerine ait hiçbir betikleri olmasa bile yüzlerce veya binlerce başka nesneyi ve bunların bileşenlerini yönetebilir. Her oyun nesnesine karşılık bir betik oluşturmak nadiren gereklidir ve yarardan çok zarar getiren karmaşıklığa yol açabilir.

Yeniden kullanılabilir oynanış davranışı için Unity geliştiricileri sıkça bileşime (composition) yönelir: aynı GameObject nesnesine eklenen `Health.cs`, `Attack.cs` veya `EnemyFinder.cs` gibi daha küçük `MonoBehaviour` betikleri kullanırlar. Defold'da genellikle eklenmiş tek bir `.script` dosyasını barındırıcı veya koordinatör olarak tutar, yeniden kullanılabilir mantığı da normal Lua modüllerine yerleştirirsiniz.

Unity'de bu bileşim şöyle görünebilir:

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

Defold'da aynı sorumluluklar genellikle eklenmiş tek bir betik ile yeniden kullanılabilir modüller arasında paylaştırılır:

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

Eklenmiş `.script`, barındırıcı veya koordinatör hâline gelir. Lua modülleri, Unity'deki küçük `MonoBehaviour` betiklerinin çoğunlukla tek bir sorumluluk içermesine benzer şekilde yeniden kullanılabilir mantık içerir.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

Önemli fark, Defold'un modüler mimariyi engellemesi değildir; bileşimin nerede yapıldığı ve oynanış kodunun nasıl iletişim kurduğudur:

| Unity | Defold |
|---|---|
| Inspector içinde birkaç `MonoBehaviour` betiği ekleyin | Bir `.script` ekleyin ve Lua modüllerini kodda bir araya getirin |
| Davranışları bağlamak için `GetComponent<T>()` veya serileştirilmiş alanları kullanın | Modül örneklerini `self` üzerinde saklayın ve nesneler arasında adresler/iletiler kullanın |
| Her bileşen kendi yaşam döngüsü yöntemlerine sahip olabilir | Barındırıcı betik `init()`, `update()`, `on_message()`, `final()` vb. çağrıları yönlendirir |
| Birçok mimari tarz mümkündür | İleti odaklı, açıkça kodda yapılan bileşim yaygın uygulamadır |

Özellikle Inspector içinde bileşenler ekleyerek davranış yapılandırmaya alışkınsanız bu yaklaşım başta alışılmadık gelebilir. Unity'de görsel olarak yapılandırabileceğiniz birçok şey Defold'da kod üzerinden oluşturulabilir, bağlanabilir, etkinleştirilebilir, devre dışı bırakılabilir veya güncellenebilir. Defold'un ileti sistemi mantığın birbirinden ayrılmasına yardımcı olur: gönderen bir adrese veri gönderir, alıcı ise bu veriyle ne yapacağına karar verir.

Bu yaklaşım önerilse de zorunlu değildir; oyun nesnesi başına birden çok betik eklemek veya nesne yönelimli programlama tarzına yaklaşmak dahil, betiklerinizi istediğiniz gibi yazabilirsiniz. Hatta bu konuda size yardımcı olacak kütüphaneler de vardır ([defold-oop](https://github.com/xiyoo0812/defold-oop) veya [lua-class](https://github.com/d954mas/lua-class)).

Mermiler, düşmanlar, parçacıklar, karolar veya basit etkileşimli öğeler gibi aynı türden çok sayıda nesne için her nesneye ayrı bir betik vermek yerine bunları bir sistem ya da yönetici betiğinden yönetmek çoğunlukla daha iyidir. Bir nesnenin kendine ait anlamlı durumu ve davranışı varsa nesne başına betik kullanın. Yeniden kullanılabilir mantık istediğinizde modülleri kullanın. Tek bir betik birçok nesneyi verimli şekilde yönetebiliyorsa sistem betiklerini kullanın.

Birden çok birimi yönetmek için Defold betik özelliklerinin, fabrikaların, adreslemenin ve iletilerin nasıl kullanılacağını gösteren bir örneği [burada](https://defold.com/examples/factory/spawn_manager/) bulabilirsiniz.

Kod yazma hakkında yararlı kılavuzlar:
- [Betik kılavuzu](/manuals/script/)
- [Kod yazma](/manuals/writing-code/)
- [Hata ayıklama](/manuals/debugging/)


### Yerleşik kod düzenleyicisi

Defold düzenleyicisi; kod tamamlama, sözdizimi vurgulama, belgelere hızlı erişim, statik kod denetimi ve yerleşik hata ayıklayıcı sunan bir kod düzenleyicisi içerir.

![Defold kod düzenleyicisi](/images/editor/code-editor.png)

### VS Code ve diğer düzenleyiciler

İsterseniz kendi harici düzenleyicinizi kullanmaya devam edebilirsiniz. Tüm Defold bileşenleri ve ilgili dosyalar metin tabanlı olduğundan bunları herhangi bir metin düzenleyicisiyle düzenleyebilirsiniz; ancak Protobuf tabanlı oldukları için doğru biçimlendirmeye ve öğe yapısına uymanız gerekir.

VS Code'a alışkınsanız ve oyununuzun kodunu yazmak için onu kullanmak istiyorsanız Visual Studio Marketplace üzerinden [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) veya [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) kurmanızı öneririz.

Defold düzenleyicisinin tercihlerini, metin dosyalarını varsayılan olarak VS Code'da (veya başka bir harici düzenleyicide) açacak şekilde de yapılandırabilirsiniz. Ayrıntılar için [Düzenleyici tercihleri](/manuals/editor-preferences/) bölümüne bakın.

### Gölgelendiriciler - GLSL

Defold, Unity'ye benzer şekilde `Vertex Programs` ve `Fragment Programs` gölgelendiricileri için GLSL (OpenGL Shading Language) kullanır. Defold, Unity gibi bir Shader Graph sunmasa da (bu bir dezavantaj olabilir) kod yazarak eşdeğer gölgelendiriciler oluşturabilirsiniz.

Gölgelendiriciler hakkında daha fazla bilgi için [Gölgelendiriciler kılavuzunu](/manuals/shader) okuyun.

#### Materyaller

Defold, `.fp` ve `.vp` gölgelendiricilerini, örnekleyicileri (dokuları) ve Vertex Attributes veya Constants gibi diğer öğeleri birbirine bağlayan bir `Material` kavramı kullanır.

Materyaller hakkında daha fazla bilgi için [Materyaller kılavuzunu](/manuals/material) okuyun.

---

## İleti sistemi

Defold'da nesneler birbirlerine doğrudan başvuru tutmaz. `GetComponent`, betikler arasında nesneler arası yöntem çağrıları veya Unity'deki gibi genel sahne erişimi yoktur.

Bunun yerine betikler ileti aktarımı yoluyla iletişim kurar: yöntem çağırmak veya bileşenlere doğrudan erişmek yerine diğer betiklere iletiler gönderirsiniz. Bu nesnelerin iletilerle ne yapacağı kendilerine bağlıdır.

Bu yaklaşım başta yabancı gelebilir; ancak gevşek bağlılığı teşvik eder ve sıkı karşılıklı bağımlılıkları azaltır.


### İleti gönderme

Unity'de iletişim genellikle şöyle görünür:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Yani nesneler birbirlerine doğrudan başvurabilir ve diğer betiklerdeki yöntemleri çağırabilir. Her şey ortak bir sahne uzayında bulunur.

Defold'da bir betikten başka bir betiğe (veya başka bir bileşene) ileti gönderirsiniz:

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

Ve bu iletileri betikte işleyebilirsiniz:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Şimdilik `#` ve `hash` öğelerini dikkate almayın; bunları daha sonra ele alacağız. Geri kalanı anlaşılır olmalıdır. Örneği oluşturulmuş herhangi bir oyun nesnesinin herhangi bir bileşenine (aynı betiğe bile) ileti gönderebilirsiniz.

#### Betik dışındaki bileşenler

Bazen `Sprite` veya `Collision` gibi bileşenlere, örneğin bunları etkinleştirmek veya devre dışı bırakmak için ileti gönderirsiniz. Bazen de `Components` öğeleri, örneğin bir çarpışma olduğunda bunu işleyebilmeniz için betiğinize ileti gönderir. Defold, motor olayları ve oynanış iletişimi için dahili olarak aynı ileti sistemini kullanır. 

Adresleme ve kullanım kuralları farklı olsa da ileti sistemi Unity'nin SendMessage veya olay sistemlerine bir ölçüde benzer.

Daha fazla ayrıntı için [İleti aktarımı kılavuzunu](/manuals/message-passing/) okuyabilirsiniz.

### Adresleme

Defold'da nesneler ve bileşenler, URL olarak bilinen adreslerle tanımlanır.

Örneği oluşturulmuş her nesne ve bileşenin kendine ait benzersiz bir adresi vardır; bunları bulmak için bir sahne grafında gezinmeniz gerekmez. Bu, adreslemeyi açık ve doğrudan hâle getirir.

Defold'da basit bir URL şöyle görünebilir:
```lua
"/player"
```

Bu, *kavramsal olarak* şuna benzer:
```c#
GameObject.Find("player")
```

Şimdi adreslerde neden `"/"` veya `"#"` kullanıldığını açıklama zamanı.

Defold URL adresi ([URL](https://en.wikipedia.org/wiki/URL) yapısına benzer şekilde) üç bölümden oluşur:

```yaml
socket: /path #fragment
```

Veya Defold adlandırmasına daha yakın biçimde açıklarsak:

```yaml
collection: /gameobject #component 
```
Yukarıdaki açıklamalara yalnızca bu 3 bölümü görsel olarak ayırmak için boşluklar eklenmiştir.

Basitçe ifade etmek gerekirse:
1. `collection:`, sonunda `:` bulunacak şekilde koleksiyon bağlamını tanımlar.
2. `/path`, tanımlayıcıdan önce `/` gelecek şekilde oyun nesnesini tanımlar.
3. `#fragment`, tanımlayıcıdan önce `#` gelecek şekilde o nesne üzerindeki belirli bileşeni (betik, sprite veya çarpışma bileşeni gibi) tanımlar.

#### Statik adres

Bu tanımlayıcılar her öğe oluşturulduğunda belirlenir ve üst-alt nesne ilişkilerini değiştirseniz bile hiçbir zaman değişmez. Bunları dosyalardaki `Id` özelliğinde ayarlayabilir veya çalışma sırasında örnek oluştururken yapılan `factory.create` ya da `collectionfactory.create` çağrılarından alabilirsiniz.

#### Göreli adresleme

Her zaman tam bir URL kullanmanız gerekmez.

Aynı koleksiyon (aynı *dünya*) içinde ileti gönderiyorsanız soket bölümünü atlayabilirsiniz:

```yaml
/gameobject #component
```
Aynı oyun nesnesi içindeki bir bileşene gönderiyorsanız oyun nesnesi bölümünü de atlayabilirsiniz:

```yaml
#component
```

İki yararlı kısa gösterim şunlardır:
- Bu *betik* bileşenine göndermek için `#`
- Bu *oyun nesnesindeki* tüm bileşenlere göndermek için `.`

Göreli adresleme ve kısa gösterimler, tam yollar belirtmeden farklı bağlamlarda ve oyun nesnelerinde yeniden kullanılabilen URL adresleri yazmanızı sağlar.

### GUI ve işleme sistemine ileti gönderme

Defold GUI dünyasını oyun nesnesi dünyasından ayırdığı için oyun nesnelerinin `.scripts` dosyalarından `.gui_scripts` dosyalarına da ileti gönderebilirsiniz.

Ayrıca `@` ile başlayan bir tanımlayıcı kullanarak özel sistem ad alanlarına ileti gönderebilirsiniz. Örneğin işleme sistemine `@render`: üzerinden erişebilir ve bunu, varsayılan işleme betiğinde izdüşümü değiştirmek gibi belirli yerleşik işleme özelliklerini yönetmek için kullanabilirsiniz:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Daha fazla ayrıntıyı [Adresleme kılavuzunda](/manuals/addressing/) bulabilirsiniz.

---

## Prefablar ve örnekler

Unity, sahnedeki herhangi bir şeyin örneğini statik veya dinamik olarak oluşturabilir; Defold da aynısını yapabilir. Unity'de bir prefab alıp `Instantiate(prefab)` çağrısını yaparsınız. Defold'da içerik örnekleri oluşturmak için 3 bileşen vardır:

- `Factory` - verilen bir prototipten, yani bir `*.go` dosyasından (prefab), **tek bir oyun nesnesinin** örneğini oluşturur.
- `Collection Factory` - verilen bir prototipten, yani bir `*.collection` dosyasından, üst-alt nesne ilişkilerine sahip **bir oyun nesnesi kümesinin** örneklerini oluşturur.
- `Collection Proxy` - bir `*.collection` dosyasından yeni bir *dünyayı* **yükler** ve örneğini oluşturur.

### Fabrika

`Prototype` özelliği uygun oyun nesnesi dosyasına ayarlanmış bir `Factory` bileşeni tanımladıktan sonra çalışma sırasında nesne oluşturmak, kodda şu çağrıyı yapmak kadar basittir:

```lua
factory.create("#my_factory")
```

Bu çağrı bileşenin adresini kullanır; bu örnekte `"#my_factory"` tanımlayıcısını kullanan göreli bir yoldur.

Yeni oluşturulan örneğin tanımlayıcısını döndürür; dolayısıyla bunu daha sonra kullanmanız gerekiyorsa bir değişkende saklamanız yararlı olur:

```lua
local new_instance_id = factory.create("#my_factory")
```

Defold'da nesneleri elle bir havuzda yönetmeniz gerekmediğini unutmayın; motor havuzlamayı sizin için dahili olarak yapar.

Daha fazla ayrıntı için [Fabrika kılavuzuna](/manuals/factory/) göz atın. 

### Koleksiyon fabrikası

`Factory` ile `Collection Factory` bileşeni arasındaki fark, koleksiyon fabrikasının aynı anda **birden çok** oyun nesnesi oluşturabilmesi ve oluşturma sırasında `*.collection` dosyasında tanımlanan üst-alt nesne ilişkilerini kurabilmesidir.

Unity'de böyle bir ayrım yoktur; Defold'un koleksiyon fabrikasıyla eşleşen özel bir kavram bulunmaz. En yakın benzetme, bir nesne hiyerarşisi içeren iç içe bir prefabdır.

Oluşturulan tüm örneklerin tanımlayıcılarını içeren bir **tablo** döndürür:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Daha fazla ayrıntı için [Koleksiyon fabrikası kılavuzuna](/manuals/collection-factory/) göz atın.

#### Örneklerin özel özellikleri

`factory.create()` veya `collectionfactory.create()` çağrısında konum, dönme, ölçek ve betik özellikleri gibi isteğe bağlı parametreler de belirtebilirsiniz. Böylece örneğin tam olarak nasıl ve nerede ortaya çıkacağını ve nasıl davranacağını yönetebilirsiniz. Örneğin:

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

İsteğe bağlı bağımsız değişkenlerin sırası önce özellikler, ardından ölçektir. Bir 2B nesnenin yalnızca X ve Y eksenlerini ölçeklerken Z değeri açıkça `1.0` olarak ayarlanmış bir `vector3` kullanın; sayısal bir ölçek üç eksene de eşit şekilde uygulanır.

#### Dinamik yükleme

Hem `Factory` hem de `Collection Factory` bileşenlerinde, büyük varlıklarının yalnızca gerektiğinde belleğe alınması ve artık kullanılmadıklarında bellekten kaldırılması için bir Prototype öğesini dinamik kaynak yükleme amacıyla işaretleyebilirsiniz.

Daha fazla ayrıntı için [Kaynak yönetimi kılavuzuna](/manuals/resource/) göz atın. 

### Koleksiyon vekili

`Collection Proxy` belirli bir `*.collection` dosyasına başvurur; ancak nesneleri (fabrikalar gibi) *geçerli dünyaya* eklemek yerine **yeni bir oyun dünyası yükler ve örneğini oluşturur**. Bu, Unity'de bir sahnenin tamamını yüklemeye bir ölçüde benzer; ancak ayrım daha katıdır.

Unity'de mevcut sahnelere ek olarak bir sahneyi şöyle yükleyebilirsiniz:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

Defold'da yeni koleksiyonu yalnızca `Collection Proxy` bileşenine bir ileti göndererek yüklersiniz:

```lua
msg.post("#myproxy", "load")
```

1. Vekile `"load"` iletisini (veya eş zamansız yükleme için `"async_load"`) gönderdiğinizde motor yeni bir dünya için bellek ayırır, o koleksiyondaki her şeyin örneğini orada oluşturur ve dünyayı yalıtılmış tutar.
2. Yükleme tamamlandığında vekil, dünyanın hazır olduğunu belirten bir `"proxy_loaded"` iletisi gönderir.
3. Ardından genellikle, yeni dünyadaki nesnelerin normal yaşam döngülerine başlaması için `"init"` ve `"enable"` iletilerini gönderirsiniz.

Yüklenen dünyalar arasında iletişim kurmak için dünya adını (`collection:`, URL adresinin ilk bölümü) içeren URL adresleriyle açıkça ileti göndermeniz gerekir.

Bu yalıtım, bölüm geçişlerini, mini oyunları veya büyük modüler sistemleri uygularken büyük bir avantaj sağlayabilir; çünkü istenmeyen etkileşimleri önler ve gerektiğinde güncelleme zamanlamasının ayrı olarak yönetilmesine de izin verir (ör. duraklatma veya ağır çekim için).

Unity'de daha önce birden çok sahne kullanıp bunların bağımsız davranmasına ihtiyaç duyduysanız `Collection Proxy` bileşenini bu kavramı doğrudan Defold'a getirmenin bir yolu olarak düşünebilirsiniz.

Daha fazla ayrıntı için [Koleksiyon vekili kılavuzuna](/manuals/collection-proxy/) göz atın.

---

## Uygulama yaşam döngüsü

Unity'nin `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` veya `OnApplicationQuit` gibi yaşam döngüsü olaylarını biliyorsunuz.

Defold'un da iyi tanımlanmış bir uygulama yaşam döngüsü vardır; ancak kavramlar ve terimler farklıdır. Defold yaşam döngüsü aşamalarını, başlangıç işlemleri sırasında, her karede ve sonlandırma işlemleri sırasında motor tarafından çağrılan bir dizi önceden tanımlanmış Lua geri çağırımı üzerinden sunar.

İşte bir karşılaştırma:

| Defold | Unity | Açıklama |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold'un başlangıç işlemleri için tek bir giriş noktası ve geri çağırımı vardır: init(). Her bileşen oluşturulduğunda çağrılır. |
| `on_input` | Girdi yöntemleri | Defold, [betik için girdi odağı ayarlandığında](/manuals/input/#input-focus) girdileri alır. Güncelleme döngüsünde ilk olarak işlenir. |
| `fixed_update()` | `FixedUpdate()` | Sabit zaman adımıyla çağrılır. Defold'da etkinleştirmek için `Use Fixed Timestep` ayarını yapmanız gerekir - [ayrıntılar](https://defold.com/manuals/project-settings/#use-fixed-timestep). 1.12.0'dan itibaren `update()` çağrısından önce çalışır. |
| `update()` | `Update()` | Geçen süreyle birlikte kare başına bir kez çağrılır. |
| `late_update()` | `LateUpdate()` | `update()` çağrısından sonra, kare işlenmeden hemen önce çağrılır. 1.12.0'dan itibaren mevcuttur. |
| `on_message` | İleti alıcısı | Defold'un iletileri almak için kullandığı temel geri çağırımdır. Kuyrukta herhangi bir ileti olduğunda işlenir. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold, oyun nesnesi çalışma sırasında (`go.delete()` kullanılarak) silindiğinde veya dünya/koleksiyon bellekten kaldırıldığında her bileşen için, uygulama sonlandırılırken de kalan tüm nesneler için `final()` geri çağırımlarını çağırır. |

::: sidenote
Birden çok bileşenin başlangıç işlemleri/güncellemesi/kaldırılması aynı anda yapıldığında Defold'un bileşenler arasında herhangi bir yürütme sırasını garanti etmediğini unutmayın. Birbirine bağımlılığı azaltılmış tasarım önerilir.
:::

### Başlangıç işlemleri

Defold'un `init()` geri çağırımını, Unity'nin `Awake()`, `Start()` ve `OnEnable()` öğelerini tek bir giriş noktasında birleştiren bir yapı olarak düşünün. Motor bu noktada her şeyi zaten hazırlamıştır ve bileşeninizin durumunu güvenle hazırlayabilirsiniz.

### İletiler ne zaman işlenir?

`init()` içinde ileti gönderebildiğiniz için iletiler ilk kez başlangıç işlemlerinin hemen ardından dağıtılır.

İletiler daha sonra her dahili işleme döngüsünün ardından, kuyrukta bir şey olduğu her seferde işlenir; bu nedenle örneğin `on_message()` bir güncelleme döngüsünde birkaç kez bile çağrılabilir.

### Güncelleme döngüsü

Defold her karede bir dizi işlem yürütür: girdileri işler, iletileri dağıtır, betik ve GUI güncellemelerini tetikler, fiziği ve dönüşümleri uygular ve sonunda grafikleri işler.

### Sonlandırma işlemleri

Defold'da temizleme her zaman silmeye veya dünyanın bellekten kaldırılmasına bağlıdır ve bileşen başına tek çıkış kancanız `final()` geri çağırımıdır.

Unity'nin modelinden ince bir farkı, bir bileşenin devre dışı bırakılması ile uygulamanın tamamının kapanması arasında ayrım olmamasıdır.

### İşleme

İşleme betiği (`*.render_script`), işleme hattının bir parçasıdır ve kendi `init()`, `update()` ve `on_message()` geri çağırımlarıyla yaşam döngüsüne de katılır; ancak bu geri çağırımlar işleme iş parçacığında çalışır ve oyun nesnesi ile GUI betiği mantığından ayrıdır.

Daha fazla ayrıntı için [Uygulama yaşam döngüsü kılavuzunu](/manuals/application-lifecycle/) okuyun.

---

## GUI

Defold'un GUI sistemi, UI Toolkit veya Canvas kullanan uGUI'ye benzer şekilde; menüler, üst katmanlar, iletişim kutuları ve diğer öğelerden oluşan kullanıcı arayüzlerine ayrılmış tek ve bütünlüklü bir çatıdır.

GUI bir bileşendir ve oyun nesneleriyle koleksiyonlardan ayrıdır. Oyun nesneleri yerine, hiyerarşi içinde düzenlenmiş ve bir GUI betiğiyle yönetilen GUI düğümleriyle çalışırsınız.

### GUI düğümleri

Defold'da bir `*.gui` bileşen dosyasını açtığınızda `"GUI nodes"` öğelerini yerleştirdiğiniz bir tuval sunulur. Bunlar GUI'nin yapı taşlarıdır. Şu türlerde GUI düğümleri ekleyebilirsiniz:

- Box (dokuya sahip dikdörtgen şekil)
- Text (herhangi bir yazı tipiyle)
- Pie (dokuya sahip, radyal dolgu sağlayan daire dilimi öğesi)
- ParticleFX
- Template (GUI prefabı gibi, iç içe yerleştirilmiş başka bir `.gui` dosyasının tamamı)
- ve Spine eklentisini kullanırken Spine düğümü.

### GUI betiği

GUI bileşeninin GUI betikleri için özel bir özelliği vardır: bileşen başına bir `*.gui_script` dosyası atarsınız ve bu, bileşenin davranışını değiştirmenizi sağlar. Dolayısıyla normal betiklere çok benzer; ancak oyun nesnesi betiklerine yönelik olan `go.*` ad alanını kullanmaz. Bunun yerine yalnızca GUI betiklerinin (`*.gui_script`) içinde çalışan özel `gui.*` ad alanı API'sini kullanır. Bunu, Canvas kullanan Unity UI (uGUI) gibi ayrı bir sahne olarak düşünebilirsiniz.

### GUI işleme

GUI öğeleri, oyun kamerasından bağımsız olarak ve genellikle ekran uzayında işlenir; ancak bu davranış özel işleme hatlarında değiştirilebilir.

Daha fazla ayrıntı için [GUI kılavuzunu](/manuals/gui/) okuyun.

## Sorting Layers nerede?

Unity'den geçerken bu konu çok sık kafa karışıklığına yol açar.

GUI bileşenlerinin `Layers` özelliği vardır ve bu, Unity'deki "Sorting Layers" ile neredeyse aynı şekilde çalışır; ancak `Sprites`, `Tilemaps`, `Models` vb. diğer bileşenler için doğrudan bir karşılığı yoktur.

Bunun yerine genellikle şunları birleştirirsiniz:
- Varsayılan kamera kullanırken Z ekseni veya Camera bileşeni kullanırken derinlik üzerinden ayrıntılı sıralama.
- Materyal etiketlerine göre neyin çizileceğini seçmek için işleme yüklemlerini kullanan işleme betiği üzerinden genel sıralama.

Ancak çok sayıda etiketle Unity Sorting Layers davranışını taklit etmeniz önerilmez; çünkü Defold'da etiketler işleme düzeyinde bir mekanizmadır. Bunları aşırı kullanmak toplu çizimi bozabilir ve çizimin ek yükünü artırabilir.

---

## Buradan sonra nereye geçmeli?

- [Defold örnekleri](/examples)
- [Öğreticiler](/tutorials)
- [Kılavuzlar](/manuals)
- [API başvuru belgeleri](/ref/go)
- [Sık sorulan sorular](/faq/faq)

Sorularınız varsa veya takılırsanız [Defold Forumu](//forum.defold.com) veya [Discord](https://defold.com/discord/) yardım istemek için çok iyi yerlerdir.
