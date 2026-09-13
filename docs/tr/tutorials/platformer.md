---
title: Defold platform oyunu öğreticisi
brief: Bu yazıda, Defold'da karolara dayalı temel bir 2B platform oyununun nasıl geliştirildiğini inceleyeceksiniz. Öğreneceğiniz mekanikler sola/sağa hareket etme, zıplama ve düşmedir.
---

# Platform oyunu

Bu yazıda, Defold'da karolara dayalı temel bir 2B platform oyununun (platformer) nasıl geliştirildiğini inceleyeceğiz. Öğreneceğimiz mekanikler sola/sağa hareket etme, zıplama ve düşmedir.

Bir platform oyunu oluşturmanın pek çok farklı yolu vardır. Rodrigo Monteiro, bu konu ve daha fazlası hakkında [burada](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/) kapsamlı bir analiz yazmış.

Platform oyunu yapmaya yeni başlıyorsanız okumanızı özellikle öneririz; çünkü pek çok değerli bilgi içeriyor. Anlatılan yöntemlerin birkaçını ve bunları Defold'da nasıl uygulayacağınızı biraz daha ayrıntılı ele alacağız. Bununla birlikte, anlatılanları diğer platformlara ve dillere taşımak da kolay olmalı (Defold'da Lua kullanıyoruz).

Vektör matematiği (doğrusal cebir) hakkında biraz bilgi sahibi olduğunuzu varsayıyoruz. Değilseniz, oyun geliştirmede son derece yararlı olduğu için bu konuda okuma yapmanız iyi olur. Wolfire'dan David Rosen, bu konuda [burada](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/) çok iyi bir yazı dizisi hazırlamış.

Defold'u zaten kullanıyorsanız _Platformer_ şablon projesini temel alan yeni bir proje oluşturabilir ve bu yazıyı okurken onunla denemeler yapabilirsiniz.

::: sidenote
Bazı okuyucular, önerdiğimiz yöntemin Box2D'nin varsayılan uygulamasıyla mümkün olmadığını belirtti. Bunun çalışması için Box2D'de birkaç değişiklik yaptık:

Kinematik (kinematic) ve statik (static) nesneler arasındaki çarpışmalar yok sayılır. `b2Body::ShouldCollide` ve `b2ContactManager::Collide` içindeki kontrolleri değiştirin.

