---
title: Defold'un yapı taşları
brief: Bu kılavuz, oyun nesnelerinin, bileşenlerin ve koleksiyonların nasıl çalıştığını ayrıntılı olarak ele alır.
---

#  Yapı taşları

Defold'un tasarımının temelinde, iyi kavranması çok önemli olan birkaç kavram bulunur. Bu kılavuz, Defold'un yapı taşlarının neler olduğunu açıklar. Bu kılavuzu okuduktan sonra [adresleme kılavuzuna](/manuals/addressing) ve [ileti aktarımı kılavuzuna](/manuals/message-passing) geçin. Hızla başlamanıza yardımcı olmak için düzenleyicinin içinden de erişebileceğiniz bir dizi [öğretici](/tutorials/getting-started) bulunur.

![Yapı taşları](images/building_blocks/building_blocks.png)

Bir Defold oyunu oluştururken kullandığınız üç temel yapı taşı türü vardır:

Koleksiyon
: Koleksiyon (collection), oyununuzu yapılandırmak için kullanılan bir dosyadır. Koleksiyonlarda oyun nesnelerinden ve diğer koleksiyonlardan oluşan hiyerarşiler oluşturursunuz. Bunlar genellikle oyun bölümlerini, düşman gruplarını veya birden fazla oyun nesnesinden oluşan karakterleri yapılandırmak için kullanılır.

Oyun nesnesi
: Oyun nesnesi (game object), bir tanımlayıcıya, konuma, dönme değerine ve ölçeğe sahip bir kapsayıcıdır. Bileşenleri barındırmak için kullanılır. Oyun nesneleri genellikle oyuncu karakterlerini, mermileri, oyunun kural sistemini veya bir bölüm yükleyicisini oluşturmak için kullanılır.

Bileşen
: Bileşenler (component), oyun nesnelerine oyunda görsel, işitsel ve/veya mantıksal bir karşılık kazandırmak için bu nesnelerin içine yerleştirilen öğelerdir. Bunlar genellikle karakter sprite bileşenleri ve betik dosyaları oluşturmak, ses efektleri veya parçacık efektleri eklemek için kullanılır.

## Koleksiyonlar {#collections}

Koleksiyonlar, oyun nesnelerini ve diğer koleksiyonları barındıran ağaç yapılarıdır. Bir koleksiyon her zaman bir dosyada saklanır.

Defold motoru başladığında, *game.project* ayar dosyasında belirtilen tek bir _başlangıç koleksiyonunu_ (bootstrap collection) yükler. Başlangıç koleksiyonu genellikle "main.collection" olarak adlandırılır, ancak istediğiniz adı kullanabilirsiniz.

Bir koleksiyon, istenen derinlikte iç içe yerleştirilmiş oyun nesneleri ve diğer koleksiyonları (alt koleksiyonun dosyasına başvurarak) içerebilir. Aşağıda "main.collection" adlı bir örnek dosya gösterilmektedir. Bu dosya bir oyun nesnesi (tanımlayıcısı "can") ve bir alt koleksiyon (tanımlayıcısı "bean") içerir. Alt koleksiyon ise iki oyun nesnesi içerir: "bean" ve "shield".

![Koleksiyon](images/building_blocks/collection.png)

"bean" tanımlayıcılı alt koleksiyonun "/main/bean.collection" adlı kendi dosyasında saklandığına ve "main.collection" dosyasında yalnızca bu dosyaya başvurulduğuna dikkat edin:

![Bean koleksiyonu](images/building_blocks/bean_collection.png)

"main" ve "bean" koleksiyonlarına karşılık gelen çalışma zamanı nesneleri olmadığından koleksiyonların kendilerini adresleyemezsiniz. Ancak bazen bir oyun nesnesine giden _yolun_ parçası olarak koleksiyonun kimliğini kullanmanız gerekir (ayrıntılar için [adresleme kılavuzuna](/manuals/addressing) bakın):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Bir koleksiyon, başka bir koleksiyona her zaman bir koleksiyon dosyasına başvuru olarak eklenir:

*Outline* görünümündeki koleksiyona <kbd>sağ tıklayın</kbd> ve <kbd>Add Collection File</kbd> seçeneğini seçin.

## Oyun nesneleri

Oyun nesneleri, oyununuz çalışırken her biri ayrı bir yaşam süresine sahip olan basit nesnelerdir. Oyun nesnelerinin konum, dönme ve ölçek değerleri vardır; bunların her biri çalışma sırasında değiştirilebilir ve her birine animasyon uygulanabilir.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Oyun nesneleri boş olarak kullanılabilir (örneğin konum işaretleyicileri olarak), ancak genellikle sprite, ses, betik, model, fabrika ve diğer çeşitli bileşenlerle donatılır. Oyun nesneleri düzenleyicide oluşturulup koleksiyon dosyalarına yerleştirilir veya çalışma sırasında _fabrika_ (factory) bileşenleri aracılığıyla dinamik olarak oluşturulur.

