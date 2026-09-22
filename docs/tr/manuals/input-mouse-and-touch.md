---
title: Defold'da fare ve dokunma girdisi
brief: Bu kılavuz fare ve dokunma girdisinin nasıl çalıştığını açıklar.
---

::: sidenote
Defold'da girdinin (input) genel olarak nasıl çalıştığını, girdinin nasıl alındığını ve betik dosyalarınızın girdiyi hangi sırayla aldığını öğrenmeniz önerilir. Girdi sistemi hakkında daha fazla bilgi için [Girdiye genel bakış kılavuzuna](/manuals/input) bakın.
:::

# Fare tetikleyicileri
Fare tetikleyicileri (mouse triggers), fare düğmelerinden ve tekerleklerinden gelen girdiyi oyun eylemlerine bağlamanızı sağlar.

![](images/input/mouse_bindings.png)

::: sidenote
`MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` ve `MOUSE_BUTTON_MIDDLE` fare düğmesi girdileri, sırasıyla `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` ve `MOUSE_BUTTON_3` ile eşdeğerdir.
:::

::: important
Aşağıdaki örnekler, yukarıdaki görüntüde gösterilen eylemleri kullanır. Tüm girdilerde olduğu gibi, girdi eylemlerinize (input action) istediğiniz adı verebilirsiniz.
:::

## Fare düğmeleri
Fare düğmeleri `pressed`, `released` ve `repeated` olayları üretir. Aşağıdaki örnek, sol fare düğmesinin girdisinin (basılma veya bırakılma) nasıl algılandığını gösterir:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- left mouse button pressed
        elseif action.released then
            -- left mouse button released
        end
    end
end
```

::: important
`MOUSE_BUTTON_LEFT` (veya `MOUSE_BUTTON_1`) girdi eylemleri, tekli dokunma girdileri için de gönderilir.
:::

## Fare tekerleği
Fare tekerleği girdileri kaydırma eylemlerini algılar. Tekerlek döndürüldüğünde `action.value` alanı `1`, aksi durumda `0` olur. (Kaydırma eylemleri, düğmeye basma gibi işlenir. Defold şu anda dokunmatik yüzeylerde hassas kaydırma girdisini desteklemez.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- mouse wheel is scrolled up
        end
    end
end
```

## Fare hareketi
Fare hareketi ayrı olarak işlenir. Girdi eşlemelerinizde (input binding) en az bir fare tetikleyicisi ayarlanmadıkça fare hareketi olayları alınmaz.

Fare hareketi girdi eşlemelerinde bir eyleme bağlanmaz; bunun yerine `action_id` değeri `nil` olarak ayarlanır ve `action` tablosu farenin konumu ve konumundaki değişimle doldurulur.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- let game object follow mouse/touch movement
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Dokunma tetikleyicileri
Tekli dokunma (single-touch) ve çoklu dokunma (multi-touch) türündeki tetikleyiciler, iOS ve Android cihazlarda hem yerel uygulamalarda hem de HTML5 dağıtım paketlerinde kullanılabilir.

![](images/input/touch_bindings.png)

## Tekli dokunma
Tekli dokunma türündeki tetikleyiciler, girdi eşlemelerinin Touch Triggers bölümünden ayarlanmaz. Bunun yerine **`MOUSE_BUTTON_LEFT` veya `MOUSE_BUTTON_1` için fare düğmesi girdisini ayarladığınızda tekli dokunma tetikleyicileri otomatik olarak ayarlanır**.

## Çoklu dokunma
Çoklu dokunma türündeki tetikleyiciler, eylem tablosunun içindeki `touch` adlı tabloyu doldurur. Tablonun elemanları `1`--`N` aralığındaki tam sayılarla indekslenir; burada `N`, dokunma noktalarının sayısıdır. Tablodaki her eleman girdi verileri içeren alanlar barındırır:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Spawn at each touch point
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Çoklu dokunmaya, `MOUSE_BUTTON_LEFT` veya `MOUSE_BUTTON_1` fare düğmesi girdisiyle aynı eylem atanmamalıdır. Aynı eylemi atamak, tekli dokunmanın yerini alır ve herhangi bir tekli dokunma olayı almanızı engeller.
:::

