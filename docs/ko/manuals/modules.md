---
title: Defold의 Lua 모듈
brief: Lua 모듈을 사용하면 프로젝트를 구조화하고 재사용 가능한 라이브러리 코드를 만들 수 있습니다. 이 매뉴얼은 Defold에서 그 방법을 설명합니다.
---

# Lua 모듈

Lua 모듈을 사용하면 프로젝트를 구조화하고 재사용 가능한 라이브러리 코드를 만들 수 있습니다. 일반적으로 프로젝트에서 중복을 피하는 것이 좋습니다. Defold에서는 Lua의 모듈 기능을 사용해 스크립트 파일 안에 다른 스크립트 파일을 포함할 수 있습니다. 이를 통해 외부 스크립트 파일에 기능과 데이터를 캡슐화하고 게임 오브젝트 및 GUI 스크립트 파일에서 재사용할 수 있습니다.

## Lua 파일 require하기

게임 프로젝트 구조 안 어딘가에 파일 확장자 ".lua"로 저장된 Lua 코드는 `require`를 사용해 스크립트 및 GUI 스크립트 파일로 로드할 수 있습니다. 새 Lua 모듈 파일을 만들려면 *Assets* 보기에서 만들려는 폴더를 마우스 오른쪽 버튼으로 클릭한 다음 <kbd>New... ▸ Lua Module</kbd>을 선택합니다. 파일에 고유한 이름을 지정하고 <kbd>Ok</kbd>를 누릅니다.

![new file](images/modules/new_name.png)

다음 코드가 "`main/anim.lua`" 파일에 추가되었다고 가정해 봅시다.

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

그러면 모든 스크립트에서 `require`로 이 파일을 로드하고 함수를 사용할 수 있습니다.

```lua
require "main.anim"

function update(self, dt)
    -- 위치 업데이트, 방향 설정 등
    ...

    -- 애니메이션 설정
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

`require` 함수는 지정된 모듈을 로드합니다. 먼저 `package.loaded` 테이블을 확인해 해당 모듈이 이미 로드되어 있는지 판단합니다. 이미 로드되어 있다면 `require`는 `package.loaded[module_name]`에 저장된 값을 반환합니다. 그렇지 않으면 로더를 통해 파일을 로드하고 평가합니다.

`require`에 전달하는 파일명 문자열의 문법은 조금 특별합니다. Lua는 파일명 문자열의 `.` 문자를 경로 구분자로 바꿉니다. macOS와 Linux에서는 `/`, Windows에서는 `\\`로 바뀝니다.

위 예제처럼 전역 범위(global scope)를 사용해 상태를 저장하고 함수를 정의하는 것은 대체로 좋지 않습니다. 이름 충돌이 생기거나 모듈의 상태가 노출되거나 모듈 사용자 사이에 커플링이 생길 위험이 있습니다.

## 모듈

Lua는 데이터와 함수를 캡슐화하기 위해 _모듈_ 을 사용합니다. Lua 모듈은 함수와 데이터를 담는 일반 Lua 테이블입니다. 전역 범위를 오염시키지 않도록 테이블은 로컬로 선언합니다.

```lua
local M = {}

-- 비공개
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

그다음 모듈을 사용할 수 있습니다. 여기서도 로컬 변수에 할당하는 것이 좋습니다.

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## 모듈 핫 리로드

간단한 모듈을 살펴봅시다.

```lua
-- module.lua
local M = {} -- 로컬 범위에 새 테이블을 생성함
M.value = 4711
return M
```

그리고 이 모듈을 사용하는 코드가 있습니다.

```lua
local m = require "module"
print(m.value) --> "4711" ("module.lua"가 변경되어 핫 리로드되어도)
```

모듈 파일을 핫 리로드하면 코드가 다시 실행되지만 `m.value`에는 아무 일도 일어나지 않습니다. 왜 그럴까요?

첫째, "module.lua"에서 만든 테이블은 로컬 범위에 생성되고, 그 테이블에 대한 _참조_ 가 사용자에게 반환됩니다. "module.lua"를 다시 로드하면 모듈 코드는 다시 평가되지만, `m`이 가리키는 테이블을 업데이트하는 대신 로컬 범위에 새 테이블을 만듭니다.

