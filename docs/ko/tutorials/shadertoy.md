---
brief: 이 튜토리얼에서는 shadertoy.com의 쉐이더를 Defold로 변환합니다.
layout: tutorial
locale: ko
title: Shadertoy에서 Defold로 변환하는 튜토리얼
---

# Shadertoy 튜토리얼

[Shadertoy.com](https://www.shadertoy.com/)은 사용자가 기여한 GL 쉐이더를 모아 둔 사이트입니다. 쉐이더 코드와 영감을 찾기에 좋은 리소스입니다. 이 튜토리얼에서는 Shadertoy의 쉐이더를 가져와 Defold에서 실행되도록 만들어 보겠습니다. 쉐이더에 대한 기본적인 이해가 있다고 가정합니다. 더 읽어 봐야 한다면 [쉐이더 매뉴얼](/manuals/shader/)에서 시작하는 것이 좋습니다.

이 튜토리얼에서 사용할 쉐이더는 Pablo Andrioli(Shadertoy 사용자명 "Kali")의 [Star Nest](https://www.shadertoy.com/view/XlfGRj)입니다. 이 쉐이더는 아주 멋진 별밭 효과를 렌더링하는 순수한 절차적 수학 블랙 매직 프래그먼트 쉐이더입니다.

![Star Nest](../images/shadertoy/starnest.png)

이 쉐이더는 꽤 복잡한 GLSL 코드 65줄뿐이지만 걱정하지 않아도 됩니다. 몇 가지 간단한 입력을 바탕으로 자기 일을 하는 블랙박스로 다룰 것입니다. 여기서 할 일은 Shadertoy 대신 Defold와 연동되도록 쉐이더를 수정하는 것입니다.

## 텍스쳐를 입힐 대상

Star Nest 쉐이더는 순수한 프래그먼트 쉐이더이므로, 쉐이더가 텍스쳐를 입힐 대상만 있으면 됩니다. 스프라이트, 타일 맵, GUI, 모델 등 여러 선택지가 있습니다. 이 튜토리얼에서는 간단한 3D 모델을 사용합니다. 그 이유는 모델 렌더링을 풀 스크린 효과로 쉽게 만들 수 있기 때문입니다. 예를 들어 시각적 포스트 프로세싱을 하려면 이런 방식이 필요합니다.

빈 프로젝트에서 시작할 수 있습니다.

1. Defold를 열고 Create From *Templates*를 선택합니다.
2. *Empty Project*를 선택합니다.
3. 디스크에서 *Title*과 *Location*을 설정합니다.
4. <kbd>Create New Project</kbd>를 클릭합니다.

![시작](../images/shadertoy/empty_project.png)

`builtins/assets/meshes`의 내장 `quad.gltf` 메쉬를 사용할 수 있습니다.

선택 사항으로 Blender나 다른 3D 모델링 프로그램에서 정사각형 평면 메쉬를 만들 수도 있습니다. 편의를 위해 4개의 버텍스 좌표는 X축에서 -1과 1, Y축에서 -1과 1에 둡니다. Blender는 기본적으로 Z축이 위를 향하므로 메쉬를 X축 기준으로 90° 회전해야 합니다. 또한 메쉬에 올바른 UV 좌표가 생성되었는지도 확인해야 합니다. Blender에서 메쉬를 선택한 상태로 *Edit Mode*에 들어간 다음 <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>을 선택합니다.

<div class='sidenote' markdown='1'>
Blender는 [blender.org](https://www.blender.org)에서 다운로드할 수 있는 무료 오픈소스 3D 소프트웨어입니다.
</div>

![Blender의 quad](../images/shadertoy/quad_blender.png)

1. Defold에서 "main.collection" 파일을 열고 새 게임 오브젝트 "star-nest"를 생성합니다.
2. "star-nest" 게임 오브젝트에 *Model* 컴포넌트를 추가합니다.
3. *Mesh* 프로퍼티를 `quad.gltf`로 설정합니다.
4. 모델의 메터리얼을 설정해야 하므로, 지금은 내장 `model.material`을 선택합니다.

모델은 씬 에디터에 나타나야 하지만 모두 검은색으로 렌더링됩니다. 아직 텍스쳐가 설정되지 않았기 때문입니다.

![Defold의 quad](../images/shadertoy/quad_default_material.png)

## 메터리얼 생성

1. `Assets` pane의 `main` 폴더에서 <kbd>Right Mouse Button</kbd>을 클릭하고 <kbd>New</kbd>-><kbd>Material</kbd>을 선택한 뒤 이름을 `star-nest`로 지정하여 새 메터리얼 파일 *`star-nest.material`*을 생성합니다.

 ![메터리얼](../images/shadertoy/new_material.png)

2. 같은 방식으로 버텍스 쉐이더 프로그램 `star-nest.vp`와 프래그먼트 쉐이더 프로그램 `star-nest.fp`를 생성합니다.
3. *star-nest.material*을 엽니다.
4. *Vertex Program*을 `star-nest.vp`로 설정합니다.
5. *Fragment Program*을 `star-nest.fp`로 설정합니다.
6. *Vertex Constant*를 추가하고 이름을 "`view_proj`", 타입을 `Viewproj`("view projection")로 지정합니다.
8. *Tags*에 "tile" 태그를 추가합니다. 이렇게 하면 스프라이트와 타일이 그려질 때 quad가 렌더 패스에 포함됩니다.

 ![메터리얼](../images/shadertoy/material.png)

### 버텍스 프로그램

1. 버텍스 쉐이더 프로그램 파일 `star-nest.vp`를 엽니다. 파일에는 다음 코드가 들어 있어야 합니다.

    ```glsl
    #version 140

    // 위치는 월드 공간 기준입니다
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### 프래그먼트 프로그램

1. 프래그먼트 쉐이더 프로그램 파일 `star-nest.fp`를 열고, 프래그먼트 색상이 UV 좌표(`var_texcoord0`)의 X와 Y 좌표를 기반으로 설정되도록 코드를 수정합니다. 이렇게 하면 모델이 올바르게 설정되었는지 확인할 수 있습니다.

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. `main.collection`의 `star-nest` 게임 오브젝트에 있는 모델 컴포넌트에서 `Material` 프로퍼티를 새로 생성한 `star-nest` 메터리얼로 설정합니다.

이제 에디터는 새 쉐이더로 모델을 렌더링해야 하며, UV 좌표가 올바른지 명확하게 확인할 수 있습니다. 왼쪽 아래 모서리는 검은색(0, 0, 0), 왼쪽 위 모서리는 초록색(0, 1, 0), 오른쪽 위 모서리는 노란색(1, 1, 0), 오른쪽 아래 모서리는 빨간색(1, 0, 0)이어야 합니다.

![Defold의 quad](../images/shadertoy/quad_material.png)

## 카메라

이제 프로젝트를 실행할 수 있습니다(<kbd>Project</kbd>-><kbd>Build</kbd> 또는 단축키 <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>). 하지만 검은 화면이 보일 것입니다. 정확히는 왼쪽 아래 모서리에 아주 작은 픽셀 하나 정도만 보일 수도 있습니다. 카메라가 없고, 기본 렌더 스크립트는 거대한 2D 공간을 보여 주는 단순한 대체 방식을 사용하기 때문입니다. 반면 우리 모델은 위치가 (0,0,0)이고 너비가 1뿐입니다.

게임에서 볼 영역을 정의하기 위해 카메라 컴포넌트가 있는 게임 오브젝트를 추가해 보겠습니다.

1. 포지션이 (0,0,1)인 `camera`라는 게임 오브젝트를 추가합니다. (기본 2D 설정에서 현재 Z축은 사용자를 향하므로, 이 게임 오브젝트가 모델 앞에 오도록 Z 좌표를 1로 설정하는 것이 중요합니다.)
2. `Camera` 컴포넌트를 추가하면 quad가 들어 있는 카메라 미리보기가 표시됩니다. 기본 프로퍼티만으로도 이 설정에서는 운 좋게 이미 올바른 결과를 볼 수 있으므로, 한 가지만 제외하면 바꿀 필요가 없습니다. 이렇게 큰 카메라 뷰 절두체(frustum)는 필요하지 않으므로 `Far Z`를 `2`로 줄일 수 있습니다.

![카메라](../images/shadertoy/camera.png)

선택 사항으로 `Orthographic Projection`을 `true`로 설정하여 카메라 타입을 바꾸고, `Orthographic Zoom`도 600 정도로 조정할 수 있습니다. 하지만 이 경우 자동 종횡비(aspect ratio)가 적용되지 않으므로 모델이 화면을 채우지 않습니다.

## Star Nest 쉐이더

이제 모든 준비가 끝났으니 실제 쉐이더 코드 작업을 시작해 보겠습니다. 먼저 원본 코드를 살펴보겠습니다. 원본은 몇 개의 섹션으로 구성되어 있습니다.

![Star Nest 쉐이더 코드](../images/shadertoy/starnest_code.png)

GLSL 버전 140의 최신 파이프라인을 사용할 것입니다. 이를 위해 파일 맨 위에 `#version 140`으로 버전을 선언합니다.

1. 5--18행은 여러 상수를 정의합니다. 이 부분은 그대로 둘 수 있습니다. 단순한 GLSL 상수이며 Shadertoy나 Defold에 특별히 의존하지 않습니다.

2. 21행과 63행에는 입력 프래그먼트 X/Y 화면 공간 텍스쳐 좌표(`in vec2 fragCoord`)와 출력 프래그먼트 색상(`out vec4 fragColor`)이 들어 있습니다.

    Defold는 버텍스 쉐이더에서 프래그먼트 쉐이더로 텍스쳐 좌표를 보간된 변수로 전달하며, 값은 UV 좌표(범위 0--1)입니다. 버텍스 쉐이더에서는 `out` qualifier로 다음과 같이 선언합니다.

    ```glsl
    // star-nest.vp에서
    out vec2 var_texcoord0;
    ```

     프래그먼트 쉐이더에서는 같은 값을 `in` qualifier로 받습니다.

    ```glsl
    // star-nest.fp에서
    in vec2 var_texcoord0;
    ```

    그런 다음 GLSL 140에서는 `out` qualifier로 명시적인 프래그먼트 출력을 선언합니다.

    ```glsl
    // star-nest.fp에서
    out vec4 out_fragColor;
    ```

    따라서 원본 Shadertoy 코드가 `fragColor`에 쓰는 위치에서 Defold 쉐이더는 `out_fragColor`에 씁니다.

3. 23--27행은 텍스쳐의 크기와 이동 방향, 스케일된 시간을 설정합니다. Shadertoy에서는 쉐이더가 `fragCoord`를 통해 픽셀 위치를 받고, 뷰포트/텍스쳐의 뷰포트 해상도는 `uniform vec3 iResolution`으로 쉐이더에 전달됩니다. 쉐이더는 프래그먼트 좌표와 해상도에서 올바른 종횡비를 가진 UV 스타일 좌표를 계산합니다. 더 나은 프레이밍을 위해 해상도 오프셋도 약간 적용합니다.

    Defold에서는 픽셀 좌표에서 시작하지 않습니다. 대신 버텍스 쉐이더에서 `var_texcoord0`을 통해 정규화된 UV 좌표를 이미 받습니다. 이 좌표는 렌더링된 quad 전체에서 `0.0`부터 `1.0` 범위입니다.

    Defold 버전에서는 `var_texcoord0`의 UV 좌표를 사용하도록 이 계산을 바꿔야 합니다.
    일반적인 변환은 다음과 같습니다.

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    정확한 `aspect` 값은 예제가 어떻게 설정되어 있는지에 따라 달라집니다. 효과가 알려진 디스플레이 크기의 풀 스크린 quad에 렌더링된다면 이 튜토리얼에서는 종횡비를 하드코딩할 수 있습니다. 효과가 임의의 창 크기를 지원해야 한다면 해상도를 프래그먼트 상수로 전달하고 GLSL 140 uniform block 안에 넣습니다.

    여기서는 시간도 설정합니다. 시간은 `uniform float iGlobalTime`으로 쉐이더에 전달됩니다. Defold(1.12.3부터)는 특수 `Time` 상수를 통해 쉐이더에 시간을 제공하며, 이 튜토리얼에서는 그것을 사용합니다.

    최신 Defold에서는 non-opaque uniform을 uniform block 안에 선언합니다.
    프래그먼트 쉐이더에서는 다음과 같이 선언합니다.

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    그런 다음 `star-nest.material`에서 이름이 `time`인 Fragment Constant를 추가하고 타입을 `Time`으로 설정합니다.

    이 값은 다음과 같이 사용할 수 있습니다.

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    여기서 `time.x`는 엔진 시작 이후의 시간이고, `time.y`는 이전 프레임으로부터의 delta time입니다.

4. 29--39행은 볼류메트릭 렌더링의 회전을 설정하며, 마우스 포지션이 회전에 영향을 줍니다. 마우스 좌표는 `uniform vec4 iMouse`로 쉐이더에 전달됩니다.

    이 튜토리얼에서는 마우스 입력을 건너뜁니다.

5. 41--62행은 쉐이더의 핵심입니다. 이 코드는 그대로 둘 수 있습니다.

## 수정된 Star Nest 쉐이더

위 섹션들을 살펴보고 필요한 변경을 적용하면 다음과 같은 쉐이더 코드가 됩니다. 읽기 쉽도록 약간 정리했습니다. Defold 버전과 Shadertoy 버전의 차이점이 표시되어 있습니다.

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// 이 컨텐츠는 MIT License에 따라 제공됩니다.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// 좌표와 방향을 얻습니다
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// 볼류메트릭 렌더링
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// 타일링 접기
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// 마법 공식
			p = abs(p) / dot(p, p) - formuparam;

			// 평균 변화량의 절댓값 합
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// 암흑 물질
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// 암흑 물질, 가까운 곳은 렌더링하지 않습니다
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// 거리에 따른 색상 지정
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// 색상 조정
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Defold의 최신 GLSL 파이프라인을 사용하기 위해 파일 맨 위에 `#version 140`을 선언합니다. 그런 다음 `#define` 선언들은 그대로 둡니다.
2. 버텍스 쉐이더는 `var_texcoord0`을 통해 UV 좌표를 프래그먼트 쉐이더로 전달합니다. GLSL 140에서 프래그먼트 쉐이더는 이 보간된 값을 `in` qualifier로 받습니다.
3. GLSL 140에서 프래그먼트 쉐이더는 `gl_FragColor`에 쓰는 대신 명시적인 출력 변수를 선언해야 합니다. 여기서는 `out vec4 out_fragColor`를 사용합니다.
4. Defold의 `Time` 메터리얼 상수는 uniform block을 통해 쉐이더에 노출됩니다. `star-nest.material`에서 이름이 `time`인 Fragment Constant를 추가하고 타입을 `Time`으로 설정합니다.
5. Shadertoy는 `mainImage(out vec4 fragColor, in vec2 fragCoord)`를 사용합니다. Defold에서는 일반적인 `void main()` 엔트리 포인트를 사용하고, `var_texcoord0`에서 보간된 UV 좌표를 읽은 뒤 최종 색상을 `out_fragColor`에 씁니다.
6. 이 튜토리얼에서는 렌더링에 사용할 정적 해상도/aspect 값을 정의합니다. 현재 모델은 정사각형이므로 `vec2 res = vec2(1.0, 1.0);`을 사용할 수 있습니다. 크기가 1280×720인 직사각형 모델이라면 대신 `vec2 res = vec2(1.78, 1.0);`을 사용하고 UV 좌표에 곱해 올바른 종횡비를 유지할 수 있습니다.
7. 원본 Shadertoy 쉐이더는 `iGlobalTime`을 사용합니다. 이 Defold 버전에서는 `time.x`에 엔진 시작 이후의 시간이 들어 있으므로 이를 로컬 `iGlobalTime` 변수에 할당하고 별밭을 통과하는 카메라 움직임을 애니메이션하는 데 사용합니다.
8. 이 튜토리얼을 단순하게 유지하기 위해 `iMouse` 값은 완전히 제거합니다. 회전 자체는 볼류메트릭 렌더링의 시각적 대칭을 줄여 주기 때문에 그대로 유지합니다.
9. 마지막으로 쉐이더는 결과 프래그먼트 색상을 `out_fragColor`에 씁니다.

프래그먼트 쉐이더 프로그램을 저장합니다. 이제 모델은 Scene editor와 런타임에서 별밭으로 멋지게 텍스쳐링되어야 합니다.

![starnest가 적용된 quad](../images/shadertoy/quad_starnest.png)


## 애니메이션 {#animation}

퍼즐의 마지막 조각은 별이 움직이도록 시간을 도입하는 것입니다. Defold(1.12.3부터)는 `Time` 타입의 프래그먼트 상수를 통해 이를 자동으로 제공합니다.

1. *star-nest.material*을 엽니다.
2. *Fragment Constant*를 추가하고 이름을 "time"으로 지정합니다.
3. *Type*을 `Time`으로 설정합니다.

![time 상수](../images/shadertoy/time_constant.png)

이제 끝입니다! 프래그먼트 쉐이더에서 이미 이 `time`을 처리하고 있습니다. 완료되었습니다!

## 연습

재미있는 이어서 해 볼 연습은 원본 마우스 이동 입력을 쉐이더에 추가하는 것입니다. 새 Fragment Constant를 만들어야 하며, 이번에는 타입을 `User`로 지정합니다. 그리고 마우스 이동을 감지하는 어떤 스크립트의 `on_input`에서 `go.set()` 함수를 사용해 새 상수에 입력 좌표를 설정하도록 업데이트해야 합니다.

즐거운 Defolding 되세요!
