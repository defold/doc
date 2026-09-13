---
title: Defold'da çarpışma iletileri
brief: İki nesne çarpıştığında motor olay geri çağırımını çağırır veya tüm alıcılara iletiler gönderir.
---

# Çarpışma iletileri

İki nesne çarpıştığında motor olay geri çağırımına (event callback) bir olay (event) gönderir veya her iki nesnenin tüm alıcılarına iletiler (message) gönderir.

## Olay filtreleme

Üretilecek olay türleri, her nesnenin şu bayraklarıyla kontrol edilebilir:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Bunların tümü varsayılan olarak `true` değerindedir.
İki çarpışma nesnesi (collision object) etkileşime girdiğinde, bu onay kutularına göre kullanıcıya ileti gönderilip gönderilmeyeceğini kontrol ederiz.

Örneğin, "Generate Contact Events" onay kutuları için:

`physics.set_event_listener()` kullanıldığında:

| Bileşen A | Bileşen B | İleti gönderilir mi? |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Evet         |
| ❌          | ✅︎          | Evet         |
| ✅︎          | ❌          | Evet         |
| ❌          | ❌          | Hayır        |

Varsayılan ileti işleyicisi kullanıldığında:

| Bileşen A | Bileşen B | İleti(ler) gönderilir mi? |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Evet (A,B) + (B,A) |
| ❌          | ✅︎          | Evet (B,A)         |
| ✅︎          | ❌          | Evet (A,B)         |
| ❌          | ❌          | Hayır              |

## Çarpışmaya tepki

Çarpışan nesnelerden biri "dynamic", "kinematic" veya "static" türündeyse `"collision_response"` iletisi gönderilir. Bu iletinin aşağıdaki alanları doldurulur:

`other_id`
: çarpışma nesnesinin çarpıştığı nesne örneğinin (instance) tanımlayıcısı (`hash`)

`other_position`
: çarpışma nesnesinin çarpıştığı örneğin dünya uzayındaki (world space) konumu (`vector3`)

`other_group`
: diğer çarpışma nesnesinin çarpışma grubu (collision group) (`hash`)

`own_group`
: çarpışma nesnesinin çarpışma grubu (`hash`)

`collision_response` iletisi, yalnızca nesnelerin gerçekte nasıl kesiştiğine dair ayrıntılara ihtiyaç duymadığınız çarpışmaları çözmek için yeterlidir; örneğin bir merminin düşmana isabet edip etmediğini algılamak istediğinizde kullanılabilir. Her karede, çarpışan her nesne çifti için bu iletilerden yalnızca bir tane gönderilir.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Temas noktası tepkisi

Çarpışan nesnelerden biri "dynamic" veya "kinematic", diğeri ise "dynamic", "kinematic" veya "static" türündeyse `"contact_point_response"` iletisi gönderilir. Bu iletinin aşağıdaki alanları doldurulur:

`position`
: temas noktasının (contact point) dünya konumu (`vector3`).

`normal`
: temas noktasının diğer nesneden geçerli nesneye doğru yönelen, dünya uzayındaki normal vektörü (`vector3`).

`relative_velocity`
: diğer nesneden gözlemlenen çarpışma nesnesinin göreli hızı (`vector3`).

`distance`
: nesneler arasındaki iç içe geçme mesafesi -- negatif değildir (`number`).

`applied_impulse`
: temasın neden olduğu itme (`number`).

`life_time`
: (*şu anda kullanılmıyor!*) temasın yaşam süresi (`number`).

`mass`
: geçerli çarpışma nesnesinin kg cinsinden kütlesi (`number`).

`other_mass`
: diğer çarpışma nesnesinin kg cinsinden kütlesi (`number`).

`other_id`
: çarpışma nesnesinin temas ettiği örneğin tanımlayıcısı (`hash`).

`other_position`
: diğer çarpışma nesnesinin dünya konumu (`vector3`).

`other_group`
: diğer çarpışma nesnesinin çarpışma grubu (`hash`).

`own_group`
: çarpışma nesnesinin çarpışma grubu (`hash`).

Nesneleri tamamen ayırmanız gereken bir oyun veya uygulamada, `"contact_point_response"` iletisi ihtiyacınız olan tüm bilgileri sağlar. Ancak, çarpışmanın niteliğine bağlı olarak, çarpışan herhangi bir nesne çifti için her karede birden fazla `"contact_point_response"` iletisi alınabileceğini unutmayın. Daha fazla bilgi için [Çarpışmaları çözme kılavuzuna](/manuals/physics-resolving-collisions) bakın.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Tetikleyici tepkisi

Çarpışan nesnelerden biri "trigger" türündeyse `"trigger_response"` iletisi gönderilir. İleti, çarpışma ilk algılandığında bir kez, nesnelerin çarpışması sona erdiğinde ise bir kez daha gönderilir. Aşağıdaki alanları içerir:

`other_id`
: çarpışma nesnesinin çarpıştığı örneğin tanımlayıcısı (`hash`).

`enter`
: etkileşim tetikleyiciye giriş ise `true`, çıkış ise `false` değerini alır. (`boolean`).

`other_group`
: diğer çarpışma nesnesinin çarpışma grubu (`hash`).

`own_group`
: çarpışma nesnesinin çarpışma grubu (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