::: sidenote
[Defold-Input varlığı](https://defold.com/assets/defoldinput/), çoklu dokunma desteğine sahip düğmeler ve analog çubuklar gibi sanal ekran kontrollerini kolayca oluşturmak için kullanılabilir.
:::


## Nesnelere tıklamayı veya dokunmayı algılama
Kullanıcının görsel bir bileşene (component) ne zaman tıkladığını veya dokunduğunu algılamak, birçok oyunda ihtiyaç duyulan çok yaygın bir işlemdir. Bu, kullanıcının bir düğmeyle veya başka bir kullanıcı arayüzü (UI) öğesiyle etkileşimi olabilir. Strateji oyununda oyuncunun yönettiği bir birim, zindan keşif oyununda bir bölümdeki hazine veya rol yapma oyununda (RPG) görev veren bir karakter gibi bir oyun nesnesiyle (game object) etkileşim de olabilir. Kullanılacak yaklaşım, görsel bileşenin türüne göre değişir.

### GUI düğümleriyle etkileşimi algılama
Kullanıcı arayüzü öğeleri için `gui.pick_node(node, x, y)` işlevi bulunur. Bu işlev, belirtilen koordinatın bir GUI düğümünün (GUI node) sınırları içinde olup olmamasına göre `true` veya `false` döndürür. Daha fazla bilgi için [API belgelerine](/ref/gui/#gui.pick_node:node-x-y), [işaretçinin öğe üzerinde olmasını algılama örneğine](/examples/gui/pointer_over/) veya [düğme örneğine](/examples/gui/button/) bakın.

### Oyun nesneleriyle etkileşimi algılama
Kamera ötelemesi ve işleme betiğinin (render script) izdüşümü gibi etkenler gerekli hesaplamaları etkilediğinden, oyun nesneleriyle etkileşimi algılamak daha karmaşıktır. Oyun nesneleriyle etkileşimi algılamak için iki genel yaklaşım vardır:

  1. Kullanıcının etkileşim kurabileceği oyun nesnelerinin konumunu ve boyutunu takip edin ve fare ya da dokunma koordinatının bu nesnelerden herhangi birinin sınırları içinde olup olmadığını kontrol edin.
  2. Kullanıcının etkileşim kurabileceği oyun nesnelerine çarpışma nesneleri (collision object) ekleyin. Fareyi veya parmağı takip eden bir çarpışma nesnesi de ekleyin ve aralarında çarpışma olup olmadığını kontrol edin.

::: sidenote
Çarpışma nesneleriyle kullanıcı girdisini algılamak için sürükleme ve tıklama desteğine sahip, kullanıma hazır bir çözümü [Defold-Input varlığında](https://defold.com/assets/defoldinput/) bulabilirsiniz.
:::

Her iki durumda da fare veya dokunma olayının ekran uzayı (screen space) koordinatları ile oyun nesnelerinin dünya uzayı (world space) koordinatları arasında dönüşüm yapmak gerekir. Bunu birkaç farklı yolla yapabilirsiniz:

  * İşleme betiğinin kullandığı görünümü ve izdüşümü elle takip edin ve bunları dünya uzayına ve dünya uzayından dönüşüm yapmak için kullanın. [Kamera kılavuzunda bunun bir örneğini bulabilirsiniz](/manuals/camera/#converting-mouse-to-world-coordinates).
  * [Üçüncü taraf bir kamera çözümü](/manuals/camera/#third-party-camera-solutions) kullanın ve sunduğu ekran uzayından dünya uzayına dönüşüm işlevlerinden yararlanın.
