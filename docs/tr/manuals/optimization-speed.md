---
title: Bir Defold oyununun çalışma zamanı performansını optimize etme
brief: Bu kılavuz, bir Defold oyununu yüksek ve kararlı bir kare hızında çalışacak şekilde nasıl optimize edeceğinizi açıklar.
---

# Çalışma hızını optimize etme
Bir oyunu yüksek ve kararlı bir kare hızında çalışacak şekilde optimize etmeye girişmeden önce darboğazların nerede olduğunu bilmeniz gerekir. Oyununuzun bir karesinde en çok süreyi gerçekte ne tüketiyor? Görüntüyü oluşturan işleme (rendering) aşaması mı? Oyun mantığınız mı? Sahne grafı (scene graph) mı? Bunu belirlemek için yerleşik profil çıkarma (profiling) araçlarını kullanmanız önerilir. Oyununuzun performansından örnekler almak için [ekran üstü veya web profil çıkarıcısını](/manuals/profiling/) kullanın, ardından optimizasyon gerekip gerekmediğine ve nelerin optimize edileceğine karar verin. Neyin zaman aldığını daha iyi anladıktan sonra sorunları ele almaya başlayabilirsiniz.

## Betik yürütme süresini azaltın
Profil çıkarıcı `Script` kapsamı için yüksek değerler gösteriyorsa betik (script) yürütme süresini azaltmanız gerekir. Genel bir kural olarak, elbette her karede mümkün olduğunca az kod çalıştırmaya çalışmalısınız. Her karede `update()` ve `on_input()` içinde çok fazla kod çalıştırmanın, özellikle düşük donanımlı cihazlarda oyununuzun performansını etkilemesi muhtemeldir. İzleyebileceğiniz bazı yönergeler şunlardır:

### Tepkisel kod kalıplarını kullanın
Bir geri çağırım (callback) alabiliyorsanız değişiklikleri düzenli aralıklarla sorgulamayın. Bir nesnenin animasyonunu kendiniz yönetmeyin veya motora devredilebilecek bir işi kendiniz yapmayın (örneğin, animasyonu kendiniz yönetmek yerine `go.animate)()` kullanmak).

### Çöp toplamayı azaltın
Her karede Lua tabloları gibi çok sayıda kısa ömürlü nesne oluşturursanız bu, eninde sonunda Lua'nın çöp toplayıcısını (garbage collector) tetikler. Bu durum, kare süresinde küçük takılmalar/ani artışlar olarak kendini gösterebilir. Mümkün olduğunda tabloları yeniden kullanın ve döngüler ile benzer yapıların içinde Lua tabloları oluşturmaktan mümkün olduğunca kaçınmaya özen gösterin.

### İleti ve eylem tanımlayıcılarının karma değerlerini önceden hesaplayın
Çok sayıda ileti işliyorsanız veya çok sayıda girdi olayını ele almanız gerekiyorsa dizelerin karma (hash) değerlerini önceden hesaplamanız önerilir. Şu kod parçasını inceleyin:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

Yukarıdaki senaryoda, her ileti alındığında dizenin karma değeri yeniden oluşturulur. Karma değerlerini bir kez oluşturup ileti işlerken bunları kullanarak bu durumu iyileştirebilirsiniz:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### URL adreslerini tercih edin ve önbelleğe alın
Bir oyun nesnesine (game object) veya bileşene (component) ileti gönderirken ya da bunları başka bir yolla adreslerken tanımlayıcıyı dize, karma değeri veya URL olarak verebilirsiniz. Dize veya karma değeri kullanılırsa bu değer sistem içinde bir URL adresine dönüştürülür. Bu nedenle, sistemden mümkün olan en iyi performansı elde etmek için sık kullanılan URL adreslerini önbelleğe almanız önerilir. Şu örneği inceleyin:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

