---
title: Defold의 물리 기반 렌더링
brief: 이 매뉴얼은 Defold에서 물리 기반 렌더링에 사용할 메터리얼 데이터에 액세스하는 기본 방법을 설명합니다.
---

# 물리 기반 렌더링(PBR)

물리 기반 렌더링(Physically Based Rendering, PBR)은 현실 세계의 물리 원리를 사용해 빛이 표면과 상호작용하는 방식을 모델링하는 쉐이딩 방식입니다. 다양한 환경에서 일관되고 사실적인 조명을 만들며, 폭넓은 조명 조건에서도 에셋이 올바르게 보이도록 합니다.

Defold의 PBR 구현은 glTF 2.0 메터리얼 명세와 관련 Khronos 익스텐션을 따릅니다. glTF 에셋을 Defold로 임포트하면 메터리얼 프로퍼티가 자동으로 파싱되어, 런타임에 쉐이더에서 액세스할 수 있는 구조화된 메터리얼 데이터로 저장됩니다.

PBR 메터리얼에는 메탈릭 반사, 표면 러프니스, 투과(transmission), 클리어코트(clearcoat), 서브서피스 스캐터링(subsurface scattering), 이리데선스(iridescence) 등의 효과가 포함될 수 있습니다.

::: sidenote
Defold는 현재 PBR 메터리얼 데이터를 쉐이더에 노출하지만, 내장 PBR 조명 모델은 제공하지 않습니다. 물리 기반 렌더링을 구현하려면 이 데이터를 자체 조명 및 반사 쉐이더에서 사용할 수 있습니다. 기본 PBR 조명 모델은 추후 Defold에 추가될 예정입니다.
:::

::: sidenote
glTF 파일에 내장된 텍스쳐는 현재 Defold에서 자동으로 할당되지 않습니다. 쉐이더에는 메터리얼 파라미터만 노출됩니다. 그래도 텍스쳐를 모델 컴포넌트에 수동으로 할당하고 쉐이더에서 샘플링할 수 있습니다.
:::

## 메터리얼 프로퍼티 개요

메터리얼 프로퍼티는 모델 컴포넌트에 할당된 glTF 2.0 소스 파일에서 파싱됩니다. 모든 프로퍼티가 표준은 아닙니다. 일부 프로퍼티는 glTF 파일을 익스포트하는 데 사용한 도구에 포함될 수도 있고 포함되지 않을 수도 있는 선택적 glTF 익스텐션을 통해 제공됩니다. 관련 익스텐션은 아래 프로퍼티 이름 뒤의 괄호 안에 표시되어 있습니다.

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
: true이면 표면의 양쪽 면이 모두 렌더링됩니다.

비조명(Unlit)
: true이면 메터리얼이 조명 계산을 우회합니다.

::: sidenote
이 프로퍼티 중 일부는 메터리얼을 렌더링하는 방법에 대한 힌트를 제공합니다. 해당 프로퍼티(alpha cutoff, alpha mode, double sided, unlit)의 데이터는 쉐이더에서 사용할 수 있지만, Defold에서 메터리얼이 렌더링되는 방식에는 영향을 주지 않습니다.
:::

## 쉐이더 통합

PBR 메터리얼 데이터는 타입과 이름 규칙을 기준으로 쉐이더에 노출됩니다. PBR 메터리얼 시스템은 파싱된 모든 메터리얼 파라미터를 `PbrMaterial`이라는 구조화된 uniform 블록을 통해 쉐이더에 제공합니다. 지원되는 각 glTF 익스텐션은 이 블록 안의 struct에 대응하며, `#define` 플래그를 사용해 조건부로 컴파일할 수 있습니다.

```glsl
uniform PbrMaterial
{
	// 메터리얼 프로퍼티
};
```

