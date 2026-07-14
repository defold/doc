---
title: Defold의 주소 지정
brief: 이 매뉴얼은 Defold가 주소 지정 문제를 어떻게 해결했는지 설명합니다.
---

# 주소 지정

실행 중인 게임을 제어하는 코드는 플레이어가 보고 듣는 것을 이동, 스케일, 애니메이션, 삭제, 조작하기 위해 모든 오브젝트와 컴포넌트에 접근할 수 있어야 합니다. Defold의 주소 지정 메커니즘은 이를 가능하게 합니다.

## 식별자

Defold는 게임 오브젝트와 컴포넌트를 참조할 때 주소(또는 URL이지만 지금은 무시하겠습니다)를 사용합니다. 이 주소는 식별자로 구성됩니다. 다음은 Defold가 주소를 사용하는 방법의 예입니다. 이 매뉴얼에서는 이것들이 어떻게 동작하는지 자세히 살펴보겠습니다.

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

아주 간단한 예제부터 시작해 보겠습니다. 단일 스프라이트 컴포넌트가 있는 게임 오브젝트가 있다고 가정해 봅시다. 이 게임 오브젝트를 제어할 스크립트 컴포넌트도 있습니다. 에디터의 구성은 다음과 비슷합니다.

![에디터의 bean](images/addressing/bean_editor.png)

이제 게임이 시작될 때 스프라이트를 비활성화해서 나중에 나타나게 만들고 싶습니다. "controller.script"에 다음 코드를 넣으면 쉽게 할 수 있습니다.

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. '#' 문자 때문에 혼란스러워도 걱정하지 마세요. 곧 설명하겠습니다.

이 코드는 예상대로 동작합니다. 게임이 시작되면 스크립트 컴포넌트는 식별자 "body"로 스프라이트 컴포넌트에 *주소를 지정*하고, 그 주소를 사용해 "disable" *메세지*를 보냅니다. 이 특수 엔진 메세지의 효과로 스프라이트 컴포넌트가 스프라이트 그래픽을 숨깁니다. 도식화하면 구성은 다음과 같습니다.

![bean](images/addressing/bean.png)

이 구성의 식별자는 개발자가 정하며, 각 이름 컨텍스트 안에서 고유해야 합니다. 여기서는 게임 오브젝트에 "bean"이라는 식별자를 주고, 스프라이트 컴포넌트에는 "body"라는 이름을, 캐릭터를 제어하는 스크립트 컴포넌트에는 "controller"라는 이름을 주었습니다. 문자열 URL 주소에 사용하는 식별자에는 `:` 또는 `#` 문자를 넣지 않아야 합니다. URL 문법에서 `:`은 소켓 구분자로, `#`은 게임 오브젝트/컴포넌트 구분자로 예약되어 있기 때문입니다. 그 외 문장 부호는 URL 파서가 거부하지 않습니다.

::: sidenote
이름을 선택하지 않으면 에디터가 선택합니다. 에디터에서 새 게임 오브젝트나 컴포넌트를 만들 때마다 고유한 *Id* 프로퍼티가 자동으로 설정됩니다.

- 게임 오브젝트는 자동으로 "go"라는 id에 번호가 붙은 이름("go2", "go3" 등)을 받습니다.
- 컴포넌트는 컴포넌트 타입에 해당하는 id("sprite", "sprite2" 등)를 받습니다.

원한다면 이렇게 자동으로 할당된 이름을 그대로 사용할 수 있지만, 식별자를 좋고 설명적인 이름으로 바꾸는 것을 권장합니다.
:::

이제 다른 스프라이트 컴포넌트를 추가하고 bean에게 방패를 줘 봅시다.

![bean](images/addressing/bean_shield_editor.png)

새 컴포넌트는 게임 오브젝트 안에서 유니크하게 식별되어야 합니다. 이 컴포넌트에 "body"라는 이름을 준다면, 스크립트 코드가 어떤 스프라이트에 "disable" 메세지를 보내야 하는지 모호해집니다. 따라서 유니크하고 설명적인 식별자인 "shield"를 선택합니다. 이제 "body"와 "shield" 스프라이트를 원하는 대로 활성화하거나 비활성화할 수 있습니다.

