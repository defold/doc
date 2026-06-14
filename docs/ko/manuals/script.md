---
title: 스크립트로 게임 로직 작성하기
brief: 이 매뉴얼은 스크립트 컴포넌트를 사용해 게임 로직을 추가하는 방법을 설명합니다.
---

# 스크립트

스크립트 컴포넌트를 사용하면 [Lua 프로그래밍 언어](/manuals/lua)로 게임 로직을 만들 수 있습니다.


## 스크립트 타입

Defold에는 세 가지 Lua 스크립트 타입이 있으며, 각 타입마다 사용할 수 있는 Defold 라이브러리가 다릅니다.

게임 오브젝트 스크립트
: 확장자 _.script_. 이 스크립트는 다른 [컴포넌트](/manuals/components)와 마찬가지로 게임 오브젝트에 추가되며, Defold는 엔진 라이프사이클 함수의 일부로 Lua 코드를 실행합니다. 게임 오브젝트 스크립트는 보통 게임 오브젝트와 레벨 로딩, 게임 규칙 등 게임을 하나로 묶는 로직을 제어하는 데 사용됩니다. 게임 오브젝트 스크립트는 [GO](/ref/go) 함수와 [GUI](/ref/gui) 및 [Render](/ref/render) 함수를 제외한 모든 Defold 라이브러리 함수에 액세스할 수 있습니다.


GUI 스크립트
: 확장자 _.gui_script_. GUI 컴포넌트가 실행하며, 보통 헤드업 디스플레이, 메뉴 등 GUI 요소를 표시하는 데 필요한 로직을 담습니다. Defold는 엔진 라이프사이클 함수의 일부로 Lua 코드를 실행합니다. GUI 스크립트는 [GUI](/ref/gui) 함수와 [GO](/ref/go) 및 [Render](/ref/render) 함수를 제외한 모든 Defold 라이브러리 함수에 액세스할 수 있습니다.


렌더 스크립트
: 확장자 _.render_script_. 렌더링 파이프라인이 실행하며, 매 프레임 모든 앱/게임 그래픽을 렌더링하는 데 필요한 로직을 담습니다. 렌더 스크립트는 게임 라이프사이클에서 특별한 위치를 차지합니다. 자세한 내용은 [어플리케이션 라이프사이클 문서](/manuals/application-lifecycle)에서 확인할 수 있습니다. 렌더 스크립트는 [Render](/ref/render) 함수와 [GO](/ref/go) 및 [GUI](/ref/gui) 함수를 제외한 모든 Defold 라이브러리 함수에 액세스할 수 있습니다.


## 스크립트 실행, 콜백과 self

Defold는 엔진 라이프사이클의 일부로 Lua 스크립트를 실행하고, 미리 정의된 콜백 함수 집합을 통해 라이프사이클을 노출합니다. 게임 오브젝트에 스크립트 컴포넌트를 추가하면 해당 스크립트는 게임 오브젝트와 그 컴포넌트의 라이프사이클에 포함됩니다. 스크립트는 로드될 때 Lua 컨텍스트에서 평가되며, 그 뒤 엔진이 다음 함수들을 실행하고 현재 스크립트 컴포넌트 인스턴스에 대한 참조를 파라미터로 전달합니다. 이 `self` 참조를 사용해 컴포넌트 인스턴스에 상태를 저장할 수 있습니다.

::: important
`self`는 Lua 테이블처럼 동작하는 `userdata` 오브젝트이지만, `pairs()`나 `ipairs()`로 순회할 수 없고 `pprint()`로 출력할 수 없습니다.
:::

#### `init(self)`
컴포넌트가 초기화될 때 호출됩니다.

```lua
function init(self)
  -- 이 변수들은 컴포넌트 인스턴스의 수명 동안 사용할 수 있습니다
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
컴포넌트가 삭제될 때 호출됩니다. 예를 들어 컴포넌트가 삭제될 때 함께 삭제되어야 하는 게임 오브젝트를 스폰했다면 정리 작업에 유용합니다.

```lua
function final(self)
  if self.my_var == "something" then
      -- 정리 작업을 수행합니다
  end
end
```

#### `fixed_update(self, dt)`
프레임레이트와 독립적인 업데이트입니다. 파라미터 `dt`에는 마지막 업데이트 이후의 delta time이 담깁니다. 이 함수는 프레임 타이밍과 고정 업데이트 주파수에 따라 `0-N`번 호출됩니다. 이 함수는 *game.project*에서 `Physics`-->`Use Fixed Timestep`가 활성화되어 있고 `Engine`-->`Fixed Update Frequency`가 0보다 클 때만 호출됩니다. 안정적인 물리 시뮬레이션을 얻기 위해 정해진 간격으로 물리 오브젝트를 조작하려는 경우 유용합니다.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
모든 스크립트의 `fixed_update` 콜백 뒤에 프레임마다 한 번 호출됩니다(Fixed Timestep이 활성화된 경우). 파라미터 `dt`에는 마지막 프레임 이후의 delta time이 담깁니다.

```lua
function update(self, dt)
  self.age = self.age + dt -- timestep만큼 age를 증가시킵니다
