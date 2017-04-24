# Collection factories
컬렉션 팩토리 컴포넌트는 게임 오브젝트(컬렉션)의 설계도면 계층구조(blueprint hierarchies)를 만들어 실행중인 게임으로 스폰하는데 사용됩니다. 이 매뉴얼은 컬렉션 팩토리가 어떻게 동작하며 어떻게 사용하면 되는지 설명합니다.

컬렉션은 재사용 가능한 템플릿(프리펩(prefab) 같은)을 생성하기 위한 강력한 메커니즘을 제공합니다. 컬렉션에 대한 개요를 보고 싶다면 [Building blocks](/manuals/building-blocks) 문서를 참고 바랍니다. 컬렉션은 에디터상에서 배치해도 되고 컴파일 타임에 게임으로 복제할 수도 있는데, 동적으로 게임에 추가하는 방법으로는 아래 두 가지가 있습니다.

1. 컬렉션 프록시(Collection proxy)를 통해 로드하는 방법. 이 방법은 근본적으로 고립된 새 월드(new isolated world)(물리 반응 방식을 포함함)를 실행중인 게임에 불러옵니다. 로드된 컬렉션은 새 소켓 으로 엑세스할 수 있으며, 컬렉션에 포함된 모든 에셋은 프록시가 로딩을 시작한다는 메세지를 받으면 프록시를 통해 로드됩니다. 이 방식은 레벨 스테이지를 변경하려는 경우에 아주 유용하게 사용됩니다. 더 많은 정보를 알고 싶다면 [Collection proxy](/manuals/collection-proxy) 문서를 참고 바랍니다.

2. 컬렉션 팩토리(Collection factory) 컴포넌트는  현재의 메인 컬렉션에 컬렉션 프록시의 컨텐츠를 스폰 할 수 있게 해줍니다. 이 방식은 마치 어떤 컬렉션 안에 있는 모든 오브젝트들에게 일일히 팩토리(factory) 컴포넌트를 넣어서 오브젝트간 부-모 계층을 만드는 방식과 유사합니다. 일반적인 사용처로는 게임 오브젝트가 여러 개의 게임 오브젝트로 구성된 적(enemy: 몸체+무기) 같은 개체를 스폰하는데 유용합니다.

## Spawning a collection
컬렉션을 스폰 하는 것은 게임 오브젝트를 스폰하는 방식과 똑같이 수행됩니다. 간단한 예를 들자면, 우리가 행성 스프라이트를 만들고 이 행성 표면에 복합적인 게임 오브젝트로 구성된 우주인 모형 여러 개를 스폰해야 한다고 칩시다. 우리는 그냥 컬렉션 프록시(**Collection factory**)를 "planet" 게임오브젝트에 추가하고 **Prototype** 속성을 "astronaut.collection" (일단 존재한다고 치고)으로 설정하면 됩니다.

![Collection factory](images/collection_factory/collection_factory_factory.png)

이번엔 팩토리에게 우주인을 스폰하라는 메세지를 보내면 됩니다.

```lua
local astro = collectionfactory.create("#factory", nil, nil, {}, nil)
```
스폰된 우주인은 게임 오브젝트들의 트리구조로 되어 있으며, 스폰 이후에 이 오브젝트들을 다루기 위한 주소를 받을 수 있습니다.

![Collection to spawn](images/collection_factory/collection_factory_collection.png)

보통의 팩토리 컴포넌트라면 스폰된 오브젝트의 아이디(id)를 반환하지만, 컬렉션 팩토리는 각 오브젝트들의 런타임 아이디를 컬렉션명-로컬명(collection-local id)의 해쉬값으로 만들고 이들을 테이블에 매핑해 반환합니다. 접두사 "/collectionNN/" 가 각 아이디에 추가되어 각 인스턴스를 유니크하게 식별해 줍니다.

```lua
pprint(astro)
-- DEBUG:SCRIPT:
-- {
--   hash: [/probe2] = hash: [/collection0/probe2],
--   hash: [/probe1] = hash: [/collection0/probe1],
--   hash: [/astronaut] = hash: [/collection0/astronaut],
-- }
```

"astronaut"과 "probe" 사이의 부-모 관계는 오브젝트의 id/path 에 영향을 주지 않지만 런타임시에 씬-그래프(scene-graph)에서는 영향을 줍니다. 예를 들면 부-모 관계의 오브젝트들을 함께 트랜스폼(이동,회전,스케일)하거나 오브젝트의 부-모를 재설정하는 것으로는 절대 id가 바뀌지 않습니다.

## Properties
컬렉션을 스폰 할 때, 컬렉션-로컬(collection-local) 오브젝트 아이디가 쌍(pair)으로 구성된 테이블을 사용하여 각각의 부분 게임 오브젝트에게 적당한 파라미터를 보낼 수 있으며, 이는 각 스크립트 속성을 셋팅합니다.

```lua
-- planet.script
--
local props = {}
props[hash("/astronaut")] = { size = 10.0 }
props[hash("/probe1")] = { color = hash("red") }
props[hash("/probe2")] = { color = hash("green") }
local astro = collectionfactory.create("#factory", nil, nil, props, nil)
...
```
"astronaut"가 스폰된 각각의 인스턴스들은 넘겨진 값으로 "size" 속성을 셋팅하게 되고, 각 "probe" 들은 "color" 속성이 셋팅됩니다.

```lua
-- probe.script
--
go.property("color", hash("blue"))

function init(self)
  ...
```

우주인 여러 명을 스폰하고 적당히 배치하여 알맞은 속성 값들을 보내면, 아래처럼 사랑이 넘치는 행성을 만들 수 있습니다.

![Populated planet](images/collection_factory/collection_factory_game.png)

