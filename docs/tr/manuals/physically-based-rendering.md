---
title: Defold'da fiziksel tabanlı işleme
brief: Bu kılavuz, Defold'da fiziksel tabanlı işleme için materyal verilerine erişmenin temellerini açıklar.
---

# Fiziksel tabanlı işleme (PBR)

Fiziksel tabanlı işleme (Physically Based Rendering, PBR), görüntü oluştururken ışığın yüzeylerle etkileşimini gerçek dünyadaki fizik ilkelerini kullanarak modelleyen bir gölgelendirme yaklaşımıdır. Farklı ortamlarda tutarlı, gerçekçi aydınlatma sağlar ve varlıkların (asset) çok çeşitli aydınlatma koşullarında doğru görünmesini mümkün kılar.

Defold'un PBR uygulaması, glTF 2.0 materyal (material) belirtimini ve ilgili Khronos uzantılarını izler. glTF varlıklarını Defold'a içe aktardığınızda materyal özellikleri otomatik olarak ayrıştırılır ve çalışma sırasında gölgelendiricilerden (shader) erişilebilen yapılandırılmış materyal verileri olarak saklanır.

PBR materyalleri metalik yansımalar, yüzey pürüzlülüğü, ışık geçirimi, saydam kaplama, yüzey altı saçılma, yanardönerlik gibi etkiler ve daha fazlasını içerebilir.

::: sidenote
Defold şu anda PBR materyal verilerini gölgelendiricilere sunar, ancak yerleşik bir PBR aydınlatma modeli sağlamaz. Fiziksel tabanlı işleme elde etmek için bu verileri kendi aydınlatma ve yansıma gölgelendiricilerinizde kullanabilirsiniz. Defold'a ileride varsayılan bir PBR aydınlatma modeli eklenecektir.
:::

::: sidenote
glTF dosyalarındaki gömülü dokular (texture) şu anda Defold'da otomatik olarak atanmaz. Gölgelendiricilere yalnızca materyal parametreleri sunulur. Yine de dokuları model bileşenlerine (model component) elle atayabilir ve gölgelendiricinizde bunlardan örnekleme yapabilirsiniz.
:::

## Materyal özelliklerine genel bakış

Materyal özellikleri, bir model bileşenine atanan glTF 2.0 kaynak dosyalarından ayrıştırılır. Özelliklerin tümü standart değildir. Bazıları isteğe bağlı glTF uzantıları aracılığıyla sağlanır; glTF dosyasını dışa aktarmak için kullanılan araç bu uzantıları dosyaya dahil edebilir veya etmeyebilir. İlgili uzantı aşağıda özellik adından sonra parantez içinde belirtilmiştir.

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
: Değeri true ise yüzeyin her iki tarafı da işlenir.

Aydınlatmasız
: Değeri true ise materyal aydınlatma hesaplamalarını atlar.

::: sidenote
Bu özelliklerden bazıları, materyalin nasıl işlenmesi gerektiğine ilişkin ipuçları sağlar. Bu özelliklerin (alfa kesme eşiği, alfa modu, çift taraflı ve aydınlatmasız) verilerine gölgelendiricilerden erişilebilir, ancak bu veriler materyalin Defold'da nasıl işlendiğini etkilemez.
:::

## Gölgelendiriciyle bütünleştirme

PBR materyal verileri, türlere ve adlandırma kuralına göre gölgelendiricilere sunulur. PBR materyal sistemi, ayrıştırılan tüm materyal parametrelerini `PbrMaterial` adlı yapılandırılmış bir uniform bloğu aracılığıyla gölgelendiricilere sağlar. Desteklenen her glTF uzantısı, bu blok içinde `#define` bayrakları kullanılarak koşullu olarak derlenebilen bir yapıya (struct) karşılık gelir.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Materyalin çeşitli özellikleri, gölgelendiricide sabit yapılar olarak tanımlanır. Defold'un iç işleyişinde sabitler bu şekilde ayarlandığından, veriler mümkün olduğunca `vec4` değerleri içinde bir araya getirilmiştir. Verilerin bu şekilde birleştirildiği durumlar, aşağıda her özelliğe ait gölgelendirici kod parçalarında yorumlarla belirtilmiştir:

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
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
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

