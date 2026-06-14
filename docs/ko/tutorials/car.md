---
title: Defold에서 간단한 자동차 만들기.
brief: Defold를 처음 접하는 경우, 이 가이드는 에디터에서 방향을 잡는 데 도움을 줍니다. 또한 Defold의 기본 개념과 가장 흔한 빌딩 블록인 게임 오브젝트, 컬렉션, 스크립트, 스프라이트도 설명합니다.
---

# 자동차 만들기

Defold를 처음 접하는 경우, 이 가이드는 에디터에서 방향을 잡는 데 도움을 줍니다. 또한 Defold의 기본 개념과 가장 흔한 빌딩 블록인 게임 오브젝트(game object), 컬렉션(collection), 스크립트(script), 스프라이트(sprite)도 설명합니다.

빈 프로젝트에서 시작해 아주 작지만 플레이할 수 있는 어플리케이션을 단계별로 만들어 보겠습니다. 끝까지 진행하면 Defold가 어떻게 동작하는지 감을 잡고, 더 긴 튜토리얼을 진행하거나 곧바로 매뉴얼을 살펴볼 준비가 될 것입니다.

::: sidenote
튜토리얼 전체에서 개념이나 특정 작업 방법에 대한 자세한 설명은 이 문단처럼 표시됩니다. 이런 섹션이 너무 자세하다고 느껴지면 건너뛰어도 됩니다.
:::

## 새 프로젝트 만들기

![New Project](images/new_empty.png)

1. Defold를 시작합니다.
2. 왼쪽에서 *New Project*를 선택합니다.
3. *From Template* 탭을 선택합니다.
4. *Empty Project*를 선택합니다.
5. 로컬 드라이브에서 프로젝트를 만들 위치를 선택합니다.
6. *Create New Project*를 클릭합니다.

## 에디터

[새 프로젝트](/manuals/project-setup/)를 만들고 에디터에서 여는 것으로 시작합니다. *main/main.collection* 파일을 더블 클릭하면 파일이 열립니다.

![Editor overview](../manuals/images/editor/editor2_overview.png)

에디터는 다음과 같은 주요 영역으로 구성되어 있습니다.

Assets pane
: 프로젝트의 모든 파일을 보여주는 뷰입니다. 파일 타입마다 다른 아이콘이 있습니다. 파일을 더블 클릭하면 해당 파일 타입에 맞는 에디터에서 열립니다. 특수한 읽기 전용 폴더인 *builtins*는 모든 프로젝트에 공통으로 포함되며, 기본 렌더 스크립트, 폰트, 다양한 컴포넌트 렌더링용 메터리얼 등 유용한 항목을 포함합니다.

Main Editor View
: 편집 중인 파일 타입에 따라 이 뷰에는 해당 타입의 에디터가 표시됩니다. 가장 흔히 사용하는 것은 여기 보이는 Scene editor입니다. 열린 각 파일은 별도의 탭으로 표시됩니다.

Changed Files
: 마지막 동기화 이후 현재 브랜치에서 수행한 모든 편집 목록을 포함합니다. 따라서 이 창에 항목이 보인다면 아직 서버에 올라가지 않은 변경 사항이 있다는 뜻입니다. 이 뷰에서 텍스트 전용 diff를 열고 변경 사항을 되돌릴 수 있습니다.

Outline
: 현재 편집 중인 파일의 내용을 계층 뷰로 보여줍니다. 이 뷰에서 오브젝트와 컴포넌트를 추가, 삭제, 수정, 선택할 수 있습니다.

Properties
: 현재 선택한 오브젝트 또는 컴포넌트에 설정된 프로퍼티입니다.

Console
: 게임을 실행할 때 이 뷰는 게임엔진에서 나오는 출력(로그, 오류, 디버그 정보 등)과 스크립트의 사용자 정의 `print()` 및 `pprint()` 디버그 메세지를 캡처합니다. 앱이나 게임이 시작되지 않는다면 콘솔을 가장 먼저 확인해야 합니다. 콘솔 뒤에는 오류 정보를 표시하는 여러 탭과, 파티클 효과를 만들 때 사용하는 Curve Editor가 있습니다.

## 게임 실행하기

"Empty" 프로젝트 템플릿은 실제로 완전히 비어 있습니다. 그래도 <kbd>Project ▸ Build</kbd>를 선택해 프로젝트를 빌드하고 게임을 실행합니다.

![Build](images/car/start_build_and_launch.png)

