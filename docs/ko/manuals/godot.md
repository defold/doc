---
title: Godot 사용자를 위한 Defold
brief: Godot에서 익숙한 개념을 Defold와 비교하고, 같은 작업을 Defold의 도구와 API로 구현하는 방법을 소개합니다.
---

# Godot 사용자를 위한 Defold {#defold-for-godot-users}

Godot로 게임을 만들어 봤다면 그 경험을 Defold에서도 상당 부분 활용할 수 있습니다. 이 가이드는 Godot에서 배운 내용을 바탕으로 Defold에서 빠르게 게임을 만드는 방법을 소개합니다. 두 엔진의 동작이 달라 실수하기 쉬운 부분도 함께 짚어 봅니다. 이 문서에서 사용한 Godot 버전은 4.7입니다.

## 소개 {#introduction}

Defold는 2D와 3D 게임을 위한 무료 크로스 플랫폼 게임 엔진으로, Windows, Linux, macOS용 에디터를 제공합니다. 엔진과 에디터의 전체 소스 코드는 [GitHub](https://github.com/defold/defold/)에 공개되어 있습니다. 직접 빌드하거나 운영체제에 맞는 버전을 다운로드할 수 있습니다.

처음 보면 Defold와 Godot는 무척 비슷합니다. 두 엔진 모두 재사용할 수 있는 요소를 조합해 게임을 구성하고 스크립트로 동작을 추가합니다. Godot에는 용도별로 특화된 노드가 많습니다. Defold에서는 비교적 적은 수의 범용 컴포넌트(component)를 조합하고, Lua 스크립트와 모듈로 게임플레이를 구현합니다. 예를 들어 플레이어 캐릭터는 게임 오브젝트(game object) 하나에 스프라이트나 모델, 충돌 오브젝트, 스크립트를 컴포넌트로 추가해 만들 수 있습니다.

Defold는 런타임의 크기를 작게 유지하고 리소스를 효율적으로 사용하는 데 중점을 둡니다. 이는 특히 웹과 모바일 게임에서 유용합니다. 일부 엔진 리소스는 메모리를 미리 할당할 수 있도록 최대 개수를 사전에 설정합니다.

Defold에는 바로 쓸 수 있는 게임플레이 요소나 UI 요소가 Godot보다 적을 수 있지만, 기본 컴포넌트를 조합하거나 확장해 같은 결과를 얻을 수 있습니다. Defold는 핵심 엔진을 최대한 가볍게 유지합니다. 필요 없는 기능을 제외해 더 줄이거나 네이티브 익스텐션(Native Extension)과 Lua 모듈로 확장할 수 있습니다. [Defold Asset Portal](https://defold.com/assets/)에는 복잡한 UI나 고급 렌더링 파이프라인을 구성하고 개발 작업을 간소화하는 데 사용할 수 있는 모듈, 라이브러리, 익스텐션이 수백 개 있습니다.

Defold의 다른 기능은 [제품 소개 페이지](https://defold.com/product/)에서 확인할 수 있습니다.

## 설치 {#installation}

1. [다운로드 페이지](https://defold.com/download/)에서 운영체제에 맞는 Defold를 다운로드합니다.
2. 압축을 풀고 에디터를 실행합니다.

별도의 허브나 내보내기 템플릿을 설치할 필요 없이 첫 프로젝트를 만들고 실행할 수 있습니다. 플랫폼별 설치 방법은 [설치 매뉴얼](/manuals/install/)을 참고하세요.

에디터에서 Defold를 직접 업데이트할 수 있습니다. 기존 프로젝트의 엔진 버전을 올릴 때는 릴리스 노트를 확인하고 대상 플랫폼에서 게임을 테스트하세요.

## 시작 화면 {#welcome-screen}

Defold를 실행하면 시작 화면에서 최근 프로젝트를 열거나 새 프로젝트를 만들 수 있습니다. Godot의 프로젝트 관리자와 비슷한 역할을 합니다.

![Godot 프로젝트 관리자와 Defold 시작 화면](images/godot/godot_1.png)

Defold에서는 다음 중 하나를 선택해 새 프로젝트를 시작할 수 있습니다.

- **Templates**에서 기본 빈 프로젝트나 특정 플랫폼용 프로젝트를 선택합니다.
- **Tutorials**에는 안내에 따라 진행하는 입문용 프로젝트가 있습니다.
- **Samples**에는 직접 실행하고 살펴볼 수 있는 예제와 스타터 키트가 있습니다.

![Godot 프로젝트 관리자와 Defold 시작 화면](images/godot/godot_2.png)

Defold의 Samples에는 Godot Asset Store에서 볼 수 있는 스타터 키트와 예제처럼 새 프로젝트의 출발점으로 삼을 수 있는 프로젝트와 예제가 있습니다.

![Godot 프로젝트 관리자와 Defold 시작 화면](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Defold 에디터 개요 {#defold-editor-overview}

주요 창의 이름과 위치는 달라도 용도는 익숙할 것입니다. 아래 그림에서는 두 에디터를 쉽게 비교할 수 있도록 Godot 에디터의 패널을 Defold의 기본 배치와 비슷하게 조정했습니다.

![Godot 에디터의 주요 창](images/godot/godot_4.png)
![Defold 에디터의 주요 창](images/godot/godot_5.png)

| Godot | Defold | Defold 에디터에서의 용도 |
|---|---|---|
| FileSystem 독 | Assets | 프로젝트의 파일과 폴더를 관리합니다. 디스크에 있는 프로젝트 디렉토리의 구조를 그대로 보여 줍니다. |
| 2D/3D 뷰와 리소스 에디터 | Main editor | 컬렉션, GUI, 아틀라스, 스크립트 등 어떤 파일을 여느냐에 따라 바뀝니다. 두 창으로 나눌 수 있습니다. |
| Scene 독 | Outline | 현재 리소스의 구조를 보여 줍니다. 런타임 전체의 씬 트리를 표시하는 창과는 다릅니다. |
| Inspector | Properties | 선택한 오브젝트, 컴포넌트 또는 리소스의 프로퍼티를 보여 줍니다. |
| Output 및 Debugger | Tools | Console, Build Errors, Search Results, 디버거 등이 있습니다. |
| 버전 관리 통합 | Changed Files | Git을 사용하는 프로젝트에서 변경 사항을 보여 줍니다. |

Defold 3D 에디터의 오른쪽 위에는 툴바가 있습니다. 각 도구의 용도는 [씬 편집 매뉴얼](/manuals/scene-editing/#toolbar-overview)을 참고하세요.

### 2D와 3D 씬 방향 {#2d-and-3d-scene-orientation}

:[2D와 3D 씬 방향](../shared/2d-and-3d-scene-orientation.md)

### 창 {#panes}

Defold 에디터의 창은 별도 윈도우로 분리할 수 없지만, 가장자리를 드래그해 크기를 조절할 수 있습니다. `F6`, `F7`, `F8` 키나 `View` 메뉴로 각 창을 표시하거나 숨길 수도 있습니다.

![에디터 창 표시와 숨기기](images/editor/editor_panes.png)

### 좌표 {#coordinates}

기본 렌더 스크립트를 사용하고 Defold 컬렉션(collection)에 카메라 컴포넌트가 없다면, 2D에서 좌표 `(0, 0)`은 게임 창의 왼쪽 아래에 있습니다. Y의 양의 방향은 **위쪽**이고 X의 양의 방향은 오른쪽입니다.

일반적인 Godot의 2D 화면 좌표계에서는 Y의 양의 방향이 **아래쪽**입니다. 위치 값이나 이동 코드를 옮길 때 이 차이를 기억하세요.

![Defold와 Godot의 2D 좌표계 차이](images/godot/godot_6.png)

Godot의 3D 좌표계에서는 Defold와 마찬가지로 Y의 양의 방향이 위쪽입니다. Defold의 2D와 3D 게임은 같은 3D 좌표계를 사용합니다. 일반적인 2D 설정에서는 XY 평면을 직교 투영(orthographic projection)으로 봅니다. 필요하면 카메라를 다르게 설정할 수 있습니다.

![Defold와 Godot의 3D 좌표계 비교](images/godot/godot_7.png)

Defold 에디터에 대한 자세한 내용은 [에디터 개요 매뉴얼](/manuals/editor/)을 참고하세요.

---

## 핵심 개념 {#key-concepts}

Godot에서는 노드로 **씬(Scene)**을 구성합니다. Defold에서는 컴포넌트, 게임 오브젝트, 그리고 게임 오브젝트를 묶는 컬렉션을 사용합니다.

예를 들어 Godot에서는 `Node2D`에 `Sprite2D` 자식을 추가하고 루트에 스크립트를 연결해 플레이어를 만든 다음 첫 번째 `Scene`에 배치할 수 있습니다.
Defold에서는 게임 오브젝트에 `Sprite`와 `Script` 컴포넌트를 추가해 플레이어를 만들고 이를 컬렉션에 배치합니다.

![Godot의 노드 구성과 Defold의 게임 오브젝트 및 컴포넌트 구성 비교](images/godot/key_concepts.png)

각 개념은 [빌딩 블록 매뉴얼](/manuals/building-blocks/)에서 자세히 설명합니다.

### 게임 오브젝트 {#game-objects}

Defold의 **게임 오브젝트**는 컴포넌트를 담는 *컨테이너*이며 다음 두 가지를 제공합니다.

- **식별자**
- 위치, 회전, 스케일을 나타내는 **변형(transform)**

게임 오브젝트는 Godot의 `Node2D`나 `Node3D`와 비슷한 역할을 할 수 있습니다. Defold에는 2D 전용 게임 오브젝트 타입이 없습니다. 2D 게임의 오브젝트를 포함해 모든 게임 오브젝트가 3D 변형을 사용합니다.

게임 오브젝트끼리 부모-자식 관계를 설정하면 자식이 부모의 변형을 상속합니다. 이 관계는 컬렉션에서 설정하거나 런타임에 바꿀 수 있습니다. 부모가 바뀌어도 게임 오브젝트의 주소는 그대로입니다.

컬렉션 안에서 게임 오브젝트를 **내장(embedded)** 오브젝트로 정의하면 그 정의가 `.collection` 파일에 직접 저장됩니다. 또는 재사용할 수 있는 `.go` 프로토타입을 참조로 추가할 수 있습니다. 내장 오브젝트의 정의를 편집하면 해당 컬렉션만 바뀌며, 독립적으로 정의한 다른 오브젝트에는 영향을 주지 않습니다. `.go` 프로토타입을 편집하면 이를 참조하는 인스턴스가 업데이트됩니다. 단, 인스턴스에서 별도로 재정의한 값은 유지됩니다. 내장 오브젝트끼리도 컴포넌트 리소스를 참조로 공유할 수 있으므로, 공유 리소스를 편집하면 이를 사용하는 다른 오브젝트에도 변경 사항이 반영됩니다. 컬렉션 자체를 재사용한 경우에는 그 컬렉션을 참조하는 모든 곳에 내장 오브젝트의 변경 사항이 반영됩니다.

### 컴포넌트 {#components}

컴포넌트는 각각 특정 기능을 맡는 빌딩 블록입니다. 예를 들어 게임 오브젝트에 외형, 물리, 오디오 또는 동작을 부여합니다.

게임 오브젝트에 `Sprite` 컴포넌트를 추가하면 이미지를 표시하고, `Sound` 컴포넌트를 추가하면 오디오를 재생하며, `Script` 컴포넌트를 추가하면 Lua 코드를 실행할 수 있습니다.

컴포넌트는 게임 오브젝트에 속하며 자식 컴포넌트를 가질 수 없습니다. 계층 구조를 만들려면 컬렉션의 게임 오브젝트끼리 부모-자식 관계를 설정합니다.

Godot에서처럼 컴포넌트에 직접 스크립트를 붙여 그 동작을 바꿀 수도 없습니다. 대신 Properties 창에서 컴포넌트를 조정할 수 있으며, GDExtension과 비슷한 네이티브 익스텐션으로 새 컴포넌트를 만들 수도 있습니다. 예를 들어 Defold가 공식 제공하는 [Rive](https://github.com/defold/extension-rive)와 [Spine](https://github.com/defold/extension-spine), 커뮤니티에서 제공하는 [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold)와 [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation)이 있습니다.

Defold에서 스크립트는 어떤 게임 오브젝트에나 추가할 수 있는 독립적인 컴포넌트입니다. 한 게임 오브젝트에 스크립트를 비롯한 여러 컴포넌트를 붙일 수 있습니다.

컴포넌트끼리 계층을 이루지 않고 사용자 스크립트와도 분리되어 있으므로, Defold는 데이터 지향 설계를 활용해 컴포넌트를 메모리에 효율적으로 배치합니다.

| Godot 노드 | Defold 컴포넌트 | 설명 |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [스프라이트](/manuals/sprite/) | 아틀라스(여러 이미지를 담은 텍스쳐)나 타일 소스의 2D 텍스쳐와 플립북 애니메이션을 렌더링합니다. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` 및 각 노드의 3D 버전 | [충돌 오브젝트](/manuals/physics-objects/) | 물리와 트리거를 처리합니다. 충돌 모양은 자식 노드로 분리하지 않고 이 컴포넌트 안에 직접 정의합니다. 정적, 동적, 키네마틱, 트리거 타입 중에서 선택할 수 있습니다. |
| 노드에 연결한 `.gd` 스크립트 | Script | Lua 코드로 게임 로직과 입력을 처리하고 다른 컴포넌트와 게임 오브젝트를 제어합니다. |
| `TileMapLayer` | [타일맵](/manuals/tilemap/) | 타일 소스와 타일맵 레이어를 사용해 그리드 기반 맵을 렌더링합니다. |
| `Label` | [GUI 텍스트 노드](/manuals/gui-text/) | 인터페이스의 텍스트에는 GUI 텍스트를 사용합니다. 게임 월드 안의 텍스트에는 [라벨 컴포넌트](/manuals/label/)를 사용합니다. |
| `AudioStreamPlayer` | [사운드](/manuals/sound/) | 오디오를 재생합니다. Speed, Pan, Gain을 설정할 수 있습니다. |
| `Camera2D` / `Camera3D` | [카메라](/manuals/camera/) | 직교 투영과 원근 투영을 지원합니다. |
| `Control` 계층 / `CanvasLayer` | [GUI](/manuals/gui/) | GUI 컴포넌트 안에 Box, Text, Pie 등의 노드로 별도의 계층을 구성하며, GUI 처리는 전용 `.gui_script`가 맡습니다. |
| `MeshInstance3D` | [모델](/manuals/model/) 또는 [메쉬](/manuals/mesh/) | 모델은 임포트한 3D 컨텐츠를, 메쉬는 버퍼로 구성한 사용자 정의 지오메트리를 지원합니다. |
| `CPUParticles2D` / `GPUParticles2D` 및 각 노드의 3D 버전 | [ParticleFX](/manuals/particlefx/) | Defold의 파티클 에디터에서 설정한 2D/3D 파티클을 방출합니다. |
| `PackedScene.instantiate()` | Factory / Collection Factory | 런타임에 생성할 게임 오브젝트와 컬렉션을 지정하는 컴포넌트가 각각 따로 있습니다. |

### 컬렉션과 월드 {#collections-and-worlds}

**컬렉션**은 게임 오브젝트, 각 오브젝트의 컴포넌트, 오브젝트 사이의 부모-자식 관계를 정의합니다. 여러 오브젝트를 묶어 재사용하려면 컬렉션 안에 다른 컬렉션을 넣으면 됩니다. Godot의 중첩 씬과 비슷합니다. Defold는 Godot처럼 씬을 상속해서 편집하는 범용 기능을 제공하지 않습니다. 대신 프로토타입과 컬렉션을 재사용하고 프로퍼티나 스크립트로 인스턴스를 조정합니다.

컬렉션 파일 자체는 런타임에 존재하는 개체가 아닙니다. 메서드를 호출할 수 있는 컬렉션 오브젝트도, 컬렉션 자체에 해당하는 루트 노드도 없습니다. Defold는 컬렉션 파일의 정의를 읽어 런타임에 게임 오브젝트와 컴포넌트를 생성하고 계층을 구성합니다.

Defold는 게임을 시작할 때 `game.project` 파일을 읽습니다. **Bootstrap ▸ Main Collection**에 설정한 컬렉션을 가장 먼저 로드해 최초의 게임 월드를 만듭니다. 그 안에 중첩된 컬렉션의 오브젝트도 같은 월드에 속합니다.

**컬렉션 팩토리(Collection Factory)** 컴포넌트는 게임 오브젝트와 그 컴포넌트로 이루어진 그룹을 팩토리가 속한 **기존 월드**에 생성합니다.

**컬렉션 프록시(Collection Proxy)**는 별도의 컬렉션을 로드해 독립된 주소 네임스페이스와 물리 시뮬레이션을 갖는 **새 월드**를 만듭니다. 예를 들어 기존 레벨의 지형과 상호작용할 적을 생성할지, 아니면 완전히 새로운 레벨을 필요에 따라 비동기로 로드할지 결정할 때 이 차이가 중요합니다. 두 방법은 아래에서 살펴봅니다.

Godot에서는 인스턴스 생성과 씬 전환에 모두 `PackedScene`을 사용합니다. 이 중 `SceneTree`를 통한 씬 전환이 컬렉션 프록시로 별도의 월드를 로드하는 방식과 비슷합니다.

두 엔진의 대응 관계를 정리하면 다음과 같습니다.

| Godot | Defold | 설명 |
|---|---|---|
| 자식 노드가 있는 `Node3D` | 컴포넌트가 있는 게임 오브젝트 | 컴포넌트는 기능과 동작을, 게임 오브젝트는 변형과 식별자를 제공합니다. |
| `Node2D` / `Node3D`의 변형 | 게임 오브젝트의 변형 | 모든 게임 오브젝트에 내장되어 있습니다. |
| 씬 / `PackedScene` | 게임 오브젝트 프로토타입(`.go`) 또는 컬렉션(`.collection`) | 프로토타입은 오브젝트 하나를, 컬렉션은 계층 관계가 있는 오브젝트 그룹을 정의합니다. |
| `PackedScene.instantiate()` | 팩토리 또는 컬렉션 팩토리 | 현재 월드에 게임 오브젝트 하나나 그룹을 만들고 그 식별자를 반환합니다. |
| `SceneTree`와 `PackedScene.instantiate()`를 통한 씬 전환 | 컬렉션 프록시 | 별도의 새 월드를 로드해 만들고 그 안에 게임 오브젝트를 생성합니다. |

---

## 코드 작성 {#code-writing}

Defold 에디터에는 모든 텍스트 파일과 스크립트를 편집할 수 있는 코드 에디터가 내장되어 있습니다. 자동 완성, 코드 포멧팅, 데이터와 함수의 구성을 보여 주는 Structure 뷰 등을 지원합니다. 자세한 내용은 [내장 코드 에디터 사용하기](/manuals/writing-code/#using-the-built-in-code-editor)를 참고하세요.

Defold의 텍스트 파일과 스크립트는 외부 에디터에서도 열 수 있습니다. Defold는 VS Code 같은 외부 도구와의 연동을 돕는 기능을 제공합니다. 자세한 내용은 [외부 코드 에디터 사용하기](/manuals/writing-code/#using-an-external-code-editor)를 참고하세요.

### Lua와 스크립트 {#lua-and-scripts}

Defold에서는 게임플레이 스크립트를 Lua로 작성합니다. GDScript와 비슷하게 느껴질 수 있지만 몇 가지 중요한 차이가 있습니다. Defold는 Lua의 정적 타입 방언인 Teal도 지원합니다. 또한 GDExtension처럼 대상 플랫폼에 따라 C, C++, C#, Objective-C, Java, JavaScript로 작성한 네이티브 익스텐션을 사용할 수 있습니다. 익스텐션은 뒤에서 따로 다룹니다.

Defold에서 주로 사용하는 Lua 파일은 다음과 같습니다.

| 파일 | 용도 |
|---|---|
| `.script` | 게임 로직과 동작을 구현합니다. `go`, `factory`, `sprite`, `tilemap`, `physics` 등의 API로 다른 게임 오브젝트와 컴포넌트를 제어합니다. |
| `.gui_script` | GUI 전용 스크립트로, `gui` API를 사용해 동작을 정의합니다. |
| `.render_script` | `render` API로 렌더링을 제어합니다. |
| `.lua` | 코드 라이브러리나 유틸리티 스크립트처럼 여러 곳에서 재사용할 수 있는 Lua 모듈입니다. `require()`로 불러옵니다. |

Lua 테이블에는 데이터와 함수 중 하나만 담을 수도 있고 둘 다 담을 수도 있습니다. 코드를 정리하기 위해 GDScript의 클래스 계층을 그대로 재현할 필요는 없습니다. 재사용할 로직을 모듈에 넣고 해당 동작을 담당하는 스크립트에서 호출하세요.

Defold는 Lua 5.1과 호환되는 스크립팅 환경을 사용합니다. 언어와 플랫폼별 차이는 [Defold에서의 Lua](/manuals/lua/)를 참고하세요.

### 어플리케이션 라이프사이클 {#application-lifecycle}

일반적으로 Defold 게임은 초기화 단계에서 시작해 종료 처리 단계에서 끝납니다. 두 단계 사이에서는 프레임마다 업데이트 루프가 돌면서 변형과 컴포넌트를 갱신하고 코드를 실행하며 메세지를 처리합니다.

![Defold 어플리케이션의 라이프사이클](images/application_lifecycle/application_lifecycle.png)

Godot를 비롯한 다른 게임 엔진처럼 Defold 스크립트에도 어플리케이션의 각 단계에서 호출되는 Lua 콜백 함수가 있습니다. 이름은 달라도 역할은 익숙할 것입니다.

| Godot | Defold | 역할 |
|---|---|---|
| `_ready()` | `init(self)` | 인스턴스 데이터를 초기화하고 필요하면 입력 포커스를 획득합니다. |
| `_process(delta)` | `update(self, dt)` | 프레임마다 한 번 업데이트합니다. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | 고정 업데이트가 활성화되면 일정한 시간 간격으로 업데이트합니다. |
| `_input(event)` | `on_input(self, action_id, action)` | 오브젝트의 입력 리스너에 전달된 입력을 처리합니다. |
| 시그널 콜백 | `on_message(self, message_id, message, sender)` | 스크립트나 엔진 컴포넌트가 보낸 메세지를 받습니다. |
| `_exit_tree()` | `final(self)` | 스크립트 인스턴스의 수명이 끝날 때 정리 작업을 합니다. |

Godot에서는 자식의 `_ready()`가 부모보다 먼저 호출됩니다. Defold는 게임 오브젝트나 컴포넌트 사이의 초기화 순서와 업데이트 순서를 보장하지 않습니다. 특정 오브젝트의 `init()`이 먼저 실행된다고 가정하지 말고 메세지로 동작을 조율하세요.

`fixed_update()`를 사용하려면 `game.project`에서 **Engine ▸ Fixed Update Frequency**를 60과 같은 양수로 설정하고 **Physics ▸ Use Fixed Timestep**을 활성화합니다.

일반 업데이트가 끝난 뒤 렌더링 전에 카메라 조정 같은 작업을 하려면 `late_update(self, dt)`를 사용할 수 있습니다. 필요하면 그 뒤에 변형이 마지막으로 한 번 더 갱신될 수 있습니다.

컴포넌트를 비활성화하는 것과 삭제하는 것은 다릅니다.

전체 실행 순서와 스크립트 타입별 콜백은 [어플리케이션 라이프사이클 매뉴얼](/manuals/application-lifecycle/)을 참고하세요.

### 인스턴스 데이터와 지역 데이터 {#instance-data-vs-local-data}

각 스크립트 컴포넌트 인스턴스는 콜백에 자신만의 `self`를 전달받고, 여기에 `self.health`나 `self.target` 같은 인스턴스 상태를 저장합니다. 같은 게임 오브젝트에 붙은 스크립트 컴포넌트 두 개도 서로 다른 `self`를 사용합니다. `self`의 필드에는 테이블처럼 접근할 수 있지만 실제 타입은 Lua 테이블이 아닌 userdata이므로 `pairs(self)` 같은 연산을 사용할 수 없습니다. Godot에서는 인스턴스 변수(`var`)가 비슷한 역할을 합니다.

Godot는 각 `.gd` 파일을 클래스의 설계도로 취급합니다. `.gd` 파일 하나를 적 10개에 붙이면 클래스 인스턴스가 10개 생성되고, 각 인스턴스에는 파일 최상위에서 var로 선언한 변수의 사본이 생깁니다.

Defold는 스크립트 리소스를 로드할 때 `.script` 파일을 하나의 Lua 코드 청크로 실행합니다. 각 스크립트 컴포넌트 인스턴스는 `init(self)`, `update(self, dt)` 같은 라이프사이클 콜백에서 자신만의 `self`를 받습니다.

반면 Defold의 `.script` 파일 최상위에서 선언한 지역 변수는 이 스크립트의 **모든 인스턴스**가 공유합니다. 이런 파일 수준의 지역 변수에 대응하는 Godot 개념은 정적 변수(`static var`)입니다.

![Defold에서 인스턴스 데이터와 지역 데이터의 차이](images/lua/self_local.png)

위 예제에서 한 인스턴스의 `self.has_shield`를 `true`로 바꿔도 다른 인스턴스에는 영향을 주지 않습니다. 반면 지역 변수 `color`는 이 스크립트 파일을 사용하는 모든 인스턴스가 공유하므로 값을 바꾸면 다른 인스턴스에도 영향을 줄 수 있습니다.

### 프로퍼티 {#properties}

인스턴스별로 편집할 수 있는 **프로퍼티**를 만들 때는 `go.property()`를 사용합니다. 값은 `self`를 통해 접근할 수 있습니다. Godot의 `@export`처럼 에디터에 값을 노출하며, Defold에서는 `Properties` 창에 표시됩니다.

![Defold 에디터의 Properties 창](images/script-properties/properties.png)

Godot에서 `Node3D`에 연결하는 **GDScript** 예제입니다.

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

Defold에서는 같은 동작을 **Lua**로 작성해 스크립트 컴포넌트로 붙입니다.

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Lua에서는 이 프로퍼티에 `self.speed`로 접근하며, 오브젝트를 생성할 때 값을 전달할 수도 있습니다. Defold의 변형은 2D에서도 `vector3`를 사용하므로 Z 좌표까지 지정합니다.

지원하는 프로퍼티 타입은 [스크립트 프로퍼티](/manuals/script-properties/)를, 더 많은 예제는 [스크립트 매뉴얼](/manuals/script/)을 참고하세요.

---

## 메세지와 주소 지정 {#messages-and-addressing}

Godot에서 오브젝트는 시그널(signal)로 연결된 리스너에 이벤트를 알립니다. Defold 스크립트는 일반적으로 오브젝트나 컴포넌트의 주소로 메세지를 보내 통신합니다.

Defold에서는 어느 스크립트에서나 `msg.post()` 함수로 메세지를 보낼 수 있습니다. 수신한 메세지는 스크립트의 `on_message()` 콜백에서 처리합니다.

![Defold의 메세지 전달](images/message_passing/messages_overview.png)

예를 들어 플레이어가 HUD에 점수 변경을 알리는 상황을 살펴봅시다.

Godot에서 `Player`(`Node2D`)는 `player.gd`를 사용합니다. 같은 부모를 둔 `GUI`(`CanvasLayer`)는 `gui.gd`를 사용하고, 그 아래에는 `ScoreText`라는 Label 노드가 있습니다.

![Godot에서 점수 변경 시그널을 사용하는 노드 구성](images/godot/godot_signals.png)

Defold에서 `player` 게임 오브젝트에는 `player.script`가 있습니다. `hud` 게임 오브젝트의 `gui` 컴포넌트에는 `score` 텍스트 노드가 있고, 이 컴포넌트는 `hud.gui_script`를 사용합니다.

![Defold에서 점수 변경 메세지를 사용하는 게임 오브젝트 구성](images/godot/defold_messages.png)

### 메세지 보내기 {#sending-messages}

Godot에서 Player와 GUI는 형제 노드입니다. Player가 자신의 `score_changed` 시그널을 GUI 스크립트의 메서드에 연결하면 그 메서드가 Label을 업데이트합니다.

**GDScript**로 작성한 `player.gd`입니다.

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

Godot의 `Player`는 `score_changed` 시그널을 정의합니다. `_ready()`에서 이 시그널을 GUI 스크립트의 `set_score()` 메서드에 연결합니다. `collect()`가 호출될 때마다 점수를 올리고 시그널로 새 값을 보냅니다.

Defold에서는 입력 바인딩에서 **Space** 키를 `collect` 동작에 연결합니다. `player`는 `init()`에서 점수를 초기화하고 입력 이벤트를 받기 위해 입력 포커스를 요청합니다. `collect(self)`가 호출되면 점수를 올리고, 새 점수를 메세지 테이블에 담아 `score_changed` 메세지를 `/hud#gui`로 보냅니다.

**Lua**로 작성한 `player.script`입니다.

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

Defold에서는 Player가 GUI에 시그널을 미리 연결할 필요 없이 수신자의 주소로 메세지를 보냅니다. 이 방식에 Defold의 상대 주소 지정을 활용하면 재사용할 수 있는 함수와 스크립트를 작성할 수 있습니다.

### 메세지 수신과 처리 {#receiving-and-handling-messages}

이제 GUI가 값을 받아 점수 텍스트를 업데이트합니다.

**GDScript** 파일 `gui.gd`는 `GUI`(`CanvasLayer`)에 연결합니다.

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

GUI 스크립트는 `set_score()`를 통해 시그널이 보낸 값을 받은 다음 자식인 `ScoreText` Label을 업데이트합니다. Player는 Label에 직접 접근하거나 값을 변경하지 않습니다.

Defold의 GUI 스크립트는 먼저 `gui.get_node()`로 점수 텍스트 노드를 가져옵니다. GUI 컴포넌트가 메세지를 받으면 `on_message()`에서 메세지 ID를 확인합니다. ID가 `score_changed`이면 `message.value`를 읽고 `gui.set_text()`로 텍스트를 갱신합니다.

**Lua** 파일 `hud.gui_script`는 GUI 컴포넌트에 지정합니다.

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

여기서 메세지의 수신자는 점수 텍스트 노드가 아니라 GUI **컴포넌트**입니다. 메세지를 받은 GUI 스크립트가 메세지를 어떻게 사용할지, 어느 텍스트 노드를 갱신할지 결정합니다.

두 화면의 초기 텍스트는 모두 `Score: 0`입니다. 점수가 바뀌면 두 예제 스크립트 모두 텍스트 전체를 점수 숫자로 바꿉니다.

`msg.post()`는 수신자를 즉시 호출하는 대신 나중에 전달할 메세지를 큐에 넣으며, 수신 스크립트의 실행 결과를 반환하지 않습니다. 대개 같은 프레임 안에 메세지가 전달되지만, 한 프레임에 처리할 수 있는 전달 횟수에는 한계가 있습니다. 따라서 메세지가 길게 연쇄되면 다음 프레임까지 전달이 이어질 수 있습니다. 응답이 필요하면 수신자가 `on_message()`에 전달된 발신자 URL로 별도의 메세지를 보낼 수 있습니다. 자세한 내용은 [메세지 체인](/manuals/message-passing/#message-chains)을 참고하세요.

여러 리스너와 통신하는 방식도 다릅니다. Godot에서는 시그널 하나에 여러 메서드를 연결할 수 있고, 시그널을 보내면 연결된 모든 리스너가 통지를 받습니다. Defold의 메세지는 특정 주소로 보냅니다. 여러 수신자에게 알리려면 각 주소로 메세지를 보내거나 게임에서 구독 시스템을 구현하면 됩니다.

### 오브젝트 찾기와 Defold의 주소 지정 {#finding-an-object-addressing-in-defold}

Defold에는 다른 스크립트 인스턴스를 나타내는 Lua 오브젝트를 반환하는 범용 `get_node()` 함수가 없습니다. 대신 식별자나 **URL**을 `go.get_position()`, `go.set()`, `msg.post()` 같은 엔진 API에 전달합니다.

Defold의 URL은 세 부분으로 구성됩니다.

```lua
socket:/path#component
```

- **소켓(Socket)**은 부트스트랩의 메인 컬렉션이나 컬렉션 프록시로 로드한 월드 등 하나의 월드를 식별합니다.
- **경로(Path)**는 해당 월드 안에서 게임 오브젝트를 식별합니다.
- **컴포넌트(Component)**는 그 게임 오브젝트에 속한 컴포넌트를 식별합니다.

전체 URL을 쓰거나 일부를 생략해 상대 주소를 만들 수 있습니다. 예를 들어 스크립트에서 컴포넌트 부분만 지정하면 같은 게임 오브젝트에 있는 컴포넌트를 가리킵니다. 자주 쓰는 주소는 다음과 같습니다.

| 주소 | 의미 |
|---|---|
| `"#sprite"` | 현재 게임 오브젝트의 sprite 컴포넌트입니다. |
| `"/player#controller"` | 현재 월드에서 player 오브젝트에 붙은 controller 컴포넌트입니다. |
| `"level:/player#controller"` | 로드된 level 월드에 있는 player 오브젝트의 controller 컴포넌트입니다. |
| `"."` | 현재 `Game Object`를 가리키는 약칭입니다. 메세지는 이 오브젝트의 컴포넌트들에 전달됩니다. |
| `"#"` | 현재 `Script` 컴포넌트를 가리키는 약칭입니다. |

중첩 컬렉션은 오브젝트 경로에 접두사를 더할 수 있지만, 변형을 상속하기 위해 부모를 바꾸는 작업은 오브젝트의 주소를 바꾸지 않습니다.

동적으로 생성한 오브젝트를 다시 참조하려면 `factory.create()`나 `collectionfactory.create()`가 반환한 식별자를 코드에 보관하세요.

게임플레이에서 오브젝트를 조회하거나 `call_group()`으로 호출할 때 쓰는 Godot의 그룹 기능은 Defold에 내장되어 있지 않습니다. 이와 같은 기능이 필요하면 오브젝트를 직접 등록해 두거나 메세지를 전달할 경로를 구현해야 합니다.

Defold에서 충돌 오브젝트의 물리 그룹은 충돌을 필터링하는 데 사용합니다. 마스크에 지정한 그룹에 따라 서로 충돌할지를 결정하며 메세지 전달과는 관계가 없습니다.

프로젝트를 시작할 때 [주소 지정](/manuals/addressing/)과 [메세지 전달](/manuals/message-passing/) 매뉴얼을 읽어 보세요. 첫 프로젝트에서 자주 생기는 의문을 해결하는 데 도움이 됩니다.

---

## 오토로드와 공유 상태 {#autoloads-and-shared-state}

Defold의 메세지 시스템으로 통신하는 것 외에, Lua 모듈의 함수를 직접 호출하는 방법도 있습니다.

Godot에서 **오토로드(Autoload)**에 공유 데이터를 저장했다면 Defold에서는 Lua 모듈을 같은 용도로 사용할 수 있습니다. 예를 들어 모듈을 `modules/game_state.lua`에 저장하고 `require "modules.game_state"`로 로드합니다.

**GDScript** 예제에서는 `game_state.gd`를 `GameState`라는 이름의 오토로드로 등록합니다.

```gdscript
extends Node
var score: int = 0
```

이에 대응하는 **Lua** 모듈 `modules/game_state.lua`입니다.

```lua
local M = { score = 0 }
return M
```

이제 다른 스크립트에서 공유 데이터를 사용할 수 있습니다.

**GDScript**

```gdscript
func add_point():
    GameState.score += 1
```

**Lua**

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

`require()`는 모듈을 캐시에 보관하므로 호출한 곳에서는 그 모듈이 반환한 테이블을 공유합니다. 게임 오브젝트, GUI, 렌더 스크립트는 같은 Lua 상태를 공유합니다. 컬렉션 프록시를 언로드해도 모듈 데이터는 초기화되지 않습니다. 새 게임을 시작할 때 필요하면 직접 초기화하세요.

Defold의 Lua 모듈은 게임 오브젝트가 아니므로 라이프사이클, 메세지, 입력 콜백을 받지 않습니다. Godot에서 오토로드로 매 프레임 로직을 실행하거나 사운드를 재생하거나 레벨 전환을 관리했다면, Defold에서는 컬렉션 안의 게임 오브젝트에 붙인 스크립트에 그 동작을 작성하세요. 다음과 같이 모듈에 함수를 정의하고 스크립트의 라이프사이클 콜백에서 명시적으로 호출할 수도 있습니다.

Lua 모듈 `my_module`입니다.

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

모듈을 호출하는 Lua 스크립트입니다.
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

인스턴스마다 데이터를 따로 유지하려면, 모듈이 새 테이블을 만드는 함수를 반환하도록 하고 그 함수로 만든 테이블을 `self`에 저장하면 됩니다. 자세한 설명과 핫 리로드 시 주의할 점은 [모듈 매뉴얼](/manuals/modules/)을 참고하세요.

---

## 오브젝트 생성과 레벨 로드 {#spawning-objects-and-loading-levels}

### 팩토리 {#factories}

Defold에서 게임 오브젝트 하나를 생성하려면 **Factory** 컴포넌트를 추가하고 **Prototype**에 생성할 오브젝트의 `.go` 파일을 지정합니다.

컬렉션의 경우에는 **Collection Factory** 컴포넌트를 추가하고 `.collection` 파일을 지정합니다. 오브젝트들의 부모-자식 관계를 유지한 채 그룹 전체를 생성합니다.

다음 Godot 예제에서는 씬의 원점에 배치한 `Node2D`에 스크립트를 붙여 총알을 생성합니다.

**GDScript**

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

Defold에서는 게임 오브젝트에 ID가 `bullet_factory`인 팩토리 컴포넌트를 붙입니다. `factory.create()`를 호출하면 이 팩토리의 `Prototype`이 참조하는 게임 오브젝트를 생성할 수 있습니다.

![Defold에서 총알을 생성하는 팩토리 설정](images/godot/defold_factory.png)

위 화면에서는 `init()`에서 팩토리를 호출합니다. 다음 함수는 생성할 위치를 지정하고 새 오브젝트의 식별자를 반환하는 예제입니다.

**Lua**

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

Defold의 함수가 반환하는 값은 메서드를 가진 오브젝트가 아니라 오브젝트의 **식별자**입니다. 이 식별자를 `go` 함수에 전달할 수 있습니다. 생성된 오브젝트에 `controller`라는 스크립트 컴포넌트가 있다면 `msg.url(nil, id, "controller")`로 그 컴포넌트의 URL을 만들 수 있습니다.

컬렉션 팩토리는 프로토타입 안의 오브젝트 ID를 새로 생성한 오브젝트의 ID에 대응시키는 테이블을 반환합니다. 나중에 이 오브젝트들을 삭제하려면 테이블을 보관하세요.

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

Godot의 `queue_free()`와 달리 Defold의 `go.delete(id)`는 기본적으로 자식을 재귀적으로 삭제하지 않습니다. 오브젝트와 그 아래에 현재 연결된 모든 자손을 삭제하려면 `go.delete(id, true)`를 사용하세요. 팩토리가 반환한 테이블을 `go.delete(ids)`에 넘기면 테이블에 있는 오브젝트들만 삭제하고, 나중에 그 아래에 붙인 다른 오브젝트는 남겨 둡니다. 반면 루트 오브젝트를 지정해 재귀적으로 삭제하면 나중에 붙인 오브젝트까지 현재 그 아래에 있는 모든 오브젝트가 삭제됩니다. [`go.delete()`](/ref/go/#go.delete)를 참고하세요.

Defold는 게임 오브젝트와 컴포넌트에 필요한 공간을 미리 할당합니다. 개수 제한에 걸려 생성에 실패하면 `game.project`에서 **Collection ▸ Max Instances**와 해당 컴포넌트의 제한을 확인하세요. 모든 제한을 일괄적으로 높이면 메모리 사용량도 늘어납니다.

프로퍼티, 변형, 동적 로드에 대한 자세한 내용은 [팩토리](/manuals/factory/)와 [컬렉션 팩토리](/manuals/collection-factory/) 매뉴얼을 참고하세요.

### 컬렉션 프록시 {#collection-proxies}

레벨 전환 등을 위해 Defold에서 컬렉션을 로드하려면, 계속 유지할 게임 오브젝트에 **Collection Proxy** 컴포넌트를 추가하고 **Collection** 프로퍼티에 대상 `.collection` 파일을 지정합니다.

![Defold에서 컬렉션 프록시 설정](images/godot/defold_proxy.png)

`"load"` 또는 `"async_load"`를 `msg.post()`로 보냅니다. 로드가 끝나면 프록시가 `"proxy_loaded"` 메세지로 응답합니다. on_message의 `sender`로 전달된 주소에 `"init"`과 `"enable"`을 차례로 보내 로드한 컬렉션의 월드를 초기화하고 실행합니다.

이 방식으로 어떤 월드를 로드하고 실행할지 직접 제어할 수 있습니다. Godot에서 씬을 바꿀 때와 달리 현재 씬이 자동으로 교체되지는 않습니다. 다른 컬렉션을 언로드해 월드를 제거하려면 해당 프록시에 `"unload"` 메세지를 보내세요. 프록시는 월드를 자동으로 비활성화하고 종료 처리한 다음 언로드하고 `"proxy_unloaded"`로 응답합니다. 각 단계를 직접 제어해야 한다면 `"disable"`과 `"final"`을 따로 보낼 수도 있습니다.

서로 다른 프록시 월드에 속한 충돌 오브젝트끼리는 두 월드가 동시에 로드되어 한 화면에 보이더라도 충돌하지 않습니다. 다만 게임 오브젝트와 컴포넌트는 대상 소켓이 포함된 URL을 사용해 월드 사이에서 메세지를 주고받을 수 있습니다.

레벨 전환을 구현하기 전에 [컬렉션 프록시 매뉴얼](/manuals/collection-proxy/)을 읽어 보세요. 로드와 언로드, 입력 전달, 로드된 월드의 업데이트 속도 제어를 설명합니다.

## 프로젝트 리소스와 에셋 {#project-resources-and-assets}

Defold 프로젝트는 `game.project`와 스크립트, 리소스가 들어 있는 폴더입니다. **Assets** 창은 이 폴더의 구조를 그대로 보여 줍니다. 대부분의 Defold 리소스 정의는 텍스트 파일이므로 버전 관리 시스템에서 변경 내용을 확인할 수 있습니다.

게임을 빌드하거나 번들링하면 Defold는 소스 리소스를 런타임 포멧으로 변환합니다. 메인 컬렉션, 팩토리, 컬렉션 프록시에서 참조하는 리소스는 의존성 트리를 이룹니다. 프로젝트 폴더에 파일을 넣었더라도 어디에서도 참조하지 않으면 번들에 포함되지 않습니다.

Godot의 사용자 정의 `Resource` 클래스와 `.tres` 파일에 대응하는 단일 범용 기능은 Defold에 없습니다. 엔진 컨텐츠에는 Defold의 리소스 타입을, 게임 고유의 데이터에는 Lua 테이블이나 데이터 파일을 사용하세요. [`resource` API](/ref/resource/)를 사용하면 지원되는 리소스를 런타임에 만들거나 수정할 수 있습니다.

일반 팩토리의 리소스는 팩토리와 함께 로드됩니다. 로드를 미루려면 **Load Dynamically**를 활성화하고 `factory.load()`나 `collectionfactory.load()`로 비동기 로드하세요. 컬렉션 프록시의 컨텐츠는 로드를 요청할 때 불러옵니다.

번들에 있는 컨텐츠를 나중에 로드하는 것과 컨텐츠 자체를 나중에 다운로드하는 것은 별개의 작업입니다. Defold의 [Live Update](/manuals/live-update/)를 사용하면 초기 번들에서 일부 컨텐츠를 제외하고 별도로 제공할 수 있습니다.

자세한 내용은 [리소스 관리 매뉴얼](/manuals/resource/)을 참고하세요.

---

## 입력 {#input}

Godot의 `InputMap`에 해당하는 Defold 파일은 `.input_binding`입니다. 키보드, 게임패드, 마우스, 터치, 텍스트 입력의 트리거를 동작 이름에 연결하고, `game.project`의 **Input ▸ Game Binding**에서 이 바인딩 파일을 선택합니다.

![Defold의 입력 바인딩](images/input/defold_input.png)

Defold에서 입력을 받을 게임 오브젝트는 먼저 **입력 포커스를 획득**해야 합니다. 그러면 오브젝트가 인풋 스택에 올라가고, 그 오브젝트의 스크립트와 GUI 컴포넌트가 `on_input()` 콜백을 받을 수 있습니다.

위 화면에서는 Space 키가 `collect`에 바인딩되어 있습니다. 아래는 별도의 예제로, 실행하려면 입력 바인딩에 `fire`라는 동작도 추가해야 합니다.

**GDScript**

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua**

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

`action` 테이블에는 입력 종류에 따라 `pressed`, `released`, `value` 등의 값이 담깁니다.

입력은 가장 최근에 포커스를 획득한 리스너부터 인풋 스택을 따라 전달됩니다. 예를 들어 메뉴에서 클릭을 처리한 뒤 다른 곳에 전달하지 않으려면 `on_input()`에서 `true`를 반환해 동작을 소비합니다.

프록시로 로드한 월드에서는 그 안의 리스너뿐 아니라 프록시를 가진 오브젝트도 입력 포커스를 획득해야 합니다. 잘 동작하던 스크립트가 레벨 전환 후 입력을 받지 못한다면 두 단계 중 하나를 빠뜨렸는지 확인하세요.

자세한 내용은 [입력](/manuals/input/), [마우스와 터치](/manuals/input-mouse-and-touch/), [게임패드](/manuals/input-gamepads/) 매뉴얼을 참고하세요.

---

## 물리와 충돌 {#physics-and-collisions}

Defold의 **충돌 오브젝트(Collision Object)**는 Godot의 물리 바디에 해당합니다. 물리 설정과 충돌 모양을 **하나의 컴포넌트**에 함께 정의합니다. `game.project`에서 2D 또는 3D 물리를 선택할 수 있습니다. App Manifest에서는 사용할 물리 엔진 버전을 바꾸거나 물리를 완전히 비활성화할 수도 있습니다.

Defold의 충돌 오브젝트에는 네 가지 타입이 있습니다.

| Godot | Defold 타입 | 설명 |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | 움직이지 않습니다. 동적 오브젝트가 여기에 부딪히면 반응합니다. |
| `RigidBody2D` / `3D` | `Dynamic` | 물리 엔진이 움직임을 시뮬레이션하고 충돌을 해결합니다. |
| `CharacterBody2D` / `3D` | `Kinematic` | 물리 엔진은 충돌 정보를 제공하고, 그에 대한 반응과 충돌 해결은 코드에서 처리합니다. |
| `Area2D` | `Trigger` | 물리적인 반응 없이 진입과 이탈 이벤트만 알립니다. |

Defold의 키네마틱 오브젝트는 `move_and_slide()`를 사용하는 `CharacterBody2D`와 동작이 다릅니다. Defold는 접촉을 감지해 충돌 응답 메세지에 관련 정보를 담아 보내지만, 이동과 충돌 반응은 스크립트에서 구현합니다. 캐릭터 컨트롤러를 만들 때는 [충돌 해결 매뉴얼](/manuals/physics-resolving-collisions/)을 참고하세요.

그룹과 마스크는 번호가 붙은 충돌 레이어 대신 이름을 사용합니다. 충돌이 감지되려면 **양쪽 오브젝트가 모두 자기 마스크에 상대 오브젝트의 그룹을 포함해야 합니다**.

![Defold의 충돌 그룹과 마스크](images/physics/collision_groups.png)

위 화면에서 `danger`라는 게임 오브젝트는 `player` 그룹에 속하고, `player`라는 오브젝트는 `danger` 그룹에 속합니다. 그룹 이름은 오브젝트 ID와 같을 필요가 없습니다. 그림의 마스크 설정에서는 이 두 그룹이 서로 충돌할 수 있습니다.

기본적으로 충돌 오브젝트는 자신이 속한 게임 오브젝트의 스크립트에 메세지를 보냅니다. `on_message()`에서 `"collision_response"`, `"contact_point_response"`, `"trigger_response"`를 처리하세요. 트리거 메세지는 `enter` 필드로 진입과 이탈을 구분합니다. 오브젝트들이 계속 닿아 있는 동안 충돌과 접촉 메세지가 반복될 수 있으므로 메세지마다 새로 충돌했다고 가정하면 안 됩니다.

물리 이벤트는 [충돌 이벤트 리스너](/manuals/physics-events/)로도 처리할 수 있습니다. 리스너를 등록하면 기본 물리 메세지 전달을 대체해 더 이상 해당 메세지가 전송되지 않으므로, 어느 방식을 쓸지 정해야 합니다.

단순한 기본 모양부터 복잡한 모양까지 다양한 충돌 모양을 사용할 수 있습니다. 자세한 내용은 [충돌 모양 매뉴얼](/manuals/physics-shapes)을 참고하세요.

![메쉬 충돌 모양](images/physics/mesh.png)

관련 개념과 API는 [물리 개요](/manuals/physics/), [충돌 오브젝트](/manuals/physics-objects/), [충돌 메세지](/manuals/physics-messages/), [레이 캐스트](/manuals/physics-ray-casts/) 매뉴얼을 참고하세요.

---

## GUI {#gui}

Defold의 UI는 `.gui` 파일로 만드는 **GUI 컴포넌트** 안에 구성합니다. 여기에는 박스, 텍스트, 파이 등의 GUI 노드를 배치할 수 있습니다. Godot에서 `CanvasLayer`에 붙인 스크립트처럼, 전용 `.gui_script`가 GUI 컴포넌트를 제어합니다.

이 노드들은 GUI에 속하며 게임 오브젝트의 변형 계층과는 분리되어 있습니다. 기본적으로 GUI는 게임 화면 위에 그려지며, 게임 카메라나 GUI 컴포넌트를 가진 게임 오브젝트가 움직여도 따라 움직이지 않습니다.

`.gui_script`를 지정하면 `gui.get_node()`, `gui.set_text()` 등의 `gui` 함수로 노드를 제어할 수 있습니다. `gui` API는 GUI 스크립트에서만, `go` API는 게임 오브젝트 스크립트에서만 사용할 수 있습니다. 두 스크립트 사이는 앞서 살펴본 점수 예제처럼 메세지로 통신합니다.

템플릿을 사용하면 다른 GUI의 노드 계층을 재사용할 수 있습니다. Godot에서 노드를 재사용하는 것과 비슷합니다.

Defold는 Godot의 Button이나 레이아웃 Container처럼 완성된 위젯을 제공하는 대신, 단순한 노드를 조합해 UI를 만들도록 합니다. 예를 들어 버튼을 만들려면 박스와 텍스트를 배치하고 GUI 스크립트에서 입력을 처리합니다. 포인터가 노드 위에 있는지는 `gui.pick_node()`로 확인합니다.

Defold GUI는 Godot의 `CanvasLayer`와 비슷한 **레이어(Layers)**도 지원합니다. Defold에서 레이어는 번호 대신 이름으로 구분하며, Layers 목록에 배치된 순서가 그리기 순서를 결정합니다.

앵커, 피벗, 조정 모드, [GUI 레이아웃](/manuals/gui-layouts/)을 사용하면 다양한 화면에 맞춰 인터페이스를 배치할 수 있습니다. Godot의 레이아웃 Container와 목적은 비슷하지만 각 기능이 하는 일은 다릅니다.

더 크거나 복잡한 UI라면 레이아웃과 위젯 코드를 직접 작성하거나 [Druid](https://defold.com/assets/druid/) 같은 커뮤니티 라이브러리를 사용할 수 있습니다.

자세한 내용은 [GUI](/manuals/gui/)와 [GUI 스크립트](/manuals/gui-script/) 매뉴얼을 참고하세요.

## 애니메이션 {#animation}

Defold에는 `AnimationPlayer`에 대응하는 도구 하나가 있는 대신 용도에 따라 여러 애니메이션 도구가 있습니다.

- **플립북 애니메이션**은 스프라이트와 GUI 박스에 여러 이미지를 순서대로 표시합니다.
- **모델 애니메이션**은 3D 모델에서 임포트한 스켈레탈 애니메이션을 재생합니다.
- **프로퍼티 애니메이션**은 `go.animate()`나 `gui.animate()`로 값을 보간합니다.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)**, **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)**는 익스텐션을 통해 추가로 사용할 수 있는 애니메이션 포멧입니다.

### 트윈과 Defold의 프로퍼티 애니메이션 {#tweens-defold-property-animations}

Godot의 간단한 트윈(Tween)은 Defold의 프로퍼티 애니메이션으로 구현할 수 있습니다. 다음 두 예제는 모두 0.5초 동안 오브젝트를 `X = 200`까지 이동시킵니다.

`Node2D`에 연결한 **GDScript**입니다.

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

게임 오브젝트 스크립트에 작성하는 **Lua** 코드입니다.

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

여러 프로퍼티를 바꾸거나 소리를 재생하고 게임플레이 이벤트를 일으키는 시퀀스는 Lua로 각 단계를 조율합니다. Defold에는 아직 애니메이션 타임라인 전용 에디터가 없습니다. Tools 창의 Curve Editor는 개별 파티클의 수명에 따른 ParticleFX 프로퍼티 곡선을 편집하는 도구입니다.

[애니메이션](/manuals/animation/), [프로퍼티 애니메이션](/manuals/property-animation/), [플립북 애니메이션](/manuals/flipbook-animation/), [모델 애니메이션](/manuals/model-animation/) 매뉴얼을 참고하세요. 애니메이션 개요에는 Spine과 Rive 익스텐션 링크도 있습니다.

## 타일맵 {#tilemaps}

Defold의 `Tilemap` 컴포넌트는 타일을 격자로 배치한 **타일 소스**를 사용합니다. 내장 타일맵 에디터에서 각 레이어에 타일을 칠하고, 런타임에는 `tilemap` API로 타일을 바꿀 수 있습니다.

Defold의 내장 타일맵은 직사각형 그리드를 사용합니다. Godot의 지형 세트와 오토타일링 규칙은 아직 Defold로 그대로 옮길 수 없습니다. 필요한 동작을 코드로 구현하거나 [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website)나 [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold)처럼 Defold용으로 내보낼 수 있는 외부 맵 도구를 사용하세요.

[타일맵 매뉴얼](/manuals/tilemap/)을 참고하세요.

---

## 렌더링 파이프라인 {#rendering-pipeline}

Defold에서는 사용자 정의 `.render` 파일과 `.render_script`, 쉐이더를 조합해 렌더링 파이프라인 전체를 스크립트로 제어할 수 있습니다. 대부분의 게임에는 내장된 기본 렌더링 파이프라인을 그대로 사용할 수 있습니다.

Defold의 기본 렌더 스크립트는 일반적인 2D와 3D 컨텐츠를 처리합니다. 사용자 정의 `.render_script`에서는 그리기 패스, 렌더 타겟을 비롯한 렌더링 작업을 제어합니다. 메터리얼에 태그를 지정하면 렌더 predicate로 그릴 컴포넌트 그룹을 선택할 수 있습니다. Defold는 PBR 렌더링도 기본으로 지원합니다. 커뮤니티에서 만든 다양한 렌더링 파이프라인과 쉐이더도 있습니다.


Defold는 GLSL 쉐이더를 사용하며 버텍스와 프래그먼트 코드를 별도의 파일에 작성합니다. Godot는 GLSL과 비슷하지만 엔진 고유의 내장 기능이 있는 언어를 사용하므로, Godot나 Shadertoy 등에서 가져온 쉐이더는 수정이 필요할 수 있습니다. Defold 쉐이더의 요구 사항은 [쉐이더 매뉴얼](/manuals/shader/)을 참고하세요.

Defold의 **메터리얼(Material)**은 버텍스 및 프래그먼트 프로그램(쉐이더), 텍스쳐, 쉐이더 상수와 어트리뷰트를 연결합니다. 처음 메터리얼을 만들 때는 `builtins` 폴더에 있는 기본 메터리얼을 출발점으로 삼을 수 있습니다.

기본 동작을 바꾸려면 [렌더링](/manuals/render/), [메터리얼](/manuals/material/), [쉐이더](/manuals/shader/) 매뉴얼을 참고하세요.

### 그리기 순서와 레이어 {#draw-order-and-layers}

Godot의 정수형 `z_index`에 바로 대응하는 Defold 프로퍼티는 없습니다. Defold는 기본적으로 3D 엔진이므로 2D 정렬 전용 정수 대신 공간상의 실제 Z 좌표를 사용합니다. Z축으로 이동할 때 깊이가 어떻게 달라지는지는 렌더링 설정에 따라 다릅니다.

Defold의 **기본** 직교 투영에서는 Z 위치가 -1.0에서 1.0 사이인 오브젝트만 렌더링합니다. 레이어를 나누려면 0.1이나 0.2 같은 소수를 사용할 수 있으며, 그 범위는 렌더 스크립트에 메세지를 보내 변경할 수 있습니다. 기본 설정에서는 이 범위 안의 게임 오브젝트나 스프라이트 컴포넌트를 실제 Z 위치로 정렬합니다. Z가 클수록 위에 그려지므로 Godot의 `z_index`와 비슷하게 느껴질 수 있습니다. 원근 카메라로 바꾸거나 `.render_script`를 수정하면 그 순서가 달라질 수 있습니다.

Defold의 GUI 노드는 월드 Z 좌표를 무시합니다. 기본적으로 GUI 컴포넌트는 월드 스프라이트를 그린 뒤 별도 패스에서 렌더링되므로 GUI 노드의 Z 위치를 바꿔도 그리기 순서는 바뀌지 않습니다. 순서는 Outline에 표시된 GUI 계층의 위에서 아래 방향과 GUI의 `Layers`로 결정됩니다. 레이어는 드로우콜을 묶을 수 있도록 노드 순서보다 우선하며, 이 점은 Godot의 `CanvasLayer` 레이어와 비슷합니다.

### 카메라와 좌표 {#cameras-and-coordinates}

게임 오브젝트에 `Camera` 컴포넌트를 붙이면 그 오브젝트를 이동해 카메라를 움직일 수 있습니다. 일반적인 2D 뷰에는 직교 투영을, 3D 뷰에는 원근 투영을 설정합니다.

기본 렌더 스크립트는 가장 최근에 활성화된 카메라를 자동으로 사용합니다. 카메라가 하나도 없으면 기본 2D 직교 뷰로 렌더링하고, 카메라가 하나 있으면 그 카메라를 사용합니다. 우선 이 설정으로 시작하고 게임에 필요할 때 렌더링을 조정하세요.

카메라는 월드 좌표가 화면에 표시되는 방식을 바꿉니다. 게임 월드의 포인터 입력을 처리할 때는 포인터 좌표를 그대로 월드 위치로 사용하지 말고 [카메라 API](/ref/camera/)의 좌표 변환 함수를 사용하세요. GUI 노드의 입력 판정에는 기본적으로 GUI 좌표를 사용합니다.

투영, 줌, 좌표 변환은 [카메라 매뉴얼](/manuals/camera/)을 참고하세요.

---

## 게임 내보내기 {#exporting-a-game}

Defold에서는 게임 내보내기를 **번들링(bundling)**이라고 합니다. **Project ▸ Bundle**을 선택하고 대상 플랫폼을 고른 다음 번들 옵션을 설정합니다. 빌드 도구는 에디터가 제공하므로 Godot의 내보내기 템플릿에 해당하는 것을 별도로 설치할 필요가 없습니다.

메인 컬렉션, 입력 바인딩, 화면 크기 등의 프로젝트 및 플랫폼 설정은 `game.project`에 저장됩니다. 플랫폼에 따라 서명이나 스토어 요구 사항을 충족해야 할 수 있습니다. 네이티브 익스텐션이 있는 프로젝트에서 클라우드 빌드 서비스로 사용자 정의 엔진을 빌드하려면 네트워크 연결이 필요합니다. 직접 로컬 빌드 환경을 설정할 수도 있습니다.

최종 번들 크기는 에셋, 익스텐션, 빌드 설정에 따라 달라집니다. 게임에 무엇이 포함됐는지 확인하려면 `Build Report`를 생성하세요.

[번들링](/manuals/bundling/), [프로젝트 설정](/manuals/project-settings/), [HTML5](/manuals/html5/) 매뉴얼을 참고하세요. 특히 쉐이더, 네이티브 익스텐션, 플랫폼 서비스를 사용하는 게임이라면 개발 초기에 대상 플랫폼에서 번들을 테스트하세요.

## 라이브러리와 익스텐션 {#libraries-and-extensions}

Defold 프로젝트에는 공유 스크립트와 리소스를 담은 **라이브러리 의존성(Library Dependencies)**을 추가할 수 있습니다. `game.project`에 라이브러리의 아카이브 URL을 추가한 다음 라이브러리를 가져옵니다. 라이브러리를 찾으려면 Defold [Asset Portal](https://defold.com/assets/)을 살펴보세요. 에디터 익스텐션인 **Asset Store**를 사용하면 Godot처럼 Defold 에디터 안에서 직접 에셋을 검색하고 다운로드할 수 있습니다.

에디터를 확장할 때는 **에디터 스크립트와 UI**로 명령을 추가하고, 작업을 자동화하고, 사용자 정의 에디터 UI를 만들 수 있습니다. 예를 들어 레벨 편집, 리소스 생성, 오토타일링 같은 반복 작업을 빠르게 처리할 수 있습니다. Godot의 `EditorPlugin` 및 `@tool`과 일부 역할이 겹치지만 Defold 고유의 `editor` API와 라이프사이클을 사용합니다.

Lua만으로 구현하기 어려운 엔진 기능에는 **네이티브 익스텐션**을 사용합니다. 스크립트에서 호출할 수 있도록 네이티브 코드를 노출하거나 컴포넌트와 플랫폼 연동 기능을 추가할 수 있습니다. GDExtension과 비슷한 역할을 하지만 API와 빌드 과정이 다릅니다.

[라이브러리](/manuals/libraries/), [에디터 스크립트](/manuals/editor-scripts/), [네이티브 익스텐션](/manuals/extensions/) 매뉴얼을 참고하세요.

## 핫 리로드 {#hot-reload}

Defold에서는 실행 중인 게임에 핫 리로드를 적용할 수 있습니다. 게임을 빌드해 실행하고, 지원되는 리소스를 편집해 저장한 다음 **File ▸ Hot Reload**를 선택하면 변경 사항이 반영됩니다. 기기에서 실행 중인 디버그 빌드를 대상으로 지정한 경우에도 핫 리로드를 사용할 수 있습니다.

스크립트를 다시 로드해도 `init()`은 다시 호출되지 않습니다. 기존 인스턴스 데이터가 유지되므로 새로 지정한 초기값이 `self`에 자동으로 반영되지 않습니다. 기존 상태를 조정하려면 `on_reload(self)`를 사용하고, 처음부터 실행하려면 다시 빌드하세요. Lua 모듈이 새 테이블을 반환하도록 다시 로드되어도 다른 스크립트가 보관하고 있는 기존 테이블 참조는 바뀌지 않습니다. 자세한 내용은 [모듈 매뉴얼](/manuals/modules/)을 참고하세요.

[핫 리로드 매뉴얼](/manuals/hot-reload/)을 참고하세요.

## 중단점과 디버깅 {#breakpoints-and-debugging}

에디터의 내장 디버거로 중단점을 지정하고 코드를 단계별로 실행하며 실행 상태를 살펴볼 수 있습니다. 런타임 출력은 Console에서, 빌드 문제는 Build Errors에서 확인합니다. 프로파일러에서는 프레임 시간, 메모리, 렌더링을 살펴볼 수 있고, 빌드 리포트에서는 어떤 리소스가 번들 크기에 영향을 주는지 확인할 수 있습니다.

[게임 로직 디버깅](/manuals/debugging-game-logic/)과 [프로파일링](/manuals/profiling/) 매뉴얼을 참고하세요.

## 작업 자동화 {#automated-workflows}

Defold는 작업 자동화와 AI를 활용한 개발에 사용할 수 있는 여러 인터페이스를 제공합니다. 에디터 스크립트로 반복 작업을 자동화할 수 있으며, OpenAPI로 문서화된 에디터 HTTP API를 통해 외부 도구와 AI 에이전트가 프로젝트를 살펴보고 명령을 실행하거나 빌드를 시작할 수 있습니다. 엔진의 HTTP 서비스와 Automation Bridge 익스텐션을 사용하면 실행 상태를 살펴보고 입력을 시뮬레이션하거나 스크린샷을 찍을 수 있습니다. Codex, Claude Code, Cursor 같은 AI 코딩 에이전트는 이런 도구를 함께 사용해 프로젝트를 수정하고 게임을 빌드한 뒤 동작을 테스트하고 문제를 고치는 과정을 반복할 수 있습니다.

자세한 내용은 [자동화](/manuals/automation/), [에디터 HTTP API](/manuals/editor-http-api/), [엔진 서비스](/manuals/engine-service/), [자동화 테스트](/manuals/automated-testing/) 매뉴얼을 참고하세요.

---

## 자주 하는 실수 {#common-pitfalls}

### 컬렉션을 루트 노드로 취급하기 {#treating-a-collection-as-a-root-node}

Defold 컬렉션은 게임 오브젝트와 그 관계를 정의하지만 런타임에서 루트 오브젝트가 되지는 않습니다. 레벨 안의 오브젝트들을 조율하려면 전용 스크립트를 가진 게임 오브젝트를 추가하세요. [컬렉션과 월드](#collections-and-worlds)를 참고하세요.

### 계층 전체 삭제하기 {#deleting-a-hierarchy}

Godot의 `queue_free()`는 노드의 자손까지 삭제합니다. Defold의 `go.delete(id)`는 재귀 삭제를 요청하지 않는 한 자식 게임 오브젝트를 남겨 둡니다. 재귀 삭제 예제와 컬렉션 팩토리로 생성한 오브젝트의 정리 방법은 [팩토리](#factories)를 참고하세요.

### 씬을 상속할 수 있다고 가정하기 {#expecting-scene-inheritance}

Defold에는 Godot와 같은 씬 상속 방식이 없으므로 파생 씬의 구조를 같은 방식으로 마음대로 재정의할 수 없습니다. 대신 프로토타입과 컬렉션을 재사용하고 프로퍼티나 스크립트로 인스턴스를 조정할 수 있습니다. [컬렉션과 월드](#collections-and-worlds)를 참고하세요.

### 오브젝트 참조로 다른 스크립트의 함수 호출하기 {#calling-another-script-through-an-object-reference}

Defold 게임 오브젝트의 식별자만으로는 다른 스크립트 인스턴스의 함수에 접근할 수 없습니다. 컴포넌트 사이는 메세지로 통신하고 공용 함수는 Lua 모듈에 두세요. [메세지와 주소 지정](#messages-and-addressing) 및 [오토로드와 공유 상태](#autoloads-and-shared-state)를 참고하세요.

### 인스턴스 상태를 파일 최상위 지역 변수에 저장하기 {#keeping-instance-state-in-a-top-level-local}

스크립트 파일의 최상위 지역 변수는 그 파일을 사용하는 인스턴스들이 공유합니다. 따라서 한 인스턴스에서 값을 바꾸면 다른 인스턴스에도 영향을 줄 수 있습니다. [인스턴스 데이터와 지역 데이터](#instance-data-vs-local-data)에서 설명한 대로 인스턴스별 상태는 `self`에 저장하세요.

### 입력이 자동으로 활성화된다고 가정하기 {#assuming-input-is-enabled-automatically}

Defold 게임 오브젝트의 컴포넌트가 입력을 받으려면 먼저 그 오브젝트가 입력 포커스를 획득해야 합니다. 프록시로 로드한 월드라면 프록시를 가진 오브젝트도 포커스가 필요합니다. 바인딩, 포커스, 인풋 스택의 동작은 [입력](#input)을 참고하세요.

### 키네마틱 오브젝트가 충돌면을 따라 자동으로 미끄러진다고 가정하기 {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold는 키네마틱 충돌 오브젝트의 접촉을 감지하지만, Godot의 `move_and_slide()`에 해당하는 동작을 자동으로 수행하지는 않습니다. 이동과 충돌 반응은 스크립트에서 처리해야 합니다. [물리와 충돌](#physics-and-collisions)을 참고하세요.

### 충돌 마스크를 한쪽에만 설정하기 {#configuring-only-one-collision-mask}

한쪽 오브젝트만 상대방과 상호작용하도록 설정하면 충돌이 감지되지 않습니다. 두 오브젝트 모두 자기 마스크에 상대 오브젝트의 그룹을 포함해야 합니다. [물리와 충돌](#physics-and-collisions)을 참고하세요.

### 2D 좌표를 그대로 복사하기 {#copying-2d-coordinates-unchanged}

Godot와 일반적인 Defold 2D 설정에서는 Y축 방향이 서로 반대입니다. 이동 코드를 그대로 복사하면 오브젝트가 예상과 반대 방향으로 움직일 수 있습니다. 카메라를 사용하는 경우에는 화면 위치와 월드 위치도 다릅니다. [좌표](#coordinates) 및 [카메라와 좌표](#cameras-and-coordinates)를 참고하세요.

### 월드 Z 좌표로 GUI 노드 정렬하기 {#using-world-z-to-sort-gui-nodes}

Defold에서는 GUI 노드의 Z 위치를 바꿔도 그리기 순서가 달라지지 않습니다. [그리기 순서와 레이어](#draw-order-and-layers)에서 설명한 대로 GUI 노드의 순서와 레이어를 사용하세요.

### 핫 리로드로 오브젝트가 다시 시작된다고 가정하기 {#expecting-hot-reload-to-restart-the-object}

스크립트를 핫 리로드해도 `init()`이 다시 실행되지 않으므로 인스턴스 상태에는 이전 값이 남을 수 있습니다. 기존 상태와 모듈 리로드 처리 방법은 [핫 리로드](#hot-reload)를 참고하세요.

### 레벨을 언로드하면 공유 상태가 초기화된다고 가정하기 {#expecting-a-level-unload-to-clear-shared-state}

Godot 오토로드의 상태와 캐시된 Lua 모듈의 상태는 모두 레벨이 바뀌어도 유지될 수 있습니다. 필요할 때 공유 데이터를 직접 초기화하세요. Lua 모듈은 오토로드 노드와 달리 자동으로 콜백을 받지 않습니다. [오토로드와 공유 상태](#autoloads-and-shared-state)를 참고하세요.

## 다음에 살펴볼 자료 {#where-to-go-from-here}

[Defold Learn Hub](https://defold.com/learn/)에는 처음 시작하는 데 필요한 자료부터 더 깊이 배우기 위한 매뉴얼, 예제, 튜토리얼, 동영상, 강좌까지 한곳에 모여 있습니다. 다음 자료부터 살펴보세요.

- [빌딩 블록](/manuals/building-blocks/)
- [주소 지정](/manuals/addressing/)
- [메세지 전달](/manuals/message-passing/)
- [Defold 예제](/examples/)
- [튜토리얼](/tutorials/)
- [API 레퍼런스](/ref/go/)

막히는 부분이 있으면 [Defold 포럼](https://forum.defold.com/)이나 [Discord](https://defold.com/discord/)에서 질문하세요. 작은 예제 프로젝트를 첨부하고 Godot의 어떤 동작을 재현하려는지 설명하면 다른 사람이 도와주기 쉽습니다.
