---
title: Defold 메터리얼 매뉴얼
brief: 이 매뉴얼은 메터리얼, 쉐이더 상수, 샘플러를 다루는 방법을 설명합니다.
---

# 메터리얼

메터리얼은 그래픽 컴포넌트(스프라이트, 타일맵, 폰트, GUI 노드, 모델 등)를 어떻게 렌더링할지 표현하는 데 사용됩니다.

메터리얼은 렌더링 파이프라인에서 렌더링할 오브젝트를 선택하는 데 사용되는 정보인 _tags_를 포함합니다. 또한 사용 가능한 그래픽 드라이버를 통해 컴파일되고 그래픽 하드웨어에 업로드되어, 컴포넌트가 매 프레임 렌더링될 때 실행되는 _쉐이더 프로그램_에 대한 참조도 포함합니다.

* 렌더 파이프라인에 대한 자세한 내용은 [Render 문서](/manuals/render)를 참고하세요.
* 쉐이더 프로그램에 대한 자세한 설명은 [쉐이더 문서](/manuals/shader)를 참고하세요.

## 메터리얼 만들기

메터리얼을 만들려면 *Assets* 브라우저에서 대상 폴더를 <kbd>right click</kbd>하고 <kbd>New... ▸ Material</kbd>을 선택합니다. 메뉴에서 <kbd>File ▸ New...</kbd>를 선택한 다음 <kbd>Material</kbd>을 선택할 수도 있습니다. 새 메터리얼 파일의 이름을 지정하고 <kbd>Ok</kbd>를 누릅니다.

![Material file](images/materials/material_file.png)

새 메터리얼이 *Material Editor*에서 열립니다.

![Material editor](images/materials/material.png)

메터리얼 파일에는 다음 정보가 포함됩니다.

Name
: 메터리얼의 식별자입니다. 이 이름은 메터리얼을 빌드에 포함하기 위해 *Render* 리소스에 나열할 때 사용됩니다. 또한 render API 함수 `render.enable_material()`에서도 사용됩니다. 이름은 고유해야 합니다.

Vertex Program
: 이 메터리얼로 렌더링할 때 사용할 버텍스 쉐이더 프로그램 파일(*`.vp`*)입니다. 버텍스 쉐이더 프로그램은 컴포넌트의 각 primitive 버텍스마다 GPU에서 실행됩니다. 각 버텍스의 화면 위치를 계산하고, 선택적으로 프래그먼트 프로그램에 입력되도록 보간되는 "varying" 변수를 출력합니다.

Fragment Program
: 이 메터리얼로 렌더링할 때 사용할 프래그먼트 쉐이더 프로그램 파일(*`.fp`*)입니다. 이 프로그램은 primitive의 각 프래그먼트(픽셀)마다 GPU에서 실행되며, 각 프래그먼트의 색상을 결정하는 것이 목적입니다. 보통 입력 변수(varying 변수 또는 상수)를 기반으로 텍스쳐 조회와 계산을 수행합니다.

Vertex Constants
: 버텍스 쉐이더 프로그램에 전달될 uniform입니다. 사용할 수 있는 상수 목록은 아래를 참고하세요.

Fragment Constants
: 프래그먼트 쉐이더 프로그램에 전달될 uniform입니다. 사용할 수 있는 상수 목록은 아래를 참고하세요.

Samplers
: 메터리얼 파일에서 특정 샘플러를 선택적으로 설정할 수 있습니다. 샘플러를 추가하고, 쉐이더 프로그램에서 사용하는 이름과 같게 이름을 지정한 다음, 원하는 wrap 및 filter 설정을 지정합니다.

