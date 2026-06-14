---
title: Defold의 GUI 스크립트
brief: 이 매뉴얼은 GUI 스크립팅을 설명합니다.
---

# GUI 스크립트

GUI의 로직을 제어하고 노드를 애니메이션하려면 Lua 스크립트를 사용합니다. GUI 스크립트는 일반 게임 오브젝트 스크립트와 같은 방식으로 동작하지만, 다른 파일 타입으로 저장되며 `gui` 모듈 함수라는 다른 함수 집합에 액세스할 수 있습니다.

## GUI에 스크립트 추가하기

GUI에 스크립트를 추가하려면 먼저 *Assets* 브라우저의 한 위치에서 <kbd>마우스 오른쪽 버튼 클릭</kbd>하고 팝업 컨텍스트 메뉴에서 <kbd>New ▸ Gui Script</kbd>를 선택해 GUI 스크립트 파일을 만듭니다.

에디터가 새 스크립트 파일을 자동으로 엽니다. 이 파일은 템플릿을 기반으로 하며, 게임 오브젝트 스크립트와 마찬가지로 비어 있는 라이프사이클 함수가 들어 있습니다:

```lua
function init(self)
   -- 여기에 초기화 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end

function final(self)
   -- 여기에 마무리 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end

function update(self, dt)
   -- 여기에 업데이트 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end

function on_message(self, message_id, message, sender)
   -- 여기에 메세지 처리 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end

function on_input(self, action_id, action)
   -- 여기에 입력 처리 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end

function on_reload(self)
   -- 여기에 입력 처리 코드를 추가합니다
   -- 필요하지 않으면 이 함수를 제거합니다
end
```

스크립트를 GUI 컴포넌트에 첨부하려면 GUI 컴포넌트 프로토타입 파일(다른 엔진에서 "prefabs" 또는 "blueprints"라고도 부르는 것)을 열고 *Outline*에서 루트를 선택해 GUI *Properties*를 표시합니다. *Script* 프로퍼티를 스크립트 파일로 설정합니다.

![Script](images/gui-script/set_script.png)

GUI 컴포넌트가 게임 안의 어딘가에 있는 게임 오브젝트에 추가되어 있다면 이제 스크립트가 실행됩니다.

## "gui" 네임스페이스

GUI 스크립트는 `gui` 네임스페이스와 [모든 `gui` 함수](/ref/gui)에 액세스할 수 있습니다. `go` 네임스페이스는 사용할 수 없으므로 게임 오브젝트 로직은 스크립트 컴포넌트로 분리하고 GUI와 게임 오브젝트 스크립트 사이에서 통신해야 합니다. `go` 함수를 사용하려고 하면 에러가 발생합니다.

```lua
function init(self)
   local id = go.get_id()
end
```

```txt
ERROR:SCRIPT: /main/my_gui.gui_script:2: You can only access go.* functions and values from a script instance (.script file)
stack traceback:
   [C]: in function 'get_id'
   /main/my_gui.gui_script:2: in function </main/my_gui.gui_script:1>
```

## 메세지 전달

스크립트가 첨부된 모든 GUI 컴포넌트는 메세지 전달을 통해 게임 런타임 환경의 다른 오브젝트와 통신할 수 있으며, 다른 스크립트 컴포넌트처럼 동작합니다.

다른 스크립트 컴포넌트와 같은 방식으로 GUI 컴포넌트의 주소를 지정합니다.

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![메세지 전달](images/gui-script/message_passing.png)

## 노드 주소 지정

GUI 노드는 컴포넌트에 첨부된 GUI 스크립트로 조작할 수 있습니다. 각 노드에는 에디터에서 설정하는 유니크한 *Id*가 있어야 합니다.

![메세지 전달](images/gui-script/node_id.png)

*Id*를 사용하면 스크립트가 노드에 대한 참조를 가져와 [`gui` 네임스페이스 함수](/ref/gui)로 조작할 수 있습니다.

```lua
-- 체력바를 10 단위만큼 확장합니다
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## 동적으로 생성한 노드

런타임에 스크립트로 새 노드를 생성하는 방법은 두 가지입니다. 첫 번째 방법은 `gui.new_[type]_node()` 함수를 호출해 노드를 처음부터 만드는 것입니다. 이 함수들은 새 노드에 대한 참조를 반환하며, 그 참조를 사용해 노드를 조작할 수 있습니다.

```lua
-- 새 box 노드를 생성합니다
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- 새 텍스트 노드를 생성합니다
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![동적 노드](images/gui-script/dynamic_nodes.png)

새 노드를 만드는 다른 방법은 `gui.clone()` 함수로 기존 노드를 복제하거나, `gui.clone_tree()` 함수로 노드 트리를 복제하는 것입니다.

```lua
-- healthbar를 복제합니다
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- button 노드 트리를 복제합니다
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- 새 트리 루트를 가져옵니다
local new_root = new_button_nodes["my_button"]

-- 루트와 자식을 오른쪽으로 300만큼 이동합니다
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## 동적 노드 Id

동적으로 생성한 노드에는 id가 할당되지 않습니다. 이는 의도된 설계입니다. 노드에 액세스하려면 `gui.new_[type]_node()`, `gui.clone()`, `gui.clone_tree()`에서 반환된 참조만 있으면 되며, 그 참조를 추적해야 합니다.

```lua
-- 텍스트 노드를 추가합니다
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode"에는 노드에 대한 참조가 들어 있습니다.
-- 노드에는 id가 없으며, 그래도 괜찮습니다. 이미 참조가 있는데
-- gui.get_node()를 호출할 이유가 없습니다.
```
