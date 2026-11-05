---
title: Renderizado basado en física en Defold
brief: Este manual explica cómo usar materiales PBR integrados y personalizar el sombreado basado en física en Defold.
---

# Renderizado basado en física (PBR) {#physically-based-rendering-pbr}

El renderizado basado en física (Physically Based Rendering, PBR) es una técnica de sombreado que modela la interacción de la luz con las superficies mediante principios físicos. Las propiedades del material, como el color base, el factor metálico y la rugosidad, describen la superficie independientemente de la iluminación de la escena.

Los materiales glTF integrados proporcionan iluminación PBR. Defold también expone a shaders personalizados las propiedades de materiales glTF 2.0 importados y los datos de las extensiones Khronos admitidas.

## Materiales PBR integrados {#built-in-pbr-materials}

Asigna un archivo glTF o GLB a la propiedad *Scene* de un [componente Model](/manuals/model). Cuando el editor ofrezca completar materiales y texturas, elige <kbd>Auto Fill</kbd> para aplicar las asignaciones de materiales generadas de la escena y reemplazar las existentes. Estos materiales usan los shaders glTF integrados y pueden referenciar directamente imágenes integradas. Elige <kbd>Keep Current</kbd> para conservar tus asignaciones y establecer materiales y texturas manualmente. Consulta el [flujo de importación de modelos](/manuals/importing-models/#using-a-model) para explorar recursos integrados y seleccionar mallas individuales.

Los siguientes materiales están disponibles en `/builtins/materials/`. Elige la variante que corresponda a tu modelo y al uso de instancias:

| Tipo de modelo | Material |
|---|---|
| Estático, sin instancias | `gltf.material` |
| Estático, con instancias | `gltf_instanced.material` |
| Con skinning (animado), sin instancias | `gltf_skinned.material` |
| Con skinning (animado), con instancias | `gltf_skinned_instanced.material` |

Los cuatro usan espacio de vértices local y el mismo fragment shader `gltf.fp`. Las variantes con skinning lo realizan en la GPU. Consulta los [requisitos de materiales de modelos](/manuals/model/#material) para conocer el skinning en GPU y el uso de instancias.

Para asignar texturas manualmente, los materiales integrados usan estos nombres de sampler:

| Textura | Sampler | Datos usados |
|---|---|---|
| Color base | `PbrMetallicRoughness_baseColorTexture` | Color RGB y alpha |
| Metálico/rugosidad | `PbrMetallicRoughness_metallicRoughnessTexture` | Rugosidad en G, factor metálico en B |
| Normal | `PbrMaterial_normalTexture` | Normal en espacio tangente en RGB |
| Oclusión | `PbrMaterial_occlusionTexture` | Oclusión en R |
| Emisiva | `PbrMaterial_emissiveTexture` | Color RGB |

Configura una [cámara](/manuals/camera/#using-the-camera) y agrega [componentes de luz](/manuals/light) para iluminar el modelo. El shader usa luces direccionales, puntuales y focos para la iluminación directa, además de luces ambientales para una contribución ambiental sencilla. Los materiales tienen la etiqueta `model`, que dibuja el script de render predeterminado. Un script de render personalizado debe dibujar un predicado correspondiente.

### Comportamiento de los shaders integrados {#built-in-shader-behavior}

Los shaders integrados implementan sombreado metálico/rugosidad, color base y de vértices, mapeo de normales cuando hay datos tangentes, oclusión y emisión, incluida la intensidad emisiva. Las texturas de color base y emisivas se decodifican desde sRGB para la iluminación, y el color final se vuelve a convertir a sRGB. Los mapas de metálico/rugosidad, normales y oclusión contienen datos lineales.

El shader respeta los materiales sin iluminación y el alpha enmascarado, y ajusta las normales de las superficies de doble cara. El estado de renderizado sigue siendo relevante:

- Para materiales de doble cara, desactiva el descarte de caras en el paso de renderizado correspondiente para que las caras traseras lleguen al shader.
- Para alpha mezclado, el shader genera alpha no premultiplicado. Activa la mezcla con `graphics.BLEND_FACTOR_SRC_ALPHA` y `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA`, y gestiona el orden de dibujo de los objetos transparentes y las escrituras de profundidad en tu script de render. El paso de modelos predeterminado no activa la mezcla automáticamente.

La contribución ambiental integrada es una aproximación, sin iluminación mediante mapas de entorno ni sombras. Los efectos como clearcoat, transmisión, sheen, iridiscencia y el flujo especular/brillo requieren sombreado personalizado; importar sus parámetros no activa esos efectos en `gltf.fp`.

## Resumen de propiedades de material {#material-properties-overview}

Las siguientes propiedades se analizan a partir de los archivos fuente glTF 2.0 asignados a un componente Model. Esta lista describe los datos de material disponibles; la iluminación integrada usa el subconjunto descrito anteriormente. No todas las propiedades son estándar. Algunas proceden de extensiones glTF opcionales que la herramienta usada para exportar el archivo puede incluir o no. La extensión correspondiente se indica entre paréntesis después del nombre de la propiedad.

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
: Solicita renderizar ambos lados de la superficie. El paso de renderizado debe permitir que las caras traseras lleguen al shader.

Unlit
: Si es true, el material omite los cálculos de iluminación.

## Integración con shaders {#shader-integration}

Las siguientes secciones tratan los shaders personalizados. Copia el recurso `.material` integrado adecuado y `gltf.fp` a tu proyecto, y apunta el *Fragment Program* del material copiado a tu shader. Conserva el vertex program glTF correspondiente, los nombres de sampler y el espacio de vértices local, salvo que también reemplaces esas interfaces.

Las funciones auxiliares integradas separan el muestreo de texturas de la preparación de superficies, los cálculos BRDF y la iluminación. `gltf_sampling.glsl` lee el bloque uniform sin procesar `PbrMaterial` y produce un valor `PBRMaterial` con las entradas de material resueltas y lineales. `gltf_lighting.glsl` proporciona iluminación directa y ambiental y combina sus contribuciones. Las mayúsculas distinguen el bloque uniform sin procesar del struct de material muestreado.

### Shader de ejemplo {#example-shader}

Este fragment shader aumenta la rugosidad mínima conservando la iluminación integrada. Funciona con los vertex programs que usan las cuatro variantes de materiales glTF:

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

Edita las entradas del material muestreado antes de llamar a `pbr_create_material_info()`. Si cambias la posición o las normales de una superficie en espacio de vista, llama a `pbr_finalize_surface(surface, var_view)` para actualizar sus campos derivados en espacio del mundo. Para una BRDF personalizada o contribuciones de luz individuales, usa o reemplaza `pbr_evaluate_brdf()` y `pbr_evaluate_light()` de las funciones auxiliares integradas.

Puedes reemplazar `lighting.indirect` por tu propia iluminación de entorno o iluminación global. Sus contribuciones difusa y especular son luz saliente lineal, por lo que no debes aplicar la BRDF del material por segunda vez. Aplica la visibilidad de sombras a la contribución de luz directa correspondiente; los argumentos de visibilidad de `pbr_compose_lighting()` solo afectan a la iluminación indirecta. Para un pipeline HDR, escribe color lineal en el destino intermedio y realiza la conversión sRGB en el paso final.

### Datos de material sin procesar {#raw-material-data}

Para un shader totalmente personalizado, declara un bloque uniform llamado `PbrMaterial` con los nombres y tipos de miembros reconocidos. Defold rellena los campos correspondientes a partir del material glTF fuente. Las declaraciones siguientes describen los structs de funcionalidades disponibles; incluye solo los que necesite tu shader. Declarar un struct proporciona datos, pero tu shader debe implementar su muestreo e iluminación.

No vuelvas a declarar el bloque uniform ni `PbrMetallicRoughness` al incluir `gltf_sampling.glsl`, que ya los declara. Las siguientes declaraciones son una alternativa para shaders que gestionan sus propias entradas de material.

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

Las propiedades comunes y los structs de funcionalidades son miembros del bloque uniform. Los componentes empaquetados son:

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

Omite del bloque los miembros de funcionalidades que no uses. Si el bloque o los campos reconocidos de una funcionalidad no están presentes, no se suministran los datos correspondientes. Los indicadores de presencia de textura describen las referencias a texturas del material fuente; un material personalizado sigue necesitando declaraciones de sampler y asignaciones de texturas correspondientes para los mapas que muestrea.

### Constantes {#constants}

Los campos de funcionalidades usan nombres como `pbrMetallicRoughness.baseColorFactor`; los campos comunes usan nombres como `pbrEmissiveFactorAndStrength`. El motor rellena estas constantes a partir del material importado, o de un material predeterminado cuando el modelo no tiene datos de material. Establecer valores predeterminados en el recurso `.material` no reemplaza los valores importados.

Para personalizar el sombreado integrado, edita el `PBRMaterial` muestreado antes de derivar sus valores BRDF, como en el ejemplo anterior. Para controles adicionales en runtime, declara tus propias constantes de shader y usa la [API de constantes de material de modelos](/manuals/model/#material-constants).

## Siguientes pasos {#next-steps}

Usa los materiales integrados para el flujo estándar glTF metálico/rugosidad. Amplía las funciones auxiliares de shaders o proporciona tu propio material si necesitas otra BRDF, iluminación de entorno, sombras o efectos adicionales de materiales glTF.

Consulta también:

* [Manual de luces](/manuals/light)
* [Manual de materiales](/manuals/material)
* [Manual de shaders](/manuals/shader)
* [Manual de render](/manuals/render)
* [especificación glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