Tags
: 메터리얼과 연결된 태그입니다. 태그는 엔진에서 _bitmask_로 표현되며, 함께 그려야 하는 컴포넌트를 수집하기 위해 [`render.predicate()`](/ref/render#render.predicate)에서 사용됩니다. 이 방법은 [Render 문서](/manuals/render)를 참고하세요. 한 프로젝트에서 사용할 수 있는 태그의 최대 개수는 32개입니다.

## Attribute {#attributes}

쉐이더 attribute(버텍스 스트림 또는 버텍스 attribute라고도 함)는 GPU가 지오메트리를 렌더링하기 위해 메모리에서 버텍스를 가져오는 방식을 위한 메커니즘입니다. 버텍스 쉐이더는 `attribute` 키워드를 사용해 스트림 집합을 지정하며, 대부분의 경우 Defold는 스트림 이름을 기반으로 내부에서 데이터를 자동으로 만들고 바인딩합니다. 하지만 엔진이 만들지 않는 특정 효과를 구현하기 위해 버텍스마다 더 많은 데이터를 전달하고 싶을 때도 있습니다. 버텍스 attribute는 다음 필드로 설정할 수 있습니다.

Name
: attribute 이름입니다. 쉐이더 상수와 마찬가지로 attribute 설정은 버텍스 프로그램에 지정된 attribute와 일치할 때만 사용됩니다.

Semantic type
: semantic type은 attribute가 *무엇*인지, 그리고/또는 에디터에서 *어떻게* 표시되어야 하는지의 의미를 나타냅니다. 예를 들어 attribute에 `SEMANTIC_TYPE_COLOR`를 지정하면 에디터에는 color picker가 표시되지만, 데이터는 엔진에서 쉐이더로 그대로 전달됩니다.

  - `SEMANTIC_TYPE_NONE` 기본 semantic type입니다. attribute의 메터리얼 데이터를 버텍스 버퍼로 직접 전달하는 것 외에는 attribute에 다른 영향을 주지 않습니다(기본값).
  - `SEMANTIC_TYPE_POSITION` attribute에 대해 버텍스별 위치 데이터를 생성합니다. 좌표 공간과 함께 사용해 위치가 계산되는 방식을 엔진에 알려줄 수 있습니다.
  - `SEMANTIC_TYPE_TEXCOORD` attribute에 대해 버텍스별 텍스쳐 좌표를 생성합니다.
  - `SEMANTIC_TYPE_PAGE_INDEX` attribute에 대해 버텍스별 page index를 생성합니다.
  - `SEMANTIC_TYPE_COLOR` 에디터가 attribute를 해석하는 방식에 영향을 줍니다. attribute가 color semantic으로 설정되면 inspector에 color picker 위젯이 표시됩니다.
  - `SEMANTIC_TYPE_NORMAL` attribute에 대해 버텍스별 normal 데이터를 생성합니다.
  - `SEMANTIC_TYPE_TANGENT` attribute에 대해 버텍스별 tangent 데이터를 생성합니다.
  - `SEMANTIC_TYPE_WORLD_MATRIX` attribute에 대해 버텍스별 world matrix 데이터를 생성합니다.
  - `SEMANTIC_TYPE_NORMAL_MATRIX` attribute에 대해 버텍스별 normal matrix 데이터를 생성합니다.
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` attribute에 대해 버텍스별 3x3 텍스쳐 transform matrix를 생성합니다. 파티클 컴포넌트의 경우 엔진은 컴포넌트의 image 프로퍼티에 대해 좌표를 아틀라스 공간으로 변환하는 matrix를 제공합니다. 스프라이트 컴포넌트의 경우 엔진은 컴포넌트가 사용하는 각 이미지에 대한 matrix를 제공합니다(멀티 텍스쳐링 사용 시). 모델 컴포넌트에는 identity matrix가 제공됩니다.

Data type
: attribute의 backing data에 대한 데이터 타입입니다.

  - `TYPE_BYTE` 부호 있는 8비트 byte 값
  - `TYPE_UNSIGNED_BYTE` 부호 없는 8비트 byte 값
  - `TYPE_SHORT` 부호 있는 16비트 short 값
  - `TYPE_UNSIGNED_SHORT` 부호 없는 16비트 short 값
  - `TYPE_INT` 부호 있는 integer 값
  - `TYPE_UNSIGNED_INT` 부호 없는 integer 값
  - `TYPE_FLOAT` floating point 값(기본값)

Normalize
: true이면 GPU 드라이버가 attribute 값을 정규화합니다. 전체 정밀도가 필요하지는 않지만 구체적인 한계를 몰라도 어떤 계산을 하고 싶을 때 유용할 수 있습니다. 예를 들어 color vector는 일반적으로 0..255의 byte 값만 필요하지만, 쉐이더에서는 여전히 0..1 값처럼 처리됩니다.

Coordinate space
: 일부 semantic type은 여러 좌표 공간으로 데이터를 제공하는 것을 지원합니다. 스프라이트로 빌보딩 효과를 구현하려면 일반적으로 로컬 공간의 position attribute와, 가장 효과적인 배칭을 위한 월드 공간의 완전히 변환된 위치가 필요합니다.

Vector type
: attribute의 vector type입니다.

  - `VECTOR_TYPE_SCALAR` 단일 scalar 값
  - `VECTOR_TYPE_VEC2` 2D vector
  - `VECTOR_TYPE_VEC3` 3D vector
  - `VECTOR_TYPE_VEC4` 4D vector(기본값)
  - `VECTOR_TYPE_MAT2` 2D matrix
  - `VECTOR_TYPE_MAT3` 3D matrix
  - `VECTOR_TYPE_MAT4` 4D matrix

Step function
: attribute 데이터를 vertex function에 어떻게 제공할지 지정합니다. 이 항목은 인스턴싱에만 관련됩니다.

  - `Vertex` 버텍스마다 한 번입니다. 예를 들어 position attribute는 일반적으로 mesh의 버텍스마다 vertex function에 제공됩니다(기본값).
  - `Instance` 인스턴스마다 한 번입니다. 예를 들어 world matrix attribute는 일반적으로 인스턴스마다 한 번 vertex function에 제공됩니다.

Value
: attribute의 값입니다. attribute 값은 컴포넌트별로 오버라이드할 수 있지만, 그렇지 않으면 버텍스 attribute의 기본값으로 동작합니다. 참고: *default* attribute(position, texture coordinates, page indices)의 경우 값은 무시됩니다.

::: sidenote
커스텀 attribute는 스트림을 더 작은 데이터 타입이나 다른 element count를 사용하도록 재설정하여 CPU와 GPU 양쪽의 메모리 사용량을 줄이는 데에도 사용할 수 있습니다.
:::

### 기본 attribute semantic

메터리얼 시스템은 런타임에 특정 이름 집합에 대해 attribute 이름을 기반으로 기본 semantic type을 자동으로 할당합니다.

  - `position` - semantic type: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - semantic type: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - semantic type: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - semantic type: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - semantic type: `SEMANTIC_TYPE_COLOR`
  - `normal` - semantic type: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - semantic type: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - semantic type: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - semantic type: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - semantic type: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

메터리얼에 이 attribute들에 대한 항목이 있으면, 기본 semantic type은 Material Editor에서 설정한 값으로 오버라이드됩니다.

### 커스텀 버텍스 attribute 데이터 설정

사용자 정의 쉐이더 상수와 마찬가지로, `go.get`, `go.set`, `go.animate`를 호출해 런타임에 버텍스 attribute도 업데이트할 수 있습니다.

![Custom material attribute](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

다만 버텍스 attribute를 업데이트할 때는 몇 가지 주의할 점이 있습니다. 컴포넌트가 해당 값을 사용할 수 있는지는 attribute의 semantic type에 따라 달라집니다. 예를 들어 스프라이트 컴포넌트는 `SEMANTIC_TYPE_POSITION`을 지원하므로, 이 semantic type을 가진 attribute를 업데이트하면 컴포넌트는 오버라이드된 값을 무시합니다. semantic type이 해당 데이터는 항상 스프라이트 위치에서 생성되어야 한다고 지정하기 때문입니다.

버텍스 attribute가 scalar이거나 `Vec4`가 아닌 vector type인 경우에도 `go.set`을 사용해 데이터를 설정할 수 있습니다.

```lua
-- vec4의 마지막 두 컴포넌트는 사용되지 않습니다!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

matrix attribute도 마찬가지입니다. attribute가 `Mat4`가 아닌 matrix type인 경우에도 `go.set`을 사용해 데이터를 설정할 수 있습니다.

### 커스텀 버텍스 attribute 사용 예

텍스쳐 transform attribute를 사용해 UV 좌표를 아틀라스 공간으로 변환하는 예입니다.

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // transform에서 position 추출
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // transform에서 scale 추출
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // 로컬 UV(0..1)로 변환
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // 또는 UV 좌표가 이미 0..1 범위에 있다면,
  // transform을 곱해 바로 아틀라스 공간으로 변환할 수 있습니다.
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // 값을 프래그먼트 쉐이더로 전달
  var_texcoord0 = localUV;

  // ... 버텍스 쉐이더의 나머지 부분
}
```

### 인스턴싱

인스턴싱은 씬에서 같은 오브젝트의 여러 복사본을 효율적으로 그리는 데 사용하는 기법입니다. 오브젝트가 사용될 때마다 별도의 복사본을 만드는 대신, 인스턴싱을 사용하면 그래픽 엔진이 단일 오브젝트를 만들고 여러 번 재사용할 수 있습니다. 예를 들어 큰 숲이 있는 게임에서 나무마다 별도의 나무 모델을 만드는 대신, 인스턴싱을 사용하면 하나의 나무 모델을 만든 뒤 서로 다른 위치와 스케일로 수백 또는 수천 번 배치할 수 있습니다. 그러면 각 나무에 대해 개별 draw call을 사용하는 대신 숲을 하나의 draw call로 렌더링할 수 있습니다.

::: sidenote
인스턴싱은 현재 Model 컴포넌트에서만 사용할 수 있습니다.
:::

인스턴싱은 가능할 때 자동으로 활성화됩니다. Defold는 draw state를 가능한 한 많이 배칭하는 데 크게 의존하므로, 인스턴싱이 동작하려면 몇 가지 요구 사항을 충족해야 합니다.

- 모든 인스턴스에 같은 메터리얼을 사용해야 합니다. 커스텀 메터리얼이 `render.enable_material`로 설정되어 있어도 인스턴싱은 계속 동작합니다.
- 메터리얼은 'local' vertex space를 사용하도록 설정되어야 합니다.
- 메터리얼에는 인스턴스마다 반복되는 버텍스 attribute가 하나 이상 있어야 합니다.
- 상수 값은 모든 인스턴스에서 같아야 합니다. 대신 상수 값을 커스텀 버텍스 attribute나 다른 backing method(예: 텍스쳐)에 넣을 수 있습니다.
- 텍스쳐나 storage buffer 같은 쉐이더 리소스는 모든 인스턴스에서 같아야 합니다.

버텍스 attribute가 인스턴스마다 반복되도록 설정하려면 `Step function`을 `Instance`로 설정해야 합니다. 특정 semantic type의 경우 이름을 기반으로 이 작업이 자동으로 수행되지만(위의 `Default attribute semantics` 표 참고), Material Editor에서 `Step function`을 `Instance`로 설정해 수동으로 지정할 수도 있습니다.

간단한 예로, 다음 씬에는 각각 모델 컴포넌트가 있는 네 개의 게임 오브젝트가 있습니다.

![Instancing setup](images/materials/instancing-setup.png)

메터리얼은 다음과 같이 설정되어 있으며, 인스턴스마다 반복되는 단일 커스텀 버텍스 attribute가 있습니다.

![Instancing material](images/materials/instancing-material.png)

버텍스 쉐이더에는 여러 인스턴스별 attribute가 지정되어 있습니다.

```glsl
// 버텍스별 attributes
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// 인스턴스별 attributes
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

