# Welcome to Defold
Defold에 오신 것을 환영합니다. 이 메뉴얼은 Defold의 핵심 컨셉을 다루며, 가장 중요한 기능에 대한 개요를 알려드리려 합니다. 모든 설명은 간단하게 제공되며, 자세한 내용은 링크를 통해 확인 바랍니다.

## Philosophy(철학)
Defold는 단순함과 명료함을 철학으로 디자인 되었으며, 턴키(turn-key)방식의 생산 플랫폼이지만, 모든 것을 제작하는 도구는 아닙니다. 대신 우리는 Defold가 게임 제작자들에게 독창적인 비전을 실현할 수 있게끔 쉽고, 강력한 도구로서 힘을 실어 줄 수 있을 것으로 믿고 있습니다.

때로는 더 많은 작업이 들어갈 수도 있지만, 우리의 철학적 목표는 분명합니다. 준비된 솔루션이 완벽히 들어맞는 경우는 좀처럼 드물며 모든 게임 제작자들에게 정확하게 필요한 도구를 제공하는것은 어렵거나 불가능합니다.

당신이 경험있는 개발자라면, 아마 Defold의 핵심 컨셉을 쉽게 이해할 수 있을 것입니다. 하지만 심플함에도 불구하고 우리의 컨셉 일부는 당신이 처음 예상했던 것과는 다를 수 있으므로 주의깊게 읽어 주시기 바랍니다.

## Scripts
스크립트는 게임 오브젝트의 동작을 정의하는 프로그램을 포함하고 있는 컴포넌트입니다. 스크립트를 이용하여 당신은 오브젝트들(플레이어나 다른 오브젝트들 까지도)이 어떻게 다양한 상호작용으로 반응 해야 하는지 등의 게임 규칙을 명시 할 수 있습니다. 모든 스크립트는 Lua(루아)로 프로그래밍 됩니다. Defold를 사용하기 위해서, 당신이나 당신의 팀원들은 Lua 프로그래밍을 공부할 필요가 있습니다. 더 많은 정보가 필요하면 디폴드의 Lua 문서를 읽어 보시기 바랍니다.

오브젝트간에 의사소통을 위해서 Defold는 Message passing(메세지 전달)을 통해 Lua를 확장합니다. 또한 Defold는 유용한 함수 라이브러리를 제공합니다.

예를 들어, 게임 오브젝트로부터 폭파 사운드를 내는 Lua 코드는 다음과 같습니다. :

    msg.post("#explosion", "play_sound")

여기서 "explosion"은 스크립트가 위치한 오브젝트의 사운드 컴포넌트 이름입니다. "play_sound"는 사운드 컴포넌트가 반응할 메세지입니다. 이것은 컴포넌트간 어떻게 소통하는지 Message passing의 간단한 예제입니다. 여기서 스크립트와 오브젝트 사이에 데이터는 공유되지 않고 있습니다. 컴포넌트(스크립트를 포함한)는 오직 msg.post() 함수를 사용해서 메세지를 넘길 뿐입니다.

## Messages
컴포넌트는 메세지 전달을 통해 각기 다른 시스템과 의사소통합니다. 또한 컴포넌트는 특정한 동작을 trigger(트리거)하거나 변경하는 미리 정의된 메세지 세트(a set of predefined messages)에 응답합니다. 당신은 그래픽을 숨기거나, 사운드를 내거나, 물리 객체가 움직이게끔 메세지를 보낼 수도 있습니다. 또한 인스턴스간 물리 충돌이 일어났을 때 메세지를 사용해서 컴포넌트 들에게 이벤트를 알리기도 합니다.

이 메세지 전달 메커니즘은 각각 보내진 메세지들을 받을 수 있는 수신자를 필요로 합니다. 그러므로, 게임의 모든 오브젝트와 컴포넌트는 서로에게 메세지를 보낼 수 있게 unique URL을 가집니다.

메세지 전달이 어떻게 동작하는지 깊이 있는 설명을 원하시면 the Message passing documentation을 참조하시기 바랍니다.

