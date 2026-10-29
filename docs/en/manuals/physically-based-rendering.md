---
title: Physically based rendering in Defold
brief: This manual explains how to use built-in PBR materials and customize physically based shading in Defold.
---

# Physically Based Rendering (PBR)

Physically Based Rendering (PBR) is a shading approach that models how light interacts with surfaces using physical principles. Material properties such as base color, metallic factor and roughness describe the surface independently of the scene's lighting.

Since Defold 1.14.1, built-in glTF materials provide PBR lighting. Defold also exposes imported glTF 2.0 material properties and supported Khronos extension data to custom shaders.

## Built-in PBR materials

Assign a glTF or GLB file to the *Scene* property of a [Model component](/manuals/model). When the editor offers to fill in materials and textures, accepting the offer applies the scene's generated material bindings, replacing existing bindings if present. These materials use the built-in glTF shaders. You can also assign materials and textures manually.

The following materials are available in `/builtins/materials/`. Choose the variant that matches your model and whether it uses instancing:

| Model type | Material |
|---|---|
| Static, non-instanced | `gltf.material` |
| Static, instanced | `gltf_instanced.material` |
| Skinned (animated), non-instanced | `gltf_skinned.material` |
| Skinned (animated), instanced | `gltf_skinned_instanced.material` |

