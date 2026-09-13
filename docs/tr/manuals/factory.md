---
title: Fabrika bileşeni kılavuzu
brief: Bu kılavuz, oyun nesnelerini çalışma sırasında dinamik olarak oluşturmak için fabrika bileşenlerinin nasıl kullanılacağını açıklar.
---

# Fabrika bileşenleri

Fabrika bileşenleri (factory components), çalışan bir oyunda bir nesne havuzundan oyun nesnelerini (game object) dinamik olarak oluşturmak için kullanılır.

Bir oyun nesnesine fabrika bileşeni eklediğinizde, fabrikanın oluşturacağı tüm yeni oyun nesneleri için hangi oyun nesnesi dosyasını prototip (prototype; diğer motorlarda "prefabs" veya "blueprints" olarak da bilinir) olarak kullanacağını *Prototype* özelliğinde belirtirsiniz.

![Fabrika bileşeni](images/factory/factory_collection.png)

![Fabrika bileşeni](images/factory/factory_component.png)

Bir oyun nesnesinin oluşturulmasını tetiklemek için `factory.create()` işlevini çağırın:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Çalışma sırasında oluşturulan oyun nesnesi](images/factory/factory_spawned.png)

`factory.create()` 5 parametre alır:

`url`
: Yeni bir oyun nesnesi oluşturacak fabrika bileşeninin tanımlayıcısı.

`[position]`
: (isteğe bağlı) Yeni oyun nesnesinin dünya uzayındaki konumu. Bu değer `vector3` türünde olmalıdır. Konum belirtmezseniz oyun nesnesi, `factory.create()` işlevini çağıran oyun nesnesinin konumunda oluşturulur.

`[rotation]`
: (isteğe bağlı) Yeni oyun nesnesinin dünya uzayındaki dönme değeri. Bu değer `quat` türünde olmalıdır.

`[properties]`
: (isteğe bağlı) Oyun nesnesini başlatırken kullanılacak betik özelliği değerlerini içeren bir Lua tablosu. Betik özellikleri hakkında bilgi için [Betik özellikleri kılavuzuna](/manuals/script-properties) bakın.