둘째, Lua는 `require`로 로드한 파일을 캐쉬합니다. 파일을 처음 require하면 이후 `require` 호출에서 더 빠르게 읽을 수 있도록 [`package.loaded`](/ref/package/#package.loaded) 테이블에 넣습니다. 파일의 항목을 `nil`로 설정하면 디스크에서 강제로 다시 읽을 수 있습니다. `package.loaded["my_module"] = nil`.

모듈을 올바르게 핫 리로드하려면 모듈을 다시 로드하고, 캐쉬를 초기화한 다음, 그 모듈을 사용하는 모든 파일도 다시 로드해야 합니다. 이는 최적과는 거리가 멉니다.

대신 _개발 중에_ 사용할 우회 방법을 고려할 수 있습니다. 모듈 테이블을 전역 범위에 두고, 파일을 평가할 때마다 새 테이블을 만들지 않고 `M`이 전역 테이블을 참조하게 하는 방법입니다. 그러면 모듈을 다시 로드할 때 전역 테이블의 내용이 변경됩니다.

```lua
--- module.lua

-- 완료되면 local M = {}로 교체하세요
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## 모듈과 상태

상태가 있는 모듈은 모듈의 모든 사용자 간에 공유되는 내부 상태를 유지하며, 싱글톤과 비교할 수 있습니다.

```lua
local M = {}

-- 모듈의 모든 사용자가 이 테이블을 공유함
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

반면 상태가 없는 모듈은 내부 상태를 유지하지 않습니다. 대신 모듈 사용자에게 로컬인 별도 테이블로 상태를 외부화하는 메커니즘을 제공합니다. 이를 구현하는 몇 가지 방법은 다음과 같습니다.

상태 테이블 사용
: 아마 가장 쉬운 접근 방식은 상태만 담은 새 테이블을 반환하는 생성자 함수를 사용하는 것입니다. 상태 테이블을 조작하는 모든 함수의 첫 번째 파라미터로 상태를 명시적으로 모듈에 전달합니다.

  ```lua
  local M = {}

  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end

  function M.get_state(the_state)
      return the_state.value
  end

  function M.new(v)
      local state = {
          value = v
      }
      return state
  end

  return M
  ```

  모듈은 다음과 같이 사용합니다.

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

메타테이블 사용
: 또 다른 접근 방식은 호출할 때마다 상태와 모듈의 공개 함수를 담은 새 테이블을 반환하는 생성자 함수를 사용하는 것입니다.

  ```lua
  local M = {}

  function M:alter_state(v)
      -- : 표기법을 사용할 때 self가 첫 번째 인자로 추가됨
      self.value = self.value + v
  end

  function M:get_state()
      return self.value
  end

  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end

  return M
  ```

  모듈은 다음과 같이 사용합니다.

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- : 표기법을 사용할 때 "my_state"가 첫 번째 인자로 추가됨
  print(my_state:get_state()) --> 43
  ```

클로저 사용
: 세 번째 방법은 모든 상태와 함수를 담은 클로저를 반환하는 것입니다. 메타테이블을 사용할 때처럼 인스턴스를 인자로 전달할 필요가 없습니다. 명시적으로 전달할 필요도, 콜론 연산자를 사용해 암시적으로 전달할 필요도 없습니다. 이 방법은 함수 호출이 `__index` 메타메서드를 거칠 필요가 없으므로 메타테이블을 사용하는 것보다 어느 정도 더 빠릅니다. 하지만 각 클로저가 메서드의 자체 복사본을 포함하므로 메모리 사용량은 더 높습니다.

  ```lua
  local M = {}

  function M.new(v)
      local state = {
          value = v
      }

      state.alter_state = function(v)
          state.value = state.value + v
      end

      state.get_state = function()
          return state.value
      end

      return state
  end

  return M
  ```

  모듈은 다음과 같이 사용합니다.

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state())
  ```
