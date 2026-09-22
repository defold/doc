---
title: Betik bileşeni özellikleri
brief: Bu kılavuz, betik bileşenlerine özel özelliklerin nasıl ekleneceğini ve bunlara düzenleyiciden ve çalışma zamanı betiklerinden nasıl erişileceğini açıklar.
---

# Betik özellikleri

Betik özellikleri (script properties), belirli bir oyun nesnesi (game object) örneği için özel özellikler tanımlamanın ve bunları dışarıya açmanın basit ve güçlü bir yolunu sunar. Betik özellikleri, belirli örneklerde doğrudan düzenleyicide değiştirilebilir ve ayarları, bir oyun nesnesinin davranışını değiştirmek için kodda kullanılabilir. Betik özelliklerinin çok yararlı olduğu birçok durum vardır:

* Düzenleyicide belirli örnekler için değerleri geçersiz kılmak ve böylece betiğin yeniden kullanılabilirliğini artırmak istediğinizde.
* Bir oyun nesnesini başlangıç değerleriyle çalışma sırasında oluşturmak istediğinizde.
* Bir özelliğin değerlerine animasyon uygulamak istediğinizde.
* Bir betikteki durum verilerine başka bir betikten erişmek istediğinizde. (Nesneler arasında özelliklere sık sık erişiyorsanız verileri paylaşılan bir depolama alanına taşımanın daha iyi olabileceğini unutmayın.)

Yaygın kullanım örnekleri arasında belirli bir düşman yapay zekâsının canını veya hızını, toplanabilir bir nesnenin renk çarpanını (tint), bir sprite bileşeninin atlasını ya da bir düğme nesnesine basıldığında hangi iletinin gönderileceğini ve/veya nereye gönderileceğini ayarlamak yer alır.

## Betik özelliği tanımlama

Betik özellikleri, özel `go.property()` işleviyle tanımlanarak bir betik bileşenine (script component) eklenir. Bu işlevin en üst düzeyde, yani `init()` ve `update()` gibi yaşam döngüsü işlevlerinin dışında kullanılması gerekir. Özellik için verilen varsayılan değer, özelliğin türünü belirler: `number`, `boolean`, `string`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` ve `resource` (aşağıya bakın).

::: important
Karma değerinden (hash value) özgün dizeyi geri elde etmenin, hata ayıklamayı kolaylaştırmak amacıyla yalnızca Debug derlemesinde çalıştığını unutmayın. Release derlemesinde geri elde edilebilecek dize değeri bulunmaz; bu nedenle `tostring()` işlevini bir `hash` değeri üzerinde kullanarak bu değerden dizeyi elde etmeye çalışmak anlamsızdır.
:::


```lua
-- can.script
-- Define script properties for health and an attack target
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- store initial position of target.
  -- self.target is a url referencing another object.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- decrease the health property
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

Ardından, bu betikten oluşturulan her betik bileşeni örneği için özellik değerleri ayarlanabilir.

![Özellikleri olan bileşen](images/script-properties/component.png)

 Düzenleyicideki *Outline* görünümünde betik bileşenini seçin; özellikler, düzenleyebilmeniz için *Properties* görünümünde belirir:

![Properties görünümü](images/script-properties/properties.png)

Örneğe özgü yeni bir değerle geçersiz kılınan her özellik mavi renkle işaretlenir. Değeri varsayılana (betikte ayarlanan değere) döndürmek için özellik adının yanındaki sıfırlama düğmesine tıklayın.


::: important
Betik özellikleri proje derlenirken ayrıştırılır. Değer ifadeleri değerlendirilmez. Bu, `go.property("hp", 3+6)` gibi bir ifadenin çalışmayacağı, ancak `go.property("hp", 9)` ifadesinin çalışacağı anlamına gelir.
:::

### Metin özellikleri

Defold 1.13.2 sürümünden itibaren, varsayılan değer olarak verilen bir dize bir metin özelliği tanımlar. Metin özellikleri UTF-8 ve yeni satır karakterlerini destekler ve düzenleyicide çok satırlı bir alanda düzenlenir:

```lua
go.property("greeting", "Hello!\nWelcome, José!")

function init(self)
    go.set("#label", "text", self.greeting)
end
```

Diğer betik özelliklerinde olduğu gibi metin özelliklerini de geçersiz kılmak için bir oyun nesnesindeki veya koleksiyondaki (collection) betik bileşenini seçin. Varsayılan değerlerde veya bunları geçersiz kılan değerlerde gömülü NUL karakterlerine izin verilmez.

Diğer betikler, betik bileşeninin URL adresi üzerinden bir metin özelliğini okuyabilir ve yazabilir. Örneğin, yukarıdaki betiği ve bir etiket (label) bileşenini koleksiyondaki `speaker` adlı oyun nesnesine, bileşen tanımlayıcıları `script` ve `label` olacak şekilde ekleyin. Bunları başka bir betiğin `init()` işlevinden güncelleyin:

```lua
function init(self)
    local greeting = go.get("/speaker#script", "greeting")
    go.set("/speaker#script", "greeting", greeting .. "\nEnjoy the game!")
    go.set("/speaker#label", "text", go.get("/speaker#script", "greeting"))
end
```

Betik özelliğini değiştirmek, etiket bileşenini otomatik olarak güncellemez; son satır yeni değeri açıkça etiket bileşeninin `text` özelliğine kopyalar.

## Betik özelliklerine erişme

Tanımlanmış her betik özelliğine, betik örneği başvurusu olan `self` içinde saklanan bir üye olarak erişilebilir:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Read and write the property
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Kullanıcı tanımlı betik özellikleri `go.get()` ile de okunabilir ve `go.set()` ile yazılabilir. Vektörler ve kuaterniyonlar (quaternion) dahil sayısal özelliklere `go.animate()` ile animasyon uygulanabilir. Metin özellikleri okunabilir ve yazılabilir, ancak bunlara animasyon uygulanamaz:

```lua
-- another.script

-- increase "my_property" in "myobject#script" by 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animate "my_property" in "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Fabrikayla oluşturulan nesneler

Oyun nesnesini oluşturmak için bir fabrika (factory) kullanıyorsanız betik özelliklerini oluşturma anında ayarlayabilirsiniz:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accessing factory-created script properties
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

`collectionfactory.create()` aracılığıyla çalışma sırasında bir oyun nesnesi hiyerarşisi oluştururken nesne tanımlayıcılarını özellik tablolarıyla eşleştirmeniz gerekir. Bunlar bir tabloda bir araya getirilir ve `create()` işlevine iletilir:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

`factory.create()` ve `collectionfactory.create()` aracılığıyla verilen özellik değerleri, prototip dosyasında ayarlanan tüm değerlerin yanı sıra betikteki varsayılan değerleri de geçersiz kılar.

Bir oyun nesnesine bağlı birden çok betik bileşeni aynı özelliği tanımlıyorsa her bileşen, `factory.create()` veya `collectionfactory.create()` işlevine verilen değerle başlatılır.


## Kaynak özellikleri {#resource-properties}

Kaynak özellikleri (resource properties), temel veri türlerine ait betik özellikleriyle aynı şekilde tanımlanır:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Bir kaynak özelliği tanımlandığında, diğer betik özellikleri gibi *Properties* görünümünde belirir; ancak dosya/kaynak seçmeye yarayan bir alan olarak gösterilir:

![Kaynak özellikleri](images/script-properties/resource-properties.png)

Kaynak özelliklerine `go.get()` ile veya `self` betik örneği başvurusu üzerinden erişir ve bunları `go.set()` ile kullanırsınız:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
