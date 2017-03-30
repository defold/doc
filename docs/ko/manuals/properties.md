# Properties
이 메뉴얼은 Defold에 존재하는 프로퍼티들의 종류와 이 프로퍼티를 어떻게 사용하고 에니메이션 처리하는지 설명합니다.

## Property types
Defold에서는 여러 개의 프로퍼티 세트가 있습니다.

* 시스템이 정의한 게임 오브젝트 트랜스폼 (위치, 회전, 스케일) 그리고 컴포넌트별 특정 프로퍼티(예를 들어, 스프라이트의 픽셀 사이즈나 충돌 오브젝트의 질량값 등)
* Lua 스크립트에 정의된 스크립트 컴포넌트의 프로퍼티 (자세한 것은 [Script properties](Script properties) 문서 참고)
* GUI 노드 프로퍼티
* 쉐이더나 메터리얼 파일에 정의된 쉐이더 상수 (자세한 것은 [Material](Material) 문서 참고)

프로퍼티가 어디에 있는지에 따라 보통의 함수 혹은 특정 함수를 통해 액세스 할 수있습니다. 많은 프로퍼티들은 자동으로 에니메이션될 수 있습니다. 내장 시스템을 통한 애니메이션 프로퍼티는 직접 프로퍼티를 다루는 것(update() 함수 내에서) 보다 성능과 편리함을 이유로 강력히 권장합니다.

또한 vector3, vector4, quaternion 형식의 복합 프로퍼티는 하위 컴포넌트(x,y,z,w)를 노출하는데 점(dot)을 이용해 이름의 접미사에 붙여 개별적으로 컴포넌트에 접근할 수 있습니다. 예를 들어, 게임 오브젝트 위치의 x 컴포넌트를 수정하려면 아래와 같이 할 수 있습니다.

```lua
-- "game_object"의 x 좌표를 10으로 셋팅
go.set("game_object", "position.x", 10)
```

go.get(), go.set(), go.animate() 함수는 첫번째 인자와 두번째의 프로퍼티 식별자로 레퍼런스를 얻게 됩니다. 이 레퍼런스는 게임 오브젝드나 컴포넌트를 식별하며 문자열이나 해쉬나 URL이 될 수 있습니다. URL은 [Message passing](Message passing) 문서에 자세히 설명되어 있습니다. 프로퍼티 식별자는 프로퍼티에 이름을 지정하는 문자열 혹은 해쉬값입니다.

```lua
-- sprite 컴포넌트의 x-scale 값을 변경
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

GUI 노드의 경우, 노드 식별자는 특정 프로퍼티 함수로 제공됩니다.

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
```