검은 화면은 그다지 흥미롭지 않을 수 있지만, 실행 중인 Defold 게임 어플리케이션이며 쉽게 더 재미있는 것으로 바꿀 수 있습니다. 이제 그렇게 해 보겠습니다.

::: sidenote
Defold 에디터는 파일 단위로 동작합니다. *Assets pane*에서 파일을 더블 클릭하면 적절한 에디터에서 파일이 열립니다. 그러면 해당 파일의 내용을 작업할 수 있습니다.

파일 편집을 마쳤으면 저장해야 합니다. 메인 메뉴에서 <kbd>File ▸ Save</kbd>를 선택합니다. 에디터는 저장되지 않은 변경 사항이 있는 파일의 탭 이름에 별표 '\*'를 붙여 힌트를 줍니다.

![File with unsaved changes](images/car/file_changed.png)
:::

## 자동차 조립하기

먼저 새 컬렉션을 만들겠습니다. 컬렉션(collection)은 배치하고 위치를 잡아 둔 게임 오브젝트의 컨테이너입니다. 컬렉션은 주로 게임 레벨을 만드는 데 사용되지만, 함께 속한 게임 오브젝트 그룹이나 계층구조를 재사용해야 할 때도 매우 유용합니다. 컬렉션을 일종의 프리팹(prefab)으로 생각하면 도움이 될 수 있습니다.

*Assets pane*에서 *main* 폴더를 클릭한 다음, 마우스 오른쪽 버튼을 누르고 <kbd>New ▸ Collection File</kbd>을 선택합니다. 메인 메뉴에서 <kbd>File ▸ New ▸ Collection File</kbd>을 선택해도 됩니다.

![New Collection file](images/car/start_new_collection.png)

새 컬렉션 파일 이름을 *car.collection*으로 지정하고 엽니다. 이 새 빈 컬렉션을 사용해 몇 개의 게임 오브젝트로 작은 자동차를 만들겠습니다. 게임 오브젝트(game object)는 게임을 만드는 데 사용하는 컴포넌트(스프라이트, 사운드, 로직 스크립트 등)의 컨테이너입니다. 각 게임 오브젝트는 게임 안에서 id로 유니크하게 식별됩니다. 게임 오브젝트는 메세지 전달을 통해 서로 통신할 수 있지만, 자세한 내용은 나중에 다룹니다.

또한 여기에서 한 것처럼 컬렉션 안에 게임 오브젝트를 내장(in-place)으로 만들 수도 있습니다. 이렇게 하면 하나뿐인 오브젝트가 만들어집니다. 이 오브젝트를 복사할 수는 있지만 각 복사본은 서로 독립적입니다. 하나를 변경해도 다른 복사본에는 영향을 주지 않습니다. 즉, 게임 오브젝트를 10개 복사한 뒤 모두 바꾸고 싶다는 사실을 깨닫게 되면, 그 오브젝트의 인스턴스 10개를 모두 편집해야 합니다. 따라서 내장으로 만든 게임 오브젝트는 많은 복사본을 만들 생각이 없는 오브젝트에 사용해야 합니다.

반면 _파일_에 저장된 게임 오브젝트는 프로토타입(prototype)으로 동작합니다(다른 엔진에서는 "prefabs" 또는 "blueprints"라고도 합니다). 파일로 저장된 게임 오브젝트의 인스턴스를 컬렉션에 배치하면 각 오브젝트는 _참조로_ 배치됩니다. 즉 프로토타입을 기반으로 한 클론입니다. 프로토타입을 변경해야 한다고 결정하면, 그 프로토타입을 기반으로 배치된 모든 게임 오브젝트가 즉시 업데이트됩니다.

![Add car gameobject](images/car/start_add_car_gameobject.png)

*Outline* 뷰에서 루트 "Collection" 노드를 선택하고, 마우스 오른쪽 버튼을 누른 다음 <kbd>Add Game Object</kbd>를 선택합니다. id가 "go"인 새 게임 오브젝트가 컬렉션에 나타납니다. 이 오브젝트를 선택하고 *Properties* 뷰에서 id를 "car"로 설정합니다. 지금까지의 "car"는 그다지 흥미롭지 않습니다. 비어 있고, 시각적 표현도 로직도 없습니다. 시각적 표현을 추가하려면 스프라이트 _컴포넌트_를 추가해야 합니다.

