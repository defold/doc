---
title: 컬렉션 프록시 매뉴얼
brief: 이 매뉴얼은 새 게임 월드를 동적으로 만들고 전환하는 방법을 설명합니다.
---

# 컬렉션 프록시

컬렉션 프록시(Collection proxy) 컴포넌트는 컬렉션 파일의 컨텐츠를 기반으로 새 게임 "월드"를 동적으로 로드하고 언로드하는 데 사용됩니다. 게임 레벨 전환, GUI 화면 전환, 레벨 전체에서 서사적인 "씬" 로드 및 언로드, 미니게임 로드 및 언로드 등에 사용할 수 있습니다.

Defold는 모든 게임 오브젝트를 컬렉션 안에 구성합니다. 컬렉션은 게임 오브젝트와 다른 컬렉션(즉, 서브-컬렉션)을 포함할 수 있습니다. 컬렉션 프록시를 사용하면 컨텐츠를 별도 컬렉션으로 나누고, 스크립트를 통해 이 컬렉션들의 로드와 언로드를 동적으로 관리할 수 있습니다.

컬렉션 프록시는 [컬렉션 팩토리 컴포넌트](/manuals/collection-factory/)와 다릅니다. 컬렉션 팩토리는 컬렉션의 컨텐츠를 현재 게임 월드 안에 인스턴스화합니다. 컬렉션 프록시는 런타임에 새 게임 월드를 만들기 때문에 용도가 다릅니다.

## 컬렉션 프록시 컴포넌트 생성하기

1. 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 컨텍스트 메뉴에서 <kbd>Add Component ▸ Collection Proxy</kbd>를 선택하여 게임 오브젝트에 컬렉션 프록시 컴포넌트를 추가합니다.

2. *Collection* 프로퍼티를 나중에 런타임에 동적으로 로드하려는 컬렉션을 참조하도록 설정합니다. 이 참조는 정적이며, 참조된 컬렉션의 모든 컨텐츠가 최종 게임에 포함되도록 보장합니다.

![프록시 컴포넌트 추가](images/collection-proxy/create_proxy.png)

(*Exclude* 박스를 체크하고 [Live update 기능](/manuals/live-update/)을 사용하면 빌드에서 컨텐츠를 제외하고 대신 코드로 다운로드할 수 있습니다.)

## 부트스트랩