end
```

#### `late_update(self, dt)`
모든 스크립트의 `update` 콜백 뒤, 렌더 직전에 프레임마다 한 번 호출됩니다. 파라미터 `dt`에는 마지막 프레임 이후의 delta time이 담깁니다.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
메세지가 [`msg.post()`](/ref/msg#msg.post)를 통해 스크립트 컴포넌트로 전송되면 엔진은 수신자 컴포넌트의 이 함수를 호출합니다. [메세지 전달에 대해 자세히 알아보세요](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
이 컴포넌트가 입력 포커스를 획득했다면([`acquire_input_focus`](/ref/go/#acquire_input_focus) 참고), 입력이 등록될 때 엔진이 이 함수를 호출합니다. [입력 처리에 대해 자세히 알아보세요](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
이 함수는 에디터의 핫 리로드 기능(<kbd>Edit ▸ Reload Resource</kbd>)을 통해 스크립트가 다시 로드될 때 호출됩니다. 디버깅, 테스트 및 튜닝에 매우 유용합니다. [핫 리로드에 대해 자세히 알아보세요](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- 이 게임 오브젝트의 age를 출력합니다
end
```


## 반응형 로직

스크립트 컴포넌트를 가진 게임 오브젝트는 특정 로직을 구현합니다. 그 로직은 외부 요인에 의존하는 경우가 많습니다. 적 AI는 플레이어가 AI의 특정 반경 안에 들어왔을 때 반응할 수 있고, 문은 플레이어 상호작용의 결과로 잠금 해제되고 열릴 수 있습니다.

`update()` 함수를 사용하면 매 프레임 실행되는 상태 머신으로 정의된 복잡한 동작을 구현할 수 있으며, 때로는 이것이 적절한 접근 방식입니다. 하지만 `update()`를 호출할 때마다 비용이 발생합니다. 이 함수가 꼭 필요하지 않다면 삭제하고, 대신 로직을 _반응형_으로 구성해 보세요. 어떤 메세지가 응답을 트리거할 때까지 수동적으로 기다리는 편이, 응답할 데이터를 찾기 위해 게임 월드를 능동적으로 검사하는 것보다 비용이 낮습니다. 또한 설계 문제를 반응형으로 해결하면 더 깔끔하고 안정적인 설계와 구현으로 이어지는 경우도 많습니다.

구체적인 예를 살펴보겠습니다. 스크립트 컴포넌트가 시작된 뒤 2초 후에 메세지를 보내도록 하고 싶다고 가정합니다. 그다음 특정 응답 메세지를 기다렸다가, 응답을 받은 뒤 5초 후에 다른 메세지를 보내야 합니다. 이에 대한 비반응형 코드는 다음과 비슷합니다.

```lua
function init(self)
    -- 시간을 추적하기 위한 카운터입니다.
    self.counter = 0
    -- 상태를 추적하기 위해 필요합니다.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- 2초 후 메세지를 보냅니다
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- "response"를 받은 뒤 5초 후 메세지를 보냅니다
        msg.post("another_object", "another_message")
        -- 이 상태 블록에 다시 도달하지 않도록 state를 nil로 만듭니다.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- "first" 상태가 끝났습니다. 다음 상태로 들어갑니다
        self.state = "second"
        -- 카운터를 0으로 되돌립니다
        self.counter = 0
    end
end
```

이처럼 꽤 단순한 경우에도 로직이 상당히 얽힙니다. 모듈의 코루틴을 사용하면 이 코드를 더 보기 좋게 만들 수도 있지만(아래 참고), 여기서는 대신 반응형으로 만들고 내장 타이밍 메커니즘을 사용해 보겠습니다.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- 2초 기다린 뒤 send_first()를 호출합니다
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- 5초 기다린 뒤 send_second()를 호출합니다
		timer.delay(5, false, send_second)
	end
end
```

이 방식은 더 깔끔하고 따라가기 쉽습니다. 로직을 따라가기 어렵게 만들고 미묘한 버그로 이어질 수 있는 내부 상태 변수를 없앨 수 있습니다. 또한 `update()` 함수도 완전히 제거합니다. 그러면 스크립트가 아무 작업도 하지 않을 때도 엔진이 초당 60번 호출해야 하는 부담이 사라집니다.


## 전처리

Lua 전처리기와 특수 마크업을 사용해 빌드 변형에 따라 조건부로 코드를 포함할 수 있습니다. 예:

```lua
-- 다음 키워드 중 하나를 사용합니다: RELEASE, DEBUG 또는 HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE
local lives_num = 3
--#ENDIF
```

이 전처리기는 빌드 익스텐션으로 사용할 수 있습니다. 설치 및 사용 방법에 대한 자세한 내용은 [GitHub의 익스텐션 페이지](https://github.com/defold/extension-lua-preprocessor)에서 확인하세요.


## 에디터 지원

Defold 에디터는 구문 색상 표시와 자동 완성으로 Lua 스크립트 편집을 지원합니다. Defold 함수 이름을 완성하려면 *Ctrl+Space*를 눌러 입력 중인 내용과 일치하는 함수 목록을 표시합니다.

![자동 완성](images/script/completion.png)
