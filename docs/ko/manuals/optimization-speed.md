---
title: Defold 게임의 런타임 성능 최적화
brief: 이 매뉴얼은 Defold 게임이 안정적으로 높은 프레임 레이트로 실행되도록 최적화하는 방법을 설명합니다.
---

# 런타임 속도 최적화
게임을 안정적으로 높은 프레임 레이트로 실행되도록 최적화하려면, 먼저 병목 지점이 어디인지 알아야 합니다. 게임의 한 프레임에서 실제로 가장 많은 시간을 차지하는 것은 무엇인가요? 렌더링인가요? 게임 로직인가요? 씬 그래프인가요? 이를 파악하려면 내장 프로파일링 도구를 사용하는 것이 좋습니다. [온스크린 또는 웹 프로파일러](/manuals/profiling/)를 사용해 게임 성능을 샘플링한 뒤, 최적화가 필요한지와 무엇을 최적화할지 결정하세요. 어떤 부분에 시간이 걸리는지 더 잘 이해하면 문제 해결을 시작할 수 있습니다.

## 스크립트 실행 시간 줄이기
프로파일러에서 `Script` 스코프의 값이 높게 나타난다면 스크립트 실행 시간을 줄여야 합니다. 일반적인 원칙으로, 매 프레임 실행하는 코드는 가능한 한 적어야 합니다. 매 프레임 `update()`와 `on_input()`에서 많은 코드를 실행하면 게임 성능에 영향을 줄 가능성이 높으며, 특히 저사양 디바이스에서 그렇습니다. 몇 가지 지침은 다음과 같습니다.

### 반응형 코드 패턴 사용하기
콜백을 받을 수 있다면 변경 사항을 폴링하지 마세요. 애니메이션이나 작업을 엔진에 맡길 수 있다면 직접 수행하지 마세요(예: 직접 애니메이션하는 대신 `go.animate)()` 사용).

### 가비지 컬렉션 줄이기
매 프레임 Lua 테이블처럼 수명이 짧은 오브젝트를 많이 만들면 결국 Lua의 가비지 컬렉터가 실행됩니다. 이때 프레임 시간에 작은 끊김이나 스파이크가 나타날 수 있습니다. 가능한 곳에서는 테이블을 재사용하고, 가능하다면 루프와 비슷한 구조 안에서 Lua 테이블을 생성하지 않도록 주의하세요.

### 메세지와 입력 동작 id를 미리 해쉬하기
메세지 처리를 많이 하거나 처리해야 할 입력 이벤트가 많다면 문자열을 미리 해쉬해 두는 것이 좋습니다. 다음 코드를 생각해 보세요.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

위 상황에서는 메세지를 받을 때마다 해쉬된 문자열이 다시 생성됩니다. 해쉬된 문자열을 한 번만 만들고, 메세지를 처리할 때 해쉬된 버전을 사용하면 이를 개선할 수 있습니다.

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### URL을 선호하고 캐쉬하기
메세지 전달이나 다른 방식으로 게임 오브젝트 또는 컴포넌트의 주소를 지정할 때는 문자열이나 해쉬 형태의 id를 제공할 수도 있고 URL을 제공할 수도 있습니다. 문자열이나 해쉬를 사용하면 내부적으로 URL로 변환됩니다. 따라서 시스템에서 가능한 최상의 성능을 얻으려면 자주 사용하는 URL을 캐쉬하는 것이 좋습니다. 다음 예를 생각해 보세요.

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- pos로 무언가 수행
```

세 경우 모두 id가 `enemy`인 게임 오브젝트의 위치를 가져옵니다. 첫 번째와 두 번째 경우에는 id(문자열 또는 해쉬)가 사용되기 전에 URL로 변환됩니다. 이는 최상의 성능을 위해 URL을 캐쉬하고 캐쉬된 버전을 사용하는 것이 더 좋다는 점을 보여줍니다.

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- pos로 무언가 수행
    end
```

## 프레임 렌더링 시간 줄이기
프로파일러에서 `Render`와 `Render Script` 스코프의 값이 높게 나타난다면 프레임 렌더링 시간을 줄여야 합니다. 프레임 렌더링 시간을 줄이려면 고려할 사항이 몇 가지 있습니다.

* 드로우 콜 줄이기 - 드로우 콜 줄이기에 대한 자세한 내용은 [이 포럼 게시물](https://forum.defold.com/t/draw-calls-and-defold/4674)을 참고하세요.
* 오버드로우 줄이기
* 쉐이더 복잡도 줄이기 - GLSL 최적화에 대해서는 [이 Khronos 글](https://www.khronos.org/opengl/wiki/GLSL_Optimizations)을 읽어 보세요. Defold에서 사용하는 기본 쉐이더(`builtins/materials`에 있음)를 수정하고 쉐이더에 `highp`가 필요하지 않은 경우 더 낮은 precision을 선택할 수도 있습니다. cross-compile된 GLSL ES 쉐이더는 부동 소수점 값에 `mediump`, 정수에 `highp`를 기본으로 사용하며, 이 기본값은 Shader 프로젝트 설정에서 변경할 수 있습니다. 변수별로 명시한 qualifier가 우선합니다. [쉐이더 precision 문서](/manuals/shader/#precision)를 참고하세요.

## 씬 그래프 복잡도 줄이기
프로파일러에서 `GameObject` 스코프, 더 구체적으로는 `UpdateTransform` 샘플의 값이 높게 나타난다면 씬 그래프 복잡도를 줄여야 합니다. 취할 수 있는 조치는 다음과 같습니다.

* 컬링 - 현재 보이지 않는 게임 오브젝트와 그 컴포넌트를 비활성화하세요. 이를 판단하는 방법은 게임의 종류에 따라 크게 달라집니다. 2D 게임에서는 사각형 영역 밖에 있는 게임 오브젝트를 항상 비활성화하는 것만으로 충분할 수 있습니다. 물리 트리거를 사용해 이를 감지하거나 오브젝트를 버켓(bucket)으로 분할할 수 있습니다. 어떤 오브젝트를 비활성화하거나 활성화할지 알게 되면 각 게임 오브젝트에 `disable` 또는 `enable` 메세지를 보내면 됩니다.

## 절두체 컬링
렌더 스크립트는 정의된 바운딩 박스(절두체) 밖에 있는 게임 오브젝트 컴포넌트의 렌더링을 자동으로 무시할 수 있습니다. Frustum Culling에 대한 자세한 내용은 [렌더링 파이프라인 매뉴얼](/manuals/render/#frustum-culling)에서 확인하세요.

# 플랫폼별 최적화

## Android Device Performance Framework
Android Dynamic Performance Framework는 게임이 Android 디바이스의 전원 및 발열 시스템과 더 직접적으로 상호작용할 수 있게 해주는 API 모음입니다. Android 시스템의 동적 동작을 모니터링하고, 디바이스가 과열되지 않는 지속 가능한 수준에서 게임 성능을 최적화할 수 있습니다. [Android Dynamic Performance Framework extension](https://defold.com/extension-adpf/)을 사용해 Android 디바이스용 Defold 게임의 성능을 모니터링하고 최적화하세요.