컴포넌트는 게임 오브젝트에 존재감(그래픽, 사운드)과 기능(스폰 팩토리, 충돌, 스크립트로 작성한 동작)을 확장하는 데 사용됩니다. 컴포넌트는 단독으로 존재할 수 없으며 반드시 게임 오브젝트 안에 있어야 합니다. 컴포넌트는 보통 게임 오브젝트와 같은 파일 안에 내장으로 정의됩니다. 하지만 컴포넌트를 재사용하려면, 게임 오브젝트처럼 별도 파일에 저장하고 어떤 게임 오브젝트 파일에서든 참조로 포함할 수 있습니다. 일부 컴포넌트 타입(예: Lua 스크립트)은 별도의 컴포넌트 파일에 배치한 뒤 오브젝트에서 참조로 포함해야 합니다.

컴포넌트를 직접 조작하는 것이 아니라는 점에 유의하세요. 컴포넌트를 포함하는 게임 오브젝트의 프로퍼티를 이동, 회전, 스케일, 애니메이션할 수 있습니다.

![Add car component](images/car/start_add_car_component.png)

"car" 게임 오브젝트를 선택하고, 마우스 오른쪽 버튼을 누른 다음 <kbd>Add Component</kbd>를 선택합니다. 그런 다음 *Sprite*를 선택하고 *Ok*를 클릭합니다. *Outline* 뷰에서 스프라이트를 선택하면 몇 가지 프로퍼티를 설정해야 한다는 것을 볼 수 있습니다.

Image
: 스프라이트에 사용할 이미지 소스가 필요합니다. *Assets pane* 뷰에서 "main"을 선택하고, 마우스 오른쪽 버튼을 누른 뒤 <kbd>New ▸ Atlas File</kbd>을 선택해 아틀라스 이미지 파일을 만듭니다. 새 아틀라스 파일 이름을 *sprites.atlas*로 지정하고 더블 클릭해서 아틀라스 에디터에서 엽니다. 아래의 두 이미지 파일을 컴퓨터에 저장하고 *Assets pane* 뷰의 *main*으로 드래그합니다. 이제 아틀라스 에디터에서 Atlas 루트 노드를 선택하고, 마우스 오른쪽 버튼을 누른 다음 <kbd>Add Images</kbd>를 선택합니다. 자동차와 타이어 이미지를 아틀라스에 추가하고 저장합니다. 이제 "car" 컬렉션의 "car" 게임 오브젝트에 있는 스프라이트 컴포넌트의 이미지 소스로 *sprites.atlas*를 선택할 수 있습니다.

게임에 사용할 이미지:

![Car image](images/car/start_car.png)
![Tire image](images/car/start_tire.png)

이 이미지들을 아틀라스에 추가합니다.

![Sprites atlas](images/car/start_sprites_atlas.png)

![Sprite properties](images/car/start_sprite_properties.png)

Default Animation
: 이 값을 "car"(또는 자동차 이미지에 지정한 이름)로 설정합니다. 각 스프라이트에는 게임에서 표시될 때 재생되는 기본 애니메이션이 필요합니다. 아틀라스에 이미지를 추가하면 Defold가 각 이미지 파일에 대해 한 프레임짜리(정지) 애니메이션을 편리하게 만들어 줍니다.

## 자동차 완성하기

계속해서 컬렉션에 게임 오브젝트 두 개를 더 추가합니다. 이름을 "left_wheel"과 "right_wheel"로 지정하고, 각각에 스프라이트 컴포넌트를 넣어 *sprites.atlas*에 추가한 타이어 이미지를 표시하게 합니다. 그런 다음 휠 게임 오브젝트를 잡아 "car" 위로 드롭해 "car" 아래의 자식으로 만듭니다. 다른 게임 오브젝트 아래에 자식으로 있는 게임 오브젝트는 부모가 움직일 때 부모에 붙어서 움직입니다. 개별적으로도 움직일 수 있지만, 모든 움직임은 부모 오브젝트를 기준으로 일어납니다. 타이어의 경우 자동차에 붙어 있어야 하고, 조향할 때 약간 좌우로 회전시키기만 하면 되므로 이 방식이 완벽합니다. 컬렉션은 게임 오브젝트를 개수 제한 없이 포함할 수 있으며, 나란히 둘 수도 있고 복잡한 부모-자식 트리로 배치할 수도 있으며, 두 방식을 섞을 수도 있습니다.

