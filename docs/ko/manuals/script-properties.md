---
title: Defold manual
---

# Script properties
스크립트 프로퍼티는 특정 게임 오브젝트 인스턴스의 동작이나 외형을 제어하고 에디터 상에서 코딩 없이 수정할 수 있도록 프로퍼티를 노출하는 강력하고 간단한 방법을 제공합니다.

스크립트 프로퍼티는 인스턴스에 따라 특정 스크립트 프로퍼티를 오버라이드(overrides) 할 수 있습니다. 일반적인 사용 사례로는 특정 적 AI의 체력, 속도라던가 아이템 오브젝트의 색상이나 버튼 클릭시 어떤 메세지를 보낼지 등등... 아래의 사례처럼 스크립트 프로퍼티를 유용하게 활용할 수 있는 많은 경우가 있습니다.

* 에디터상에서 특정 인스턴스의 값들을 오버라이드 하려 할 때, 그리고 스크립트 재 사용성(re-usability)을 높일 필요가 있을 때
* 초기값으로 게임 오브젝트를 스폰해야 할 때
* 프로퍼티의 값에 에니메이션을 적용하려 할 때
* 다른 스크립트에서 데이터에 엑세스 하려 할 때

> 데이터에 자주 엑세스하는 경우, 성능상의 이유로 프로퍼티보다는 테이블로부터 액세스 하는 것이 더 낫습니다.

스크립트의 동작이나 컴포넌트 프로퍼티를 제어하는데 사용되는 대부분 값의 유형은 스크립트 프로퍼티로 노출될 수 있습니다.

#### Booleans
True 또는 False
#### Numbers
숫자형(numerical) 값
#### Hashes
해쉬된(hash) 문자열 값
#### URLs
오프젝트나 컴포넌트를 참조
#### Vector3
3 차원 벡터 값
#### Vector4
4 차원 벡터 값
#### Quaternion
쿼터니온 값

예를 들어, 게임 오브젝트의 체력을 제어하는 스크립트가 있다고 가정해 봅시다. 이 스크립트는 take_damage 라는 메세지를 통해 데미지를 입힐 수 있습니다.

```lua
function init(self)
    self.health = 100
end

function on_message(self, message_id, message, sender)
    if message_id == hash("take_damage") then
        self.health = self.health - message.damage
        if self.health <= 0 then
            go.delete()
        end
    end
end
```

체력이 0이 되면, 이 스크립트는 게임 오브젝트를 파괴 시킵니다. 이제 두 개의 게임 오브젝트에서 이 스크립트를 사용하려 하지만, 서로 다른 체력 값을 가져야 한다고 칩시다. go.property 함수를 사용하면 스크립트 프로퍼티를 정의 할 수 있으며 특정 게임 오브젝트 인스턴스의 값을 셋팅할 수 있게 됩니다.

```lua
-- self.health 는 기본값으로 100을 자동 셋팅함
go.property("health", 100)

function on_message(self, message_id, message, sender)
    if message_id == hash("take_damage") then
        self.health = self.health - message.damage
        if self.health <= 0 then
            go.delete()
        end
    end
end
```

이 스크립트를 포함하는 모든 게임 오브젝트는 값을 구체적으로 설정할 수 있습니다. 에디터의 Outline 창에서 스크립트 노드를 선택하면 Properties 창에서 프로퍼티가 노출되어 값을 수정할 수 있게 됩니다.

![Script Properties](images/script_properties/script_properties.png)

> 하위 컬렉션 내에 게임 오브젝트가 있는 경우, 컬렉션의 게임 오브젝트 노드를 확장하여 스크립트를 선택하면 됩니다.

이 에디터 프로퍼티 인스펙터(editor property inspector)는 선언된 프로퍼티의 유형에 맞게 위젯을 자동적으로 보여줍니다. 숫자형은 텍스트 박스로, 벡터나 쿼터니온 형은 여러개의 텍스트 박스로, 해쉬값은 문자열을 해쉬시켜 주고, URL은 관련된 모든 로컬 오브젝트나 컴포넌트를(동일한 컬렉션에 위치한 것만) 드롭다운 리스트로 보여줍니다. 또한 URL을 수동으로 입력하는 것도 가능합니다.

![](images/script_properties/script_properties_example.png)

## Factory created objects
팩토리를 사용하여 게임 오브젝트를 생성하는 경우, 생성시에 스크립트 프로퍼티를 셋팅하는 것도 가능합니다.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("create_my_object") then
        factory.create("#factory", go.get_position(), go.get_rotation(), { health = 50 })
    end
end
```

프로퍼티 값은  factory.create()를 통하면 스크립트의 기본값 뿐만 아니라 게임오브젝트 파일의 값들을 오버라이드(override) 합니다.

> 만약 게임 오브젝트에 여러 개의 스크립트 컴포넌트를 연결했다면, 이 스크립트 파일들 전부에게 스크립트 프로퍼티를 설정할 수 있습니다. 예를 들어 위의 게임 오브젝트 예제에서 체력 프로퍼티를 포함하고 있는 다른 스크립트 컴포넌트가 있다고 가정하면, factory.create() 가 호출 될 때, 두 스크립트의 체력 프로퍼티 모두 제공된 값으로 설정됩니다.