All four use local vertex space and the same `gltf.fp` fragment shader. The skinned variants perform skinning on the GPU. See the [model material requirements](/manuals/model/#material) for GPU skinning and instancing.

For manual texture bindings, the built-in materials use these sampler names:

| Texture | Sampler | Data used |
|---|---|---|
| Base color | `PbrMetallicRoughness_baseColorTexture` | RGB color and alpha |
| Metallic/roughness | `PbrMetallicRoughness_metallicRoughnessTexture` | Roughness in G, metallic in B |
| Normal | `PbrMaterial_normalTexture` | Tangent-space normal in RGB |
| Occlusion | `PbrMaterial_occlusionTexture` | Occlusion in R |
| Emissive | `PbrMaterial_emissiveTexture` | RGB color |

Set up a [camera](/manuals/camera/#using-the-camera) and add [light components](/manuals/light) to illuminate the model. The shader uses directional, point and spot lights for direct lighting, plus ambient lights for a simple ambient contribution. The materials have the `model` tag, which the default render script draws. A custom render script must draw a matching predicate.

### Built-in shader behavior

The built-in shaders implement metallic/roughness shading, base color and vertex color, normal mapping when tangent data is available, occlusion, and emission including emissive strength. Base-color and emissive textures are decoded from sRGB for lighting, and the final color is converted back to sRGB. Metallic/roughness, normal and occlusion maps contain linear data.

The shader honors unlit materials and masked alpha, and adjusts normals for double-sided surfaces. Render state still matters:

- For double-sided materials, disable face culling in the relevant render pass so back faces reach the shader.
- For blended alpha, the shader outputs straight alpha. Enable blending with `graphics.BLEND_FACTOR_SRC_ALPHA` and `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA`, and manage transparent-object draw order and depth writes in your render script. The default model pass does not enable blending automatically.

The built-in ambient contribution is an approximation, without environment-map lighting or shadows. Effects such as clearcoat, transmission, sheen, iridescence and the specular/glossiness workflow require custom shading; importing their parameters does not enable these effects in `gltf.fp`.

## Material properties overview

The following properties are parsed from glTF 2.0 source files assigned to a model component. This list describes the available material data; the built-in lighting uses the subset described above. Not all properties are standard. Some are provided through optional glTF extensions that may or may not be included by the tool used to export the glTF file. The relevant extension is denoted in parentheses after the property name below.

Metallic roughness
: Describes how light interacts with the material. The default PBR model.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: An alternative to metallic roughness. Often used in older assets.

Clearcoat (KHR_materials_clearcoat)
: Adds a transparent coating layer with its own roughness and normal map.

Ior (KHR_materials_ior)
: Adds an index of refraction.

Specular (KHR_materials_specular)
: Adds a dedicated specular intensity and color channel.

Iridescence (KHR_materials_iridescence)
: Simulates thin-film interference for materials like soap bubbles or pearls.

Sheen (KHR_materials_sheen)
: Models fabric-like micro-surface reflections.

Transmission (KHR_materials_transmission)
: Models light transmission for transparent or glass-like materials.

Volume (KHR_materials_volume)
: Supports volumetric effects like thickness and attenuation.

Emissive strength (KHR_materials_emissive_strength)
: Controls emissive brightness independent of base color.

Normal map
: Normal map for surface detail.

Occlusion map
: Ambient occlusion map.

Emissive map
: Self-emissive texture for glowing surfaces.

Emissive factor
: RGB multiplier for emissive intensity

Alpha cutoff
: Threshold for masked transparency.

Alpha mode
: Opaque, Masked, or Blended transparency modes.

Double sided
: Requests rendering of both sides of the surface. The render pass must allow back faces to reach the shader.

Unlit
: If true, the material bypasses lighting calculations.

## Shader integration

The following sections cover custom shaders. Copy the appropriate built-in `.material` resource and `gltf.fp` into your project, then point the copied material's *Fragment Program* to your shader. Keep the matching glTF vertex program, sampler names and local vertex space unless you are also replacing those interfaces.

The built-in helpers separate texture sampling from surface preparation, BRDF calculations and lighting. `gltf_sampling.glsl` reads the raw `PbrMaterial` uniform block and produces a `PBRMaterial` value containing resolved, linear material inputs. `gltf_lighting.glsl` provides direct and ambient lighting and combines their contributions. The capitalization distinguishes the raw uniform block from the sampled material struct.

### Example shader

This fragment shader raises the minimum roughness while retaining the built-in lighting. It works with the vertex programs used by all four glTF material variants:

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

Edit sampled material inputs before calling `pbr_create_material_info()`. If you change a surface's view-space position or normals, call `pbr_finalize_surface(surface, var_view)` to update its derived world-space fields. For a custom BRDF or individual light contributions, use or replace `pbr_evaluate_brdf()` and `pbr_evaluate_light()` from the built-in helpers.

You can replace `lighting.indirect` with your own environment lighting or global illumination. Its diffuse and specular contributions are linear outgoing light, so do not apply the material's BRDF a second time. Apply shadow visibility to the appropriate direct-light contribution; the visibility arguments to `pbr_compose_lighting()` affect indirect lighting only. For an HDR pipeline, write linear color to the intermediate target and perform the sRGB conversion in the final pass.

### Raw material data

For a fully custom shader, declare a uniform block named `PbrMaterial` with the recognized member names and types. Defold fills matching fields from the source glTF material. The declarations below describe the available feature structs; include only those your shader needs. Declaring a struct supplies data, but your shader must implement its sampling and lighting behavior.

Do not redeclare the uniform block or `PbrMetallicRoughness` when including `gltf_sampling.glsl`, which already declares them. The following declarations are an alternative for shaders that manage their own material inputs.

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

The common properties and feature structs are members of the uniform block. The packed components are:

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

Omit unused feature members from the block. If the block or a feature's recognized fields are absent, the corresponding data is not supplied. Texture-presence flags describe the source material's texture references; a custom material still needs matching sampler declarations and texture bindings for the maps it samples.

### Constants

Feature fields use names such as `pbrMetallicRoughness.baseColorFactor`; common fields use names such as `pbrEmissiveFactorAndStrength`. The engine populates these constants from the imported material, or from a default material when the model has no material data. Setting defaults in the `.material` resource does not override the imported values.

To customize the built-in shading, edit the sampled `PBRMaterial` before deriving its BRDF values, as in the example above. For additional runtime controls, declare your own shader constants and use the [model material constant API](/manuals/model/#material-constants).

## Next steps

Use the built-in materials for the standard glTF metallic/roughness workflow. Extend the shader helpers or provide your own material when you need a different BRDF, environment lighting, shadows or additional glTF material effects.

See also:

* [Light manual](/manuals/light)
* [Material manual](/manuals/material)
* [Shaders manual](/manuals/shader)
* [Render manual](/manuals/render)
* [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
