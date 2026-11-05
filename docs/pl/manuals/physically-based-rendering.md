---
title: Renderowanie oparte na fizyce w silniku Defold
brief: Ta instrukcja wyjaśnia, jak korzystać z wbudowanych materiałów PBR i dostosowywać cieniowanie oparte na fizyce w silniku Defold.
---

# Renderowanie oparte na fizyce (PBR)

Renderowanie oparte na fizyce (ang. Physically Based Rendering, PBR) to podejście do cieniowania modelujące oddziaływanie światła z powierzchniami zgodnie z zasadami fizyki. Właściwości materiału, takie jak kolor bazowy, metaliczność i chropowatość, opisują powierzchnię niezależnie od oświetlenia sceny.

Wbudowane materiały glTF zapewniają oświetlenie PBR. Defold udostępnia również zaimportowane właściwości materiałów glTF 2.0 i dane obsługiwanych rozszerzeń Khronos własnym shaderom.

## Wbudowane materiały PBR {#built-in-pbr-materials}

Przypisz plik glTF lub GLB do właściwości *Scene* [komponentu Model](/manuals/model). Gdy edytor zaproponuje wypełnienie materiałów i tekstur, wybierz <kbd>Auto Fill</kbd>, aby zastosować wygenerowane powiązania materiałów sceny, zastępując istniejące powiązania, jeśli są obecne. Te materiały używają wbudowanych shaderów glTF i mogą bezpośrednio odwoływać się do osadzonych obrazów. Wybierz <kbd>Keep Current</kbd>, aby zachować swoje powiązania i ręcznie przypisać materiały oraz tekstury. [Przebieg importowania modelu](/manuals/importing-models/#using-a-model) opisuje przeglądanie osadzonych zasobów i wybieranie pojedynczych siatek.

W `/builtins/materials/` dostępne są następujące materiały. Wybierz wariant pasujący do modelu i sposobu jego instancjonowania:

| Typ modelu | Materiał |
|---|---|
| Statyczny, bez instancjonowania | `gltf.material` |
| Statyczny, instancjonowany | `gltf_instanced.material` |
| Ze skinningiem (animowany), bez instancjonowania | `gltf_skinned.material` |
| Ze skinningiem (animowany), instancjonowany | `gltf_skinned_instanced.material` |

Wszystkie cztery używają lokalnej przestrzeni wierzchołków i tego samego shadera fragmentów `gltf.fp`. Warianty ze skinningiem wykonują go na GPU. Zobacz [wymagania materiałów modeli](/manuals/model/#material) dotyczące skinningu GPU i instancjonowania.

Przy ręcznym przypisywaniu tekstur wbudowane materiały używają następujących nazw samplerów:

| Tekstura | Sampler | Używane dane |
|---|---|---|
| Kolor bazowy | `PbrMetallicRoughness_baseColorTexture` | Kolor RGB i alfa |
| Metaliczność/chropowatość | `PbrMetallicRoughness_metallicRoughnessTexture` | Chropowatość w G, metaliczność w B |
| Normalne | `PbrMaterial_normalTexture` | Normalna w przestrzeni stycznych w RGB |
| Okluzja | `PbrMaterial_occlusionTexture` | Okluzja w R |
| Emisja | `PbrMaterial_emissiveTexture` | Kolor RGB |

Skonfiguruj [kamerę](/manuals/camera/#using-the-camera) i dodaj [komponenty światła](/manuals/light), aby oświetlić model. Shader używa świateł kierunkowych, punktowych i stożkowych do oświetlenia bezpośredniego oraz świateł otoczenia do prostego składnika ambient. Materiały mają znacznik `model`, rysowany przez domyślny skrypt renderowania. Własny skrypt renderowania musi rysować pasujący predykat.

### Zachowanie wbudowanych shaderów {#built-in-shader-behavior}

Wbudowane shadery implementują cieniowanie metallic/roughness, kolor bazowy i kolor wierzchołków, mapowanie normalnych przy dostępnych danych stycznych, okluzję oraz emisję z uwzględnieniem jej siły. Tekstury koloru bazowego i emisji są dekodowane z sRGB do obliczeń oświetlenia, a końcowy kolor jest przekształcany z powrotem do sRGB. Mapy metaliczności/chropowatości, normalnych i okluzji zawierają dane liniowe.

Shader uwzględnia materiały nieoświetlane i maskowaną alfę oraz dostosowuje normalne powierzchni dwustronnych. Stan renderowania nadal ma znaczenie:

- Dla materiałów dwustronnych wyłącz odrzucanie ścian w odpowiednim przebiegu renderowania, aby tylne ściany trafiały do shadera.
- Przy mieszaniu alfa shader zwraca alfę bez premultiplikacji. Włącz mieszanie z `graphics.BLEND_FACTOR_SRC_ALPHA` i `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` oraz zarządzaj kolejnością rysowania obiektów przezroczystych i zapisem głębokości w skrypcie renderowania. Domyślny przebieg modeli nie włącza mieszania automatycznie.

Wbudowany składnik ambient jest przybliżeniem, bez oświetlenia mapą środowiska i bez cieni. Efekty takie jak clearcoat, transmisja, sheen, iryzacja i model specular/glossiness wymagają własnego cieniowania; zaimportowanie ich parametrów nie włącza tych efektów w `gltf.fp`.

## Przegląd właściwości materiałów {#material-properties-overview}

Poniższe właściwości są odczytywane z plików źródłowych glTF 2.0 przypisanych do komponentu Model. Lista opisuje dostępne dane materiału; wbudowane oświetlenie korzysta z podzbioru opisanego powyżej. Nie wszystkie właściwości są standardowe. Niektóre pochodzą z opcjonalnych rozszerzeń glTF, które narzędzie eksportujące może dołączać lub pomijać. Odpowiednie rozszerzenie podano w nawiasie po nazwie właściwości.

Metallic roughness
: Opisuje oddziaływanie światła z materiałem. Domyślny model PBR.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: Alternatywa dla metallic roughness. Często używana w starszych zasobach.

Clearcoat (KHR_materials_clearcoat)
: Dodaje przezroczystą warstwę powłoki z własną chropowatością i mapą normalnych.

Ior (KHR_materials_ior)
: Dodaje współczynnik załamania światła.

Specular (KHR_materials_specular)
: Dodaje osobny kanał intensywności i koloru odbicia zwierciadlanego.

Iridescence (KHR_materials_iridescence)
: Symuluje interferencję cienkich warstw w materiałach takich jak bańki mydlane lub perły.

Sheen (KHR_materials_sheen)
: Modeluje odbicia mikropowierzchni podobnych do tkanin.

Transmission (KHR_materials_transmission)
: Modeluje transmisję światła przez materiały przezroczyste lub przypominające szkło.

Volume (KHR_materials_volume)
: Obsługuje efekty objętościowe, takie jak grubość i tłumienie.

Emissive strength (KHR_materials_emissive_strength)
: Steruje jasnością emisji niezależnie od koloru bazowego.

Normal map
: Mapa normalnych opisująca szczegóły powierzchni.

Occlusion map
: Mapa okluzji otoczenia.

Emissive map
: Tekstura samoświecenia dla świecących powierzchni.

Emissive factor
: Mnożnik RGB intensywności emisji.

Alpha cutoff
: Próg maskowanej przezroczystości.

Alpha mode
: Tryb przezroczystości: Opaque, Masked lub Blended.

Double sided
: Żąda renderowania obu stron powierzchni. Przebieg renderowania musi przepuszczać tylne ściany do shadera.

Unlit
: Wartość true powoduje pominięcie obliczeń oświetlenia dla materiału.

## Integracja z shaderami {#shader-integration}

Poniższe sekcje dotyczą własnych shaderów. Skopiuj odpowiedni wbudowany zasób `.material` i `gltf.fp` do projektu, a następnie ustaw *Fragment Program* skopiowanego materiału na swój shader. Zachowaj pasujący program wierzchołków glTF, nazwy samplerów i lokalną przestrzeń wierzchołków, chyba że zastępujesz również te interfejsy.

Wbudowane funkcje pomocnicze oddzielają próbkowanie tekstur od przygotowania powierzchni, obliczeń BRDF i oświetlenia. `gltf_sampling.glsl` odczytuje surowy blok uniformów `PbrMaterial` i tworzy wartość `PBRMaterial` zawierającą rozwiązane, liniowe dane wejściowe materiału. `gltf_lighting.glsl` zapewnia oświetlenie bezpośrednie i otoczenia oraz łączy ich wkład. Wielkość liter odróżnia surowy blok uniformów od struktury spróbkowanego materiału.

### Przykładowy shader {#example-shader}

Ten shader fragmentów podwyższa minimalną chropowatość, zachowując wbudowane oświetlenie. Działa z programami wierzchołków wszystkich czterech wariantów materiałów glTF:

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

Edytuj spróbkowane dane wejściowe materiału przed wywołaniem `pbr_create_material_info()`. Jeśli zmienisz pozycję powierzchni w przestrzeni widoku lub jej normalne, wywołaj `pbr_finalize_surface(surface, var_view)`, aby zaktualizować pochodne pola w przestrzeni świata. Dla własnego BRDF lub wkładu pojedynczych świateł użyj albo zastąp `pbr_evaluate_brdf()` i `pbr_evaluate_light()` z wbudowanych funkcji pomocniczych.

Możesz zastąpić `lighting.indirect` własnym oświetleniem środowiskowym lub globalnym. Jego składniki rozproszony i zwierciadlany to liniowe światło wychodzące, więc nie stosuj BRDF materiału po raz drugi. Zastosuj widoczność cienia do odpowiedniego składnika światła bezpośredniego; argumenty widoczności `pbr_compose_lighting()` wpływają tylko na oświetlenie pośrednie. W potoku HDR zapisuj liniowy kolor do celu pośredniego, a konwersję sRGB wykonuj w ostatnim przebiegu.

### Surowe dane materiału {#raw-material-data}

Dla całkowicie własnego shadera zadeklaruj blok uniformów `PbrMaterial` z rozpoznawanymi nazwami i typami pól. Defold wypełnia pasujące pola z materiału źródłowego glTF. Poniższe deklaracje opisują dostępne struktury funkcji; dołączaj tylko te potrzebne shaderowi. Deklaracja struktury dostarcza dane, ale shader musi implementować jej próbkowanie i zachowanie oświetlenia.

Nie deklaruj ponownie bloku uniformów ani `PbrMetallicRoughness`, gdy dołączasz `gltf_sampling.glsl`, który już je deklaruje. Poniższe deklaracje są alternatywą dla shaderów samodzielnie zarządzających danymi wejściowymi materiału.

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

Wspólne właściwości i struktury funkcji są polami bloku uniformów. Upakowane składowe wyglądają następująco:

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

Pomiń nieużywane pola funkcji w bloku. Jeśli brakuje bloku lub rozpoznawanych pól danej funkcji, odpowiadające im dane nie są dostarczane. Flagi obecności tekstur opisują odwołania do tekstur materiału źródłowego; własny materiał nadal wymaga pasujących deklaracji samplerów i powiązań tekstur dla próbkowanych map.

### Stałe {#constants}

Pola funkcji używają nazw takich jak `pbrMetallicRoughness.baseColorFactor`; pola wspólne nazw takich jak `pbrEmissiveFactorAndStrength`. Silnik wypełnia te stałe z zaimportowanego materiału lub z materiału domyślnego, gdy model nie ma danych materiałowych. Ustawienie wartości domyślnych w zasobie `.material` nie nadpisuje zaimportowanych wartości.

Aby dostosować wbudowane cieniowanie, edytuj spróbkowany `PBRMaterial` przed wyprowadzeniem wartości BRDF, jak w powyższym przykładzie. Dla dodatkowego sterowania w czasie działania zadeklaruj własne stałe shadera i użyj [API stałych materiału modelu](/manuals/model/#material-constants).

## Dalsze kroki {#next-steps}

Używaj wbudowanych materiałów w standardowym modelu metallic/roughness glTF. Rozszerz funkcje pomocnicze shaderów albo udostępnij własny materiał, jeśli potrzebujesz innego BRDF, oświetlenia środowiskowego, cieni lub dodatkowych efektów materiałów glTF.

Zobacz też:

* [Podręcznik świateł](/manuals/light)
* [Podręcznik materiałów](/manuals/material)
* [Podręcznik shaderów](/manuals/shader)
* [Podręcznik renderowania](/manuals/render)
* [Specyfikacja glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
