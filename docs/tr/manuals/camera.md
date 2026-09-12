---
title: Kamera bileşeni kılavuzu
brief: Bu kılavuz, Defold kamera bileşeninin işlevlerini açıklar.
---

# Kameralar

Defold'da kamera, oyun dünyasının görüntü alanını (viewport) ve izdüşümünü (projection) değiştiren bir bileşendir (component). Kamera bileşeni, görüntü oluşturma sürecini yöneten işleme betiğine (render script) bir görünüm matrisi ve bir izdüşüm matrisi sağlayan temel bir perspektif veya ortografik kamera tanımlar.

Perspektif kamera genellikle 3B oyunlarda kullanılır. Bu oyunlarda kameranın görünümü ile nesnelerin boyutu ve perspektifi; görüş hacmine (view frustum), kameradan oyun içindeki nesnelere olan uzaklığa ve bakış açısına göre belirlenir.

2B oyunlarda sahnenin ortografik izdüşümle işlenmesi (rendering) sıklıkla tercih edilir. Bu durumda kameranın görünümünü artık bir görüş hacmi değil, bir kutu belirler. Ortografik izdüşüm, nesnelerin boyutunu uzaklıklarına göre değiştirmediği için gerçekçi değildir. 1000 birim uzaktaki bir nesne, kameranın hemen önündeki bir nesneyle aynı boyutta işlenir.

![izdüşümler](images/camera/projections.png)


## Kamera oluşturma

Kamera oluşturmak için bir oyun nesnesine (game object) <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Camera</kbd> seçeneğini seçin. Alternatif olarak, proje hiyerarşisinde bir bileşen dosyası oluşturup bu dosyayı oyun nesnesine ekleyebilirsiniz.

![kamera bileşeni oluşturma](images/camera/create.png)

Kamera bileşeni, kameranın *görüş hacmini* tanımlayan şu özelliklere sahiptir:

![kamera ayarları](images/camera/settings.png)

Id
: Bileşenin tanımlayıcısı

Aspect Ratio
: (**Yalnızca perspektif kamera**) - Görüş hacminin genişliğinin yüksekliğine oranı. 1.0, kare bir görünüm varsaydığınız anlamına gelir. 1.33, 1024x768 gibi 4:3 oranlı bir görünüm için uygundur. 1.78 ise 16:9 oranlı bir görünüm için uygundur. *Auto Aspect Ratio* etkinse bu ayar yok sayılır.

Fov
: (**Yalnızca perspektif kamera**) - Kameranın *dikey* görüş açısının (FOV) _radyan_ cinsinden değeri. Görüş açısı ne kadar geniş olursa kamera o kadar çok şey görür.

Near Z
: Yakın kırpma düzleminin Z değeri.

Far Z
: Uzak kırpma düzleminin Z değeri.

Auto Aspect Ratio
: (**Yalnızca perspektif kamera**) - Kameranın en boy oranını otomatik olarak hesaplaması için bu ayarı etkinleştirin.

Orthographic Projection
: Kamerayı ortografik izdüşüme geçirmek için bu ayarı etkinleştirin (aşağıya bakın).

Orthographic Zoom
: (**Yalnızca ortografik kamera**) - Kullanıcının belirlediği yakınlaştırma çarpanı (> 1 = yakınlaştırma, < 1 = uzaklaştırma). `Fixed` modunda bu, uygulanan yakınlaştırma değeridir. `Auto Fit` ve `Auto Cover` modlarında otomatik hesaplanan yakınlaştırma değeriyle çarpılır; böylece otomatik boyutlandırmayı devre dışı bırakmadan ek yakınlaştırma uygulanabilir.

Orthographic Mode
: (**Yalnızca ortografik kamera**) - Ortografik kameranın pencere boyutuna ve tasarım çözünürlüğünüze (`game.project` → `display.width/height` değerleri) göre yakınlaştırmayı nasıl belirlediğini denetler.
  - `Fixed` (sabit yakınlaştırma kullanır): Geçerli `Orthographic Zoom` değerini olduğu gibi kullanır.
  - `Auto Fit` (sığdırma): Tasarım alanının tamamının pencereye sığmasını sağlayacak yakınlaştırma değerini otomatik olarak hesaplar, ardından bunu `Orthographic Zoom` ile çarpar. Yanlarda veya üstte/altta ek içerik gösterebilir.
  - `Auto Cover` (kaplama): Tasarım alanının pencerenin tamamını kaplamasını sağlayacak yakınlaştırma değerini otomatik olarak hesaplar, ardından bunu `Orthographic Zoom` ile çarpar. Yanlardan veya üstten/alttan kırpabilir.
  Yalnızca `Orthographic Projection` etkinken kullanılabilir.


