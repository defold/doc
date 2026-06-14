---
title: Flash 사용자를 위한 Defold
brief: 이 가이드는 Flash 게임 개발자를 위한 대안으로 Defold를 소개합니다. Flash 게임 개발에서 사용하는 주요 컨셉 일부를 다루고, Defold에서 이에 해당하는 도구와 방법을 설명합니다.
---

# Flash 사용자를 위한 Defold

이 가이드는 Flash 게임 개발자를 위한 대안으로 Defold를 소개합니다. Flash 게임 개발에서 사용하는 주요 컨셉 일부를 다루고, Defold에서 이에 해당하는 도구와 방법을 설명합니다.

## 소개

Flash의 주요 장점 중 하나는 접근성이 좋고 진입 장벽이 낮다는 점이었습니다. 신규 사용자는 프로그램을 빠르게 배울 수 있었고, 적은 시간 투자로 기본적인 게임을 만들 수 있었습니다. Defold도 게임 디자인 전용 도구 모음을 제공해 비슷한 장점을 제공하며, 동시에 고급 개발자가 더 정교한 요구사항에 맞는 고급 솔루션을 만들 수 있게 합니다. 예를 들어 개발자는 기본 렌더 스크립트를 편집할 수 있습니다.

Flash 게임은 ActionScript(가장 최근 버전은 3.0)로 프로그래밍하지만, Defold 스크립팅은 Lua로 작성합니다. 이 가이드에서는 Lua와 ActionScript 3.0을 자세히 비교하지 않습니다. [Defold 매뉴얼](/manuals/lua)은 Defold에서 Lua 프로그래밍을 시작하기 좋은 소개를 제공하며, 온라인에서 무료로 볼 수 있는 매우 유용한 [Programming in Lua](https://www.lua.org/pil/)(초판)를 참조합니다.

Jesse Warden의 글에는 [ActionScript와 Lua의 기본 비교](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html)가 있으며, 좋은 출발점이 될 수 있습니다. 다만 Defold와 Flash가 구성되는 방식에는 언어 수준에서 보이는 것보다 더 깊은 차이가 있습니다. ActionScript와 Flash는 클래스와 상속을 사용하는 전통적인 의미의 객체 지향 방식입니다. Defold에는 클래스도 상속도 없습니다. 대신 오디오비주얼 표현, 동작, 데이터를 포함할 수 있는 *게임 오브젝트(game object)* 개념이 있습니다. 게임 오브젝트에 대한 작업은 Defold API에서 제공하는 *함수*로 수행합니다. 또한 Defold는 오브젝트 간 통신에 *메세지*를 사용하도록 권장합니다. 메세지는 메서드 호출보다 높은 수준의 구성요소이며, 메서드 호출처럼 사용하도록 의도된 것이 아닙니다. 이러한 차이는 중요하고 익숙해지는 데 시간이 걸리지만, 이 가이드에서 자세히 다루지는 않습니다.

대신 이 가이드는 Flash 게임 개발의 주요 컨셉 일부를 살펴보고, Defold에서 가장 가까운 대응 개념이 무엇인지 개략적으로 설명합니다. Flash에서 Defold로 전환할 때 빠르게 시작할 수 있도록 유사점과 차이점, 흔한 함정을 함께 다룹니다.

## 무비 클립과 게임 오브젝트

무비 클립은 Flash 게임 개발의 핵심 컴포넌트입니다. 무비 클립은 심볼이며, 각각 고유한 타임라인을 포함합니다. Defold에서 가장 가까운 대응 개념은 게임 오브젝트입니다.

![게임 오브젝트와 무비 클립](images/flash/go_movieclip.png)

Flash 무비 클립과 달리 Defold 게임 오브젝트에는 타임라인이 없습니다. 대신 게임 오브젝트는 여러 컴포넌트로 구성됩니다. 컴포넌트에는 스프라이트, 사운드, 스크립트 등이 포함됩니다. 사용 가능한 컴포넌트에 대한 자세한 내용은 [빌딩 블록 문서](/manuals/building-blocks)와 관련 글을 참고하세요. 아래 스크린샷의 게임 오브젝트는 스프라이트와 스크립트로 구성되어 있습니다. 스크립트 컴포넌트는 오브젝트의 라이프사이클 전체에서 게임 오브젝트의 동작과 모습을 제어하는 데 사용됩니다.

![스크립트 컴포넌트](images/flash/script_component.png)

무비 클립은 다른 무비 클립을 포함할 수 있지만, 게임 오브젝트는 게임 오브젝트를 *포함*할 수 없습니다. 하지만 게임 오브젝트는 다른 게임 오브젝트의 *자식*으로 연결할 수 있으며, 이렇게 하면 함께 이동, 스케일 변경, 회전할 수 있는 계층구조를 만들 수 있습니다.

## Flash—수동으로 무비 클립 생성하기

Flash에서는 무비 클립 인스턴스를 라이브러리에서 타임라인으로 드래그해 씬에 수동으로 추가할 수 있습니다. 아래 스크린샷은 각 Flash 로고가 "logo" 무비 클립의 인스턴스인 상황을 보여줍니다.

![수동 무비 클립](images/flash/manual_movie_clips.png)

## Defold—수동으로 게임 오브젝트 생성하기

앞서 언급했듯이 Defold에는 타임라인 개념이 없습니다. 대신 게임 오브젝트는 컬렉션 안에 구성됩니다. 컬렉션은 게임 오브젝트와 다른 컬렉션을 담는 컨테이너(또는 prefab)입니다. 가장 기본적인 수준에서는 게임이 컬렉션 하나만으로 구성될 수 있습니다. 더 흔하게는 Defold 게임이 여러 컬렉션을 사용하며, 이 컬렉션들은 부트스트랩 "main" 컬렉션에 수동으로 추가되거나 [컬렉션 프록시](/manuals/collection-proxy)를 통해 동적으로 로드됩니다. "levels" 또는 "screens"를 로드하는 이런 개념에는 Flash에서 직접 대응되는 것이 없습니다.

아래 예제에서 "main" 컬렉션은 "logo" 게임 오브젝트(왼쪽 *Assets* 브라우저 창에 보임)의 인스턴스 세 개(오른쪽 *Outline* 창에 나열됨)를 포함합니다.

![수동 게임 오브젝트](images/flash/manual_game_objects.png)

## Flash—수동으로 생성한 무비 클립 참조하기

Flash에서 수동으로 생성한 무비 클립을 참조하려면 직접 정의한 인스턴스 이름을 사용해야 합니다.

![flash 인스턴스 이름](images/flash/flash_instance_name.png)

## Defold—게임 오브젝트 id

Defold에서는 모든 게임 오브젝트와 컴포넌트를 주소를 통해 참조합니다. 대부분의 경우 간단한 이름이나 축약형만으로 충분합니다. 예를 들면 다음과 같습니다.

- `"."`는 현재 게임 오브젝트를 가리킵니다.
- `"#"`는 현재 컴포넌트(스크립트)를 가리킵니다.
- `"logo"`는 id가 "logo"인 게임 오브젝트를 가리킵니다.
- `"#script"`는 현재 게임 오브젝트 안에서 id가 "script"인 컴포넌트를 가리킵니다.
- `"logo#script"`는 id가 "logo"인 게임 오브젝트 안에서 id가 "script"인 컴포넌트를 가리킵니다.

수동으로 배치한 게임 오브젝트의 주소는 할당된 *Id* 프로퍼티로 결정됩니다(스크린샷 오른쪽 아래 참고). id는 현재 작업 중인 컬렉션 파일 안에서 고유해야 합니다. 에디터는 id를 자동으로 설정하지만, 생성하는 각 게임 오브젝트 인스턴스마다 변경할 수 있습니다.

![게임 오브젝트 id](images/flash/game_object_id.png)

::: sidenote
게임 오브젝트의 id는 해당 스크립트 컴포넌트에서 다음 코드를 실행해 확인할 수 있습니다. `print(go.get_id())`. 이 코드는 현재 게임 오브젝트의 id를 콘솔에 출력합니다.
:::

주소 지정 모델과 메세지 전달은 Defold 게임 개발의 핵심 컨셉입니다. [주소 지정 매뉴얼](/manuals/addressing)과 [메세지 전달 매뉴얼](/manuals/message-passing)에서 이를 자세히 설명합니다.

## Flash—동적으로 무비 클립 생성하기

Flash에서 무비 클립을 동적으로 생성하려면 먼저 ActionScript Linkage를 설정해야 합니다.

![actionscript linkage](images/flash/actionscript_linkage.png)

그러면 클래스(이 경우 Logo)가 만들어지고, 이 클래스의 새 인스턴스를 인스턴스화할 수 있습니다. Logo 클래스의 인스턴스를 Stage에 추가하는 작업은 아래처럼 할 수 있습니다.

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold—팩토리를 사용해 게임 오브젝트 생성하기

Defold에서는 *팩토리*를 사용해 게임 오브젝트를 동적으로 생성합니다. 팩토리는 특정 게임 오브젝트의 복사본을 스폰하는 데 사용되는 컴포넌트입니다. 이 예제에서는 "logo" 게임 오브젝트를 프로토타입으로 사용하는 팩토리를 만들었습니다.

![logo 팩토리](images/flash/logo_factory.png)

모든 컴포넌트와 마찬가지로 팩토리도 사용하기 전에 게임 오브젝트에 추가해야 한다는 점이 중요합니다. 이 예제에서는 팩토리 컴포넌트를 담기 위해 "factories"라는 게임 오브젝트를 만들었습니다.

![팩토리 컴포넌트](images/flash/factory_component.png)

logo 게임 오브젝트의 인스턴스를 생성하기 위해 호출할 함수는 다음과 같습니다.

```lua
local logo_id = factory.create("factories#logo_factory")
```

URL은 `factory.create()`의 필수 파라미터입니다. 또한 위치, 회전, 프로퍼티, 스케일을 설정하기 위한 선택 파라미터를 추가할 수 있습니다. 팩토리 컴포넌트에 대한 자세한 내용은 [팩토리 매뉴얼](/manuals/factory)을 참고하세요. `factory.create()`를 호출하면 생성된 게임 오브젝트의 id가 반환된다는 점도 알아둘 만합니다. 이 id는 나중에 참조할 수 있도록 테이블(배열에 해당하는 Lua의 자료구조)에 저장할 수 있습니다.

## Flash—stage

Flash에서는 Timeline(아래 스크린샷의 위쪽 영역)과 Stage(Timeline 아래에 보이는 영역)에 익숙합니다.

![timeline과 stage](images/flash/stage.png)

위의 무비 클립 섹션에서 설명했듯이 Stage는 기본적으로 Flash 게임의 최상위 컨테이너이며, 프로젝트를 익스포트할 때마다 생성됩니다. Stage에는 기본적으로 하나의 자식인 *`MainTimeline`*이 있습니다. 프로젝트에서 생성되는 각 무비 클립에는 자체 타임라인이 있으며, 다른 심볼(무비 클립 포함)을 담는 컨테이너 역할을 할 수 있습니다.

## Defold—컬렉션

Flash Stage에 해당하는 Defold 개념은 컬렉션입니다. 엔진이 시작되면 컬렉션 파일의 컨텐츠를 기반으로 새 게임 월드를 만듭니다. 기본적으로 이 파일의 이름은 "main.collection"이지만, 모든 Defold 프로젝트의 루트에 있는 *game.project* 설정 파일에 접근해 시작 시 로드할 컬렉션을 변경할 수 있습니다.

![game.project](images/flash/game_project.png)

컬렉션은 에디터에서 게임 오브젝트와 다른 컬렉션을 구성하는 데 사용되는 컨테이너입니다. 컬렉션의 컨텐츠는 일반 게임 오브젝트 팩토리와 같은 방식으로 동작하는 [컬렉션 팩토리](/manuals/collection-factory/#spawning-a-collection)를 사용해 스크립트에서 런타임으로 스폰할 수도 있습니다. 이는 예를 들어 적 무리나 코인 수집 아이템 패턴을 스폰할 때 유용합니다. 아래 스크린샷에서는 "logos" 컬렉션의 인스턴스 두 개를 "main" 컬렉션 안에 수동으로 배치했습니다.

![컬렉션](images/flash/collection.png)

경우에 따라 완전히 새로운 게임 월드를 로드해야 할 수 있습니다. [컬렉션 프록시](/manuals/collection-proxy/) 컴포넌트를 사용하면 컬렉션 파일의 컨텐츠를 기반으로 새 게임 월드를 만들 수 있습니다. 이는 새 게임 레벨, 미니 게임, 컷씬을 로드하는 등의 상황에 유용합니다.

## Flash—timeline

Flash 타임라인은 주로 다양한 프레임별 기법이나 shape/motion tween을 사용한 애니메이션에 사용됩니다. 프로젝트의 전체 FPS(frames per second) 설정은 프레임이 표시되는 시간을 정의합니다. 고급 사용자는 게임 전체의 FPS나 개별 무비 클립의 FPS까지 수정할 수 있습니다.

Shape tween은 두 상태 사이의 벡터 그래픽 보간을 허용합니다. 아래에서 사각형을 삼각형으로 shape tweening하는 예제처럼, 대부분 단순한 도형과 용도에만 유용합니다.

![timeline](images/flash/timeline.png)

Motion tween은 크기, 위치, 회전 등 오브젝트의 여러 프로퍼티에 애니메이션을 적용할 수 있게 합니다. 아래 예제에서는 나열된 모든 프로퍼티가 수정되었습니다.

![motion tween](images/flash/tween.png)

## Defold—프로퍼티 애니메이션

Defold는 벡터 그래픽이 아니라 픽셀 이미지를 사용하므로 shape tweening에 해당하는 기능이 없습니다. 하지만 motion tweening에는 [프로퍼티 애니메이션](/ref/go/#go.animate)이라는 강력한 대응 기능이 있습니다. 이는 `go.animate()` 함수를 사용해 스크립트로 수행합니다. `go.animate()` 함수는 사용할 수 있는 여러 easing 함수(커스텀 함수 포함) 중 하나를 사용해 프로퍼티(색상, 스케일, 회전, 위치 등)를 시작 값에서 원하는 종료 값으로 보간합니다. Flash에서는 더 고급 easing 함수를 사용자가 직접 구현해야 했지만, Defold에는 엔진에 내장된 [많은 easing 함수](/manuals/property-animation/#easing)가 포함되어 있습니다.

Flash가 애니메이션을 위해 타임라인의 그래픽 키프레임을 사용하는 반면, Defold에서 그래픽 애니메이션을 만드는 주요 방법 중 하나는 임포트한 이미지 시퀀스의 플립북 애니메이션입니다. 애니메이션은 아틀라스라는 게임 오브젝트 컴포넌트 안에 구성됩니다. 이 예제에는 "run"이라는 애니메이션 시퀀스를 가진 게임 캐릭터용 아틀라스가 있습니다. 이 시퀀스는 일련의 png 파일로 구성됩니다.

![플립북](images/flash/flipbook.png)

## Flash—깊이 인덱스

Flash에서는 디스플레이 리스트가 무엇을 어떤 순서로 표시할지 결정합니다. 컨테이너(Stage 등) 안의 오브젝트 순서는 인덱스로 처리됩니다. `addChild()` 메서드를 사용해 컨테이너에 추가된 오브젝트는 자동으로 인덱스의 맨 위 위치를 차지하며, 0부터 시작해 오브젝트가 추가될 때마다 증가합니다. 아래 스크린샷에서는 "logo" 무비 클립의 인스턴스 세 개를 생성했습니다.

![깊이 인덱스](images/flash/depth_index.png)

디스플레이 리스트의 위치는 각 로고 인스턴스 옆의 숫자로 표시됩니다. 무비 클립의 x/y 위치를 처리하는 코드를 제외하면, 위 상태는 다음처럼 생성할 수 있습니다.

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

어떤 오브젝트가 다른 오브젝트보다 위나 아래에 표시되는지는 디스플레이 리스트 인덱스에서의 상대 위치로 결정됩니다. 예를 들어 두 오브젝트의 인덱스 위치를 바꾸면 이를 잘 확인할 수 있습니다.

```as
swapChildren(logo2,logo3);
```

결과는 아래처럼 보입니다(인덱스 위치가 갱신됨).

![깊이 인덱스](images/flash/depth_index_2.png)

## Defold—z 포지션

Defold에서 게임 오브젝트의 포지션은 x, y, z 세 변수로 구성된 벡터로 표현됩니다. z 포지션은 게임 오브젝트의 깊이를 결정합니다. 기본 [렌더 스크립트](/manuals/render)에서 사용할 수 있는 z 포지션 범위는 -1부터 1까지입니다.

::: sidenote
z 포지션이 -1부터 1까지의 범위 밖에 있는 게임 오브젝트는 렌더링되지 않으므로 보이지 않습니다. 이는 Defold를 처음 접하는 개발자가 흔히 겪는 함정이며, 게임 오브젝트가 보여야 할 때 보이지 않는다면 기억해 둘 만합니다.
:::

Flash에서는 에디터가 깊이 인덱싱을 암시적으로만 보여주고 *Bring Forward*와 *Send Backward* 같은 명령으로 수정할 수 있지만, Defold에서는 에디터에서 오브젝트의 z 포지션을 직접 설정할 수 있습니다. 아래 스크린샷에서는 "logo3"가 맨 위에 표시되며 z 포지션이 0.2인 것을 볼 수 있습니다. 다른 게임 오브젝트의 z 포지션은 0.0과 0.1입니다.

![z-order](images/flash/z_order.png)

하나 이상의 컬렉션 안에 중첩된 게임 오브젝트의 z 포지션은 자체 z 포지션과 모든 부모의 z 포지션을 합쳐 결정된다는 점에 유의하세요. 예를 들어 위의 logo 게임 오브젝트가 "logos" 컬렉션 안에 배치되고, 그 "logos" 컬렉션이 다시 "main" 안에 배치되었다고 가정해 보겠습니다(아래 스크린샷 참고). "logos" 컬렉션의 z 포지션이 0.9라면, 그 안에 포함된 게임 오브젝트들의 z 포지션은 0.9, 1.0, 1.1이 됩니다. 따라서 "logo3"는 z 포지션이 1보다 크므로 렌더링되지 않습니다.

![z-order](images/flash/z_order_outline.png)

물론 게임 오브젝트의 z 포지션은 스크립트로 변경할 수 있습니다. 아래 코드가 게임 오브젝트의 스크립트 컴포넌트 안에 있다고 가정합니다.

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Flash `hitTestObject`와 `hitTestPoint` 충돌 감지

Flash의 기본 충돌 감지는 `hitTestObject()` 메서드를 사용해 수행합니다. 이 예제에는 "bullet"과 "bullseye"라는 무비 클립 두 개가 있습니다. 아래 스크린샷이 이를 보여줍니다. 파란 경계 박스는 Flash 에디터에서 심볼을 선택할 때 보이며, 이 경계 박스가 `hitTestObject()` 메서드의 결과를 결정합니다.

![hit test](images/flash/hittest.png)

`hitTestObject()`를 사용한 충돌 감지는 다음과 같이 수행합니다.

```as
bullet.hitTestObject(bullseye);
```

이 경우 경계 박스를 사용하는 것은 적절하지 않습니다. 아래 상황에서도 히트가 등록되기 때문입니다.

![hit test 경계 박스](images/flash/hitboundingbox.png)

`hitTestObject()`의 대안은 `hitTestPoint()` 메서드입니다. 이 메서드에는 `shapeFlag` 파라미터가 있으며, 이를 사용하면 경계 박스가 아니라 오브젝트의 실제 픽셀을 대상으로 히트 테스트를 수행할 수 있습니다. `hitTestPoint()`를 사용한 충돌 감지는 아래처럼 할 수 있습니다.

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

이 줄은 bullet의 x, y 위치(이 상황에서는 왼쪽 위)를 타겟의 shape와 비교해 검사합니다. `hitTestPoint()`는 점을 shape와 비교해 검사하므로, 어떤 점(또는 점들!)을 검사할지가 중요한 고려사항입니다.

## Defold—충돌 오브젝트

Defold에는 충돌을 감지하고 스크립트가 이에 반응할 수 있게 하는 물리 엔진이 포함되어 있습니다. Defold의 충돌 감지는 게임 오브젝트에 충돌 오브젝트 컴포넌트를 할당하는 것에서 시작합니다. 아래 스크린샷에서는 "bullet" 게임 오브젝트에 충돌 오브젝트를 추가했습니다. 충돌 오브젝트는 빨간색 투명 박스로 표시됩니다(에디터에서만 보임).

![충돌 오브젝트](images/flash/collision_object.png)

Defold에는 사실적인 충돌을 자동으로 시뮬레이션할 수 있는 Box2D 물리 엔진의 수정 버전이 포함되어 있습니다. 이 가이드는 Flash의 충돌 감지와 가장 비슷한 Kinematic 충돌 오브젝트를 사용한다고 가정합니다. Dynamic 충돌 오브젝트에 대한 자세한 내용은 Defold [물리 매뉴얼](/manuals/physics)을 읽어보세요.

충돌 오브젝트에는 다음 프로퍼티가 포함됩니다.

![충돌 오브젝트 프로퍼티](images/flash/collision_object_properties.png)

bullet 그래픽에 가장 적합했기 때문에 box shape를 사용했습니다. 2D 충돌에 사용되는 다른 shape인 sphere는 타겟에 사용합니다. 타입을 Kinematic으로 설정하면 내장 물리 엔진이 아니라 스크립트가 충돌 해결을 수행한다는 뜻입니다(다른 타입에 대한 자세한 내용은 [물리 매뉴얼](/manuals/physics)을 참고하세요). *Group*과 *Mask* 프로퍼티는 각각 오브젝트가 어떤 충돌 그룹에 속하는지, 그리고 어떤 충돌 그룹을 대상으로 검사해야 하는지를 결정합니다. 현재 설정에서는 "bullet"이 "target"과만 충돌할 수 있습니다. 설정이 아래처럼 변경되었다고 가정해 보겠습니다.

![충돌 group/mask](images/flash/collision_groupmask.png)

이제 bullet은 target 및 다른 bullet과 충돌할 수 있습니다. 참고로 타겟에는 다음과 같은 충돌 오브젝트를 설정했습니다.

![bullet 충돌 오브젝트](images/flash/collision_object_bullet.png)

*Group* 프로퍼티가 "target"으로 설정되어 있고 *Mask*가 "bullet"으로 설정되어 있는 점에 주목하세요.

Flash에서는 스크립트가 명시적으로 호출할 때만 충돌 감지가 발생합니다. Defold에서는 충돌 오브젝트가 활성화되어 있는 한 충돌 감지가 백그라운드에서 계속 발생합니다. 충돌이 발생하면 게임 오브젝트의 모든 컴포넌트(가장 관련이 큰 것은 스크립트 컴포넌트)에 메세지가 전송됩니다. 이 메세지는 [`collision_response`와 `contact_point_response`](/manuals/physics-messages)이며, 원하는 방식으로 충돌을 해결하는 데 필요한 모든 정보를 포함합니다.

Defold 충돌 감지의 장점은 Flash보다 더 고급 기능을 제공한다는 점입니다. 비교적 복잡한 shape 간 충돌을 매우 적은 설정 작업만으로 감지할 수 있습니다. 충돌 감지는 자동으로 수행되므로, 서로 다른 충돌 그룹의 여러 오브젝트를 반복해서 순회하며 명시적으로 히트 테스트를 수행할 필요가 없습니다. 주요 단점은 Flash의 `shapeFlag`에 해당하는 기능이 없다는 점입니다. 하지만 대부분의 용도에는 기본 box와 sphere shape의 조합으로 충분합니다. 더 복잡한 상황에서는 커스텀 shape도 [가능합니다](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash—이벤트 처리

이벤트 오브젝트와 연결된 리스너는 여러 이벤트(예: 마우스 클릭, 버튼 누름, 클립 로드)를 감지하고 그에 대한 응답으로 동작을 실행하는 데 사용됩니다. 사용할 수 있는 이벤트는 다양합니다.

## Defold—콜백 함수와 메세징

Flash 이벤트 처리 시스템에 해당하는 Defold의 기능은 몇 가지 요소로 구성됩니다. 먼저 각 스크립트 컴포넌트에는 특정 이벤트를 감지하는 콜백 함수 세트가 있습니다. 다음과 같습니다.

init
:   스크립트 컴포넌트가 초기화될 때 호출됩니다. Flash의 생성자 함수에 해당합니다.

final
:   스크립트 컴포넌트가 삭제될 때 호출됩니다(예: 스폰된 게임 오브젝트가 제거됨).

update
:   매 프레임 호출됩니다. Flash의 `enterFrame`에 해당합니다.

on_message
:   스크립트 컴포넌트가 메세지를 받을 때 호출됩니다.

on_input
:   사용자 입력(예: 마우스 또는 키보드)이 [입력 포커스](/ref/go/#acquire_input_focus)를 가진 게임 오브젝트로 전송될 때 호출됩니다. 입력 포커스가 있다는 것은 해당 오브젝트가 모든 입력을 받고 이에 반응할 수 있다는 뜻입니다.

on_reload
:   스크립트 컴포넌트가 리로드될 때 호출됩니다.

위에 나열된 콜백 함수는 모두 선택 사항이며, 사용하지 않으면 제거할 수 있습니다. 입력 설정 방법에 대한 자세한 내용은 [입력 매뉴얼](/manuals/input)을 참고하세요. 컬렉션 프록시로 작업할 때 흔한 함정이 있으므로, 자세한 내용은 입력 매뉴얼의 [이 섹션](/manuals/input/#input-dispatch-and-on_input)을 참고하세요.

충돌 감지 섹션에서 설명했듯이 충돌 이벤트는 관련된 게임 오브젝트로 메세지를 보내 처리합니다. 각각의 스크립트 컴포넌트는 `on_message` 콜백 함수에서 메세지를 받습니다.

## Flash—버튼 심볼

Flash는 버튼 전용 심볼 타입을 사용합니다. 버튼은 사용자 상호작용이 감지될 때 동작을 실행하기 위해 특정 이벤트 핸들러 메서드(예: `click`, `buttonDown`)를 사용합니다. 버튼 심볼의 "Hit" 섹션에 있는 버튼의 그래픽 shape가 버튼의 히트 영역을 결정합니다.

![버튼](images/flash/button.png)

## Defold—GUI 씬과 스크립트

Defold에는 네이티브 버튼 컴포넌트가 없으며, Flash에서 버튼을 처리하는 방식처럼 특정 게임 오브젝트의 shape에 대해 클릭을 쉽게 감지할 수도 없습니다. 가장 일반적인 해결책은 [GUI](/manuals/gui) 컴포넌트를 사용하는 것입니다. 이는 부분적으로 Defold GUI 컴포넌트의 위치가 게임 내 카메라(사용 중인 경우)의 영향을 받지 않기 때문입니다. 또한 GUI API에는 클릭이나 터치 이벤트 같은 사용자 입력이 GUI 요소의 경계 안에 있는지 감지하는 함수가 포함되어 있습니다.

## 디버깅

Flash에서 디버깅할 때는 `trace()` 명령이 유용합니다. Defold에서 이에 해당하는 것은 `print()`이며, `trace()`와 같은 방식으로 사용합니다.

```lua
print("Hello world!"")
```

하나의 `print()` 함수를 사용해 여러 변수를 출력할 수 있습니다.

```lua
print(score, health, ammo)
```

테이블을 다룰 때 유용한 `pprint()` 함수(pretty print)도 있습니다. 이 함수는 중첩된 테이블을 포함해 테이블의 내용을 출력합니다. 아래 스크립트를 생각해 보겠습니다.

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

여기에는 테이블(`world`) 안에 중첩된 테이블(`factions`)이 포함되어 있습니다. 일반 `print()` 명령을 사용하면 테이블의 고유 id는 출력되지만 실제 내용은 출력되지 않습니다.

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

위에서 보인 것처럼 `pprint()` 함수를 사용하면 더 의미 있는 결과를 얻을 수 있습니다.

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

게임에서 충돌 감지를 사용한다면 아래 메세지를 게시해 physics debugging을 토글할 수 있습니다.

```lua
msg.post("@system:", "toggle_physics_debug")
```

Physics debug는 프로젝트 설정에서도 활성화할 수 있습니다. physics debug를 토글하기 전의 프로젝트는 다음과 같습니다.

![디버그 없음](images/flash/no_debug.png)

physics debug를 토글하면 게임 오브젝트에 추가된 충돌 오브젝트가 표시됩니다.

![디버그 있음](images/flash/with_debug.png)

충돌이 발생하면 관련 충돌 오브젝트가 밝게 표시됩니다. 또한 충돌 벡터도 표시됩니다.

![충돌](images/flash/collision.png)

마지막으로 CPU와 메모리 사용량을 모니터링하는 방법은 [프로파일러 문서](/ref/profiler/)를 참고하세요. 고급 디버깅 기법에 대한 자세한 내용은 Defold 매뉴얼의 [디버깅 섹션](/manuals/debugging)을 참고하세요.

## 다음 단계

- [Defold 예제](/examples)
- [튜토리얼](/tutorials)
- [매뉴얼](/manuals)
- [레퍼런스](/ref/go)
- [FAQ](/faq/faq)

질문이 있거나 막히는 부분이 있다면 [Defold 포럼](//forum.defold.com)에서 도움을 요청해 보세요.
