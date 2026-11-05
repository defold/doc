---
title: Defold의 물리 기반 렌더링
brief: 이 매뉴얼은 Defold의 내장 PBR 메터리얼을 사용하고 물리 기반 셰이딩을 사용자 지정하는 방법을 설명합니다.
---

# 물리 기반 렌더링(PBR)

물리 기반 렌더링(Physically Based Rendering, PBR)은 물리 법칙으로 빛과 표면의 상호작용을 모델링하는 셰이딩 방식입니다. 기본 색상, 금속성 계수, 거칠기 등의 메터리얼 프로퍼티는 씬의 조명과 독립적으로 표면을 설명합니다.

내장 glTF 메터리얼은 PBR 조명을 제공합니다. Defold는 임포트된 glTF 2.0 메터리얼 프로퍼티와 지원하는 Khronos 익스텐션 데이터도 커스텀 쉐이더에 노출합니다.

## 내장 PBR 메터리얼 {#built-in-pbr-materials}

glTF 또는 GLB 파일을 [Model 컴포넌트](/manuals/model)의 *Scene* 프로퍼티에 지정합니다. 에디터가 메터리얼과 텍스쳐 채우기를 제안하면 <kbd>Auto Fill</kbd>을 선택하여 씬에서 생성된 메터리얼 바인딩을 적용합니다. 기존 바인딩이 있으면 교체됩니다. 이 메터리얼은 내장 glTF 쉐이더를 사용하고 내장 이미지를 직접 참조할 수 있습니다. 바인딩을 유지하고 메터리얼과 텍스쳐를 직접 지정하려면 <kbd>Keep Current</kbd>를 선택하세요. 내장 리소스 탐색과 개별 메쉬 선택은 [모델 임포트 절차](/manuals/importing-models/#using-a-model)를 참고하세요.

`/builtins/materials/`에서 다음 메터리얼을 사용할 수 있습니다. 모델과 인스턴싱 사용 여부에 맞는 변형을 선택하세요:

| 모델 타입 | 메터리얼 |
|---|---|
| 정적, 인스턴싱 없음 | `gltf.material` |
| 정적, 인스턴싱 사용 | `gltf_instanced.material` |
| 스킨드(애니메이션), 인스턴싱 없음 | `gltf_skinned.material` |
| 스킨드(애니메이션), 인스턴싱 사용 | `gltf_skinned_instanced.material` |

네 가지 모두 로컬 버텍스 공간과 같은 `gltf.fp` 프래그먼트 쉐이더를 사용합니다. 스킨드 변형은 GPU에서 스키닝을 수행합니다. GPU 스키닝과 인스턴싱은 [모델 메터리얼 요구 사항](/manuals/model/#material)을 참고하세요.

텍스쳐를 직접 바인딩할 때 내장 메터리얼은 다음 샘플러 이름을 사용합니다:

| 텍스쳐 | 샘플러 | 사용 데이터 |
|---|---|---|
| 기본 색상 | `PbrMetallicRoughness_baseColorTexture` | RGB 색상과 알파 |
| 금속성/거칠기 | `PbrMetallicRoughness_metallicRoughnessTexture` | G의 거칠기, B의 금속성 |
| 노멀 | `PbrMaterial_normalTexture` | RGB의 탄젠트 공간 노멀 |
| 오클루전 | `PbrMaterial_occlusionTexture` | R의 오클루전 |
| 발광 | `PbrMaterial_emissiveTexture` | RGB 색상 |

[카메라](/manuals/camera/#using-the-camera)를 설정하고 [조명 컴포넌트](/manuals/light)를 추가하여 모델을 비춥니다. 쉐이더는 직접 조명에 방향성, 포인트, 스폿 조명을 사용하고, 간단한 주변광 효과에 앰비언트 조명을 사용합니다. 메터리얼에는 기본 렌더 스크립트가 그리는 `model` 태그가 있습니다. 커스텀 렌더 스크립트는 일치하는 프레디킷을 그려야 합니다.

### 내장 쉐이더 동작 {#built-in-shader-behavior}

내장 쉐이더는 금속성/거칠기 셰이딩, 기본 색상과 버텍스 색상, 탄젠트 데이터가 있을 때의 노멀 매핑, 오클루전, 발광 강도를 포함한 발광을 구현합니다. 기본 색상과 발광 텍스쳐는 조명 계산을 위해 sRGB에서 디코딩하고 최종 색상은 다시 sRGB로 변환합니다. 금속성/거칠기, 노멀, 오클루전 맵은 선형 데이터를 담습니다.

쉐이더는 비조명 메터리얼과 마스크 알파를 처리하고 양면 표면의 노멀을 조정합니다. 렌더 상태도 여전히 중요합니다:

- 양면 메터리얼에서는 뒷면이 쉐이더에 도달하도록 해당 렌더 패스의 면 컬링을 비활성화하세요.
- 혼합 알파에서 쉐이더는 straight alpha를 출력합니다. `graphics.BLEND_FACTOR_SRC_ALPHA`와 `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA`로 블렌딩을 활성화하고, 렌더 스크립트에서 투명 오브젝트의 그리기 순서와 깊이 쓰기를 관리하세요. 기본 모델 패스는 블렌딩을 자동으로 활성화하지 않습니다.

내장 주변광은 환경 맵 조명이나 그림자가 없는 근사 방식입니다. clearcoat, transmission, sheen, iridescence, specular/glossiness 워크플로우 등의 효과에는 커스텀 셰이딩이 필요합니다. 매개변수를 임포트하는 것만으로 `gltf.fp`에서 이 효과들이 활성화되지는 않습니다.

## 메터리얼 프로퍼티 개요

다음 프로퍼티는 모델 컴포넌트에 지정한 glTF 2.0 소스 파일에서 파싱됩니다. 이 목록은 사용할 수 있는 메터리얼 데이터를 설명하며, 내장 조명은 위에서 설명한 일부만 사용합니다. 모든 프로퍼티가 표준인 것은 아닙니다. 일부는 선택적 glTF 익스텐션에서 제공하므로 glTF를 익스포트하는 도구에 따라 포함되지 않을 수도 있습니다. 관련 익스텐션은 아래 프로퍼티 이름 뒤 괄호에 표시합니다.

메탈릭 러프니스(Metallic roughness)
: 빛이 메터리얼과 상호작용하는 방식을 설명합니다. 기본 PBR 모델입니다.

스페큘러 글로시니스(Specular glossiness) (KHR_materials_pbrSpecularGlossiness)
: 메탈릭 러프니스의 대안입니다. 오래된 에셋에서 자주 사용됩니다.

클리어코트(Clearcoat) (KHR_materials_clearcoat)
: 자체 러프니스와 노멀 맵을 가진 투명 코팅 레이어를 추가합니다.

굴절률(Ior) (KHR_materials_ior)
: 굴절률을 추가합니다.

스페큘러(Specular) (KHR_materials_specular)
: 전용 스페큘러 강도와 색상 채널을 추가합니다.

이리데선스(Iridescence) (KHR_materials_iridescence)
: 비누방울이나 진주 같은 메터리얼의 박막 간섭을 시뮬레이션합니다.

광택(Sheen) (KHR_materials_sheen)
: 천과 비슷한 미세 표면 반사를 모델링합니다.

투과(Transmission) (KHR_materials_transmission)
: 투명하거나 유리와 비슷한 메터리얼의 빛 투과를 모델링합니다.

볼륨(Volume) (KHR_materials_volume)
: 두께와 감쇠 같은 볼류메트릭 효과를 지원합니다.

방출 강도(Emissive strength) (KHR_materials_emissive_strength)
: 기본 색상과 독립적으로 방출 밝기를 제어합니다.

노멀 맵(Normal map)
: 표면 디테일을 위한 노멀 맵입니다.

오클루전 맵(Occlusion map)
: 앰비언트 오클루전 맵입니다.

방출 맵(Emissive map)
: 빛나는 표면을 위한 자체 발광 텍스쳐입니다.

방출 계수(Emissive factor)
: 방출 강도에 대한 RGB 곱셈값입니다.

알파 컷오프(Alpha cutoff)
: 마스크된 투명도의 임계값입니다.

알파 모드(Alpha mode)
: Opaque, Masked 또는 Blended 투명도 모드입니다.

양면(Double sided)
: 표면의 양면 렌더링을 요청합니다. 렌더 패스에서 뒷면이 쉐이더에 도달하도록 허용해야 합니다.

비조명(Unlit)
: true이면 메터리얼이 조명 계산을 우회합니다.

## 쉐이더 통합

다음 섹션은 커스텀 쉐이더를 다룹니다. 적절한 내장 `.material` 리소스와 `gltf.fp`를 프로젝트에 복사한 다음 복사한 메터리얼의 *Fragment Program*을 자신의 쉐이더로 지정합니다. 해당 인터페이스도 교체하는 경우가 아니라면 일치하는 glTF 버텍스 프로그램, 샘플러 이름, 로컬 버텍스 공간을 유지하세요.

내장 헬퍼는 텍스쳐 샘플링을 표면 준비, BRDF 계산, 조명과 분리합니다. `gltf_sampling.glsl`은 원시 `PbrMaterial` uniform 블록을 읽어 해석된 선형 메터리얼 입력을 담은 `PBRMaterial` 값을 만듭니다. `gltf_lighting.glsl`은 직접 조명과 주변광을 제공하고 결과를 결합합니다. 대소문자 차이로 원시 uniform 블록과 샘플링된 메터리얼 구조체를 구분합니다.

### 예제 쉐이더

다음 프래그먼트 쉐이더는 내장 조명을 유지하면서 최소 거칠기를 높입니다. 네 가지 glTF 메터리얼 변형이 사용하는 버텍스 프로그램 모두에서 동작합니다:

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

`pbr_create_material_info()`를 호출하기 전에 샘플링된 메터리얼 입력을 수정합니다. 표면의 뷰 공간 위치나 노멀을 바꾸면 `pbr_finalize_surface(surface, var_view)`를 호출하여 파생된 월드 공간 필드를 갱신하세요. 커스텀 BRDF나 개별 조명의 기여도를 처리하려면 내장 헬퍼의 `pbr_evaluate_brdf()`와 `pbr_evaluate_light()`를 사용하거나 교체하세요.

`lighting.indirect`를 자신의 환경 조명이나 전역 조명으로 교체할 수 있습니다. diffuse와 specular 성분은 선형 출사광이므로 메터리얼의 BRDF를 다시 적용하지 마세요. 그림자 가시성은 해당 직접 조명 성분에 적용하세요. `pbr_compose_lighting()`의 가시성 인자는 간접 조명에만 영향을 줍니다. HDR 파이프라인에서는 중간 타겟에 선형 색상을 기록하고 최종 패스에서 sRGB로 변환합니다.

### 원시 메터리얼 데이터 {#raw-material-data}

완전히 커스텀인 쉐이더는 인식되는 멤버 이름과 타입으로 `PbrMaterial` uniform 블록을 선언합니다. Defold는 원본 glTF 메터리얼에서 일치하는 필드를 채웁니다. 아래 선언은 사용할 수 있는 기능 구조체를 설명하며 쉐이더에 필요한 것만 포함하세요. 구조체 선언은 데이터를 제공하지만 샘플링과 조명 동작은 쉐이더에서 구현해야 합니다.

`gltf_sampling.glsl`에는 이미 uniform 블록과 `PbrMetallicRoughness`가 선언되어 있으므로 이를 포함할 때 중복 선언하지 마세요. 다음 선언은 메터리얼 입력을 직접 관리하는 쉐이더를 위한 대안입니다.

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

공통 프로퍼티와 기능 구조체는 uniform 블록의 멤버입니다. 패킹된 성분은 다음과 같습니다:

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

사용하지 않는 기능 멤버는 블록에서 생략하세요. 블록이나 기능의 인식되는 필드가 없으면 해당 데이터는 제공되지 않습니다. 텍스쳐 존재 플래그는 원본 메터리얼의 텍스쳐 참조를 나타냅니다. 커스텀 메터리얼에는 샘플링할 맵에 맞는 샘플러 선언과 텍스쳐 바인딩이 여전히 필요합니다.

### 상수

기능 필드는 `pbrMetallicRoughness.baseColorFactor` 같은 이름을, 공통 필드는 `pbrEmissiveFactorAndStrength` 같은 이름을 사용합니다. 엔진은 임포트된 메터리얼에서 이 상수들을 채우며, 모델에 메터리얼 데이터가 없으면 기본 메터리얼을 사용합니다. `.material` 리소스에 기본값을 설정해도 임포트된 값을 덮어쓰지 않습니다.

내장 셰이딩을 변경하려면 위 예제처럼 BRDF 값을 계산하기 전에 샘플링된 `PBRMaterial`을 수정합니다. 추가 런타임 제어가 필요하면 자신의 쉐이더 상수를 선언하고 [모델 메터리얼 상수 API](/manuals/model/#material-constants)를 사용하세요.

## 다음 단계

표준 glTF metallic/roughness 워크플로우에는 내장 메터리얼을 사용합니다. 다른 BRDF, 환경 조명, 그림자, 추가 glTF 메터리얼 효과가 필요하면 쉐이더 헬퍼를 확장하거나 자신의 메터리얼을 제공하세요.

참고 항목:

* [조명 매뉴얼](/manuals/light)
* [메터리얼 매뉴얼](/manuals/material)
* [쉐이더 매뉴얼](/manuals/shader)
* [렌더 매뉴얼](/manuals/render)
* [glTF 2.0 명세](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
