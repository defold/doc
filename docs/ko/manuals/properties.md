---
title: Defold의 프로퍼티
brief: 이 매뉴얼은 Defold에 어떤 종류의 프로퍼티가 있는지, 그리고 이를 어떻게 사용하고 애니메이션하는지 설명합니다.
---

# 프로퍼티

Defold는 읽고, 설정하고, 애니메이션할 수 있는 게임 오브젝트, 컴포넌트, GUI 노드의 프로퍼티를 노출합니다. 다음과 같은 종류의 프로퍼티가 있습니다.

* 시스템이 정의한 게임 오브젝트 변형(transform: 위치, 회전, 스케일) 및 컴포넌트별 프로퍼티(예: 스프라이트의 픽셀 크기 또는 충돌 오브젝트의 질량)
* Lua 스크립트에 정의된 사용자 정의 스크립트 컴포넌트 프로퍼티(자세한 내용은 [스크립트 프로퍼티 문서](/manuals/script-properties) 참고)
* GUI 노드 프로퍼티
* 쉐이더와 메터리얼 파일에 정의된 쉐이더 상수(자세한 내용은 [메터리얼 문서](/manuals/material) 참고)

숫자형 프로퍼티의 입력 필드 위에 마우스를 올리면 드래그 핸들이 표시됩니다. 핸들을 각각 오른쪽/왼쪽 또는 위/아래로 드래그하여 값을 늘리거나 줄일 수 있습니다.

프로퍼티가 어디에 있느냐에 따라 범용 함수나 프로퍼티 전용 함수로 액세스합니다. 많은 프로퍼티는 자동으로 애니메이션할 수 있습니다. 성능과 편의성 측면에서 프로퍼티를 직접 조작하는 방식(`update()` 함수 안에서)보다 내장 시스템으로 프로퍼티를 애니메이션하는 방식을 강력히 권장합니다.

`vector3`, `vector4`, `quaternion` 타입의 복합 프로퍼티는 하위 컴포넌트(`x`, `y`, `z`, `w`)도 노출합니다. 이름 뒤에 점(`.`)과 컴포넌트 이름을 붙여 각 컴포넌트를 개별적으로 지정할 수 있습니다. 예를 들어 게임 오브젝트 위치의 x 컴포넌트를 설정하려면 다음과 같이 합니다.

```lua
-- "game_object"의 x 위치를 10으로 설정합니다.
go.set("game_object", "position.x", 10)
```

`go.get()`, `go.set()`, `go.animate()` 함수는 첫 번째 파라미터로 참조를, 두 번째 파라미터로 프로퍼티 식별자를 받습니다. 참조는 게임 오브젝트나 컴포넌트를 식별하며 문자열, 해쉬 또는 URL일 수 있습니다. URL은 [주소 지정 매뉴얼](/manuals/addressing)에서 자세히 설명합니다. 프로퍼티 식별자는 해당 프로퍼티의 이름을 나타내는 문자열 또는 해쉬입니다.

```lua
-- 스프라이트 컴포넌트의 x-scale을 설정합니다.
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

GUI 노드에서는 프로퍼티 전용 함수 또는 일반 `gui.get()` 및 `gui.set()` 함수의 첫 번째 파라미터로 노드를 전달합니다.

```lua
-- 버튼의 색상을 가져옵니다.
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## 게임 오브젝트와 컴포넌트 프로퍼티