![bean](images/addressing/bean_shield.png)

::: sidenote
식별자를 두 번 이상 사용하려고 하면 에디터가 에러를 표시하므로 실제로는 문제가 되지 않습니다.

![bean](images/addressing/name_collision.png)
:::

이제 게임 오브젝트를 더 추가하면 어떤 일이 생기는지 살펴봅시다. 두 개의 "bean"을 작은 팀으로 묶고 싶다고 가정해 봅시다. bean 게임 오브젝트 하나는 "bean", 다른 하나는 "buddy"라고 부르기로 합니다. 또한 "bean"이 잠시 동안 대기 상태였으면 "buddy"에게 춤을 추기 시작하라고 알려야 합니다. 이는 "bean"의 "controller" 스크립트 컴포넌트에서 "buddy"의 "controller" 스크립트로 "dance"라는 커스텀 메세지를 보내서 수행합니다.

![bean](images/addressing/bean_buddy.png)

::: sidenote
각 게임 오브젝트마다 하나씩 "controller"라는 이름의 컴포넌트가 두 개 있지만, 각 게임 오브젝트가 새 이름 컨텍스트를 만들기 때문에 완전히 유효합니다.
:::

메세지의 수신자가 메세지를 보내는 게임 오브젝트("bean") 밖에 있으므로, 코드는 어떤 "controller"가 메세지를 받아야 하는지 지정해야 합니다. 타겟 게임 오브젝트 id와 컴포넌트 id를 모두 지정해야 합니다. 컴포넌트의 전체 주소는 `"buddy#controller"`가 되며, 이 주소는 두 개의 별도 부분으로 구성됩니다.

- 먼저 타겟 게임 오브젝트의 식별자("buddy")가 옵니다.
- 그 다음 게임 오브젝트/컴포넌트 구분 문자("#")가 옵니다.
- 마지막으로 타겟 컴포넌트의 식별자("controller")를 씁니다.

이전의 단일 게임 오브젝트 예제로 돌아가 보면, 타겟 주소에서 게임 오브젝트 식별자 부분을 생략하면 코드가 *현재 게임 오브젝트* 안의 컴포넌트에 주소를 지정할 수 있음을 알 수 있습니다.

예를 들어 `"#body"`는 현재 게임 오브젝트의 "body" 컴포넌트 주소를 나타냅니다. 이는 매우 유용합니다. "body" 컴포넌트가 있기만 하면 이 코드는 *어떤* 게임 오브젝트에서도 동작하기 때문입니다.

## 컬렉션

컬렉션(collection)을 사용하면 게임 오브젝트의 그룹 또는 계층구조를 만들고 제어된 방식으로 재사용할 수 있습니다. 에디터에서 게임을 컨텐츠로 채울 때 컬렉션 파일을 템플릿(또는 "프로토타입", "프리팹")으로 사용합니다.

bean/buddy 팀을 많이 만들고 싶다고 가정해 봅시다. 좋은 방법은 새 *컬렉션 파일*에 템플릿을 만드는 것입니다(이름은 "team.collection"으로 지정합니다). 컬렉션 파일 안에 팀 게임 오브젝트를 구성하고 저장합니다. 그런 다음 그 컬렉션 파일 컨텐츠의 인스턴스를 main 부트스트랩 컬렉션에 넣고, 해당 인스턴스에 식별자를 부여합니다(이름은 "team_1"로 지정합니다).

![bean](images/addressing/team_editor.png)

이 구조에서도 "bean" 게임 오브젝트는 `"buddy#controller"` 주소로 "buddy"의 "controller" 컴포넌트를 계속 참조할 수 있습니다.

![bean](images/addressing/collection_team.png)

그리고 "team.collection"의 두 번째 인스턴스를 추가해도(이름은 "team_2"로 지정합니다), "team_2" 스크립트 컴포넌트 안에서 실행되는 코드는 똑같이 잘 동작합니다. "team_2" 컬렉션의 "bean" 게임 오브젝트 인스턴스는 여전히 `"buddy#controller"` 주소로 "buddy"의 "controller" 컴포넌트에 주소를 지정할 수 있습니다.

