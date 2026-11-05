---
title: Фізично обґрунтований рендеринг у Defold
brief: Цей посібник пояснює, як використовувати вбудовані матеріали PBR і налаштовувати фізично обґрунтоване затінення в Defold.
---

# Фізично обґрунтований рендеринг (PBR) {#physically-based-rendering-pbr}

Фізично обґрунтований рендеринг (Physically Based Rendering, PBR) — це підхід до затінення, що моделює взаємодію світла з поверхнями на основі фізичних принципів. Такі властивості матеріалу, як базовий колір, металевість і шорсткість, описують поверхню незалежно від освітлення сцени.

Вбудовані матеріали glTF надають освітлення PBR. Defold також надає власним шейдерам імпортовані властивості матеріалів glTF 2.0 й дані підтримуваних розширень Khronos.

## Вбудовані матеріали PBR {#built-in-pbr-materials}

Призначте файл glTF або GLB властивості *Scene* [компонента Model](/manuals/model). Коли редактор запропонує заповнити матеріали й текстури, виберіть <kbd>Auto Fill</kbd>, щоб застосувати згенеровані прив’язки матеріалів сцени, замінивши наявні прив’язки. Ці матеріали використовують вбудовані шейдери glTF і можуть безпосередньо посилатися на вбудовані зображення. Виберіть <kbd>Keep Current</kbd>, щоб зберегти свої прив’язки й призначити матеріали та текстури вручну. Про перегляд вбудованих ресурсів і вибір окремих сіток див. [процес імпорту моделей](/manuals/importing-models/#using-a-model).

У `/builtins/materials/` доступні такі матеріали. Виберіть варіант, що відповідає моделі та використанню інстансингу:

| Тип моделі | Матеріал |
|---|---|
| Статична, без інстансингу | `gltf.material` |
| Статична, з інстансингом | `gltf_instanced.material` |
| Зі скінінгом (анімована), без інстансингу | `gltf_skinned.material` |
| Зі скінінгом (анімована), з інстансингом | `gltf_skinned_instanced.material` |

Усі чотири використовують локальний простір вершин і той самий фрагментний шейдер `gltf.fp`. Варіанти зі скінінгом виконують його на GPU. Про скінінг на GPU й інстансинг див. [вимоги матеріалів моделей](/manuals/model/#material).

Для ручного призначення текстур вбудовані матеріали використовують такі назви семплерів:

| Текстура | Семплер | Дані |
|---|---|---|
| Базовий колір | `PbrMetallicRoughness_baseColorTexture` | Колір RGB і альфа-канал |
| Металевість/шорсткість | `PbrMetallicRoughness_metallicRoughnessTexture` | Шорсткість у G, металевість у B |
| Нормаль | `PbrMaterial_normalTexture` | Нормаль у дотичному просторі в RGB |
| Оклюзія | `PbrMaterial_occlusionTexture` | Оклюзія в R |
| Випромінювання | `PbrMaterial_emissiveTexture` | Колір RGB |

Налаштуйте [камеру](/manuals/camera/#using-the-camera) і додайте [компоненти світла](/manuals/light), щоб освітити модель. Шейдер використовує спрямовані, точкові та прожекторні джерела для прямого освітлення й фонові джерела для простого внеску навколишнього освітлення. Матеріали мають тег `model`, який малює стандартний скрипт рендерингу. Власний скрипт рендерингу має малювати відповідний предикат.

### Поведінка вбудованих шейдерів {#built-in-shader-behavior}

Вбудовані шейдери реалізують затінення metallic/roughness, базовий колір і колір вершин, карти нормалей за наявності даних дотичних, оклюзію та випромінювання з урахуванням його сили. Текстури базового кольору й випромінювання декодуються з sRGB для освітлення, а кінцевий колір перетворюється назад у sRGB. Карти металевості/шорсткості, нормалей і оклюзії містять лінійні дані.

Шейдер враховує матеріали без освітлення та альфа-маску й коригує нормалі двосторонніх поверхонь. Стан рендерингу залишається важливим:

- Для двосторонніх матеріалів вимкніть відсікання граней у відповідному проході рендерингу, щоб задні грані потрапляли до шейдера.
- Для змішуваної прозорості шейдер виводить непримножений альфа-канал. Увімкніть змішування з `graphics.BLEND_FACTOR_SRC_ALPHA` і `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` та керуйте порядком малювання прозорих об’єктів і записом глибини у скрипті рендерингу. Стандартний прохід моделей не вмикає змішування автоматично.

Вбудований внесок навколишнього освітлення є наближенням без освітлення картою оточення чи тіней. Такі ефекти, як прозоре покриття, світлопропускання, полиск, іризація та процес specular/glossiness, потребують власного затінення; імпорт їхніх параметрів не вмикає ці ефекти у `gltf.fp`.

## Огляд властивостей матеріалів {#material-properties-overview}

Наведені нижче властивості зчитуються з вихідних файлів glTF 2.0, призначених компоненту моделі. Список описує доступні дані матеріалів; вбудоване освітлення використовує підмножину, описану вище. Не всі властивості є стандартними. Деякі надаються через необов’язкові розширення glTF, які засіб експорту файлу glTF може включати або не включати. Нижче відповідне розширення вказано в дужках після назви властивості.

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
: Запитує рендеринг обох боків поверхні. Прохід рендерингу має пропускати задні грані до шейдера.

Без освітлення
: Якщо значення дорівнює true, матеріал оминає обчислення освітлення.


## Інтеграція з шейдерами {#shader-integration}

Наступні розділи стосуються власних шейдерів. Скопіюйте відповідний вбудований ресурс `.material` і `gltf.fp` до проєкту, а потім спрямуйте *Fragment Program* копії матеріалу на свій шейдер. Зберігайте відповідну вершинну програму glTF, назви семплерів і локальний простір вершин, якщо не замінюєте також ці інтерфейси.

Вбудовані допоміжні функції відокремлюють вибірку текстур від підготовки поверхні, обчислень BRDF і освітлення. `gltf_sampling.glsl` читає необроблений блок uniform `PbrMaterial` і створює значення `PBRMaterial` із розв’язаними лінійними вхідними даними матеріалу. `gltf_lighting.glsl` надає пряме й навколишнє освітлення та поєднує їхній внесок. Регістр літер відрізняє необроблений блок uniform від структури вибраного матеріалу.

### Приклад шейдера {#example-shader}

Цей фрагментний шейдер підвищує мінімальну шорсткість, зберігаючи вбудоване освітлення. Він працює з вершинними програмами всіх чотирьох варіантів матеріалів glTF:

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

Змінюйте вибрані вхідні дані матеріалу до виклику `pbr_create_material_info()`. Якщо змінюєте позицію або нормалі поверхні у просторі виду, викличте `pbr_finalize_surface(surface, var_view)`, щоб оновити похідні поля світового простору. Для власної BRDF або внеску окремих джерел світла використовуйте або замініть `pbr_evaluate_brdf()` і `pbr_evaluate_light()` із вбудованих допоміжних функцій.

Можна замінити `lighting.indirect` власним освітленням оточення або глобальним освітленням. Його дифузний і дзеркальний внески є лінійним вихідним світлом, тому не застосовуйте BRDF матеріалу вдруге. Застосовуйте видимість тіні до відповідного внеску прямого світла; аргументи видимості `pbr_compose_lighting()` впливають лише на непряме освітлення. Для конвеєра HDR записуйте лінійний колір у проміжну ціль і виконуйте перетворення sRGB у фінальному проході.

### Необроблені дані матеріалу {#raw-material-data}

Для повністю власного шейдера оголосіть блок uniform `PbrMaterial` із розпізнаваними назвами й типами полів. Defold заповнює відповідні поля з вихідного матеріалу glTF. Оголошення нижче описують доступні структури можливостей; включайте лише потрібні шейдеру. Оголошення структури надає дані, але шейдер має реалізувати їхню вибірку й поведінку освітлення.

Не оголошуйте повторно блок uniform або `PbrMetallicRoughness`, коли включаєте `gltf_sampling.glsl`, оскільки він уже їх оголошує. Наступні оголошення є альтернативою для шейдерів, які самостійно керують вхідними даними матеріалу.

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

Спільні властивості й структури можливостей є полями блоку uniform. Упаковані компоненти:

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

Пропускайте невикористовувані поля можливостей у блоці. Якщо блок або розпізнавані поля можливості відсутні, відповідні дані не надаються. Прапорці наявності текстур описують посилання вихідного матеріалу на текстури; власний матеріал усе одно потребує відповідних оголошень семплерів і прив’язок текстур для карт, із яких він вибирає дані.

### Константи {#constants}

Поля можливостей мають назви на кшталт `pbrMetallicRoughness.baseColorFactor`, а спільні поля — на кшталт `pbrEmissiveFactorAndStrength`. Рушій заповнює ці константи з імпортованого матеріалу або з типового матеріалу, якщо модель не має даних матеріалу. Задання типових значень у ресурсі `.material` не перевизначає імпортованих значень.

Щоб налаштувати вбудоване затінення, змініть вибраний `PBRMaterial` перед обчисленням його значень BRDF, як у прикладі вище. Для додаткового керування під час виконання оголосіть власні константи шейдера й використовуйте [API констант матеріалу моделі](/manuals/model/#material-constants).

## Подальші кроки {#next-steps}

Використовуйте вбудовані матеріали для стандартного процесу glTF metallic/roughness. Розширюйте допоміжні функції шейдера або створюйте власний матеріал, коли потрібні інша BRDF, освітлення оточення, тіні чи додаткові ефекти матеріалів glTF.

Див. також:

* [Посібник зі світла](/manuals/light)
* [Посібник із матеріалів](/manuals/material)
* [Посібник із шейдерів](/manuals/shader)
* [Посібник із рендерингу](/manuals/render)
* [Специфікація glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
