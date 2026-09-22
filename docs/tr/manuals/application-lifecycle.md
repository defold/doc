---
title: Defold uygulama yaşam döngüsü kılavuzu
brief: Bu kılavuz, Defold oyunlarının ve uygulamalarının yaşam döngüsünü ayrıntılarıyla açıklar.
---

# Uygulama yaşam döngüsü

Bir Defold uygulamasının veya oyununun yaşam döngüsü (lifecycle), genel hatlarıyla basittir. Motor üç yürütme aşamasından geçer: başlangıç işlemleri (initialization), uygulamaların ve oyunların zamanlarının çoğunu geçirdiği güncelleme döngüsü (update loop) ve sonlandırma işlemleri (finalization).

::: sidenote
Bu kılavuz, Defold'un 1.12.0 ve sonraki sürümlerini kapsar. 1.12.0 sürümünde yaşam döngüsüyle ilgili değişiklikler yapılmış ve yeni `late_update()` işlevi eklenmiştir.
:::

![Yaşam döngüsüne genel bakış](images/application_lifecycle/application_lifecycle.png)

Çoğu durumda Defold'un iç işleyişini temel düzeyde anlamak yeterlidir. Ancak Defold'un görevlerini tam olarak hangi sırayla yürüttüğünün kritik önem taşıdığı uç durumlarla karşılaşabilirsiniz. Bu belge, motorun bir uygulamayı baştan sona nasıl çalıştırdığını açıklar.

