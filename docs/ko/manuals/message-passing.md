# Message passing
메세지 전달은 오브젝트간 종속성을 만들지 않으면서 통신할 수 있도록 하는 Defold의 메커니즘입니다. 이 매뉴얼은 이 메커니즘에 대해 자세히 설명하며 **게임오브젝트, 컴포넌트, 컬렉션**에 대한 기본 지식이 있다고 가정하고 설명하도록 하겠습니다.

프로그래밍에서 오브젝트나 코드모듈, 컴포넌트간의 [결합](http://ko.wikipedia.org/wiki/결합도)(coupling)을 가능한 느슨하게 만드는 것은 일반적으로 아주 좋은 방법입니다. 다른 오브젝트의 내부동작에 의존하는 오브젝트는 단단히 결합된 것으로 간주되며 이 결합은 종종 코드를 수정하기 어렵게 만들고 추적하기 매우 어려운 버그를 발생시키기도 합니다. 

Defold의 Lua 통합(integration)은 Java, C++, C# 같이 상속을 사용한 클래스 구조로 어플리케이션을 개발하듯이 객체지향을 제공하지는 않습니다. 대신 Defold는 아래와 같이 간단하고 강력한 객체 지향 설계로 Lua의 기능을 확장합니다:

* 오브젝트간 통신을 위한 [메세지 전달(Message passing)](/manuals/message-passing)
* 모든 오브젝트는 자체적인 내부 상태와 제어 가능한 자체 메모리를 가짐. "self" 참조를 통해서 가능함
* 기존 오브젝트에 메세지를 보낼 수 있으며, 메세지에 어떻게 응답할지는 코드에 따라 다름. on_message() 함수를 통해 메시지를 받을 수 있으며 특정 메세지를 처리하는 코드가 없으면 아무 일도 일어나지 않음

## Addressing and URLs
Defold의 모든 오브젝트는 URL(Uniform Resource Locator)을 통해 고유한 주소가 지정됩니다. 이 주소는 컴파일시에 설정되며 오브젝트의 수명이 지속되는 동안 유지됩니다. 즉 오브젝트에 주소를 지정하면 오브젝트가 존재하는 동안은 유효한 상태로 유지되므로 저장된 오브젝트의 참조를 업데이트 하는 것에 대해 걱정할 필요가 없습니다.

프로젝트를 구성할 때, 게임 오브젝트를 컬렉션 계층에 추가하면 아주 심플한 구조로 최상위 컬렉션 바로 아래에 게임 오브젝트들이 나열됩니다.  하지만 때로는 좀 더 다양하게 오브젝트들을 그룹화 할 필요가 있습니다. 예를 들어 다음과 같은 게임이 있다고 가정해 봅시다:

* 영웅 캐릭터와 적 캐릭터를 포함하는 레벨 컬렉션
* 그리고 온-스크린(on-screen) 인터페이스

여기에 이를 위한 일반적인 구조가 있습니다:

![Message passing structure](images/message_passing/message_passing_structure.png)

이 게임의 구성은:

* id가 "main"과 "level"인  두 개의 컬렉션 . "level"은 "main" 안에 있음
* id가 "hero"와 "enemy"와 "interface"인 세 개의 게임 오브젝트
* "interface"는 "main" 안에 있음
* "hero"와 "enemy"는 "level" 안에 있음
* 예제의 각 게임 오브젝트는 두 개의 컴포넌트를 포함하고 있음
    * "hero"와 "enemy" 게임 오브젝트는 "brain"이라는 스크립트 컴포넌트와 "body"라는 스프라이트 컴포넌트를 포함하고 있음
    * "interface" 게임 오브젝트는 "control"이라는 스크립트 컴포넌트와 "gui"라는 GUI컴포넌트를 포함하고 있음
    * "interface"의 "gui"컴포넌트는 GUI스크립트가 첨부되어 있음

게임 컨텐츠 중 일부는 프로젝트의 특정 파일에 저장됩니다. 예를 들어, 컬렉션은 항상 파일에 저장되므로 "main" 컬렉션과 "level"컬렉션 파일이 적어도 한 개씩은 필요합니다. 그러나 이것은 별로 중요하지 않습니다. 중요한 것은 파일의 이름과 프로젝트 폴더에서의 파일 위치는 전혀 관련이 없다는 것을 깨닫는 것이 더 중요합니다. 주소 지정을 위해 중요한 두 가지 사항이 있습니다:

1. id를 무엇으로 지었는가
2. 어떤 컬렉션에 넣었는가

게임 오브젝트 혹은 컬렉션을 배치하면 Defold 에디터는 현재 컬렉션에서 고유한 아이디를 자동으로 지정합니다. 이 이름은 원하는 대로 수정할 수 있습니다. 에디터는 id를 추적해서 이름이 충돌하지 않는지 확인합니다. 만약 강제로 이름 충돌을 나게 하면 Defold 에디터는 에러를 발생합니다.

모든 주소들은 게임 실행중의 각 메세지 발신자와 수신자를 고유하게 식별하는 **URL**로 표현할 수 있습니다. URL은 3개의 컴포넌트로 구성되어 있으며 일반적으로 다음과 같은 형식으로 쓸 수 있습니다:

```lua
"[socket:][path][#fragment]"
```

대부분의 경우에 이러한 URL 컴포넌트는 게임 오브젝트나 컴포넌트를 지명하는데 사용되긴 하지만 이 형식은 일반적입니다.

#### socket
발신자 혹은 수신자가 존재하는 "world"를 식별합니다. 이는 [컬렉션 프록시(Collection proxy)](/manuals/collection-proxy)를 사용하는데 매우 중요하며 동적으로 불러운 컬렉션을 식별하는데 사용됩니다.

#### path
URL의 이 부분은 일반적으로 타겟 게임 오브젝트의 전체 id를 포함합니다.

#### fragment
지정된 게임 오브젝트 내의 타겟 컴포넌트의 id입니다. 

위에서 "hero" 게임 오브젝트의 스크립트에 대한 전체 URL은 아래와 같습니다:

```lua
main:/level/hero#brain
```

그리고 아래 방법으로 메세지를 보낼 수 있습니다:

```lua
-- "enemy"의 스크립트로 "hello" 메세지를 보냄
msg.post("main:/level/enemy#brain", "hello")
```

알 수 없는 수신자에게 메세지를 보내면, Defold는 콘솔창에 에러를 출력합니다.

    ERROR:GAMEOBJECT: Instance '/level/enemy' could not be found when dispatching message 'hello' sent from default:/level/hero#brain

대부분의 경우엔 위 처럼 전체 URL을 사용하는 것은 불필요하며 너무 구체적입니다. 대신에 샘플 게임을 통해 어떻게 메세지를 써야 하는지에 대해 약 3가지의 일반적인 예제를 살펴 보도록 하겠습니다:

![Message passing](images/message_passing/message_passing.png)

#### Message 1
"knock" 메세지가 "hero" 스크립트 컴포넌트로부터 "enemy" 스크립트 컴포넌트로 전송됩니다. 이 두 오브젝트가 컬렉션 계층구조상 동일한 위치에 있다면 URL의 socket 부분("world", root, main collection 등등)도 동일하므로 이 부분을 생략해서 아래와 같이 쓸 수 있습니다:

```lua
-- "hero"의 스크립트 컴포넌트로부터 "enemy"의 스크립트 컴포넌트로 "knock" 전송하기
msg.post("/level/enemy#brain", "knock")
```

URL의 socket부분을 지정하지 않으면, 이 메세지는 발신자가 동일한 socket의 수신자에게 전송되는 것으로 간주됩니다. Defold는 URL의 path 부분에서도 id의 일부를 생략 할 수 있습니다. "/"로 시작하는 path는 절대경로이며 항상 socket(일반적으로 main collection)의 root에서부터 시작되어 오브젝트의 id가 나타날 때 까지 완전히 계층적인 전체 경로(path)로 써야 합니다. "hero"와 "enemy"의 id가 각각 "/level/hero"와 "/level/enemy" 이기 때문에 "/level"을 생략하여 상대적 혹은 부분적인 id를 쓸 수 있습니다:

```lua
-- "hero"의 스크립트 컴포넌트로부터 "enemy"의 스크립트 컴포넌트로 "knock" 전송하기
msg.post("enemy#brain", "knock")
```

앞부분에 "/"를 사용하여 "/enemy#brain" 처럼 쓰지 않도록 주의 바랍니다. 맨 앞에 "/"를 추가하면 "main" 컬렉션의 root에서 "enemy"라는 게임 오브젝트를 찾아보려 하겠지만 root에 이런 오브젝트는 존재하지 않습니다. 자, 이제는 URL의 fragment 부분을 생략하면 무슨일이 발생할까요?


```lua
-- "hero"의 스크립트 컴포넌트로부터 "enemy"로 "knock" 전송하기
msg.post("enemy", "knock")
```

이것은 완벽히 유효합니다. 목적지 컴포넌트의 이름을 생략하면 이 메세지는 해당 게임 오브젝트에 있는 모든 컴포넌트들에게 브로드캐스트 됩니다. 브로드캐스팅은 성능을 떨어뜨리며 불명확성으로 인해 버그를 유발할 수도 있으므로 컴포넌트의 이름을 명확하게 지정하는 것을 권장합니다.

#### Message 2
"increase_score" 메세지는 "hero" 게임 오브젝트의 스크립트 컴포넌트로부터 "interface" 게임 오브젝트의 스크립트 컴포넌트로 전송됩니다.

```lua
-- "hero"의 스크립트 컴포넌트로부터 "interface"의 스크립트 컴포넌트로 "increase_score"를 보냄
msg.post("/interface#controller", "increase_score")
```

위 케이스에서는 상대(relative)경로의 id를 쓸 수 없습니다. "hero"의 관점에서 볼 때 절대(absolute)적이고 완전한 full id("../interface" 처럼 파일 시스템 같은 표기법은 허용되지 않으므로)를 사용해야 합니다. 그러나 "interface"의 스크립트 쪽에서 메세지를 보내는 경우라면 상대경로도 가능합니다:

```lua
-- "interface"의 스크립트 컴포넌트로부터 "hero"의 스크립트로 "increase_score_response"를 보냄
msg.post("level/hero#brain", "increase_score_response")
```

다시 말하지만, 앞쪽의 "/"가 생략된 것에 주목하십시오. 상대경로의 id를 사용하면 발신자와 수신자는 컬렉션 계층의 모든 위치에서 통신할 수 있습니다. 이 방법은 오브젝트나 오브젝트 계층을 여러번 인스턴스화 하거나 동적으로 스폰할 필요가 있을 때 매우 유용합니다.

#### Message 3
"update_minimap" 메세지는 "enemy" 게임 오브젝트로부터 "interface" 게임오브젝트의 "gui" 스크립트로 전송됩니다.

```lua
-- "enemy"의 스크립트 컴포넌트에서 "interface"의 GUI 스크립트로 "update_minimap"를 전송함
msg.post("/interface#gui", "update_minimap")
```

여기는 상대경로로 URL을 쓸 수 없는 또 다른 케이스입니다. 대신 "interface" 오브젝트의 full id를 써서 이 메세지를 "gui" 컴포넌트로 보내야 합니다. 스크립트와 GUI컴포넌트는 Lua스크립트와 관련된 유일한 게임 오브젝트 컴포넌트이며 임의의 메세지에 반응할 수 있습니다. GUI스크립트는 GUI씬에만 추가되어야 하는것을 기억하세요. GUI스크립트와 다른 스크립트간의 메세지 송수신은 다른 오브젝트간 송수신 방식과 완전히 동일하게 동작합니다.

###### Shorthands (약칭)
우리는 메세지를 작성할 때 URL에서 불필요한 정보는 생략하는것이 어떻게 가능한지 살펴봤습니다. 추가적으로 Defold는 두 가지 편리한 약칭을 제공합니다:

**"."**
현재 게임 오브젝트를 가리키는 URL 약칭

**"#"**
현재 스크립트를 가리키는 URL 약칭

예를 들어:

```lua
-- 이 게임오브젝트가 입력 포커스를 얻도록 하자
msg.post(".", "acquire_input_focus")
```

```lua
-- 이 스크립트로 "reset" 메세지를 보냄
msg.post("#", "reset")
```

## A concrete example (구체적인 예제)
간단한 예제를 살펴봅시다. 당신의 게임에 스탯(체력, 점수, 별점 보너스 등) 같이 화면에 보여야할 요소들이 있는 HUD가 있으며, 이 HUD는 "hud"라는 게임 오브젝트로 제어된다고 가정해 봅시다.

![HUD](images/message_passing/HUD.png)

우리는 체력을 증감 시킬 수 있으며 이 작업을 "hud" 오브젝트의 스크립트 컴포넌트로 메세지를 보내서 수행합니다:

```lua
msg.post("hud#script", "increase_health")
```

이렇게 하면 id (혹은 name)이 "increase_health"인 메세지를 "hud" 오브젝트의 "script"라는 수신자 컴포넌트로 게시(post)하게 됩니다. Defold는 다음번 메세지가 발송(dispatch)되면 메세지를 배달하며, 이는 현재 프레임 내에서 발생합니다.

다음으로 메세지를 응답 받으면 멋진 방식으로 점수가 증가하는 코드를 작성하여 "hud" 게임 오브젝트에 추가합니다.

```lua
-- file: hud.script

function on_message(self, message_id, message, sender)
    if message_id == hash("increase_health") then
        -- 하트 1개를 삐까뻔쩍한 애니메이션으로 HUD에 추가해 보자.
        …
    end
end
```

## Message data
msg.post()의 함수 형태는 다음과 같습니다.

```lua
msg.post(receiver, message_id[, message])
```

우리는 편의상 HUD의 모든 정보를 한번에 셋팅할 수 있는 한 개의 메세지를 추가해 보도록 하겠습니다. 메세지의 이름을 "set_stats"로 정하고 **메세지** 파라미터로 새로운 데이터를 첨부합니다:

```lua
-- 메세지로 table 데이터를 전송하기
msg.post("hud#script", "set_stats", { score = 100, stars = 2, health = 4 })
```

이 호출은 추가적인 데이터와 함께 **메세지** 파라미터를 추가합니다. 이 인수는 선택적이며 중괄호 안에서 키-값 쌍으로 이루어진 Lua 테이블이어야 합니다. 거의 모든 자료형의 데이터가 Lua 테이블 메세지에 포함될 수 있습니다. 숫자형, 문자열형, 불린형, URL, 해쉬, 중첩 테이블 모두 전달 할 수 있지만 함수(function) 타입은 불가능합니다.

```lua
-- Send table data containing a nested table
local invtable = { sword = true, shield = true, bow = true, arrows = 9 }
local msgdata = { score = 100, stars = 2, health = 4, inventory = invtable }
msg.post("hud#script", "set_stats", msgdata)
```

> **메세지** 파라미터 테이블의 크기에는 엄격한 제한사항이 있습니다. 이 제한은 2kb 까지입니다. 현재 테이블이 소모하는 정확한 메모리 사이즈를 알아내는 방법은 없지만, collectgarbage("count") 를 사용하여 테이블에 값을 삽입하기 전후를 따져서 메모리 사용량을 측정할 수 있습니다.

## on_message()
on_message() 함수는 3개의 파라미터를 가집니다. (게임 오브젝트 자신의 참조를 포함하는 "self"와는 별개로)

#### message_id
메세지의 이름입니다. 이 이름은 해쉬(hash)됩니다.

#### message
메세지의 데이터입니다. 이것은 Lua 테이블입니다.

#### sender
발신자의 전체 URL입니다.

```lua
function on_message(self, message_id, message, sender)
    -- message id 출력하기
    print(message_id)
    -- message data 출력하기 (테이블이라 pprint를 사용했지!)
    pprint(message)
    -- sender 출력하기
    print(sender)
end
```

위 코드가 실행되면 콘솔창에 아래 내용이 출력됩니다:

```
DEBUG:SCRIPT: hash: [set_stats]
DEBUG:SCRIPT:
{
  health = 4,
  stars = 2,
  score = 100,
}
DEBUG:SCRIPT: url: [main:/game_controller#script]
```

다음은 "hud" 게임 오브젝트가 어떤 방식으로 "set_stats"를 간단히 구현했는지 보여주는 예제입니다:

```lua
function init(self)
        -- 하트10개 별10개로 GUI 노드를 복제함
        self.heart_nodes = {}
        self.star_nodes = {}
        local heart_node = gui.get_node("heart")
        local star_node = gui.get_node("star")

        -- 쉽게 억세스 할 수 있게 모든 노드를 테이블에 저장함
        table.insert(self.heart_nodes, heart_node)
        -- 노드가 비활성화 된 채로 시작함
        gui.set_enabled(heart_node, false)

        for i = 1, 9 do
                local clone = gui.clone(heart_node)
                local pos = gui.get_position(heart_node)
                pos.x = pos.x + i * 32
                gui.set_position(clone, pos)
                table.insert(self.heart_nodes, clone)
                gui.set_enabled(clone, false)
        end
        table.insert(self.star_nodes, star_node)
        gui.set_enabled(star_node, false)
        for i = 1, 9 do
                local clone = gui.clone(star_node)
                local pos = gui.get_position(star_node)
                pos.x = pos.x + i * 32
                gui.set_position(clone, pos)
                table.insert(self.star_nodes, clone)
                gui.set_enabled(clone, false)
        end
end

function on_message(self, message_id, message, sender)
        if message_id == hash("set_stats") then
                -- 점수 GUI노드를 업데이트하기
                gui.set_text(gui.get_node("score"), message.score)
                -- 하트 노드의 수만큼 활성화
                for i = 1, message.health do
                        gui.set_enabled(self.heart_nodes[i], true)
                end
                -- 별 노드의 수만큼 활성화
                for i = 1, message.stars do
                        gui.set_enabled(self.star_nodes[i], true)
                end
        end
end
```

## Child-parent vs. collection-object hierarchies (부모-자식 계층구조와 컬렉션-오브젝트 계층구조 비교하기)
우리는 경로(path)를 통한 오브젝트 주소 지정이 Defold에서 정적(static)이라는 것을 알았으며 이는 게임 로직을 코딩할 때 항상 오브젝트 id의 무결성을 신뢰해도 된다는 것을 의미합니다.

오브젝트간의 부모-자식 계층구조는 오브젝트가 어떻게 변형(transformations)에 반응하는지 영향을 주는 동적인 관계(dynamic relation)입니다. 오브젝트에 적용되는 모든 변형은 이 오브젝트의 자식들에게도 적용됩니다. "set_parent" 메세지를 보내는 것으로 런타임시 오브젝트 부모를 변경할 수 있습니다.

```lua
local parent = go.get_id("tree")
msg.post(".", "set_parent", { parent_id = parent })
```

부모-자식 계층구조는 에디터에서 설정할 수도 있으며 여전히 동적인 (dynamic) 상태입니다. 예를 들어, 하트가 달린 나무를 만들어 봅시다. 이는 "tree" 오브젝트와 몇 개의 "heart" 오브젝트로 구성되어 있습니다. 또한 나무가 살아가는데 필요한 "pot"도 있습니다. 우선 이 오브젝트들을 부모와 자식관계로 만들기 위해 "hearttree"라고 불리우는 컬렉션에 오브젝트들을 배치합니다. 그리고 나서 "heart" 오브젝트를 "tree" 오브젝트에 드래그 하여 간단히 자식객체로 만들 수 있습니다. 

![Heart tree](images/message_passing/editor_heart_tree.png)

나무에 하트 자식들을 만듬으로써, 마치 나무 오브젝트의 일부분인 것 처럼 나무에 주는 모든 변형이  하트들에게 영향을 주게 됩니다. 따라서 나무를 앞뒤로 움직이게 애니메이션 처리를 하면 하트들도 따라서 움직이게 됩니다.

> "hearttree" 컬렉션 내의 하트 오브젝트에 대한 경로는 우리가 설정한 동적인 부모-자식 관계에 의해 영향을 받지 않습니다.

> /hearttree/heart1 ("/hearttree/tree/heart1"가 아님)
/hearttree/heart2
/hearttree/heart3
/hearttree/heart4

> 부모-자식 관계는 컬렉션 계층구조 내의 오브젝트 주소와 별개입니다. 따라서, 부모-자식 관계는 결코 오브젝트의 URL에 반영되지 않습니다.

## Advanced topics

#### Constructing URLs
드물긴 하지만 프로그래밍 방식으로 URL 오브젝트를 만들어야할 경우가 있을 수도 있습니다. 이럴 땐 아래와 같이 하세요:

```lua
local my_url = msg.url()
my_url.socket = "main" -- 유효한 이름으로 지정하기
my_url.path = hash("/hearttree/tree") -- 문자열이나 해쉬로 지정하기
my_url.fragment = "script" -- 문자열이나 해쉬로 지정하기
msg.post(my_url, "grow")
```

URL 및 해당 컴포넌트들을 조사해보면:

```lua
print(my_url) --> url: [main:/hearttree/tree#script]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/hearttree/tree]
print(my_url.fragment) --> hash: [script]
```

#### System sockets
Defold는 엔진의 특정 서브 시스템과 통신하기 위해 URL의 socket 부분을 활용합니다:

1. @physics:
2. @render:
3. @system:

path나 fragment 부분은 필요 없습니다.

예를 들어, 아래 메세지를 보냄으로써 시스템 프로파일러를 토글할 수 있습니다.

```lua
 msg.post("@system:", "toggle_profile")
```

#### Collection Proxies
Defold가 시작되면 게임 프로젝트 셋팅창의 "bootstrap" 아래의 "main_collection" 항목에 지정된 컬렉션을 자동으로 로드하고 초기화 합니다. 

별도의 컬렉션에 각기 다른 게임 레벨을 유지해야 하는 등, 서로 다른 컬렉션을 동적으로 불러와야할 경우가 있을 수 있습니다. Defold는 동적으로 로드되는 컬렉션을 위해 컬렉션 프록시(Collection Proxy) 오브젝트를 사용합니다.

예를 들어 우리가 컬렉션 프록시 오브젝트를 추가하고 "level"이라고 명명된 몇몇 컬렉션을 대체하는 것으로 셋팅한다면, 이 프록시에게 메세지를 보내는 것으로 컬렉션을 로드할 수 있습니다.

![Proxy](images/message_passing/message_passing_proxy.png)

```lua
msg.post("/loader#levelproxy", "load")
```

컬렉션이 로드되면 메세지를 돌려받고 초기화 작업 및 다른 최상위 컬렉션으로 메세지를 보내는 것을 시작할 수 있습니다.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- 컬렉션이 로드되었고 활성화를 해보자
        msg.post(sender, "enable")
        -- 로드된 컬렉션의 아무나에게 메세지를 보내보자
        msg.post("level:/gamemaster#script", "wake_up")
    end
end
```

이와 같이 최상위 컬렉션 간에 메세지를 보내면, URL의 socket 필드를 사용하여 타겟 오브젝트가 상주하는 컬렉션을 지정해야 합니다.

> 자세한 설명은 [Collection proxy](/manuals/collection-proxy) 문서에서 찾을 수 있습니다.

#### Message chains
게시된 메세지들이 디스패치되고 수신자의 on_message()가 호출되면, 응답 코드를 담아 또 새 메세지를 게시하여 주거니 받거니 하는 것은 일반적인 개발 방식입니다. 당신은 엔진이 디스패치 해야하는 긴 메세지 체인을 구축할 수 있습니다. 이것은 언제 발생할까요?

짧게 대답하자면 이 디스패치는 즉시 발생합니다. 게임엔진은 메세지들을 처리하는 작업을 시작하고 당신이 새 메세지를 게시하여 큐를 계속 채우더라도 메세지 큐가 비워질 때까지 계속 처리합니다. 

그러나 게임엔진이 메세지큐를 비울 수 있는 횟수는 제한이 있습니다. 이는 긴 메세지 체인을 한 프레임 내에서 효과적으로 제한합니다. 다음 스크립트를 사용하여 각 update() 사이에 엔진이 처리할 수 있는 디스패치 수가 얼마나 되는지 쉽게 테스트 할 수 있습니다.

```lua
function init(self)
        -- 오브젝트 초기화 동안 긴 메세지 체인을 시작해 볼까나
        -- 그리고 update()마다 숫자를 증가하자
        print("INIT")
        msg.post("#", "msg")
        self.updates = 0
        self.count = 0
end

function update(self, dt)
        if self.updates < 5 then
                self.updates = self.updates + 1
                print("UPDATE " .. self.updates)
                print(self.count .. " 회 디스패치 됨.")
                self.count = 0
        end
end

function on_message(self, message_id, message, sender)
        if message_id == hash("msg") then
                self.count = self.count + 1
                msg.post("#", "msg")
        end
end
```

이 스크립트를 실행하면 아래 처럼 출력 됩니다:

```
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 회 디스패치 됨.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 회 디스패치 됨.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 회 디스패치 됨.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 회 디스패치 됨.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 회 디스패치 됨.
```

이 버전의 Defold 엔진은 init()과 첫 update() 호출 사이에 10회의 메세지 큐 디스패치가 발생한다는 것을 알 수 있습니다. 그런 다음 매 update() 마다 75회의 메세지가 수행되었습니다.