Defold 엔진이 시작되면 *부트스트랩 컬렉션*의 모든 게임 오브젝트를 런타임에 로드하고 인스턴스화합니다. 그런 다음 게임 오브젝트와 그 컴포넌트를 초기화하고 활성화합니다. 엔진이 어떤 부트스트랩 컬렉션을 사용할지는 [프로젝트 설정](/manuals/project-settings/#main-collection)에서 설정합니다. 관례상 이 컬렉션 파일의 이름은 보통 "main.collection"입니다.

![부트스트랩](images/collection-proxy/bootstrap.png)

엔진은 부트스트랩 컬렉션의 컨텐츠가 인스턴스화될 전체 "게임 월드"에 필요한 메모리를 할당하여 게임 오브젝트와 그 컴포넌트를 담을 수 있게 합니다. 충돌 오브젝트와 물리 시뮬레이션을 위한 별도의 물리 월드도 생성됩니다.

스크립트 컴포넌트는 부트스트랩 월드 밖에서도 게임의 모든 오브젝트에 주소를 지정할 수 있어야 하므로, 월드에는 고유한 이름이 부여됩니다. 이 이름은 컬렉션 파일에서 설정하는 *Name* 프로퍼티입니다.

![부트스트랩](images/collection-proxy/collection_id.png)

로드되는 컬렉션에 컬렉션 프록시 컴포넌트가 포함되어 있더라도, 그 프록시가 참조하는 컬렉션은 자동으로 로드되지 *않습니다*. 이러한 리소스의 로드는 스크립트로 제어해야 합니다.

## 컬렉션 로드하기

프록시를 통해 컬렉션을 동적으로 로드하려면 스크립트에서 프록시 컴포넌트로 `"load"`라는 메세지를 보냅니다.

```lua
-- "myproxy" 프록시에 로드를 시작하라고 알립니다.
msg.post("#myproxy", "load")
```

![로드](images/collection-proxy/proxy_load.png)

프록시 컴포넌트는 엔진에 새 월드를 위한 공간을 할당하도록 지시합니다. 별도의 런타임 물리 월드도 생성되고, "`mylevel.collection`" 컬렉션 안의 모든 게임 오브젝트가 인스턴스화됩니다.

새 월드는 컬렉션 파일의 *Name* 프로퍼티에서 이름을 가져옵니다. 이 예제에서는 "`mylevel`"로 설정되어 있습니다. 이름은 고유해야 합니다. 컬렉션 파일에 설정된 *Name*이 이미 로드된 월드에서 사용 중이면 엔진은 이름 충돌 오류를 알립니다.

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

엔진이 컬렉션 로드를 마치면 컬렉션 프록시 컴포넌트는 `"load"` 메세지를 보낸 스크립트로 `"proxy_loaded"`라는 메세지를 다시 보냅니다. 그러면 스크립트는 이 메세지에 반응해 컬렉션을 초기화하고 활성화할 수 있습니다.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- 새 월드가 로드되었습니다. 초기화하고 활성화합니다.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: 이 메세지는 컬렉션 프록시 컴포넌트에 자신의 컬렉션을 새 월드로 로드하기 시작하라고 알립니다. 프록시는 작업이 끝나면 `"proxy_loaded"`라는 메세지를 다시 보냅니다.

`"async_load"`
: 이 메세지는 컬렉션 프록시 컴포넌트에 자신의 컬렉션을 새 월드로 백그라운드 로드하기 시작하라고 알립니다. 프록시는 작업이 끝나면 `"proxy_loaded"`라는 메세지를 다시 보냅니다.

`"init"`
: 이 메세지는 인스턴스화된 모든 게임 오브젝트와 컴포넌트를 초기화해야 한다고 컬렉션 프록시 컴포넌트에 알립니다. 이 단계에서 모든 스크립트의 `init()` 함수가 호출됩니다.

`"enable"`
: 이 메세지는 모든 게임 오브젝트와 컴포넌트를 활성화해야 한다고 컬렉션 프록시 컴포넌트에 알립니다. 예를 들어 모든 스프라이트 컴포넌트는 활성화되면 그리기를 시작합니다.

## 새 월드에 주소 지정하기

컬렉션 파일 프로퍼티에 설정된 *Name*은 로드된 월드 안의 게임 오브젝트와 컴포넌트에 주소를 지정하는 데 사용됩니다. 예를 들어 부트스트랩 컬렉션에 loader 오브젝트를 만든 경우, 로드된 어떤 컬렉션에서든 이 오브젝트와 통신해야 할 수 있습니다.

```lua
-- loader에게 다음 레벨을 로드하라고 알립니다.
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![로드](images/collection-proxy/message_passing.png)

그리고 loader에서 로드된 컬렉션 안의 게임 오브젝트와 통신해야 한다면 [오브젝트의 전체 URL](/manuals/addressing/#urls)을 사용해 메세지를 보낼 수 있습니다.

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
컬렉션 밖에서 로드된 컬렉션 안의 게임 오브젝트에 직접 액세스할 수는 없습니다.

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## 월드 언로드하기

로드된 컬렉션을 언로드하려면 로드 단계와 반대되는 단계에 해당하는 메세지를 보냅니다.

```lua
-- 레벨 언로드
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: 이 메세지는 월드 안의 모든 게임 오브젝트와 컴포넌트를 비활성화하라고 컬렉션 프록시 컴포넌트에 알립니다. 이 단계에서 스프라이트는 렌더링을 멈춥니다.

`"final"`
: 이 메세지는 월드 안의 모든 게임 오브젝트와 컴포넌트를 마무리하라고 컬렉션 프록시 컴포넌트에 알립니다. 이 단계에서 모든 스크립트의 `final()` 함수가 호출됩니다.

`"unload"`
: 이 메세지는 컬렉션 프록시에 월드를 메모리에서 완전히 제거하라고 알립니다.

더 세밀한 제어가 필요하지 않다면 컬렉션을 먼저 비활성화하고 마무리하지 않고 `"unload"` 메세지를 바로 보낼 수 있습니다. 그러면 프록시는 컬렉션이 언로드되기 전에 자동으로 컬렉션을 비활성화하고 마무리합니다.

컬렉션 프록시가 컬렉션 언로드를 마치면 `"unload"` 메세지를 보낸 스크립트로 `"proxy_unloaded"` 메세지를 다시 보냅니다.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- 좋습니다. 월드가 언로드되었습니다...
        ...
    end
end
```


## 타임스텝

컬렉션 프록시 업데이트는 _타임스텝(time step)_을 변경하여 스케일할 수 있습니다. 즉 게임이 안정적으로 60 FPS로 틱하더라도 프록시는 더 빠르거나 느린 속도로 업데이트될 수 있으며, 다음과 같은 항목에 영향을 줍니다.

* 물리 시뮬레이션 속도
* `update()`에 전달되는 `dt`
* [게임 오브젝트 및 GUI 프로퍼티 애니메이션](https://defold.com/manuals/animation/#property-animation-1)
* [플립북 애니메이션](https://defold.com/manuals/animation/#flip-book-animation)
* [Particle FX 시뮬레이션](https://defold.com/manuals/particlefx/)
* 타이머 속도

업데이트 모드도 설정할 수 있으며, 이를 통해 스케일링을 불연속적으로 수행할지(스케일 팩터가 1.0보다 작을 때만 의미가 있습니다) 또는 연속적으로 수행할지 제어할 수 있습니다.

프록시에 `set_time_step` 메세지를 보내 스케일 팩터와 스케일링 모드를 제어합니다.

```lua
-- 로드된 월드를 1/5 속도로 업데이트합니다.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

타임스텝을 변경할 때 어떤 일이 일어나는지 확인하려면, 스크립트 컴포넌트에 다음 코드가 있는 오브젝트를 만들고 타임스텝을 변경할 컬렉션 안에 넣습니다.

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

타임스텝이 0.2이면 콘솔에 다음 결과가 나타납니다.

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()`는 여전히 초당 60번 호출되지만 `dt` 값이 바뀝니다. `update()` 호출 중 1/5(0.2)만 1/60(60 FPS에 해당)의 `dt`를 가지고, 나머지는 0입니다. 모든 물리 시뮬레이션도 해당 `dt`에 따라 업데이트되므로 프레임 다섯 개 중 하나에서만 진행됩니다.

::: sidenote
예를 들어 팝업을 표시하는 동안이나 창이 포커스를 잃었을 때 컬렉션 타임스텝 기능을 사용해 게임을 일시정지할 수 있습니다. 일시정지하려면 `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})`을 사용하고, 재개하려면 `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})`을 사용합니다.
:::

자세한 내용은 [`set_time_step`](/ref/collectionproxy#set_time_step)을 참고하세요.

## 주의사항과 일반적인 문제

Physics
: 컬렉션 프록시를 통해 둘 이상의 최상위 컬렉션, 즉 *게임 월드*를 엔진에 로드할 수 있습니다. 이때 각 최상위 컬렉션은 별도의 물리 월드라는 점을 알아야 합니다. 물리 상호작용(충돌, 트리거, ray-cast)은 같은 월드에 속한 오브젝트 사이에서만 발생합니다. 따라서 두 월드의 충돌 오브젝트가 시각적으로 정확히 겹쳐 있더라도, 둘 사이에는 물리 상호작용이 일어날 수 없습니다.

Memory
: 로드된 각 컬렉션은 새 게임 월드를 만들며, 이 월드는 비교적 큰 메모리 사용량을 동반합니다. 프록시를 통해 수십 개의 컬렉션을 동시에 로드한다면 설계를 다시 검토하는 것이 좋습니다. 게임 오브젝트 계층구조의 인스턴스를 많이 스폰하려면 [컬렉션 팩토리](/manuals/collection-factory)가 더 적합합니다.

Input
: 로드된 컬렉션 안에 입력 동작이 필요한 오브젝트가 있다면, 컬렉션 프록시가 들어 있는 게임 오브젝트가 입력을 획득하도록 해야 합니다. 게임 오브젝트가 입력 메세지를 받으면 이 메세지는 해당 오브젝트의 컴포넌트, 즉 컬렉션 프록시로 전파됩니다. 입력 동작은 프록시를 통해 로드된 컬렉션으로 전달됩니다.
