---
title: Defold'da cihaz girdisi
brief: Bu kılavuz, girdinin nasıl çalıştığını, girdi eylemlerini yakalamayı ve bu eylemlere tepki veren betikler oluşturmayı açıklar.
---

# Girdi

Motor, tüm kullanıcı girdilerini yakalar ve girdi odağı (input focus) edinmiş oyun nesnelerinde (game object) bulunan, `on_input()` işlevini uygulayan betik ve GUI betiği bileşenlerine (component) eylemler olarak dağıtır. Bu kılavuz, girdiyi yakalamak için girdi eşlemelerini (input binding) nasıl ayarlayacağınızı ve girdiye tepki veren kodu nasıl oluşturacağınızı açıklar.

Girdi sistemi, girdiyi oyununuza uygun gördüğünüz şekilde yönetmenizi sağlayan basit ve güçlü kavramlar kullanır.

![Girdi eşlemeleri](images/input/overview.png)

Cihazlar
: Bilgisayarınızın veya mobil cihazınızın parçası olan ya da bunlara bağlanan girdi cihazları, Defold çalışma zamanı ortamına sistem düzeyinde ham girdi sağlar. Aşağıdaki cihaz türleri desteklenir:

  1. Klavye (tek tuş girdisi ve metin girdisi)
  2. Fare (konum, düğme tıklamaları ve fare tekerleği eylemleri)
  3. Tekli ve çoklu dokunma (iOS ve Android cihazlarda ve mobil cihazlardaki HTML5 uygulamalarında)
  4. Oyun kumandaları (işletim sistemi tarafından desteklendiği ve [gamepads](/manuals/input-gamepads/#gamepads-settings-file) dosyasında eşlendiği şekilde)

Girdi eşlemeleri
: Girdi bir betiğe gönderilmeden önce, cihazdan gelen ham girdi, girdi eşlemeleri tablosu aracılığıyla anlamlı *eylemlere* dönüştürülür.

Eylemler
: Eylemler, girdi eşlemeleri dosyasında listelediğiniz adlarla (bu adların karma değerleriyle) tanımlanır. Her eylem ayrıca girdiyle ilgili veriler içerir: bir düğmeye basılıp basılmadığı veya düğmenin bırakılıp bırakılmadığı, fare ve dokunma koordinatları vb.

Girdi dinleyicileri
: Herhangi bir betik bileşeni veya GUI betiği, *girdi odağı edinerek* girdi eylemleri (input action) alabilir. Aynı anda birden fazla dinleyici etkin olabilir.

Girdi yığını
: Girdi yığını (input stack), odağı ilk edinen dinleyicinin en altta, son edinen dinleyicinin en üstte olduğu girdi dinleyicileri listesidir.

Girdiyi tüketme
: Bir betik, aldığı girdiyi tüketmeyi seçerek yığının daha aşağısındaki dinleyicilerin bu girdiyi almasını engelleyebilir.

## Girdi eşlemelerini ayarlama

Girdi eşlemeleri, cihaz girdileri betik bileşenlerinize ve GUI betiklerinize dağıtılmadan önce bunların adlandırılmış *eylemlere* nasıl dönüştürüleceğini belirtmenizi sağlayan, proje genelinde geçerli bir tablodur. Yeni bir girdi eşlemesi dosyası oluşturmak için *Assets* görünümünde bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Input Binding</kbd> seçeneğini seçin. Motorun yeni dosyayı kullanması için *game.project* dosyasındaki *Game Binding* alanını değiştirin.

![Girdi eşlemesi ayarı](images/input/setting.png)

Tüm yeni proje şablonlarıyla birlikte varsayılan bir girdi eşlemesi dosyası otomatik olarak oluşturulur; bu nedenle genellikle yeni bir eşleme dosyası oluşturmanız gerekmez. Varsayılan dosyanın adı `game.input_binding` şeklindedir ve projenin kök dizinindeki `input` klasöründe bulunur. Dosyayı düzenleyicide açmak için dosyaya <kbd>çift tıklayın</kbd>:

![Girdi eşlemelerini ayarlama](images/input/input_binding.png)

Yeni bir eşleme oluşturmak için ilgili tetikleyici türü bölümünün altındaki <kbd>+</kbd> düğmesine tıklayın. Her kayıt iki alan içerir:

*Input*
: Kullanılabilir girdilerin kaydırılabilir listesinden seçilen, dinlenecek ham girdi.

*Action*
: Girdi eylemleri oluşturulup betiklerinize dağıtılırken onlara verilen eylem adı. Aynı eylem adı birden fazla girdiye atanabilir. Örneğin, <kbd>Space</kbd> tuşunu ve oyun kumandasının `A` düğmesini `jump` eylemine bağlayabilirsiniz. Ne yazık ki dokunma girdilerinin diğer girdilerle aynı eylem adlarını kullanmasını engelleyen bilinen bir hata olduğunu unutmayın.

## Tetikleyici türleri

Cihaza özgü beş tür tetikleyici oluşturabilirsiniz:

Key Triggers
: Tek tuşluk klavye girdisi. Her tuş, karşılık gelen bir eyleme ayrı ayrı eşlenir. Daha fazla bilgi için [tuş ve metin girdisi kılavuzuna](/manuals/input-key-and-text) bakın.

Text Triggers
: Metin tetikleyicileri, serbest metin girdisini okumak için kullanılır. Daha fazla bilgi için [tuş ve metin girdisi kılavuzuna](/manuals/input-key-and-text) bakın

Mouse Triggers
: Fare düğmelerinden ve kaydırma tekerleklerinden gelen girdi. Daha fazla bilgi için [fare ve dokunma girdisi kılavuzuna](/manuals/input-mouse-and-touch) bakın.

Touch Triggers
: Tekli dokunma ve çoklu dokunma türündeki tetikleyiciler, iOS ve Android cihazlarda yerel uygulamalarda ve HTML5 dağıtım paketlerinde kullanılabilir. Daha fazla bilgi için [fare ve dokunma kılavuzuna](/manuals/input-mouse-and-touch) bakın.

Gamepad Triggers
: Oyun kumandası tetikleyicileri, standart oyun kumandası girdisini oyun işlevlerine bağlamanızı sağlar. Daha fazla bilgi için [oyun kumandaları kılavuzuna](/manuals/input-gamepads) bakın.

### İvmeölçer girdisi

Defold, yukarıda listelenen beş farklı tetikleyici türüne ek olarak yerel Android ve iOS uygulamalarında ivmeölçer girdisini de destekler. *game.project* dosyanızın *Input* bölümündeki *Use Accelerometer* kutusunu işaretleyin.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- react to accelerometer data
    end
end
```

## Girdi odağı {#input-focus}

Bir betik bileşeninde veya GUI betiğinde girdi eylemlerini dinlemek için, bileşeni barındıran oyun nesnesine `acquire_input_focus` iletisi gönderilmelidir:

```lua
-- tell the current game object (".") to acquire input focus
msg.post(".", "acquire_input_focus")
```

Bu ileti, motora oyun nesnelerindeki girdi alabilen bileşenleri (betik bileşenleri, GUI bileşenleri ve koleksiyon vekilleri) *girdi yığınına* ekleme talimatı verir. Oyun nesnesinin bileşenleri girdi yığınının en üstüne yerleştirilir; son eklenen bileşen yığının en üstünde olur. Oyun nesnesinde girdi alabilen birden fazla bileşen varsa tüm bileşenlerin yığına ekleneceğini unutmayın:

![Girdi yığını](images/input/input_stack.png)

Daha önce girdi odağı edinmiş bir oyun nesnesi bunu yeniden yaparsa bileşenleri yığının en üstüne taşınır.


## Girdi dağıtımı ve on_input() {#input-dispatch-and-on_input}

Girdi eylemleri, girdi yığınına göre yukarıdan aşağıya doğru dağıtılır.

![Eylem dağıtımı](images/input/actions.png)

Yığında bulunan ve `on_input()` işlevini içeren her bileşende bu işlev, kare boyunca her girdi eylemi için bir kez, aşağıdaki bağımsız değişkenlerle çağrılır:

`self`
: Geçerli betik örneği.

`action_id`
: Eylemin, girdi eşlemelerinde ayarlanan adının karma değeri.

`action`
: Girdinin değeri, konumu (mutlak konum ve konum farkı), düğme girdisinin `pressed` olup olmadığı gibi eylemle ilgili yararlı verileri içeren bir tablo. Kullanılabilir eylem alanlarıyla ilgili ayrıntılar için [on_input()](/ref/go#on_input) işlevine bakın.

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- move left
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- move right
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Girdi odağı ve koleksiyon vekili bileşenleri

Bir koleksiyon vekili (collection proxy) aracılığıyla dinamik olarak yüklenen her oyun dünyasının kendi girdi yığını vardır. Eylem dağıtımının yüklenen dünyanın girdi yığınına ulaşması için vekil bileşenin ana dünyanın girdi yığınında bulunması gerekir. Dağıtım ana yığında aşağıya doğru devam etmeden önce, yüklenen dünyanın yığınındaki tüm bileşenler ele alınır:

![Eylemlerin vekillere dağıtımı](images/input/proxy.png)

::: important
Koleksiyon vekili bileşenini barındıran oyun nesnesine `acquire_input_focus` göndermeyi unutmak yaygın bir hatadır. Bu adımın atlanması, girdinin yüklenen dünyanın girdi yığınındaki herhangi bir bileşene ulaşmasını engeller.
:::


### Girdiyi bırakma

Girdi eylemlerini dinlemeyi durdurmak için oyun nesnesine bir `release_input_focus` iletisi gönderin. Bu ileti, oyun nesnesinin girdi yığınında bulunan tüm bileşenlerini yığından çıkarır:

```lua
-- tell the current game object (".") to release input focus.
msg.post(".", "release_input_focus")
```


## Girdiyi tüketme

Bir bileşenin `on_input()` işlevi, eylemlerin yığında daha aşağıya aktarılıp aktarılmayacağını etkin olarak denetleyebilir:

- `on_input()` işlevi `false` döndürürse veya bir dönüş değeri belirtilmezse (bu durumda Lua'da yanlış olarak değerlendirilen `nil` değeri döndürülür) girdi eylemleri, girdi yığınındaki bir sonraki bileşene aktarılır.
- `on_input()` işlevi `true` döndürürse girdi tüketilir. Girdi yığınının daha aşağısındaki hiçbir bileşen bu girdiyi almaz. Bunun *tüm* girdi yığınları için geçerli olduğunu unutmayın. Bir vekil aracılığıyla yüklenen dünyanın yığınındaki bir bileşen, girdiyi tüketerek ana yığındaki bileşenlerin girdi almasını engelleyebilir:

![Girdiyi tüketme](images/input/consuming.png)

Girdiyi tüketmenin, girdiyi oyunun farklı bölümleri arasında yönlendirmek için basit ve güçlü bir yol sunduğu birçok kullanım durumu vardır. Örneğin, geçici olarak oyunun girdi dinleyen tek bölümü olacak bir açılır menüye ihtiyacınız olduğunu düşünün:

![Girdiyi tüketme](images/input/game.png)

Duraklatma menüsü başlangıçta gizlidir (devre dışıdır) ve oyuncu oyun içi bilgi göstergesindeki (HUD) `PAUSE` öğesine dokunduğunda etkinleştirilir:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- Did the player press PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Tell the pause menu to take over.
            msg.post("pause_menu", "show")
        end
    end
end
```

![Duraklatma menüsü](images/input/game_paused.png)

Duraklatma menüsünün GUI bileşeni girdi odağı edinir ve girdiyi tüketerek açılır menüyle ilgili girdiler dışındaki tüm girdileri engeller:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Show the pause menu.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Acquire input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- do things...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Hide the pause menu
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Release input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume all input. Anything below us on the input stack
  -- will never see input until we release input focus.
  return true
end
```
