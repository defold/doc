---
title: Rendu physiquement réaliste dans Defold
brief: Ce manuel explique comment utiliser les matériaux PBR intégrés et personnaliser l'ombrage physiquement réaliste dans Defold.
---

# Rendu physiquement réaliste (PBR) {#physically-based-rendering-pbr}

Le rendu physiquement réaliste (Physically Based Rendering, PBR) est une approche de l'ombrage qui modélise l'interaction de la lumière avec les surfaces à l'aide de principes physiques. Les propriétés du matériau, telles que la couleur de base, le facteur métallique et la rugosité, décrivent la surface indépendamment de l'éclairage de la scène.

Les matériaux glTF intégrés fournissent un éclairage PBR. Defold expose également les propriétés des matériaux glTF 2.0 importés et les données des extensions Khronos prises en charge aux shaders personnalisés.

## Matériaux PBR intégrés {#built-in-pbr-materials}

Affectez un fichier glTF ou GLB à la propriété *Scene* d'un [composant Model](/manuals/model). Lorsque l'éditeur propose de renseigner les matériaux et les textures, choisissez <kbd>Auto Fill</kbd> pour appliquer les liaisons de matériaux générées depuis la scène, en remplaçant les liaisons existantes. Ces matériaux utilisent les shaders glTF intégrés et peuvent référencer directement les images intégrées. Choisissez <kbd>Keep Current</kbd> pour conserver vos liaisons et affecter manuellement les matériaux et textures. Consultez le [flux d'importation de modèles](/manuals/importing-models/#using-a-model) pour parcourir les ressources intégrées et sélectionner des maillages individuels.

Les matériaux suivants sont disponibles dans `/builtins/materials/`. Choisissez la variante correspondant à votre modèle et à son utilisation éventuelle de l'instanciation :

| Type de modèle | Matériau |
|---|---|
| Statique, sans instanciation | `gltf.material` |
| Statique, avec instanciation | `gltf_instanced.material` |
| Avec skinning (animé), sans instanciation | `gltf_skinned.material` |
| Avec skinning (animé), avec instanciation | `gltf_skinned_instanced.material` |

Les quatre utilisent l'espace local pour les sommets et le même shader de fragment `gltf.fp`. Les variantes avec skinning effectuent celui-ci sur le GPU. Consultez les [exigences des matériaux de modèles](/manuals/model/#material) pour le skinning sur GPU et l'instanciation.

Pour les liaisons de textures manuelles, les matériaux intégrés utilisent les noms de samplers suivants :

| Texture | Sampler | Données utilisées |
|---|---|---|
| Couleur de base | `PbrMetallicRoughness_baseColorTexture` | Couleur RGB et alpha |
| Métal/rugosité | `PbrMetallicRoughness_metallicRoughnessTexture` | Rugosité dans G, métal dans B |
| Normale | `PbrMaterial_normalTexture` | Normale dans l'espace tangent en RGB |
| Occlusion | `PbrMaterial_occlusionTexture` | Occlusion dans R |
| Émission | `PbrMaterial_emissiveTexture` | Couleur RGB |

Configurez une [caméra](/manuals/camera/#using-the-camera) et ajoutez des [composants Light](/manuals/light) pour éclairer le modèle. Le shader utilise les lumières directionnelles, ponctuelles et spots pour l'éclairage direct, ainsi que les lumières ambiantes pour une contribution ambiante simple. Les matériaux possèdent le tag `model`, que le script de rendu par défaut dessine. Un script de rendu personnalisé doit dessiner un prédicat correspondant.

### Comportement des shaders intégrés {#built-in-shader-behavior}

Les shaders intégrés implémentent l'ombrage métal/rugosité, la couleur de base et la couleur des sommets, le placage de normales lorsque des données de tangentes sont disponibles, l'occlusion et l'émission, y compris son intensité. Les textures de couleur de base et d'émission sont décodées depuis sRGB pour l'éclairage, et la couleur finale est reconvertie en sRGB. Les textures métal/rugosité, de normales et d'occlusion contiennent des données linéaires.

Le shader respecte les matériaux sans éclairage et l'alpha masqué, et ajuste les normales des surfaces à double face. L'état de rendu reste important :

- Pour les matériaux à double face, désactivez l'élimination des faces dans la passe de rendu concernée afin que les faces arrière atteignent le shader.
- Pour l'alpha mélangé, le shader produit un alpha non prémultiplié. Activez le mélange avec `graphics.BLEND_FACTOR_SRC_ALPHA` et `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA`, puis gérez l'ordre de dessin des objets transparents et les écritures de profondeur dans votre script de rendu. La passe de modèles par défaut n'active pas automatiquement le mélange.

La contribution ambiante intégrée est une approximation, sans éclairage par carte d'environnement ni ombres. Les effets comme le vernis, la transmission, le lustre, l'iridescence et le flux spéculaire/brillance nécessitent un ombrage personnalisé ; l'importation de leurs paramètres n'active pas ces effets dans `gltf.fp`.

## Présentation des propriétés des matériaux {#material-properties-overview}

Les propriétés suivantes sont extraites des fichiers source glTF 2.0 affectés à un composant Model. Cette liste décrit les données de matériau disponibles ; l'éclairage intégré utilise le sous-ensemble décrit ci-dessus. Toutes les propriétés ne sont pas standard. Certaines sont fournies par des extensions glTF facultatives, que l'outil d'exportation peut inclure ou non. L'extension concernée est indiquée entre parenthèses après le nom de propriété ci-dessous.

Métal/rugosité
: Décrit la manière dont la lumière interagit avec le matériau. Le modèle PBR par défaut.

Spéculaire/brillance (KHR_materials_pbrSpecularGlossiness)
: Une alternative au modèle métal/rugosité. Souvent utilisée dans les ressources plus anciennes.

Vernis (KHR_materials_clearcoat)
: Ajoute une couche transparente avec sa propre rugosité et sa propre carte de normales.

Indice de réfraction (KHR_materials_ior)
: Ajoute un indice de réfraction.

Spéculaire (KHR_materials_specular)
: Ajoute des canaux dédiés à l'intensité et à la couleur spéculaires.

Iridescence (KHR_materials_iridescence)
: Simule les interférences de couches minces pour des matériaux comme les bulles de savon ou les perles.

Lustre (KHR_materials_sheen)
: Modélise les réflexions de microsurface semblables à celles d'un tissu.

Transmission (KHR_materials_transmission)
: Modélise la transmission de la lumière pour les matériaux transparents ou semblables au verre.

Volume (KHR_materials_volume)
: Prend en charge les effets volumétriques comme l'épaisseur et l'atténuation.

Intensité d'émission (KHR_materials_emissive_strength)
: Contrôle la luminosité émise indépendamment de la couleur de base.

Carte de normales
: Carte de normales pour les détails de surface.

Carte d'occlusion
: Carte d'occlusion ambiante.

Carte d'émission
: Texture auto-émissive pour les surfaces lumineuses.

Facteur d'émission
: Multiplicateur RGB de l'intensité d'émission.

Seuil alpha
: Seuil de transparence masquée.

Mode alpha
: Modes de transparence opaque, masquée ou mélangée.

Double face
: Demande le rendu des deux côtés de la surface. La passe de rendu doit permettre aux faces arrière d'atteindre le shader.

Sans éclairage
: Si vrai, le matériau ignore les calculs d'éclairage.

## Intégration aux shaders {#shader-integration}

Les sections suivantes concernent les shaders personnalisés. Copiez la ressource `.material` intégrée appropriée et `gltf.fp` dans votre projet, puis faites pointer le *Fragment Program* du matériau copié vers votre shader. Conservez le programme de sommets glTF correspondant, les noms des samplers et l'espace local des sommets, sauf si vous remplacez aussi ces interfaces.

Les fonctions utilitaires intégrées séparent l'échantillonnage des textures de la préparation des surfaces, des calculs de BRDF et de l'éclairage. `gltf_sampling.glsl` lit le bloc uniforme brut `PbrMaterial` et produit une valeur `PBRMaterial` contenant les entrées de matériau résolues et linéaires. `gltf_lighting.glsl` fournit l'éclairage direct et ambiant et combine leurs contributions. La capitalisation distingue le bloc uniforme brut de la structure du matériau échantillonné.

### Exemple de shader {#example-shader}

Ce shader de fragment augmente la rugosité minimale tout en conservant l'éclairage intégré. Il fonctionne avec les programmes de sommets utilisés par les quatre variantes de matériaux glTF :

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

Modifiez les entrées de matériau échantillonnées avant d'appeler `pbr_create_material_info()`. Si vous changez la position dans l'espace de vue ou les normales d'une surface, appelez `pbr_finalize_surface(surface, var_view)` pour actualiser ses champs dérivés dans l'espace monde. Pour une BRDF personnalisée ou des contributions lumineuses individuelles, utilisez ou remplacez `pbr_evaluate_brdf()` et `pbr_evaluate_light()` dans les fonctions utilitaires intégrées.

Vous pouvez remplacer `lighting.indirect` par votre propre éclairage d'environnement ou illumination globale. Ses contributions diffuses et spéculaires sont une lumière sortante linéaire ; n'appliquez donc pas une deuxième fois la BRDF du matériau. Appliquez la visibilité des ombres à la contribution lumineuse directe concernée ; les arguments de visibilité de `pbr_compose_lighting()` n'affectent que l'éclairage indirect. Pour un pipeline HDR, écrivez la couleur linéaire dans la cible intermédiaire et effectuez la conversion sRGB dans la passe finale.

### Données brutes du matériau {#raw-material-data}

Pour un shader entièrement personnalisé, déclarez un bloc uniforme nommé `PbrMaterial` avec les noms et types de membres reconnus. Defold remplit les champs correspondants depuis le matériau glTF source. Les déclarations ci-dessous décrivent les structures de fonctionnalités disponibles ; n'incluez que celles nécessaires à votre shader. Déclarer une structure fournit les données, mais votre shader doit implémenter son comportement d'échantillonnage et d'éclairage.

Ne redéclarez pas le bloc uniforme ni `PbrMetallicRoughness` lorsque vous incluez `gltf_sampling.glsl`, qui les déclare déjà. Les déclarations suivantes constituent une alternative pour les shaders qui gèrent leurs propres entrées de matériau.

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

Les propriétés communes et les structures de fonctionnalités sont des membres du bloc uniforme. Les composantes regroupées sont les suivantes :

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

Omettez les membres de fonctionnalités inutilisés du bloc. Si le bloc ou les champs reconnus d'une fonctionnalité sont absents, les données correspondantes ne sont pas fournies. Les indicateurs de présence de textures décrivent les références de textures du matériau source ; un matériau personnalisé a toujours besoin de déclarations de samplers et de liaisons de textures correspondantes pour les cartes qu'il échantillonne.

### Constantes {#constants}

Les champs de fonctionnalités utilisent des noms comme `pbrMetallicRoughness.baseColorFactor` ; les champs communs utilisent des noms comme `pbrEmissiveFactorAndStrength`. Le moteur renseigne ces constantes depuis le matériau importé, ou depuis un matériau par défaut lorsque le modèle ne contient pas de données de matériau. Définir des valeurs par défaut dans la ressource `.material` ne remplace pas les valeurs importées.

Pour personnaliser l'ombrage intégré, modifiez le `PBRMaterial` échantillonné avant de dériver ses valeurs de BRDF, comme dans l'exemple ci-dessus. Pour des contrôles supplémentaires à l'exécution, déclarez vos propres constantes de shader et utilisez l'[API des constantes de matériau de modèle](/manuals/model/#material-constants).

## Pour aller plus loin {#next-steps}

Utilisez les matériaux intégrés pour le flux glTF standard métal/rugosité. Étendez les fonctions utilitaires des shaders ou fournissez votre propre matériau lorsque vous avez besoin d'une BRDF différente, d'un éclairage d'environnement, d'ombres ou d'effets de matériau glTF supplémentaires.

Voir aussi :

* [Manuel des lumières](/manuals/light)
* [Manuel des matériaux](/manuals/material)
* [Manuel des shaders](/manuals/shader)
* [Manuel du rendu](/manuals/render)
* [Spécification glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
