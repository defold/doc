---
title: Defold의 Light 컴포넌트
brief: 이 매뉴얼은 환경광, 방향광, 점광원 및 스포트라이트를 사용하는 방법과 쉐이더에서 라이트 데이터에 액세스하는 방법을 설명합니다.
---

# Light 컴포넌트

Light 컴포넌트는 컬렉션의 광원을 나타냅니다. 현재 Defold는 다음 네 가지 라이트 리소스 타입을 지원합니다:

- 환경광(Ambient light) (`.ambient_light`)
- 방향광(Directional light) (`.directional_light`)
- 점광원(Point light) (`.point_light`)
- 스포트라이트(Spot light) (`.spot_light`)

라이트 리소스는 다른 컴포넌트 리소스와 마찬가지로 게임 오브젝트에 추가합니다. 게임 오브젝트 바로 아래에 라이트 컴포넌트를 생성하거나, *Assets* 브라우저에서 라이트 리소스를 생성한 다음 *Outline* 창에서 게임 오브젝트에 컴포넌트로 추가할 수 있습니다.

Defold는 모든 메터리얼에 조명을 자동으로 적용하지 않습니다. 엔진이 라이트를 수집하여 내장 라이트 버퍼를 통해 쉐이더에 제공합니다. 라이트 데이터를 어떻게 사용할지는 메터리얼 쉐이더에서 결정합니다.

아래 예제에서는 동일한 씬을 사용하여 각 라이트 타입이 최종 결과에 미치는 영향을 보여줍니다:

![라이트가 없는 씬](images/light/no_light.png)

## 라이트 프로퍼티

모든 라이트 색상은 RGB 값입니다. 라이트 리소스에서는 알파 채널을 사용하지 않습니다.

### 환경광

환경광은 씬에 일정한 빛을 더합니다. 게임 오브젝트의 위치, 회전 또는 스케일에 영향을 받지 않습니다. 전반적인 배경 조명으로 사용하거나 오브젝트에 조명이 적용되지 않은 것처럼 보이게 할 수 있습니다.

에디터에서 환경광 컴포넌트는 중앙을 향하도록 회전된 화살표 아이콘으로 표시됩니다. 아이콘의 색상은 `color` 프로퍼티와 같습니다.

![낮은 강도의 환경광](images/light/ambient_light_less_intensity.png)

프로퍼티:

`color`
: 환경광의 RGB 색상입니다.

`intensity`
: 환경광 색상에 곱해지는 값입니다.

![높은 강도의 환경광](images/light/ambient_light_full_intensity.png)

환경광은 쉐이더 라이트 버퍼의 단일 환경광 색상 `light_info.xyz`에 누적됩니다. `lights[]` 배열의 항목을 차지하지 않습니다. 씬에 환경광 컴포넌트가 여러 개 있어도 모든 환경광이 혼합된 하나의 출력 색상만 생성됩니다.

### 방향광

방향광은 햇빛처럼 한 방향에서 오는 빛을 나타냅니다. 게임 오브젝트의 위치나 스케일은 사용하지 않으며, 라이트 방향은 로컬 전방 방향 `(0, 0, -1)`에 게임 오브젝트의 월드 회전을 적용하여 구합니다.

에디터에서 방향광 컴포넌트는 방향을 나타내는 3D 화살표가 달린 색상 있는 태양 아이콘으로 표시됩니다.

![방향광](images/light/directional_light.png)

프로퍼티:

`color`
: 방향광의 RGB 색상입니다.

`intensity`
: 방향광 색상에 곱해지는 값입니다.


방향광이 비추는 반대쪽 표면이 완전히 어두워지지 않도록 방향광과 환경광을 함께 사용하는 경우가 많습니다.

![방향광과 환경광](images/light/directional_and_ambient_light.png)

### 점광원

점광원은 게임 오브젝트의 월드 위치에서 바깥쪽으로 빛을 방출합니다. 점광원의 위치는 게임 오브젝트의 월드 위치에서 가져옵니다.

에디터에서 점광원 컴포넌트는 주변으로 광선이 뻗어 나가는 점과 `range`를 나타내는 원으로 표시되며, 점의 색상은 `color` 프로퍼티를 나타냅니다.

![점광원](images/light/point_light.png)

프로퍼티:

`color`
: 점광원의 RGB 색상입니다.

`intensity`
: 점광원 색상에 곱해지는 값입니다.

`range`
: 월드 단위로 나타낸 라이트 반경입니다.

유효 범위는 게임 오브젝트 월드 스케일의 축별 절댓값 중 가장 작은 값만큼 곱해집니다.

![점광원 범위](images/light/point_light_range.png)

라이트 색상을 변경하면 점광원의 기여 색상이 바뀌며, 범위는 광원에서 빛이 얼마나 멀리 도달하는지를 제어합니다.

![녹색 점광원의 범위](images/light/point_ight_range_green_color.png)

### 스포트라이트

스포트라이트는 게임 오브젝트의 월드 위치에서 원뿔 형태로 빛을 방출합니다. 방향은 `(0, 0, -1)`에 게임 오브젝트의 월드 회전을 적용하여 구합니다.