Ayrıca temas mesafesi (Box2D'de separation olarak adlandırılır) geri çağırım işlevine (callback function) iletilmez.
`b2ManifoldPoint` yapısına bir mesafe üyesi ekleyin ve `b2Collide*` işlevlerinde güncellendiğinden emin olun.
:::

## Çarpışma algılama

Oyuncunun bölüm geometrisinin (level geometry) içinden geçmesini önlemek için çarpışma algılama (collision detection) gerekir.
Oyununuza ve özel gereksinimlerine bağlı olarak bunu ele almanın çeşitli yolları vardır.
Mümkünse bunu bir fizik motoruna (physics engine) bırakmak en kolay yollardan biridir.
Defold'da 2B oyunlar için [Box2D](http://box2d.org/) fizik motorunu kullanıyoruz.
Box2D'nin varsayılan uygulaması gereken tüm özellikleri içermez; yaptığımız değişiklikler için bu yazının sonuna bakın.

Bir fizik motoru, fiziksel davranışı benzetmek için fizik nesnelerinin durumlarını şekilleriyle birlikte saklar. Benzetim sırasında çarpışmaları da bildirir; böylece oyun, çarpışmalar gerçekleştiğinde tepki verebilir. Çoğu fizik motorunda üç nesne türü vardır: _statik_, _dinamik_ (dynamic) ve _kinematik_ nesneler (bu adlar diğer fizik motorlarında farklı olabilir). Başka nesne türleri de vardır, ancak şimdilik onları bir kenara bırakalım.

- *Statik* bir nesne hiçbir zaman hareket etmez (örneğin bölüm geometrisi).
- *Dinamik* bir nesne, benzetim sırasında hıza (velocity) dönüştürülen kuvvetlerden ve torklardan etkilenir.
- *Kinematik* bir nesne uygulama mantığı tarafından kontrol edilir, ancak yine de diğer dinamik nesneleri etkiler.

Böyle bir oyunda, gerçek dünyadaki fiziksel davranışa benzeyen bir şey arıyoruz; ancak hızlı tepki veren kontroller ve dengeli mekanikler çok daha önemlidir. İyi hissettiren bir zıplamanın fiziksel olarak doğru olması veya gerçek dünyadaki yerçekimine göre davranması gerekmez. Yine de [bu](http://hypertextbook.com/facts/2007/mariogravity.shtml) analiz, Mario oyunlarındaki yerçekiminin her sürümde 9,8 m/s<sup>2</sup> değerine yaklaştığını gösteriyor. :-)

Amaçlanan deneyimi elde etmek üzere mekanikleri tasarlayıp ince ayar yapabilmek için olup bitenleri tamamen kontrol edebilmemiz önemlidir. Bu nedenle oyuncu karakterini kinematik bir nesneyle modellemeyi seçiyoruz. Böylece fiziksel kuvvetlerle uğraşmadan oyuncu karakterini istediğimiz gibi hareket ettirebiliriz. Bu, karakteri bölüm geometrisinden ayırmayı kendimizin çözmesi gerektiği anlamına gelir (bunu ileride ayrıntılı olarak ele alacağız), ancak bu dezavantajı kabul ediyoruz. Oyuncu karakterini fizik dünyasında bir kutu şekliyle temsil edeceğiz.

## Hareket

Oyuncu karakterinin kinematik bir nesneyle temsil edilmesine karar verdiğimize göre, konumunu ayarlayarak onu serbestçe hareket ettirebiliriz. Sola/sağa hareketle başlayalım.

Karaktere ağırlık hissi vermek için hareketi ivmeye dayandıracağız. Sıradan bir araçta olduğu gibi ivme, oyuncu karakterinin en yüksek sürate ne kadar çabuk ulaşabileceğini ve yön değiştirebileceğini belirler. İvme, karenin (frame) zaman adımı boyunca---genellikle `dt` (delta-`t`) parametresiyle verilir---etki eder ve ardından hıza eklenir. Benzer biçimde hız da kare boyunca etki eder ve ortaya çıkan öteleme (translation) konuma eklenir. Matematikte buna [zamana göre integral alma](http://en.wikipedia.org/wiki/Integral) denir.

![Hızın yaklaşık integralinin alınması](images/platformer/integration.png)

İki dikey çizgi karenin başlangıcını ve sonunu gösterir. Çizgilerin yüksekliği, oyuncu karakterinin bu iki andaki hızıdır. Bu hızlara `v0` ve `v1` diyelim. `v1`, ivmenin (eğrinin eğiminin) `dt` zaman adımı boyunca uygulanmasıyla elde edilir:

![Hız denklemi](images/platformer/equationofvelocity.png)

Turuncu alan, geçerli kare sırasında oyuncu karakterine uygulamamız gereken ötelemedir. Geometrik olarak alanı yaklaşık şu şekilde hesaplayabiliriz:

![Öteleme denklemi](images/platformer/equationoftranslation.png)

Güncelleme döngüsünde karakteri hareket ettirmek için ivmenin ve hızın integralini şöyle alırız:

1. Girdiye (input) göre hedef sürati belirleyin
2. Geçerli süratimizle hedef sürat arasındaki farkı hesaplayın
3. İvmeyi farkın yönünde etki edecek şekilde ayarlayın
4. Yukarıdaki gibi bu karedeki hız değişimini hesaplayın (`dv`, hız değişimi anlamındaki delta-velocity ifadesinin kısaltmasıdır):

    ```lua
    local dv = acceleration * dt
    ```

5. `dv` değerinin amaçlanan sürat farkını aşıp aşmadığını kontrol edin; aşıyorsa onu bu farkla sınırlandırın
6. Geçerli hızı daha sonra kullanmak üzere kaydedin (şu anda önceki karede kullanılan hız olan `self.velocity`):

    ```lua
    local v0 = self.velocity
    ```

7. Hız değişimini ekleyerek yeni hızı hesaplayın:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Yukarıdaki gibi hızın integralini alarak bu karedeki x yönündeki ötelemeyi hesaplayın:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Bunu oyuncu karakterine uygulayın

Defold'da girdiyi nasıl işleyeceğinizden emin değilseniz, bu konuda [burada](/manuals/input) bir kılavuz var.

Bu aşamada karakteri sola ve sağa hareket ettirebiliyor, kontrollerde ağırlık hissi ve akıcılık elde edebiliyoruz. Şimdi yerçekimini ekleyelim!

Yerçekimi de bir ivmedir, ancak oyuncuyu y ekseni boyunca etkiler. Bu, yukarıda açıklanan hareket ivmesiyle aynı şekilde uygulanacağı anlamına gelir. Yukarıdaki hesaplamaları vektörlerle çalışacak biçimde değiştirip 3. adımda yerçekimini ivmenin y bileşenine dahil etmemiz yeterlidir. Vektör matematiğini sevmemek mümkün mü! :-)

## Çarpışmaya tepki

Oyuncu karakterimiz artık hareket edip düşebildiğine göre, çarpışmaya tepkileri (collision response) inceleme zamanı geldi.
Bölüm geometrisinin üzerine inmemiz ve onun boyunca hareket etmemiz gerektiği açık. Hiçbir şeyle iç içe geçmediğimizden emin olmak için fizik motorunun sağladığı temas noktalarını (contact point) kullanacağız.

Bir temas noktası, temasın _normal vektörünü_ (çarpıştığımız nesnenin dışına doğru yönelir, ancak diğer motorlarda farklı olabilir) ve diğer nesnenin ne kadar içine girdiğimizi ölçen bir _mesafeyi_ içerir. Oyuncuyu bölüm geometrisinden ayırmak için ihtiyacımız olan tek şey budur.
Kutu kullandığımız için bir kare sırasında birden fazla temas noktası alabiliriz. Örneğin kutunun iki köşesi yatay zeminle kesiştiğinde veya oyuncu bir köşeye doğru hareket ettiğinde bu durum oluşur.

![Oyuncu karakterine etki eden temas normalleri](images/platformer/collision.png)

Aynı düzeltmeyi birden fazla kez yapmamak için düzeltmeleri bir vektörde biriktiririz; böylece gereğinden fazla düzeltme yapmadığımızdan emin oluruz. Aksi halde çarpıştığımız nesneden fazla uzaklaşırdık. Yukarıdaki görüntüde, iki okla (normal vektörleriyle) gösterilen iki temas noktamız olduğunu görebilirsiniz. İç içe geçme mesafesi her iki temas için de aynıdır; bu mesafeyi her seferinde doğrudan kullansaydık oyuncuyu amaçlanan miktarın iki katı kadar hareket ettirirdik.

::: sidenote
Biriktirilen düzeltmeleri her karede sıfır vektörüne sıfırlamak önemlidir.
`update()` işlevinin sonuna şöyle bir satır ekleyin:
`self.corrections = vmath.vector3()`
:::

Her temas noktası için çağrılacak bir geri çağırım işlevi olduğunu varsayarsak, o işlevde ayırma işlemini şöyle yapabilirsiniz:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Düzeltme vektörünün temas normali üzerine izdüşümünü alın (ilk temas noktası için düzeltme vektörü sıfır vektörüdür)
2. Bu temas noktası için yapmamız gereken düzeltme miktarını hesaplayın
3. Bunu düzeltme vektörüne ekleyin
4. Düzeltmeyi oyuncu karakterine uygulayın

Oyuncunun hızının temas noktasına doğru yönelen kısmını da sıfırlamamız gerekir:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Hızın normal üzerine izdüşümünü alın
2. İzdüşüm negatifse, hızın bir kısmı temas noktasına doğru yöneliyor demektir; bu durumda o bileşeni kaldırın

## Zıplama

Artık bölüm geometrisi üzerinde koşup aşağı düşebildiğimize göre, zıplama zamanı geldi! Platform oyunlarında zıplama pek çok farklı şekilde uygulanabilir. Bu oyunda Super Mario Bros ve Super Meat Boy'dakine benzer bir şey hedefliyoruz. Zıplarken oyuncu karakteri, temelde sabit bir sürat olan bir itmeyle yukarı doğru itilir.

Yerçekimi karakteri sürekli yeniden aşağı çeker ve bunun sonucunda hoş bir zıplama yayı oluşur. Oyuncu havadayken de karakteri kontrol edebilir. Oyuncu, zıplama yayının tepe noktasından önce zıplama düğmesini bırakırsa zıplamayı erken sonlandırmak için yukarı yönlü sürat azaltılır.

1. Girdi düğmesine basıldığında şunu yapın:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Bu işlem yalnızca girdi düğmesine _basıldığı anda_ yapılmalıdır; düğmenin sürekli _basılı tutulduğu_ her karede değil.

2. Girdi düğmesi bırakıldığında şunu yapın:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike, [Super Mario Bros 3](http://meyermike.com/wp/?p=175) ve [Super Meat Boy](http://meyermike.com/wp/?p=160) oyunlarındaki zıplama yaylarını gösteren, incelemeye değer güzel grafikler hazırlamış.

## Bölüm geometrisi

Bölüm geometrisi, oyuncu karakterinin (ve muhtemelen başka şeylerin) çarpıştığı çevrenin çarpışma şekilleridir. Defold'da bu geometriyi oluşturmanın iki yolu vardır.

Bir seçenek, oluşturduğunuz bölümlerin üzerine ayrı çarpışma şekilleri yerleştirmektir. Bu yöntem çok esnektir ve grafiklerin hassas biçimde konumlandırılmasına olanak tanır. Özellikle yumuşak eğimler istiyorsanız kullanışlıdır.
[Braid](http://braid-game.com/) oyunu, bölümleri oluşturmak için bu yöntemi kullanmıştır; bu öğreticideki örnek bölüm de aynı yöntemle oluşturulmuştur. Defold düzenleyicisindeki görünümü şöyledir:

![Bölüm geometrisinin ve oyuncunun dünyaya yerleştirildiği Defold düzenleyicisi](images/platformer/editor.png)

Başka bir seçenek de bölümleri karolardan oluşturmak ve düzenleyicinin karo grafiklerine göre fizik şekillerini otomatik olarak üretmesini sağlamaktır. Bu, bölümleri değiştirdiğinizde bölüm geometrisinin de otomatik olarak güncelleneceği anlamına gelir ve son derece yararlı olabilir.

Yerleştirilen karolar hizalanıyorsa fizik şekilleri otomatik olarak tek bir şekilde birleştirilir.
Böylece birkaç yatay karo üzerinde kayarken oyuncu karakterinizin durmasına veya takılmasına neden olabilecek boşluklar ortadan kalkar. Bu işlem, yükleme sırasında Box2D'de karo çokgenlerinin kenar şekilleriyle değiştirilmesiyle yapılır.

![Birleştirilerek tek şekil haline getirilmiş birden fazla karo çokgeni](images/platformer/stitching.png)

Yukarıdaki örnekte, platform oyunu grafiklerinin bir parçasından yan yana beş karo oluşturduk. Görüntüde, yerleştirilen karoların (üstte) birleştirilmiş tek bir şekle (alttaki gri dış hat) nasıl karşılık geldiğini görebilirsiniz.

Daha fazla bilgi için [fizik](/manuals/physics) ve [karolar](/manuals/2dgraphics) hakkındaki kılavuzlarımıza bakın.

## Son sözler

Platform oyunu mekanikleri hakkında daha fazla bilgi istiyorsanız [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide) oyunundaki fizikle ilgili burada etkileyici miktarda bilgi bulabilirsiniz.

Şablon projemizi bir iOS aygıtında veya fareyle denerseniz zıplama oldukça tuhaf hissettirebilir.
Bu, tek dokunma girdisiyle platform oyunu oynatmaya yönelik pek başarılı olmayan denememizden kaynaklanıyor. :-)

Bu oyundaki animasyonları nasıl ele aldığımızdan söz etmedik. Aşağıdaki *player.script* dosyasındaki `update_animations()` işlevini inceleyerek fikir edinebilirsiniz.

Umarız bu bilgileri yararlı bulmuşsunuzdur!
Lütfen hepimizin oynayabileceği harika bir platform oyunu yapın! <3

## Kod

*player.script* dosyasının içeriği şöyle:

```lua
-- player.script

-- these are the tweaks for the mechanics, feel free to change them for a different feeling
-- the acceleration to move right/left
local move_acceleration = 3500
-- acceleration factor to use when air-borne
local air_acceleration_factor = 0.8
-- max speed right/left
local max_speed = 450
-- gravity pulling the player down in pixel units
local gravity = -1000
-- take-off speed when jumping in pixel units
local jump_takeoff_speed = 550
-- time within a double tap must occur to be considered a jump (only used for mouse/touch controls)
local touch_jump_timeout = 0.2

-- prehashing ids improves performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- this lets us handle input in this script
    msg.post(".", "acquire_input_focus")

    -- initial player velocity
    self.velocity = vmath.vector3(0, 0, 0)
    -- support variable to keep track of collisions and separation
    self.correction = vmath.vector3()
    -- if the player stands on ground or not
    self.ground_contact = false
    -- movement input in the range [-1,1]
    self.move_input = 0
    -- the currently playing animation
    self.anim = nil
    -- timer that controls the jump-window when using mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- only play animations which are not already playing
    if self.anim ~= anim then
        -- tell the sprite to play the animation
        sprite.play_flipbook("#sprite", anim)
        -- remember which animation is playing
        self.anim = anim
    end
end

local function update_animations(self)
    -- make sure the player character faces the right way
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- make sure the right animation is playing
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determine the target speed based on input
    local target_speed = self.move_input * max_speed
    -- calculate the difference between our current speed and the target speed
    local speed_diff = target_speed - self.velocity.x
    -- the complete acceleration to integrate over this frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- set the acceleration to work in the direction of the difference
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- decrease the acceleration when air-borne to give a slower feel
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calculate the velocity change this frame (dv is short for delta-velocity)
    local dv = acceleration * dt
    -- check if dv exceeds the intended speed difference, clamp it in that case
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- save the current velocity for later use
    -- (self.velocity, which right now is the velocity used the previous frame)
    local v0 = self.velocity
    -- calculate the new velocity by adding the velocity change
    self.velocity = self.velocity + dv
    -- calculate the translation this frame by integrating the velocity
    local dp = (v0 + self.velocity) * dt * 0.5
    -- apply it to the player character
    go.set_position(go.get_position() + dp)

    -- update the jump timer
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- check if we received a contact point message
    if message_id == msg_contact_point_response then
        -- check that the object is something we consider an obstacle
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    -- (extend this with a counter to do things like double-jumps)
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
        -- play animation
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move towards the touch-point
        local diff = action.x - go.get_position().x
        -- only give input when far away (more than 10 pixels)
        if math.abs(diff) > 10 then
            -- slow down when less than 100 pixels away
            self.move_input = diff / 100
            -- clamp input to [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- start timing the last release to see if we are about to jump
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- jump on double tap
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
