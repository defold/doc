---
title: Defold'da işleme hattı
brief: Bu kılavuz, Defold'un işleme hattının nasıl çalıştığını ve nasıl programlanabileceğini açıklar.
---

# İşleme

Motorun ekranda gösterdiği tüm nesneler (sprite bileşenleri, modeller, karolar, parçacıklar veya GUI düğümleri) bir işleyici (renderer) tarafından çizilir. İşleyicinin merkezinde işleme hattını (render pipeline) yöneten bir işleme betiği (render script) bulunur. Varsayılan olarak her 2B nesne, belirtilen harmanlama ile doğru bit eşlem kullanılarak ve doğru Z derinliğinde çizilir---bu nedenle sıralama ve basit harmanlama dışında işleme (rendering), yani görüntü oluşturma hakkında hiç düşünmeniz gerekmeyebilir. Çoğu 2B oyun için varsayılan hat iyi çalışır, ancak oyununuzun özel gereksinimleri olabilir. Bu durumda Defold, gereksinimlerinize özel bir işleme hattı yazmanıza olanak tanır.

### İşleme hattı - Ne, ne zaman ve nerede?

İşleme hattı neyin, ne zaman ve nerede işleneceğini denetler. Neyin işleneceği [işleme yüklemleri](#render-predicates) (render predicates) ile denetlenir. Bir yüklemin ne zaman işleneceği [işleme betiğinde](#the-render-script), nerede işleneceği ise [görünüm izdüşümü](#default-view-projection) ile denetlenir. İşleme hattı, bir işleme yükleminin çizdiği grafiklerden tanımlı bir sınırlayıcı kutunun veya görüş hacminin (frustum) dışında kalanları da eleyebilir. Bu işleme görüş hacmi dışında kalanları eleme (frustum culling) denir.


## Varsayılan işleme

İşleme dosyası, geçerli işleme betiğine bir başvurunun yanı sıra işleme betiğinde kullanılabilir olması gereken özel materyalleri (material) içerir ([`render.enable_material()`](/ref/render/#render.enable_material) ile kullanın)

İşleme hattının merkezinde _işleme betiği_ bulunur. Bu, `init()`, `update()` ve `on_message()` işlevlerini içeren bir Lua betiğidir ve öncelikle altta yatan grafik API'siyle etkileşim kurmak için kullanılır. İşleme betiğinin oyununuzun yaşam döngüsünde özel bir yeri vardır. Ayrıntıları [Uygulama yaşam döngüsü belgesinde](/manuals/application-lifecycle) bulabilirsiniz.

Projelerinizin "Builtins" klasöründe varsayılan işleme kaynağını ("default.render") ve varsayılan işleme betiğini ("default.render_script") bulabilirsiniz.

![Yerleşik işleme](images/render/builtin.png)

Özel bir işleyici hazırlamak için:

1. "default.render" ve "default.render_script" dosyalarını proje hiyerarşinizde bir konuma kopyalayın. Elbette sıfırdan bir işleme betiği oluşturabilirsiniz; ancak özellikle Defold'a ve/veya grafik programlamaya yeni başlıyorsanız varsayılan betiğin bir kopyasıyla başlamanız iyi olur.

2. "default.render" dosyasının kopyasını düzenleyin ve *Script* özelliğini, işleme betiğinizin kopyasına başvuracak şekilde değiştirin.

3. *game.project* ayar dosyasındaki (*bootstrap* altında bulunan) *Render* özelliğini, "default.render" dosyasının kopyasına başvuracak şekilde değiştirin.


## İşleme yüklemleri {#render-predicates}

Nesnelerin çizim sırasını denetleyebilmek için işleme _yüklemleri_ oluşturursunuz. Bir yüklem, seçilen materyal _etiketlerine_ göre neyin çizileceğini bildirir.

Ekrana çizilen her nesneye, nesnenin ekrana nasıl çizileceğini denetleyen bir materyal bağlıdır. Materyalde, materyalle ilişkilendirilecek bir veya daha fazla _etiket_ belirtirsiniz.

Ardından işleme betiğinizde bir *işleme yüklemi* oluşturabilir ve bu yükleme hangi etiketlerin ait olacağını belirtebilirsiniz. Motora yüklemi çizmesini söylediğinizde, materyali bu yüklem için belirtilen etiketlerin tamamını içeren her nesne çizilir.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


Materyallerin nasıl çalıştığına ilişkin ayrıntılı açıklamayı [Materyal belgesinde](/manuals/material) bulabilirsiniz.


## Varsayılan görünüm izdüşümü {#default-view-projection}

Varsayılan işleme betiği, 2B oyunlara uygun bir ortografik izdüşüm (orthographic projection) kullanacak şekilde yapılandırılmıştır. Üç farklı ortografik izdüşüm sunar: `Stretch` (varsayılan), `Fixed Fit` ve `Fixed`. Varsayılan işleme betiğindeki ortografik izdüşümlere alternatif olarak, bir kamera bileşeninin (camera component) sağladığı izdüşüm matrisini kullanma seçeneğiniz de vardır.

### Esnetme izdüşümü

Esnetme izdüşümü, pencere yeniden boyutlandırıldığında bile her zaman oyununuzun *game.project* dosyasında ayarlanan boyutlara eşit bir alanını çizer. En boy oranı değişirse oyun içeriği dikey veya yatay olarak esnetilir:

![Esnetme izdüşümü](images/render/stretch_projection.png)

*Özgün pencere boyutuyla esnetme izdüşümü*

![Yeniden boyutlandırıldığında esnetme izdüşümü](images/render/stretch_projection_resized.png)

*Pencere yatay olarak esnetildiğinde esnetme izdüşümü*

Esnetme izdüşümü varsayılan izdüşümdür; ancak başka bir izdüşüme geçtiyseniz ve geri dönmeniz gerekiyorsa bunu işleme betiğine bir ileti (message) göndererek yapabilirsiniz:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Sabit sığdırma izdüşümü

Esnetme izdüşümü gibi sabit sığdırma izdüşümü de her zaman oyunun *game.project* dosyasında ayarlanan boyutlara eşit bir alanını gösterir; ancak pencere yeniden boyutlandırılır ve en boy oranı değişirse oyun içeriği özgün en boy oranını korur ve dikey veya yatay yönde daha fazla oyun içeriği gösterilir:

![Sabit sığdırma izdüşümü](images/render/fixed_fit_projection.png)

*Özgün pencere boyutuyla sabit sığdırma izdüşümü*

![Yeniden boyutlandırıldığında sabit sığdırma izdüşümü](images/render/fixed_fit_projection_resized.png)

*Pencere yatay olarak esnetildiğinde sabit sığdırma izdüşümü*

![Küçültüldüğünde sabit sığdırma izdüşümü](images/render/fixed_fit_projection_resized_smaller.png)

*Pencere özgün boyutunun %50'sine küçültüldüğünde sabit sığdırma izdüşümü*

Sabit sığdırma izdüşümünü işleme betiğine bir ileti göndererek etkinleştirebilirsiniz:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Sabit izdüşüm {#fixed-projection}

Sabit izdüşüm, özgün en boy oranını korur ve oyun içeriğinizi sabit bir yakınlaştırma düzeyiyle işler. Bu, yakınlaştırma düzeyi %100'den farklı bir değere ayarlanırsa oyunun *game.project* dosyasındaki boyutlarla tanımlanan alanından daha fazlasının veya daha azının gösterileceği anlamına gelir:

![Sabit izdüşüm](images/render/fixed_projection_zoom_2_0.png)

*Yakınlaştırma 2 olarak ayarlandığında sabit izdüşüm*

![Sabit izdüşüm](images/render/fixed_projection_zoom_0_5.png)

*Yakınlaştırma 0,5 olarak ayarlandığında sabit izdüşüm*

![Sabit izdüşüm](images/render/fixed_projection_zoom_2_0_resized.png)

*Yakınlaştırma 2 olarak ayarlandığında ve pencere özgün boyutunun %50'sine küçültüldüğünde sabit izdüşüm*

Sabit izdüşümü işleme betiğine bir ileti göndererek etkinleştirebilirsiniz:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Kamera izdüşümü

Varsayılan işleme betiği kullanılırken projede etkin [kamera bileşenleri](/manuals/camera) varsa, bunlar işleme betiğinde ayarlanan diğer tüm görünüm / izdüşümlere göre önceliklidir. İşleme betiklerinde kamera bileşenleriyle nasıl çalışılacağı hakkında daha fazla bilgi için [Kamera belgesine](/manuals/camera) bakın.

Ortografik kameralar, kameranın pencereye nasıl uyum sağlayacağını denetleyen bir `Orthographic Mode` ayarını destekler:
- `Fixed`, kameranın `Orthographic Zoom` değerini kullanır.
- `Auto Fit` (sığdırma), tasarım alanının tamamını görünür tutar.
- `Auto Cover` (kaplama), pencereyi doldurur ve kırpma yapabilir.

Modlar arasında düzenleyicide veya çalışma sırasında Camera API'si aracılığıyla geçiş yapabilirsiniz:

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Görüş hacmi dışında kalanları eleme {#frustum-culling}

Defold'un işleme API'si, geliştiricilerin görüş hacmi dışında kalanları eleme adı verilen işlemi gerçekleştirmesine olanak tanır. Görüş hacmi dışında kalanları eleme etkinleştirildiğinde, tanımlı bir sınırlayıcı kutunun veya görüş hacminin dışında kalan grafikler yok sayılır. Aynı anda yalnızca bir bölümü görülebilen büyük bir oyun dünyasında, görüş hacmi dışında kalanları eleme, işleme için GPU'ya gönderilmesi gereken veri miktarını önemli ölçüde azaltabilir; böylece performansı artırır ve (mobil cihazlarda) pil tasarrufu sağlar. Sınırlayıcı kutuyu oluşturmak için kameranın görünümünü ve izdüşümünü kullanmak yaygındır. Varsayılan işleme betiği, bir görüş hacmi hesaplamak için (kameradan gelen) görünümü ve izdüşümü kullanır.

`render.draw()` işlevine `frustum` seçeneğinde bir görünüm-izdüşüm matrisi geçirerek bir çizim çağrısı için görüş hacmi dışında kalanları elemeyi etkinleştirin:

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Bir kamera bileşeniyle işleme yaparken `render.set_camera()`, sonraki çizim çağrıları için kameranın görünüm-izdüşüm matrisini otomatik olarak kullanabilir:

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

Bu yöntemlerden biri kullanıldığında parçacık efekti yayıcıları kendi sınırlarına göre elenir.

Görüş hacmi dışında kalanları eleme, motorda her bileşen türü için ayrı uygulanır. Geçerli durum:

| Bileşen     | Destekleniyor |
|-------------|-----------|
| Sprite      | EVET      |
| Model       | EVET      |
| Örgü        | EVET (1)  |
| Etiket      | EVET      |
| Spine       | EVET      |
| Parçacık efekti | EVET   |
| Karo haritası | EVET    |
| Rive        | HAYIR     |

1 = Örgünün sınırlayıcı kutusunun geliştirici tarafından ayarlanması gerekir. [Daha fazla bilgi](/manuals/mesh/#frustum-culling).


::: sidenote
Defold 1.13.0'dan itibaren bileşenlerin temel geometrik şekilleri (primitive), köşelerin saat yönünün tersine sıralanmasını (vertex winding) kullanır ve şeklin normali kameraya doğru bakar. Sprite bileşenleri, GUI düğümleri, karo haritaları (karo ızgaraları) ve parçacık efektleri diğer bileşen türleriyle aynı sıralamayı kullanır; böylece tüm bileşenler için aynı yüz eleme ayarları kullanılabilir.

Bu durum, model dışındaki bileşenler için yüz eleme ayarlayan projeleri etkileyebilir. Bir bileşen beklenmedik şekilde elenirse, `render.set_cull_face(graphics.FACE_TYPE_BACK)` ile arka yüzlerin seçildiğinden emin olun veya varsayılan `graphics.FACE_TYPE_BACK` modunu kullanmak için `render.set_cull_face()` çağrısını kaldırın.
:::

## Koordinat sistemleri

Bileşenlerin işlenmesinden söz ederken genellikle hangi koordinat sisteminde işlendikleri belirtilir. Çoğu oyunda bazı bileşenler dünya uzayında (world space), bazıları ise ekran uzayında (screen space) çizilir.

GUI bileşenleri ve bunların düğümleri genellikle ekran uzayı koordinatlarında çizilir; ekranın sol alt köşesinin koordinatı (0,0), sağ üst köşesininki ise (ekran genişliği, ekran yüksekliği) olur. Ekran uzayı koordinat sistemi, bir kamera tarafından hiçbir zaman kaydırılmaz veya başka bir şekilde ötelenmez. Böylece dünya nasıl işlenirse işlensin GUI düğümleri her zaman ekranda çizilir.

Oyun dünyanızdaki oyun nesnelerinin (game object) kullandığı sprite bileşenleri, karo haritaları ve diğer bileşenler genellikle dünya uzayı koordinat sisteminde çizilir. İşleme betiğinizde hiçbir değişiklik yapmaz ve görünüm izdüşümünü değiştirmek için kamera bileşeni kullanmazsanız bu koordinat sistemi ekran uzayı koordinat sistemiyle aynıdır; ancak bir kamera ekleyip onu hareket ettirdiğiniz veya görünüm izdüşümünü değiştirdiğiniz anda iki koordinat sistemi farklılaşır. Kamera hareket ederken dünyanın diğer bölümlerinin işlenmesi için ekranın sol alt köşesi (0, 0) konumundan kaydırılır. İzdüşüm değişirse koordinatlar hem ötelenir (yani 0, 0 konumundan kaydırılır) hem de bir ölçek katsayısıyla değiştirilir.


## İşleme betiği {#the-render-script}

Aşağıda, yerleşik betiğin biraz değiştirilmiş bir sürümü olan özel bir işleme betiğinin kodu yer alır.

init()
: `init()` işlevi, yüklemleri, görünümü ve temizleme rengini ayarlamak için kullanılır. Bu değişkenler asıl işleme sırasında kullanılır.

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: `update()` işlevi her karede bir kez çağrılır. Görevi, altta yatan OpenGL ES API'lerini (OpenGL Embedded Systems API) çağırarak asıl çizimi gerçekleştirmektir. `update()` işlevinde neler olduğunu doğru anlamak için OpenGL'in nasıl çalıştığını anlamanız gerekir. OpenGL ES hakkında birçok iyi kaynak bulunur. Resmî site iyi bir başlangıç noktasıdır. Siteye https://www.khronos.org/opengles/ adresinden ulaşabilirsiniz.

  Bu örnek, 3B modelleri çizmek için gereken hazırlığı içerir. `init()` işlevi bir `self.predicates.model` yüklemi tanımlamıştır. Başka bir yerde "model" etiketine sahip bir materyal oluşturulmuştur. Bu materyali kullanan bazı model bileşenleri de vardır:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Buraya kadar betik basit ve anlaşılır bir işleme betiğidir. Her karede aynı şekilde çizim yapar. Ancak bazen işleme betiğine durum bilgisi eklemek ve bu duruma bağlı olarak farklı işlemler gerçekleştirmek istenebilir. Oyun kodunun diğer bölümlerinden işleme betiğiyle iletişim kurmak da istenebilir.

on_message()
: Bir işleme betiği, bir `on_message()` işlevi tanımlayarak oyununuzun veya uygulamanızın diğer bölümlerinden iletiler alabilir. Harici bir bileşenin işleme betiğine bilgi gönderdiği yaygın durumlardan biri _kameradır_. Kamera odağını edinmiş bir kamera bileşeni, her karede görünümünü ve izdüşümünü otomatik olarak işleme betiğine gönderir. Bu iletinin adı `"set_view_projection"` olur:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Bununla birlikte herhangi bir betik veya GUI betiği, özel `@render` soketi üzerinden işleme betiğine ileti gönderebilir:

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## İşleme kaynakları
Belirli motor kaynaklarını işleme betiğine geçirmek için bunları projeye atanmış `.render` dosyasındaki `Render Resources` tablosuna ekleyebilirsiniz:

![İşleme kaynakları](images/render/render_resources.png)

Bu kaynakların bir işleme betiğinde kullanımı:

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Defold şu anda başvurulan işleme kaynakları olarak yalnızca `Materials` ve `Render Targets` türlerini destekler; ancak bu sistem zamanla daha fazla kaynak türünü destekleyecektir.
:::

### Çok örnekli işleme hedefleri {#multisampled-render-targets}

İşleme hedefleri (render targets), çok örnekli kenar yumuşatmayı (multisample anti-aliasing, MSAA) destekler. Bu, ekran dışı bir işleme geçişinde geometrinin kenarlarını yumuşatır. Hedefin örnek sayısı, pencerenin kenar yumuşatmasını denetleyen [Display ▸ Samples](/manuals/project-settings/#samples) ayarından bağımsızdır.

Bir `.render_target` kaynağı için düzenleyicide **Sample Count** değerini `1`, `2`, `4`, `8` veya `16` olarak ayarlayın. `1` değeri çoklu örneklemeyi devre dışı bırakır. Kaynağı `.render` dosyanızın **Render Resources** tablosuna ekleyin ve yukarıdaki örnekte olduğu gibi atanan adını `render.set_render_target()` ile kullanın.

Alternatif olarak, işleme betiğinizin `init()` işlevinde bir hedef oluşturun. `sample_count` alanını dış parametre tablosuna, eklerin (attachments) yanına yerleştirin:

```lua
self.offscreen = render.render_target({
    sample_count = 4,
    [graphics.BUFFER_TYPE_COLOR0_BIT] = {
        format = graphics.TEXTURE_FORMAT_RGBA,
        width = 1024,
        height = 1024,
        min_filter = graphics.TEXTURE_FILTER_LINEAR,
        mag_filter = graphics.TEXTURE_FILTER_LINEAR,
        u_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
        v_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
    },
})
self.scene_predicate = render.predicate({"scene"})
self.present_predicate = render.predicate({"present"})
```

Bu örnekte yalnızca renk içeren bir hedef kullanılır. Bir hedefteki tüm renk, derinlik ve şablon ekleri, hedefin örnek sayısını paylaşır. Geçiş derinlik testi gerektiriyorsa bir derinlik eki ve olağan derinlik testi durumunu ekleyin.

Aşağıdaki `update()` kod parçası için sahne materyallerine `scene` etiketini, tam ekran bir dörtgenin (quad) materyaline de `present` etiketini verin. Dörtgenin materyalinin `0` numaralı doku biriminden örnekleme yapması gerekir. Her geçiş için uygun görünümü ve izdüşümü ayarlayın:

```lua
render.set_render_target(self.offscreen)
render.set_viewport(0, 0, 1024, 1024)
render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = vmath.vector4(0, 0, 0, 1)})
-- Set the scene view and projection here.
render.draw(self.scene_predicate)

render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.set_viewport(0, 0, render.get_window_width(), render.get_window_height())
-- Set the full-screen quad view and projection here.
render.enable_texture(0, self.offscreen, graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.present_predicate)
render.disable_texture(0)
```

Başka bir hedefe geçildiğinde işleme geçişi tamamlanır ve önceki hedefin çok örnekli renk eklerindeki örnekler otomatik olarak birleştirilir (resolve). `render.enable_texture()`, örnekleri birleştirilmiş renk dokusunu bağlar; böylece dörtgen sıradan bir doku örnekleyicisi kullanır. Ayrı bir örnek birleştirme komutu gerekmez.

İstenen örnek sayısı varsayılan olarak `1` değerindedir ve pozitif bir tam sayı olmalıdır. Grafik arka uçları, desteklenmeyen örnek sayısı isteklerini desteklenen ve ikinin kuvveti olan bir sayıya indirir; gerekirse `1` değerine döner ve sayı değiştiğinde günlüğe bir uyarı kaydeder. Daha yüksek örnek sayıları, eklerin gerektirdiği belleği artırır.

Bir işleme hedefi kaynağı kullanırken, fiilen kullanılan örnek sayısını bir oyun nesnesinin `.script` dosyasından `resource.get_render_target_info()` ile inceleyin. Örneğin, `/render/offscreen.render_target` kaynağını **Render Resources** tablosuna ekledikten sonra:

```lua
function init(self)
    local info = resource.get_render_target_info("/render/offscreen.render_targetc")
    print("Render target sample count:", info.sample_count)
end
```

Cihaz desteğini kontrol ederken istenen örnek sayısının kullanılabildiğini varsaymak yerine fiilen kullanılan bu sayıyı kullanın. Parametre ve sonuç tablolarının tamamı için [`render.render_target()`](/ref/beta/render/#render.render_target:parameters) ve [`resource.get_render_target_info()`](/ref/beta/resource/#resource.get_render_target_info:path) belgelerine bakın.

## Doku tanıtıcıları

Defold'da dokular, motor içinde bir tanıtıcı (handle) ile temsil edilir; bu, temelde bir doku nesnesini motorun her yerinde benzersiz olarak tanımlaması gereken bir sayıya karşılık gelir. Bu, söz konusu tanıtıcıları işleme sistemi ile bir oyun nesnesi betiği arasında geçirerek oyun nesneleri dünyası ile işleme dünyası arasında köprü kurabileceğiniz anlamına gelir. Örneğin, bir oyun nesnesine bağlı betikte dinamik bir doku oluşturulabilir ve bir çizim komutunda genel doku olarak kullanılmak üzere işleyiciye gönderilebilir.

Bir `.script` dosyasında:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

Bir `.render_script` dosyasında:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
Şu anda bir kaynağın hangi dokuya işaret etmesi gerektiğini değiştirmenin bir yolu yoktur; ham tanıtıcıları bu şekilde yalnızca işleme betiğinde kullanabilirsiniz.
:::

## Desteklenen grafik API'leri
Defold işleme betiği API'si, işleme işlemlerini aşağıdaki grafik API'lerine dönüştürür:

:[Graphics API](../shared/graphics-api.md)


## Sistem iletileri

`"set_view_projection"`
: Bu ileti, kamera odağını edinmiş kamera bileşenleri tarafından gönderilir.

`"window_resized"`
: Motor, pencere boyutu değiştiğinde bu iletiyi gönderir. Hedef pencere boyutu değiştiğinde işlemeyi değiştirmek için bu iletiyi dinleyebilirsiniz. Masaüstünde bu, gerçek oyun penceresinin yeniden boyutlandırıldığı anlamına gelir; mobil cihazlarda ise bu ileti her yönelim değişikliğinde gönderilir.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: Hata ayıklama çizgisi çizer. `ray_casts`, vektörler ve daha fazlasını görselleştirmek için kullanın. Çizgiler `render.draw_debug3d()` çağrısıyla çizilir.

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Hata ayıklama metni çizer. Hata ayıklama bilgilerini yazdırmak için kullanın. Metin, yerleşik `always_on_top.font` yazı tipiyle çizilir. Sistem yazı tipinin `debug_text` etiketine sahip bir materyali vardır ve varsayılan işleme betiğinde diğer metinlerle birlikte işlenir.

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

`@system` soketine gönderilen `"toggle_profile"` iletisiyle erişilen görsel profil çıkarıcı, betikle programlanabilir işleyicinin bir parçası değildir. İşleme betiğinizden ayrı olarak çizilir.


## Çizim çağrıları ve toplu çizim {#draw-calls-and-batching}

Çizim çağrısı (draw call), bir doku, bir materyal ve isteğe bağlı ek ayarlar kullanarak bir nesneyi ekrana çizmek üzere GPU'yu hazırlama sürecini tanımlayan terimdir. Bu süreç genellikle yoğun kaynak kullanır ve çizim çağrısı sayısının olabildiğince az tutulması önerilir. Çizim çağrılarının sayısını ve işlenmelerinin ne kadar sürdüğünü [yerleşik profil çıkarıcı](/manuals/profiling/) ile ölçebilirsiniz.

Defold, aşağıda tanımlanan kurallara göre çizim çağrılarının sayısını azaltmak için işleme işlemlerini toplu çizim (batching) için gruplamaya çalışır. Kurallar GUI bileşenleri ile diğer tüm bileşen türleri arasında farklılık gösterir.


### GUI dışındaki bileşenler için toplu çizim kuralları

Her `render.draw()` çağrısı, dünya uzayında sıralanan eşleşen öğelerin nasıl sıralanacağını denetler. Varsayılan değer `render.SORT_BACK_TO_FRONT` olur; yakından uzağa işleme için `render.SORT_FRONT_TO_BACK`, eklenme sırasını korumak için ise `render.SORT_NONE` kullanın:

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

Seçilen sıra, hangi öğelerin yan yana geleceğini belirler ve bu nedenle toplu çizimi etkileyebilir. Bu sıralı listede her nesne, aşağıdaki koşullar karşılandığında önceki nesneyle aynı çizim çağrısında gruplanır:

* Aynı koleksiyon vekiline (collection proxy) ait olması
* Aynı bileşen türünde olması (sprite, parçacık efekti, karo haritası vb.)
* Aynı dokuyu kullanması (atlas veya karo kaynağı)
* Aynı materyale sahip olması
* Aynı gölgelendirici sabitlerine sahip olması (renk çarpanı gibi)

Bu, aynı koleksiyon vekilindeki iki sprite bileşeni seçilen sıralama sonrasında yan yana gelirse ve aynı dokuyu, materyali ve sabitleri kullanırsa aynı çizim çağrısında gruplanacakları anlamına gelir.


### GUI bileşenleri için toplu çizim kuralları

Bir GUI bileşenindeki düğümler, düğüm listesinde yukarıdan aşağıya doğru işlenir. Listedeki her düğüm, aşağıdaki koşullar karşılandığında önceki düğümle aynı çizim çağrısında gruplanır:

* Aynı türde olması (kutu, metin, daire dilimi vb.)
* Aynı dokuyu kullanması (atlas veya karo kaynağı)
* Aynı harmanlama moduna sahip olması.
* Aynı yazı tipine sahip olması (yalnızca metin düğümleri için)
* Aynı şablon ayarlarına sahip olması

::: sidenote
Düğümler bileşen bazında işlenir. Bu, farklı GUI bileşenlerindeki düğümlerin toplu çizim için gruplanmayacağı anlamına gelir.
:::

Düğümleri hiyerarşiler halinde düzenleyebilmek, düğümleri yönetilebilir birimler halinde gruplamayı kolaylaştırır. Ancak farklı düğüm türlerini karıştırırsanız hiyerarşiler toplu çizimi bozabilir. GUI katmanlarını kullanarak düğüm hiyerarşilerini korurken GUI düğümlerini daha etkili biçimde toplu çizim için gruplamak mümkündür. GUI katmanları ve bunların çizim çağrılarını nasıl etkilediği hakkında daha fazla bilgiyi [GUI kılavuzunda](/manuals/gui#layers-and-draw-calls) bulabilirsiniz.