에디터에서 스포트라이트 컴포넌트는 색상 있는 램프 아이콘과 외부 및 내부 원뿔을 보여주는 안내선으로 표시됩니다.

![스포트라이트](images/light/spot_light.png)

프로퍼티:

`color`
: 스포트라이트의 RGB 색상입니다.

`intensity`
: 스포트라이트 색상에 곱해지는 값입니다.

`range`
: 월드 단위로 나타낸 라이트 반경입니다.

`inner_cone_angle`
: 에디터에서 도 단위로 나타낸 내부 원뿔 각도입니다. 이 원뿔 안의 픽셀에는 스포트라이트의 기여가 완전히 적용됩니다.

`outer_cone_angle`
: 에디터에서 도 단위로 나타낸 외부 원뿔 각도입니다. 내부 원뿔과 외부 원뿔 사이에서 빛이 점차 약해집니다.

유효 범위는 게임 오브젝트 월드 스케일의 축별 절댓값 중 가장 작은 값만큼 곱해집니다. 원뿔 각도는 도 단위로 편집되며 컴파일된 라이트 리소스에서 라디안으로 변환됩니다.

![스포트라이트 기즈모](images/light/spot_light_gizmos.png)

## 유효성 검사

빌드 파이프라인은 라이트 리소스 데이터의 유효성을 검사하고 정규화합니다:

- `color`에는 숫자가 정확히 세 개 있어야 합니다.
- `intensity`는 `0` 이상으로 제한됩니다.
- 점광원과 스포트라이트의 `range`는 `0` 이상으로 제한됩니다.
- 스포트라이트의 원뿔 각도는 `0..180`도 범위로 제한됩니다.
- `inner_cone_angle`은 `outer_cone_angle`을 초과하지 않도록 제한됩니다.

## 프로젝트 제한

라이트 컴포넌트의 최대 개수는 `light.max_count` 프로젝트 설정으로 제어합니다. 기본값은 `64`입니다.

환경광은 쉐이더 `lights[]` 배열의 항목을 사용하지 않지만, 여전히 Light 컴포넌트이므로 `light.max_count`에 포함됩니다. 방향광, 점광원 및 스포트라이트는 활성화된 동안 `lights[]`의 항목을 사용합니다.

라이트 컴포넌트 수가 `light.max_count`를 초과하면 엔진에서 컴포넌트 버퍼가 가득 찼다는 오류를 보고합니다.

## 쉐이더의 라이트 버퍼

쉐이더에서 내장 레이아웃을 사용하는 `LightBuffer`라는 uniform 블록을 선언하면 활성 라이트에 액세스할 수 있습니다. 엔진은 이 블록을 감지하여 이를 사용하는 메터리얼과 컴퓨트 프로그램에 라이트 데이터를 자동으로 바인딩합니다.

![라이트 버퍼 쉐이더](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: 월드 위치, w: 사용하지 않음
    vec4 color;           // rgb: 색상, a: 사용하지 않음
    vec4 direction_range; // xyz: 정규화된 월드 방향, w: 범위
    vec4 params;          // x: 타입, y: 강도, z: 내부 원뿔, w: 외부 원뿔
};

uniform LightBuffer
{
    // xyz: 누적된 환경광 색상, w: 활성화된 비환경광 라이트 수
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

라이트 타입은 `lights[i].params.x`에 저장됩니다:

| 타입 | 값 |
|------|-------|
| 방향광 | `0` |
| 점광원 | `1` |
| 스포트라이트 | `2` |

쉐이더에 `light.max_count`보다 작은 `lights[]` 배열을 선언할 수 있지만 더 큰 배열은 선언할 수 없습니다. 라이트 루프는 항상 선언된 배열 크기로 범위를 제한합니다:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // 방향광
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // 점광원
        {
            result += light_color;
        }
        else if (type == 2) // 스포트라이트
        {
            result += light_color;
        }
    }

    return result;
}
```

위 예제는 버퍼에 액세스하는 패턴을 보여줍니다. 실제 점광원 또는 스포트라이트 쉐이더에서는 쉐이딩되는 지점에서 `lights[i].position.xyz`까지의 벡터도 계산하고, `lights[i].direction_range.w`를 사용해 거리에 따른 감쇠를 적용해야 합니다. 스포트라이트의 경우에는 `lights[i].params.z`와 `lights[i].params.w`를 라디안 단위의 원뿔 각도로 사용해야 합니다.

## 내장 조명 헬퍼

Defold는 `/builtins/materials/lighting.glsl`에 쉐이더 헬퍼를 포함합니다. `MAX_LIGHT_COUNT`를 정의하고 헬퍼에서 요구하는 varying을 제공한 다음 프래그먼트 쉐이더에서 헬퍼를 포함합니다:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

헬퍼는 `LIGHT_DIRECTIONAL`, `LIGHT_POINT`, `LIGHT_SPOT` 상수를 정의하고 `ambient_light()`를 제공하며, 버퍼의 라이트를 위한 Lambert 확산광 함수를 제공합니다.

## 함께 보기

- [쉐이더 매뉴얼](/manuals/shader)
- [메터리얼 매뉴얼](/manuals/material)
- [렌더 매뉴얼](/manuals/render)
