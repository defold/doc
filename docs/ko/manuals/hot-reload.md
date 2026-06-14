---
title: 핫 리로드
brief: 이 매뉴얼은 Defold의 핫 리로드 기능을 설명합니다.
---

# 리소스 핫 리로드

Defold에서는 리소스를 핫 리로드할 수 있습니다. 게임을 개발할 때 이 기능은 특정 작업 속도를 크게 높여 줍니다. 실행 중인 게임의 코드와 컨텐츠를 변경할 수 있습니다. 일반적인 사용 사례는 다음과 같습니다:

- Lua 스크립트의 게임플레이 파라미터를 조정합니다.
- 파티클 효과나 GUI 요소 같은 그래픽 요소를 편집하고 조정한 뒤, 적절한 컨텍스트에서 결과를 확인합니다.
- 쉐이더 코드를 편집하고 조정한 뒤, 적절한 컨텍스트에서 결과를 확인합니다.
- 게임을 멈추지 않고 레벨을 다시 시작하거나 상태를 설정하는 등 게임 테스트를 더 쉽게 합니다.

## 핫 리로드하는 방법

에디터에서 게임을 시작합니다(<kbd>Project ▸ Build</kbd>).

업데이트된 리소스를 다시 로드하려면 메뉴 항목 <kbd>File ▸ Hot Reload</kbd>를 선택하거나 키보드의 해당 단축키를 누르면 됩니다:

![리소스 다시 로드](images/hot-reload/menu.png)

## 기기에서 핫 리로드

핫 리로드는 데스크톱뿐 아니라 기기에서도 동작합니다. 기기에서 사용하려면 모바일 기기에서 게임의 디버그 빌드나 [개발용 앱](/manuals/dev-app)을 실행한 다음, 에디터에서 해당 기기를 타겟으로 선택합니다:

![타겟 기기](images/hot-reload/target.png)

이제 빌드하고 실행하면 에디터가 모든 에셋을 기기에서 실행 중인 앱으로 업로드하고 게임을 시작합니다. 이후부터 핫 리로드하는 모든 파일은 기기에서도 업데이트됩니다.

예를 들어 휴대폰에서 실행 중인 게임에 표시되고 있는 GUI에 버튼 몇 개를 추가하려면, GUI 파일을 열면 됩니다:

![GUI 리로드](images/hot-reload/gui.png)

새 버튼을 추가하고 저장한 뒤 GUI 파일을 핫 리로드합니다. 이제 휴대폰 화면에서 새 버튼을 볼 수 있습니다:

![리로드된 GUI](images/hot-reload/gui-reloaded.png)

파일을 핫 리로드하면 엔진은 다시 로드된 각 리소스 파일을 콘솔에 출력합니다.

## 스크립트 리로드

핫 리로드된 Lua 스크립트 파일은 실행 중인 Lua 환경에서 다시 실행됩니다.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

`my_value`를 11로 변경하고 파일을 핫 리로드하면 즉시 효과가 반영됩니다:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

핫 리로드는 라이프사이클 함수의 실행을 변경하지 않습니다. 예를 들어 핫 리로드 시 `init()`은 호출되지 않습니다. 하지만 라이프사이클 함수를 재정의하면 새 버전이 사용됩니다.

## Lua 모듈 리로드

모듈 파일에서 전역 범위에 변수를 추가하는 한, 파일을 다시 로드하면 이러한 전역 변수가 변경됩니다:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- "my_module.lua"를 핫 리로드하면 새 값이 출력됩니다
end
```

일반적인 Lua 모듈 패턴은 로컬 테이블을 만들고 값을 채운 다음 반환하는 방식입니다:

```lua
--- my_module.lua
local M = {} -- 여기서 새 테이블 오브젝트가 생성됩니다
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- "my_module.lua"를 변경하고 핫 리로드해도 10이 출력됩니다
end
```

"my_module.lua"를 변경하고 다시 로드해도 "user.script"의 동작은 변경되지 _않습니다_. 왜 그런지와 이 함정을 피하는 방법은 [모듈 매뉴얼](/manuals/modules)을 참고하세요.

## `on_reload()` 함수

모든 스크립트 컴포넌트는 `on_reload()` 함수를 정의할 수 있습니다. 이 함수가 있으면 스크립트가 리로드될 때마다 호출됩니다. 데이터 검사나 변경, 메세지 보내기 등에 유용합니다:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## 쉐이더 코드 리로드

버텍스 쉐이더와 프래그먼트 쉐이더를 리로드하면 GLSL 코드는 그래픽 드라이버에 의해 다시 컴파일되고 GPU에 업로드됩니다. GLSL은 매우 낮은 수준에서 작성되므로 쉐이더 코드가 크래시를 일으키기 쉽고, 그렇게 되면 엔진도 함께 종료됩니다.
