---
title: Physikalisch basiertes Rendering in Defold
brief: Dieses Handbuch erklärt die Grundlagen des Zugriffs auf Materialdaten für physikalisch basiertes Rendering in Defold.
---

# Physikalisch basiertes Rendering (PBR) {#physically-based-rendering-pbr}

Physikalisch basiertes Rendering (Physically Based Rendering, PBR) ist ein Shading-Verfahren, das anhand realer physikalischer Prinzipien modelliert, wie Licht mit Oberflächen interagiert. Es erzeugt eine konsistente, realistische Beleuchtung in unterschiedlichen Umgebungen und ermöglicht es, Assets unter verschiedensten Lichtbedingungen korrekt darzustellen.

Die PBR-Implementierung von Defold folgt der Materialspezifikation von glTF 2.0 und den zugehörigen Khronos-Erweiterungen. Wenn du glTF-Assets in Defold importierst, werden Materialeigenschaften automatisch eingelesen und als strukturierte Materialdaten gespeichert, auf die Shader zur Laufzeit zugreifen können.

PBR-Materialien können Effekte wie metallische Reflexionen, Oberflächenrauheit, Transmission, Klarlack, Streuung unter der Oberfläche, Irideszenz und weitere Effekte enthalten.

::: sidenote
Defold stellt Shadern derzeit PBR-Materialdaten zur Verfügung, bietet aber kein integriertes PBR-Beleuchtungsmodell. Du kannst diese Daten in deinen eigenen Beleuchtungs- und Reflexions-Shadern verwenden, um physikalisch basiertes Rendering zu erreichen. Ein standardmäßiges PBR-Beleuchtungsmodell wird Defold zu einem späteren Zeitpunkt hinzugefügt.
:::

::: sidenote
Eingebettete Texturen aus glTF-Dateien werden in Defold derzeit nicht automatisch zugewiesen. Nur Materialparameter werden Shadern zur Verfügung gestellt. Du kannst Texturen weiterhin manuell Modellkomponenten (model components) zuweisen und sie in deinem Shader abtasten.
:::

## Übersicht der Materialeigenschaften {#material-properties-overview}

Die Materialeigenschaften werden aus den glTF-2.0-Quelldateien eingelesen, die einer Modellkomponente zugewiesen sind. Nicht alle Eigenschaften gehören zum Standard. Einige werden durch optionale glTF-Erweiterungen bereitgestellt, die das zum Exportieren der glTF-Datei verwendete Werkzeug möglicherweise einbezieht. Die jeweilige Erweiterung steht unten in Klammern hinter dem Namen der Eigenschaft.

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
: Wenn der Wert true ist, werden beide Seiten der Oberfläche gerendert.

Unbeleuchtet
: Wenn der Wert true ist, umgeht das Material die Beleuchtungsberechnungen.

::: sidenote
Einige dieser Eigenschaften geben Hinweise darauf, wie das Material gerendert werden sollte. Die Daten für diese Eigenschaften (Alpha-Schwellenwert, Alphamodus, doppelseitig und unbeleuchtet) stehen in den Shadern zur Verfügung, beeinflussen aber nicht, wie das Material in Defold gerendert wird.
:::

## Shader-Integration

Die PBR-Materialdaten werden den Shadern anhand von Typen und Namenskonventionen zur Verfügung gestellt. Das PBR-Materialsystem stellt Shadern alle eingelesenen Materialparameter über einen strukturierten Uniform-Block namens `PbrMaterial` bereit. Jede unterstützte glTF-Erweiterung entspricht einer Struktur innerhalb dieses Blocks, die mithilfe von `#define`-Flags bedingt kompiliert werden kann.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Die verschiedenen Merkmale des Materials werden im Shader als festgelegte Strukturen angegeben. Die Daten wurden so weit wie möglich in `vec4`-Vektoren zusammengefasst, da Konstanten in Defold intern auf diese Weise gesetzt werden. Wo Daten zusammengefasst wurden, wird dies in den Kommentaren der folgenden Shader-Ausschnitte für jedes Merkmal angegeben:

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

Die gemeinsamen Eigenschaften werden direkt in der Material-Uniform gesetzt (beachte auch hier die Zusammenfassung der Daten in `vec4`).

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

### Beispiel-Shader {#example-shader}

Hier siehst du einen Beispiel-Shader, der alle Merkmale enthält und ein Namensschema für Texturbindungen vorschlägt (auch dies musst du manuell handhaben). Beachte, dass du Merkmale einfach deaktivieren kannst, indem du `#define`-Anweisungen um die einzelnen Felder von `PbrMaterial` selbst setzt, wie im folgenden Beispiel gezeigt:

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
Wenn bestimmte Datenfelder in der Materialstruktur nicht gefunden werden, werden die Daten für diese Merkmale nicht gesetzt. Wenn beispielsweise `pbrClearCoat` in der Materialstruktur fehlt, werden keine Klarlackdaten gesetzt. Wenn der Uniform-Block nicht gefunden wird, werden beim Rendern überhaupt keine Daten gesetzt.
:::

### Konstanten {#constants}

Jede Materialeigenschaft entspricht einer internen Render-Konstante in Defold. Du kannst Standardwerte überschreiben, indem du direkt in der Materialressource Konstanten nach dem Namensmuster `pbrFeature.structMember` definierst. Diese Werte werden automatisch angewendet, wenn die entsprechenden Daten im glTF-Material fehlen.

![Materialkonstanten](images/physically-based-rendering/material-constants.png)

## Nächste Schritte {#next-steps}

Um die Materialdaten für physikalisch basierte Beleuchtung zu verwenden, implementiere eine BRDF in deinem Fragment-Shader mit den Parametern aus dem Block `PbrMaterial`.
Siehe auch:

* [Shader-Handbuch](/manuals/shader)
* [Rendering-Handbuch](/manuals/render)
* [glTF-2.0-Spezifikation](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
