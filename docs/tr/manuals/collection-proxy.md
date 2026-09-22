---
title: Koleksiyon vekili kılavuzu
brief: Bu kılavuz, yeni oyun dünyalarını dinamik olarak oluşturmayı ve aralarında geçiş yapmayı açıklar.
---

# Koleksiyon vekili

Koleksiyon vekili (collection proxy) bileşeni (component), bir koleksiyon (collection) dosyasının içeriğine göre yeni oyun "dünyalarını" dinamik olarak yüklemek ve bellekten kaldırmak için kullanılır. Koleksiyon vekilleri; oyun seviyeleri ve GUI ekranları arasında geçiş yapmak, bir seviye boyunca hikâye "sahnelerini" yükleyip bellekten kaldırmak, mini oyunları yükleyip bellekten kaldırmak ve daha fazlası için kullanılabilir.

Defold, tüm oyun nesnelerini (game object) koleksiyonlar halinde düzenler. Bir koleksiyon, oyun nesneleri ve başka koleksiyonlar (yani alt koleksiyonlar) içerebilir. Koleksiyon vekilleri, içeriğinizi ayrı koleksiyonlara bölmenizi ve ardından bu koleksiyonların yüklenmesini ve bellekten kaldırılmasını betikler aracılığıyla dinamik olarak yönetmenizi sağlar.

Koleksiyon vekilleri, [koleksiyon fabrikası (collection factory) bileşenlerinden](/manuals/collection-factory/) farklıdır. Bir koleksiyon fabrikası, koleksiyon içeriğinin örneklerini geçerli oyun dünyasında oluşturur. Koleksiyon vekilleri ise çalışma sırasında yeni bir oyun dünyası oluşturur ve bu nedenle farklı kullanım alanlarına sahiptir.

## Koleksiyon vekili bileşeni oluşturma

1. Bir oyun nesnesine <kbd>sağ tıklayın</kbd> ve bağlam menüsünden <kbd>Add Component ▸ Collection Proxy</kbd> seçeneğini seçerek oyun nesnesine bir koleksiyon vekili bileşeni ekleyin.

2. *Collection* özelliğini, daha sonra çalışma zamanı ortamına dinamik olarak yüklemek istediğiniz bir koleksiyona başvuracak şekilde ayarlayın. Bu, proje derleme sırasında belirlenen statik bir bağımlılıktır: başvurulan koleksiyon ve bağımlılıkları derlenir. *Exclude* işaretli olmadığı sürece ana dağıtım paketine dahil edilirler. *Exclude* işaretliyse yalnızca hariç tutulan vekiller üzerinden başvurulan kaynaklar Live Update için ana dağıtım paketinin dışında bırakılabilir ve yüklenmemiş vekil, aşağıda anlatıldığı gibi çalışma sırasında başka bir derlenmiş koleksiyona yönlendirilebilir.

![Vekil bileşeni ekleme](images/collection-proxy/create_proxy.png)

(İçeriği derleme çıktısından hariç tutup bunun yerine kodla indirmek için *Exclude* kutusunu işaretleyebilir ve [Live Update özelliğini](/manuals/live-update/) kullanabilirsiniz.)

## Başlangıç

