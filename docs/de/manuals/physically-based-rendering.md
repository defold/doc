---
title: Physikalisch basiertes Rendering in Defold
brief: Dieses Handbuch erklärt, wie du integrierte PBR-Materialien verwendest und physikalisch basierte Schattierung in Defold anpasst.
---

# Physikalisch basiertes Rendering (PBR) {#physically-based-rendering-pbr}

Physikalisch basiertes Rendering (Physically Based Rendering, PBR) ist ein Schattierungsansatz, der die Wechselwirkung zwischen Licht und Oberflächen anhand physikalischer Prinzipien modelliert. Materialeigenschaften wie Grundfarbe, Metallfaktor und Rauheit beschreiben die Oberfläche unabhängig von der Beleuchtung der Szene.

Integrierte glTF-Materialien bieten PBR-Beleuchtung. Defold stellt benutzerdefinierten Shadern außerdem importierte glTF-2.0-Materialeigenschaften und unterstützte Khronos-Erweiterungsdaten bereit.

## Integrierte PBR-Materialien {#built-in-pbr-materials}

Weise der Eigenschaft *Scene* einer [Modellkomponente](/manuals/model) eine glTF- oder GLB-Datei zu. Wenn der Editor anbietet, Materialien und Texturen auszufüllen, wähle <kbd>Auto Fill</kbd>, um die erzeugten Materialbindungen der Szene anzuwenden und gegebenenfalls bestehende Bindungen zu ersetzen. Diese Materialien verwenden die integrierten glTF-Shader und können eingebettete Bilder direkt referenzieren. Wähle <kbd>Keep Current</kbd>, um deine Bindungen beizubehalten und Materialien und Texturen manuell zuzuweisen. Das Durchsuchen eingebetteter Ressourcen und die Auswahl einzelner Meshes beschreibt der [Ablauf des Modellimports](/manuals/importing-models/#using-a-model).

Die folgenden Materialien sind unter `/builtins/materials/` verfügbar. Wähle die Variante passend zu deinem Modell und dessen Verwendung von Instanzierung:

| Modelltyp | Material |
|---|---|
| Statisch, nicht instanziert | `gltf.material` |
| Statisch, instanziert | `gltf_instanced.material` |
| Mit Skinning (animiert), nicht instanziert | `gltf_skinned.material` |
| Mit Skinning (animiert), instanziert | `gltf_skinned_instanced.material` |

Alle vier verwenden lokalen Vertex-Raum und denselben Fragment-Shader `gltf.fp`. Die Skinning-Varianten führen das Skinning auf der GPU aus. Siehe die [Anforderungen an Modellmaterialien](/manuals/model/#material) für GPU-Skinning und Instanzierung.

Für manuelle Texturbindungen verwenden die integrierten Materialien folgende Samplernamen:

| Textur | Sampler | Verwendete Daten |
|---|---|---|
| Grundfarbe | `PbrMetallicRoughness_baseColorTexture` | RGB-Farbe und Alpha |
| Metall/Rauheit | `PbrMetallicRoughness_metallicRoughnessTexture` | Rauheit in G, Metall in B |
| Normalen | `PbrMaterial_normalTexture` | Normale im Tangentenraum in RGB |
| Verdeckung | `PbrMaterial_occlusionTexture` | Verdeckung in R |
| Emission | `PbrMaterial_emissiveTexture` | RGB-Farbe |

Richte eine [Kamera](/manuals/camera/#using-the-camera) ein und füge [Lichtkomponenten](/manuals/light) hinzu, um das Modell zu beleuchten. Der Shader verwendet gerichtete Lichtquellen, Punkt- und Spotlichter für direkte Beleuchtung sowie Umgebungslichtquellen für einen einfachen Umgebungsanteil. Die Materialien besitzen das Tag `model`, das vom Standard-Renderskript gezeichnet wird. Ein eigenes Renderskript muss ein passendes Prädikat zeichnen.

### Verhalten der integrierten Shader {#built-in-shader-behavior}

Die integrierten Shader implementieren Metallic-/Roughness-Schattierung, Grund- und Vertex-Farbe, Normal Mapping bei verfügbaren Tangentendaten, Verdeckung und Emission einschließlich Emissionsstärke. Grundfarben- und Emissionstexturen werden für die Beleuchtung aus sRGB dekodiert, die Endfarbe wird zurück nach sRGB konvertiert. Metallic-/Roughness-, Normalen- und Verdeckungstexturen enthalten lineare Daten.

Der Shader berücksichtigt unbeleuchtete Materialien und maskiertes Alpha und passt Normalen für doppelseitige Oberflächen an. Der Renderzustand bleibt wichtig:

- Deaktiviere bei doppelseitigen Materialien Face Culling im entsprechenden Renderdurchlauf, damit Rückseiten den Shader erreichen.
- Bei Alpha-Blending gibt der Shader nicht vormultipliziertes Alpha aus. Aktiviere Blending mit `graphics.BLEND_FACTOR_SRC_ALPHA` und `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` und verwalte Zeichenreihenfolge und Tiefenschreibzugriffe transparenter Objekte im Renderskript. Der standardmäßige Model-Durchlauf aktiviert Blending nicht automatisch.

Der integrierte Umgebungsanteil ist eine Näherung ohne Environment-Map-Beleuchtung oder Schatten. Effekte wie Klarlack, Transmission, Sheen, Irisieren und der Specular-/Glossiness-Workflow benötigen eigene Schattierung; der Import ihrer Parameter aktiviert diese Effekte nicht in `gltf.fp`.

## Übersicht der Materialeigenschaften {#material-properties-overview}

Die folgenden Eigenschaften werden aus glTF-2.0-Quelldateien eingelesen, die einer Modellkomponente zugewiesen sind. Diese Liste beschreibt die verfügbaren Materialdaten; die integrierte Beleuchtung verwendet die oben beschriebene Teilmenge. Nicht alle Eigenschaften gehören zum Standard. Einige stammen aus optionalen glTF-Erweiterungen, die das zum Export verwendete Werkzeug möglicherweise einbezieht. Die jeweilige Erweiterung steht unten in Klammern hinter dem Eigenschaftsnamen.

Metallizität und Rauheit
: Beschreibt, wie Licht mit dem Material interagiert. Das standardmäßige PBR-Modell.

Glanzreflexion und Glätte (KHR_materials_pbrSpecularGlossiness)
: Eine Alternative zu Metallizität und Rauheit. Wird häufig in älteren Assets verwendet.

Klarlack (KHR_materials_clearcoat)
: Fügt eine transparente Beschichtung mit eigener Rauheit und Normalen-Map hinzu.

Brechungsindex (Ior) (KHR_materials_ior)
: Fügt einen Brechungsindex hinzu.

Glanzreflexion (KHR_materials_specular)
: Fügt einen eigenen Intensitäts- und Farbkanal für Glanzreflexionen hinzu.

Irideszenz (KHR_materials_iridescence)
: Simuliert Dünnschichtinterferenz für Materialien wie Seifenblasen oder Perlen.

Schimmer (KHR_materials_sheen)
: Modelliert stoffähnliche Reflexionen an Mikrooberflächen.

Transmission (KHR_materials_transmission)
: Modelliert die Lichtdurchlässigkeit transparenter oder glasähnlicher Materialien.

Volumen (KHR_materials_volume)
: Unterstützt volumetrische Effekte wie Dicke und Abschwächung.

Emissionsstärke (KHR_materials_emissive_strength)
: Steuert die Helligkeit der Eigenemission unabhängig von der Grundfarbe.

Normalen-Map
: Normalen-Map für Oberflächendetails.

Okklusions-Map
: Map für Umgebungsverdeckung (Ambient Occlusion).

Emissions-Map
: Selbstleuchtende Textur für leuchtende Oberflächen.

Emissionsfaktor
: RGB-Multiplikator für die Emissionsintensität

Alpha-Schwellenwert
: Schwellenwert für maskierte Transparenz.

Alphamodus
: Transparenzmodi Opaque, Masked oder Blended.

Doppelseitig
: Fordert das Rendern beider Seiten der Oberfläche an. Der Renderdurchlauf muss zulassen, dass Rückseiten den Shader erreichen.

Unbeleuchtet
: Wenn der Wert true ist, umgeht das Material die Beleuchtungsberechnungen.

## Shader-Integration

Die folgenden Abschnitte behandeln benutzerdefinierte Shader. Kopiere die passende integrierte `.material`-Ressource und `gltf.fp` in dein Projekt und setze *Fragment Program* des kopierten Materials auf deinen Shader. Behalte das passende glTF-Vertex-Programm, die Samplernamen und lokalen Vertex-Raum bei, sofern du nicht auch diese Schnittstellen ersetzt.

Die integrierten Hilfsfunktionen trennen Texturabtastung von Oberflächenvorbereitung, BRDF-Berechnungen und Beleuchtung. `gltf_sampling.glsl` liest den rohen Uniform-Block `PbrMaterial` und erzeugt einen Wert vom Typ `PBRMaterial` mit aufgelösten, linearen Materialeingaben. `gltf_lighting.glsl` stellt direkte und Umgebungsbeleuchtung bereit und kombiniert deren Beiträge. Die Großschreibung unterscheidet den rohen Uniform-Block von der Struktur des abgetasteten Materials.

### Beispielshader {#example-shader}

Dieser Fragment-Shader erhöht die Mindestrauheit und behält dabei die integrierte Beleuchtung bei. Er funktioniert mit den Vertex-Programmen aller vier glTF-Materialvarianten:

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

Bearbeite abgetastete Materialeingaben vor dem Aufruf von `pbr_create_material_info()`. Wenn du die Position im Ansichtsraum oder die Normalen einer Oberfläche änderst, rufe `pbr_finalize_surface(surface, var_view)` auf, um ihre abgeleiteten Felder im Weltraum zu aktualisieren. Verwende oder ersetze für eine eigene BRDF oder einzelne Lichtbeiträge `pbr_evaluate_brdf()` und `pbr_evaluate_light()` aus den integrierten Hilfsfunktionen.

Du kannst `lighting.indirect` durch eigene Umgebungsbeleuchtung oder globale Beleuchtung ersetzen. Seine diffusen und spiegelnden Beiträge sind lineares ausgehendes Licht; wende die BRDF des Materials daher kein zweites Mal an. Wende Schattensichtbarkeit auf den entsprechenden direkten Lichtbeitrag an; die Sichtbarkeitsargumente von `pbr_compose_lighting()` beeinflussen nur indirekte Beleuchtung. Schreibe für eine HDR-Pipeline lineare Farbe in das Zwischenziel und führe die sRGB-Konvertierung im letzten Durchlauf aus.

### Rohe Materialdaten {#raw-material-data}

Deklariere für einen vollständig eigenen Shader einen Uniform-Block namens `PbrMaterial` mit den erkannten Feldnamen und Typen. Defold füllt passende Felder aus dem glTF-Quellmaterial. Die folgenden Deklarationen beschreiben die verfügbaren Funktionsstrukturen; beziehe nur diejenigen ein, die dein Shader benötigt. Die Deklaration einer Struktur stellt Daten bereit, ihr Abtast- und Beleuchtungsverhalten muss dein Shader jedoch implementieren.

Deklariere den Uniform-Block oder `PbrMetallicRoughness` nicht erneut, wenn du `gltf_sampling.glsl` einbindest, da sie dort bereits deklariert sind. Die folgenden Deklarationen sind eine Alternative für Shader, die ihre Materialeingaben selbst verwalten.

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

Die gemeinsamen Eigenschaften und Funktionsstrukturen sind Mitglieder des Uniform-Blocks. Die gepackten Komponenten sind:

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

Lasse ungenutzte Funktionsmitglieder aus dem Block weg. Fehlen der Block oder die erkannten Felder einer Funktion, werden die entsprechenden Daten nicht bereitgestellt. Flags zum Vorhandensein von Texturen beschreiben die Texturreferenzen des Quellmaterials; ein eigenes Material benötigt weiterhin passende Samplerdeklarationen und Texturbindungen für die abgetasteten Texturen.

### Konstanten {#constants}

Funktionsfelder verwenden Namen wie `pbrMetallicRoughness.baseColorFactor`; gemeinsame Felder verwenden Namen wie `pbrEmissiveFactorAndStrength`. Die Engine befüllt diese Konstanten aus dem importierten Material oder aus einem Standardmaterial, wenn das Modell keine Materialdaten besitzt. Standardwerte in der `.material`-Ressource überschreiben die importierten Werte nicht.

Um die integrierte Schattierung anzupassen, bearbeite das abgetastete `PBRMaterial` vor der Ableitung seiner BRDF-Werte, wie im obigen Beispiel. Deklariere für zusätzliche Steuerungsmöglichkeiten zur Laufzeit eigene Shader-Konstanten und verwende die [API für Modellmaterialkonstanten](/manuals/model/#material-constants).

## Nächste Schritte {#next-steps}

Verwende die integrierten Materialien für den standardmäßigen glTF-Metallic-/Roughness-Workflow. Erweitere die Shader-Hilfsfunktionen oder stelle ein eigenes Material bereit, wenn du eine andere BRDF, Umgebungsbeleuchtung, Schatten oder zusätzliche glTF-Materialeffekte benötigst.

Siehe auch:

* [Lichthandbuch](/manuals/light)
* [Materialhandbuch](/manuals/material)
* [Shader-Handbuch](/manuals/shader)
* [Rendering-Handbuch](/manuals/render)
* [glTF-2.0-Spezifikation](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