`mtx_world`와 `mtx_normal`은 기본적으로 step function `Instance`를 사용하도록 설정됩니다. Material Editor에서 이 항목들을 추가하고 `Step function`을 `Vertex`로 설정하면 변경할 수 있으며, 이렇게 하면 attribute가 인스턴스마다가 아니라 버텍스마다 반복됩니다.

이 경우 인스턴싱이 동작하는지 확인하려면 web profiler를 보면 됩니다. 이 경우 box의 인스턴스 사이에서 달라지는 것이 인스턴스별 attribute뿐이므로, 하나의 draw call로 렌더링할 수 있습니다.

![Instancing draw calls](images/materials/instancing-draw-calls.png)

#### 하위 호환성

OpenGL 기반 그래픽 어댑터에서 인스턴싱은 데스크탑의 경우 OpenGL 3.1 이상, 모바일의 경우 OpenGL ES 3.0 이상이 필요합니다. 즉 OpenGL ES2 또는 더 오래된 OpenGL 버전을 사용하는 매우 오래된 장치는 인스턴싱을 지원하지 않을 수 있습니다. 이 경우 개발자가 특별히 신경 쓰지 않아도 기본적으로 렌더링은 계속 동작하지만, 실제 인스턴싱을 사용할 때만큼 성능이 좋지 않을 수 있습니다. 현재는 인스턴싱 지원 여부를 감지할 방법이 없지만, 앞으로는 이 기능이 추가되어 더 저렴한 메터리얼을 사용하거나, 일반적으로 인스턴싱에 적합한 후보인 foliage 또는 clutter 같은 것을 완전히 건너뛸 수 있게 될 예정입니다.