![bean](images/addressing/teams_editor.png)

## 상대 주소 지정

`"buddy#controller"` 주소가 두 컬렉션의 게임 오브젝트 모두에서 동작하는 이유는 이 주소가 *상대* 주소이기 때문입니다. "team_1"과 "team_2" 컬렉션은 각각 새 이름 컨텍스트, 또는 "네임스페이스"를 만듭니다. Defold는 주소를 지정할 때 컬렉션이 만드는 이름 컨텍스트를 고려하여 이름 충돌을 피합니다.

![상대 id](images/addressing/relative_same.png)

- "team_1" 이름 컨텍스트 안에서는 "bean"과 "buddy" 게임 오브젝트가 유니크하게 식별됩니다.
- 마찬가지로 "team_2" 이름 컨텍스트 안에서도 "bean"과 "buddy" 게임 오브젝트가 유니크하게 식별됩니다.

상대 주소 지정은 타겟 주소를 해석할 때 현재 이름 컨텍스트를 자동으로 앞에 붙이는 방식으로 동작합니다. 이 역시 매우 유용하고 강력합니다. 코드가 포함된 게임 오브젝트 그룹을 만들고 게임 전체에서 효율적으로 재사용할 수 있기 때문입니다.

### 약칭

Defold는 완전한 URL을 지정하지 않고 메세지를 보낼 때 사용할 수 있는 두 가지 편리한 약칭을 제공합니다.

:[Shorthands](../shared/url-shorthands.md)

## 게임 오브젝트 경로

이름 지정 메커니즘을 올바르게 이해하기 위해 프로젝트를 빌드하고 실행할 때 어떤 일이 일어나는지 살펴봅시다.

1. 에디터가 부트스트랩 컬렉션("main.collection")과 그 안의 모든 컨텐츠(게임 오브젝트와 다른 컬렉션)를 읽습니다.
2. 각 정적 게임 오브젝트에 대해 컴파일러가 식별자를 만듭니다. 이 식별자는 부트스트랩 루트에서 시작해 컬렉션 계층구조를 따라 오브젝트까지 내려가는 "경로"로 만들어집니다. 각 레벨마다 '/' 문자가 추가됩니다.

위 예제의 경우 게임은 다음 4개의 게임 오브젝트와 함께 실행됩니다.

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
식별자는 해쉬된 값으로 저장됩니다. 런타임은 각 컬렉션 식별자의 해쉬 상태도 저장하며, 이는 상대 문자열을 절대 id로 이어서 해쉬하는 데 사용됩니다.
:::

런타임에는 컬렉션 그룹화가 존재하지 않습니다. 특정 게임 오브젝트가 컴파일 전에 어떤 컬렉션에 속했는지 알아낼 방법은 없습니다. 컬렉션 안의 모든 오브젝트를 한 번에 조작하는 것도 불가능합니다. 이러한 작업이 필요하다면 코드에서 직접 쉽게 추적할 수 있습니다. 각 오브젝트의 식별자는 정적이며, 오브젝트의 수명 동안 고정되어 있음이 보장됩니다. 이는 오브젝트의 식별자를 안전하게 저장했다가 나중에 사용할 수 있음을 의미합니다.

## 절대 주소 지정

주소를 지정할 때 위에서 설명한 전체 식별자를 사용할 수 있습니다. 대부분의 경우 컨텐츠 재사용이 가능하므로 상대 주소 지정이 선호되지만, 절대 주소 지정이 필요한 경우도 있습니다.

예를 들어 각 bean 오브젝트의 상태를 추적하는 AI 매니저가 필요하다고 가정해 봅시다. bean들이 자신의 활성 상태를 매니저에게 보고하고, 매니저는 그 상태를 바탕으로 전술적 결정을 내리고 bean들에게 명령을 내리게 하고 싶습니다. 이 경우에는 스크립트 컴포넌트가 있는 단일 manager 게임 오브젝트를 만들고, 부트스트랩 컬렉션에서 팀 컬렉션 옆에 배치하는 것이 적절합니다.

![manager 오브젝트](images/addressing/manager_editor.png)

