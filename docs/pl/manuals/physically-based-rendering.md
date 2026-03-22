---
title: Renderowanie oparte na modelu fizycznym w Defold
brief: Ta instrukcja wyjaśnia podstawy dostępu do danych materiału dla renderowania opartego na modelu fizycznym w Defold.
---

# Renderowanie oparte na modelu fizycznym (PBR)

Renderowanie oparte na modelu fizycznym (Physically Based Rendering, PBR) to podejście do cieniowania, które modeluje interakcję światła z powierzchniami w oparciu o rzeczywiste zasady fizyczne. Zapewnia spójne, realistyczne oświetlenie w różnych środowiskach i pozwala zasobom wyglądać poprawnie w szerokim zakresie warunków oświetleniowych.

Implementacja PBR w Defold opiera się na specyfikacji materiałów glTF 2.0 oraz powiązanych rozszerzeniach Khronos. Gdy importujesz zasoby glTF do Defold, właściwości materiału są automatycznie odczytywane i zapisywane jako uporządkowane dane materiału, do których można odwołać się w shaderach w czasie działania programu.

Materiały PBR mogą obejmować efekty takie jak metaliczne odbicia, chropowatość powierzchni, transmisję, clearcoat, rozpraszanie podpowierzchniowe, iryzację i wiele innych.

::: sidenote
Defold obecnie udostępnia shaderom dane materiału PBR, ale nie zapewnia wbudowanego modelu oświetlenia PBR. Możesz użyć tych danych we własnych shaderach oświetlenia i odbić, aby uzyskać renderowanie oparte na modelu fizycznym. Domyślny model oświetlenia PBR zostanie dodany do Defold na późniejszym etapie.
:::

::: sidenote
Osadzone tekstury z plików glTF nie są obecnie automatycznie przypisywane w Defold. Shaderom udostępniane są tylko parametry materiału. Nadal możesz ręcznie przypisać tekstury do komponentów modeli i pobierać je w shaderze.
:::

## Przegląd właściwości materiału

Właściwości materiału są odczytywane z plików źródłowych glTF 2.0 przypisanych do komponentu modelu. Nie wszystkie właściwości są standardowe. Niektóre są dostarczane przez opcjonalne rozszerzenia glTF, które mogą, ale nie muszą, zostać dołączone przez narzędzie użyte do eksportu pliku glTF. Odpowiednie rozszerzenie jest oznaczone w nawiasie po nazwie właściwości poniżej.

Metallic roughness
: Opisuje sposób interakcji światła z materiałem. Domyślny model PBR.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: Alternatywa dla metallic roughness. Często używana w starszych zasobach.

Clearcoat (KHR_materials_clearcoat)
: Dodaje przezroczystą warstwę powłoki z własną chropowatością i mapą normalnych.

Ior (KHR_materials_ior)
: Dodaje współczynnik załamania światła.

Specular (KHR_materials_specular)
: Dodaje osobne kanały intensywności i koloru odbić lustrzanych.

Iridescence (KHR_materials_iridescence)
: Symuluje interferencję cienkich warstw w materiałach takich jak bańki mydlane lub perły.

Sheen (KHR_materials_sheen)
: Modeluje odbicia mikrostruktury podobne do tkanin.

Transmission (KHR_materials_transmission)
: Modeluje przepuszczanie światła w materiałach przezroczystych lub podobnych do szkła.

Volume (KHR_materials_volume)
: Obsługuje efekty wolumetryczne, takie jak grubość i tłumienie.

Emissive strength (KHR_materials_emissive_strength)
: Kontroluje jasność emisji niezależnie od koloru bazowego.

Normal map
: Mapa normalnych dla detali powierzchni.

Occlusion map
: Mapa okluzji otoczenia.

Emissive map
: Tekstura samoluminescencyjna dla świecących powierzchni.

Emissive factor
: Mnożnik RGB dla intensywności emisji.

Alpha cutoff
: Próg przezroczystości maskowanej.

Alpha mode
: Tryb przezroczystości: Opaque, Masked lub Blended.

Double sided
: Jeśli ma wartość true, renderowane są obie strony powierzchni.

Unlit
: Jeśli ma wartość true, materiał pomija obliczenia oświetlenia.

::: sidenote
Niektóre z tych właściwości dostarczają wskazówek, jak materiał powinien być renderowany. Dane dla właściwości (`alpha cutoff`, `alpha mode`, `double sided` i `unlit`) są dostępne w shaderach, ale nie wpływają na to, jak materiał jest renderowany w Defold.
:::

## Integracja ze shaderami

Dane materiału PBR są udostępniane shaderom na podstawie typów i konwencji nazewnictwa. System materiałów PBR przekazuje wszystkie odczytane parametry materiału do shaderów przez uporządkowany blok uniformów o nazwie `PbrMaterial`. Każde obsługiwane rozszerzenie glTF odpowiada strukturze w tym bloku, którą można kompilować warunkowo za pomocą znaczników `#define`.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Różne cechy materiału są w shaderze opisane jako stałe struktury. Dane zostały spakowane do `vec4` w maksymalnym możliwym stopniu, ponieważ w ten sposób stałe są wewnętrznie ustawiane w Defold. W przypadkach, w których dane zostały spakowane, zostało to oznaczone komentarzami w przykładach shaderów dla każdej funkcji poniżej:

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

Wspólne właściwości są ustawiane w samym uniformie materiału (i ponownie warto zwrócić uwagę na pakowanie danych do `vec4`).

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

### Przykładowy shader

Poniżej znajduje się przykład shadera zawierającego wszystkie funkcje oraz proponowany schemat nazewnictwa dla powiązań tekstur (tę część również trzeba obsłużyć ręcznie). Zwróć uwagę, że możesz wyłączyć poszczególne funkcje, używając `#define` wokół każdego elementu `PbrMaterial`, tak jak pokazano w przykładzie poniżej:

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
uniform sampler2D PbrClearCoat_clearCoatTexture;
uniform sampler2D PbrClearCoat_clearCoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearCoatNormalTexture;

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
Jeśli w strukturze materiału nie zostaną znalezione określone punkty danych, dane dla tych funkcji nie zostaną ustawione. Na przykład jeśli w strukturze materiału nie ma `pbrClearCoat`, dane clear coat nie zostaną ustawione. Jeśli blok uniformów nie zostanie znaleziony, podczas renderowania nie zostaną ustawione żadne dane.
:::

### Stałe

Każda właściwość materiału odpowiada wewnętrznej stałej renderowania w Defold. Możesz nadpisać wartości domyślne, definiując stałe bezpośrednio w zasobie materiału, zgodnie ze wzorcem nazewnictwa `pbrFeature.structMember`. Te wartości zostaną zastosowane automatycznie, jeśli odpowiadające im dane są nieobecne w materiale glTF.

![Stałe materiału](images/physically-based-rendering/material-constants.png)

## Następne kroki

Aby użyć danych materiału do renderowania opartego na modelu fizycznym, zaimplementuj BRDF w shaderze fragmentu, korzystając z parametrów udostępnionych w bloku `PbrMaterial`.
Zobacz także:

* [Instrukcja do shaderów](/manuals/shader)
* [Instrukcja do renderowania](/manuals/render)
* [Specyfikacja glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
