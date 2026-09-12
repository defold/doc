---
title: Defold materyal kılavuzu
brief: Bu kılavuz, materyaller, gölgelendirici sabitleri ve örnekleyicilerle nasıl çalışılacağını açıklar.
---

# Materyaller

Materyaller (material), bir grafik bileşeninin (component) görüntüsü oluşturulurken kullanılacak işleme (rendering) biçimini tanımlar; bu bileşen bir sprite bileşeni, karo haritası, yazı tipi, GUI düğümü, model vb. olabilir.

Bir materyal, işleme hattında işlenecek nesneleri seçmeye yarayan bilgileri _etiketler_ olarak tutar. Ayrıca, kullanılabilir grafik sürücüsü aracılığıyla derlenip grafik donanımına yüklenen ve bileşen her karede işlenirken çalıştırılan _gölgelendirici programlarına_ (shader programs) başvurular da tutar.

* İşleme hattı hakkında daha fazla bilgi için [İşleme belgelerine](/manuals/render) bakın.
* Gölgelendirici programlarının ayrıntılı açıklaması için [Gölgelendirici belgelerine](/manuals/shader) bakın.

## Materyal oluşturma

Materyal oluşturmak için *Assets* tarayıcısındaki hedef klasöre <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Material</kbd> seçeneğini seçin. (Menüden <kbd>File ▸ New...</kbd> seçeneğini, ardından <kbd>Material</kbd> seçeneğini de seçebilirsiniz). Yeni materyal dosyasına bir ad verin ve <kbd>Ok</kbd> düğmesine basın.

![Materyal dosyası](images/materials/material_file.png)

Yeni materyal *Material Editor* içinde açılır.

![Materyal düzenleyicisi](images/materials/material.png)

Materyal dosyası aşağıdaki bilgileri içerir:

Name
: Materyalin kimliği. Bu ad, materyali derlemeye dahil etmek üzere *Render* kaynağında listelemek için kullanılır. Ad ayrıca `render.enable_material()` işleme API'si işlevinde de kullanılır. Adın benzersiz olması önerilir.

Vertex Program
: Materyalle işleme yaparken kullanılacak köşe gölgelendiricisi (vertex shader) program dosyası (*`.vp`*). Köşe gölgelendiricisi programı, bileşenin geometrik temel öğelerini (primitive) oluşturan her köşe için GPU üzerinde çalıştırılır. Her köşenin ekran konumunu hesaplar ve isteğe bağlı olarak ara değerleme (interpolation) uygulanıp parça programına girdi olarak verilen "varying" değişkenleri üretir.

Fragment Program
: Materyalle işleme yaparken kullanılacak parça gölgelendiricisi (fragment shader) program dosyası (*`.fp`*). Program, bir geometrik temel öğenin her parçası (pikseli) için GPU üzerinde çalışır ve amacı her parçanın rengini belirlemektir. Bu genellikle doku sorgulamaları ve girdi değişkenlerine (varying değişkenleri veya sabitler) dayalı hesaplamalarla yapılır.

Vertex Constants
: Köşe gölgelendiricisi programına iletilecek uniform değerleri. Kullanılabilir sabitlerin listesi için aşağıya bakın.

Fragment Constants
: Parça gölgelendiricisi programına iletilecek uniform değerleri. Kullanılabilir sabitlerin listesi için aşağıya bakın.

Samplers
: Materyal dosyasında isteğe bağlı olarak belirli örnekleyicileri (sampler) yapılandırabilirsiniz. Bir örnekleyici ekleyin, gölgelendirici programında kullanılan ada göre adlandırın ve sarma ile filtreleme ayarlarını istediğiniz gibi belirleyin.

