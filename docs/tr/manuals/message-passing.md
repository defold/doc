---
title: Defold'da ileti aktarımı
brief: İleti aktarımı, Defold'un gevşek bağlı nesnelerin iletişim kurmasını sağlamak için kullandığı mekanizmadır. Bu kılavuz, bu mekanizmayı ayrıntılı olarak açıklar.
---

# İleti aktarımı

İleti aktarımı (message passing), Defold oyun nesnelerinin (game object) birbirleriyle iletişim kurmasını sağlayan bir mekanizmadır. Bu kılavuz, Defold'un [adresleme mekanizması](/manuals/addressing) ve [temel yapı taşları](/manuals/building-blocks) hakkında temel bilgiye sahip olduğunuzu varsayar.

Defold'daki nesne yönelimi, uygulamanızı (Java, C++ veya C#'ta olduğu gibi) kalıtım içeren sınıf hiyerarşileri kurarak ve nesnelerinizde üye işlevler tanımlayarak oluşturmanız anlamına gelmez. Bunun yerine Defold, Lua'yı nesne durumunun betik bileşenlerinde (script component) tutulduğu ve `self` başvurusu üzerinden erişilebildiği basit ve güçlü bir nesne yönelimli tasarımla genişletir. Ayrıca nesneler arasında iletişim için eşzamansız ileti aktarımı kullanılarak nesneler birbirinden tamamen bağımsız tutulabilir.


## Kullanım örnekleri

Önce birkaç basit kullanım örneğine bakalım. Şu öğelerden oluşan bir oyun geliştirdiğinizi varsayalım:

1. GUI bileşeni (GUI component) içeren bir oyun nesnesini barındıran ana başlangıç koleksiyonu (bootstrap collection); GUI, bir mini harita ve bir puan sayacından oluşur. Ayrıca "level" tanımlayıcısına sahip bir koleksiyon (collection) vardır.
2. "level" adlı koleksiyon iki oyun nesnesi içerir: oyuncunun yönettiği bir kahraman karakter ve bir düşman.

![İleti aktarımı yapısı](images/message_passing/message_passing_structure.png)

::: sidenote
Bu örneğin içeriği iki ayrı dosyada bulunur. Ana başlangıç koleksiyonu için bir dosya, "level" tanımlayıcısına sahip koleksiyon için de bir dosya vardır. Ancak Defold'da dosya adları _önemli değildir_. Önemli olan, örneklere (instance) atadığınız kimliktir.
:::

Oyunda, nesneler arasında iletişim gerektiren birkaç basit mekanik vardır:

![İleti aktarımı](images/message_passing/message_passing.png)

① Kahraman düşmana yumruk atar
: Bu mekaniğin bir parçası olarak "hero" betik bileşeninden "enemy" betik bileşenine bir `"punch"` iletisi gönderilir. Her iki nesne de koleksiyon hiyerarşisinde aynı yerde bulunduğundan göreli adresleme tercih edilir:

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Oyunda yalnızca tek bir güç düzeyine sahip yumruk hareketi bulunduğundan, iletinin adı olan "punch" dışında herhangi bir bilgi içermesi gerekmez.

  Düşmanın betik bileşeninde, iletiyi almak için bir işlev oluşturursunuz:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  Bu durumda kod yalnızca iletinin adına bakar (ad, `message_id` parametresinde karma değeri alınmış bir dize olarak gönderilir). Kod, ileti verisiyle veya gönderenle ilgilenmez---"punch" iletisini gönderen *herkes* zavallı düşmana hasar verir.

② Kahramanın puan kazanması
: Oyuncu bir düşmanı her yendiğinde puanı artar. Ayrıca "hero" oyun nesnesinin betik bileşeninden "interface" oyun nesnesinin "gui" bileşenine bir `"update_score"` iletisi gönderilir.

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  Bu durumda göreli bir adres yazmak mümkün değildir; çünkü "interface" adlandırma hiyerarşisinin kökündeyken "hero" kökte değildir. İleti, kendisine bir betik eklenmiş olan GUI bileşenine gönderilir; böylece bileşen iletiye uygun şekilde tepki verebilir. Betikler, GUI betikleri ve işleme betikleri (render script) arasında serbestçe ileti gönderilebilir.

  `"update_score"` iletisi, puan verisiyle birlikte gönderilir. Veri, `message` parametresinde bir Lua tablosu olarak aktarılır:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Düşmanın mini haritadaki konumu
: Oyuncunun ekranında, düşmanların yerini bulmayı ve onları izlemeyi kolaylaştıran bir mini harita vardır. Her düşman, "interface" oyun nesnesindeki "gui" bileşenine bir `"update_minimap"` iletisi göndererek kendi konumunu bildirmekten sorumludur:

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  GUI betiğinin kodu her düşmanın konumunu izlemelidir; aynı düşman yeni bir konum gönderirse eski konum değiştirilmelidir. İletiyi gönderen (`sender` parametresinde aktarılır), konumları içeren bir Lua tablosunda anahtar olarak kullanılabilir:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- update position on map
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- update the minimap with new positions
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## İleti gönderme