`[scale]`
: (isteğe bağlı) Oluşturulan oyun nesnesinin ölçeği. Ölçek, tüm eksenlerde aynı oranda ölçeklendirmeyi belirten bir `number` (0'dan büyük) olarak ifade edilebilir. Her bileşenin ilgili eksendeki ölçeklendirmeyi belirttiği bir `vector3` de verebilirsiniz.

Örneğin:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Spawn with no rotation but double scale.
-- Set the score of the star to 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Yıldız oyun nesnesinin "score" özelliğini ayarlar.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. "score" betik özelliği varsayılan bir değerle tanımlanır.
2. "score" betik özelliğine, "self" içinde saklanan bir değer olarak başvurun.

![Özellik ve ölçeklendirme ile oluşturulan oyun nesnesi](images/factory/factory_spawned2.png)

::: sidenote
Defold şu anda çarpışma şekillerinin eksenlere göre farklı oranlarda ölçeklendirilmesini desteklemiyor. Örneğin `vmath.vector3(1.0, 2.0, 1.0)` gibi eksenlere göre farklı oranlar içeren bir ölçek değeri verirseniz sprite bileşeni doğru şekilde ölçeklenir ancak çarpışma şekilleri doğru şekilde ölçeklenmez.
:::


## Fabrikayla oluşturulan nesneleri adresleme

Defold'un adresleme mekanizması, çalışan bir oyundaki her nesneye ve bileşene erişmenizi sağlar. [Adresleme kılavuzu](/manuals/addressing/), sistemin nasıl çalıştığını oldukça ayrıntılı olarak açıklar. Aynı adresleme mekanizmasını çalışma sırasında oluşturulan oyun nesneleri ve bunların bileşenleri için de kullanabilirsiniz. Örneğin bir ileti gönderirken, oluşturulan nesnenin tanımlayıcısını kullanmak çoğu zaman yeterlidir:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
İletiyi belirli bir bileşen yerine oyun nesnesinin kendisine göndermek, aslında iletiyi tüm bileşenlere gönderir. Bu genellikle bir sorun oluşturmaz ancak nesnenin çok sayıda bileşeni varsa bunu aklınızda bulundurmanızda yarar vardır.
:::

Peki, örneğin bir çarpışma nesnesini devre dışı bırakmak veya sprite görüntüsünü değiştirmek için, çalışma sırasında oluşturulan bir oyun nesnesinin belirli bir bileşenine erişmeniz gerekirse? Çözüm, oyun nesnesinin tanımlayıcısı ile bileşenin tanımlayıcısından bir URL oluşturmaktır.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Oluşturulan nesneleri ve üst nesneleri takip etme

`factory.create()` işlevini çağırdığınızda yeni oyun nesnesinin tanımlayıcısı döndürülür; bu tanımlayıcıyı daha sonra başvurmak üzere saklayabilirsiniz. Yaygın bir kullanım, nesneler oluşturup tanımlayıcılarını bir tabloya eklemektir. Böylece, örneğin bir bölümün düzenini sıfırlarken, daha sonra hepsini silebilirsiniz:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Spawn a coin and store it in the "coins" table.
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

Daha sonra:

```lua
-- spawner.script
-- Delete all spawned coins.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- or alternatively
go.delete(self.spawned_coins)
```

Oluşturulan nesnenin, kendisini oluşturan oyun nesnesinden haberdar olmasını istemek de yaygındır. Örneğin, aynı anda yalnızca bir örneği oluşturulabilen bir otonom nesne türü söz konusu olabilir. Bu durumda oluşturulan nesnenin, yeni bir nesne oluşturulabilmesi için silindiğinde veya devre dışı bırakıldığında kendisini oluşturan nesneye haber vermesi gerekir:

```lua
-- spawner.script
-- Spawn a drone and set its parent to the url of this script component
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

Oluşturulan nesnenin mantığı ise şöyledir:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- I'm dead.
    msg.post(self.parent, "drone_dead")
end
```

## Fabrika kaynaklarını dinamik olarak yükleme {#dynamic-loading-of-factory-resources}

Fabrika özelliklerindeki *Load Dynamically* onay kutusunu işaretlediğinizde motor, fabrikayla ilişkili kaynakların yüklenmesini erteler.

![Dinamik yükleme](images/factory/load_dynamically.png)

Kutu işaretli değilken motor, fabrika bileşeni yüklendiğinde prototip kaynaklarını yükler; böylece bunlar nesne oluşturmak için hemen hazır olur.

Kutu işaretliyken iki kullanım seçeneğiniz vardır:

Eşzamanlı yükleme
: Nesneler oluşturmak istediğinizde [`factory.create()`](/ref/factory/#factory.create) işlevini çağırın. Bu işlem önce kaynakları eşzamanlı olarak yükler, ardından yeni örnekler oluşturur. Yükleme kısa bir takılmaya neden olabilir.

  ```lua
  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling create without having called
      -- load will create the resources synchronously.
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the factory component
      -- holds no reference.
      go.delete(self.go_id)

      -- Calling unload will do nothing since factory holds no references
      factory.unload("#factory")
  end
  ```

Eşzamansız yükleme
: Kaynakları açıkça eşzamansız olarak yüklemek için [`factory.load()`](/ref/factory/#factory.load) işlevini çağırın. Kaynaklar nesne oluşturmak için hazır olduğunda bir geri çağırım (callback) alınır.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_id = factory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling load will load the resources.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the factory component
      -- still holds a reference.
      go.delete(self.go_id)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      factory.unload("#factory")
  end
  ```

## Dinamik prototip

Fabrika özelliklerindeki *Dynamic Prototype* onay kutusunu işaretleyerek fabrikanın hangi *Prototype* değerini kullanarak nesne oluşturabileceğini değiştirebilirsiniz.

![Dinamik prototip](images/factory/dynamic_prototype.png)

*Dynamic Prototype* seçeneği işaretliyken fabrika bileşeni, `factory.set_prototype()` işlevini kullanarak prototipini değiştirebilir. Örnek:

```lua
factory.unload("#factory") -- unload the previous resources
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
*Dynamic Prototype* seçeneği etkinleştirildiğinde koleksiyonun (collection) bileşen sayısı optimize edilemez ve fabrika bileşenini içeren koleksiyon, *game.project* dosyasındaki varsayılan bileşen sayılarını kullanır.
:::


## Örnek sınırları

*Collection* altındaki *Max Instances* proje ayarı, her koleksiyondaki (dünyadaki) oyun nesnesi sayısının üst sınırıdır. Defold, proje derleme sırasında güvenli olduğunu belirleyebildiğinde daha küçük bir kapasite ayırabilir. Düzenleyicide yerleştirilmiş veya çalışma sırasında oluşturulmuş olsun, bir dünyada aynı anda var olan tüm oyun nesneleri kapasiteye dahil edilir.

![En fazla örnek sayısı](images/factory/factory_max_instances.png)

Gerçekte ayrılan kapasite, proje derleme sırasında yapılan analize bağlıdır:

* Proje derleme sırasında sabit bir oyun nesnesi sayısı belirlenebildiğinde kapasite, derlenmiş nesne sayısıdır ve *Max Instances* ile sınırlıdır. Bu genellikle koleksiyonda fabrika veya koleksiyon fabrikası (collection factory) bulunmadığında gerçekleşir.
* Fabrika veya koleksiyon fabrikası içeren bir koleksiyon, oyun nesnesi kapasitesi için *Max Instances* değerini kullanır. Statik olarak başvurulan bir prototip için, proje derleme işlemi fabrikanın oluşturabileceği bileşen türlerini belirler. Bu türler, projede kendileri için belirlenen en yüksek sayıları kullanırken etkilenmeyen bileşen türleri yine tam olarak belirlenen sayıları kullanabilir.
* *Dynamic Prototype* seçeneğini etkinleştirmek, fabrika bileşenini içeren koleksiyon için bileşen sayısı analizini devre dışı bırakır; bu nedenle koleksiyon, *Max Instances* değerini ve bileşen başına yapılandırılmış en yüksek sayıları kullanır.

*Max Instances* değerini, dinamik bir dünyada aynı anda var olabilecek en fazla oyun nesnesi sayısına göre planlayın. Diğer bileşen sınırlarının nasıl hesaplandığını öğrenmek için [Bileşen sayısı üst sınırı optimizasyonları](/manuals/project-settings/#component-max-count-optimizations) bölümüne bakın.

## Oyun nesnelerini havuzda tutma

Çalışma sırasında oluşturulan oyun nesnelerini bir havuzda saklayıp yeniden kullanmak iyi bir fikir gibi görünebilir. Ancak motor zaten kendi içinde nesne havuzlama işlemini yaptığı için ek işlem yükü yalnızca işleri yavaşlatır. Oyun nesnelerini silip yenilerini oluşturmak hem daha hızlı hem de daha temizdir.