## Factories
몇몇 상황에서는 게임오브젝트를 수동으로 컬렉션에 배치하는 것이 아니라, 동적으로 생성시켜야 할 때가 있습니다.
예를 들어, 플레이어가 트리거를 누르면 총이 쏴지며, 총알이 동적으로 스폰되어 날아가야 할 경우 처럼 말이죠. 이처럼 게임오브젝트를 동적으로 생성하기 위해 (미리 할당된 객체 풀로부터), 당신은 팩토리 컴포넌트를 사용할 수 있습니다.

![](http://www.defold.com/static/images/introduction/introduction_factory.png)

Defold는 2가지 타입의 팩토리를 제공합니다. 각 매뉴얼에서 자세한 내용을 읽을 수 있습니다.

* Factories
* Collection factories

## Collaboration(공동작업)
대다수 게임들은 둘 이상의 공동작업으로 만들어 집니다. 우리는 함께 일하는 능력이 곧 빠른 개발 사이클의 핵심이라고 믿습니다. 그러므로 공동작업은 Defold 플랫폼의 주춧돌입니다.

![](http://www.defold.com/static/images/introduction/introduction_collaboration.png)

새 프로젝트를 생성하면, 우리 서버에 자동적으로 중앙 저장소(repository)가 생성됩니다. 개발하는 동안은 이 저장소의 개인보기(personal view)에서 파일이 생성되거나 수정됩니다. 당신이 작업을 완료하고 공유할 준비가 되면, 개인보기를 중앙 저장소에 동기화합니다. 에디터는 당신의 변경사항을 업로드하고 다른 팀원이 올린 새 변경 사항을 다운로드하고 당신이나 누군가 프로젝트 데이터의 같은 조각을 수정했다면 충돌을 해결하기도 합니다. 모든 변경사항은 기록되며 당신의 프로젝트에서 발생하는 모든 히스토리가 로그에 남습니다. 당신은 백업을 걱정할 필요가 없으며 당신의 팀에게 파일들을 이메일로 보낼 필요도 없습니다. 워크플로우 문서에서 프로젝트 공동작업에 대해 더 읽어보세요.

Defold의 협업툴은 유명하고 아주 강력한 분산 버전 관리 시스템인 "Git"을 사용합니다. (Git에 관심이 있다면 http://git-scm.com을 읽어 보시기 바랍니다.)

## Libraries
Project branches(프로젝트 브랜치)를 통하여 협업하는 것 외에도, Defold는 강력한 라이브러리 메커니즘을 통해 프로젝트간 데이터를 공유할 수 있습니다. 당신은 모든 팀이나 스스로를 위하여 모든 프로젝트들로부터 접근할 수 있는 공유 라이브러리를 구성하여 사용할 수 있습니다. 라이브러리 문서에서 라이브러리 메커니즘을 읽어보시기 바랍니다.

## Building blocks
빌딩 블록은 게임이나 앱을 만들기 위해 사용 가능한 구성요소들 입니다. 이것은 Defold 편집기에서 빌딩 블록의 타입에 따라 아이콘으로 구분됩니다. 

#### Game object
![](http://www.defold.com/static/images/icons/brick.png)
게임 오브젝트에 대한 설명은 위를 참고하세요.

#### Collection
![](http://www.defold.com/static/images/icons/bricks.png)
컬렉션에 대한 설명은 위를 참고하세요.

#### Script
![](http://www.defold.com/static/images/icons/cog.png)
스크립트에 대한 설명은 위를 참고하세요.

#### Sound
![](http://www.defold.com/static/images/icons/sound.png)
사운드 컴포넌트는 특정 사운드를 재생합니다. 현재 Defold는 WAV 타입의 사운드파일을 지원합니다.

#### Collision object
![](http://www.defold.com/static/images/icons/weight.png)
충돌 오브젝트는 게임오브젝트의 물리속성(모양, 무게, 마찰력, 반발력 등)을 담당하는 컴포넌트입니다. 이 속성들은 충돌 오브젝트가 다른 충돌 오브젝트와 어떻게 충돌하는지를 관장합니다. 충돌 오브젝트의 가장 일반적인 타입은 Kinematic objects, Dynamic objects 그리고 triggers입니다. Kinematic객체는 당신이 수동으로 반응해야 하는 상세한 충돌 정보를 제공하며, Dynamic객체는 물리엔진에 의해 뉴턴의 물리법칙을 따르게끔 자동적으로 시뮬레이트 됩니다. Trigger는 특정한 모양(Shape)이 다른 특정한 모양을 가진 트리거와 교차되거나 교차에서 벗어난 경우를 감지합니다.

#### Factory
![](http://www.defold.com/static/images/icons/factory.png)
팩토리에 대한 설명은 위를 참고하세요.

#### Sprite
![](http://www.defold.com/static/images/icons/pictures.png)
스프라이트는 게임오브젝트의 그래픽 처리를 담당하는 컴포넌트입니다. 타일 소스나 아틀라스로부터 이미지를 표시합니다. 스프라이트는 flip-book이나 본 애니메이션을 위해 빌트인으로 지원하고 있습니다. 스프라이트는 일반적으로 아이템이나 캐릭터를 위해 사용됩니다. 더 자세한 정보를 위해 2D graphic 문서를 보시기 바랍니다.

#### Atlas
![](http://www.defold.com/static/images/icons/pictures_atlas.png)
아틀라스는 나누어진 이미지들의 모음입니다. 이것은 메모리나 성능을 이유로 커다란 시트로 컴파일 되었습니다. 당신은 이 이미지들이나 이미지들의 flip-book 애니메이션 시리즈를 저장할 수 있습니다. 아틀라스는 그래픽 자원을 공유하기 위해 스프라이트나 파티클FX 컴포넌트에 의해 사용됩니다. 더 자세한 정보를 위해 2D graphic 문서를 보시기 바랍니다.
![](http://www.defold.com/static/images/introduction/introduction_atlas.png)

#### Tile source
![](http://www.defold.com/static/images/icons/small_tiles.png)
타일소스는 크기가 같은 여러 개의 작은 이미지로 구성된 텍스쳐를 나타냅니다. 이 컴포넌트는 플립북 애니메이션을 지원합니다. 당시는 타일 소스에서 이미지 시퀀스를 활용하여 애니메이션을 정의 할 수 있습니다. 또한 타일소스는 이미지 데이터로부터 자동으로 충돌 모양을 계산할 수도 있습니다. 이것은 오브젝트가 충돌하거나 반응하는 타일로 된 레벨을 제작하는데 매우 유용합니다. 타일 소스는 그래픽 리소스를 공유하는 타일 맵(스프라이트와 파티클FX 그리고 아틀라스가 일반적으로 선호되긴 하지만) 컴포넌트에 의해 사용됩니다. 더 많은 정보를 위해 2D graphic 문서를 보시기 바랍니다.
![](http://www.defold.com/static/images/introduction/introduction_tilesource.png)
![](http://www.defold.com/static/images/introduction/introduction_tilesource_animation.png)
![](http://www.defold.com/static/images/introduction/introduction_tilesource_hull.png)

#### Tile map
![](http://www.defold.com/static/images/icons/layer_grid.png)
타일 맵 컴포넌트는 타일 소스의 이미지를 하나 이상의 겹쳐진 격자로 표시합니다. 이것은 주로 바닥, 벽, 건축물, 장애물 같은 게임의 환경요소들을 만드는데 사용되곤 합니다. 타일 맵은 지정된 블렌드 모드(blend mode)로 여러 레이어들을 겹쳐서 표시 할 수 있는데, 예를 들어 잔디 타일 배경 위에 나뭇잎 등을 깔아 놓을때 유용합니다. 또한 동적으로 타일의 이미지를 바꾸는 것도 가능합니다. 예를 들어, 다리를 파괴해서 건너가지 못하게 하는 동작을 간단하게 무너진 다리의 이미지와 물리형태를 가진 타일로 교체함으로써 처리 할 수 있습니다.
![Tile map](http://www.defold.com/static/images/introduction/introduction_tilemap.png)
![Tile map palette](http://www.defold.com/static/images/introduction/introduction_tilemap_palette.png)

#### ParticleFX
![](http://www.defold.com/static/images/icons/clouds.png)
파티클은 게임에서 특별하고 멋진 비주얼 이펙트를 생성하는데 매우 유용합니다. 당신은 안개, 연기, 불, 비, 떨어지는 낙엽같은 효과를 만들 수 있습니다. Defold는 강력한 파티클 이펙트 편집기를 포함하고 있으며 당신이 게임에서 실시간으로 실행시켜서 이펙트를 제작하거나 최적화 할 수도 있습니다. 더 많은 내용을 보시려면 파티클FX 문서를 참고 바랍니다.
![](http://www.defold.com/static/images/introduction/introduction_particlefx.png)

#### GUI
![](http://www.defold.com/static/images/icons/text_allcaps.png)
GUI컴포넌트는 텍스트나 텍스쳐블록 같은 사용자 인터페이스를 구성하는데 사용되는 요소를 포함하고 있습니다. 각 요소들은 스크립트나 애니메이션이나 계층적인 구조로 구성할 수 있습니다. GUI컴포넌트는 일반적으로 HUD나 메뉴, 스크린 알람 등을 만드는데 사용됩니다. GUI컴포넌트는 GUI스크립트로 제어하는데 이는 GUI의 동작과 유저 상호작용을 제어하는것을 정의합니다. 더 자세한 것은 GUI documentation을 참고 바랍니다.
![GUI](http://www.defold.com/static/images/introduction/introduction_gui.png)

#### GUI script
![](http://www.defold.com/static/images/icons/cog.png)
GUI스크립트는 GUI컴포넌트의 동작을 정의하는데 사용됩니다. 이것은 GUI애니메이션을 제어하거나 유저가 어떻게 GUI와 상호작용하는지를 제어합니다.

#### Font
![](http://www.defold.com/static/images/icons/font.png)
폰트는 TrueType이나 OneType 폰트 파일을 사용할 수 있습니다. 폰트는 크기나 윤곽선과 그림자같은 꾸밈을 지정할 수 있습니다. 폰트는 GUI컴포넌트에서 사용됩니다.
![](http://www.defold.com/static/images/introduction/introduction_font.png)

#### Input binding
![](http://www.defold.com/static/images/icons/keyboard.png)
인풋바인딩 파일은 게임에서 하드웨어 입력(마우스, 키보드, 터치스크린, 게임패드 등)을 해석하는 방법을 정의합니다. 이 파일은 "jump"나 "move_formard" 같은 동작을 하드웨어 입력에 바인딩 합니다. 입력을 기다리는 스크립트 컴포넌트에서 게임이나 앱이 특정 입력을 받아야만 하는 동작을 스크립트 할 수 있습니다. 자세한 것은 Input documentation을 참고 바랍니다.
![](http://www.defold.com/static/images/introduction/introduction_input_binding.png)

#### Camera
![](http://www.defold.com/static/images/icons/camera.png)
카메라 컴포넌트는 게임월드의 특정 부분이 보여지거나 어떻게 투영되는지 결정하는걸 도와줍니다. 일반적인 사용 사례로는 카메라에 플레이어나 플레이어 주변을 부드럽게 따라다니는 별도의 게임 오브젝트를 연결하는 것입니다.

#### Material
![](http://www.defold.com/static/images/icons/large_tiles.png)
메터리얼은 어떻게 각 오브젝트들이 특정 속성과 쉐이더에 의해 렌더링되는지 정의합니다.

#### Render
![](http://www.defold.com/static/images/icons/paintcan.png)
렌더 파일에는 게임을 화면에 렌더링 할 때 사용되는 설정들이 들어 있습니다. 렌더 파일은 렌더링에 사용할 렌더링 스크립트와 메터리얼을 정의합니다.

#### Render script
![](http://www.defold.com/static/images/icons/cog.png)
렌더 스크립트는 게임이나 앱이 어떻게 화면에 렌더링 되어야 하는지를 제어하는 루아 스크립트 입니다. 가장 일반적인 경우를 다루는 기본 렌더 스크립트가 있지만 커스텀 라이팅 모델이나 다른 효과가 필요하다면 직접 작성할 수 있습니다.

#### Collection proxy
![](http://www.defold.com/static/images/icons/bricks_proxy.png)
컬렉션 프록시는 게임이나 앱이 실행되는 동안 컬렉션을 동적으로 불러오고 활성화하는데 사용됩니다. 가장 일반적인 경우로는 특정 레벨을 컬렉션 프록시로 불러올 수 있습니다. 자세한 것은 컬렉션 프록시 문서를 참고 바랍니다.