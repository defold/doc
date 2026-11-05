---
title: Физически корректный рендеринг в Defold
brief: В этом руководстве описано, как использовать встроенные PBR-материалы и настраивать физически корректное затенение в Defold.
---

# Physically Based Rendering (PBR)

Physically Based Rendering (PBR) — подход к затенению, моделирующий взаимодействие света с поверхностями на основе физических принципов. Свойства материала, такие как базовый цвет, металличность и шероховатость, описывают поверхность независимо от освещения сцены.

Встроенные материалы glTF предоставляют PBR-освещение. Defold также предоставляет пользовательским шейдерам импортированные свойства материалов glTF 2.0 и данные поддерживаемых расширений Khronos.

## Встроенные PBR-материалы {#built-in-pbr-materials}

Назначьте файл glTF или GLB в свойстве *Scene* [компонента Model](/manuals/model). Когда редактор предложит заполнить материалы и текстуры, выберите <kbd>Auto Fill</kbd>, чтобы применить сгенерированные привязки материалов сцены, заменив существующие. Эти материалы используют встроенные шейдеры glTF и могут напрямую ссылаться на встроенные изображения. Выберите <kbd>Keep Current</kbd>, чтобы сохранить привязки и назначить материалы и текстуры вручную. Просмотр встроенных ресурсов и выбор отдельных сеток описаны в [порядке импорта модели](/manuals/importing-models/#using-a-model).

Следующие материалы доступны в `/builtins/materials/`. Выберите вариант, соответствующий модели и использованию инстансинга:

| Тип модели | Материал |
|---|---|
| Статическая, без инстансинга | `gltf.material` |
| Статическая, с инстансингом | `gltf_instanced.material` |
| Со скиннингом (анимированная), без инстансинга | `gltf_skinned.material` |
| Со скиннингом (анимированная), с инстансингом | `gltf_skinned_instanced.material` |

Все четыре используют локальное пространство вершин и один фрагментный шейдер `gltf.fp`. Варианты со скиннингом выполняют его на GPU. См. [требования к материалам моделей](/manuals/model/#material) для GPU-скиннинга и инстансинга.

Для ручной привязки текстур встроенные материалы используют следующие имена сэмплеров:

| Текстура | Сэмплер | Используемые данные |
|---|---|---|
| Базовый цвет | `PbrMetallicRoughness_baseColorTexture` | Цвет RGB и альфа |
| Металличность/шероховатость | `PbrMetallicRoughness_metallicRoughnessTexture` | Шероховатость в G, металличность в B |
| Нормали | `PbrMaterial_normalTexture` | Нормаль в касательном пространстве в RGB |
| Затенение | `PbrMaterial_occlusionTexture` | Затенение в R |
| Свечение | `PbrMaterial_emissiveTexture` | Цвет RGB |

Настройте [камеру](/manuals/camera/#using-the-camera) и добавьте [компоненты источников света](/manuals/light) для освещения модели. Для прямого освещения шейдер использует направленные, точечные и прожекторные источники, а также фоновое освещение для простого вклада окружающего света. Материалы имеют тег `model`, который отрисовывает стандартный рендер-скрипт. Пользовательский рендер-скрипт должен отрисовывать соответствующий предикат.

### Поведение встроенного шейдера {#built-in-shader-behavior}

Встроенные шейдеры реализуют затенение metallic/roughness, базовый цвет и цвет вершин, карты нормалей при наличии данных касательных, затенение и свечение, включая его интенсивность. Для освещения текстуры базового цвета и свечения декодируются из sRGB, а итоговый цвет преобразуется обратно в sRGB. Карты металличности/шероховатости, нормалей и затенения содержат линейные данные.

Шейдер учитывает неосвещаемые материалы и маскированную альфа-прозрачность, а также корректирует нормали для двусторонних поверхностей. Состояние рендеринга по-прежнему важно:

- Для двусторонних материалов отключите отсечение граней в соответствующем проходе рендеринга, чтобы обратные грани попадали в шейдер.
- Для смешиваемой альфа-прозрачности шейдер выводит непредумноженную альфу. Включите смешивание с `graphics.BLEND_FACTOR_SRC_ALPHA` и `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA`, управляйте порядком отрисовки прозрачных объектов и записью глубины в рендер-скрипте. Стандартный проход моделей не включает смешивание автоматически.

Встроенный вклад фонового освещения — приближение, без освещения картой окружения и теней. Эффекты clearcoat, transmission, sheen, iridescence и подход specular/glossiness требуют собственного затенения; импорт их параметров не включает эти эффекты в `gltf.fp`.

## Обзор свойств материалов {#material-properties-overview}

Следующие свойства извлекаются из исходных файлов glTF 2.0, назначенных компоненту Model. Список описывает доступные данные материала; встроенное освещение использует подмножество, описанное выше. Не все свойства являются стандартными. Некоторые предоставляются через необязательные расширения glTF, которые могут присутствовать или отсутствовать в зависимости от инструмента экспорта glTF-файла. Соответствующее расширение указано в скобках после имени свойства ниже.

Metallic roughness
: Описывает, как свет взаимодействует с материалом. Это стандартная PBR-модель по умолчанию.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: Альтернатива metallic roughness. Часто используется в более старых ассетах.

Clearcoat (KHR_materials_clearcoat)
: Добавляет прозрачный слой покрытия с собственной шероховатостью и normal map.

Ior (KHR_materials_ior)
: Добавляет показатель преломления.

Specular (KHR_materials_specular)
: Добавляет отдельный канал интенсивности и цвета specular.

Iridescence (KHR_materials_iridescence)
: Имитирует интерференцию в тонкой плёнке для материалов вроде мыльных пузырей или перламутра.

Sheen (KHR_materials_sheen)
: Моделирует микроповерхностные отражения, характерные для ткани.

Transmission (KHR_materials_transmission)
: Моделирует прохождение света через прозрачные или стеклоподобные материалы.

Volume (KHR_materials_volume)
: Поддерживает объёмные эффекты, такие как толщина и attenuation.

Emissive strength (KHR_materials_emissive_strength)
: Управляет яркостью свечения независимо от базового цвета.

Normal map
: Карта нормалей для поверхностных деталей.

Occlusion map
: Карта ambient occlusion.

Emissive map
: Текстура самосвечения для светящихся поверхностей.

Emissive factor
: RGB-множитель интенсивности свечения.

Alpha cutoff
: Порог для маскированной прозрачности.

Alpha mode
: Режим прозрачности: Opaque, Masked или Blended.

Double sided
: Запрашивает отрисовку обеих сторон поверхности. Проход рендеринга должен позволять обратным граням попадать в шейдер.

Unlit
: Если true, материал не участвует в вычислениях освещения.

## Интеграция с шейдерами {#shader-integration}

Следующие разделы посвящены пользовательским шейдерам. Скопируйте подходящий встроенный ресурс `.material` и `gltf.fp` в проект, затем укажите свой шейдер в *Fragment Program* скопированного материала. Сохраните соответствующую вершинную программу glTF, имена сэмплеров и локальное пространство вершин, если не заменяете эти интерфейсы.

Встроенные вспомогательные функции разделяют выборку текстур, подготовку поверхности, вычисления BRDF и освещение. `gltf_sampling.glsl` читает исходный uniform-блок `PbrMaterial` и создаёт значение `PBRMaterial` с разрешёнными линейными входными данными материала. `gltf_lighting.glsl` предоставляет прямое и фоновое освещение и объединяет их вклады. Регистр букв отличает исходный uniform-блок от структуры материала с выбранными данными текстур.

### Пример шейдера {#example-shader}

Этот фрагментный шейдер повышает минимальную шероховатость, сохраняя встроенное освещение. Он работает с вершинными программами всех четырёх вариантов материалов glTF:

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

Изменяйте входные данные материала после выборки до вызова `pbr_create_material_info()`. Если меняете положение поверхности в пространстве вида или её нормали, вызовите `pbr_finalize_surface(surface, var_view)` для обновления производных полей в мировом пространстве. Для собственной BRDF или вклада отдельных источников света используйте либо замените `pbr_evaluate_brdf()` и `pbr_evaluate_light()` из встроенных вспомогательных функций.

Можно заменить `lighting.indirect` собственным освещением окружения или глобальным освещением. Его диффузный и зеркальный вклады — линейный исходящий свет, поэтому не применяйте BRDF материала второй раз. Применяйте видимость теней к соответствующему вкладу прямого света; аргументы видимости `pbr_compose_lighting()` влияют только на непрямое освещение. Для HDR-конвейера записывайте линейный цвет в промежуточную цель, а преобразование sRGB выполняйте в финальном проходе.

### Исходные данные материала {#raw-material-data}

Для полностью собственного шейдера объявите uniform-блок `PbrMaterial` с распознаваемыми именами и типами членов. Defold заполняет соответствующие поля из исходного материала glTF. Объявления ниже описывают доступные структуры свойств; включайте только нужные шейдеру. Объявление структуры предоставляет данные, но шейдер должен сам реализовать их выборку и поведение освещения.

Не объявляйте повторно uniform-блок или `PbrMetallicRoughness` при включении `gltf_sampling.glsl`, который уже их объявляет. Следующие объявления — альтернатива для шейдеров, управляющих собственными входными данными материала.

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

Общие свойства и структуры отдельных возможностей являются членами uniform-блока. Упакованные компоненты:

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

Исключайте из блока неиспользуемые члены. Если блок или распознаваемые поля возможности отсутствуют, соответствующие данные не передаются. Флаги наличия текстур описывают ссылки на текстуры в исходном материале; пользовательскому материалу по-прежнему нужны соответствующие объявления сэмплеров и привязки текстур для карт, из которых он делает выборку.

### Константы {#constants}

Поля отдельных возможностей используют имена вида `pbrMetallicRoughness.baseColorFactor`; общие поля — имена вида `pbrEmissiveFactorAndStrength`. Движок заполняет эти константы из импортированного материала либо из материала по умолчанию, если модель не содержит данных материала. Значения по умолчанию в ресурсе `.material` не переопределяют импортированные значения.

Для настройки встроенного затенения изменяйте полученный после выборки `PBRMaterial` до вычисления значений BRDF, как в примере выше. Для дополнительных средств управления во время выполнения объявите собственные константы шейдера и используйте [API констант материала модели](/manuals/model/#material-constants).

## Дальнейшие шаги {#next-steps}

Используйте встроенные материалы для стандартного подхода glTF metallic/roughness. Расширяйте вспомогательные функции шейдера или предоставляйте свой материал, если нужны другая BRDF, освещение окружения, тени или дополнительные эффекты материалов glTF.

См. также:

* [Руководство по источникам света](/manuals/light)
* [Руководство по материалам](/manuals/material)
* [Руководство по шейдерам](/manuals/shader)
* [Руководство по рендерингу](/manuals/render)
* [Спецификация glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