Uygulama, motorun çalışması için gereken her şeyin başlangıç işlemlerini yaparak başlar. Ana koleksiyonu (main collection) yükler ve `init()` Lua işlevi bulunan, yüklenmiş tüm bileşenlerin (component) [`init()`](/ref/go#init) işlevini çağırır. Bunlar betik bileşenleri ve GUI betiği içeren GUI bileşenleridir. Böylece kendi başlangıç işlemlerinizi yapabilirsiniz.

Uygulama daha sonra yaşam süresinin büyük bölümünü geçireceği güncelleme döngüsüne girer. Her karede oyun nesneleri (game object) ve içerdikleri bileşenler güncellenir. Betiklerde ve GUI betiklerinde bulunan [`update()`](/ref/go#update) işlevleri çağrılır. Güncelleme döngüsü sırasında iletiler alıcılarına dağıtılır, sesler çalınır ve tüm grafikler, görüntü oluşturmak üzere işlenir (rendering).

Bir noktada uygulamanın yaşam döngüsü sona erer. Uygulama kapanmadan önce motor güncelleme döngüsünden çıkar ve sonlandırma aşamasına girer. Yüklenmiş tüm oyun nesnelerini silinmek üzere hazırlar. Nesnelerin tüm bileşenlerinin [`final()`](/ref/go#final) işlevleri çağrılır; böylece kendi temizleme işlemlerinizi yapabilirsiniz. Ardından nesneler silinir ve ana koleksiyon bellekten kaldırılır.

["İletileri dağıtma"](#dispatching-messages) geçişindeki adımlar, daha anlaşılır olması için bu kılavuzun sonunda ayrı bir şemada gösterilir ve şemalarda küçük bir "oklu zarf" simgesi 📩 ile işaretlenir.

## Başlangıç işlemleri

Oyununuz burada başlar; bu, çalışan oyunun ilk adımıdır. 3 aşamaya ayrılabilir:

![Başlangıç işlemleri](images/application_lifecycle/initialization.png)

### Ön başlatma

Ön başlatma (`Preinitialization`) aşamasında motor, ana koleksiyon (başlangıç koleksiyonu, bootstrap collection) yüklenmeden önce birçok adım gerçekleştirir. Bellek profil çıkarıcısı, soketler, grafikler, HID (girdi aygıtları), ses, fizik ve daha pek çok şey hazırlanır. Uygulama yapılandırması (*game.project*) da yüklenir ve hazırlanır.

![Ön başlatma](images/application_lifecycle/pre_init.png)

Kullanıcının denetleyebildiği ilk giriş noktası, motorun başlangıç işlemlerinin sonunda geçerli işleme betiğinin `init()` işlevinin çağrılmasıdır.

Ardından ana koleksiyon yüklenir ve başlangıç işlemleri yapılır.

### Koleksiyonun başlangıç işlemleri

`Collection Init` aşamasında, koleksiyondaki tüm oyun nesneleri dönüşümlerini, yani öteleme (konum değişikliği), dönme ve ölçeklemeyi alt nesnelerine uygular. Ardından tüm bileşenlerin mevcut `init()` işlevleri çağrılır.

![Koleksiyonun başlangıç işlemleri](images/application_lifecycle/collection_init.png)

::: sidenote
Oyun nesnesi bileşenlerinin `init()` işlevlerinin çağrılma sırası tanımlanmamıştır. Motorun aynı koleksiyona ait nesnelerin başlangıç işlemlerini belirli bir sırayla yaptığını varsaymayın.
:::

### Başlangıç işlemlerinde güncelleme sonrası aşama

Motor daha sonra tam bir `Post Update` geçişi gerçekleştirir; bu, ilerleyen süreçte her `Update Loop` adımından sonra gerçekleştirilen geçişin aynısıdır. Bu geçiş başlangıç işlemlerinin sonunda gerçekleştirilir çünkü `init()` kodunuz yeni iletiler gönderebilir, fabrikalara (factory) yeni nesneler oluşturmalarını söyleyebilir, nesneleri silinmek üzere işaretleyebilir ve başka eylemler gerçekleştirebilir.

![Güncelleme sonrası aşama](images/application_lifecycle/post_init.png)

Bu geçiş, ileti teslimini, fabrikaların oyun nesnelerini fiilen oluşturmasını ve nesnelerin silinmesini gerçekleştirir. `Post Update` geçişinin, kuyruktaki iletileri teslim etmenin yanı sıra koleksiyon vekillerine (collection proxy) gönderilen iletileri de işleyen bir "iletileri dağıtma" adım dizisi içerdiğine dikkat edin. Bunun sonucunda gereken vekil güncellemeleri (etkinleştirme, devre dışı bırakma, başlangıç işlemleri, sonlandırma işlemleri, yükleme ve bellekten kaldırılmak üzere işaretleme) bu adımlar sırasında gerçekleştirilir.

`init()` sırasında bir [koleksiyon vekili](/manuals/collection-proxy) yüklemek, içerdiği tüm nesnelerin başlangıç işlemlerinin yapıldığından emin olmak ve ardından koleksiyonu vekil aracılığıyla bellekten kaldırmak mümkündür. Bunların tümü ilk bileşenin `update()` işlevi çağrılmadan, yani motor başlangıç işlemleri aşamasından çıkıp güncelleme döngüsüne girmeden önce gerçekleşebilir:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## Güncelleme döngüsü

`Update Loop`, her karede bir kez belirli bir adım dizisini yürütür. Bu dizi 5 ana aşamayla tanımlanabilir:

![Güncelleme döngüsü](images/application_lifecycle/update_loop.png)

1. Girdi (işleme ve ele alma)
2. Güncelleme (sabit zaman adımlı, normal, geç güncellemeler ve motor bileşenlerinin güncellemeleri dahil)
3. İşleme güncellemesi
4. Güncelleme sonrası aşama (koleksiyon vekillerini bellekten kaldırma, oyun nesnelerini oluşturma ve silme)
5. Kare işleme (son grafik görüntüsü oluşturulur)

### Girdi aşaması

Girdi, kullanılabilir aygıtlardan okunur, [girdi eşlemelerine (input binding)](/manuals/input) göre eşlenir ve ardından dağıtılır. Girdi odağını edinmiş her oyun nesnesinin tüm bileşenlerinin `on_input()` işlevlerine girdi gönderilir. Bir betik bileşeni ve GUI betiği içeren bir GUI bileşeni bulunan oyun nesnesinde, her iki bileşenin de `on_input()` işlevlerine girdi iletilir; bunun için bu işlevlerin tanımlanmış olması ve bileşenlerin girdi odağını edinmiş olması gerekir.

![Girdi aşaması](images/application_lifecycle/input_phase.png)

Girdi odağını edinmiş ve koleksiyon vekili bileşenleri içeren her oyun nesnesi, girdiyi vekil koleksiyonunun içindeki bileşenlere dağıtır. Bu işlem, etkin koleksiyon vekillerinin içindeki etkin koleksiyon vekilleri boyunca özyinelemeli olarak devam eder.

### Güncelleme aşaması

`Update` aşaması, `Update Loop` döngüsünün bir parçasıdır. Kök koleksiyon için bir kez başlatılır, ardından etkin her koleksiyon vekili için özyinelemeli olarak çalışır.

Defold, bir koleksiyon içinde geri çağırımları (callback) bileşen türüne göre işler: ilgili aşamayı uygulayan bir bileşen türünün tüm örneklerini dolaşır, her örnek için Lua geri çağırımını çağırır, bekleyen iletileri dağıtır ve ardından sıradaki bileşen türüne geçer.

*Betik* bileşenlerinin Lua geri çağırım aşamalarının genel sırası şöyledir:

1. `fixed_update()` - kare başına 0..N kez çağrılır (sabit zaman adımı kullanılıyorsa)
2. `update()` - kare başına 1 kez çağrılır
3. `late_update()` - kare başına 1 kez çağrılır

![Güncelleme aşaması](images/application_lifecycle/update_phase.png)


Ana koleksiyondaki her oyun nesnesi bileşeni dolaşılır. Bu bileşenlerden herhangi birinin betiğinde `fixed_update()`/`update()`/`late_update()` işlevi varsa bu işlev çağrılır. Bileşen bir koleksiyon vekiliyse vekil koleksiyonundaki her bileşen, `Update` aşamasındaki tüm adımlarla özyinelemeli olarak güncellenir.

::: sidenote
Oyun nesnesi bileşenlerinin `update()` işlevlerinin çağrılma sırası tanımlanmamıştır. Motorun aynı koleksiyona ait nesneleri belirli bir sırayla güncellediğini varsaymayın. Aynı durum `fixed_update()` ve `late_update()` için de geçerlidir (1.12.0 sürümünden itibaren).
:::

#### Fizik

Çarpışma nesnesi bileşenleri için fizik iletileri (çarpışmalar, tetikleyiciler, ışın sorgusu yanıtları vb.), bu bileşenleri barındıran oyun nesnesinde `on_message()` işlevi olan bir betik içeren tüm bileşenlere dağıtılır.

Fizik benzetimi için [sabit zaman adımı](/manuals/physics/#physics-updates) kullanılıyorsa tüm betik bileşenlerinin `fixed_update()` işlevi de çağrılabilir. Bu işlev, fizik tabanlı oyunlarda kararlı bir fizik benzetimi elde etmek için fizik nesnelerini düzenli aralıklarla değiştirmek istediğinizde yararlıdır.

#### Dönüşümler

**Her** bileşen türünün güncellemesinden önce, `Update Loop` sırasında birden çok kez, gerekirse dönüşümler güncellenir. Böylece oyun nesnelerinin tüm hareket, dönme ve ölçekleme değişiklikleri her oyun nesnesi bileşenine ve tüm alt oyun nesnelerinin bileşenlerine uygulanır.

`Update Loop` sonunda, gerekirse ek bir son dönüşüm güncellemesi yapılır.

#### Motorun güncelleme aşaması (sabit zaman adımlı güncellemeler olmadan)

Aşağıdaki tablolar *motor düzeyindeki* güncelleme geçişlerini açıklar. Bileşenlerin motor içindeki kesin öncelik sırasına (motorun uygulama ayrıntılarından biridir) bilinçli olarak yer vermezler; ancak betik yazımı açısından önemli olan sıralama güvencelerini yansıtırlar:

- `fixed_update()`, `update()` işlevinden önce çalışır
- `late_update()`, `update()` işlevinden sonra çalışır
- gönderilen iletiler, bileşen türlerinin güncellemeleri arasında ve betik geri çağırım aşamaları arasında dağıtılır

`Use Fixed Timestep` değeri `false` olduğunda ve/veya Fixed Update Frequency değeri `0` olduğunda, aşamanın başında `dt` hazırlanır ve ardından akış aşağıdaki tabloda gösterildiği gibi ilerler:

:::sidenote
**Her** bileşen türünün güncellemesinden sonra tüm iletilerin dağıtıldığına dikkat edin; tabloyu sade tutmak için bu işlem aşağıdaki tabloda işaretlenmemiştir.
:::

| Adım | Motor aşaması | Lua geri çağırımı | Açıklama |
|-|-|-|-|
| 1 | **Güncelleme** | `update()` | Güncelleme aşamasını uygulayan her bileşen türü için motorun iç öncelik sırasıyla kare başına bir kez çağrılır. Ayrıca `go.animate()` ile başlatılan oyun nesnesi özelliği animasyonları burada ayrı bir bileşen türü olarak güncellenir. **Fizik** bileşenleri burada güncellenir. Etkin her koleksiyon vekili için tüm `Update` aşaması 1. adımdan başlayarak özyinelemeli olarak çağrılır. |
| 2 | **Geç güncelleme** | `late_update()` | Geç güncelleme aşamasını uygulayan her bileşen türü için motorun iç öncelik sırasıyla kare başına bir kez çağrılır. |
| 3 | **Dönüşümler** | | Sonda her bileşen için, gerekirse ek bir son dönüşüm güncellemesi gerçekleştirilir. |

#### Sabit zaman adımıyla motorun güncelleme aşaması

`Use Fixed Timestep` değeri `true` ve Fixed Update Frequency değeri sıfırdan farklı olduğunda, aşamanın başında `dt` (geçen süre), `fixed_dt` ve `num_fixed_steps` (`0..N`) hazırlanır. Sonuncusu, sabit sayıda güncelleme yapılmasını sağlamak için son güncellemeden bu yana geçen süreye göre belirlenen, sabit zaman adımlı güncellemenin kaç kez çağrılacağını gösterir.

:::sidenote
**Her** bileşen türünün güncellemesinden sonra tüm iletilerin dağıtıldığına dikkat edin; tabloyu sade tutmak için bu işlem aşağıdaki tabloda işaretlenmemiştir.
:::

Ardından döngü başlar:

| Adım | Motor aşaması | Lua geri çağırımı | Açıklama |
|-|-|-|-|
| 1 | **Sabit zaman adımlı güncelleme** | `fixed_update()` | Sabit zaman adımlı güncelleme aşamasını uygulayan her bileşen türü için motorun iç öncelik sırasıyla, zamanlamaya bağlı olarak kare başına `0..N` kez çağrılır. *Fizik* bileşenlerinin sabit zaman adımlı güncelleme adımlarını da içerir. |
| 2 | **Güncelleme** | `update()` | Güncelleme aşamasını uygulayan her bileşen türü için motorun iç öncelik sırasıyla kare başına bir kez çağrılır. Ayrıca `go.animate()` ile başlatılan oyun nesnesi özelliği animasyonları burada ayrı bir bileşen türü olarak güncellenir. Etkin her koleksiyon vekili için `Update` aşaması 1. adımdan başlayarak özyinelemeli olarak çağrılır. |
| 3 | **Geç güncelleme** | `late_update()` | Geç güncelleme aşamasını uygulayan her bileşen türü için motorun iç öncelik sırasıyla kare başına bir kez çağrılır. |
| 4 | **Dönüşümler** | | Sonda her bileşen için, gerekirse ek bir son dönüşüm güncellemesi gerçekleştirilir. |

Defold'un güncelleme aşamasındaki iç işleyişi hakkında daha fazla ayrıntıya ihtiyaç duyarsanız doğrudan [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp) kodunu okumanız yararlı olur.

### İşleme güncellemesi aşaması

İşleme güncellemesi bloğu önce `@render` soketine gönderilen tüm iletileri (örneğin kamera bileşeninin `set_view_projection` iletilerini, `set_clear_color` iletilerini vb.) dağıtır. Ardından işleme betiğinin `update()` işlevi çağrılır.

![İşleme güncellemesi aşaması](images/application_lifecycle/render_update_phase.png)

### Güncelleme sonrası aşama

Güncellemelerden sonra, güncelleme sonrası adım dizisi çalıştırılır. Bu dizi, bellekten kaldırılmak üzere işaretlenen koleksiyon vekillerini bellekten kaldırır (bu işlem "iletileri dağıtma" adım dizisi sırasında gerçekleşir). Silinmek üzere işaretlenen her oyun nesnesi, varsa bileşenlerinin tüm `final()` işlevlerini çağırır. `final()` işlevlerindeki kod genellikle kuyruğa yeni iletiler gönderdiğinden, ardından "iletileri dağıtma" geçişi çalıştırılır.

![Güncelleme sonrası aşama](images/application_lifecycle/post_update_phase.png)

Sonraki adımda, oyun nesnesi oluşturması istenen her fabrika bileşeni bu nesneyi oluşturur. Son olarak, silinmek üzere işaretlenen oyun nesneleri fiilen silinir.

### İşleme aşaması

Güncelleme döngüsünün son adımı, `@system` iletilerinin (`exit`, `reboot` iletileri, profil çıkarıcıyı açıp kapatma, video kaydını başlatma ve durdurma vb.) dağıtılmasını içerir.

![İşleme aşaması](images/application_lifecycle/render_phase.png)

Ardından grafikler ve görsel profil çıkarıcının görüntüsü işlenir ([Hata ayıklama belgelerine](/manuals/debugging) bakın). Grafikler işlendikten sonra video kaydı yapılır.

#### Kare hızı ve koleksiyonun zaman adımı

Saniyedeki kare güncellemesi sayısı (güncelleme döngüsünün saniyedeki çalıştırılma sayısına eşittir), proje ayarlarında veya `@system` soketine `set_update_frequency` iletisi gönderilerek program aracılığıyla ayarlanabilir. Ayrıca vekile bir `set_time_step` iletisi göndererek koleksiyon vekillerinin _zaman adımını_ ayrı ayrı ayarlamak mümkündür. Bir koleksiyonun zaman adımını değiştirmek kare hızını etkilemez. Fizik güncellemesinin zaman adımını ve `update().` işlevine iletilen `dt` değişkenini etkiler. Zaman adımını değiştirmenin, her karede `update()` işlevinin kaç kez çağrılacağını değiştirmediğine de dikkat edin --- her zaman tam olarak bir kez çağrılır.

(Ayrıntılar için [Koleksiyon vekili kılavuzuna](/manuals/collection-proxy) ve [`set_time_step`](/ref/collectionproxy#set-time-step) başvurusuna bakın)

#### Motorun çalışmasını kısıtlama

Defold 1.12.0 ile, girdileri algılamaya devam ederken motor güncellemelerini ve işlemeyi tamamen atlayabilen bir motor kısıtlama (engine throttling) API'si sunulmuştur. Herhangi bir girdi motoru yeniden uyandırır ve motor bir bekleme süresinden sonra yeniden kısıtlı çalışmaya geçebilir.

Ayrıntılar ve kullanım örnekleri için `sys.set_engine_throttle()` API'sine bakın.

## Sonlandırma işlemleri

Uygulama kapanırken önce son güncelleme döngüsünün adım dizisini tamamlar. Bu dizi, her vekil koleksiyonundaki tüm oyun nesnelerinin sonlandırma işlemlerini yapıp nesneleri silerek tüm koleksiyon vekillerini bellekten kaldırır.

Bu tamamlandığında motor, ana koleksiyonu ve nesnelerini ele alan bir sonlandırma dizisine girer:

![Sonlandırma işlemleri](images/application_lifecycle/finalization.png)

Önce bileşenlerin `final()` işlevleri çağrılır. Ardından iletiler dağıtılır. Son olarak tüm oyun nesneleri silinir ve ana koleksiyon bellekten kaldırılır.

Motor daha sonra arka planda alt sistemleri kapatmaya devam eder: proje yapılandırması silinir, bellek profil çıkarıcısı kapatılır ve benzeri işlemler gerçekleştirilir.

Uygulama artık tamamen kapanmıştır.

## İletileri dağıtma {#dispatching-messages}

**İletileri dağıtma**, **her** bileşen türünün güncellemesinden sonra gerçekleştirilen özel bir geçiştir; örneğin sprite bileşenlerinin güncellenmesi, betiklerin güncellenmesi ve ileti gönderebilecek diğer eylemlerden sonra çalıştırılır. Bu geçiş sırasında bir kuyrukta biriken, gönderilmiş tüm iletiler dağıtılır. Bunlar şemalarda küçük "oklu zarf" simgeleri 📩 ile işaretlenir.

![İletileri dağıtma](images/application_lifecycle/dispatch_messages.png)

Her bileşen için `on_message()` çağrılarak tüm **kullanıcı tanımlı iletiler** dağıtıldıktan sonra, Defold'un özel iletileri her koleksiyon vekili için (şemada da gösterildiği gibi) aşağıdaki sırayla işlenir:

1. `load` iletileri - yüklenmek üzere işaretlenen koleksiyon vekillerini yükler, yanıt olarak `proxy_loaded` iletisi gönderir.
2. `unload` iletileri - bellekten kaldırılmak üzere işaretlenen koleksiyon vekillerini bellekten kaldırır, yanıt olarak `proxy_unloaded` iletisi gönderir.
3. `init` iletileri - başlangıç işlemleri yapılacak tüm koleksiyon vekilleri için `Collection Init` aşamasını tetikler.
4. `final` iletileri - sonlandırılmak üzere işaretlenen vekilin tüm bileşenlerinde `final()` işlevini tetikler.
5. `enable` iletileri - koleksiyon vekilini etkinleştirir; böylece bir sonraki karede bu vekil için `Update Loop` çalıştırılır. Bu işlem, koleksiyonun her bileşeni için dolaylı olarak `init()` işlevini tetikler.
6. `disable` iletileri - koleksiyon vekilini devre dışı bırakır; böylece bir sonraki karede bu vekil için `Update Loop` **çalıştırılmaz**. Bu vekil için `Update Loop` çalıştırılmasını tamamen durdurur.

Alıcı bileşenlerin `on_message()` kodu ek iletiler gönderebildiğinden, ileti dağıtıcısı ileti kuyruğu boşalana kadar gönderilen iletileri özyinelemeli olarak dağıtmaya devam eder. Ancak ileti dağıtıcısının ileti kuyruğunu kaç kez dolaşacağına ilişkin bir sınır vardır. Ayrıntılar için [İleti zincirlerine](/manuals/message-passing) bakın.