타이어 게임 오브젝트를 선택한 다음 <kbd>Scene ▸ Move Tool</kbd>을 선택해 제자리로 이동합니다. 화살표 핸들이나 중앙의 초록색 사각형을 잡고 오브젝트를 적절한 위치로 움직입니다. 마지막으로 해야 할 일은 타이어가 자동차 아래에 그려지도록 하는 것입니다. 이를 위해 포지션의 Z 컴포넌트를 -0.5로 설정합니다. 게임의 모든 시각적 항목은 Z 값에 따라 정렬되어 뒤에서 앞으로 그려집니다. Z 값이 0인 오브젝트는 Z 값이 -0.5인 오브젝트 위에 그려집니다. 자동차 게임 오브젝트의 기본 Z 값은 0이므로, 타이어 오브젝트에 새 값을 설정하면 타이어가 자동차 이미지 아래에 놓입니다.

![Car collection complete](images/car/start_car_collection_complete.png)

## 자동차 스크립트

퍼즐의 마지막 조각은 자동차를 제어할 _스크립트_입니다. 스크립트는 게임 오브젝트의 동작을 정의하는 프로그램을 포함한 컴포넌트입니다. 스크립트를 사용하면 게임의 규칙과 오브젝트가 여러 상호작용(플레이어 및 다른 오브젝트와의 상호작용)에 어떻게 반응해야 하는지를 지정할 수 있습니다. 모든 스크립트는 Lua 프로그래밍 언어로 작성됩니다. Defold로 작업하려면 사용자 또는 팀원 중 누군가는 Lua 프로그래밍을 배워야 합니다.

*Assets pane*에서 "main"을 선택하고, 마우스 오른쪽 버튼을 누른 뒤 <kbd>New ▸ Script File</kbd>을 선택합니다. 새 파일 이름을 *car.script*로 지정한 다음, *Outline* 뷰에서 "car"를 선택하고 마우스 오른쪽 버튼을 누른 뒤 <kbd>Add Component File</kbd>을 선택해 "car" 게임 오브젝트에 추가합니다. *car.script*를 선택하고 *OK*를 클릭합니다. 컬렉션 파일을 저장합니다.

*car.script*를 더블 클릭해 엽니다.

::: sidenote
Defold는 게임 로직을 코딩하기 위한 여러 라이프사이클 함수를 제공합니다. 자세한 내용은 [스크립트 매뉴얼](/manuals/script)을 읽어 보세요.
:::

이 튜토리얼에서는 필요하지 않으므로 먼저 `final`, `on_message`, `on_reload` 함수를 제거합니다.

다음으로, `init` 함수가 시작되기 전에 아래 코드 줄을 추가합니다.

```lua
-- 상수
local turn_speed = 0.1                           									  -- Slerp 계수
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30도
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30도
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- 0도
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- 뒤/앞 바퀴 쌍 중심 사이의 벡터

local acceleration = 100 																						-- 자동차의 가속도

-- 입력을 미리 해쉬합니다
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

여기에서 한 변경은 꽤 간단합니다. 나중에 자동차를 코딩할 때 사용할 여러 `constants`를 스크립트에 추가했을 뿐입니다.

::: sidenote
해쉬를 미리 변수에 저장하는 방식에 주목하세요. 이렇게 하면 코드가 더 읽기 쉽고 성능도 좋아지므로 실제로 좋은 습관입니다.
:::

다음으로, `init` 함수가 아래 내용을 포함하도록 편집합니다.

```lua
function init(self)
	-- 렌더 스크립트(builtins/render/default.render_script 참고)에 메세지를 보내 clear color를 설정합니다.
	-- 이렇게 하면 게임의 배경색이 바뀝니다. vector4에는 색상 정보가 들어 있습니다.
	-- 채널별 범위는 0-1입니다: Red = 0.2. Green = 0.2, Blue = 0.2, Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- 입력에 반응할 수 있도록 입력 포커스를 획득합니다
	msg.post(".", "acquire_input_focus")		-- <2>

	-- 몇 가지 변수
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- 속도와 가속도는 자동차 기준입니다(회전되지 않음)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- 입력 벡터입니다. 나중에 on_input 함수에서 입력을 저장하도록 수정됩니다.
	self.input = vmath.vector3()