Yukarıda gördüğümüz gibi, ileti gönderme mekanizması oldukça basittir. İletinizi ileti kuyruğuna ekleyen `msg.post()` işlevini çağırırsınız. Ardından motor, her karede kuyruğu tarar ve her iletiyi hedef adresine teslim eder. Bazı sistem iletilerini (`"enable"`, `"disable"`, `"set_parent"` vb.) motor kodu işler. Motor ayrıca nesnelerinize teslim edilen bazı sistem iletileri de üretir (fizik çarpışmalarında `"collision_response"` gibi). Betik bileşenlerine gönderilen kullanıcı tanımlı iletiler için motor yalnızca `on_message()` adlı özel bir Defold Lua işlevini çağırır.

Var olan herhangi bir nesneye veya bileşene istediğiniz iletileri gönderebilirsiniz; iletiye yanıt vermek alıcı taraftaki koda bağlıdır. Bir betik bileşenine ileti gönderirseniz ve betik kodu iletiyi yok sayarsa bu bir sorun oluşturmaz. İletileri işleme sorumluluğu tamamen alıcı taraftadır.

Motor, iletinin hedef adresini kontrol eder. Bilinmeyen bir alıcıya ileti göndermeye çalışırsanız Defold konsolda bir hata bildirir:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

`msg.post()` çağrısının tam imzası şöyledir:

`msg.post(receiver, message_id, [message])`

receiver
: Hedef bileşenin veya oyun nesnesinin tanımlayıcısı. Bir oyun nesnesini hedeflerseniz iletinin bu oyun nesnesindeki tüm bileşenlere gönderileceğini unutmayın.

message_id
: İletinin adını içeren bir dize veya karma değeri alınmış dize.

[message]
: İleti verisinin anahtar-değer çiftlerini içeren isteğe bağlı bir Lua tablosu. İletinin Lua tablosuna neredeyse her tür veri eklenebilir. Sayılar, dizeler, mantıksal değerler, URL değerleri, karma değerleri ve iç içe tablolar aktarabilirsiniz. İşlevleri aktaramazsınız.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
`message` parametresindeki tablonun boyutu için kesin bir sınır vardır. Bu sınır 2 kilobayt olarak belirlenmiştir. Bir tablonun bellekte kapladığı tam boyutu belirlemenin şu anda basit bir yolu yoktur; ancak bellek kullanımını izlemek için tabloyu eklemeden önce ve sonra `collectgarbage("count")` kullanabilirsiniz.
:::

### Kısa gösterimler

Defold, tam bir URL belirtmeden ileti göndermek için kullanabileceğiniz iki kullanışlı kısa gösterim sunar:

:[Shorthands](../shared/url-shorthands.md)


## İleti alma

İleti almak için hedef betik bileşeninin `on_message()` adlı bir işlev içerdiğinden emin olmanız yeterlidir. İşlev dört parametre kabul eder:

`function on_message(self, message_id, message, sender)`

`self`
: Betik bileşeninin kendisine bir başvuru.

`message_id`
: İletinin adını içerir. Adın _karma değeri alınmıştır_.

`message`
: İleti verisini içerir. Bu bir Lua tablosudur. Veri yoksa tablo boştur.

`sender`
: Gönderenin tam URL adresini içerir.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Oyun dünyaları arasında ileti aktarımı

Çalışma zamanı ortamına yeni bir oyun dünyası yüklemek için koleksiyon vekili (collection proxy) bileşeni kullanıyorsanız oyun dünyaları arasında ileti aktarmak isteyeceksiniz. Bir koleksiyonu vekil aracılığıyla yüklediğinizi ve koleksiyonun *Name* özelliğinin "level" olarak ayarlandığını varsayalım:

![Koleksiyon adı](images/message_passing/collection_name.png)

Koleksiyon yüklenip başlangıç işlemleri tamamlandıktan ve etkinleştirildikten hemen sonra, alıcı adresinin "socket" alanında oyun dünyasının adını belirterek yeni dünyadaki herhangi bir bileşene veya nesneye ileti gönderebilirsiniz:

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```
Vekillerin nasıl çalıştığına ilişkin daha ayrıntılı bir açıklamayı [Koleksiyon vekilleri](/manuals/collection-proxy) belgesinde bulabilirsiniz.

## İleti zincirleri

Gönderilmiş bir ileti sonunda dağıtıldığında alıcıların `on_message()` işlevi çağrılır. Tepki veren kodun, ileti kuyruğuna eklenen yeni iletiler göndermesi oldukça yaygındır.

Motor dağıtıma başladığında ileti kuyruğunu işler, her iletinin alıcısının `on_message()` işlevini çağırır ve ileti kuyruğu boşalana kadar devam eder. Dağıtım turu sırasında kuyruğa yeni iletiler eklenirse bir tur daha gerçekleştirir. Ancak motorun kuyruğu boşaltmayı kaç kez deneyeceğine ilişkin kesin bir sınır vardır; bu da bir kare içinde tamamen dağıtılmasını bekleyebileceğiniz ileti zincirlerinin uzunluğunu sınırlar. Motorun her `update()` çağrısı arasında kaç ileti dağıtım turu gerçekleştirdiğini aşağıdaki betikle kolayca test edebilirsiniz:

```lua
function init(self)
    -- We’re starting a long message chain during object init
    -- and keeps it running through a number of update() steps.
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

Bu betiği çalıştırmak aşağıdakine benzer bir çıktı verir:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Defold motorunun bu belirli sürümünün, `init()` ile ilk `update()` çağrısı arasında ileti kuyruğunda 10 ileti dağıtım turu gerçekleştirdiğini görüyoruz. Ardından sonraki her güncelleme döngüsünde 75 tur gerçekleştirir.
