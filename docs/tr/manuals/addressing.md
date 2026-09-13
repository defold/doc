---
title: Defold'da adresleme
brief: Bu kılavuz, Defold'un adresleme sorununu nasıl çözdüğünü açıklar.
---

# Adresleme

Çalışan bir oyunu denetleyen kod, oyuncunun gördüğü ve duyduğu öğeleri taşımak, ölçeklemek, canlandırmak, silmek ve değiştirmek için her nesneye ve bileşene (component) erişebilmelidir. Defold'un adresleme (addressing) mekanizması bunu mümkün kılar.

## Tanımlayıcılar

Defold, oyun nesnelerine (game object) ve bileşenlere başvurmak için adresler (veya URL'ler; şimdilik bunu bir kenara bırakalım) kullanır. Bu adresler tanımlayıcılardan (identifier) oluşur. Aşağıdakilerin tümü, Defold'un adresleri nasıl kullandığına ilişkin örneklerdir. Bu kılavuz boyunca bunların nasıl çalıştığını ayrıntılı olarak inceleyeceğiz:

```lua
local id = factory.create("#enemy_factory")
go.set("my_gameobject#my_label", "text", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Çok basit bir örnekle başlayalım. Tek bir sprite bileşeni içeren bir oyun nesneniz olduğunu varsayalım. Oyun nesnesini denetlemek için bir betik bileşeniniz (script component) de var. Düzenleyicideki yapı şuna benzer:

![Düzenleyicide bean](images/addressing/bean_editor.png)

Şimdi, daha sonra görünür kılabilmek için oyun başladığında sprite bileşenini devre dışı bırakmak istiyorsunuz. Aşağıdaki kodu "controller.script" dosyasına ekleyerek bunu kolayca yapabilirsiniz:

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. '#' karakteri kafanızı karıştırdıysa endişelenmeyin. Birazdan buna değineceğiz.

Bu kod beklendiği gibi çalışır. Oyun başladığında betik bileşeni, sprite bileşenini "body" tanımlayıcısıyla *adresler* ve bu adresi kullanarak ona "disable" adlı bir *ileti* (message) gönderir. Bu özel motor iletisi, sprite bileşeninin sprite görselini gizlemesini sağlar. Yapı şematik olarak şöyle görünür:

![bean](images/addressing/bean.png)

Bu yapıdaki tanımlayıcılar geliştirici tarafından belirlenir ve kendi adlandırma bağlamları (naming context) içinde benzersiz olmalıdır. Burada oyun nesnesine "bean" tanımlayıcısını vermeyi seçtik; sprite bileşenine "body", karakteri denetleyen betik bileşenine ise "controller" adını verdik. Dize olarak yazılan URL adreslerinde kullanılan tanımlayıcılar `:` veya `#` içermemelidir; çünkü URL sözdiziminde `:` karakteri soket ayırıcısı, `#` karakteri ise oyun nesnesi/bileşen ayırıcısı olarak kullanılmak üzere ayrılmıştır. URL ayrıştırıcısı bunların dışında noktalama işaretlerini reddetmez.

::: sidenote
Bir ad seçmezseniz düzenleyici sizin yerinize seçer. Düzenleyicide yeni bir oyun nesnesi veya bileşen oluşturduğunuzda, benzersiz bir *Id* özelliği otomatik olarak ayarlanır.

- Oyun nesnelerine otomatik olarak, bir sıra numarasıyla birlikte "go" adlı bir tanımlayıcı verilir ("go2", "go3" vb.).
- Bileşenlere, bileşen türüne karşılık gelen bir tanımlayıcı verilir ("sprite", "sprite2" vb.).

İsterseniz otomatik olarak atanan bu adları kullanmayı sürdürebilirsiniz, ancak tanımlayıcıları uygun ve açıklayıcı adlarla değiştirmenizi öneririz.
:::

Şimdi başka bir sprite bileşeni ekleyip bean nesnesine bir kalkan verelim:

![bean](images/addressing/bean_shield_editor.png)

Yeni bileşenin oyun nesnesi içinde benzersiz bir tanımlayıcısı olmalıdır. Ona "body" adını verseydiniz, betik kodunun "disable" iletisini hangi sprite bileşenine göndermesi gerektiği belirsiz olurdu. Bu nedenle benzersiz (ve açıklayıcı) "shield" tanımlayıcısını seçiyoruz. Artık "body" ve "shield" sprite bileşenlerini istediğimiz gibi etkinleştirebilir ve devre dışı bırakabiliriz.

![bean](images/addressing/bean_shield.png)

::: sidenote
Bir tanımlayıcıyı birden fazla kez kullanmaya çalışırsanız düzenleyici hata bildirir; dolayısıyla bu durum uygulamada hiçbir zaman sorun olmaz:

![bean](images/addressing/name_collision.png)
:::

Şimdi daha fazla oyun nesnesi eklerseniz neler olacağına bakalım. İki "bean" nesnesini eşleştirerek küçük bir takım oluşturmak istediğinizi varsayalım. Bu oyun nesnelerinden birine "bean", diğerine "buddy" adını vermeye karar veriyorsunuz. Ayrıca, "bean" bir süre boşta kaldığında "buddy" nesnesine dans etmeye başlamasını söylemelidir. Bunun için "bean" içindeki "controller" betik bileşeninden "buddy" içindeki "controller" betiğine "dance" adlı özel bir ileti gönderilir:

![bean](images/addressing/bean_buddy.png)

::: sidenote
Her oyun nesnesinde bir tane olmak üzere "controller" adlı iki ayrı bileşen vardır, ancak her oyun nesnesi yeni bir adlandırma bağlamı oluşturduğundan bu tamamen geçerlidir.
:::

İletinin alıcısı, iletiyi gönderen oyun nesnesinin ("bean") dışında olduğundan, kodun iletiyi hangi "controller" bileşeninin alacağını belirtmesi gerekir. Hem hedef oyun nesnesinin tanımlayıcısı hem de bileşenin tanımlayıcısı belirtilmelidir. Bileşenin tam adresi `"buddy#controller"` olur ve bu adres iki ayrı bölümden oluşur.

- Önce hedef oyun nesnesinin tanımlayıcısı ("buddy") gelir,
- ardından oyun nesnesi/bileşen ayırıcı karakteri ("#") gelir,
- son olarak hedef bileşenin tanımlayıcısını ("controller") yazarsınız.

Tek bir oyun nesnesi içeren önceki örneğe dönersek, hedef adresin oyun nesnesi tanımlayıcısı bölümünü yazmadığımızda kodun *geçerli oyun nesnesindeki* bileşenleri adresleyebildiğini görürüz.

Örneğin, `"#body"` geçerli oyun nesnesindeki "body" bileşeninin adresini belirtir. Bu çok kullanışlıdır; çünkü bu kod, "body" bileşeni bulunduğu sürece *herhangi bir* oyun nesnesinde çalışır.

## Koleksiyonlar

Koleksiyonlar (collection), oyun nesnesi grupları veya hiyerarşileri oluşturmanızı ve bunları kontrollü bir şekilde yeniden kullanmanızı sağlar. Oyununuza içerik eklerken düzenleyicide koleksiyon dosyalarını şablon (ya da "prototip" veya "prefab") olarak kullanırsınız.

Çok sayıda bean/buddy takımı oluşturmak istediğinizi varsayalım. Bunun iyi bir yolu, yeni bir *koleksiyon dosyasında* bir şablon oluşturmaktır (dosyaya "team.collection" adını verin). Takımın oyun nesnelerini koleksiyon dosyasında oluşturup dosyayı kaydedin. Ardından bu koleksiyon dosyasının içeriğinin bir örneğini (instance) ana başlangıç koleksiyonunuza (bootstrap collection) yerleştirin ve örneğe bir tanımlayıcı verin ("team_1" adını verin):

![bean](images/addressing/team_editor.png)

Bu yapıda "bean" oyun nesnesi, `"buddy#controller"` adresiyle "buddy" içindeki "controller" bileşenine başvurmaya devam edebilir.

![bean](images/addressing/collection_team.png)

"team.collection" dosyasının ikinci bir örneğini eklerseniz ("team_2" adını verin), "team_2" içindeki betik bileşenlerinde çalışan kod da aynı şekilde çalışır. "team_2" koleksiyonundaki "bean" oyun nesnesi örneği, "buddy" içindeki "controller" bileşenini yine `"buddy#controller"` adresiyle adresleyebilir.

![bean](images/addressing/teams_editor.png)

## Göreli adresleme

`"buddy#controller"` adresi, *göreli* (relative) bir adres olduğu için her iki koleksiyondaki oyun nesneleri için de çalışır. "team_1" ve "team_2" koleksiyonlarının her biri yeni bir adlandırma bağlamı, başka bir deyişle bir "ad alanı" (namespace) oluşturur. Defold, adresleme sırasında koleksiyonun oluşturduğu adlandırma bağlamını dikkate alarak ad çakışmalarını önler:

![Göreli tanımlayıcı](images/addressing/relative_same.png)

- "team_1" adlandırma bağlamı içinde "bean" ve "buddy" oyun nesneleri benzersiz olarak tanımlanır.
- Benzer şekilde, "team_2" adlandırma bağlamı içinde de "bean" ve "buddy" oyun nesneleri benzersiz olarak tanımlanır.

Göreli adresleme, bir hedef adres çözümlenirken başına geçerli adlandırma bağlamının otomatik olarak eklenmesiyle çalışır. Bu da son derece kullanışlı ve güçlüdür; çünkü kodlarıyla birlikte oyun nesnesi grupları oluşturabilir ve bunları oyunun tamamında verimli bir şekilde yeniden kullanabilirsiniz.

### Kısa gösterimler

Defold, tam bir URL belirtmeden ileti göndermek için kullanabileceğiniz iki kullanışlı kısa gösterim sunar:

:[Shorthands](../shared/url-shorthands.md)

## Oyun nesnesi yolları

Adlandırma mekanizmasını doğru anlamak için projeyi derleyip çalıştırdığınızda neler olduğuna bakalım:

1. Düzenleyici, başlangıç koleksiyonunu ("main.collection") ve içeriğinin tamamını (oyun nesneleri ve diğer koleksiyonlar) okur.
2. Derleyici, her statik oyun nesnesi için bir tanımlayıcı oluşturur. Bunlar, başlangıç koleksiyonunun kökünden başlayıp koleksiyon hiyerarşisinde nesneye kadar inen "yollar" olarak oluşturulur. Her düzeyde bir '/' karakteri eklenir.

Yukarıdaki örneğimizde oyun, aşağıdaki 4 oyun nesnesiyle çalışır:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Tanımlayıcılar karma değerleri (hash) olarak saklanır. Çalışma zamanı ortamı, her koleksiyon tanımlayıcısının karma durumunu da saklar; bu durum, göreli dizenin karma hesaplamasını sürdürüp mutlak bir tanımlayıcı elde etmek için kullanılır.
:::

Çalışma sırasında koleksiyon gruplaması mevcut değildir. Belirli bir oyun nesnesinin derlemeden önce hangi koleksiyona ait olduğunu öğrenmenin bir yolu yoktur. Bir koleksiyondaki tüm nesneleri aynı anda değiştirmek de mümkün değildir. Bu tür işlemler yapmanız gerekiyorsa takibi kodda kendiniz kolayca yapabilirsiniz. Her nesnenin tanımlayıcısı statiktir ve nesnenin yaşam süresi boyunca sabit kalması garanti edilir. Bu, bir nesnenin tanımlayıcısını güvenle saklayıp daha sonra kullanabileceğiniz anlamına gelir.

## Mutlak adresleme

Adresleme sırasında yukarıda açıklanan tam tanımlayıcıları kullanmak mümkündür. Çoğu durumda içeriğin yeniden kullanılmasını sağladığı için göreli adresleme tercih edilir, ancak mutlak adreslemenin (absolute addressing) gerekli olduğu durumlar da vardır.

Örneğin, her bean nesnesinin durumunu izleyen bir yapay zekâ yöneticisi istediğinizi varsayalım. Bean nesnelerinin geçerli durumlarını yöneticiye bildirmesini, yöneticinin de bu durumlara göre taktik kararlar alıp bean nesnelerine emir vermesini istiyorsunuz. Bu durumda, betik bileşeni içeren tek bir yönetici oyun nesnesi oluşturup bunu başlangıç koleksiyonunda takım koleksiyonlarının yanına yerleştirmek oldukça mantıklı olur.

![Yönetici nesnesi](images/addressing/manager_editor.png)

Bu durumda her bean nesnesi, yöneticiye durum iletileri göndermekten sorumludur: Bir düşman görürse "contact", vurulup hasar alırsa "ouch!". Bunun çalışması için bean nesnesinin denetleyici betiği, "manager" içindeki "controller" bileşenine ileti göndermek üzere mutlak adreslemeyi kullanır.

'/' ile başlayan her adres, oyun dünyasının kökünden çözümlenir. Bu, oyun başlangıcında yüklenen *başlangıç koleksiyonunun* köküne karşılık gelir.

Yönetici betiğinin mutlak adresi `"/manager#controller"` olur ve bu mutlak adres, nerede kullanılırsa kullanılsın doğru bileşene çözümlenir.

![Takımlar ve yönetici](images/addressing/teams_manager.png)

![Mutlak adresleme](images/addressing/absolute.png)

## Karma değeri alınmış tanımlayıcılar

Motor, tüm tanımlayıcıları karma değerleri olarak saklar. Bağımsız değişken olarak bileşen veya oyun nesnesi alan tüm işlevler bir dize, karma değeri veya URL nesnesi kabul eder. Yukarıda, adresleme için dizelerin nasıl kullanıldığını gördük.

Bir oyun nesnesinin tanımlayıcısını aldığınızda motor her zaman karma değeri alınmış bir mutlak yol tanımlayıcısı döndürür:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Böyle bir tanımlayıcıyı dize tanımlayıcısının yerine kullanabilir veya kendiniz oluşturabilirsiniz. Ancak karma değeri alınmış bir tanımlayıcının nesnenin yoluna, yani mutlak bir adrese karşılık geldiğini unutmayın:

::: sidenote
Göreli adreslerin dize olarak verilmesi gerekir; çünkü motor, geçerli adlandırma bağlamının (koleksiyonun) karma durumunu temel alıp verilen dizeyi karma hesaplamasına ekleyerek yeni bir karma tanımlayıcısı hesaplar.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL'ler {#urls}

Konuyu tamamlamak için Defold adreslerinin tam biçimi olan URL'ye bakalım.

URL, genellikle özel bir biçime sahip dize olarak yazılan bir nesnedir. Genel bir URL üç bölümden oluşur:

`[socket:][path][#fragment]`

socket
: Hedefin oyun dünyasını tanımlar. [Koleksiyon vekilleriyle (collection proxy)](/manuals/collection-proxy) çalışırken bu önemlidir ve bu durumda _dinamik olarak yüklenen koleksiyonu_ tanımlamak için kullanılır.

path
: URL'nin bu bölümü, hedef oyun nesnesinin tam tanımlayıcısını içerir.

fragment
: Belirtilen oyun nesnesi içindeki hedef bileşenin tanımlayıcısıdır.

Yukarıda gördüğümüz gibi, çoğu durumda bu bilgilerin bir kısmını veya çoğunu yazmayabilirsiniz. Soketi (socket) belirtmeniz neredeyse hiçbir zaman gerekmez; yolu belirtmeniz ise her zaman olmasa da çoğunlukla gerekir. Başka bir oyun dünyasındaki öğeleri adreslemeniz gerektiğinde URL'nin soket bölümünü belirtmeniz gerekir. Örneğin, yukarıdaki "manager" oyun nesnesindeki "controller" betiğinin tam URL dizesi şöyledir:

`"main:/manager#controller"`

team_2 içindeki buddy denetleyicisinin adresi ise şöyledir:

`"main:/team_2/buddy#controller"`

Bu adreslere ileti gönderebiliriz:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## URL nesneleri oluşturma

URL nesneleri Lua koduyla da oluşturulabilir:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