## 버텍스와 프래그먼트 상수 {#vertex-and-fragment-constants}

쉐이더 상수, 또는 "uniform"은 엔진에서 버텍스 및 프래그먼트 쉐이더 프로그램으로 전달되는 값입니다. 상수를 사용하려면 메터리얼 파일에서 *Vertex Constant* 프로퍼티 또는 *Fragment Constant* 프로퍼티로 정의합니다. 대응하는 `uniform` 변수는 쉐이더 프로그램에 정의되어 있어야 합니다. 메터리얼에는 다음 상수를 설정할 수 있습니다.

`CONSTANT_TYPE_WORLD`
: 월드 matrix입니다. 버텍스를 월드 공간으로 변환하는 데 사용합니다. 일부 컴포넌트 타입에서는 버텍스가 버텍스 프로그램에 도착할 때 이미 월드 공간에 있습니다(배칭 때문). 이 경우 쉐이더에서 월드 matrix를 곱하면 잘못된 결과가 나옵니다.

`CONSTANT_TYPE_VIEW`
: 뷰 matrix입니다. 버텍스를 뷰(카메라) 공간으로 변환하는 데 사용합니다.

`CONSTANT_TYPE_PROJECTION`
: 프로젝션 matrix입니다. 버텍스를 화면 공간으로 변환하는 데 사용합니다.