## Kamerayı kullanma

Tüm kameralar bir kare sırasında otomatik olarak etkinleştirilir ve güncellenir; Lua'nın `camera` modülü tüm betik bağlamlarında kullanılabilir. Defold 1.8.1 sürümünden itibaren kamera bileşenine `acquire_camera_focus` iletisi göndererek kamerayı açıkça etkinleştirmek artık gerekli değildir. Odağı edinmek ve bırakmak için kullanılan eski iletiler hâlâ kullanılabilir; ancak etkinleştirmek veya devre dışı bırakmak istediğiniz diğer bileşenlerde olduğu gibi `enable` ve `disable` iletilerini kullanmanız önerilir:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

O anda kullanılabilir olan tüm kameraları listelemek için `camera.get_cameras()` kullanabilirsiniz:

```lua
-- Note: The render calls are only available in a render script.
--       The camera.get_cameras() function can be used anywhere,
--       but render.set_camera can only be used in a render script.

for k,v in pairs(camera.get_cameras()) do
    -- the camera table contains the URLs of all cameras
    render.set_camera(v)
    -- do rendering here - anything rendered here that uses materials with
    -- view and projection matrices specified, will use matrices from the camera.
end
-- to disable a camera, pass in nil (or no arguments at all) to render.set_camera.
-- after this call, all render calls will use the view and projection matrices
-- that are specified on the render context (render.set_view and render.set_projection)
render.set_camera()
```

Betiklerde kullanılan `camera` modülü, kamerayı değiştirmek için kullanılabilecek çeşitli işlevler sunar. Aşağıda bunlardan yalnızca birkaçı gösterilmiştir; kullanılabilir tüm işlevleri görmek için [API belgelerindeki](/ref/camera/) kılavuza bakın).

```lua
camera.get_aspect_ratio(camera) -- get aspect ratio
camera.get_far_z(camera) -- get far z
camera.get_fov(camera) -- get field of view
camera.get_orthographic_mode(camera) -- get orthographic mode (one of camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- get the user-controlled zoom multiplier
camera.get_orthographic_auto_zoom(camera) -- get the automatically calculated zoom
camera.set_aspect_ratio(camera, ratio) -- set aspect ratio
camera.set_far_z(camera, far_z) -- set far z
camera.set_near_z(camera, near_z) -- set near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- set orthographic mode
... And so forth
```

Kamera, bileşenin tam sahne yolu olan bir URL ile tanımlanır. Bu yol; koleksiyonu (collection), bileşenin ait olduğu oyun nesnesini ve bileşenin tanımlayıcısını içerir. Bu örnekte, kamera bileşenini aynı koleksiyon içinden tanımlamak için `/go#camera` URL adresini, farklı bir koleksiyondan veya işleme betiğinden kameraya erişirken ise `main:/go#camera` adresini kullanırsınız.

![kamera bileşeni oluşturma](images/camera/create.png)

```lua
-- Accessing a camera from a script in the same collection:
camera.get_fov("/go#camera")

-- Accessing a camera from a script in a different collection:
camera.get_fov("main:/go#camera")

-- Accessing a camera from the render script:
render.set_camera("main:/go#camera")
```

Her karede, o anda kamera odağına sahip olan kamera bileşeni `@render` soketine bir `set_view_projection` iletisi gönderir:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Kamera bileşeninden gönderilen ileti bir görünüm matrisi ve bir izdüşüm matrisi içerir.

Kamera bileşeni, kameranın *Orthographic Projection* özelliğine bağlı olarak işleme betiğine perspektif veya ortografik bir izdüşüm matrisi sağlar. İzdüşüm matrisi ayrıca tanımlanan yakın ve uzak kırpma düzlemlerini, kameranın görüş açısını ve en boy oranı ayarlarını da hesaba katar.

Kameranın sağladığı görünüm matrisi, kameranın konumunu ve yönelimini tanımlar. *Orthographic Projection* kullanan bir kamera, görünümü bağlı olduğu oyun nesnesinin konumuna ortalar; *Perspective Projection* kullanan bir kamerada ise görünümün sol alt köşesi, bağlı olduğu oyun nesnesinin konumunda yer alır.


### İşleme betiği

Varsayılan işleme betiği kullanıldığında Defold, işleme için kullanılacak kamera olarak en son etkinleştirilen kamerayı otomatik olarak ayarlar. Bu değişiklikten önce, kamera bileşenlerinden gelen görünüm ve izdüşümün kullanılması gerektiğini işleyiciye bildirmek için projedeki bir betiğin açıkça `use_camera_projection` iletisini göndermesi gerekiyordu. Bu artık gerekli değildir, ancak geriye dönük uyumluluk için hâlâ yapılabilir.

