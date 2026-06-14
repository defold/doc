---
title: 스크립트 컴포넌트 프로퍼티
brief: 이 매뉴얼은 스크립트 컴포넌트에 커스텀 프로퍼티를 추가하고 에디터와 런타임 스크립트에서 액세스하는 방법을 설명합니다.
---

# 스크립트 프로퍼티

스크립트 프로퍼티는 특정 게임 오브젝트 인스턴스에 대한 커스텀 프로퍼티를 정의하고 노출하는 간단하고 강력한 방법을 제공합니다. 스크립트 프로퍼티는 에디터에서 특정 인스턴스별로 직접 편집할 수 있으며, 코드에서 그 설정값을 사용해 게임 오브젝트의 동작을 바꿀 수 있습니다. 스크립트 프로퍼티가 매우 유용한 경우는 많습니다:

* 에디터에서 특정 인스턴스의 값을 오버라이드해 스크립트 재사용성을 높이고 싶을 때.
* 초기값을 사용해 게임 오브젝트를 스폰하고 싶을 때.
* 프로퍼티 값에 애니메이션을 적용하고 싶을 때.
* 한 스크립트의 상태 데이터에 다른 스크립트에서 액세스하고 싶을 때. (오브젝트 간에 프로퍼티를 자주 액세스한다면 데이터를 공유 저장소로 옮기는 편이 더 나을 수 있습니다.)

일반적인 사용 사례로는 특정 적 AI의 체력이나 속도, 픽업 오브젝트의 색조 색상, 스프라이트의 아틀라스, 또는 버튼 오브젝트를 눌렀을 때 어떤 메세지를 어디로 보낼지 설정하는 것이 있습니다.

## 스크립트 프로퍼티 정의

스크립트 프로퍼티는 `go.property()` 특수 함수로 정의해 스크립트 컴포넌트에 추가합니다. 이 함수는 `init()`과 `update()` 같은 라이프사이클 함수 바깥의 최상위 레벨에서 사용해야 합니다. 프로퍼티에 제공한 기본값이 프로퍼티의 타입을 결정합니다: `number`, `boolean`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion`, `resource`(아래 참고).

::: important
해쉬값의 역변환은 디버깅을 돕기 위해 Debug 빌드에서만 동작합니다. Release 빌드에는 역변환된 문자열 값이 존재하지 않으므로, `hash` 값에서 문자열을 추출하려고 `tostring()`을 사용하는 것은 의미가 없습니다.
:::


```lua
-- can.script
-- health와 공격 타겟을 위한 스크립트 프로퍼티 정의
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- 타겟의 초기 위치 저장.
  -- self.target은 다른 오브젝트를 참조하는 url입니다.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- health 프로퍼티 감소
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

이 스크립트를 기반으로 만든 모든 스크립트 컴포넌트 인스턴스는 이후 프로퍼티 값을 설정할 수 있습니다.

![프로퍼티가 있는 컴포넌트](images/script-properties/component.png)

에디터의 *Outline* 뷰에서 스크립트 컴포넌트를 선택하면 *Properties* 뷰에 프로퍼티가 나타나고, 여기에서 값을 편집할 수 있습니다:

![프로퍼티](images/script-properties/properties.png)

새 인스턴스별 값으로 오버라이드된 모든 프로퍼티는 파란색으로 표시됩니다. 프로퍼티 이름 옆의 재설정 버튼을 클릭하면 값을 기본값(스크립트에 설정된 값)으로 되돌릴 수 있습니다.


::: important
스크립트 프로퍼티는 프로젝트를 빌드할 때 파싱됩니다. 값 표현식은 평가되지 않습니다. 즉, `go.property("hp", 3+6)` 같은 코드는 동작하지 않지만 `go.property("hp", 9)`는 동작합니다.
:::

## 스크립트 프로퍼티 액세스

정의된 모든 스크립트 프로퍼티는 스크립트 인스턴스 참조인 `self`에 저장된 멤버로 사용할 수 있습니다:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- 프로퍼티 읽기 및 쓰기
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

사용자가 정의한 스크립트 프로퍼티도 다른 프로퍼티와 같은 방식으로 `get`, `set`, `animate` 함수를 통해 액세스할 수 있습니다:

```lua
-- another.script

-- "myobject#my_script"의 "my_property"를 1 증가
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- "myobject#my_script"의 "my_property" 애니메이션
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## 팩토리로 생성한 오브젝트

팩토리를 사용해 게임 오브젝트를 생성하는 경우 생성 시점에 스크립트 프로퍼티를 설정할 수 있습니다:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- 팩토리로 생성한 오브젝트의 스크립트 프로퍼티 액세스
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

`collectionfactory.create()`를 통해 게임 오브젝트 계층구조를 스폰할 때는 오브젝트 id와 프로퍼티 테이블을 쌍으로 묶어야 합니다. 이 쌍들을 하나의 테이블에 넣어 `create()` 함수에 전달합니다:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

`factory.create()`와 `collectionfactory.create()`를 통해 제공한 프로퍼티 값은 프로토타입 파일에 설정된 값과 스크립트의 기본값을 모두 오버라이드합니다.

게임 오브젝트에 연결된 여러 스크립트 컴포넌트가 같은 프로퍼티를 정의하면, 각 컴포넌트는 `factory.create()` 또는 `collectionfactory.create()`에 제공된 값으로 초기화됩니다.


## 리소스 프로퍼티

리소스 프로퍼티는 기본 데이터 타입의 스크립트 프로퍼티와 같은 방식으로 정의합니다:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

리소스 프로퍼티를 정의하면 다른 스크립트 프로퍼티처럼 *Properties* 뷰에 표시되지만, 파일/리소스 브라우저 필드로 표시됩니다:

![리소스 프로퍼티](images/script-properties/resource-properties.png)

리소스 프로퍼티는 `go.get()`으로 또는 `self` 스크립트 인스턴스 참조를 통해 액세스하고, `go.set()`으로 사용할 수 있습니다:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