end
```

무엇을 바꾼 것인지 궁금한가요? 설명은 다음과 같습니다.

1. 배경색을 회색으로 설정해 달라고 렌더 스크립트에 메세지를 보냅니다. 렌더 스크립트는 오브젝트가 화면에 표시되는 방식을 제어하는 Defold의 특수 스크립트입니다.
2. 스크립트 컴포넌트나 GUI 스크립트에서 입력 동작을 받으려면, 해당 컴포넌트를 가진 게임 오브젝트에 `acquire_input_focus` 메세지를 보내야 합니다. 여기서는 자동차 스크립트를 가진 게임 오브젝트에 이 메세지를 보냅니다.
3. 그런 다음 자동차의 현재 상태를 추적하는 데 사용할 몇 가지 변수를 선언합니다.

쉽죠? 이제 `update` 함수를 편집해 아래 내용을 포함하도록 하겠습니다.

```lua
function update(self, dt)
	-- y 입력으로 가속도를 설정합니다
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- 앞바퀴와 뒷바퀴의 새 위치를 계산합니다
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- 자동차의 새 방향을 계산합니다
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- 현재 가속도를 기준으로 새 속도를 계산합니다
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- 현재 속도와 방향을 기준으로 포지션을 업데이트합니다
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- vmath.slerp를 사용해 바퀴를 보간합니다
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- 바퀴 회전을 업데이트합니다
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- 게임 오브젝트의 회전을 방향으로 설정합니다
	go.set_rotation(self.direction)

	-- 가속도와 입력을 재설정합니다
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

꽤 큰 함수였습니다. 하지만 걱정하지 마세요. 전체 동작 방식은 다음과 같습니다.

1. 먼저 입력 벡터를 기준으로 가속도 벡터를 설정합니다. 이렇게 하면 자동차의 가속도가 입력 방향을 따르게 됩니다.
2. 다음으로, 자동차의 뒷바퀴는 항상 앞으로 움직이고 앞바퀴는 틀어진 방향으로 움직인다는 단순한 로직을 기준으로 두 바퀴의 변위를 계산합니다.
3. 두 바퀴의 변위를 기준으로 자동차의 새 이동 방향을 계산합니다.
4. 여기에서 계산된 가속도를 속도에 더합니다.
5. 마지막으로 현재 속도를 기준으로 자동차의 포지션을 업데이트합니다.
6. 왼쪽/오른쪽 입력을 기준으로 조향 각도를 slerp합니다. 이렇게 하면 입력이 바뀔 때마다 바퀴가 즉시 튀듯이 회전하지 않습니다.
7. 그런 다음 자동차의 현재 조향 각도를 기준으로 바퀴의 회전을 설정합니다. 마찬가지로 자동차의 회전은 현재 이동 중인 방향을 기준으로 설정합니다.
8. 마지막으로 가속도와 입력 벡터를 재설정합니다.

마지막으로 자동차가 입력에 반응하게 할 차례입니다. `on_input` 함수를 아래와 같이 업데이트합니다.

```lua
function on_input(self, action_id, action)
	-- 키 입력에 대응하도록 입력 벡터를 설정합니다
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

이 함수는 실제로 꽤 간단합니다. 입력을 받아 입력 벡터를 설정할 뿐입니다.

편집 내용을 저장하는 것을 잊지 마세요.

## 입력

아직 입력 동작이 설정되어 있지 않으므로 이를 고쳐 보겠습니다. */input/game.input_bindings* 파일을 열고 "accelerate", "brake", "left", "right"에 대한 *key_trigger* 바인딩을 추가합니다. 이 값들을 화살표 키(KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN)로 설정합니다.

![Input bindings](images/car/start_input_bindings.png)

## 게임에 자동차 추가하기

이제 자동차를 굴릴 준비가 되었습니다. "car.collection" 안에 자동차를 만들었지만, 아직 게임 안에는 존재하지 않습니다. 현재 엔진은 시작할 때 "main.collection"을 로드하기 때문입니다. 이를 해결하려면 *car.collection*을 *main.collection*에 추가하기만 하면 됩니다. *main.collection*을 열고, *Outline* 뷰에서 "Collection" 루트 노드를 선택한 다음, 마우스 오른쪽 버튼을 누르고 <kbd>Add Collection From File</kbd>을 선택합니다. *car.collection*을 선택하고 *OK*를 클릭합니다. 이제 *car.collection*의 내용이 새 인스턴스로 *main.collection*에 배치됩니다. *car.collection*의 내용을 변경하면 게임이 빌드될 때 컬렉션의 각 인스턴스가 자동으로 업데이트됩니다.

![Adding the car collection](images/car/start_adding_car_collection.png)

이제 <kbd>Project ▸ Build</kbd>를 선택하고 새 자동차를 몰아 보세요!
이제 자동차를 원하는 대로 움직일 수 있다는 것을 알 수 있습니다. 하지만 아직 뭔가 맞지 않습니다. 조작을 멈춰도 자동차가 멈추지 않습니다. 이제 그 부분을 추가할 차례입니다!

## 항력이 해결해 줍니다

현실 세계에서 오브젝트가 움직일 때마다 항력(drag)이 오브젝트의 반대 방향으로 작용해 속도를 늦춥니다. 이 힘은 움직이는 오브젝트의 속도 제곱에 거의 비례하므로, `D = k * |V| * V`로 설명할 수 있습니다. 여기서 `k`는 상수, `V`는 속도, `|V|`는 그 크기(속력)입니다. 이제 이를 추가해 보겠습니다.

스크립트 맨 위의 상수 섹션에 다음 상수를 추가합니다.

```lua
local drag = 1.1	        -- 항력 상수 <1>
```

그런 다음 `update` 함수에서 아래 줄 바로 위에 다음 줄들을 추가하고 파일을 저장합니다.

```lua
function update(self, dt)
	...
  -- 현재 가속도를 기준으로 새 속도를 계산합니다
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- 속력은 속도의 크기입니다
	local speed = vmath.length_sqr(self.velocity)

	-- 항력을 적용합니다
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- 이미 충분히 느리면 멈춥니다
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. 항력 값을 상수로 선언합니다.
2. 이동 중인 속력을 계산합니다.
3. 공식을 기준으로 현재 가속도에 항력을 적용합니다.
4. 자동차가 이미 충분히 느리면 멈춥니다.