메터리얼의 여러 기능은 쉐이더에서 고정된 struct로 지정됩니다. Defold 내부에서 상수가 설정되는 방식에 맞게 데이터는 가능한 한 `vec4`에 패킹되어 있습니다. 데이터가 패킹된 경우에는 아래 각 기능의 쉐이더 스니펫에 주석으로 표시되어 있습니다:

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (기본값=1.0), G: roughness (기본값=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: baseColorTexture 사용, G: metallicRoughnessTexture 사용
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (기본값=1.0), A: glossiness (기본값=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: diffuseTexture 사용, G: specularGlossinessTexture 사용
	vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
	// R: clearCoat (기본값=0.0), G: clearCoatRoughness (기본값=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: clearCoatTexture 사용, G: clearCoatRoughnessTexture 사용, B: clearCoatNormalTexture 사용
	vec4 clearCoatTextures;
};

struct PbrTransmission
{
	// R: transmission (기본값=0.0)
	vec4 transmissionFactor;
	// R: transmissionTexture 사용
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (기본값=0.0)
	vec4 ior;
};

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (기본값=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: specularTexture 사용, G: specularColorTexture 사용
	vec4 specularTextures;
};

struct PbrVolume
{
	// R: thicknessFactor (기본값=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (기본값=-1.0)
	vec4 attenuationDistance;
	// R: thicknessTexture 사용
	vec4 volumeTextures;
};

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (기본값=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: sheenColorTexture 사용, G: sheenRoughnessTexture 사용
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (기본값=1.0)
	vec4 emissiveStrength;
};

struct PbrIridescence
{
	// R: iridescenceFactor (기본값=0.0), G: iridescenceIor (기본값=1.3), B: iridescenceThicknessMin (기본값=100.0), A: iridescenceThicknessMax (기본값=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: iridescenceTexture 사용, G: iridescenceThicknessTexture 사용
	vec4 iridescenceTextures;
};
```

공통 프로퍼티는 메터리얼 uniform 자체에 설정됩니다(다시 말하지만 데이터가 `vec4`로 패킹된다는 점에 유의하세요).

```glsl
// 공통 텍스쳐
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// 공통 프로퍼티:

	// R: alphaCutoff (기본값=0.5), G: doubleSided (기본값=false), B: unlit (기본값=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: normalTexture 사용, G: occlusionTexture 사용, B: emissiveTexture 사용
	vec4 pbrCommonTextures;

	// 다른 프로퍼티...
};
```

### 예제 쉐이더

다음은 모든 기능을 포함하고 텍스쳐 바인딩에 대해 제안하는 이름 지정 방식을 보여주는 예제 쉐이더입니다(이 역시 수동으로 처리해야 합니다). 아래 예제처럼 `PbrMaterial` 자체의 각 멤버를 `#define` 조건으로 감싸면 기능을 간단히 끌 수 있습니다:

```glsl
// 기능 플래그입니다. 쉐이더를 줄이려면 주석 처리하거나 제거하세요.
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

// 공통
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (기본값=1.0), G: roughness (기본값=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: baseColorTexture 사용, G: metallicRoughnessTexture 사용
    vec4 metallicRoughnessTextures;
};

// PbrSpecularGlossiness
uniform sampler2D PbrSpecularGlossiness_diffuseTexture;
uniform sampler2D PbrSpecularGlossiness_specularGlossinessTexture;

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (기본값=1.0), A: glossiness (기본값=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: diffuseTexture 사용, G: specularGlossinessTexture 사용
	vec4 specularGlossinessTextures;
};

// PbrClearCoat
uniform sampler2D PbrClearCoat_clearcoatTexture;
uniform sampler2D PbrClearCoat_clearcoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearcoatNormalTexture;

struct PbrClearCoat
{
	// R: clearCoat (기본값=0.0), G: clearCoatRoughness (기본값=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: clearCoatTexture 사용, G: clearCoatRoughnessTexture 사용, B: clearCoatNormalTexture 사용
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

struct PbrTransmission
{
	// R: transmission (기본값=0.0)
	vec4 transmissionFactor;
	// R: transmissionTexture 사용
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (기본값=0.0)
	vec4 ior;
};

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (기본값=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: specularTexture 사용, G: specularColorTexture 사용
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (기본값=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (기본값=-1.0)
	vec4 attenuationDistance;
	// R: thicknessTexture 사용
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (기본값=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: sheenColorTexture 사용, G: sheenRoughnessTexture 사용
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (기본값=1.0)
	vec4 emissiveStrength;
};

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (기본값=0.0), G: iridescenceIor (기본값=1.3), B: iridescenceThicknessMin (기본값=100.0), A: iridescenceThicknessMax (기본값=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: iridescenceTexture 사용, G: iridescenceThicknessTexture 사용
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// 공통 프로퍼티
	// R: alphaCutoff (기본값=0.5), G: doubleSided (기본값=false), B: unlit (기본값=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: normalTexture 사용, G: occlusionTexture 사용, B: emissiveTexture 사용
	vec4 pbrCommonTextures;

	// 기능
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
메터리얼 struct에서 특정 데이터 포인트를 찾지 못하면 해당 기능의 데이터는 설정되지 않습니다. 예를 들어 메터리얼 struct에 `pbrClearCoat`가 없으면 클리어코트 데이터가 설정되지 않습니다. uniform 블록을 찾지 못하면 렌더링 중 어떤 데이터도 설정되지 않습니다.
:::

### 상수

각 메터리얼 프로퍼티는 Defold 내부의 렌더 상수에 대응합니다. 메터리얼 리소스 자체에 `pbrFeature.structMember` 이름 패턴을 따르는 상수를 정의하여 기본값을 오버라이드할 수 있습니다. glTF 메터리얼에 일치하는 데이터가 없으면 이 값이 자동으로 적용됩니다.

![메터리얼 상수](images/physically-based-rendering/material-constants.png)

## 다음 단계

메터리얼 데이터를 물리 기반 조명에 사용하려면 `PbrMaterial` 블록에서 제공되는 파라미터를 사용해 프래그먼트 쉐이더에 BRDF를 구현하세요.
참고 항목:

* [쉐이더 매뉴얼](/manuals/shader)
* [렌더 매뉴얼](/manuals/render)
* [glTF 2.0 명세](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