이제 각 bean은 상태 메세지를 매니저에게 보낼 책임이 있습니다. 적을 발견하면 "contact", 맞아서 피해를 받으면 "ouch!"를 보냅니다. 이것이 동작하려면 bean controller 스크립트가 절대 주소 지정을 사용해 "manager"의 "controller" 컴포넌트로 메세지를 보내야 합니다.

'/'로 시작하는 모든 주소는 게임 월드의 루트에서부터 해석됩니다. 이는 게임 시작 시 로드되는 *부트스트랩 컬렉션*의 루트에 해당합니다.

manager 스크립트의 절대 주소는 `"/manager#controller"`이며, 이 절대 주소는 어디에서 사용하든 올바른 컴포넌트로 해석됩니다.

![팀과 manager](images/addressing/teams_manager.png)

![절대 주소 지정](images/addressing/absolute.png)

## 해쉬된 식별자

엔진은 모든 식별자를 해쉬된 값으로 저장합니다. 컴포넌트나 게임 오브젝트를 인자로 받는 모든 함수는 문자열, 해쉬 또는 URL 오브젝트를 받습니다. 위에서는 주소 지정에 문자열을 사용하는 방법을 살펴보았습니다.

게임 오브젝트의 식별자를 가져오면 엔진은 항상 해쉬된 절대 경로 식별자를 반환합니다.

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

이러한 식별자를 문자열 id 대신 사용할 수도 있고, 직접 만들 수도 있습니다. 하지만 해쉬된 id는 오브젝트의 경로, 즉 절대 주소에 해당한다는 점에 유의하세요.

::: sidenote
상대 주소를 문자열로 제공해야 하는 이유는 엔진이 현재 이름 컨텍스트(컬렉션)의 해쉬 상태에 주어진 문자열을 더해 새 해쉬 id를 계산하기 때문입니다.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- 이 코드는 동작하지 않습니다! 상대 주소는 문자열로 제공해야 합니다.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL {#urls}

전체 그림을 완성하기 위해 Defold 주소의 전체 형식인 URL을 살펴봅시다.

URL은 오브젝트이며, 보통 특수한 형식의 문자열로 작성합니다. 일반적인 URL은 세 부분으로 구성됩니다.

`[socket:][path][#fragment]`

socket
: 타겟의 게임 월드를 식별합니다. 이는 [컬렉션 프록시](/manuals/collection-proxy)로 작업할 때 중요하며, 이때 _동적으로 로드된 컬렉션_을 식별하는 데 사용됩니다.

path
: URL의 이 부분에는 타겟 게임 오브젝트의 전체 id가 들어 있습니다.

fragment
: 지정된 게임 오브젝트 안의 타겟 컴포넌트 식별자입니다.

위에서 보았듯이 대부분의 경우 이 정보의 일부 또는 대부분을 생략할 수 있습니다. socket을 지정해야 하는 경우는 거의 없으며, path는 자주 지정해야 하지만 항상 그런 것은 아닙니다. 다른 게임 월드 안의 대상에 주소를 지정해야 하는 경우에는 URL의 socket 부분을 지정해야 합니다. 예를 들어 위의 "manager" 게임 오브젝트에 있는 "controller" 스크립트의 전체 URL 문자열은 다음과 같습니다.

`"main:/manager#controller"`

그리고 team_2의 buddy controller는 다음과 같습니다.

`"main:/team_2/buddy#controller"`

이들에게 메세지를 보낼 수 있습니다.

```lua
-- manager 스크립트와 팀 buddy bean에 "hello"를 보냅니다.
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## URL 오브젝트 만들기

URL 오브젝트는 Lua 코드에서 프로그래밍 방식으로 만들 수도 있습니다.

```lua
-- 문자열에서 URL 오브젝트를 만듭니다.
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- 파라미터에서 URL을 만듭니다.
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- 빈 URL 오브젝트에서 구성합니다.
local my_url = msg.url()
my_url.socket = "main" -- 유효한 이름으로 지정합니다.
my_url.path = hash("/manager") -- 문자열 또는 해쉬로 지정합니다.
my_url.fragment = "controller" -- 문자열 또는 해쉬로 지정합니다.

-- URL로 지정한 타겟에 게시합니다.
msg.post(my_url, "hello_manager!")
```