Alternatif olarak, bir işleme betiğinde işleme için kullanılacak belirli bir kamera ayarlayabilirsiniz. Bu, örneğin çok oyunculu bir oyunda, işleme için hangi kameranın kullanılacağını daha ayrıntılı denetlemeniz gereken durumlarda yararlı olabilir.

```lua
-- render.set_camera will automatically use the view and projection matrices
-- for any rendering happening until render.set_camera() is called.
render.set_camera("main:/my_go#camera")
```

Bir kameranın etkin olup olmadığını denetlemek için [Kamera API'sindeki](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera) `get_enabled` işlevini kullanabilirsiniz:

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- camera is enabled, use it for rendering!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
`set_camera` işlevini görüş hacmi dışında kalanları eleme (frustum culling) ile birlikte kullanmak için bunu işleve bir seçenek olarak iletmeniz gerekir:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Kamerayı kaydırma

Kamera bileşeninin bağlı olduğu oyun nesnesini hareket ettirerek kamerayı oyun dünyasında kaydırabilir/hareket ettirebilirsiniz. Kamera bileşeni, kameranın x ve y eksenlerindeki geçerli konumuna göre güncellenmiş bir görünüm matrisini otomatik olarak gönderir.

### Kamerayla yakınlaştırma ve uzaklaştırma

Perspektif kamera kullanırken, kameranın bağlı olduğu oyun nesnesini z ekseni boyunca hareket ettirerek yakınlaştırma ve uzaklaştırma yapabilirsiniz. Kamera bileşeni, kameranın geçerli z konumuna göre güncellenmiş bir görünüm matrisini otomatik olarak gönderir.

Ortografik kamera kullanırken, kameranın *Orthographic Zoom* özelliğini düzenleyicide veya çalışma sırasında değiştirerek yakınlaştırma ve uzaklaştırma yapabilirsiniz:

```lua
-- In Fixed mode, this is the effective zoom.
go.set("#camera", "orthographic_zoom", 2)
```

`Auto Fit` ve `Auto Cover` modlarında *Orthographic Zoom*, otomatik hesaplanan yakınlaştırma değerinin üzerine uygulanır; yok sayılmaz. Örneğin, tasarım alanını pencereye sığdırıp ardından ek %25 yakınlaştırma uygulamak için düzenleyicide *Orthographic Mode* değerini `Auto Fit`, *Orthographic Zoom* değerini ise `1.25` olarak ayarlayın. Çalışma sırasında aynı ayarları yapmak için:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()`, `Auto Fit` ve `Auto Cover` modlarında geçerli pencere ve proje boyutlarından hesaplanan yakınlaştırma değerini döndürür. `Fixed` modunda `1.0` döndürür. Aynı değere, salt okunur `orthographic_auto_zoom` bileşen özelliği üzerinden de erişilebilir:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Ortografik kamera kullanırken yakınlaştırmanın nasıl belirleneceğini `Orthographic Mode` ayarıyla veya betik aracılığıyla da değiştirebilirsiniz:

```lua
-- get current mode (one of camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- switch to auto-fit (contain) to always keep the full design area visible
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- switch to auto-cover to ensure the design area covers the window
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- switch to fixed mode to use orthographic_zoom without automatic sizing
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Uyarlanabilir yakınlaştırma

Uyarlanabilir yakınlaştırmanın temelinde, ekran çözünürlüğü *game.project* dosyasında ayarlanan başlangıç çözünürlüğünden farklılaştığında kameranın yakınlaştırma değerini ayarlamak yatar.

Uyarlanabilir yakınlaştırmada yaygın olarak kullanılan iki yaklaşım vardır:

1. En yüksek yakınlaştırma - *game.project* dosyasındaki başlangıç çözünürlüğünün kapsadığı içeriğin ekranı doldurup ekran sınırlarının dışına taşmasını sağlayan bir yakınlaştırma değeri hesaplayın. Bu, yanlarda veya üstte ve altta bazı içerikleri gizleyebilir.
2. En düşük yakınlaştırma - *game.project* dosyasındaki başlangıç çözünürlüğünün kapsadığı içeriğin tamamen ekran sınırları içinde kalmasını sağlayan bir yakınlaştırma değeri hesaplayın. Bu, yanlarda veya üstte ve altta ek içerik gösterebilir.

Örnek:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: ensure that the initial design dimensions will fill and expand beyond the screen bounds
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: ensure that the initial design dimensions will shrink and be contained within the screen bounds
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Uyarlanabilir yakınlaştırmanın eksiksiz bir örneğini [bu örnek projede](https://github.com/defold/sample-adaptive-zoom) görebilirsiniz.

Not: Ortografik kamera kullanırken artık `Orthographic Mode` değerini `Auto Fit` (sığdırma) veya `Auto Cover` (kaplama) olarak ayarlayarak özel kod yazmadan sığdırma/kaplama davranışını elde edebilirsiniz. Bu modlarda, pencere boyutu ve tasarım çözünürlüğünden hesaplanan yakınlaştırma değeri `Orthographic Zoom` ile çarpılır.


### Bir oyun nesnesini takip etme

Kamera bileşeninin bağlı olduğu oyun nesnesini, takip edilecek oyun nesnesinin alt nesnesi olarak ayarlayarak kameranın bu oyun nesnesini takip etmesini sağlayabilirsiniz:

![oyun nesnesini takip etme](images/camera/follow.png)

Alternatif olarak, takip edilecek oyun nesnesi hareket ettikçe kamera bileşeninin bağlı olduğu oyun nesnesinin konumunu her karede güncelleyebilirsiniz.

### Ekran ve dünya koordinatları arasında dönüştürme {#converting-mouse-to-world-coordinates}

Kamera kaydırıldığında, yakınlaştırma veya uzaklaştırma yapıldığında ya da izdüşümü değiştirildiğinde, girdi koordinatları artık dünya koordinatlarıyla doğrudan eşleşmez. Kamera dönüştürme işlevlerini `action.screen_x` ve `action.screen_y` ile kullanın. İsteğe bağlı kamera URL adresi belirtilmezse en son etkinleştirilen kamera kullanılır.

Ortografik bir kamerada [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]), bir ekran pikseli için kameranın yakın düzlemindeki noktayı dünya uzayında döndürür:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Perspektif bir kamerada [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]), Z bileşeni kamera düzleminden dünya birimleriyle ölçülen görünüm derinliği olan bir `vector3` alır:

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) ters dönüşümü gerçekleştirir. Ekran pikseli cinsinden X ve Y değerlerini, Z bileşeninde ise aynı kurala göre belirlenen görünüm derinliğini döndürür; böylece sonucu tekrar `camera.screen_to_world()` işlevine iletilebilir:

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Koordinat dönüşümünü çalışırken görmek için [Örnekler sayfasını](https://defold.com/examples/render/screen_to_world/) ziyaret edin. Aynı API'leri gösteren bir [örnek proje](https://github.com/defold/sample-screen-to-world-coordinates/) de vardır.

::: sidenote
[Bu kılavuzda sözü edilen üçüncü taraf kamera çözümleri](/manuals/camera/#third-party-camera-solutions), ekran koordinatlarına ve ekran koordinatlarından dönüştürme işlevleri sağlar.
:::

## Çalışma sırasında değiştirme
Çeşitli iletiler ve özellikler aracılığıyla kameraları çalışma sırasında değiştirebilirsiniz ([kullanım için API belgelerine](/ref/camera/) bakın).

Kameranın, `go.get()` ve `go.set()` kullanılarak değiştirilebilen çeşitli özellikleri vardır:

`fov`
: Kameranın görüş açısı (`number`).

`near_z`
: Kameranın yakın Z değeri (`number`).

`far_z`
: Kameranın uzak Z değeri (`number`).

`orthographic_zoom`
: Kullanıcının belirlediği ortografik kamera yakınlaştırma çarpanı. `Auto Fit` ve `Auto Cover` modlarında `orthographic_auto_zoom` ile çarpılır. (`number`).

`orthographic_auto_zoom`
: `Auto Fit` ve `Auto Cover` modları için hesaplanan ortografik yakınlaştırma değeri; `Fixed` modunda ise `1.0`. SALT OKUNUR. (`number`).

`aspect_ratio`
: Görüş hacminin genişliğinin yüksekliğine oranı. Perspektif kameranın izdüşümü hesaplanırken kullanılır. (`number`).

`view`
: Kameranın hesaplanan görünüm matrisi. SALT OKUNUR. (`matrix4`).

`projection`
: Kameranın hesaplanan izdüşüm matrisi. SALT OKUNUR. (`matrix4`).


## Üçüncü taraf kamera çözümleri {#third-party-camera-solutions}

Topluluk tarafından geliştirilen kamera çözümleri; ekran sarsıntısı, oyun nesnelerini takip etme, ekran koordinatlarını dünya koordinatlarına dönüştürme gibi yaygın özellikler ve çok daha fazlasını sunar. Bunları Defold varlık portalından indirebilirsiniz:

- Björn Ritzl tarafından geliştirilen [Orthographic camera](https://defold.com/assets/orthographic/) (yalnızca 2B).
- Klayton Kowalski tarafından geliştirilen [Defold Rendy](https://defold.com/assets/defold-rendy/) (2B ve 3B).
