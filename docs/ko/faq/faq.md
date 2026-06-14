---
title: Defold 엔진과 에디터 FAQ
brief: Defold 게임엔진, 에디터, 플랫폼에 대해 자주 묻는 질문입니다.
---

# 자주 묻는 질문

## 일반 질문

#### Q: Defold는 정말 무료인가요?

A: 예, 모든 기능을 갖춘 Defold 엔진과 에디터는 완전히 무료입니다. 숨겨진 비용, 수수료, 로열티가 없습니다. 그냥 무료입니다.


#### Q: Defold Foundation은 왜 Defold를 무료로 제공하나요?

A: [Defold Foundation](/foundation)의 목표 중 하나는 전 세계 개발자가 Defold 소프트웨어를 사용할 수 있고, 소스 코드도 무료로 이용할 수 있도록 하는 것입니다.


#### Q: Defold는 얼마나 오래 지원되나요?

A: 저희는 Defold에 깊이 전념하고 있습니다. [Defold Foundation](/foundation)은 앞으로 오랫동안 Defold의 책임 있는 소유자로 존재할 수 있도록 설립되었습니다. 사라지지 않습니다.


#### Q: 전문 개발에 Defold를 믿고 사용할 수 있나요?

A: 물론입니다. Defold는 점점 더 많은 전문 게임 개발자와 게임 스튜디오에서 사용하고 있습니다. Defold로 만든 게임 예시는 [games showcase](/showcase)를 확인하세요.


#### Q: 어떤 사용자 추적을 하나요?

A: 서비스와 제품을 개선하기 위해 웹사이트와 Defold 에디터의 익명 사용 데이터를 기록합니다. 사용자가 만드는 게임에는 사용자 추적이 없습니다(직접 분석 서비스를 추가하지 않는 한). 자세한 내용은 [Privacy Policy](/privacy-policy)를 읽어보세요.


#### Q: Defold는 누가 만들었나요?

A: Defold는 Ragnar Svensson과 Christian Murray가 만들었습니다. 두 사람은 2009년에 엔진, 에디터, 서버 작업을 시작했습니다. King과 Defold는 2013년에 파트너십을 시작했고, King은 2014년에 Defold를 인수했습니다. 전체 이야기는 [여기](/about)에서 읽을 수 있습니다.


## 게임 개발 질문

#### Q: Defold로 3D 게임을 만들 수 있나요?

A: 물론입니다! 엔진은 완전한 3D 엔진입니다. 하지만 도구 세트는 2D용으로 만들어져 있으므로 많은 부분을 직접 처리해야 합니다. 더 나은 3D 지원은 계획되어 있습니다.


## 프로그래밍 언어 질문

#### Q: Defold에서는 어떤 프로그래밍 언어로 작업하나요?