Defold motoru başlatıldığında, bir *başlangıç koleksiyonundan (bootstrap collection)* tüm oyun nesnelerini çalışma zamanı ortamına yükler ve örneklerini oluşturur. Ardından oyun nesnelerinin ve bileşenlerinin başlangıç işlemlerini gerçekleştirip onları etkinleştirir. Motorun hangi başlangıç koleksiyonunu kullanacağı [proje ayarlarında](/manuals/project-settings/#main-collection) belirlenir. Bu koleksiyon dosyasına genellikle `main.collection` adı verilir.

![Başlangıç](images/collection-proxy/bootstrap.png)

Motor, oyun nesnelerini ve bileşenlerini barındırmak için başlangıç koleksiyonunun içeriğinden örneklerin oluşturulacağı "oyun dünyasının" tamamına gereken belleği ayırır. Çarpışma nesneleri ve fizik simülasyonu için ayrı bir fizik dünyası da oluşturulur.

Betik bileşenlerinin, başlangıç dünyasının dışından bile oyundaki tüm nesneleri adresleyebilmesi gerektiğinden bu dünyaya benzersiz bir ad verilir. Bu ad, koleksiyon dosyasında ayarladığınız *Name* özelliğidir:

![Başlangıç](images/collection-proxy/collection_id.png)

Yüklenen koleksiyon koleksiyon vekili bileşenleri içeriyorsa bu bileşenlerin başvurduğu koleksiyonlar otomatik olarak *yüklenmez*. Bu kaynakların yüklenmesini betikler aracılığıyla yönetmeniz gerekir.

## Koleksiyon yükleme

Bir koleksiyonu vekil aracılığıyla dinamik olarak yüklemek için bir betikten vekil bileşenine `"load"` adlı ileti gönderilir:

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![Yükleme](images/collection-proxy/proxy_load.png)

Vekil bileşeni, motora yeni bir dünya için yer ayırmasını söyler. Çalışma zamanı ortamında ayrı bir fizik dünyası da oluşturulur ve "`mylevel.collection`" koleksiyonundaki tüm oyun nesnelerinin örnekleri oluşturulur.

Yeni dünya, adını koleksiyon dosyasındaki *Name* özelliğinden alır; bu örnekte özellik "`mylevel`" olarak ayarlanmıştır. Adın benzersiz olması gerekir. Koleksiyon dosyasında ayarlanan *Name* değeri yüklenmiş bir dünya için zaten kullanılıyorsa motor bir ad çakışması hatası bildirir:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Motor koleksiyonu yüklemeyi tamamladığında koleksiyon vekili bileşeni, `"load"` iletisini gönderen betiğe `"proxy_loaded"` adlı bir ileti gönderir. Betik daha sonra bu iletiye yanıt olarak koleksiyonun başlangıç işlemlerini gerçekleştirip koleksiyonu etkinleştirebilir:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Bu ileti, koleksiyon vekili bileşenine koleksiyonunu yeni bir dünyaya yüklemeye başlamasını söyler. Vekil, işini tamamladığında `"proxy_loaded"` adlı bir ileti gönderir.

`"async_load"`
: Bu ileti, koleksiyon vekili bileşenine koleksiyonunu arka planda yeni bir dünyaya yüklemeye başlamasını söyler. Vekil, işini tamamladığında `"proxy_loaded"` adlı bir ileti gönderir.

`"init"`
: Bu ileti, koleksiyon vekili bileşenine, örnekleri oluşturulan tüm oyun nesnelerinin ve bileşenlerin başlangıç işlemlerinin gerçekleştirilmesi gerektiğini söyler. Bu aşamada tüm betiklerin `init()` işlevleri çağrılır.

`"enable"`
: Bu ileti, koleksiyon vekili bileşenine tüm oyun nesnelerinin ve bileşenlerin etkinleştirilmesi gerektiğini söyler. Örneğin, tüm sprite bileşenleri etkinleştirildiklerinde çizilmeye başlar.

## Hariç tutulan bir vekilin koleksiyonunu değiştirme {#changing-an-excluded-proxys-collection}

[`collectionproxy.set_collection()`](/ref/collectionproxy/#collectionproxy.set_collection) işlevi, hariç tutulmuş ve yüklenmemiş bir vekili derlenmiş bir koleksiyona yönlendirebilir. Bu, bir Live Update paketi bağlandıktan sonra yararlıdır. Vekilin *Exclude* seçeneği işaretli olmalı ve vekil yüklenmiş veya yükleniyor durumda olmamalıdır. Yol, `.collectionc` ile bitmelidir. Vekil yüklendiğinde koleksiyon ve tüm bağımlılıkları kaynak sistemi tarafından erişilebilir durumda olmalıdır.

Vekili yüklemeden önce dönüş değerini kontrol edin. Yeni dünyanın başlangıç işlemlerini yalnızca `proxy_loaded` iletisini aldıktan sonra gerçekleştirip dünyayı etkinleştirin:

```lua
local function load_mounted_level()
    local ok, result = collectionproxy.set_collection(
        "#level_proxy",
        "/level_pack/level_3.collectionc"
    )

    if ok then
        msg.post("#level_proxy", "load")
    else
        print("Unable to change proxy collection", result)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

Düzenleyicide atanan koleksiyona dönmek için vekil yüklenmiş veya yükleniyor durumda değilken `collectionproxy.set_collection("#level_proxy", nil)` işlevini çağırın. İçerik indirme ve bağlama işlemleri için [Live Update betik yazımı kılavuzuna](/manuals/live-update-scripting/), `collectionproxy.RESULT_*` hata kodları için API başvurusuna bakın.

## Yeni dünyadaki nesneleri adresleme

Koleksiyon dosyası özelliklerinde ayarlanan *Name* değeri, yüklenen dünyadaki oyun nesnelerini ve bileşenlerini adreslemek için kullanılır. Örneğin, başlangıç koleksiyonunda bir yükleyici nesnesi oluşturursanız yüklenmiş herhangi bir koleksiyondan bu nesneyle iletişim kurmanız gerekebilir:

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![Yükleme](images/collection-proxy/message_passing.png)

Yükleyiciden, yüklenen koleksiyondaki bir oyun nesnesiyle iletişim kurmanız gerekirse [nesnenin tam URL adresini](/manuals/addressing/#urls) kullanarak bir ileti gönderebilirsiniz:

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
Yüklenmiş bir koleksiyondaki oyun nesnelerine koleksiyonun dışından doğrudan erişmek mümkün değildir:

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Bir dünyayı bellekten kaldırma

Yüklenmiş bir koleksiyonu bellekten kaldırmak için yükleme adımlarının tersine karşılık gelen iletileri gönderirsiniz:

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Bu ileti, koleksiyon vekili bileşenine dünyadaki tüm oyun nesnelerini ve bileşenlerini devre dışı bırakmasını söyler. Bu aşamada sprite bileşenleri için görüntü oluşturma, yani işleme (rendering), durur.

`"final"`
: Bu ileti, koleksiyon vekili bileşenine dünyadaki tüm oyun nesnelerinin ve bileşenlerinin sonlandırma işlemlerini gerçekleştirmesini söyler. Bu aşamada tüm betiklerin `final()` işlevleri çağrılır.

`"unload"`
: Bu ileti, koleksiyon vekiline dünyayı bellekten tamamen kaldırmasını söyler.

Daha ayrıntılı denetime ihtiyacınız yoksa koleksiyonu önce devre dışı bırakıp sonlandırma işlemlerini gerçekleştirmeden doğrudan `"unload"` iletisini gönderebilirsiniz. Bu durumda vekil, koleksiyonu bellekten kaldırmadan önce otomatik olarak devre dışı bırakır ve sonlandırma işlemlerini gerçekleştirir.

Koleksiyon vekili, koleksiyonu bellekten kaldırmayı tamamladığında `"unload"` iletisini gönderen betiğe `"proxy_unloaded"` iletisini gönderir:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## Zaman adımı

Koleksiyon vekilinin güncellemeleri, _zaman adımı (time step)_ değiştirilerek ölçeklenebilir. Bu, oyun sabit 60 FPS hızında çalışsa bile bir vekilin daha yüksek veya daha düşük bir hızda güncellenebileceği ve şu gibi unsurları etkileyebileceği anlamına gelir:

* Fizik simülasyonu hızı
* `update()` işlevine geçirilen `dt` değeri
* [Oyun nesnesi ve GUI özellik animasyonları](https://defold.com/manuals/animation/#property-animation-1)
* [Kare dizisi animasyonları](https://defold.com/manuals/animation/#flip-book-animation)
* [Parçacık efekti simülasyonları](https://defold.com/manuals/particlefx/)
* Zamanlayıcı hızı

Güncelleme modunu da ayarlayabilirsiniz. Böylece ölçeklemenin kesikli olarak mı (yalnızca ölçek çarpanı 1,0'dan küçükse anlamlıdır) yoksa sürekli olarak mı yapılacağını denetleyebilirsiniz.

Ölçek çarpanını ve ölçekleme modunu, vekile bir `set_time_step` iletisi göndererek denetlersiniz:

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Zaman adımını değiştirirken neler olduğunu görmek için betik bileşeninde aşağıdaki kodu içeren bir nesne oluşturup zaman adımını değiştirdiğimiz koleksiyona yerleştirebiliriz:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Zaman adımı 0,2 olduğunda konsolda şu sonucu alırız:

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` hâlâ saniyede 60 kez çağrılır, ancak `dt` değeri değişir. `update()` çağrılarının yalnızca 1/5'inde (0,2) `dt` değerinin 1/60 (60 FPS'ye karşılık gelir) olduğunu görürüz---geri kalanında bu değer sıfırdır. Tüm fizik simülasyonları da bu `dt` değerine göre güncellenir ve karelerin yalnızca beşte birinde ilerler.

::: sidenote
Koleksiyonun zaman adımı işlevini, örneğin bir açılır pencere gösterilirken veya pencere odağını kaybettiğinde oyununuzu duraklatmak için kullanabilirsiniz. Duraklatmak için `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})`, devam ettirmek için `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` kullanın.
:::

Daha fazla ayrıntı için [`set_time_step`](/ref/collectionproxy#set_time_step) başvurusuna bakın.

## Dikkat edilmesi gerekenler ve yaygın sorunlar

Fizik
: Koleksiyon vekilleri aracılığıyla motora birden fazla en üst düzey koleksiyon, yani *oyun dünyası*, yüklemek mümkündür. Bunu yaparken her en üst düzey koleksiyonun ayrı bir fizik dünyası olduğunu bilmek önemlidir. Fizik etkileşimleri (çarpışmalar, tetikleyiciler, ışın sorguları) yalnızca aynı dünyaya ait nesneler arasında gerçekleşir. Bu nedenle iki dünyadaki çarpışma nesneleri görsel olarak tam üst üste gelseler bile aralarında herhangi bir fizik etkileşimi olamaz.

Bellek
: Yüklenen her koleksiyon, görece büyük miktarda bellek kullanan yeni bir oyun dünyası oluşturur. Vekiller aracılığıyla aynı anda onlarca koleksiyon yüklüyorsanız tasarımınızı yeniden değerlendirmek isteyebilirsiniz. Oyun nesnesi hiyerarşilerinin çok sayıda örneğini çalışma sırasında oluşturmak için [koleksiyon fabrikaları](/manuals/collection-factory) daha uygundur.

Girdi
: Yüklenen koleksiyonunuzda girdi eylemlerine ihtiyaç duyan nesneler varsa koleksiyon vekilini içeren oyun nesnesinin girdiyi aldığından emin olmanız gerekir. Oyun nesnesi girdi iletileri aldığında bunlar nesnenin bileşenlerine, yani koleksiyon vekillerine aktarılır. Girdi eylemleri vekil aracılığıyla yüklenen koleksiyona gönderilir.