Ortak özellikler doğrudan materyalin uniform bloğunda ayarlanır (burada da verilerin `vec4` içinde bir araya getirildiğine dikkat edin).

```glsl
// Common textures
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// Common properties:

	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Other properties...
};
```

### Örnek gölgelendirici

Aşağıda, tüm özellikleri ve doku bağlamaları için önerilen bir adlandırma şemasını içeren örnek bir gölgelendirici verilmiştir (bu bağlamaların yine elle yapılması gerekir). Aşağıdaki örnekte gösterildiği gibi, `PbrMaterial` bloğunun her bir üyesinin çevresinde `#define` kullanarak özellikleri kapatabileceğinizi unutmayın:

```glsl
// Feature flags, comment or remove these to slim down the shader.
#define PBR_METALLIC_ROUGHNESS
#define PBR_SPECULAR_GLOSSINESS
#define PBR_CLEARCOAT
#define PBR_TRANSMISSION
#define PBR_IOR
#define PBR_SPECULAR
#define PBR_VOLUME
#define PBR_SHEEN
#define PBR_EMISSIVE_STRENGTH
#define PBR_IRIDESCENCE

// Common
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

// PbrSpecularGlossiness
uniform sampler2D PbrSpecularGlossiness_diffuseTexture;
uniform sampler2D PbrSpecularGlossiness_specularGlossinessTexture;

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Default=1.0), A: glossiness (Default=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: use diffuseTexture, G: use specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

// PbrClearCoat
uniform sampler2D PbrClearCoat_clearcoatTexture;
uniform sampler2D PbrClearCoat_clearcoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearcoatNormalTexture;

struct PbrClearCoat
{
	// R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

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

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Default=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: use specularTexture, G: use specularColorTexture
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
	vec4 attenuationDistance;
	// R: use thicknessTexture
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

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

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: use iridescenceTexture, G: use iridescenceThicknessTexture
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// Common properties
	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Features
#ifdef PBR_METALLIC_ROUGHNESS
	PbrMetallicRoughness  pbrMetallicRoughness;
#endif
#ifdef PBR_SPECULAR_GLOSSINESS
	PbrSpecularGlossiness pbrSpecularGlossiness;
#endif
#ifdef PBR_CLEARCOAT
	PbrClearCoat pbrClearCoat;
#endif
#ifdef PBR_TRANSMISSION
	PbrTransmission pbrTransmission;
#endif
#ifdef PBR_IOR
	PbrIor pbrIor;
#endif
#ifdef PBR_SPECULAR
	PbrSpecular pbrSpecular;
#endif
#ifdef PBR_VOLUME
	PbrVolume pbrVolume;
#endif
#ifdef PBR_SHEEN
	PbrSheen pbrSheen;
#endif
#ifdef PBR_EMISSIVE_STRENGTH
	PbrEmissiveStrength pbrEmissiveStrength;
#endif
#ifdef PBR_IRIDESCENCE
	PbrIridescence pbrIridescence;
#endif
};
```

::: sidenote
Materyal yapısında belirli veri alanları bulunamazsa bu özelliklere ait veriler ayarlanmaz. Örneğin, materyal yapısında `pbrClearCoat` yoksa saydam kaplama verisi ayarlanmaz. Uniform bloğu bulunamazsa işleme sırasında hiçbir veri ayarlanmaz.
:::

### Sabitler

Her materyal özelliği, Defold'un iç işleyişindeki bir işleme sabitine karşılık gelir. `pbrFeature.structMember` adlandırma kalıbını izleyerek doğrudan materyal kaynağında sabitler tanımlayabilir ve varsayılan değerleri geçersiz kılabilirsiniz. glTF materyalinde karşılık gelen veriler eksikse bu değerler otomatik olarak uygulanır.

![Materyal sabitleri](images/physically-based-rendering/material-constants.png)

## Sonraki adımlar

Materyal verilerini fiziksel tabanlı aydınlatma için kullanmak üzere, `PbrMaterial` bloğunda sağlanan parametreleri kullanarak parça gölgelendiricinizde bir BRDF uygulayın.
Ayrıca bakınız:

* [Gölgelendiriciler kılavuzu](/manuals/shader)
* [İşleme kılavuzu](/manuals/render)
* [glTF 2.0 belirtimi](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