## System defined game object and component properties
모든 게임 오브젝트와 몇몇 컴포넌트 타입은 런타임시 읽고 다룰 수 있는 프로퍼티를 가지고 있습니다. 이 값은 [go.get()](http://www.defold.com/ref/go#go.get)로 읽고 [go.set()](http://www.defold.com/ref/go#go.set)으로 쓸 수 있으며 프로퍼티 값의 타입에 따라서 [go.animate()](http://www.defold.com/ref/go#go.animate)으로 값을 에니메이션 처리 할 수 있습니다. 몇몇 프로퍼티는 읽기 전용입니다.

``get``
[go.get()](http://www.defold.com/ref/go#go.get)으로 읽을 수 있음

``get+set``
[go.get()](http://www.defold.com/ref/go#go.get)으로 읽고 [go.set()](http://www.defold.com/ref/go#go.set)으로 쓸 수 있음. 숫자형 값은 [go.animate()](http://www.defold.com/ref/go#go.animate) 으로 애니메이션 처리 가능

> 게임 오브젝트의 프로퍼티를 읽고 쓸 수 있는 go.get_position(), go.set_position(), go.get_rotation(), go.set_rotation() 등등의 레거시 함수도 있습니다.

### GAME OBJECT PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **position** | 게임 오브젝트의 로컬 좌표값 | ``vector3`` | ``get+set`` |
| **rotation** | 게임 오브젝트의 로컬 회전값 (쿼터니온) | ``quaternion`` | ``get+set`` |
| **euler** | 게임 오브젝트의 로컬 회전값 (오일러 각) | ``vector3`` | ``get+set`` |
| **scale** | 게임 오브젝트의 로컬 균일(uniform) 스케일값 (1이면 100%(원본)스케일) | ``number`` | ``get+set`` |

### SPRITE COMPONENT PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **size** | 스프라이트의 크기가 아닌, 아틀라스 소스에서 가져온 크기 | ``vector3`` | ``get`` |
| **scale** | 스프라이트의 비균일(Non uniform) 스케일값.  vector를 사용하여 각 축(axis) 마다 다른 비율을 설정할 수 있음. x와 y축을 두 배로 늘리려면 vmath.vector3(2.0, 2.0, 0) 를 사용하면 됨 | ``vector3`` | ``get+set`` |

### COLLISION OBJECT COMPONENT PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **mass** | 충돌 오브젝트의 질량 | ``number`` | ``get`` |
| **linear_velocity** | 충돌 오브젝트의 현재 선형 속도 | ``vector3`` | ``get`` |
| **angular_velocity** | 충돌 오브젝트의 현재 각 속도 | ``vector3`` | ``get`` |
| **linear_damping** | 충돌 오브젝트의 선형 제동값 | ``vector3`` | ``get+set`` |
| **angular_damping** | 충돌 오브젝트의 각 제동값 | ``vector3`` | ``get+set`` |

### SPINE MODEL COMPONENT PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **animation** | 현재 애니메이션 | ``hash`` | ``get`` |
| **skin** | 현재 반영된 모델의 스킨(에니메이션 될 수 없음!) | ``hash`` | ``get+set`` |
| **cursor** | 애니메이션 재생 커서의 현재 위치(0~1 사이) | ``number`` | ``get+set`` |
| **playback_rate** | 애니메이션 재생 속도. 기본 애니메이션 속도의 배수(multiplier) | ``number`` | ``get+set`` |

### MODEL (3D) COMPONENT PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **animation** | 현재 애니메이션 | ``hash`` | ``get`` |
| **cursor** | 애니메이션 재생 커서의 현재 위치(0~1 사이) | ``number`` | ``get+set`` |
| **playback_rate** | 애니메이션 재생 속도. 기본 애니메이션 속도의 배수(multiplier) | ``number`` | ``get+set`` |

## GUI node properties
GUI 노드 또한 프로퍼티를 가지고 있지만, 특별한 getter, setter 함수로 읽고 쓸 수 있습니다. 각 프로퍼티는 get-과 set- 함수 형태로 존재하며 애니메이션을 만들 때 프로퍼티에 대한 참조로 사용할 수 있도록 미리 정의된 상수가 제공됩니다. 별도 프로퍼티를 참조하려면 프로퍼티의 문자열 이름이나 문자열 이름의 해쉬값을 사용해야 합니다.

* "position" (또는 gui.PROP_POSITION)
* "rotation" (또는 gui.PROP_ROTATION)
* "scale" (또는 gui.PROP_SCALE)
* "color" (또는 gui.PROP_COLOR)
* "outline" (또는 gui.PROP_OUTLINE)
* "shadow" (또는 gui.PROP_SHADOW)
* "size" (또는 gui.PROP_SIZE)
* "fill_angle" (또는 gui.PROP_FILL_ANGLE)
* "inner_radius" (또는 gui.PROP_INNER_RADIUS)
* "slice9" (또는 gui.PROP_SLICE9)

모든 색상 값은 RGBA 값에 해당하는 vector4로 인코딩 됩니다.

**x** - red color
**y** - green color
**z** - blue color
**w** - alpha

## GUI NODE PROPERTIES
|  |  |  |  |
| :------------ | :------------ | :------------ | :------------ |
| **color** | 노드의 색상 | ``vector4`` | gui.get_color(), gui.set_color() |
| **outline** | 노드의 외곽선 색 | ``vector4`` | gui.get_outline(), gui.set_outline() |
| **position** | 노드의 위치 | ``vector3`` | gui.get_position(), gui.set_position() |
| **rotation** | 노드의 회전값 (오일러각-각각의 축을 기준으로 회전하는 각도) | ``vector3`` | gui.get_rotation(), gui.set_rotation() |
| **scale** | 노드의 스케일(각각의 축을 기준으로 스케일됨) | ``vector3`` | gui.get_scale(), gui.set_scale() |
| **shadow** | 노드의 그림자 색상 | ``vector4`` | gui.get_shadow(), gui.set_shadow() |
| **size** | 노드의 스케일되지 않은 사이즈(unscaled size) | ``vector3`` | gui.get_size(), gui.set_size() |
| **fill_angle** | pie 노드에 색상을 채우기 위한 반시계 방향의 각도 | ``number`` | gui.get_fill_angle(), gui.set_fill_angle() |
| **inner_radius** | pie 노드의 내부 반지름 | ``number`` | gui.get_inner_radius(), gui.set_inner_radius() |
| **slice9** | slice9 노드의 가장자리 거리(edge distance) | ``vector4`` | - |
