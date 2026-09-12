---
title: Koleksiyon fabrikası kılavuzu
brief: Bu kılavuz, oyun nesnesi hiyerarşilerini çalışma sırasında oluşturmak için koleksiyon fabrikası bileşenlerinin nasıl kullanılacağını açıklar.
---

# Koleksiyon fabrikaları

Koleksiyon fabrikası (collection factory) bileşeni (component), koleksiyon (collection) dosyalarında saklanan oyun nesnesi (game object) gruplarını ve hiyerarşilerini çalışan bir oyunda oluşturmak için kullanılır.

Koleksiyonlar, Defold'da yeniden kullanılabilir şablonlar, diğer adıyla "prefab"lar oluşturmak için güçlü bir mekanizma sağlar. Koleksiyonlara genel bir bakış için [Yapı taşları belgelerine](/manuals/building-blocks#collections) bakın. Koleksiyonlar düzenleyicide yerleştirilebilir veya oyuna dinamik olarak eklenebilir.

Bir koleksiyon fabrikası bileşeniyle, koleksiyon dosyasının içeriğini bir oyun dünyasında çalışma sırasında oluşturabilirsiniz. Bu, koleksiyondaki tüm oyun nesnelerini fabrika (factory) aracılığıyla oluşturup ardından nesneler arasında üst-alt nesne hiyerarşisini kurmaya benzer. Tipik bir kullanım örneği, birden çok oyun nesnesinden oluşan düşmanlar oluşturmaktır (örneğin düşman + silah).

## Çalışma sırasında koleksiyon oluşturma {#spawning-a-collection}

Bir karakter oyun nesnesi ve karaktere alt nesne olarak bağlı ayrı bir kalkan oyun nesnesi istediğimizi varsayalım. Oyun nesnesi hiyerarşisini bir koleksiyon dosyasında oluşturup `bean.collection` olarak kaydediyoruz.

::: sidenote
*Koleksiyon vekili* (collection proxy) bileşeni, bir koleksiyona dayanarak ayrı bir fizik dünyası da içeren yeni bir oyun dünyası oluşturmak için kullanılır. Yeni dünyaya yeni bir soket üzerinden erişilir. Yüklemeyi başlatması için vekile ileti gönderdiğinizde, koleksiyondaki tüm varlıklar vekil aracılığıyla yüklenir. Bu, koleksiyon vekillerini örneğin bir oyunda bölüm değiştirmek için çok kullanışlı kılar. Ancak yeni oyun dünyaları oldukça fazla ek yük getirir; bu nedenle onları küçük öğeleri dinamik olarak yüklemek için kullanmayın. Daha fazla bilgi için [Koleksiyon vekili belgelerine](/manuals/collection-proxy) bakın.
:::

![Çalışma sırasında oluşturulacak koleksiyon](images/collection_factory/collection.png)

Ardından, oluşturma işlemini üstlenecek bir oyun nesnesine *Collection factory* ekliyor ve `bean.collection` dosyasını bileşenin *Prototype* değeri olarak ayarlıyoruz:

![Koleksiyon fabrikası](images/collection_factory/factory.png)

Artık bir `bean` ve kalkan oluşturmak için `collectionfactory.create()` işlevini çağırmak yeterlidir:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

İşlev 5 parametre alır:

`url`
: Yeni oyun nesnesi kümesini oluşturacak koleksiyon fabrikası bileşeninin tanımlayıcısı.

`[position]`
: (isteğe bağlı) Oluşturulan oyun nesnelerinin dünya konumu. Bu değer bir `vector3` olmalıdır. Bir konum belirtmezseniz nesneler koleksiyon fabrikası bileşeninin konumunda oluşturulur.

`[rotation]`
: (isteğe bağlı) Yeni oyun nesnelerinin dünya uzayındaki dönmesi. Bu değer bir `quat` olmalıdır.