모든 게임 오브젝트와 일부 컴포넌트 타입에는 런타임에 읽고 조작할 수 있는 프로퍼티가 있습니다. 이 값은 [`go.get()`](/ref/go#go.get)으로 읽고 [`go.set()`](/ref/go#go.set)으로 씁니다. 프로퍼티 값 타입에 따라 [`go.animate()`](/ref/go#go.animate)로 값을 애니메이션할 수 있습니다. 일부 프로퍼티는 읽기 전용입니다.

`get`{.mark}
: [`go.get()`](/ref/go#go.get)으로 읽을 수 있습니다.

`get+set`{.mark}
: [`go.get()`](/ref/go#go.get)으로 읽고 [`go.set()`](/ref/go#go.set)으로 쓸 수 있습니다. 숫자형 값은 [`go.animate()`](/ref/go#go.animate)로 애니메이션할 수 있습니다.

*게임 오브젝트 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | 게임 오브젝트의 로컬 위치입니다. | `vector3`      | `get+set`{.mark} |
| *rotation* | 쿼터니언(`quaternion`)으로 표현된 게임 오브젝트의 로컬 회전입니다.  | `quaternion` | `get+set`{.mark} |
| *euler*    | 게임 오브젝트의 로컬 회전인 오일러 각도(Euler angles)입니다. | `vector3` | `get+set`{.mark} |
| *scale*    | 각 컴포넌트가 각 축의 배율을 포함하는 벡터로 표현된 게임 오브젝트의 로컬 비균일 스케일입니다. Z를 변경하지 않고 X와 Y 크기를 두 배로 만들려면 `vmath.vector3(2.0, 2.0, 1.0)`을 사용합니다. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | X축과 Y축을 따르는 게임 오브젝트의 로컬 비균일 스케일입니다. Z 스케일링이 의도되지 않았다면 이 프로퍼티 또는 `go.set_scale_xy()`를 사용하세요. | `vector3` | `get+set`{.mark} |

::: sidenote
게임 오브젝트 변형을 다루는 전용 함수도 있습니다. `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()`, `go.set_scale_xy()`입니다.
:::

*스프라이트 컴포넌트 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | 스프라이트의 스케일되지 않은 크기, 즉 소스 아틀라스에서 가져온 크기입니다. | `vector3` | `get`{.mark} |
| *image* | 스프라이트의 텍스쳐 경로 해쉬입니다. | `hash` | `get`{.mark}|
| *scale* | 스프라이트의 비균일 스케일입니다. | `vector3` | `get+set`{.mark}|
| *scale.xy* | 스프라이트의 X축과 Y축 비균일 스케일입니다. | `vector3` | `get+set`{.mark}|
| *material* | 스프라이트에서 사용하는 메터리얼입니다. | `hash` | `get+set`{.mark}|
| *cursor* | 재생 커서의 위치(0--1 사이)입니다. | `number` | `get+set`{.mark}|
| *playback_rate* | flipbook 애니메이션의 프레임레이트입니다. | `number` | `get+set`{.mark}|

*충돌 오브젝트 컴포넌트 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | 충돌 오브젝트의 질량입니다. | `number` | `get`{.mark} |
| *linear_velocity* | 충돌 오브젝트의 현재 선형 속도입니다. | `vector3` | `get`{.mark} |
| *angular_velocity* | 충돌 오브젝트의 현재 각속도입니다. | `vector3` | `get`{.mark} |
| *linear_damping* | 충돌 오브젝트의 선형 감쇠입니다. | `vector3` | `get+set`{.mark} |
| *angular_damping* | 충돌 오브젝트의 각 감쇠입니다. | `vector3` | `get+set`{.mark} |

*모델(3D) 컴포넌트 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | 현재 애니메이션입니다.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | 모델의 텍스쳐 경로 해쉬입니다. | `hash` | `get+set`{.mark}|
| *cursor*  | 재생 커서의 위치(0--1 사이)입니다. | `number`   | `get+set`{.mark} |
| *playback_rate* | 애니메이션의 재생 속도입니다. 애니메이션 재생 속도에 대한 배율입니다. | `number` | `get+set`{.mark} |
| *material* | 모델에서 사용하는 메터리얼입니다. | `hash` | `get+set`{.mark}|

*라벨 컴포넌트 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | 라벨의 스케일입니다. | `vector3` | `get+set`{.mark} |
| *scale.xy* | 라벨의 X축과 Y축 스케일입니다. | `vector3` | `get+set`{.mark}|
| *color*     | 라벨의 색상입니다. | `vector4` | `get+set`{.mark} |
| *outline* | 라벨의 외곽선 색상입니다. | `vector4` | `get+set`{.mark} |
| *shadow* | 라벨의 그림자 색상입니다. | `vector4` | `get+set`{.mark} |
| *size* | 라벨의 크기입니다. 줄바꿈이 활성화되어 있으면 이 크기가 텍스트를 제한합니다. | `vector3` | `get+set`{.mark} |
| *material* | 라벨에서 사용하는 메터리얼입니다. | `hash` | `get+set`{.mark}|
| *font* | 라벨에서 사용하는 폰트입니다. | `hash` | `get+set`{.mark}|


## GUI 노드 프로퍼티

GUI 노드에는 `gui.get_position()`과 `gui.set_position()` 같은 프로퍼티 전용 getter 및 setter 함수가 있습니다. 아래 나열된 내장 프로퍼티는 `gui.get(node, property)`와 `gui.set(node, property, value)`로도 읽고 쓸 수 있습니다. 다른 노드 값에는 여전히 전용 함수가 필요할 수 있습니다. GUI 노드의 메터리얼 상수도 일반 함수를 사용합니다. 벡터 프로퍼티의 한 컴포넌트를 지정하려면 이름을 덧붙이세요. 예: `gui.set(node, "color.x", 1)`.

일반 함수와 프로퍼티 전용 함수가 항상 같은 값 타입을 사용하는 것은 아닙니다. `gui.get()`은 전체 `position`, `scale`, `size`, `euler` 프로퍼티에 대해 `vector4`를 반환하지만, 이에 대응하는 프로퍼티 전용 함수는 `vector3`를 반환합니다. `gui.set()`은 이러한 프로퍼티에 `vector3` 또는 `vector4`를 받습니다. 일반 `rotation` 프로퍼티는 쿼터니언을 사용합니다. 회전을 각도로 설정하려면 `euler`를 사용하세요.

* `position` (또는 `gui.PROP_POSITION`)
* `rotation` (또는 `gui.PROP_ROTATION`)
* `euler` (또는 `gui.PROP_EULER`)
* `scale` (또는 `gui.PROP_SCALE`)
* `color` (또는 `gui.PROP_COLOR`)
* `outline` (또는 `gui.PROP_OUTLINE`)
* `shadow` (또는 `gui.PROP_SHADOW`)
* `size` (또는 `gui.PROP_SIZE`)
* `fill_angle` (또는 `gui.PROP_FILL_ANGLE`)
* `inner_radius` (또는 `gui.PROP_INNER_RADIUS`)
* `leading` (또는 `gui.PROP_LEADING`)
* `tracking` (또는 `gui.PROP_TRACKING`)
* `slice9` (또는 `gui.PROP_SLICE9`)

모든 색상 값은 각 컴포넌트가 RGBA 값에 해당하는 `vector4`로 인코딩된다는 점에 유의하세요.

`x`
: 빨간색 색상 컴포넌트

`y`
: 녹색 색상 컴포넌트

`z`
: 파란색 색상 컴포넌트

`w`
: 알파 컴포넌트

*GUI 노드 프로퍼티*

| 프로퍼티   | 설명                            | 타입            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | 노드의 표면 색상입니다.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | 노드의 외곽선 색상입니다.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | 노드의 위치입니다. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | 노드의 회전입니다. getter는 쿼터니언을 반환하고 setter는 쿼터니언 또는 벡터로 표현한 오일러 각도를 받습니다. | `quaternion`, `vector3` 또는 `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | 각도로 표현된 노드의 오일러 회전입니다. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | 각 축에 대한 배율로 표현된 노드의 스케일입니다. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | 노드의 그림자 색상입니다. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | 노드의 스케일되지 않은 크기입니다. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | 반시계 방향 각도로 표현된 파이 노드의 채우기 각도입니다. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | 파이 노드의 내부 반지름입니다. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | 텍스트 노드의 줄 간격 배율입니다. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | 텍스트 노드의 자간 배율입니다. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | slice9 노드의 가장자리 거리입니다. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