A: Defold 프로젝트의 게임 로직은 주로 Lua 언어로 작성합니다. 구체적으로는 Lua 5.1/LuaJIT를 사용하며, 자세한 내용은 [Lua 매뉴얼](/manuals/lua)을 참고하세요. Lua는 가볍고 빠르며 매우 강력한 동적 언어입니다. Defold는 Lua 코드를 생성하는 transpiler를 지원합니다. Transpiler 익스텐션을 설치하면 [Teal](https://github.com/defold/extension-teal) 같은 대체 언어로 정적 검사를 받는 Lua를 작성할 수 있습니다. 플랫폼에 따라 네이티브 코드(C/C++, Objective-C, Java, JavaScript)를 사용해 [Defold 엔진을 새로운 기능으로 확장](/manuals/extensions/)할 수도 있습니다. [커스텀 메터리얼](/manuals/material/)을 만들 때는 OpenGL ES SL shader language로 버텍스 쉐이더와 프래그먼트 쉐이더를 작성합니다.


#### Q: C++로 게임 로직을 작성할 수 있나요?

A: Defold의 C++ 지원은 주로 서드파티 SDK나 플랫폼별 API와 연동하는 네이티브 익스텐션을 작성하기 위한 것입니다. [dmSDK](https://defold.com/ref/stable/dmGameObject/)(네이티브 익스텐션에서 사용하는 Defold용 C++ API)는 점진적으로 더 많은 기능이 추가될 예정이며, 개발자가 원한다면 모든 게임 로직을 C++로 작성할 수 있게 하는 것이 목표입니다. Lua는 여전히 게임 로직에 사용하는 주 언어로 남겠지만, 확장된 C++ API를 통해 C++로도 게임 로직을 작성할 수 있게 됩니다. C++ API 확장 작업은 주로 기존 private 헤더 파일을 public 섹션으로 옮기고, public 사용에 맞게 API를 정리하는 작업입니다.


#### Q: Defold에서 TypeScript를 사용할 수 있나요?

A: TypeScript는 공식적으로 지원되지 않습니다. 커뮤니티에서 [ts-defold](https://ts-defold.dev/)라는 툴킷을 유지 관리하고 있으며, 이를 사용하면 VSCode에서 바로 TypeScript를 작성하고 Lua로 transpile할 수 있습니다.


#### Q: Defold에서 Haxe를 사용할 수 있나요?

A: Haxe는 공식적으로 지원되지 않습니다. 커뮤니티에서 Haxe를 작성하고 Lua로 transpile하기 위한 [hxdefold](https://github.com/hxdefold/hxdefold)를 유지 관리하고 있습니다.


#### Q: Defold에서 C#을 사용할 수 있나요?

A: Defold Foundation은 C# 지원을 추가했고 이를 라이브러리 종속성으로 사용할 수 있게 했습니다. C#은 널리 사용되는 프로그래밍 언어이며, C#에 크게 투자한 스튜디오와 개발자가 Defold로 전환하는 데 도움이 됩니다.


#### Q: C# 지원 추가가 Defold에 부정적인 영향을 줄까 걱정됩니다. 걱정해야 하나요?

A: Defold는 Lua를 기본 스크립팅 언어에서 대체하려는 것이 아닙니다. C# 지원은 익스텐션을 위한 새 언어로 추가됩니다. 프로젝트에서 C# 익스텐션을 사용하기로 선택하지 않는 한 엔진에는 영향을 주지 않습니다.

C# 지원에는 실행 파일 크기, 런타임 성능 같은 비용이 따르지만, 이는 개별 개발자나 스튜디오가 결정할 문제입니다.

C# 자체로 보면 비교적 작은 변경입니다. 익스텐션 시스템은 이미 여러 언어(C/C++/Java/Objective-C/Zig)를 지원하기 때문입니다. C# 바인딩을 생성해 SDK를 동기화 상태로 유지합니다. 이렇게 하면 최소한의 노력으로 바인딩을 최신 상태로 유지할 수 있습니다.

Defold Foundation은 이전에는 Defold에 C# 지원을 추가하는 것에 반대했지만, 여러 이유로 의견을 바꾸었습니다.

* 스튜디오와 개발자들이 C# 지원을 계속 요청합니다.
* C# 지원 범위가 익스텐션 전용으로 축소되었습니다(즉, 작업량이 적습니다).
* 코어 엔진은 영향을 받지 않습니다.
* C# API를 생성 방식으로 유지하면 최소한의 노력으로 동기화 상태를 유지할 수 있습니다.
* C# 지원은 DotNet 9와 NativeAOT를 기반으로 하며, 기존 빌드 파이프라인이 다른 Defold 익스텐션처럼 링크할 수 있는 정적 라이브러리를 생성합니다.


## 플랫폼 질문

#### Q: Defold는 어떤 플랫폼에서 실행되나요?

A: 에디터/도구와 엔진 런타임은 다음 플랫폼을 지원합니다.

  | 시스템             | 버전               | 아키텍처           | 지원               |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | 에디터와 엔진      |
  | Windows            | Vista              | `x86-32`, `x86-64` | 에디터와 엔진      |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | 에디터             |
  | Linux (2)          | Any                | `x86-64`, `arm-64` | 엔진               |
  | iOS                | 15.0               | `arm-64`  `x86_64` | 엔진               |
  | Android            | 5.0 (API level 21) | `arm-32`, `arm-64` | 엔진               |
  | HTML5              |                    | `asm.js`, `wasm`   | 엔진               |

  (1 에디터는 64-bit Ubuntu용으로 빌드되고 테스트됩니다. 다른 배포판에서도 동작할 수 있지만 보장하지는 않습니다.)

  (2 엔진 런타임은 그래픽 드라이버가 최신이면 대부분의 64-bit Linux 배포판에서 실행됩니다. 그래픽 API에 대한 자세한 내용은 아래를 참고하세요.)


#### Q: Defold로 어떤 타겟 플랫폼용 게임을 개발할 수 있나요?

A: 클릭 한 번으로 PS4™, PS5™, Nintendo Switch, iOS(64-bit), Android(32-bit 및 64-bit), HTML5는 물론 macOS(x86-64 및 arm64), Windows(32-bit 및 64-bit), Linux(x86-64 및 arm64)에 퍼블리시할 수 있습니다. 하나의 코드베이스로 여러 플랫폼을 지원합니다.


#### Q: Defold는 어떤 렌더링 API에 의존하나요?

A: 개발자는 [완전히 스크립팅 가능한 렌더링 파이프라인](/manuals/render/)을 사용하는 단일 렌더 API만 신경 쓰면 됩니다. Defold 렌더 스크립트 API는 렌더 작업을 다음 그래픽 API로 변환합니다.

:[Graphics API](../shared/graphics-api.md)

#### Q: 현재 실행 중인 버전을 알 수 있는 방법이 있나요?

A: 예, Help 메뉴에서 "About" 옵션을 선택하세요. 팝업에는 Defold beta 버전과, 더 중요하게는 특정 release SHA1이 명확하게 표시됩니다. 런타임 버전을 조회하려면 [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info)를 사용하세요.

[http://d.defold.com/beta](http://d.defold.com/beta)에서 다운로드할 수 있는 최신 beta 버전은 [http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json)을 열어 확인할 수 있습니다. stable 버전에도 같은 파일이 있습니다: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json).


#### Q: 런타임에 게임이 어떤 플랫폼에서 실행 중인지 알 수 있는 방법이 있나요?

A: 예, [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info)를 확인하세요.


## 에디터 질문
:[Editor FAQ](../shared/editor-faq.md)


## Linux 질문
:[Linux FAQ](../shared/linux-faq.md)


## Android 질문
:[Android FAQ](../shared/android-faq.md)


## HTML5 질문
:[HTML5 FAQ](../shared/html5-faq.md)


## iOS 질문
:[iOS FAQ](../shared/ios-faq.md)


## Windows 질문
:[Windows FAQ](../shared/windows-faq.md)


## 콘솔 질문
:[Consoles FAQ](../shared/consoles-faq.md)


## 게임 퍼블리싱

#### Q: 게임을 AppStore에 제출하려고 합니다. IDFA에는 어떻게 답해야 하나요?

A: 제출할 때 Apple은 IDFA의 세 가지 유효한 사용 사례에 대해 세 개의 체크박스를 제공합니다.

  1. 앱 안에서 광고 제공
  2. 광고로부터 설치 기여도 측정
  3. 광고로부터 사용자 행동 기여도 측정

  옵션 1을 체크하면 앱 리뷰어는 앱에 광고가 표시되는지 확인합니다. 게임에 광고가 표시되지 않으면 거절될 수 있습니다. Defold 자체는 AD id를 사용하지 않습니다.


#### Q: 게임으로 수익을 내려면 어떻게 하나요?

A: Defold는 인앱 구매와 여러 광고 솔루션을 지원합니다. 사용 가능한 최신 수익화 옵션 목록은 Asset Portal의 [Monetization category](https://defold.com/tags/stars/monetization/)를 확인하세요.


## Defold 사용 중 오류

#### Q: 게임을 시작할 수 없고 빌드 오류도 없습니다. 무엇이 문제인가요?

A: 빌드 프로세스가 이전에 빌드 오류를 만났고 이를 수정한 뒤에도, 드문 경우 일부 파일을 다시 빌드하지 못할 수 있습니다. 메뉴에서 *Project > Rebuild And Launch*를 선택해 전체를 강제로 다시 빌드하세요.



## 게임 컨텐츠

#### Q: Defold는 prefabs를 지원하나요?

A: 예, 지원합니다. Defold에서는 이를 [컬렉션](/manuals/building-blocks/#collections)이라고 부릅니다. 컬렉션을 사용하면 복잡한 게임 오브젝트 계층구조를 만들고, 이를 에디터나 런타임에서(컬렉션 스폰을 통해) 인스턴스화할 수 있는 별도의 빌딩 블록으로 저장할 수 있습니다. GUI 노드에는 GUI 템플릿 지원이 있습니다.


#### Q: 한 게임 오브젝트를 다른 게임 오브젝트의 자식으로 추가할 수 없는 이유는 무엇인가요?

A: 게임 오브젝트 파일 안에서 자식을 추가하려고 했을 가능성이 큽니다. 이는 불가능합니다. 컬렉션 파일 안에서만 가능합니다. 이유를 이해하려면 부모-자식 계층구조가 엄격히 _씬 그래프(scene graph)_ 변형 계층구조라는 점을 기억해야 합니다. 씬(컬렉션)에 배치되거나 스폰되지 않은 게임 오브젝트는 씬 그래프의 일부가 아니므로 씬 그래프 계층구조의 일부가 될 수 없습니다. [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id)를 사용하면 게임 오브젝트의 부모 id를 얻을 수 있습니다.


#### Q: 왜 게임 오브젝트의 모든 자식에게 메세지를 브로드캐스트할 수 없나요?

A: 부모-자식 관계는 씬 그래프 변형 관계만을 표현하며, 객체지향 집합체와 혼동해서는 안 됩니다. 게임 데이터와 게임 상태가 바뀔 때 이를 가장 잘 변형하는 방법에 집중하면, 여러 오브젝트에 상태 데이터를 담은 메세지를 항상 보내야 할 필요가 줄어들 것입니다. 데이터 계층구조가 필요한 경우에는 Lua에서 쉽게 구성하고 처리할 수 있습니다.


#### Q: 스프라이트 가장자리 주변에 시각적 아티팩트가 나타나는 이유는 무엇인가요?

A: 이는 "edge bleeding"이라는 시각적 아티팩트입니다. 아틀라스에서 인접한 이미지의 가장자리 픽셀이 스프라이트에 할당된 이미지 안으로 번져 들어오는 현상입니다. 해결 방법은 아틀라스 이미지의 가장자리를 동일한 픽셀의 추가 행과 열로 패딩하는 것입니다. 다행히 Defold의 아틀라스 에디터가 이를 자동으로 처리할 수 있습니다. 아틀라스를 열고 *Extrude Borders* 값을 1로 설정하세요.


#### Q: 스프라이트에 색을 입히거나 투명하게 만들 수 있나요, 아니면 직접 쉐이더를 작성해야 하나요?

A: 기본적으로 모든 스프라이트에 사용되는 내장 스프라이트 쉐이더에는 "tint" 상수가 정의되어 있습니다.

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: 스프라이트의 z 좌표를 100으로 설정하면 렌더링되지 않습니다. 왜 그런가요?

A: 게임 오브젝트의 Z-position은 렌더링 순서를 제어합니다. 낮은 값이 높은 값보다 먼저 그려집니다. 기본 렌더 스크립트에서는 -1부터 1 사이의 depth 범위에 있는 게임 오브젝트가 그려지며, 그보다 낮거나 높은 값은 그려지지 않습니다. 렌더링 스크립트에 대한 자세한 내용은 공식 [Render 문서](/manuals/render)를 읽어보세요. GUI 노드에서는 Z 값이 무시되며 렌더링 순서에 전혀 영향을 주지 않습니다. 대신 노드는 나열된 순서와 자식 계층구조(및 레이어)에 따라 렌더링됩니다. 레이어를 사용한 GUI 렌더링과 드로우콜 최적화에 대한 자세한 내용은 공식 [GUI 문서](/manuals/gui)를 읽어보세요.


#### Q: 뷰 프로젝션 Z-range를 -100에서 100으로 바꾸면 성능에 영향이 있나요?

A: 아닙니다. 유일한 영향은 정밀도입니다. z-buffer는 logarithmic이며 0에 가까운 z 값에 대해서는 매우 세밀한 해상도를 갖고, 0에서 멀리 떨어진 값에 대해서는 해상도가 낮습니다. 예를 들어 24 bit 버퍼에서는 10.0과 10.000005를 구분할 수 있지만, 10000과 10005는 구분할 수 없습니다.


#### Q: 각도를 표현하는 방식에 일관성이 없는 이유는 무엇인가요?

A: 실제로는 일관성이 있습니다. 에디터와 게임 API에서는 각도가 모두 도(degree)로 표현됩니다. 수학 라이브러리는 라디안(radian)을 사용합니다. 현재 `angular_velocity` 물리 프로퍼티가 radians/s로 표현되는 부분에서 관례가 깨져 있는데, 이는 변경될 예정입니다.


#### Q: 텍스쳐 없이 색상만 있는 GUI box-node를 만들면 어떻게 렌더링되나요?

A: 단순한 버텍스 컬러 shape로 렌더링됩니다. 그래도 fill-rate 비용은 발생한다는 점을 기억하세요.


#### Q: 실행 중에 에셋을 변경하면 엔진이 자동으로 언로드하나요?

A: 모든 리소스는 내부적으로 ref-count됩니다. ref-count가 0이 되는 즉시 리소스가 해제됩니다.


#### Q: 게임 오브젝트에 연결된 오디오 컴포넌트 없이 오디오를 재생할 수 있나요?

A: 모든 것은 컴포넌트 기반입니다. 여러 사운드를 가진 headless 게임 오브젝트를 만들고, 사운드 컨트롤러 오브젝트에 메세지를 보내 사운드를 재생할 수 있습니다.


#### Q: 런타임에 오디오 컴포넌트와 연결된 오디오 파일을 변경할 수 있나요?

A: 일반적으로 모든 리소스는 정적으로 선언되며, 그 덕분에 리소스 관리를 무료로 얻을 수 있습니다. [리소스 프로퍼티](/manuals/script-properties/#resource-properties)를 사용하면 컴포넌트에 할당된 리소스를 변경할 수 있습니다.


#### Q: 물리 충돌 모형 프로퍼티에 액세스할 수 있는 방법이 있나요?

A: 예, physics API를 확인하세요. 특히 [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape)와 [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table)를 참고하세요.


#### Q: 씬에서 충돌 오브젝트를 빠르게 렌더링할 방법이 있나요? (Box2D의 debug draw처럼)

A: 예, *game.project*에서 *physics.debug* 플래그를 설정하세요. 공식 [Project settings 문서](/manuals/project-settings/#debug)를 참고하세요.


#### Q: contact/collision이 많으면 성능 비용은 어떻게 되나요?

A: Defold는 백그라운드에서 수정된 버전의 Box2D를 실행하며, 성능 비용은 상당히 비슷합니다. [프로파일러](/manuals/debugging)를 열면 엔진이 물리에 얼마나 많은 시간을 쓰는지 언제든지 확인할 수 있습니다. 어떤 종류의 충돌 오브젝트를 사용하는지도 고려해야 합니다. 예를 들어 static 오브젝트는 성능 측면에서 더 저렴합니다. 자세한 내용은 Defold의 공식 [Physics 문서](/manuals/physics)를 참고하세요.


#### Q: 파티클 효과 컴포넌트가 많으면 성능에 어떤 영향이 있나요?

A: 재생 중인지 아닌지에 따라 다릅니다. 재생 중이 아닌 ParticleFx는 성능 비용이 0입니다. 재생 중인 ParticleFx의 성능 영향은 설정 방식에 따라 달라지므로 프로파일러를 사용해 평가해야 합니다. 대부분의 다른 항목과 마찬가지로 메모리는 *game.project*에서 max_count로 정의된 ParticleFx 수만큼 미리 할당됩니다.


#### Q: 컬렉션 프록시를 통해 로드된 컬렉션 내부의 게임 오브젝트에서 입력을 받으려면 어떻게 하나요?

A: 각 프록시로 로드된 컬렉션은 자체 입력 스택을 가집니다. 입력은 main 컬렉션 입력 스택에서 프록시 컴포넌트를 통해 컬렉션 안의 오브젝트로 라우팅됩니다. 즉, 로드된 컬렉션 안의 게임 오브젝트가 입력 포커스를 획득하는 것만으로는 충분하지 않으며, 프록시 컴포넌트를 _가지고 있는_ 게임 오브젝트도 입력 포커스를 획득해야 합니다. 자세한 내용은 [Input 문서](/manuals/input)를 참고하세요.


#### Q: string 타입 스크립트 프로퍼티를 사용할 수 있나요?

A: 아니요. Defold는 [hash](/ref/builtins#hash) 타입의 프로퍼티를 지원합니다. 이는 타입, 상태 식별자, 또는 어떤 종류의 키를 나타내는 데 사용할 수 있습니다. Hash는 게임 오브젝트 id(경로)를 저장하는 데도 사용할 수 있지만, 에디터가 관련 URL로 드롭다운을 자동으로 채워주기 때문에 [url](/ref/msg#msg.url) 프로퍼티가 더 나은 경우가 많습니다. 자세한 내용은 [Script properties 문서](/manuals/script-properties)를 참고하세요.


#### Q: [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) 등으로 만든 matrix의 개별 cell에는 어떻게 액세스하나요?

A: `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` 등을 사용해 cell에 액세스합니다.


#### Q: [gui.clone()](/ref/gui/#gui.clone:node) 또는 [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)을 사용할 때 `Not enough resources to clone the node`가 발생합니다.

A: gui 컴포넌트의 `Max Nodes` 값을 늘리세요. Outline에서 컴포넌트의 root를 선택하면 Properties 패널에서 이 값을 찾을 수 있습니다.


## 포럼

#### Q: 제 작업물을 홍보하는 thread를 올려도 되나요?

A: 물론입니다! 이를 위한 특별한 ["Work for hire" category](https://forum.defold.com/c/work-for-hire)가 있습니다. 커뮤니티에 도움이 되는 모든 것을 항상 장려하며, 보수를 받든 받지 않든 커뮤니티에 서비스를 제공하는 것은 그 좋은 예입니다.


#### Q: thread를 만들고 제 작업물을 추가했습니다. 더 추가해도 되나요?

A: "Work for hire" thread의 bumping을 줄이기 위해, 자신의 thread에는 14일에 한 번보다 자주 게시할 수 없습니다(thread 안의 댓글에 직접 답하는 경우에는 답글을 달 수 있습니다). 14일 기간 안에 thread에 추가 작업물을 넣고 싶다면, 기존 게시물을 편집해 추가 컨텐츠를 넣어야 합니다.


#### Q: Work for Hire 카테고리에 채용 공고를 올려도 되나요?

A: 물론입니다. 자유롭게 사용하세요! 구인과 의뢰 모두에 사용할 수 있습니다. 예를 들면 “Programmer looking for 2D pixel artist; I’m rich and I’ll pay you well” 같은 글입니다.
