---
title: Defold'da fiziksel tabanlı işleme
brief: Bu kılavuz, Defold'da yerleşik PBR materyallerini kullanmayı ve fiziksel tabanlı gölgelendirmeyi özelleştirmeyi açıklar.
---

# Fiziksel tabanlı işleme (PBR) {#physically-based-rendering-pbr}

Fiziksel tabanlı işleme (Physically Based Rendering, PBR), ışığın yüzeylerle etkileşimini fizik ilkelerini kullanarak modelleyen bir gölgelendirme yaklaşımıdır. Temel renk, metaliklik çarpanı ve pürüzlülük gibi materyal özellikleri, yüzeyi sahnenin aydınlatmasından bağımsız olarak tanımlar.

Yerleşik glTF materyalleri PBR aydınlatması sağlar. Defold ayrıca içe aktarılan glTF 2.0 materyal özelliklerini ve desteklenen Khronos uzantılarının verilerini özel gölgelendiricilere sunar.

## Yerleşik PBR materyalleri {#built-in-pbr-materials}

Bir glTF veya GLB dosyasını [Model bileşeninin](/manuals/model) *Scene* özelliğine atayın. Düzenleyici materyalleri ve dokuları doldurmayı önerdiğinde sahnenin oluşturulan materyal eşlemelerini uygulamak ve varsa mevcut eşlemeleri değiştirmek için <kbd>Auto Fill</kbd> seçeneğini seçin. Bu materyaller yerleşik glTF gölgelendiricilerini kullanır ve gömülü görüntülere doğrudan başvurabilir. Eşlemelerinizi koruyup materyalleri ve dokuları elle atamak için <kbd>Keep Current</kbd> seçeneğini seçin. Gömülü kaynaklara göz atma ve tek tek örgü seçme için [model içe aktarma iş akışına](/manuals/importing-models/#using-a-model) bakın.

Aşağıdaki materyaller `/builtins/materials/` altında bulunur. Modelinize ve örnek oluşturma (instancing) kullanıp kullanmadığına uygun çeşidi seçin:

| Model türü | Materyal |
|---|---|
| Statik, örnek oluşturma kullanılmayan | `gltf.material` |
| Statik, örnek oluşturma kullanılan | `gltf_instanced.material` |
| İskelete bağlı (animasyonlu), örnek oluşturma kullanılmayan | `gltf_skinned.material` |
| İskelete bağlı (animasyonlu), örnek oluşturma kullanılan | `gltf_skinned_instanced.material` |

Dördü de yerel köşe uzayını ve aynı `gltf.fp` parça gölgelendiricisini kullanır. İskelete bağlı çeşitler, iskelete bağlama işlemini GPU üzerinde gerçekleştirir. GPU üzerinde iskelete bağlama ve örnek oluşturma için [model materyali gereksinimlerine](/manuals/model/#material) bakın.

Elle doku eşleme yaparken yerleşik materyaller şu örnekleyici adlarını kullanır:

| Doku | Örnekleyici | Kullanılan veri |
|---|---|---|
| Temel renk | `PbrMetallicRoughness_baseColorTexture` | RGB rengi ve alfa |
| Metaliklik/pürüzlülük | `PbrMetallicRoughness_metallicRoughnessTexture` | G kanalında pürüzlülük, B kanalında metaliklik |
| Normal | `PbrMaterial_normalTexture` | RGB kanallarında teğet uzayındaki normal |
| Örtme | `PbrMaterial_occlusionTexture` | R kanalında örtme |
| Işık yayma | `PbrMaterial_emissiveTexture` | RGB rengi |

Bir [kamera](/manuals/camera/#using-the-camera) kurun ve modeli aydınlatmak için [ışık bileşenleri](/manuals/light) ekleyin. Gölgelendirici, doğrudan aydınlatma için yönlü, noktasal ve spot ışıkları; basit bir ortam katkısı için de ortam ışıklarını kullanır. Materyaller, varsayılan işleme betiğinin çizdiği `model` etiketine sahiptir. Özel bir işleme betiği eşleşen bir yüklem çizmelidir.

### Yerleşik gölgelendiricinin davranışı {#built-in-shader-behavior}

Yerleşik gölgelendiriciler; metaliklik/pürüzlülük gölgelendirmesini, temel renk ve köşe rengini, teğet verileri bulunduğunda normal eşlemeyi, örtmeyi ve ışık yayma gücü dahil ışık yaymayı uygular. Aydınlatma için temel renk ve ışık yayma dokuları sRGB'den çözülür ve son renk tekrar sRGB'ye dönüştürülür. Metaliklik/pürüzlülük, normal ve örtme haritaları doğrusal veriler içerir.

Gölgelendirici, aydınlatmasız materyalleri ve maskeli alfayı dikkate alır; çift taraflı yüzeyler için normalleri ayarlar. İşleme durumu yine önemlidir:

- Çift taraflı materyallerde arka yüzlerin gölgelendiriciye ulaşması için ilgili işleme geçişinde yüz elemeyi devre dışı bırakın.
- Harmanlanan alfa için gölgelendirici düz alfa çıktısı verir. `graphics.BLEND_FACTOR_SRC_ALPHA` ve `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` ile harmanlamayı etkinleştirin; saydam nesnelerin çizim sırasını ve derinlik yazmalarını işleme betiğinizde yönetin. Varsayılan model geçişi harmanlamayı otomatik etkinleştirmez.

Yerleşik ortam katkısı, ortam haritası aydınlatması veya gölgeler içermeyen yaklaşık bir hesaplamadır. Saydam kaplama, ışık geçirimi, parıltı, yanardönerlik ve aynasal yansıma/parlaklık iş akışı gibi efektler özel gölgelendirme gerektirir; parametrelerini içe aktarmak bu efektleri `gltf.fp` içinde etkinleştirmez.

## Materyal özelliklerine genel bakış {#material-properties-overview}

Aşağıdaki özellikler, bir model bileşenine atanan glTF 2.0 kaynak dosyalarından ayrıştırılır. Liste, kullanılabilir materyal verilerini açıklar; yerleşik aydınlatma yukarıda açıklanan alt kümeyi kullanır. Özelliklerin tümü standart değildir. Bazıları isteğe bağlı glTF uzantıları aracılığıyla sağlanır; glTF dosyasını dışa aktarmak için kullanılan araç bu uzantıları dosyaya dahil edebilir veya etmeyebilir. İlgili uzantı aşağıda özellik adından sonra parantez içinde belirtilmiştir.

Metaliklik ve pürüzlülük
: Işığın materyalle nasıl etkileştiğini açıklar. Varsayılan PBR modelidir.

Aynasal yansıma ve parlaklık (KHR_materials_pbrSpecularGlossiness)
: Metaliklik ve pürüzlülük modeline bir alternatiftir. Genellikle eski varlıklarda kullanılır.

Saydam kaplama (KHR_materials_clearcoat)
: Kendi pürüzlülüğü ve normal haritası olan saydam bir kaplama katmanı ekler.

Kırılma indisi (KHR_materials_ior)
: Bir kırılma indisi ekler.

Aynasal yansıma (KHR_materials_specular)
: Aynasal yansımanın şiddeti ve rengi için özel bir kanal ekler.

Yanardönerlik (KHR_materials_iridescence)
: Sabun köpükleri veya inciler gibi materyaller için ince film girişimini simüle eder.

Parıltı (KHR_materials_sheen)
: Kumaş benzeri mikro yüzey yansımalarını modeller.

Işık geçirimi (KHR_materials_transmission)
: Saydam veya cam benzeri materyaller için ışık geçirimini modeller.

Hacim (KHR_materials_volume)
: Kalınlık ve zayıflama gibi hacimsel etkileri destekler.

Işık yayma gücü (KHR_materials_emissive_strength)
: Yayılan ışığın parlaklığını temel renkten bağımsız olarak denetler.

Normal haritası
: Yüzey ayrıntıları için normal haritası.

Örtme haritası
: Ortam örtme haritası.

Işık yayma haritası
: Parlayan yüzeyler için kendi ışığını yayan doku.

Işık yayma çarpanı
: Yayılan ışığın şiddeti için RGB çarpanı

Alfa kesme eşiği
: Maskeli saydamlık için eşik.

Alfa modu
: Opaque, Masked veya Blended saydamlık modları.

Çift taraflı
: Yüzeyin iki tarafının da işlenmesini ister. İşleme geçişi, arka yüzlerin gölgelendiriciye ulaşmasına izin vermelidir.

Aydınlatmasız
: Değeri true ise materyal aydınlatma hesaplamalarını atlar.


## Gölgelendiriciyle bütünleştirme {#shader-integration}

Aşağıdaki bölümler özel gölgelendiricileri ele alır. Uygun yerleşik `.material` kaynağını ve `gltf.fp` dosyasını projenize kopyalayın, ardından kopyalanan materyalin *Fragment Program* özelliğini kendi gölgelendiricinize yönlendirin. Bu arayüzleri de değiştirmiyorsanız eşleşen glTF köşe programını, örnekleyici adlarını ve yerel köşe uzayını koruyun.

Yerleşik yardımcılar, doku örneklemeyi yüzey hazırlığından, BRDF hesaplamalarından ve aydınlatmadan ayırır. `gltf_sampling.glsl`, ham `PbrMaterial` uniform bloğunu okur ve çözümlenmiş, doğrusal materyal girdilerini içeren bir `PBRMaterial` değeri üretir. `gltf_lighting.glsl`, doğrudan ve ortam aydınlatmasını sağlar ve katkılarını birleştirir. Büyük/küçük harf kullanımı, ham uniform bloğunu örneklenmiş materyal yapısından ayırt eder.

### Örnek gölgelendirici {#example-shader}

Bu parça gölgelendiricisi, yerleşik aydınlatmayı korurken en düşük pürüzlülüğü yükseltir. Dört glTF materyal çeşidinin tümünün kullandığı köşe programlarıyla çalışır:

```glsl
#version 140

#include "/builtins/materials/gltf_sampling.glsl"
#include "/builtins/materials/gltf_lighting.glsl"

out vec4 out_fragColor;

void main()
{
    PBRMaterial inputs = pbr_sample_material(var_texcoord0, var_color);
    inputs.roughness = max(inputs.roughness, 0.35);

    // Sample textures, including the normal map, before discarding fragments.
    PBRSurface surface = pbr_sample_surface(inputs, var_texcoord0);
    if ((!inputs.doubleSided && !gl_FrontFacing) || pbr_should_discard_alpha(inputs))
    {
        discard;
    }

    // Derive BRDF values after editing the material inputs.
    MaterialInfo material = pbr_create_material_info(inputs);
    PBRLighting lighting = pbr_create_lighting();
    if (!inputs.unlit)
    {
        lighting.direct = pbr_evaluate_direct_lighting(material, surface, var_view);
        lighting.indirect = pbr_evaluate_ambient_lighting(material, ambient_light());
    }

    vec3 color = pbr_compose_lighting(inputs, lighting, inputs.occlusion, inputs.occlusion);
    out_fragColor = vec4(pbr_linear_to_srgb(color), pbr_get_alpha(inputs));
}
```

`pbr_create_material_info()` çağrısından önce örneklenmiş materyal girdilerini düzenleyin. Bir yüzeyin görünüm uzayındaki konumunu veya normallerini değiştirirseniz türetilmiş dünya uzayı alanlarını güncellemek için `pbr_finalize_surface(surface, var_view)` çağırın. Özel bir BRDF veya tek tek ışık katkıları için yerleşik yardımcılardaki `pbr_evaluate_brdf()` ve `pbr_evaluate_light()` işlevlerini kullanın veya değiştirin.

`lighting.indirect` değerini kendi ortam aydınlatmanız veya genel aydınlatmanızla değiştirebilirsiniz. Dağınık ve aynasal yansıma katkıları doğrusal çıkan ışıktır; bu nedenle materyalin BRDF'sini ikinci kez uygulamayın. Gölge görünürlüğünü uygun doğrudan ışık katkısına uygulayın; `pbr_compose_lighting()` işlevinin görünürlük bağımsız değişkenleri yalnızca dolaylı aydınlatmayı etkiler. HDR hattı için ara hedefe doğrusal renk yazın ve sRGB dönüşümünü son geçişte yapın.

### Ham materyal verileri {#raw-material-data}

Tamamen özel bir gölgelendirici için tanınan üye adlarını ve türlerini içeren `PbrMaterial` adlı bir uniform bloğu bildirin. Defold, eşleşen alanları kaynak glTF materyalinden doldurur. Aşağıdaki bildirimler kullanılabilir özellik yapılarını açıklar; yalnızca gölgelendiricinizin ihtiyaç duyduklarını ekleyin. Yapıyı bildirmek veri sağlar, ancak örnekleme ve aydınlatma davranışını gölgelendiriciniz uygulamalıdır.

Bunları zaten bildiren `gltf_sampling.glsl` dosyasını dahil ederken uniform bloğunu veya `PbrMetallicRoughness` yapısını yeniden bildirmeyin. Aşağıdaki bildirimler, kendi materyal girdilerini yöneten gölgelendiriciler için bir alternatiftir.

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
    vec4 diffuseFactor;
    // RGB: specular (Default=1.0), A: glossiness (Default=1.0)
    vec4 specularAndSpecularGlossinessFactor;
    // R: use diffuseTexture, G: use specularGlossinessTexture
    vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
    // R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
    vec4 clearCoatAndClearCoatRoughnessFactor;
    // R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
    vec4 clearCoatTextures;
};

struct PbrTransmission
{
    // R: transmission (Default=0.0)
    vec4 transmissionFactor;
    // R: use transmissionTexture
    vec4 transmissionTextures;
};

struct PbrIor
{
    // R: ior (Default=0.0)
    vec4 ior;
};

struct PbrSpecular
{
    // RGB: specularColor, A: specularFactor (Default=1.0);
    vec4 specularColorAndSpecularFactor;
    // R: use specularTexture, G: use specularColorTexture
    vec4 specularTextures;
};

struct PbrVolume
{
    // R: thicknessFactor (Default=0.0), GBA: attenuationColor
    vec4 thicknessFactorAndAttenuationColor;
    // R: attenuationDistance (Default=-1.0)
    vec4 attenuationDistance;
    // R: use thicknessTexture
    vec4 volumeTextures;
};

struct PbrSheen
{
    // RGB: sheenColor, A: sheenRoughnessFactor (Default=0.0)
    vec4 sheenColorAndRoughnessFactor;
    // R: use sheenColorTexture, G: use sheenRoughnessTexture
    vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
    // R: emissiveStrength (Default=1.0)
    vec4 emissiveStrength;
};

struct PbrIridescence
{
    // R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
    vec4 iridescenceFactorAndIorAndThicknessMinMax;
    // R: use iridescenceTexture, G: use iridescenceThicknessTexture
    vec4 iridescenceTextures;
};
```

Ortak özellikler ve özellik yapıları uniform bloğunun üyeleridir. Paketlenmiş bileşenler şöyledir:

```glsl
uniform PbrMaterial
{
    // X: alpha cutoff, Y: double-sided, Z: unlit,
    // W: alpha mode (0 = opaque, 1 = mask, 2 = blend)
    vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
    // X: has normal texture, Y: has occlusion texture, Z: has emissive texture
    vec4 pbrCommonTextures;
    // RGB: emissive factor, W: emissive strength
    vec4 pbrEmissiveFactorAndStrength;
    // X: normal scale, Y: occlusion strength
    vec4 pbrNormalScaleAndOcclusionStrength;

    PbrMetallicRoughness pbrMetallicRoughness;
    PbrSpecularGlossiness pbrSpecularGlossiness;
    PbrClearCoat pbrClearCoat;
    PbrTransmission pbrTransmission;
    PbrIor pbrIor;
    PbrSpecular pbrSpecular;
    PbrVolume pbrVolume;
    PbrSheen pbrSheen;
    PbrEmissiveStrength pbrEmissiveStrength;
    PbrIridescence pbrIridescence;
};
```

Kullanılmayan özellik üyelerini bloktan çıkarın. Blok veya bir özelliğin tanınan alanları yoksa ilgili veriler sağlanmaz. Doku varlığı bayrakları, kaynak materyalin doku başvurularını açıklar; özel bir materyalin, örneklediği haritalar için yine de eşleşen örnekleyici bildirimlerine ve doku eşlemelerine ihtiyacı vardır.

### Sabitler {#constants}

Özellik alanları `pbrMetallicRoughness.baseColorFactor`, ortak alanlar ise `pbrEmissiveFactorAndStrength` gibi adlar kullanır. Motor bu sabitleri içe aktarılan materyalden veya modelde materyal verisi yoksa varsayılan materyalden doldurur. `.material` kaynağında varsayılanlar ayarlamak, içe aktarılan değerleri geçersiz kılmaz.

Yerleşik gölgelendirmeyi özelleştirmek için yukarıdaki örnekte olduğu gibi BRDF değerlerini türetmeden önce örneklenmiş `PBRMaterial` değerini düzenleyin. Ek çalışma zamanı denetimleri için kendi gölgelendirici sabitlerinizi bildirin ve [model materyali sabiti API'sini](/manuals/model/#material-constants) kullanın.

## Sonraki adımlar {#next-steps}

Standart glTF metaliklik/pürüzlülük iş akışı için yerleşik materyalleri kullanın. Farklı bir BRDF, ortam aydınlatması, gölgeler veya ek glTF materyal efektleri gerektiğinde gölgelendirici yardımcılarını genişletin ya da kendi materyalinizi sağlayın.

Ayrıca bakın:

* [Işık kılavuzu](/manuals/light)
* [Materyal kılavuzu](/manuals/material)
* [Gölgelendiriciler kılavuzu](/manuals/shader)
* [İşleme kılavuzu](/manuals/render)
* [glTF 2.0 belirtimi](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
