---
title: Defold'da çarpışma olayları
brief: Tüm çarpışma ve etkileşim iletilerini belirtilen tek bir işleve yönlendirmek için `physics.set_event_listener()` kullanılarak çarpışma olaylarının işlenmesi merkezileştirilebilir.
---

# Defold'da fizik olaylarını işleme

Defold, `physics.set_event_listener()` işleviyle fizik olaylarının (physics events) tek merkezden işlenmesini sağlar. Bu işlev, tüm fizik etkileşim olaylarını tek bir yerde işlemek için özel bir dinleyici (listener) belirlemenize olanak tanır; böylece kodunuz sadeleşir ve verimlilik artar.

## Fizik dünyası dinleyicisini ayarlama

Defold'da her koleksiyon vekili (collection proxy), kendine ait ayrı bir fizik dünyası (physics world) oluşturur. Bu nedenle birden çok koleksiyon vekiliyle çalışırken her biriyle ilişkili ayrı fizik dünyalarını yönetmeniz gerekir. Fizik olaylarının her dünyada doğru işlenmesini sağlamak için her koleksiyon vekilinin dünyasına özel bir fizik dünyası dinleyicisi ayarlamanız gerekir.

Bu düzen, fizik olayları dinleyicisinin vekilin temsil ettiği koleksiyonun (collection) bağlamından ayarlanması gerektiği anlamına gelir. Böylece dinleyiciyi doğrudan ilgili fizik dünyasıyla ilişkilendirir ve fizik olaylarını doğru işlemesini sağlarsınız.

Bir koleksiyon vekili içinde fizik dünyası dinleyicisinin nasıl ayarlanacağına ilişkin bir örnek:

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

Bu yöntemi uygulayarak bir koleksiyon vekilinin oluşturduğu her fizik dünyasının kendine özel bir dinleyicisi olmasını sağlarsınız. Bu, birden çok koleksiyon vekili kullanan projelerde fizik olaylarının etkili biçimde işlenmesi için çok önemlidir.

::: important
Bir dinleyici ayarlandığında, bu dinleyicinin ayarlandığı fizik dünyası için artık [fizik iletileri](/manuals/physics-messages) gönderilmez.
:::

## Olay verilerinin yapısı

Dinleyici, `self` ve bir `events` tablosuyla çağrılır. `events` tablosu, geri çağırım (callback) için toplanan tüm fizik olaylarını içeren bir dizidir. Her öğe, olay adının karma değerini içeren bir `type` alanına ve o olay türüne özgü ek alanlara sahip bir olay tablosudur.

Olay tabloları aşağıdaki verileri içerir:

1. **Temas noktası olayı (`contact_point_event`):**
Bu olay, iki çarpışma nesnesi (collision object) arasındaki bir temas noktasını (contact point) bildirir. Darbe kuvvetlerini veya çarpışmaya özel tepkileri hesaplamak gibi ayrıntılı çarpışma işlemlerinde yararlıdır.

   - `applied_impulse`: Temastan kaynaklanan itme.
   - `distance`: Nesneler arasındaki iç içe geçme mesafesi.
   - `a` ve `b`: Çarpışan varlıkları temsil eden nesneler; her biri şunları içerir:
     - `position`: Temas noktasının dünya konumu (vector3).
     - `instance_position`: Oyun nesnesi (game object) örneğinin dünya konumu (vector3).
     - `id`: Örneğin ID değeri (hash).
     - `group`: Çarpışma grubu (hash).
     - `relative_velocity`: Diğer nesneye göre hız (vector3).
     - `mass`: Kilogram cinsinden kütle (number).
     - `normal`: Diğer nesneden dışarı doğru yönelen temas normali (vector3).

2. **Çarpışma olayı (`collision_event`):**
Bu olay, iki nesne arasında bir çarpışma gerçekleştiğini belirtir. Temas noktası olayına kıyasla daha genel bir olaydır ve temas noktaları hakkında ayrıntılı bilgi gerektirmeden çarpışmaları algılamak için idealdir.

   - `a` ve `b`: Çarpışan varlıkları temsil eden nesneler; her biri şunları içerir:
     - `position`: Dünya konumu (vector3).
     - `id`: Örneğin ID değeri (hash).
     - `group`: Çarpışma grubu (hash).

3. **Tetikleyici olayı (`trigger_event`):** 
Bu olay, bir nesne bir tetikleyici (trigger) nesnesiyle etkileşime girdiğinde gönderilir. Oyununuzda bir nesnenin girip çıkmasıyla bir şeylerin gerçekleşmesini sağlayan alanlar oluşturmak için yararlıdır.

   - `enter`: Etkileşimin bir giriş (true) mi yoksa çıkış (false) mı olduğunu belirtir.
   - `a` ve `b`: Tetikleyici olayına katılan nesneler; her biri şunları içerir:
     - `id`: Örneğin ID değeri (hash).
     - `group`: Çarpışma grubu (hash).

4. **Işın sorgusu yanıtı (`ray_cast_response`):**
Bu olay, bir ışın sorgusuna (raycast) yanıt olarak gönderilir ve ışının isabet ettiği nesne hakkında bilgi sağlar.

   - `group`: İsabet edilen nesnenin çarpışma grubu (hash).
   - `request_id`: Işın sorgusu isteğinin tanımlayıcısı (number).
   - `position`: İsabet konumu (vector3).
   - `fraction`: İsabetin gerçekleştiği uzaklığın ışının uzunluğuna oranı (number).
   - `normal`: İsabet konumundaki normal (vector3).
   - `id`: İsabet edilen nesne örneğinin ID değeri (hash).

5. **Işın sorgusunun isabet etmemesi (`ray_cast_missed`):**
Bu olay, bir ışın sorgusu hiçbir nesneye isabet etmediğinde gönderilir.

   - `request_id`: İsabet etmeyen ışın sorgusu isteğinin tanımlayıcısı (number).

## Kullanım örneği

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Kısıtlamalar

Dinleyici, olay gerçekleştiği anda eşzamanlı olarak çağrılır. Bu çağrı bir zaman adımının ortasında gerçekleşir; bu da fizik dünyasının kilitli olduğu anlamına gelir. Bu durum, fizik dünyası simülasyonlarını etkileyebilecek işlevlerin, örneğin `physics.create_joint()` işlevinin kullanılmasını imkânsız kılar.

Bu kısıtlamalardan nasıl kaçınılacağını gösteren küçük bir örnek:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