## 전체 자동차 스크립트

위 단계를 완료하면 *car.script*는 다음과 같아야 합니다.

```lua
local turn_speed = 0.1                           				          	-- Slerp 계수
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30도
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30도
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- 0도
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- 뒤/앞 바퀴 쌍 중심 사이의 벡터

local acceleration = 100 		                      									-- 자동차의 가속도
local drag = 1.1                                                  	-- 항력 상수

function init(self)
	-- 렌더 스크립트(builtins/render/default.render_script 참고)에 메세지를 보내 clear color를 설정합니다.
	-- 이렇게 하면 게임의 배경색이 바뀝니다. vector4에는 색상 정보가 들어 있습니다.
	-- 채널별 범위는 0-1입니다: Red = 0.2. Green = 0.2, Blue = 0.2, Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- 입력에 반응할 수 있도록 입력 포커스를 획득합니다
	msg.post(".", "acquire_input_focus")

	-- 몇 가지 변수
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- 속도와 가속도는 자동차 기준입니다(회전되지 않음)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- 입력 벡터입니다. 나중에 on_input 함수에서 수정되어
	-- 입력을 저장합니다.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- y 입력으로 가속도를 설정합니다
	self.acceleration.y = self.input.y * acceleration

	-- 앞바퀴와 뒷바퀴의 새 위치를 계산합니다
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- 자동차의 새 방향을 계산합니다
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- 속력은 속도의 크기입니다
	local speed = vmath.length(self.velocity)

	-- 항력을 적용합니다
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- 이미 충분히 느리면 멈춥니다
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- 현재 가속도를 기준으로 새 속도를 계산합니다
	self.velocity = self.velocity + self.acceleration * dt

	-- 현재 속도와 방향을 기준으로 포지션을 업데이트합니다
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- vmath.slerp를 사용해 바퀴를 보간합니다
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- 바퀴 회전을 업데이트합니다
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- 게임 오브젝트의 회전을 방향으로 설정합니다
	go.set_rotation(self.direction)

	-- 가속도와 입력을 재설정합니다
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- 키 입력에 대응하도록 입력 벡터를 설정합니다
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## 최종 게임 실행해 보기

이제 메인 메뉴에서 <kbd>Project ▸ Build</kbd>를 선택하고 새 자동차를 몰아 보세요!

이것으로 입문 튜토리얼을 마칩니다. 직접 도전해 볼 만한 과제는 다음과 같습니다.

1. 현재 자동차는 전진과 후진 방향에서 같은 가속도로 움직입니다. 후진할 때는 자동차가 더 느리게 움직이도록 바꿔 볼 수 있습니다.
2. 일부 상수(예: 가속도)를 `properties`로 만들어 자동차의 인스턴스마다 다르게 변경할 수 있게 해 보세요.
3. 자동차에 사운드를 추가하고 부릉거리게 만들어 보세요! ([힌트](/manuals/sound/))

이제 Defold를 파고들어 보세요. 안내를 돕기 위해 많은 [매뉴얼과 튜토리얼](/learn)을 준비해 두었고, 막히는 부분이 있으면 언제든 [forum](//forum.defold.com)에 오셔도 좋습니다.

즐거운 Defolding 되세요!
