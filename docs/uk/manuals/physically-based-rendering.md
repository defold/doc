---
title: Фізично обґрунтований рендеринг у Defold
brief: Цей посібник пояснює основи доступу до даних матеріалів для фізично обґрунтованого рендерингу в Defold.
---

# Фізично обґрунтований рендеринг (PBR) {#physically-based-rendering-pbr}

Фізично обґрунтований рендеринг (Physically Based Rendering, PBR) — це підхід до затінення, що моделює взаємодію світла з поверхнями на основі фізичних принципів реального світу. Він забезпечує узгоджене, реалістичне освітлення в різних середовищах і коректний вигляд ресурсів за широкого діапазону умов освітлення.

Реалізація PBR у Defold відповідає специфікації матеріалів glTF 2.0 та пов’язаним розширенням Khronos. Під час імпорту ресурсів glTF у Defold властивості матеріалів автоматично зчитуються та зберігаються як структуровані дані матеріалів, доступні в шейдерах під час виконання.

Матеріали PBR можуть містити такі ефекти, як металеві відбиття, шорсткість поверхні, світлопропускання, прозоре покриття, підповерхневе розсіювання, іризація тощо.

::: sidenote
Наразі Defold надає шейдерам доступ до даних матеріалів PBR, але не має вбудованої моделі освітлення PBR. Ви можете використовувати ці дані у власних шейдерах освітлення та відбиття для фізично обґрунтованого рендерингу. Стандартну модель освітлення PBR буде додано до Defold пізніше.
:::

::: sidenote
Вбудовані текстури з файлів glTF наразі не призначаються в Defold автоматично. Шейдерам доступні лише параметри матеріалів. Ви все одно можете вручну призначати текстури компонентам моделі та зчитувати з них значення у своєму шейдері.
:::

## Огляд властивостей матеріалів {#material-properties-overview}

Властивості матеріалів зчитуються з вихідних файлів glTF 2.0, призначених компоненту моделі. Не всі властивості є стандартними. Деякі надаються через необов’язкові розширення glTF, які засіб експорту файлу glTF може включати або не включати. Нижче відповідне розширення вказано в дужках після назви властивості.

Металевість і шорсткість
: Описує взаємодію світла з матеріалом. Стандартна модель PBR.

Дзеркальне відбиття й глянцевість (KHR_materials_pbrSpecularGlossiness)
: Альтернатива металевості й шорсткості. Часто використовується в старіших ресурсах.

Прозоре покриття (KHR_materials_clearcoat)
: Додає шар прозорого покриття з власною шорсткістю та картою нормалей.

Показник заломлення (KHR_materials_ior)
: Додає показник заломлення.

Дзеркальне відбиття (KHR_materials_specular)
: Додає окремий канал інтенсивності та кольору дзеркального відбиття.

Іризація (KHR_materials_iridescence)
: Імітує тонкоплівкову інтерференцію для таких матеріалів, як мильні бульбашки або перли.

Полиск (KHR_materials_sheen)
: Моделює відбиття на мікроповерхні, подібній до тканини.

Світлопропускання (KHR_materials_transmission)
: Моделює пропускання світла для прозорих або склоподібних матеріалів.

Об’єм (KHR_materials_volume)
: Підтримує об’ємні ефекти, як-от товщина та ослаблення світла.

Сила випромінювання (KHR_materials_emissive_strength)
: Керує яскравістю випромінювання незалежно від базового кольору.

Карта нормалей
: Карта нормалей для деталізації поверхні.

Карта оклюзії
: Карта оклюзії навколишнього освітлення.

Карта випромінювання
: Текстура власного випромінювання для поверхонь, що світяться.

Коефіцієнт випромінювання
: Множник RGB для інтенсивності випромінювання

Поріг відсікання альфа-каналу
: Поріг для прозорості за маскою.

Режим альфа-каналу
: Режими прозорості Opaque, Masked або Blended.

Двосторонній рендеринг
: Якщо значення дорівнює true, виконується рендеринг обох боків поверхні.

Без освітлення
: Якщо значення дорівнює true, матеріал оминає обчислення освітлення.

::: sidenote
Деякі з цих властивостей підказують, як слід виконувати рендеринг матеріалу. Дані властивостей (поріг відсікання альфа-каналу, режим альфа-каналу, двосторонній рендеринг і відсутність освітлення) доступні в шейдерах, але не впливають на спосіб рендерингу матеріалу в Defold.
:::

## Інтеграція з шейдерами {#shader-integration}

Дані матеріалів PBR стають доступними шейдерам на основі типів і правил іменування. Система матеріалів PBR надає шейдерам усі зчитані параметри матеріалів через структурований блок uniform із назвою `PbrMaterial`. Кожному підтримуваному розширенню glTF відповідає структура в цьому блоці, яку можна компілювати умовно за допомогою прапорців `#define`.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Різні можливості матеріалу визначаються в шейдері як фіксовані структури. Дані максимально упаковано у `vec4`, оскільки саме так константи задаються всередині Defold. Там, де дані упаковано, це зазначено в коментарях у наведених нижче фрагментах шейдера для кожної можливості:

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

Спільні властивості задаються в самому блоці uniform матеріалу (і знову зверніть увагу на пакування даних у `vec4`).

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

### Приклад шейдера {#example-shader}

Ось приклад шейдера, який містить усі можливості та запропоновану схему іменування прив’язок текстур (нагадуємо, що їх потрібно задавати вручну). Зауважте, що ви можете вимикати можливості, просто використовуючи `#define` навколо кожного поля самого `PbrMaterial`, як показано в прикладі нижче:

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
Якщо в структурі матеріалу не знайдено певних полів даних, дані відповідних можливостей не буде задано. Наприклад, якщо в структурі матеріалу немає `pbrClearCoat`, дані прозорого покриття не буде задано. Якщо блок uniform не знайдено, під час рендерингу не буде задано жодних даних.
:::

### Константи {#constants}

Кожній властивості матеріалу відповідає внутрішня константа рендерингу в Defold. Ви можете перевизначити стандартні значення, задавши константи в самому ресурсі матеріалу за схемою іменування `pbrFeature.structMember`. Ці значення буде застосовано автоматично, якщо відповідні дані відсутні в матеріалі glTF.

![Константи матеріалу](images/physically-based-rendering/material-constants.png)

## Наступні кроки {#next-steps}

Щоб використовувати дані матеріалів для фізично обґрунтованого освітлення, реалізуйте BRDF у своєму фрагментному шейдері, використовуючи параметри з блоку `PbrMaterial`.
Див. також:

* [Посібник із шейдерів](/manuals/shader)
* [Посібник із рендерингу](/manuals/render)
* [Специфікація glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
