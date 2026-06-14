---
title: Renderizado basado en física en Defold
brief: Este manual explica los conceptos básicos de cómo acceder a los datos de material para renderizado basado en física en Defold.
---

# Renderizado basado en física (PBR)

El renderizado basado en física (Physically Based Rendering, PBR) es un enfoque de shading que modela cómo la luz interactúa con las superficies usando principios físicos del mundo real. Produce iluminación consistente y realista en distintos entornos y permite que los assets se vean correctamente bajo una amplia variedad de condiciones de iluminación.

La implementación de PBR de Defold sigue la especificación de materiales glTF 2.0 y las extensiones Khronos asociadas. Cuando importas assets glTF en Defold, las propiedades de material se analizan automáticamente y se almacenan como datos de material estructurados a los que se puede acceder en shaders durante el tiempo de ejecución.

Los materiales PBR pueden incluir efectos como reflejos metálicos, rugosidad de superficie, transmisión, clearcoat, dispersión subsuperficial, iridiscencia y más.

::: sidenote
Defold actualmente expone datos de material PBR a los shaders, pero no proporciona un modelo de iluminación PBR integrado. Puedes usar estos datos en tus propios shaders de iluminación y reflexión para lograr renderizado basado en física. Un modelo de iluminación PBR predeterminado se agregará a Defold en una etapa posterior.
:::

::: sidenote
Actualmente, las texturas incrustadas de archivos glTF no se asignan automáticamente en Defold. Solo los parámetros de material se exponen a los shaders. Aun así, puedes asignar texturas manualmente a componentes de modelo y muestrearlas en tu shader.
:::

## Resumen de propiedades de material

Las propiedades de material se analizan desde los archivos fuente glTF 2.0 asignados a un componente de modelo. No todas las propiedades son estándar. Algunas se proporcionan mediante extensiones glTF opcionales que pueden estar incluidas o no por la herramienta usada para exportar el archivo glTF. La extensión relevante se indica entre paréntesis después del nombre de la propiedad a continuación.

Metallic roughness
: Describe cómo interactúa la luz con el material. Es el modelo PBR predeterminado.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: Una alternativa a metallic roughness. Se usa a menudo en assets más antiguos.

Clearcoat (KHR_materials_clearcoat)
: Agrega una capa de recubrimiento transparente con su propia rugosidad y normal map.

Ior (KHR_materials_ior)
: Agrega un índice de refracción.

Specular (KHR_materials_specular)
: Agrega un canal dedicado de intensidad especular y color.

Iridescence (KHR_materials_iridescence)
: Simula interferencia de película delgada para materiales como burbujas de jabón o perlas.

Sheen (KHR_materials_sheen)
: Modela reflejos de microsuperficie similares a los de una tela.

Transmission (KHR_materials_transmission)
: Modela la transmisión de luz para materiales transparentes o similares al vidrio.

Volume (KHR_materials_volume)
: Admite efectos volumétricos como grosor y atenuación.

Emissive strength (KHR_materials_emissive_strength)
: Controla el brillo emisivo independientemente del color base.

Normal map
: Normal map para detalle de superficie.

Occlusion map
: Mapa de oclusión ambiental.

Emissive map
: Textura autoemisiva para superficies que brillan.

Emissive factor
: Multiplicador RGB para intensidad emisiva.

Alpha cutoff
: Umbral para transparencia enmascarada.

Alpha mode
: Modos de transparencia Opaque, Masked o Blended.

Double sided
: Si es true, se renderizan ambos lados de la superficie.

Unlit
: Si es true, el material omite los cálculos de iluminación.

::: sidenote
Algunas de estas propiedades proporcionan indicios sobre cómo debe renderizarse el material. Los datos de las propiedades (alpha cutoff, alpha mode, double sided y unlit) están disponibles en los shaders, pero no afectan cómo se renderiza el material en Defold.
:::

## Integración con shaders

Los datos de material PBR se exponen a los shaders según tipos y una convención de nombres. El sistema de materiales PBR proporciona todos los parámetros de material analizados a los shaders mediante un bloque uniform estructurado llamado `PbrMaterial`. Cada extensión glTF admitida corresponde a un struct dentro de este bloque, que se puede compilar condicionalmente mediante flags `#define`.

```glsl
uniform PbrMaterial
{
	// Propiedades de material
};
```

Las distintas funcionalidades del material se especifican como structs fijos en el shader. Los datos se han empaquetado tanto como es posible en `vec4`, ya que así se definen internamente las constantes en Defold. En los casos en que los datos se han empaquetado, se indica como comentarios en los fragmentos de shader para cada funcionalidad a continuación:

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Predeterminado=1.0), G: roughness (Predeterminado=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: usar baseColorTexture, G: usar metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Predeterminado=1.0), A: glossiness (Predeterminado=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: usar diffuseTexture, G: usar specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
	// R: clearCoat (Predeterminado=0.0), G: clearCoatRoughness (Predeterminado=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: usar clearCoatTexture, G: usar clearCoatRoughnessTexture, B: usar clearCoatNormalTexture
	vec4 clearCoatTextures;
};