Tags
: Materyalle ilişkili etiketler. Etiketler motorda, birlikte çizilmesi gereken bileşenleri toplamak üzere [`render.predicate()`](/ref/render#render.predicate) tarafından kullanılan bir _bit maskesi_ olarak temsil edilir. Bunun nasıl yapıldığını öğrenmek için [İşleme belgelerine](/manuals/render) bakın. Bir projede kullanabileceğiniz en fazla etiket sayısı 32'dir.

## Öznitelikler {#attributes}

Gölgelendirici öznitelikleri (shader attributes; köşe akışları veya köşe öznitelikleri olarak da adlandırılır), GPU biriminin geometriyi işlemek için köşeleri bellekten nasıl aldığını belirleyen bir mekanizmadır. Köşe gölgelendiricisi, `attribute` anahtar sözcüğünü kullanarak bir akış kümesi belirtir ve çoğu durumda Defold, akışların adlarına göre verileri arka planda otomatik olarak üretip bağlar. Ancak bazı durumlarda, motorun üretmediği belirli bir efekti elde etmek için köşe başına daha fazla veri iletmek isteyebilirsiniz. Bir köşe özniteliği aşağıdaki alanlarla yapılandırılabilir:

Name
: Özniteliğin adı. Gölgelendirici sabitlerine benzer şekilde, öznitelik yapılandırması yalnızca köşe programında belirtilen bir öznitelikle eşleşiyorsa kullanılır.

Semantic type
: Anlamsal tür (semantic type), özniteliğin *ne* olduğunu ve/veya düzenleyicide *nasıl* gösterilmesi gerektiğini belirtir. Örneğin, bir özniteliği `SEMANTIC_TYPE_COLOR` ile tanımlamak düzenleyicide bir renk seçici gösterir; veriler ise motordan gölgelendiriciye yine olduğu gibi iletilir.

  - `SEMANTIC_TYPE_NONE` Varsayılan anlamsal tür. Özniteliğe ait materyal verilerini doğrudan köşe arabelleğine iletmek dışında öznitelik üzerinde başka bir etkisi yoktur (varsayılan)
  - `SEMANTIC_TYPE_POSITION` Öznitelik için köşe başına konum verisi üretir. Motora konumların nasıl hesaplanacağını belirtmek için koordinat uzayıyla birlikte kullanılabilir
  - `SEMANTIC_TYPE_TEXCOORD` Öznitelik için köşe başına doku koordinatları üretir
  - `SEMANTIC_TYPE_PAGE_INDEX` Öznitelik için köşe başına sayfa indisleri üretir
  - `SEMANTIC_TYPE_COLOR` Düzenleyicinin özniteliği nasıl yorumladığını etkiler. Bir öznitelik renk anlamıyla yapılandırılırsa özellik denetleyicisinde bir renk seçici aracı gösterilir
  - `SEMANTIC_TYPE_NORMAL` Öznitelik için köşe başına normal verisi üretir
  - `SEMANTIC_TYPE_TANGENT` Öznitelik için köşe başına teğet verisi üretir
  - `SEMANTIC_TYPE_WORLD_MATRIX` Öznitelik için köşe başına dünya matrisi verisi üretir
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Öznitelik için köşe başına normal matrisi verisi üretir
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Öznitelik için köşe başına 3x3 doku dönüşüm matrisi üretir. Parçacık bileşenleri için motor, bileşendeki görüntü özelliğine ait koordinatları atlas uzayına dönüştüren bir matris sağlar. Sprite bileşenleri için motor, bileşenin kullandığı her görüntüye ait bir matris sağlar (çoklu doku kullanılırken). Model bileşenleri için birim matris sağlanır.

Data type
: Özniteliğin dayandığı verilerin veri türü.

  - `TYPE_BYTE` İşaretli 8 bitlik bayt değerleri
  - `TYPE_UNSIGNED_BYTE` İşaretsiz 8 bitlik bayt değerleri
  - `TYPE_SHORT` İşaretli 16 bitlik short değerleri
  - `TYPE_UNSIGNED_SHORT` İşaretsiz 16 bitlik short değerleri
  - `TYPE_INT` İşaretli tamsayı değerleri
  - `TYPE_UNSIGNED_INT` İşaretsiz tamsayı değerleri
  - `TYPE_FLOAT` Kayan noktalı değerler (varsayılan)

Normalize
: true ise öznitelik değerleri GPU sürücüsü tarafından normalleştirilir. Tam hassasiyete ihtiyaç duymadığınız ancak belirli sınırları bilmeden hesaplama yapmak istediğiniz durumlarda bu yararlı olabilir. Örneğin, bir renk vektörü genellikle yalnızca 0..255 aralığındaki bayt değerlerine ihtiyaç duyar, ancak gölgelendiricide yine de 0..1 aralığındaki bir değer olarak ele alınır.

Coordinate space
: Bazı anlamsal türler, verilerin farklı koordinat uzaylarında sağlanmasını destekler. Sprite bileşenleriyle kameraya dönük durma (billboarding) efekti uygularken, en etkili toplu çizim (batching) için genellikle yerel uzayda bir konum özniteliğinin yanı sıra dünya uzayına tamamen dönüştürülmüş bir konum da gerekir.

Vector type
: Özniteliğin vektör türü.

  - `VECTOR_TYPE_SCALAR` Tek skaler değer
  - `VECTOR_TYPE_VEC2` 2B vektör
  - `VECTOR_TYPE_VEC3` 3B vektör
  - `VECTOR_TYPE_VEC4` 4B vektör (varsayılan)
  - `VECTOR_TYPE_MAT2` 2B matris
  - `VECTOR_TYPE_MAT3` 3B matris
  - `VECTOR_TYPE_MAT4` 4B matris

Step function
: Öznitelik verilerinin köşe işlevine nasıl sunulacağını belirtir. Bu yalnızca örneklerle çizim (instancing) için geçerlidir.

  - `Vertex` Her köşe için bir kez; örneğin, bir konum özniteliği genellikle örgüdeki (mesh) her köşe için köşe işlevine verilir (varsayılan)
  - `Instance` Her örnek için bir kez; örneğin, bir dünya matrisi özniteliği genellikle her örnek için köşe işlevine bir kez verilir

Value
: Özniteliğin değeri. Öznitelik değerleri bileşen başına geçersiz kılınabilir; bunun dışında bu değer, köşe özniteliğinin varsayılan değeri olarak kullanılır. Not: *varsayılan* öznitelikler (konum, doku koordinatları ve sayfa indisleri) için bu değer yok sayılır.

::: sidenote
Özel öznitelikler, akışları daha küçük bir veri türü veya farklı sayıda öğe kullanacak şekilde yeniden yapılandırarak hem CPU hem de GPU üzerindeki bellek kullanımını azaltmak için de kullanılabilir.
:::

### Varsayılan öznitelik anlamları

Materyal sistemi, belirli bir ad kümesi için çalışma sırasında özniteliğin adına göre otomatik olarak varsayılan bir anlamsal tür atar:

  - `position` - anlamsal tür: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - anlamsal tür: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - anlamsal tür: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - anlamsal tür: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - anlamsal tür: `SEMANTIC_TYPE_COLOR`
  - `normal` - anlamsal tür: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - anlamsal tür: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - anlamsal tür: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - anlamsal tür: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - anlamsal tür: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Materyalde bu özniteliklere ait girdiler varsa varsayılan anlamsal türün yerine materyal düzenleyicisinde yapılandırdığınız tür kullanılır.

### Özel köşe özniteliği verilerini ayarlama

Kullanıcı tanımlı gölgelendirici sabitlerine benzer şekilde, `go.get`, `go.set` ve `go.animate` çağrılarıyla köşe özniteliklerini de çalışma sırasında güncelleyebilirsiniz:

![Özel materyal özniteliği](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

Ancak köşe özniteliklerini güncellerken dikkat edilmesi gereken bazı noktalar vardır; bir bileşenin değeri kullanıp kullanamayacağı özniteliğin anlamsal türüne bağlıdır. Örneğin, sprite bileşeni `SEMANTIC_TYPE_POSITION` türünü destekler. Bu anlamsal türe sahip bir özniteliği güncellerseniz bileşen, üzerine yazılan değeri yok sayar; çünkü anlamsal tür, verilerin her zaman sprite bileşeninin konumundan üretilmesini gerektirir.

Model bileşenleri de özel materyal özniteliklerine `go.get()`, `go.set()` ve `go.animate()` aracılığıyla erişim sağlar. Örneğin, model materyalinde `my_attribute` adlı bir öznitelik tanımladıktan sonra:

```lua
go.set("#model", "my_attribute", vmath.vector4(1, 0, 0, 1))
go.animate("#model", "my_attribute", go.PLAYBACK_LOOP_PINGPONG,
    vmath.vector4(0, 1, 0, 1), go.EASING_LINEAR, 2)
```

Birden çok örgü içeren bir modelde şu anda yalnızca ilk örgüye bu şekilde erişilebilir. Örneklerle çizimde kullanılmayan ve köşe başına tanımlı bir özniteliği güncellemek, örgü boyutuyla orantılı miktarda köşe verisinin yeniden oluşturulup yüklenmesine de yol açabilir. Bu nedenle sık güncellemeler büyük örgüler için maliyetli olabilir.

Bir köşe özniteliğinin skaler veya `Vec4` dışında bir vektör türü olduğu durumlarda da verileri `go.set` kullanarak ayarlayabilirsiniz:

```lua
-- The last two components in the vec4 will not be used!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

Aynı durum matris öznitelikleri için de geçerlidir; öznitelik `Mat4` dışında bir matris türündeyse de verileri `go.set` kullanarak ayarlayabilirsiniz.

### Özel köşe özniteliklerini kullanma örnekleri

UV koordinatlarını atlas uzayına dönüştürmek için doku dönüşüm özniteliğini kullanma:

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extract position from the transform
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extract the scale from the transform
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // convert to local UV (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Alternatively, if the UV coordinates already are in the 0..1 range,
  // you can transform into atlas space directly by multiplying the transform:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Pass the value into the fragment shader
  var_texcoord0 = localUV;

  // ... rest of vertex shader
}
```

### Örneklerle çizim

Örneklerle çizim, bir sahnede aynı nesnenin birden çok kopyasını verimli biçimde çizmek için kullanılan bir tekniktir. Nesne her kullanıldığında ayrı bir kopyasını oluşturmak yerine, grafik motorunun tek bir nesne oluşturup bunu birden çok kez yeniden kullanmasını sağlar. Örneğin, büyük bir orman içeren bir oyunda her ağaç için ayrı bir ağaç modeli oluşturmak yerine, örneklerle çizim sayesinde tek bir ağaç modeli oluşturup bunu farklı konum ve ölçeklerle yüzlerce veya binlerce kez yerleştirebilirsiniz. Böylece orman, her ağaç için ayrı çizim çağrıları yerine tek bir çizim çağrısıyla işlenebilir.

::: sidenote
Örneklerle çizim şu anda yalnızca model bileşenlerinde kullanılabilir.
:::

Örneklerle çizim, mümkün olduğunda otomatik olarak etkinleştirilir. Defold, çizim durumlarını mümkün olduğunca toplu çizim için birleştirmeye büyük ölçüde dayanır. Örneklerle çizimin çalışması için bazı gereksinimlerin karşılanması gerekir:

- Tüm örneklerde aynı materyal kullanılmalıdır. `render.enable_material` ile özel bir materyal ayarlanmışsa da örneklerle çizim çalışır)
- Materyal, 'local' köşe uzayını kullanacak şekilde yapılandırılmalıdır
- Materyalde örnek başına tekrarlanan en az bir köşe özniteliği bulunmalıdır
- Sabit değerleri tüm örneklerde aynı olmalıdır. Sabit değerleri bunun yerine özel köşe özniteliklerine konabilir veya başka bir veri saklama yöntemi kullanılabilir (örneğin bir doku)
- Dokular veya depolama arabellekleri gibi gölgelendirici kaynakları tüm örneklerde aynı olmalıdır

Bir köşe özniteliğini örnek başına tekrarlanacak şekilde yapılandırmak için `Step function` değerinin `Instance` olarak ayarlanması gerekir. Bu, belirli anlamsal türlerde ada göre otomatik olarak yapılır (yukarıdaki `Varsayılan öznitelik anlamları` tablosuna bakın), ancak materyal düzenleyicisinde `Step function` değeri `Instance` olarak ayarlanarak elle de yapılabilir.

Basit bir örnek olarak, aşağıdaki sahnede her biri bir model bileşeni içeren dört oyun nesnesi (game object) vardır:

![Örneklerle çizim kurulumu](images/materials/instancing-setup.png)

Materyal, örnek başına tekrarlanan tek bir özel köşe özniteliğiyle şu şekilde yapılandırılmıştır:

![Örneklerle çizim materyali](images/materials/instancing-material.png)

Köşe gölgelendiricisinde örnek başına kullanılan birden çok öznitelik belirtilmiştir:

```glsl
// Per vertex attributes
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Per instance attributes
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

`mtx_world` ve `mtx_normal` özniteliklerinin varsayılan olarak `Instance` adım işlevini kullanacak şekilde yapılandırıldığını unutmayın. Materyal düzenleyicisinde bunlar için birer girdi ekleyip `Step function` değerini `Vertex` olarak ayarlayarak bunu değiştirebilirsiniz. Böylece öznitelik, örnek başına değil köşe başına tekrarlanır.

Bu durumda örneklerle çizimin çalıştığını doğrulamak için web profil çıkarıcısına bakabilirsiniz. Kutunun örnekleri arasında değişen tek şey örnek başına öznitelikler olduğundan, bu durumda tek bir çizim çağrısıyla işlenebilir:

![Örneklerle çizimde çizim çağrıları](images/materials/instancing-draw-calls.png)

#### Geriye dönük uyumluluk

Masaüstünde OpenGL 3.1 ve mobilde OpenGL ES 3.0, örneklerle çizimi temel bir özellik olarak sağlar. Daha eski OpenGL ES ve WebGL bağlamları bunu `ANGLE_instanced_arrays` gibi bir uzantıyla destekleyebilir; diğer eski bağdaştırıcılar ise desteklemez. Örneklerle çizim kullanılamadığında işleme varsayılan olarak yine çalışır, ancak performansı daha düşük olabilir.

Desteği saptamak ve gerektiğinde daha az maliyetli bir materyal seçmek veya çok sayıda örnek içeren içeriği çıkarmak için `graphics.get_adapter_info()` kullanın. `features` alanı, desteklenen özellik sabitlerinin dizisidir; bu sabitlerin anahtar olarak kullanıldığı bir tablo değildir:

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

local instancing_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_INSTANCING
)
```

## Köşe ve parça sabitleri {#vertex-and-fragment-constants}

Gölgelendirici sabitleri (shader constants) veya "uniform" değerleri, motordan köşe ve parça gölgelendiricisi programlarına iletilen değerlerdir. Bir sabiti kullanmak için materyal dosyasında onu *Vertex Constant* veya *Fragment Constant* özelliği olarak tanımlayın. Karşılık gelen `uniform` değişkenlerinin gölgelendirici programında tanımlanması gerekir. Bir materyalde aşağıdaki sabitler ayarlanabilir:

`CONSTANT_TYPE_WORLD`
: Dünya matrisi. Köşeleri dünya uzayına dönüştürmek için kullanın. Bazı bileşen türlerinde köşeler, köşe programına ulaştıklarında (toplu çizim nedeniyle) zaten dünya uzayındadır. Bu durumlarda gölgelendiricide dünya matrisiyle çarpmak yanlış sonuçlar verir.

`CONSTANT_TYPE_VIEW`
: Görünüm matrisi. Köşeleri görünüm (kamera) uzayına dönüştürmek için kullanın.

`CONSTANT_TYPE_PROJECTION`
: İzdüşüm matrisi. Köşeleri ekran uzayına dönüştürmek için kullanın.

`CONSTANT_TYPE_VIEWPROJ`
: Görünüm ve izdüşüm matrislerinin önceden çarpıldığı matris.

`CONSTANT_TYPE_WORLDVIEW`
: Dünya ve görünüm matrislerinin önceden çarpıldığı matris.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Dünya, görünüm ve izdüşüm matrislerinin önceden çarpıldığı matris.

`CONSTANT_TYPE_WORLD_INVERSE`
: Dünya matrisinin tersi. Dünya uzayından nesnenin yerel uzayına geri dönüştürmek için kullanın.

`CONSTANT_TYPE_VIEW_INVERSE`
: Görünüm matrisinin tersi. Kamera uzayından dünya uzayına geri dönüştürmek için kullanın.

`CONSTANT_TYPE_PROJECTION_INVERSE`
: İzdüşüm matrisinin tersi. Kırpma uzayından kamera uzayına geri dönüştürmek için kullanın.

`CONSTANT_TYPE_VIEWPROJ_INVERSE`
: Birleştirilmiş görünüm ve izdüşüm matrislerinin tersi. Kırpma uzayından dünya uzayına geri dönüştürmek için kullanın.

`CONSTANT_TYPE_WORLDVIEW_INVERSE`
: Birleştirilmiş dünya ve görünüm matrislerinin tersi. Kamera uzayından nesnenin yerel uzayına geri dönüştürmek için kullanın.

`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`
: Birleştirilmiş dünya, görünüm ve izdüşüm matrislerinin tersi. Kırpma uzayından nesnenin yerel uzayına geri dönüştürmek için kullanın. Bu ters matris sabitleri, gölgelendiricide matris tersi hesaplama gereksinimini ortadan kaldırır.

`CONSTANT_TYPE_NORMAL`
: Normal yönelimini hesaplamak için kullanılan matris. Dünya dönüşümü, birleşik dünya-görünüm dönüşümünün dikliğini bozan eşit olmayan ölçekleme içerebilir. Normal matrisi, normalleri dönüştürürken yönle ilgili sorunları önlemek için kullanılır. (Normal matrisi, dünya-görünüm matrisinin tersinin devriğidir).

`CONSTANT_TYPE_TIME`
: Motorun sağladığı bir `vector4` değeridir; `.x` motorun başlatılmasından bu yana geçen süreyi, `.y` önceki kareden bu yana geçen süreyi içerir. `.z` ve `.w` şu anda sıfırdır. Motor bu değeri otomatik olarak günceller; `go.set()` ile güncellenmesi gerekmez. Bir örnek için [Shadertoy öğreticisine](/tutorials/shadertoy/#animation) bakın.

  Modern bir GLSL uniform bloğunda `time` adlı bir Time sabiti tanımlayın:

  ```glsl
  uniform fragment_inputs
  {
      vec4 time;
  };
  ```

`CONSTANT_TYPE_USER`
: Gölgelendirici programlarınıza iletmek istediğiniz herhangi bir özel veri için kullanabileceğiniz vector4 sabiti. Sabitin başlangıç değerini sabit tanımında ayarlayabilirsiniz, ancak bu değer [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) işlevleriyle değiştirilebilir. Değeri [go.get()](/ref/stable/go/#go.get) ile de alabilirsiniz. Tek bir bileşen örneğinin materyal sabitini değiştirmek [toplu çizimi bozar ve ek çizim çağrılarına yol açar](/manuals/render/#draw-calls-and-batching).

Örnek:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Gölgelendirici programlarınıza iletmek istediğiniz herhangi bir özel veri için kullanabileceğiniz matrix4 sabiti. Sabitin başlangıç değerini sabit tanımında ayarlayabilirsiniz, ancak bu değer [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) işlevleriyle değiştirilebilir. Değeri [go.get()](/ref/stable/go/#go.get) ile de alabilirsiniz. Tek bir bileşen örneğinin materyal sabitini değiştirmek [toplu çizimi bozar ve ek çizim çağrılarına yol açar](/manuals/render/#draw-calls-and-batching).

Örnek:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

### GUI düğümü materyal sabitleri

Bir GUI betiğinde, düğümün materyal sabitlerini okumak ve yazmak için `go` işlevleri yerine `gui.get()` ve `gui.set()` kullanın. Vektör bileşenleri, matris sabitleri ve sabit dizileri desteklenir. Seçenekler tablosundaki dizi indisleri 1'den başlar:

```lua
local node = gui.get_node("button")

local tint = gui.get(node, "tint")
gui.set(node, "tint.x", 0.5)
gui.set(node, "light_matrix", vmath.matrix4())
gui.set(node, "tint_array", vmath.vector4(1, 0, 0, 1), { index = 1 })
```

::: sidenote
`CONSTANT_TYPE_USER` veya `CONSTANT_TYPE_USER_MATRIX4` türündeki bir materyal sabitinin `go.get()` ve `go.set()` ya da `gui.get()` ve `gui.set()` ile kullanılabilmesi için gölgelendirici programında kullanılması gerekir. Sabit materyalde tanımlanmış ancak programda kullanılmamışsa materyalden kaldırılır ve çalışma sırasında kullanılamaz.
:::

## Örnekleyiciler

Örnekleyiciler, bir dokudan (karo kaynağı veya atlas) renk bilgisi örneklemek için kullanılır. Renk bilgisi daha sonra gölgelendirici programındaki hesaplamalarda kullanılabilir.

Sprite, karo haritası, GUI ve parçacık efekti bileşenleri, görüntü dokularını ilk tanımlanan `sampler2D` değerine otomatik olarak bağlar. Sprite bileşenleri birden çok dokuyu da destekler: materyalde tanımlanan her örnekleyici, sprite bileşeninde adlandırılmış bir görüntü yuvasına dönüşür. İlk doku, sprite bileşeninin animasyon verilerini sağlar ve kare dizisini yönetir. Her karede, görüntü kimliği her ek dokuda karşılık gelen görüntüyü bulmak için kullanılır; ek dokular kendi UV koordinatlarını sağlar. Bu nedenle atanan atlasların veya karo kaynaklarının eşleşen kare kimlikleri ve benzer şekilli görüntüler içermesi önerilir; çokgen biçiminde paketlenen şekillerin farklı olması doku taşmasına yol açabilir. Ayrıntılar için [Çok dokulu sprite bileşenleri](/manuals/sprite/#multi-textured-sprites) bölümüne bakın.

Ek bir doku yuvası sunmayan bir bileşen veya işleme iş akışı için, işleme betiğinden ek doku örnekleyicileri bağlamak üzere [`render.enable_texture()`](/ref/render/#render.enable_texture) kullanın.

![Sprite örnekleyicisi](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Bir bileşenin örnekleyici ayarlarını, materyal dosyasına örnekleyiciyi adıyla ekleyerek belirtebilirsiniz. Örnekleyicinizi materyal dosyasında yapılandırmazsanız genel *graphics* proje ayarları kullanılır.

![Örnekleyici ayarları](images/materials/my_sampler.png)

Model bileşenleri için örnekleyicilerinizi materyal dosyasında istediğiniz ayarlarla belirtmeniz gerekir. Düzenleyici daha sonra bu materyali kullanan herhangi bir model bileşeni için dokuları ayarlamanıza izin verir:

![Model örnekleyicileri](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Model](images/materials/model.png)

## Örnekleyici ayarları

Name
: Örnekleyicinin adı. Bu adın, parça gölgelendiricisinde tanımlanan `sampler2D` adıyla eşleşmesi önerilir.

Wrap U/W
: U ve V eksenleri için sarma modu:

  - `WRAP_MODE_REPEAT`, [0,1] aralığının dışındaki doku verilerini tekrarlar.
  - `WRAP_MODE_MIRRORED_REPEAT`, [0,1] aralığının dışındaki doku verilerini tekrarlar, ancak her ikinci tekrar aynalanır.
  - `WRAP_MODE_CLAMP_TO_EDGE`, 1.0'dan büyük değerlerin doku verisini 1.0'a, 0.0'dan küçük değerlerinkini ise 0.0'a ayarlar---yani kenar pikselleri sınıra kadar tekrarlanır.

Filter Min/Mag
: Büyütme ve küçültme filtrelemesi. En yakın komşu filtreleme, doğrusal ara değerlemeden daha az hesaplama gerektirir, ancak örnekleme kaynaklı görüntü kusurlarına (aliasing) yol açabilir. Doğrusal ara değerleme genellikle daha pürüzsüz sonuçlar sağlar:

  - `Default`, `game.project` dosyasında `Graphics` altında `Default Texture Min Filter` ve `Default Texture Mag Filter` olarak belirtilen varsayılan filtre seçeneğini kullanır.
  - `FILTER_MODE_NEAREST`, koordinatları pikselin merkezine en yakın olan tekseli kullanır.
  - `FILTER_MODE_LINEAR`, pikselin merkezine en yakın 2x2 teksel dizisinin ağırlıklı doğrusal ortalamasını ayarlar.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST`, tek bir mipmap içindeki en yakın teksel değerini seçer.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR`, en uygun iki yakın mipmap içindeki en yakın tekseli seçer ve ardından bu iki değer arasında doğrusal ara değerleme yapar.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST`, tek bir mipmap içinde doğrusal ara değerleme yapar.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR`, iki haritanın her birindeki değeri hesaplamak için doğrusal ara değerleme kullanır ve ardından bu iki değer arasında doğrusal ara değerleme yapar.

Max Anisotropy
: Anizotropik filtreleme, birden çok örnek alıp sonuçları harmanlayan gelişmiş bir filtreleme tekniğidir. Bu ayar, doku örnekleyicilerinin anizotropi düzeyini kontrol eder. GPU anizotropik filtrelemeyi desteklemiyorsa parametrenin hiçbir etkisi olmaz ve varsayılan olarak 1'e ayarlanır.

## Sabit arabellekleri

İşleme hattı çizim yaparken sabit değerlerini varsayılan sistem sabit arabelleğinden alır. Varsayılan sabitleri geçersiz kılmak ve gölgelendirici programının uniform değerlerini bunun yerine işleme betiğinde kodla ayarlamak için özel bir sabit arabelleği oluşturabilirsiniz:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Yeni bir sabit arabelleği oluşturun
2. `tint` sabitini parlak kırmızıya ayarlayın
3. Özel sabitlerimizi kullanarak işleme yükleminin (render predicate) seçtiği bileşenleri çizin

Arabelleğin sabit öğelerine normal bir Lua tablosundaki gibi başvurulduğunu, ancak arabellek üzerinde `pairs()` veya `ipairs()` ile yineleme yapılamadığını unutmayın.
