# Building blocks
이 문서에서는 *게임오브젝트, 컴포넌트, 컬렉션*이 어떻게 동작하는지 자세히 설명합니다.

Defold에서 만든 것 중 일부는 다른 소프트웨어와는 다르게 설계되어 있습니다. 이 블록들을 왜 합치며 어떻게 합치는지에 대한 이해가 조금 어려울 수도 있습니다. Defold가 어떻게 게임 리소스를 관리하고 접근하는지 이해하기 위해서는, 이 문서와 [Message passing](/manuals/message-passing) 문서를 참고 바랍니다. 여기에 있는 것들 중 일부 혹은 대부분은 생소하고 처음에는 이해하기 힘들겠지만, 걱정 마세요. 시간을 내서 에디터와 게임엔진을 다뤄보고 실행에 문제가 생기면 문서들을 둘러 보시기 바랍니다.

![Building blocks](images/building_blocks/building_blocks.png)

## Game objects
게임 오브젝트는 게임이 실행되는 동안에 각각의 수명을 가지는 간단한 객체입니다. 일반적으로 게임 오브젝트는 비주얼이나 오디오를 나타내는 요소들(예를 들어 스프라이트 컴포넌트나 사운드 컴포넌트)을 장착하여 사용됩니다.  또한 스크립트 컴포넌트를 장착해서 특정한 동작을 구현할 수도 있습니다. 따라서 게임 오브젝트는 이런 다양한 컴포넌트들을 위한 컨테이너라는 점에서 스프라이트, 모델, 사운드와는 구분됩니다. 당신은 게임 오브젝트를 생성하여 에디터상의 컬렉션에 배치시킬 수 있으며 혹은 팩토리를 사용하여 런타임시 동적으로 스폰되게 할 수도 있습니다.

여기 에디터에서 게임 오브젝트를 생성하는 두 가지 방법이 있습니다:

1. 게임오브젝트 파일을 만든 후 컬렉션에 이 파일의 인스턴스를 만들기
2. 게임오브젝트의 인스턴스를 컬렉션에 배치하여 만들기

이들 방식의 차이점을 살펴 보도록 합시다.

#### Prototypes and instances
게임 오브젝트 파일을 생성해서 게임 오브젝트를 위한 설계도(blueprint)나 프로토타입(prototype)을 만듭니다. 나중에 이 프로토타입으로 하나 혹은 다수의 게임오브젝트 인스턴스를 생성할 수 있습니다.

![Game object file](images/building_blocks/building_blocks_gameobject_file.png)

게임 오브젝트 파일을 만들어도 게임 실행시에는 아무것도 추가되는 것이 없습니다. 이 게임 오브젝트는 아직 존재하지 않으며, 실제 오브젝트를 만들 수 있는 공식만 존재할 뿐입니다. 미리 만들어 놓은 설계도를 기반으로 실제 게임 오브젝트를 만들기 위해서는, 컬렉션을 오른쪽 클릭하고 **Add Game Object File**을 선택해서 프로젝트의 컬렉션에 게임오브젝트의 인스턴스를 추가하면 됩니다.

![Game object instance](images/building_blocks/building_blocks_gameobject_instance.png)

이제 게임 오브젝트는 작동을 시작할 수 있습니다. 당신은 많은 수의 인스턴스를 만들 수도 있는데, 각각의 인스턴스는 아까 게임 오브젝트 파일에 저장된 것과 똑같은 복제본입니다.

![Game object clones](images/building_blocks/building_blocks_gameobject_clones.png)

이러한 방식의 좋은 점은 게임 오브젝트 파일을 변경하여 프로토타입을 바꾸는 경우, 이 파일을 기반으로 생성된 인스턴스들도 즉시 변경된다는 것입니다.

![Game object alter file](images/building_blocks/building_blocks_gameobject_alter.png)

#### Childing game objects
이제는 처음으로 특이하게 보이는 사례를 살펴 보도록 합시다. 위의 프로토타입 파일의 "my_gameobject" 인스턴스를 컬렉션에 추가하고, "heart"라는 이름의 게임 오브젝트를 몇몇 컴포넌트들과 함께 생성해 봅시다. (컬렉션에 오른쪽클릭 후 **Add Game Object** 선택) 마지막으로, "heart" 오브젝트를 "my_gameobject"로 드래그해서 자식 오브젝트로 만듭니다.  이제 컬렉션이 다음과 같이 수정되었습니다:

![Game object instance with child](images/building_blocks/building_blocks_gameobject_instance_child.png)

"heart" 오브젝트를 "my_gameobject"로 드래그하는 것으로 인해 "my_gameobject.go"파일이 바뀌는 것이 아닌지 생각할 수도 있지만, 그런 일은 발생하지 않습니다. 이 작업의 영향은 오직 "my_gameobject"라는 게임 오브젝트 인스턴스가 자식 오브젝트를 가지는 것 뿐입니다. 이 게임 오브젝트 인스턴스는 프로토타입과 자식오브젝트에 관한 두 가지 다른 속성을 가집니다. 게임 오브젝트 인스턴스에 자식 오브젝트들을 추가하면 프로토타입은 건드리지 않은 채로 해당 오브젝트의 **자식 속성(children property)** 이 추가됩니다.

컬렉션 파일에 마우스 오른쪽 버튼을 누르고 **Open With > Text Editor**를 선택해서 텍스트 에디터로 컬렉션을 열어 보면 게임 오브젝트 데이터 구조를 파악할 수 있습니다:
```json
name: "default"
instances {
  id: "my_gameobject"
  prototype: "/a_simple_test/my_gameobject.go"
  children: "heart"
  ...
}
scale_along_z: 0
embedded_instances {
  id: "heart"
  data: "embedded_components {\n  id: \"sprite\"\n  type: \"sprite\"\n  data: \"tile_set: \\\"/cards_example/cards_sprites.atlas\\\"\\ndefault_animation: \\\"heart\\\"\\nmaterial: \\\"/builtins/materials/sprite.material\\\"\\nblend_mode: BLEND_MODE_ALPHA\\n\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n}\n"
  ...
}
```

이처럼 게임 오브젝트 인스턴스가 **prototype** 속성을 가지고 있는 것을 위 파일에서 명확히 볼 수 있습니다. 또 다른 속성인 **children**은 "heart"라는 이름의 자식 인스턴스를 가지고 있는데, "heart"는 다른 게임오브젝트와 달리 프로토타입 기반이 아니고 내부에 위치된 게임 오브젝트(in-place game object)이므로 **embedded_instances** 아래에 나열되며 이 데이터는 현재의 컬렉션 파일에만 저장됩니다.

> 이 에디터에서 작업할 때 게임 오브젝트 프로토타입과 인스턴스를 명확하게 구분하는 것 외에도, 런타임시 고정된 아이디로 어떻게 게임 오브젝트를 식별하는지와 자식오브젝트를 설정하는 것이 아이디에 어떻게 영향을 끼치는지 시간을 들여 신중히 공부하는 것이 좋습니다. [Message passing](/manuals/message-passing) 문서에 자세한 설명이 있습니다.

지금쯤 당신은 아마 "게임 오브젝트 파일을 만들어 게임 오브젝트와 자식 오브젝트를 생성한 다음 컬렉션에 이 오브젝트를 인스턴스화 시킨 후 자식 오브젝트를 삭제하면 어떻게 될까?"라는 의문을 품을 수도 있습니다. 간단히 답변하자면 이것은 불가능합니다. 게임 오브젝트 파일은 단일 게임 오브젝트의 설계도면입니다. 오직 빌드시에 에디터에서 컬렉션을 수정하거나 런타임시에 msg.post("my_object", "set_parent", { parent_id = go.get_id("my_parent") }) 를 사용하여 게임 오브젝트의 인스턴스에 자식 오브젝트들을 추가하는 것만 가능합니다.

## Components
컴포넌트는 특정한 표현이나 기능을 게임 오브젝트에 부여하는데 사용됩니다. 이것들은 게임 오브젝트 안에 포함되어야만 하며 스스로 살아가지 못합니다. 여기에 에디터에서 새 컴포넌트를 생성하는 두가지 방법이 있습니다:

1. 컴포넌트 파일을 생성한 후 컴포넌트의 인스턴스를 게임 오브젝트 안에 만드는 방법
2. 게임 오브젝트 안에 내장(in-place) 컴포넌트 인스턴스를 만드는 방법

위 두 가지 케이스로 특정 유형의 컴포넌트를 생성해서 에디터에서 이 컴포넌트를 열면 컴포넌트의 종류에 맞는 적합한 에디터를 띄워서 컴포넌트를 다룰 수 있게 해 줍니다.

우리는 이전 섹션에서 **embedded_components** 속성을 통해서 에디터가 내장 컴포넌트를 게임 오브젝트에 어떻게 저장하는지 살펴보았습니다. 이와는 조금 다르지만 파일의 참조(reference)로부터 컴포넌트를 인스턴스화 하면 아래 처럼 나타납니다:

```json
embedded_instances {
  id: "heart2"
  data: "components {\n  id: \"sprite\"\n  component: \"/a_simple_test/my_heart.sprite\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n}\n"
  ...
}
```

컴포넌트의 특정한 데이터는 **component** 속성값을 통해 컴포넌트 파일을 참조하여 저장됩니다.

아마도 가장 자주 쓰이는 컴포넌트 타입은  동작(behaviors)을 구현하는데 쓰이는 스크립트 컴포넌트 일 것입니다.  여기서 잊기 쉬운것은 스크립트 컴포넌트와 이를 포함하는 게임오브젝트간에 명확한 경계가 있다는 사실입니다. 예를 들어, 아래는 일반적인 스타일의 메세지 전달 방법입니다:

```lua
msg.post("my_object", "my_message", { my_data = 1 }})
```

여기서 이 커스텀 메세지는 "my_object"라는 게임 오브젝트로 전송됩니다. 이것은 일반적으로 잘 동작하지만 권장하는 방식은 아닙니다. 첫째, 게임 오브젝트로 전송된 메세지는 게임 오브젝트에 포함된 모든 컴포넌트들에게 브로드캐스팅 되어 불필요한 오버헤드가 생길 수 있습니다. 둘째, 게임 오브젝트의 일부 동작을 깨트릴수도 있습니다. 예를 들어, 게임 오브젝트가 여러 개의 스크립트 컴포넌트를 가지고 있고 동시에 처리할 수 있도록 설계되지 않은 채로 이 스크립트가 전부 "my_message"라는 메세지를 기다리고 있다고 가정해 봅시다. 메세지의 주소를 지정하는데 권장하는 방법으로는 가능한 구체적이고 게임 오브젝트와 컴포넌트간 차이를 알기 쉽게 지정하는 것이 좋은 방법입니다.

```lua
msg.post("my_object#script", "my_message", { my_data = 1 })
```

#### Custom component properties
컴포넌트는 한가지 또는 다른 방법으로 컴포넌트를 변경하도록 셋팅된 유형별 특정 속성들이 있습니다. 스프라이트 컴포넌트에는 넓이(width)와 길이(height)가 있으며, 사운드 컴포넌트에는 사운드를 반복할지 여부를 결정하는 속성이 있습니다. 또 스크립트 컴포넌트에서는 특정한 속성을 직접 만들 수도 있습니다. 스크립트 파일에 속성을 만드는 코드를 추가하면 스크립트 컴포넌트의 속성을 쉽게 정의할 수 있습니다.

```lua
-- self.health는 자동으로 100을 기본값으로 셋팅함.
-- 이 스크립트 컴포넌트를 포함하는 인스턴스의 초기값을 변경할 수 있음.
go.property("health", 100)

function on_message(self, message_id, message, sender)
    -- 이제 "self.health"라는 속성값에 액세스 할 수 있음
    ...
end
```

스크립트 속성이 어떻게 동작하는지 어떻게 사용하는지 자세한 설명이 알고 싶다면 [Script properties](/manuals/script-properties) 문서를 참고 바랍니다.  스크립트 속성을 정의하면 그 속성과 연관된 자료형으로 다른 보통의 속성들처럼 파일에 저장됩니다. 게임 오브젝트가 프로토타입에 의해 인스턴스화 된 경우엔 별도의 **component_properties** 속성이 스크립트 속성(향우엔 다른 컴포넌트에도 가능할지도)을 포함하는 오브젝트 인스턴스에 추가됩니다:

![Script properties](images/building_blocks/building_blocks_properties.png)

```json
  component_properties {
    id: "script"
    properties {
      id: "my_property"
      value: "4712.0"
      type: PROPERTY_TYPE_NUMBER
    }
  }
```

반대로 임베디드 된 게임 오브젝트에서 모든 컴포넌트 속성은 명시적으로 **properties** 속성으로 컬렉션 파일에 표시됩니다:

![Embedded script properties](images/building_blocks/building_blocks_properties_embedded.png)

```json
data: "components {\n  id: \"some_script\"\n  component: \"/a_simple_test/my_thing.script\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n  properties {\n    id: \"my_property\"\n    value: \"4713.0\"\n    type: PROPERTY_TYPE_NUMBER\n  }\n}\ncomponents {\n  id: \"sprite\"\n  component: \"/a_simple_test/my_heart.sprite\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n}\n"
```

## Collections
컬렉션은 템플릿 생성을 위한 Defold의 메커니즘이며 다른 게임엔진에선 프리펩(prefab)이라고도 불려 지기도 합니다. 컬렉션은 게임 오브젝트들이나 또 다른 컬렉션들을 가지는 트리구조로 되어 있습니다. 컬렉션은 항상 파일에 저장되며 한두가지 방법으로 게임으로 불러올 수 있습니다:

1. 빌드시 컬렉션을 에디터상의 다른 컬렉션에 배치하는 방법
2. 런타임시 컬렉션 프록시(Collection proxy)를 사용해서 컬렉션에 모인 모든 리소스를 동적으로 로딩하는 방법(자세한 것은 [Collection proxy](/manuals/collection-proxy)문서를 참고 바랍니다.)

![Collection instances](images/building_blocks/building_blocks_collection_instances.png)

에디터에 위치한 컬렉션들은 수정할 수 없습니다. 예를 들어 배치된 컬렉션의 일부인 게임 오브젝트에 하위 항목을 추가할 수 없습니다. 컬렉션 인스턴스에 저장된 데이터를 보면 잘 될거 같은데 왜 안될까요? 게임 오브젝트를 포함하고 있는 이 데이터는 "my_collection.collection"이라는 참조된 컬렉션 파일 안에 있고 이것은 수정되는 것이 아닙니다.

컬렉션 파일 원본을 수정하지 않고는 컬렉션의 내용을 수정할 수 없지만, 에디터는 컬렉션에서 컴포넌트들과 연관된 스크립트 속성과 동일하게 속성값들의 수정을 허용합니다. 

![Properties in a collection](images/building_blocks/building_blocks_collection_properties.png)

```json
collection_instances {
  id: "my_collection"
  collection: "/a_simple_test/my_collection.collection"
  position {
    x: -172.74739
    y: 149.61157
    z: 0.0
  }
  rotation {
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
  }
  scale: 1.0
  instance_properties {
    id: "my_gameobject"
    properties {
      id: "script"
      properties {
        id: "my_property"
        value: "4717.0"
        type: PROPERTY_TYPE_NUMBER
      }
    }
  }
}
```

> 많이들 헷갈리는 점은 컬렉션 계층구조의 게임 오브젝트의 위치가 런타임시에 부모-자식 계층(set_parent 메세지로 맺어진)으로 된다는 것이 있습니다. 여기서 두 가지 차이점을 깨닫는 것이 중요한데, 컬렉션은 관리 및 그룹화를 의미하는 반면, 부모-자식 계층은 오브젝트가 또다른 오브젝트와 시각적으로 연결되어 씬 그래프(scene graph)를 동적으로 수정하는 것을 의미합니다. 컬렉션 계층에서는 게임 오브젝트의 위치로 id를 지정하지만 이 id는 오브젝트의 수명기간 동안엔 정적(static)상태입니다. 게임 오브젝트의 주소 지정(addressing)에 대한 자세한 설명은 [Message passing](/manuals/message-passing) 문서를 참고 바랍니다.
