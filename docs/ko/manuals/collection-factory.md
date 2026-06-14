---
title: 컬렉션 팩토리 매뉴얼
brief: 이 매뉴얼은 컬렉션 팩토리 컴포넌트를 사용해 게임 오브젝트 계층구조를 스폰하는 방법을 설명합니다.
---

# 컬렉션 팩토리

컬렉션 팩토리(Collection factory) 컴포넌트는 컬렉션 파일에 저장된 게임 오브젝트 그룹과 계층구조를 실행 중인 게임 안으로 스폰하는 데 사용됩니다.

컬렉션은 Defold에서 재사용 가능한 템플릿, 또는 "prefab"을 만들 수 있는 강력한 메커니즘을 제공합니다. 컬렉션 개요는 [빌딩 블록 문서](/manuals/building-blocks#collections)를 참고하세요. 컬렉션은 에디터에 배치할 수도 있고, 게임에 동적으로 삽입할 수도 있습니다.

컬렉션 팩토리 컴포넌트를 사용하면 컬렉션 파일의 컨텐츠를 게임 월드 안으로 스폰할 수 있습니다. 이는 컬렉션 안의 모든 게임 오브젝트를 팩토리로 스폰한 뒤 오브젝트 사이의 부모-자식 계층구조를 만드는 것과 비슷합니다. 일반적인 사용 사례는 여러 게임 오브젝트로 구성된 적(예: 적 + 무기)을 스폰하는 것입니다.

## 컬렉션 스폰하기

캐릭터 게임 오브젝트 하나와, 캐릭터의 자식인 별도 방패 게임 오브젝트가 필요하다고 가정해 봅시다. 컬렉션 파일에 게임 오브젝트 계층구조를 만들고 "bean.collection"으로 저장합니다.

::: sidenote
*컬렉션 프록시(Collection proxy)* 컴포넌트는 컬렉션을 기반으로 별도의 물리 월드를 포함하는 새 게임 월드를 만드는 데 사용됩니다. 새 월드는 새 소켓을 통해 액세스합니다. 컬렉션에 포함된 모든 에셋은 로딩을 시작하라는 메세지를 프록시에 보내면 프록시를 통해 로드됩니다. 따라서 게임에서 레벨을 변경하는 경우 등에 매우 유용합니다. 다만 새 게임 월드는 꽤 많은 오버헤드를 수반하므로 작은 컨텐츠를 동적으로 로드하는 데 사용하지 마세요. 자세한 내용은 [컬렉션 프록시 문서](/manuals/collection-proxy)를 참고하세요.
:::

![스폰할 컬렉션](images/collection_factory/collection.png)

그런 다음 스폰을 처리할 게임 오브젝트에 *Collection factory*를 추가하고, 컴포넌트의 *Prototype*을 "bean.collection"으로 설정합니다.

![컬렉션 팩토리](images/collection_factory/factory.png)

이제 bean과 shield를 스폰하려면 `collectionfactory.create()` 함수를 호출하면 됩니다.

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

이 함수는 5개의 파라미터를 받습니다.

`url`
: 새 게임 오브젝트 집합을 스폰할 컬렉션 팩토리 컴포넌트의 id입니다.

`[position]`
: (선택 사항) 스폰된 게임 오브젝트의 월드 위치입니다. `vector3`이어야 합니다. 위치를 지정하지 않으면 오브젝트는 컬렉션 팩토리 컴포넌트의 위치에 스폰됩니다.

`[rotation]`
: (선택 사항) 새 게임 오브젝트의 월드 회전입니다. `quat`이어야 합니다.

`[properties]`
: (선택 사항) 스폰된 게임 오브젝트를 초기화하는 데 사용되는 `id`-`table` 쌍의 Lua 테이블입니다. 이 테이블을 구성하는 방법은 아래를 참고하세요.

`[scale]`
: (선택 사항) 스폰된 게임 오브젝트의 스케일입니다. 스케일은 모든 축에 균일한 스케일을 지정하는 `number`(0보다 커야 함)로 표현할 수 있습니다. 각 컴포넌트가 해당 축의 스케일을 지정하는 `vector3`를 제공할 수도 있습니다.

`collectionfactory.create()`는 스폰된 게임 오브젝트의 식별자를 테이블로 반환합니다. 테이블 키는 각 오브젝트의 컬렉션-로컬 id 해쉬를 각 오브젝트의 런타임 id에 매핑합니다.

::: sidenote
"bean"과 "shield" 사이의 부모-자식 관계는 반환된 테이블에 반영되지 *않습니다*. 이 관계는 런타임 씬 그래프, 즉 오브젝트가 함께 변형되는 방식에만 존재합니다. 오브젝트의 부모를 다시 지정해도 id는 절대 바뀌지 않습니다.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. `[N]`이 카운터인 접두사 `/collection[N]/`가 id에 추가되어 각 인스턴스를 고유하게 식별합니다.

## 프로퍼티

컬렉션을 스폰할 때, 키가 오브젝트 id이고 값이 설정할 스크립트 프로퍼티 테이블인 테이블을 구성하여 각 게임 오브젝트에 프로퍼티 파라미터를 전달할 수 있습니다.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

"bean.collection"의 "bean" 게임 오브젝트가 "shield" 프로퍼티를 정의한다고 가정합니다. [스크립트 프로퍼티 매뉴얼](/manuals/script-properties)에는 스크립트 프로퍼티에 대한 정보가 있습니다.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end
end
```

## 팩토리 리소스의 동적 로딩

컬렉션 팩토리 프로퍼티에서 *Load Dynamically* 체크박스를 선택하면 엔진은 팩토리와 연결된 리소스의 로딩을 미룹니다.

![동적으로 로드](images/collection_factory/load_dynamically.png)

체크박스를 선택하지 않으면 엔진은 컬렉션 팩토리 컴포넌트가 로드될 때 프로토타입 리소스를 로드하므로 즉시 스폰할 준비가 됩니다.

체크박스를 선택하면 두 가지 방식으로 사용할 수 있습니다.

동기식 로딩
: 오브젝트를 스폰하려는 시점에 [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale])를 호출합니다. 그러면 리소스를 동기식으로 로드한 뒤 새 인스턴스를 스폰하며, 이 과정에서 끊김이 발생할 수 있습니다.

  ```lua
  function init(self)
      -- 컬렉션 팩토리의 부모 컬렉션이 로드될 때는
      -- 팩토리 리소스가 로드되지 않습니다. load를 호출하지 않고
      -- create를 호출하면 리소스가 동기식으로 생성됩니다.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)
      -- 게임 오브젝트를 삭제합니다. 리소스 참조 카운트를 줄입니다.
      -- 이 경우 컬렉션 팩토리 컴포넌트가 참조를 보유하지 않으므로
      -- 리소스가 삭제됩니다.
      go.delete(self.go_ids)

      -- 팩토리가 참조를 보유하지 않으므로 unload를 호출해도
      -- 아무 일도 일어나지 않습니다.
      collectionfactory.unload("#factory")
  end
  ```

비동기식 로딩
: [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function])를 호출해 명시적으로 리소스를 비동기식으로 로드합니다. 리소스를 스폰할 준비가 되면 콜백을 받습니다.

  ```lua
  function load_complete(self, url, result)
      -- 로딩이 완료되어 리소스를 스폰할 준비가 되었습니다.
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- 컬렉션 팩토리의 부모 컬렉션이 로드될 때는
      -- 팩토리 리소스가 로드되지 않습니다. load를 호출하면 리소스가 로드됩니다.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- 게임 오브젝트를 삭제합니다. 리소스 참조 카운트를 줄입니다.
      -- 이 경우 컬렉션 팩토리 컴포넌트가 여전히 참조를 보유하므로
      -- 리소스는 삭제되지 않습니다.
      go.delete(self.go_ids)

      -- unload를 호출하면 팩토리 컴포넌트가 보유한 리소스 참조 카운트가 줄어
      -- 리소스가 제거됩니다.
      collectionfactory.unload("#factory")
  end
  ```


## 동적 프로토타입

컬렉션 팩토리 프로퍼티에서 *Dynamic Prototype* 체크박스를 선택하면 컬렉션 팩토리가 생성할 수 있는 *Prototype*을 변경할 수 있습니다.

![동적 프로토타입](images/collection_factory/dynamic_prototype.png)

*Dynamic Prototype* 옵션을 선택하면 컬렉션 팩토리 컴포넌트는 `collectionfactory.set_prototype()` 함수를 사용해 프로토타입을 변경할 수 있습니다. 예:

```lua
collectionfactory.unload("#factory") -- 이전 리소스 언로드
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
*Dynamic Prototype* 옵션이 설정되면 컬렉션 컴포넌트 수를 최적화할 수 없으며, 해당 컬렉션은 *game.project* 파일의 기본 컴포넌트 수를 사용합니다.
:::