Oyun nesneleri bir koleksiyona yerinde eklenir veya bir oyun nesnesi dosyasına başvuru olarak eklenir:

*Outline* görünümündeki koleksiyona <kbd>sağ tıklayın</kbd> ve <kbd>Add Game Object</kbd> (yerinde eklemek için) veya <kbd>Add Game Object File</kbd> (dosya başvurusu olarak eklemek için) seçeneğini seçin.


## Bileşenler

:[components](../shared/components.md)

Kullanılabilir tüm bileşen türlerinin listesi için [bileşenlere genel bakış](/manuals/components/) sayfasına bakın.

## Yerinde veya başvuru yoluyla eklenen nesneler

Bir koleksiyon, oyun nesnesi veya bileşen _dosyası_ oluşturduğunuzda, prototip (prototype) adını verdiğimiz bir tanım oluşturursunuz (diğer motorlarda "prefabs" veya "blueprints" olarak da bilinir). Bu işlem yalnızca projenin dosya yapısına bir dosya ekler; çalışan oyununuza hiçbir şey eklenmez. Bir prototip dosyasına dayalı koleksiyon, oyun nesnesi veya bileşen örneği (instance) eklemek için koleksiyon dosyalarınızdan birine onun bir örneğini eklersiniz.

Bir nesne örneğinin hangi dosyaya dayandığını Outline görünümünde görebilirsiniz. "main.collection" dosyası, dosyalara dayalı üç örnek içerir:

1. "bean" alt koleksiyonu.
2. "bean" alt koleksiyonundaki "bean" oyun nesnesinde bulunan "bean" betik bileşeni.
3. "can" oyun nesnesindeki "can" betik bileşeni.

![Örnek](images/building_blocks/instance.png)

Bir oyun nesnesinin veya koleksiyonun birden fazla örneğine sahip olduğunuzda ve hepsini değiştirmek istediğinizde prototip dosyaları oluşturmanın yararı ortaya çıkar:

![Oyun nesnesi örnekleri](images/building_blocks/go_instance.png)

Prototip dosyasını değiştirdiğinizde, o dosyayı kullanan tüm örnekler hemen güncellenir.

![Oyun nesnesi prototipini değiştirme](images/building_blocks/go_change_blueprint.png)

Burada prototip dosyasının sprite görüntüsü değiştirilir ve dosyayı kullanan tüm örnekler hemen güncellenir:

![Güncellenen oyun nesnesi örnekleri](images/building_blocks/go_instance2.png)

## Oyun nesnelerini alt nesne olarak bağlama

Bir koleksiyon dosyasında, bir veya daha fazla oyun nesnesinin tek bir üst oyun nesnesine alt nesne olarak bağlı olduğu oyun nesnesi hiyerarşileri oluşturabilirsiniz. Bir oyun nesnesini <kbd>sürükleyip</kbd> diğerinin üzerine <kbd>bıraktığınızda</kbd>, sürüklenen oyun nesnesi hedefin alt nesnesi olur:

![Oyun nesnelerini alt nesne olarak bağlama](images/building_blocks/childing.png)

Üst-alt nesne hiyerarşileri, nesnelerin dönüşümlere nasıl tepki verdiğini etkileyen dinamik ilişkilerdir. Bir nesneye uygulanan her dönüşüm (hareket, döndürme veya ölçekleme), hem düzenleyicide hem de çalışma sırasında o nesnenin alt nesnelerine de uygulanır:

![Alt nesnenin dönüşümü](images/building_blocks/child_transform.png)

Buna karşılık, bir alt nesnenin ötelemeleri üst nesnenin yerel uzayında yapılır. Düzenleyicide <kbd>Edit ▸ World Space</kbd> (varsayılan) veya <kbd>Edit ▸ Local Space</kbd> seçeneğini seçerek bir alt oyun nesnesini yerel uzayda veya dünya uzayında düzenleyebilirsiniz.

Bir nesneye `set_parent` iletisi göndererek çalışma sırasında üst nesnesini değiştirmek de mümkündür.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Yaygın bir yanlış anlama, bir oyun nesnesinin üst-alt nesne hiyerarşisinin parçası olduğunda koleksiyon hiyerarşisindeki yerinin değiştiğidir. Oysa bunlar birbirinden çok farklı iki kavramdır. Üst-alt nesne hiyerarşileri sahne grafını dinamik olarak değiştirerek nesnelerin görsel olarak birbirine bağlanmasını sağlar. Bir oyun nesnesinin adresini belirleyen tek şey, koleksiyon hiyerarşisindeki yeridir. Adres, nesnenin yaşam süresi boyunca sabit kalır.
:::
