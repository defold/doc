---
title: Defold hesaplama kılavuzu
brief: Bu kılavuz, hesaplama programları, gölgelendirici sabitleri ve örnekleyicilerle nasıl çalışılacağını açıklar.
---

# Hesaplama programları

::: sidenote
Defold'da hesaplama gölgelendiricisi desteği şu anda *teknik önizleme* aşamasındadır.
Bu, bazı özelliklerin eksik olduğu ve API'nin gelecekte değişebileceği anlamına gelir.
:::

Hesaplama gölgelendiricileri (compute shader), GPU üzerinde genel amaçlı hesaplamalar yapmak için güçlü bir araçtır. Fizik simülasyonları, görüntü işleme ve daha pek çok görev için GPU üzerindeki paralel işlem gücünden yararlanmanızı sağlar. Bir hesaplama gölgelendiricisi, arabelleklerde veya dokularda saklanan veriler üzerinde çalışır ve işlemleri birçok GPU iş parçacığında paralel olarak gerçekleştirir. Hesaplama gölgelendiricilerini yoğun hesaplamalar için bu kadar güçlü kılan, bu paralelliktir.

* Görüntü oluşturmak için kullanılan işleme (rendering) hattı hakkında daha fazla bilgi için [İşleme belgelerine](/manuals/render) bakın.
* Gölgelendirici programlarının ayrıntılı açıklaması için [Gölgelendirici belgelerine](/manuals/shader) bakın.

## Hesaplama gölgelendiricileriyle neler yapabilirim?

Hesaplama gölgelendiricileri genel amaçlı hesaplamalarda kullanılmak üzere tasarlandığından, bunlarla yapabileceklerinizin bir sınırı yoktur. Hesaplama gölgelendiricilerinin yaygın kullanım alanlarından bazıları şunlardır:

Görüntü işleme
  - Görüntü filtreleme: Bulanıklaştırma, kenar algılama, keskinleştirme filtresi ve benzeri işlemler uygulama.
  - Renk derecelendirme: Bir görüntünün renk uzayını ayarlama.

Fizik
  - Parçacık sistemleri: Duman, ateş ve akışkan dinamiği gibi efektler için çok sayıda parçacığı simüle etme.
  - Yumuşak cisim fiziği: Kumaş ve jöle gibi şekli değişebilen nesneleri simüle etme.
  - Görünmeyenleri eleme: Örtülenleri eleme, görüş hacmi dışında kalanları eleme

Prosedürel üretim
  - Arazi üretimi: Gürültü işlevleri kullanarak ayrıntılı arazi oluşturma.
  - Bitki örtüsü ve yapraklar: Bitkileri ve ağaçları prosedürel olarak oluşturma.

İşleme efektleri
  - Küresel aydınlatma: Işığın sahnede nasıl yansıdığını yaklaşık olarak hesaplayarak gerçekçi aydınlatmayı simüle etme.
  - Vokselleştirme: Örgü verilerinden 3B bir voksel ızgarası oluşturma.

## Hesaplama gölgelendiricileri nasıl çalışır?

Genel olarak hesaplama gölgelendiricileri, bir görevi aynı anda yürütülebilecek çok sayıda küçük göreve bölerek çalışır. Bu, iş grupları (`work groups`) ve çağrılar (`invocations`) kavramlarıyla sağlanır:

İş grupları
: Hesaplama gölgelendiricisi, iş gruplarından (`work groups`) oluşan bir ızgara üzerinde çalışır. Her iş grubu sabit sayıda çağrı (veya iş parçacığı) içerir. İş gruplarının boyutu ve çağrı sayısı gölgelendirici kodunda tanımlanır.

Çağrılar
: Her çağrı (veya iş parçacığı) hesaplama gölgelendiricisi programını yürütür. Bir iş grubundaki çağrılar, paylaşılan bellek aracılığıyla veri paylaşabilir; bu da aralarında verimli iletişim ve eşzamanlama sağlar.

GPU, birden çok iş grubunda çok sayıda çağrıyı paralel olarak başlatarak hesaplama gölgelendiricisini yürütür ve uygun görevler için önemli bir hesaplama gücü sağlar.

## Hesaplama programı oluşturma

Bir hesaplama programı oluşturmak için *Assets* tarayıcısında hedef klasöre <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Compute</kbd> seçeneğini seçin. (Menüden <kbd>File ▸ New...</kbd> seçeneğini seçip ardından <kbd>Compute</kbd> seçeneğini de seçebilirsiniz). Yeni hesaplama dosyasına bir ad verin ve <kbd>Ok</kbd> düğmesine basın.

![Hesaplama dosyası](images/compute/compute_file.png)

Yeni hesaplama dosyası *Compute Editor* içinde açılır.

![Hesaplama düzenleyicisi](images/compute/compute.png)

Hesaplama dosyası aşağıdaki bilgileri içerir:

Compute Program
: Kullanılacak hesaplama gölgelendiricisi program dosyası (*`.cp`*). Gölgelendirici "soyut iş öğeleri" üzerinde çalışır; yani girdi ve çıktı veri türlerinin sabit bir tanımı yoktur. Hesaplama gölgelendiricisinin ne üretmesi gerektiğini tanımlamak programcıya bağlıdır.

Constants
: Hesaplama gölgelendiricisi programına aktarılacak uniform değerleri. Kullanılabilir sabitlerin listesi için aşağıya bakın.

Samplers
: İsteğe bağlı olarak materyal (material) dosyasında belirli örnekleyicileri (sampler) yapılandırabilirsiniz. Bir örnekleyici ekleyin, gölgelendirici programında kullanılan ada göre adlandırın ve sarma ile filtre ayarlarını istediğiniz gibi belirleyin.


## Hesaplama programını Defold'da kullanma

Materyallerden farklı olarak hesaplama programları hiçbir bileşene (component) atanmaz ve normal işleme akışının parçası değildir. Bir hesaplama programının herhangi bir iş yapabilmesi için bir işleme betiğinde (render script) yürütülmek üzere gönderilmesi (`dispatched`) gerekir. Ancak bunu yapmadan önce işleme betiğinde hesaplama programına bir başvuru olduğundan emin olmanız gerekir. Şu anda bir işleme betiğinin hesaplama programını tanımasını sağlamanın tek yolu, programı işleme betiğine başvuruyu içeren .render dosyasına eklemektir:

![Hesaplama programı içeren işleme dosyası](images/compute/compute_render_file.png)

Hesaplama programını kullanmak için önce onu işleme bağlamına bağlamanız gerekir. Bu, materyallerde olduğu gibi yapılır:

```lua
render.set_compute("my_compute")
-- Do compute work here, call render.set_compute() to unbind
render.set_compute()
```

Hesaplama sabitleri, program yürütülmek üzere gönderildiğinde otomatik olarak uygulansa da düzenleyiciden bir hesaplama programına herhangi bir girdi veya çıktı kaynağı (dokular, arabellekler vb.) bağlamak mümkün değildir. Bunun işleme betikleri aracılığıyla yapılması gerekir:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Programı belirlediğiniz çalışma uzayında çalıştırmak için programı yürütülmek üzere göndermeniz gerekir:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Hesaplama programlarından veri yazma

Şu anda bir hesaplama programından herhangi bir türde çıktı üretmek yalnızca depolama dokuları (`storage textures`) aracılığıyla mümkündür. Depolama dokusu, daha fazla işlev ve yapılandırma seçeneği sunması dışında "normal bir dokuya" benzer. Depolama dokuları, adından da anlaşılacağı gibi, bir hesaplama programından veri okuyup yazabileceğiniz genel amaçlı bir arabellek olarak kullanılabilir. Ardından aynı arabelleği okuma amacıyla farklı bir gölgelendirici programına bağlayabilirsiniz.

Defold'da bir depolama dokusu oluşturmak için bu işlemi normal bir `.script` dosyasından yapmanız gerekir. İşleme betikleri bu işlevi sunmaz; çünkü dinamik dokuların `resource` API'si aracılığıyla oluşturulması gerekir ve bu API yalnızca normal `.script` dosyalarında kullanılabilir.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Tüm parçaları birleştirme

### Gölgelendirici programı

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Betik bileşeni
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### İşleme betiği
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
    render.set_compute()
end
```

## Uyumluluk

Defold şu anda aşağıdaki grafik bağdaştırıcılarında hesaplama gölgelendiricilerini destekler:

- Vulkan
- Metal (MoltenVK aracılığıyla)
- OpenGL 4.3+
- OpenGL ES 3.1+

Etkin grafik bağdaştırıcısının hesaplama gölgelendiricilerini destekleyip desteklemediğini kontrol etmek için `graphics.get_adapter_info()` işlevini kullanın. `features` alanı, bağdaştırıcının desteklediği bağlam özelliği sabitlerini içeren bir dizidir:

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

Diziye yalnızca desteklenen özellikler dahil edilir; bu yapı, anahtar olarak özellik sabitlerini kullanan bir tablo değildir. Oyun farklı grafik bağdaştırıcılarıyla veya sürücü desteği farklı cihazlarda çalışabiliyorsa, hesaplama gölgelendiricilerini kullanmadan önce her zaman bu kontrolü yapın. OpenGL ve OpenGL ES desteği API sürümüne ve sürücüye bağlıdır. Vulkan ve MoltenVK aracılığıyla Metal, 1.0 sürümünden itibaren hesaplama gölgelendiricilerini destekler. Vulkan'ın varsayılan grafik arka ucu olmadığı platformlarda Vulkan'ı seçmek için bir [uygulama bildirimi](/manuals/app-manifest) kullanın.