`[properties]`
: (isteğe bağlı) Oluşturulan oyun nesnelerinin başlangıç işlemlerinde kullanılan `id`-`table` çiftlerini içeren bir Lua tablosu. Bu tablonun nasıl oluşturulacağını aşağıda bulabilirsiniz.

`[scale]`
: (isteğe bağlı) Oluşturulan oyun nesnelerinin ölçeği. Ölçek, tüm eksenler boyunca aynı oranda ölçekleme belirten bir `number` (0'dan büyük) olarak ifade edilebilir. Her bileşeni ilgili eksendeki ölçeklemeyi belirten bir `vector3` de verebilirsiniz.

`collectionfactory.create()`, oluşturulan oyun nesnelerinin tanımlayıcılarını bir tablo olarak döndürür. Tablo anahtarları, her nesnenin koleksiyon içindeki yerel tanımlayıcısının karma değerini, o nesnenin çalışma zamanı tanımlayıcısıyla eşler:

::: sidenote
`bean` ile `shield` arasındaki üst-alt nesne ilişkisi, döndürülen tabloya *yansıtılmaz*. Bu ilişki yalnızca çalışma zamanı sahne grafında, yani nesnelerin birlikte dönüştürülme biçiminde bulunur. Bir nesnenin üst nesnesini değiştirmek, tanımlayıcısını hiçbir zaman değiştirmez.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. Her örneği benzersiz biçimde tanımlamak için tanımlayıcıya `/collection[N]/` öneki eklenir; burada `[N]` bir sayaçtır:

## Özellikler

Çalışma sırasında bir koleksiyon oluştururken, anahtarları nesne tanımlayıcıları ve değerleri ayarlanacak betik özelliklerini içeren tablolar olan bir tablo oluşturarak her oyun nesnesine özellik parametreleri geçirebilirsiniz.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

`bean` oyun nesnesinin `bean.collection` içinde `shield` özelliğini tanımladığını varsayalım. [Betik özelliği kılavuzu](/manuals/script-properties), betik özellikleri hakkında bilgi içerir.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Fabrika kaynaklarının dinamik olarak yüklenmesi {#dynamic-loading-of-factory-resources}

Koleksiyon fabrikasının özelliklerindeki *Load Dynamically* onay kutusunu işaretlediğinizde motor, fabrikayla ilişkili kaynakların yüklenmesini erteler.

![Dinamik olarak yükleme](images/collection_factory/load_dynamically.png)

Kutu işaretli değilse motor, koleksiyon fabrikası bileşeni yüklendiğinde prototip kaynaklarını yükler; böylece kaynaklar nesne oluşturmak için hemen hazır olur.

Kutu işaretliyse iki kullanım seçeneğiniz vardır:

Eşzamanlı yükleme
: Nesne oluşturmak istediğinizde [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) işlevini çağırın. Bu işlem önce kaynakları eşzamanlı olarak yükler; bu, kısa bir takılmaya neden olabilir. Ardından yeni örnekler oluşturur.

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

Eşzamansız yükleme
: Kaynakları açıkça eşzamansız olarak yüklemek için [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) işlevini çağırın. Kaynaklar nesne oluşturmak için hazır olduğunda bir geri çağırım alınır.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## Dinamik prototip

Bir koleksiyon fabrikasının oluşturabileceği *Prototype* değerini, koleksiyon fabrikasının özelliklerindeki *Dynamic Prototype* onay kutusunu işaretleyerek değiştirebilirsiniz.

![Dinamik prototip](images/collection_factory/dynamic_prototype.png)

*Dynamic Prototype* seçeneği işaretliyken koleksiyon fabrikası bileşeni, `collectionfactory.set_prototype()` işlevini kullanarak prototipi değiştirebilir. Örnek:

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
*Dynamic Prototype* seçeneği etkinleştirildiğinde koleksiyonun bileşen sayısı optimize edilemez ve bileşenin bulunduğu koleksiyon, *game.project* dosyasındaki varsayılan bileşen sayılarını kullanır.
:::