Her üç durumda da `enemy` tanımlayıcısına sahip oyun nesnesinin konumu alınır. İlk ve ikinci durumda tanımlayıcı (dize veya karma değeri), kullanılmadan önce bir URL adresine dönüştürülür. Bu, mümkün olan en iyi performansı elde etmek için URL adreslerini önbelleğe alıp önbellekteki sürümlerini kullanmanın daha iyi olduğunu gösterir:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## Bir kareyi işlemek için gereken süreyi azaltın
Profil çıkarıcı `Render` ve `Render Script` kapsamlarında yüksek değerler gösteriyorsa bir kareyi işlemek için gereken süreyi azaltmanız gerekir. Bir kareyi işlemek için gereken süreyi azaltmaya çalışırken dikkate alınacak birkaç konu vardır:

* Çizim çağrılarını (draw call) azaltın - Çizim çağrılarını azaltma hakkında daha fazla bilgi için [bu forum gönderisini](https://forum.defold.com/t/draw-calls-and-defold/4674) okuyun
* Üst üste çizimi (overdraw) azaltın
* Gölgelendirici (shader) karmaşıklığını azaltın - GLSL optimizasyonları hakkında [Khronos'un bu makalesini](https://www.khronos.org/opengl/wiki/GLSL_Optimizations) okuyun. Ayrıca Defold'un kullandığı varsayılan gölgelendiricileri (`builtins/materials` içinde bulunurlar) değiştirebilir ve gölgelendiricinin `highp` gerektirmediği yerlerde daha düşük hassasiyet seçebilirsiniz. Çapraz derlenen GLSL ES gölgelendiricilerinde varsayılan hassasiyet, kayan noktalı değerler için `mediump`, tam sayılar için `highp` olur; bu varsayılanlar Shader proje ayarlarından değiştirilebilir. Değişken başına açıkça belirtilen niteleyiciler önceliklidir. [Gölgelendirici hassasiyeti belgelerine](/manuals/shader/#precision) bakın.

## Sahne grafının karmaşıklığını azaltın
Profil çıkarıcı `GameObject` kapsamında, daha özel olarak da `UpdateTransform` ölçüm örneğinde yüksek değerler gösteriyorsa sahne grafının karmaşıklığını azaltmanız gerekir. Yapabileceklerinizden biri şudur:

* Görünmeyenleri eleme (culling) - Oyun nesneleri o anda görünür değilse bunları (ve bileşenlerini) devre dışı bırakın. Bunun nasıl belirleneceği büyük ölçüde oyunun türüne bağlıdır. 2B bir oyunda bu, dikdörtgen bir alanın dışında kalan oyun nesnelerini her zaman devre dışı bırakmak kadar basit olabilir. Bunu algılamak için bir fizik tetikleyicisi kullanabilir veya nesnelerinizi gruplara ayırabilirsiniz. Hangi nesnelerin devre dışı bırakılacağını veya etkinleştirileceğini belirledikten sonra her oyun nesnesine bir `disable` veya `enable` iletisi göndererek bunu yaparsınız.

## Görüş hacmi dışında kalanları eleme
İşleme betiği (render script), tanımlı bir sınırlayıcı kutunun (frustum) dışında kalan oyun nesnesi bileşenlerini otomatik olarak işleme dışında bırakabilir. Görüş hacmi dışında kalanları eleme (frustum culling) hakkında daha fazla bilgi için [İşleme hattı kılavuzuna](/manuals/render/#frustum-culling) bakın.

# Platforma özgü optimizasyonlar

## Android Device Performance Framework
Android Dynamic Performance Framework, oyunların Android cihazların güç ve ısıl sistemleriyle daha doğrudan etkileşim kurmasını sağlayan bir API kümesidir. Android sistemlerindeki dinamik davranışı izlemek ve oyun performansını cihazları aşırı ısıtmayan, sürdürülebilir bir düzeyde optimize etmek mümkündür. Android cihazlar için geliştirdiğiniz Defold oyununun performansını izlemek ve optimize etmek üzere [Android Dynamic Performance Framework uzantısını](https://defold.com/extension-adpf/) kullanın.