struct PbrTransmission
{
	// R: transmission (Predeterminado=0.0)
	vec4 transmissionFactor;
	// R: usar transmissionTexture
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (Predeterminado=0.0)
	vec4 ior;
};

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Predeterminado=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: usar specularTexture, G: usar specularColorTexture
	vec4 specularTextures;
};

struct PbrVolume
{
	// R: thicknessFactor (Predeterminado=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Predeterminado=-1.0)
	vec4 attenuationDistance;
	// R: usar thicknessTexture
	vec4 volumeTextures;
};

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (Predeterminado=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: usar sheenColorTexture, G: usar sheenRoughnessTexture
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (Predeterminado=1.0)
	vec4 emissiveStrength;
};

struct PbrIridescence
{
	// R: iridescenceFactor (Predeterminado=0.0), G: iridescenceIor (Predeterminado=1.3), B: iridescenceThicknessMin (Predeterminado=100.0), A: iridescenceThicknessMax (Predeterminado=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: usar iridescenceTexture, G: usar iridescenceThicknessTexture
	vec4 iridescenceTextures;
};
```

Las propiedades comunes se definen en el propio material uniform (y, de nuevo, nota el empaquetado de datos en `vec4`).

```glsl
// Texturas comunes
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// Propiedades comunes:

	// R: alphaCutoff (Predeterminado=0.5), G: doubleSided (Predeterminado=false), B: unlit (Predeterminado=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: usar normalTexture, G: usar occlusionTexture, B: usar emissiveTexture
	vec4 pbrCommonTextures;

	// Otras propiedades...
};
```

### Shader de ejemplo

Aquí tienes un shader de ejemplo que contiene todas las funcionalidades y un esquema de nombres propuesto para bindings de textura (de nuevo, esto debe gestionarse manualmente). Ten en cuenta que puedes desactivar funcionalidades simplemente usando `#define`s alrededor de cada miembro del propio `PbrMaterial`, como se muestra en el ejemplo a continuación:

```glsl
// Flags de funcionalidad; coméntalos o elimínalos para reducir el shader.
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

// Común
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Predeterminado=1.0), G: roughness (Predeterminado=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: usar baseColorTexture, G: usar metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

// PbrSpecularGlossiness
uniform sampler2D PbrSpecularGlossiness_diffuseTexture;
uniform sampler2D PbrSpecularGlossiness_specularGlossinessTexture;

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Predeterminado=1.0), A: glossiness (Predeterminado=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: usar diffuseTexture, G: usar specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

// PbrClearCoat
uniform sampler2D PbrClearCoat_clearcoatTexture;
uniform sampler2D PbrClearCoat_clearcoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearcoatNormalTexture;

struct PbrClearCoat
{
	// R: clearCoat (Predeterminado=0.0), G: clearCoatRoughness (Predeterminado=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: usar clearCoatTexture, G: usar clearCoatRoughnessTexture, B: usar clearCoatNormalTexture
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

struct PbrTransmission
{
	// R: transmission (Predeterminado=0.0)
	vec4 transmissionFactor;
	// R: usar transmissionTexture
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (Predeterminado=0.0)
	vec4 ior;
};

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Predeterminado=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: usar specularTexture, G: usar specularColorTexture
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (Predeterminado=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Predeterminado=-1.0)
	vec4 attenuationDistance;
	// R: usar thicknessTexture
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (Predeterminado=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: usar sheenColorTexture, G: usar sheenRoughnessTexture
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (Predeterminado=1.0)
	vec4 emissiveStrength;
};

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (Predeterminado=0.0), G: iridescenceIor (Predeterminado=1.3), B: iridescenceThicknessMin (Predeterminado=100.0), A: iridescenceThicknessMax (Predeterminado=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: usar iridescenceTexture, G: usar iridescenceThicknessTexture
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// Propiedades comunes
	// R: alphaCutoff (Predeterminado=0.5), G: doubleSided (Predeterminado=false), B: unlit (Predeterminado=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: usar normalTexture, G: usar occlusionTexture, B: usar emissiveTexture
	vec4 pbrCommonTextures;

	// Funcionalidades
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
Si no se encuentran puntos de datos específicos en el struct de material, los datos de esas funcionalidades no se definirán. Por ejemplo, si no hay `pbrClearCoat` en el struct de material, no se definirá ningún dato de clear coat. Si no se encuentra el bloque uniform, no se definirá ningún dato durante el renderizado.
:::

### Constantes

Cada propiedad de material corresponde a una constante de render interna en Defold. Puedes sobrescribir los valores predeterminados definiendo constantes en el propio recurso de material, siguiendo el patrón de nombres `pbrFeature.structMember`. Estos valores se aplicarán automáticamente si faltan los datos correspondientes en el material glTF.

![Constantes de material](images/physically-based-rendering/material-constants.png)

## Siguientes pasos

Para usar los datos de material para iluminación basada en física, implementa una BRDF en tu fragment shader usando los parámetros proporcionados en el bloque `PbrMaterial`.
Consulta también:

* [Manual de shaders](/manuals/shader)
* [Manual de render](/manuals/render)
* [especificación glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
