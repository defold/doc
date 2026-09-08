---
title: Rendu basé sur la physique dans Defold
brief: Ce manuel explique les bases de l’accès aux données des matériaux pour le rendu basé sur la physique dans Defold.
---

# Rendu basé sur la physique (PBR) {#physically-based-rendering-pbr}

Le rendu basé sur la physique (Physically Based Rendering, PBR) est une méthode d’ombrage qui modélise les interactions de la lumière avec les surfaces en s’appuyant sur les principes physiques du monde réel. Il produit un éclairage cohérent et réaliste dans différents environnements et permet aux ressources d’avoir un aspect correct dans des conditions d’éclairage variées.

L’implémentation du PBR dans Defold respecte la spécification des matériaux glTF 2.0 et les extensions Khronos associées. Lorsque vous importez des ressources glTF dans Defold, les propriétés des matériaux sont automatiquement analysées et stockées sous forme de données structurées accessibles dans les shaders à l’exécution.

Les matériaux PBR peuvent inclure des effets tels que les reflets métalliques, la rugosité de surface, la transmission, le vernis, la diffusion sous-surface, l’iridescence, etc.

::: sidenote
Defold expose actuellement les données des matériaux PBR aux shaders, mais ne fournit pas de modèle d’éclairage PBR intégré. Vous pouvez utiliser ces données dans vos propres shaders d’éclairage et de réflexion pour obtenir un rendu basé sur la physique. Un modèle d’éclairage PBR par défaut sera ajouté à Defold ultérieurement.
:::

::: sidenote
Les textures intégrées aux fichiers glTF ne sont actuellement pas affectées automatiquement dans Defold. Seuls les paramètres des matériaux sont exposés aux shaders. Vous pouvez néanmoins affecter manuellement des textures aux composants (components) de modèle et les échantillonner dans votre shader.
:::

## Aperçu des propriétés des matériaux {#material-properties-overview}

Les propriétés des matériaux sont extraites des fichiers sources glTF 2.0 affectés à un composant de modèle. Toutes les propriétés ne sont pas standard. Certaines sont fournies par des extensions glTF facultatives qui peuvent être incluses ou non par l’outil utilisé pour exporter le fichier glTF. L’extension concernée est indiquée entre parenthèses après le nom de la propriété ci-dessous.

Métal et rugosité
: Décrit les interactions de la lumière avec le matériau. Il s’agit du modèle PBR par défaut.

Spéculaire et brillance (KHR_materials_pbrSpecularGlossiness)
: Une alternative au modèle métal et rugosité. Souvent utilisée dans les ressources plus anciennes.

Vernis (KHR_materials_clearcoat)
: Ajoute une couche de revêtement transparente avec sa propre rugosité et sa propre carte de normales.

Indice de réfraction (KHR_materials_ior)
: Ajoute un indice de réfraction.

Spéculaire (KHR_materials_specular)
: Ajoute un canal dédié à l’intensité et à la couleur spéculaires.

Iridescence (KHR_materials_iridescence)
: Simule les interférences de couches minces pour des matériaux comme les bulles de savon ou les perles.

Éclat (KHR_materials_sheen)
: Modélise les reflets de microsurface caractéristiques des tissus.

Transmission (KHR_materials_transmission)
: Modélise la transmission de la lumière pour les matériaux transparents ou semblables au verre.

Volume (KHR_materials_volume)
: Prend en charge des effets volumiques comme l’épaisseur et l’atténuation.

Intensité d’émission (KHR_materials_emissive_strength)
: Contrôle la luminosité émise indépendamment de la couleur de base.

Carte de normales
: Carte de normales pour les détails de surface.

Carte d’occlusion
: Carte d’occlusion ambiante.

Carte d’émission
: Texture autoémissive pour les surfaces lumineuses.

Facteur d’émission
: Multiplicateur RGB de l’intensité d’émission

Seuil alpha
: Seuil de transparence par masque.

Mode alpha
: Modes de transparence Opaque, Masked ou Blended.

Double face
: Si la valeur est true, les deux faces de la surface sont rendues.

Sans éclairage
: Si la valeur est true, le matériau ignore les calculs d’éclairage.

::: sidenote
Certaines de ces propriétés donnent des indications sur la manière dont le matériau doit être rendu. Les données de ces propriétés (seuil alpha, mode alpha, double face et sans éclairage) sont disponibles dans les shaders, mais n’affectent pas la manière dont le matériau est rendu dans Defold.
:::

## Intégration aux shaders {#shader-integration}

Les données des matériaux PBR sont exposées aux shaders en fonction des types et d’une convention de nommage. Le système de matériaux PBR fournit aux shaders tous les paramètres de matériau analysés via un bloc structuré de variables uniformes nommé `PbrMaterial`. Chaque extension glTF prise en charge correspond à une structure dans ce bloc, qui peut être compilée de manière conditionnelle à l’aide d’indicateurs `#define`.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Les différentes caractéristiques du matériau sont spécifiées sous forme de structures prédéfinies dans le shader. Les données ont été regroupées autant que possible dans des `vec4`, car c’est ainsi que les constantes sont définies en interne dans Defold. Lorsque des données ont été regroupées, des commentaires l’indiquent dans les extraits de shader de chaque caractéristique ci-dessous :

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

Les propriétés communes sont définies dans le bloc de variables uniformes du matériau lui-même (remarquez à nouveau le regroupement des données dans des `vec4`).

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

### Exemple de shader {#example-shader}

Voici un exemple de shader qui contient toutes les caractéristiques et une proposition de convention de nommage pour les liaisons de textures (là encore, elles doivent être gérées manuellement). Vous pouvez désactiver des caractéristiques simplement en utilisant des `#define` autour de chaque membre du bloc `PbrMaterial` lui-même, comme le montre l’exemple ci-dessous :

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
Si certains champs de données sont introuvables dans la structure du matériau, les données des caractéristiques correspondantes ne seront pas définies. Par exemple, si la structure du matériau ne contient pas de `pbrClearCoat`, aucune donnée de vernis ne sera définie. Si le bloc de variables uniformes est introuvable, aucune donnée ne sera définie pendant le rendu.
:::

### Constantes {#constants}

Chaque propriété de matériau correspond à une constante de rendu interne dans Defold. Vous pouvez remplacer les valeurs par défaut en définissant des constantes sur la ressource de matériau elle-même, selon le modèle de nommage `pbrFeature.structMember`. Ces valeurs seront appliquées automatiquement si les données correspondantes sont absentes du matériau glTF.

![Constantes du matériau](images/physically-based-rendering/material-constants.png)

## Étapes suivantes {#next-steps}

Pour utiliser les données du matériau afin de produire un éclairage basé sur la physique, implémentez une BRDF dans votre shader de fragment en utilisant les paramètres fournis dans le bloc `PbrMaterial`.
Voir aussi :

* [Manuel des shaders](/manuals/shader)
* [Manuel du rendu](/manuals/render)
* [Spécification glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