`CONSTANT_TYPE_VIEWPROJ`
: 뷰 matrix와 프로젝션 matrix가 이미 곱해진 matrix입니다.

`CONSTANT_TYPE_WORLDVIEW`
: 월드 matrix와 뷰 matrix가 이미 곱해진 matrix입니다.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: 월드, 뷰, 프로젝션 matrix가 이미 곱해진 matrix입니다.

`CONSTANT_TYPE_NORMAL`
: normal 방향을 계산하는 matrix입니다. 월드 transform에는 비균일 스케일링이 포함될 수 있으며, 이는 결합된 world-view transform의 직교성을 깨뜨립니다. normal matrix는 normal을 변환할 때 방향 문제를 피하기 위해 사용됩니다. normal matrix는 world-view matrix의 전치 역행렬입니다.

`CONSTANT_TYPE_USER`
: 쉐이더 프로그램으로 전달하려는 커스텀 데이터에 사용할 수 있는 vector4 상수입니다. 상수 정의에서 상수의 초기값을 설정할 수 있지만, [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 함수로 변경할 수 있습니다. [go.get()](/ref/stable/go/#go.get)으로 값을 가져올 수도 있습니다. 단일 컴포넌트 인스턴스의 메터리얼 상수를 변경하면 [렌더 배칭이 깨지고 추가 draw call이 발생합니다](/manuals/render/#draw-calls-and-batching).

예:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: 쉐이더 프로그램으로 전달하려는 커스텀 데이터에 사용할 수 있는 matrix4 상수입니다. 상수 정의에서 상수의 초기값을 설정할 수 있지만, [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 함수로 변경할 수 있습니다. [go.get()](/ref/stable/go/#go.get)으로 값을 가져올 수도 있습니다. 단일 컴포넌트 인스턴스의 메터리얼 상수를 변경하면 [렌더 배칭이 깨지고 추가 draw call이 발생합니다](/manuals/render/#draw-calls-and-batching).

예:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

::: sidenote
`CONSTANT_TYPE_USER` 또는 `CONSTANT_TYPE_MATRIX4` 타입의 메터리얼 상수를 `go.get()`과 `go.set()`으로 사용할 수 있으려면 쉐이더 프로그램에서 사용되어야 합니다. 상수가 메터리얼에는 정의되어 있지만 프로그램에서 사용되지 않으면 메터리얼에서 제거되며 런타임에 사용할 수 없습니다.
:::

## 샘플러

샘플러는 텍스쳐(타일 소스 또는 아틀라스)에서 색상 정보를 샘플링하는 데 사용됩니다. 이 색상 정보는 쉐이더 프로그램의 계산에 사용할 수 있습니다.

스프라이트, 타일맵, GUI, 파티클 효과 컴포넌트에는 `sampler2D`가 자동으로 설정됩니다. 쉐이더 프로그램에서 처음 선언된 `sampler2D`는 그래픽 컴포넌트가 참조하는 이미지에 자동으로 바인딩됩니다. 따라서 현재 이러한 컴포넌트의 경우 메터리얼 파일에서 샘플러를 지정할 필요가 없습니다. 또한 이 컴포넌트 타입들은 현재 단일 텍스쳐만 지원합니다. 쉐이더에서 여러 텍스쳐가 필요하다면 [`render.enable_texture()`](/ref/render/#render.enable_texture)를 사용하고 렌더 스크립트에서 텍스쳐 샘플러를 수동으로 설정할 수 있습니다.

![Sprite sampler](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

메터리얼 파일에서 이름으로 샘플러를 추가해 컴포넌트의 샘플러 설정을 지정할 수 있습니다. 메터리얼 파일에서 샘플러를 설정하지 않으면 전역 *graphics* 프로젝트 설정이 사용됩니다.

![Sampler settings](images/materials/my_sampler.png)

모델 컴포넌트의 경우 메터리얼 파일에 원하는 설정으로 샘플러를 지정해야 합니다. 그러면 에디터에서 해당 메터리얼을 사용하는 모든 모델 컴포넌트에 텍스쳐를 설정할 수 있습니다.

![Model samplers](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Model](images/materials/model.png)

## 샘플러 설정

Name
: 샘플러의 이름입니다. 이 이름은 프래그먼트 쉐이더에 선언된 `sampler2D`와 일치해야 합니다.

Wrap U/W
: U와 V 축의 wrap mode입니다.

  - `WRAP_MODE_REPEAT`는 [0,1] 범위 밖의 텍스쳐 데이터를 반복합니다.
  - `WRAP_MODE_MIRRORED_REPEAT`는 [0,1] 범위 밖의 텍스쳐 데이터를 반복하지만, 두 번째 반복마다 미러링됩니다.
  - `WRAP_MODE_CLAMP_TO_EDGE`는 1.0보다 큰 값의 텍스쳐 데이터를 1.0으로 설정하고, 0.0보다 작은 값은 0.0으로 설정합니다. 즉 edge pixel이 가장자리까지 반복됩니다.

Filter Min/Mag
: 확대와 축소에 사용할 필터링입니다. Nearest filtering은 linear interpolation보다 계산량이 적지만 aliasing artifact가 생길 수 있습니다. Linear interpolation은 대개 더 부드러운 결과를 제공합니다.

  - `Default`는 `game.project` 파일의 `Graphics` 아래에 `Default Texture Min Filter`와 `Default Texture Mag Filter`로 지정된 기본 필터 옵션을 사용합니다.
  - `FILTER_MODE_NEAREST`는 픽셀 중심에 가장 가까운 좌표의 texel을 사용합니다.
  - `FILTER_MODE_LINEAR`는 픽셀 중심에 가장 가까운 texel 2x2 배열의 가중 linear average를 설정합니다.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST`는 개별 mipmap 내에서 가장 가까운 texel 값을 선택합니다.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR`는 가장 적합한 두 개의 가까운 mipmap에서 가장 가까운 texel을 선택한 뒤, 두 값 사이를 선형으로 보간합니다.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST`는 개별 mipmap 내에서 선형으로 보간합니다.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR`는 linear interpolation을 사용해 두 map 각각의 값을 계산한 뒤, 두 값 사이를 선형으로 보간합니다.

Max Anisotropy
: 비등방성 필터링은 여러 샘플을 가져와 결과를 함께 블렌딩하는 고급 필터링 기법입니다. 이 설정은 텍스쳐 샘플러의 anisotropy 레벨을 제어합니다. GPU가 비등방성 필터링을 지원하지 않으면 이 파라미터는 아무 효과가 없으며 기본값인 1로 설정됩니다.

## 상수 버퍼

렌더링 파이프라인이 그릴 때는 기본 시스템 상수 버퍼에서 상수 값을 가져옵니다. 커스텀 상수 버퍼를 만들어 기본 상수를 오버라이드하고, 대신 렌더 스크립트에서 쉐이더 프로그램 uniform을 프로그래밍 방식으로 설정할 수 있습니다.

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. 새 상수 버퍼를 만듭니다.
2. `tint` 상수를 밝은 빨강색으로 설정합니다.
3. 커스텀 상수를 사용해 predicate를 그립니다.

버퍼의 상수 요소는 일반 Lua 테이블처럼 참조되지만, `pairs()` 또는 `ipairs()`로 버퍼를 반복할 수는 없습니다.
