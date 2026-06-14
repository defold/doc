---
title: Unity 사용자를 위한 Defold
brief: 이 가이드는 Unity 사용 경험이 있는 사용자가 Defold로 빠르게 전환할 수 있도록 도와줍니다. Unity에서 사용하는 핵심 컨셉 일부를 다루고, 이에 대응하는 Defold의 도구와 방식을 설명합니다.
---

# Unity 사용자를 위한 Defold

Unity 사용 경험이 있다면 이 가이드가 Defold에서 빠르게 생산성을 얻는 데 도움이 됩니다. 이 문서는 필수 사항에 집중하며, 더 깊은 세부 내용이 필요한 경우 공식 Defold 매뉴얼을 안내합니다.

## 소개

Defold는 Windows, Linux, macOS용 에디터를 갖춘 완전히 무료이며 진정한 크로스 플랫폼 3D 게임엔진입니다. 전체 소스 코드는 [Github](https://github.com/defold/defold/)에서 확인할 수 있습니다.

Defold는 저사양 디바이스에서도 성능에 집중합니다. 많은 게임플레이 상호작용을 코드와 메세지 전달로 처리하는 작은 컴포넌트 모델을 사용합니다.

Defold는 Unity보다 훨씬 작습니다. 빈 프로젝트의 엔진 크기는 모든 플랫폼에서 1-3 MB 사이입니다. 엔진의 추가 부분을 제거할 수 있으며, 일부 게임 컨텐츠를 [Live Update](/manuals/live-update)로 옮겨 나중에 별도로 다운로드할 수도 있습니다. 크기 비교와 Defold를 선택해야 하는 다른 이유는 [Why Defold 웹페이지](https://defold.com/why/)에 설명되어 있습니다.

필요에 맞게 Defold를 커스터마이즈하려면 직접 작성하거나 기존 항목을 사용할 수 있습니다.

1. 선택 가능한 몇 가지 백엔드(OpenGL, Vulkan 등)를 갖춘 완전히 스크립팅 가능한 렌더링 파이프라인(렌더 스크립트 + 메터리얼/쉐이더).
2. 네이티브 익스텐션(C++/C#)으로 작성한 코드와 컴포넌트.
3. 에디터를 커스터마이즈하기 위한 Editor Scripts와 UI 위젯.
3. 전체 소스 코드와 빌드 파이프라인이 제공되므로, 수정된 엔진과 에디터 빌드.

[Defold for Unity developers](https://www.youtube.com/watch?v=-3CzCbd4QZ0)에 관한 Game From Scratch의 비디오도 확인해 보는 것을 권장합니다.

---

## 설치

1. 사용하는 OS용 Defold를 다운로드합니다.
2. 압축을 풀고 실행합니다.

이게 전부입니다. 허브도, 추가 SDK도, 툴체인이나 플랫폼 번들 설치도 없습니다. 그래서 Defold에는 설정 과정이 없다고 말합니다.

더 자세한 내용이 필요하면 이 짧은 [설치 매뉴얼](/manuals/install/)을 읽어 보세요.

### 버전

Defold는 자주 업데이트되며 “LTS” 트랙은 없습니다. 항상 최신 버전을 사용하는 것을 권장합니다. 새 버전은 정기적으로, 보통 매월 출시되며 약 2주의 공개 베타 기간이 있습니다. Defold는 에디터에서 직접 업데이트할 수 있습니다.

---

## 시작 화면

Defold는 Unity Hub와 비슷한 시작 화면으로 사용자를 맞이하며, 여기에서 최근 프로젝트를 열 수 있습니다.

![Welcome screen comparison](images/unity/unity_defold_start.png)

또는 다음에서 새 프로젝트를 시작할 수 있습니다.
- `Templates` - 특정 플랫폼이나 장르에 맞춰 더 빠르게 설정할 수 있는 기본 빈 프로젝트,
- `Tutorials` - 첫 단계를 도와주는 안내형 학습 과정,
- `Samples` - 공식 또는 커뮤니티 제공 사용 사례와 예제,

![Welcome Templates comparison](images/unity/unity_defold_templates.png)

첫 프로젝트를 만들거나 열면 Defold Editor에서 열립니다.

## Hello World

Defold에서 무언가를 빠르게 만들어 보는 간단한 방법입니다. 단계를 따라 한 뒤 이 매뉴얼의 나머지를 계속 읽어 보세요.

1. `Templates`에서 빈 프로젝트를 선택하고, `Title`에 이름을 입력하고, 위치를 선택한 뒤 `Create New Project`를 클릭해 생성합니다. 프로젝트가 Defold Editor에서 열립니다.
![Hello World Step 1](images/unity/helloworld_1.png)
2. 왼쪽의 `Assets` 창에서 `main` 폴더를 열고 `main.collection`을 더블 클릭해 엽니다.
3. 오른쪽의 `Outline` 창에서 `Collection`을 마우스 오른쪽 버튼으로 클릭하고 `Add Game Object`를 선택합니다.
![Hello World Step 2](images/unity/helloworld_2.png)
4. 생성된 `go` 게임 오브젝트를 마우스 오른쪽 버튼으로 클릭하고 `Add Component`, 그다음 `Label`을 선택합니다.
![Hello World Step 3](images/unity/helloworld_3.png)
5. 아래쪽 왼쪽의 `Properties` 창에서 `Text` 프로퍼티에 텍스트를 입력합니다.
6. 중앙의 메인 씬 뷰에서 라벨을 드래그하고 이동해 `(480,320,0)` 근처에 놓거나, `Properties`의 `Position`에서 변경합니다.
![Hello World Step 4](images/unity/helloworld_4.png)
7. 라벨 위치를 변경한 뒤 `File` -> `Save All`을 클릭하거나 단축키 <kbd>Ctrl</kbd>+<kbd>S</kbd>(Mac에서는 <kbd>Cmd</kbd>+<kbd>S</kbd>)로 프로젝트를 저장합니다.
8. `Project` -> `Build`를 클릭하거나 단축키 <kbd>Ctrl</kbd>+<kbd>B</kbd>(Mac에서는 <kbd>Cmd</kbd>+<kbd>B</kbd>)로 프로젝트를 빌드합니다.
![Hello World Step 5](images/unity/helloworld_5.png)

이제 Defold에서 첫 프로젝트를 빌드했으며, 창에서 입력한 텍스트를 볼 수 있을 것입니다. 게임 오브젝트와 컴포넌트 개념은 익숙할 것입니다. 컬렉션, Outline, Properties, 그리고 왜 라벨을 오른쪽 위 방향으로 조금 이동해야 했는지는 아래에서 설명합니다.

---

## Defold 에디터 개요

여기서는 Unity 사용자가 처음에 알고 싶어 할 만한 관점에서 Defold Editor를 소개하지만, 이후 전체 [에디터 개요 매뉴얼](/manuals/editor)도 확인해 보는 것을 권장합니다.

### 에디터 비교

Unity와 Defold 사이에서 처음 눈에 띄는 차이는 기본 에디터 레이아웃입니다. 여기서는 Defold의 기본 레이아웃에 맞추기 위해 약간 수정한 레이아웃의 Unity Editor를 보여 줍니다. 주요 창을 시각적으로 더 쉽게 비교할 수 있도록 나란히 배치했으며, 익숙한 Unity 탭을 더 쉽게 알아볼 수 있을 것입니다.

![Editor Comparison](images/unity/defold_unity_editor.png)

기본적으로 Defold Editor는 2D 직교 투영(orthographic projection) 미리보기로 열립니다. 3D 프로젝트에서 작업하거나 Unity에 더 가까운 경험을 원한다면, 툴바에서 `2D` 토글을 해제해 2D에서 3D로 전환하고 `Perspective` 토글을 체크해 카메라 투영을 원근 투영으로 변경하는 것을 권장합니다.

![Defold Toolbar](images/unity/defold_2d.png)

툴바의 `Grid Settings`를 조정해 Unity처럼 `Y` 평면을 사용할 수도 있습니다.

![Defold 3D settings](images/unity/defold_3d.png)

### Defold 창 개요

Defold Editor는 6개의 주요 창으로 나뉩니다.

![Editor 2](images/editor/editor_overview.png)

아래는 Defold 명칭과 기능 차이의 비교입니다.

| Defold | Unity | 차이점 |
|---|---|---|
| 1. Assets | Project (Assets Browser) | Defold에서 Assets 창은 왼쪽에 도킹되어 있습니다. Defold는 `meta` 파일을 만들지 않습니다. |
| 2. Main Editor | Scene View | Defold Editor는 컨텍스트에 민감합니다(파일 타입마다 다른 에디터). 반면 Unity는 별도의 특수 창(예: Animator, Shader Graph)을 사용합니다. Defold에는 내장 코드 에디터도 있습니다. |
| 3. Outline | Hierarchy | Defold는 전역 계층구조가 아니라 현재 열린 파일 또는 선택된 요소(게임 오브젝트나 컴포넌트)만 반영합니다. |
| 4. Properties | Inspector | Defold는 게임 오브젝트의 모든 컴포넌트가 아니라 Outline의 **현재 선택 항목**에 대한 프로퍼티만 표시합니다. |
| 5. Tools | Console | Defold는 Console, Curve Editor, Build Errors, Search Results, Breakpoints, Debugger 같은 탭에서 도구를 제공합니다. |
| 6. Changed Files | Unity Version Control (Plastic) | Defold에서는 Git이 프로젝트에 통합되면 변경된 파일이 여기에 표시됩니다. 외부에서 Git을 계속 사용할 수도 있습니다. |

그 밖의 유용한 에디터 관련 명칭입니다.

| Defold | Unity | 차이점 |
|---|---|---|
| Game Build | Game Preview | 엔진으로 빌드해 실행 중인 게임을 보여 줍니다. Defold는 Unity 6+ Multiplayer Play Mode와 비슷하게 에디터에서 게임 인스턴스를 여러 개 실행할 수 있습니다. Defold에서 게임은 도킹되지 않고 항상 별도 창에서 실행됩니다. Defold는 Unity Remote와 비슷하게 외부 디바이스(예: 휴대폰)에서도 게임을 실행할 수 있습니다. |
| Tabs | Tabs | Defold는 Main Editor 뷰 안의 두 창에서 나란히 편집할 수 있습니다. 탭과 창은 단일 Editor 창 안에 도킹됩니다. 창 표시 여부는 토글할 수 있고(<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>), 창 크기도 조정할 수 있습니다. |
| Toolbar | Toolbar / Scene View Options | 최신 Unity 버전에서만 Transform 도구가 Defold와 비슷하게 Scene 뷰 안으로 이동했습니다. |
| Console | Console | Defold Console은 분리할 수 없습니다. Defold의 빌드 에러는 별도의 `Build Errors` 탭에 표시됩니다. |
| Build Errors | Compilation Errors in Console | Lua 스크립트는 인터프리트되므로 컴파일 에러가 없습니다. 하지만 프로젝트는 빌드되며, 빌드 중 일부 에러가 나타날 수 있습니다. Defold는 스크립트 정적 분석을 위해 Lua Language Server도 사용합니다. |
| Search Results | Search / Project Search | Defold에는 타입과 라벨별 필터링이 없습니다. |
| Curve Editor | Unity Curve Editor | Defold Curve Editor는 파티클 효과 프로퍼티의 곡선만 편집할 수 있습니다. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Debugger는 Defold에 기본으로 완전히 통합되어 있습니다. 중단점을 추적, 활성화, 비활성화하는 추가 탭도 있습니다. |

---

## 핵심 개념

충분히 일반화하면 대부분의 게임엔진 뒤에 있는 핵심 개념은 매우 비슷합니다. 이런 개념은 복잡하고 플랫폼 관련 작업을 엔진이 처리하는 동안 개발자가 블록을 조립하듯 더 쉽게 게임을 만들 수 있도록 돕기 위한 것입니다.

### 빌딩 블록

Defold는 몇 가지 기본 빌딩 블록만으로 동작합니다.

![Building blocks](images/unity/blocks.png)

자세한 내용은 [Defold 빌딩 블록](/manuals/building-blocks/)에 관한 전체 매뉴얼을 확인하세요.

### 게임 오브젝트
Defold는 Unity와 비슷하게 **"게임 오브젝트(Game Objects)"**를 사용합니다. 두 엔진 모두 게임 오브젝트는 ID를 가진 데이터 컨테이너이며, 위치, 회전, 스케일이라는 변형(transform)을 모두 가집니다. 하지만 Defold에서는 변형이 별도 컴포넌트가 아니라 내장되어 있습니다.

게임 오브젝트 사이에 부모-자식 관계를 만들 수 있습니다. Defold에서는 이 작업을 "컬렉션(Collection)" 안의 에디터에서만 수행하거나(아래 설명), 스크립트에서 동적으로 수행할 수 있습니다. Unity에서처럼 게임 오브젝트가 다른 게임 오브젝트를 중첩 오브젝트로 포함할 수는 없습니다.

### 컴포넌트
두 엔진 모두 게임 오브젝트를 **"컴포넌트(Components)"**로 확장할 수 있습니다. Defold는 필수 컴포넌트의 최소 집합을 제공합니다. Unity보다 2D와 3D의 구분이 적으므로(예: colliders), 전체 컴포넌트 수가 더 적고 Unity에서 쓰던 일부 컴포넌트가 없다고 느낄 수 있습니다.

#### 동작 컴포넌트

Unity에서 "component"는 보통 `GameObject`에 붙는 `MonoBehaviour`를 의미합니다. `MonoBehaviour`를 상속해 직접 만들 수도 있고, Light나 일부 물리 관련 기능 같은 내장 컴포넌트를 사용할 수도 있습니다.

Defold에서 Component는 Unity의 내장 컴포넌트에 해당하는 것만을 가리킵니다. Defold는 스크립트를 MonoBehaviour처럼 다루지 않으며, gameobject에 붙이기 위해 리스너 이벤트/콜백을 만드는 것 외에 명시적인 "표시"도 요구하지 않습니다.

커스텀 게임플레이 동작은 보통 같은 게임 오브젝트에 많은 개별 스크립트 컴포넌트로 추가하지 않습니다. 대신 Lua 모듈로 구현하고 하나의 호스트 `.script`에서 사용하거나, 여러 오브젝트를 제어하는 더 큰 시스템 스크립트에서 처리하는 경우가 일반적입니다. 아래의 코드 작성 섹션에서 더 자세히 다룹니다.

[Defold 컴포넌트는 여기](/manuals/components/)에서 더 읽어 보세요.

아래 표는 빠른 조회를 위해 유사한 Unity 컴포넌트를 보여 주며, 각 Defold 컴포넌트 매뉴얼 링크를 포함합니다.

| Defold | Unity | 차이점 |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | Defold에서는 코드로만 tint(color 프로퍼티)를 변경할 수 있습니다. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold에는 정사각형 그리드를 지원하는 내장 Tilemap Editor가 있지만(예: [Hexagon](https://github.com/selimanac/defold-hexagon/)용 익스텐션은 있음), 내장 autotiling 규칙은 없습니다. [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/), [Sprite Fusion](https://defold.com/assets/spritefusion/) 같은 도구는 Defold로 익스포트하는 옵션을 제공합니다. |
| [Label](/manuals/label/) | Text / TextMeshPro | Defold에는 풍부한 포멧을 위한 [RichText extension](https://defold.com/assets/richtext/)이 있습니다(TextMeshPro와 유사). |
| [Sound](/manuals/sound/) | AudioSource | Defold에는 전역 사운드 소스만 있으며 공간 사운드는 없습니다. Defold용 공식 [FMOD extension](https://github.com/defold/extension-fmod)이 있습니다. |
| [Factory](/manuals/factory/) | Prefab Instantiate() | Defold에서 Factory는 특정 프로토타입(prefab)을 가진 컴포넌트입니다. |
| [Collection Factory](/manuals/collection-factory/) | - (No direct component equivalent) | Defold의 Collection Factory 컴포넌트는 부모-자식 관계를 가진 여러 게임 오브젝트를 한 번에 스폰할 수 있습니다. |
| [Collision Object](/manuals/physics-objects) | Rigidbody + Collider | Defold에서는 물리 오브젝트와 충돌 모형이 하나의 컴포넌트로 결합되어 있습니다. |
| [Collision Shapes](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | Defold에서는 모형(box, sphere, capsule)을 Collision Object 컴포넌트 안에서 설정합니다. 두 엔진 모두 tilemaps와 convex hull 데이터의 충돌 모형을 지원합니다. |
| [Camera](/manuals/camera/) | Camera | Unity의 카메라는 렌더링과 포스트 프로세싱 설정이 더 많이 내장되어 있지만, Defold는 사용자가 렌더 스크립트를 통해 커스텀 제어하도록 이를 위임합니다. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defold GUI는 완전한 UI와 템플릿을 만들기 위한 강력한 컴포넌트입니다. Unity에는 이에 해당하는 단일 UI 컴포넌트가 없고 여러 UI 프레임워크가 있습니다. Defold에는 [Extension](https://github.com/britzl/extension-imgui)을 위한 익스텐션도 있습니다. |
| [GUI Script](/manuals/gui-script/) | Unity UI / uGUI scripts | Defold GUI는 전용 `gui` API를 사용하는 GUI 스크립트로 제어할 수 있습니다. |
| [Model](/manuals/model/) | MeshRenderer + Material | Defold에서 Model 컴포넌트는 3D 모델 파일, 텍스쳐, 쉐이더가 있는 메터리얼을 묶습니다. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | Defold에서 Mesh는 코드로 버텍스 집합을 관리하기 위한 컴포넌트입니다. Defold Model과 비슷하지만 훨씬 더 낮은 수준입니다. |
| [ParticleFX](/manuals/particlefx/) | Particle System | Defold의 파티클 에디터는 다양한 프로퍼티를 가진 2D/3D 파티클 효과를 지원하며, Curve Editor의 곡선을 사용해 시간에 따라 애니메이션할 수 있습니다. Trails나 Collisions는 없습니다. |
| [Script](/manuals/script/) | Script | 프로그래밍 차이에 대한 자세한 내용은 아래에서 설명합니다. |

#### 익스텐션과 커스텀 컴포넌트

Defold에는 익스텐션으로 사용할 수 있는 공식 [Spine](/extension-spine/) 및 [Rive](/extension-rive/) 컴포넌트도 있습니다.

네이티브 익스텐션을 사용해 직접 [커스텀 Components](https://github.com/defold/extension-simpledata)를 만들 수도 있습니다. 예를 들어 커뮤니티에서 만든 [Object Interpolation Component](https://github.com/indiesoftby/defold-object-interpolation)가 있습니다.

일부 Unity 컴포넌트는 Defold에 기본 제공되는 대응 항목이 없습니다. 예를 들면 Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth, Animator가 있습니다. 하지만 이런 기능은 모두 스크립트로 구현할 수 있으며, 서로 다른 lighting pipeline, 임의의 mesh(terrain 포함)를 생성하는 Mesh 컴포넌트, 커스터마이즈 가능한 trail 효과를 위한 [Hyper Trails](https://defold.com/assets/hypertrails/) 같은 솔루션이 이미 있습니다. Defold도 나중에 lights 같은 새 내장 컴포넌트를 추가할 수 있습니다.

### 리소스

일부 컴포넌트에는 Unity와 비슷하게 **"리소스(Resources)"**가 필요합니다. 예를 들어 스프라이트와 모델에는 텍스쳐가 필요합니다. 그중 몇 가지를 아래 표에서 비교합니다.

| Defold | Unity | 차이점 |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold에는 [Texture Packer용 익스텐션](https://defold.com/extension-texturepacker/)도 있습니다. |
| [Tile source](/manuals/tilesource/) | Tile Palette + Asset | Defold에서 tile source는 tilemaps의 텍스쳐로 사용할 수 있을 뿐 아니라 스프라이트나 파티클에도 사용할 수 있습니다. |
| [Font](/manuals/font/) | Font | Unity의 Text/TextMeshPro와 비슷하게 Defold Label 컴포넌트나 GUI의 텍스트 노드에서 사용됩니다. |
| [Material](/manuals/material/) | Material | Defold에서 쉐이더는 vertex program과 fragment program으로 명명됩니다. |

### 컬렉션과 Scene

Defold에서는 Unity prefabs처럼 게임 오브젝트와 컴포넌트를 별도 파일에 둘 수도 있고, 이를 조합하는 **"컬렉션(Collection)"** 파일 안에 정의할 수도 있습니다.

Defold의 컬렉션은 기본적으로 정적 씬 설명을 담은 텍스트 파일입니다. 컬렉션은 런타임 오브젝트가 **아닙니다**. 게임에서 어떤 게임 오브젝트를 인스턴스화해야 하는지, 그리고 그 오브젝트들 사이의 부모-자식 관계를 어떻게 설정해야 하는지만 정의합니다.

#### 게임 월드

Unity scenes는 기본적으로 같은 전역 게임 상태와 물리 시뮬레이션, 사실상 같은 *월드*(*게임 월드*)를 공유합니다. Defold에는 두 가지 옵션이 있습니다.
1. `Factory`를 통해 단일 게임 오브젝트 파일에서, 또는 `Collection Factory`를 통해 컬렉션 파일에서 게임 오브젝트를 이미 인스턴스화된 특정 *월드*에 prefabs처럼 인스턴스화합니다.
2. 부트스트랩에서 로드한 컬렉션이나 `Collection Proxy` 컴포넌트를 통해 런타임에 별도 게임 *월드*를 만들고, 그 월드가 자체 게임 오브젝트, 물리 월드, 엔진 동작, 주소 지정 네임스페이스를 갖도록 합니다.

Factories와 Proxy 컴포넌트도 아래에서 설명합니다.
[Building Blocks 매뉴얼](/manuals/building-blocks/#collections)에서 컬렉션에 대해 더 읽어 보세요.

---

## 프로젝트 리소스와 에셋

Unity와 Defold는 둘 다 게임 컨텐츠를 프로젝트 디렉토리에 저장하지만, 에셋을 추적하고 준비하는 방식이 다릅니다.

### 에셋

Unity는 에셋을 `Assets/`에 보관하고 `.meta` 파일을 생성합니다. Defold에는 meta 파일이 없습니다. Defold의 프로젝트는 디스크에 있는 것과 정확히 같은 폴더 구조일 뿐이며, `Assets` 창은 항상 이를 그대로 반영합니다.

### 리소스 포멧

Unity는 뒤에서 에셋을 임포트하고 다른 포멧으로 변환합니다. Defold에서는 소스 리소스(`.png`, `.gltf`, `.wav`, `.ogg` 등)를 직접 다루고 이를 `Components`에 할당합니다.

Unity는 단일 이미지를 Sprite로 사용할 수 있습니다. Defold에서는 이미지를 Models/Meshes에 직접 사용할 수 있지만, Sprites/GUI/Tilemaps/Particles에는 atlas(패킹된 텍스쳐)나 tilesource(그리드 기반 타일)가 필요합니다.

대부분의 Defold 리소스는 텍스트로 저장되므로 버전 관리에 적합합니다.

### Library 캐쉬

Unity는 임포트한 에셋을 위해 `Library/` 폴더를 생성합니다. Defold에는 그런 디렉토리가 없습니다. 에셋은 빌드 중 처리되며, 캐쉬된 출력은 빌드 폴더 아래에 저장됩니다(선택적으로 로컬/원격 빌드 캐쉬 사용 가능).

---

## 코드 작성

Defold에서 `MonoBehaviour` 스크립트에 해당하는 것은 Script 컴포넌트이지만, 알아둘 만한 차이가 몇 가지 있습니다.

### Lua

Defold 스크립트는 동적 타입의 멀티 패러다임 [Lua](https://www.lua.org/) 언어로 작성됩니다.

Lua 스크립트에는 몇 가지 타입이 있습니다. `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script`, 그리고 `*.lua` 모듈입니다.

### Teal

Defold는 정적 타입 Lua 방언인 [Teal](https://teal-language.org/)처럼 Lua 코드를 출력하는 트랜스파일러 사용을 지원하지만, 이 기능은 더 제한적이며 추가 설정이 필요합니다. 자세한 내용은 [Teal Extension Repository](https://github.com/defold/extension-teal)에서 확인할 수 있습니다.

### C++/C# 네이티브 익스텐션

Defold 네이티브 익스텐션은 타겟 플랫폼에 따라 C, C++, C#, Objective-C, Java 또는 JS 같은 여러 다른 언어로 작성할 수 있습니다. C#에 매우 익숙하다면 대부분의 게임 로직을 C# 익스텐션으로 구성하고 작은 Lua 부트스트랩 스크립트에서 호출하는 것도 기술적으로는 가능합니다. 다만 이는 고급 API 지식이 필요하므로 초보자에게는 권장하지 않습니다.

[Defold 네이티브 익스텐션 매뉴얼](/manuals/extensions/)에서 익스텐션에 대해 더 읽어 보세요.


### MonoBehaviours에서 Lua 모듈로

Unity는 열린 스크립팅 모델을 가지고 있습니다. `MonoBehaviour`가 에디터에서 동작을 추가하는 기본 방식이므로, 많은 Unity 프로젝트는 중요한 GameObject마다 `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager` 같은 컨트롤러 스타일 스크립트 하나로 시작합니다.

Defold는 기본 아키텍처가 더 구체적입니다. 게임 오브젝트에 `.script`가 있을 수는 있지만, Defold의 강력한 주소 지정과 메세지 전달 덕분에 하나의 스크립트가 자체 스크립트가 전혀 없는 수백 또는 수천 개의 다른 오브젝트와 그 컴포넌트를 제어할 수 있으므로, 모든 게임 오브젝트마다 스크립트를 만들 필요는 거의 없습니다. 각 게임 오브젝트에 맞춰 스크립트를 만드는 일은 거의 필요하지 않으며, 오히려 비생산적인 복잡성을 만들 수 있습니다.

재사용 가능한 게임플레이 동작을 위해 Unity 개발자는 보통 composition으로 이동합니다. 같은 GameObject에 `Health.cs`, `Attack.cs`, `EnemyFinder.cs` 같은 더 작은 `MonoBehaviour` 스크립트를 붙이는 방식입니다. Defold에서는 일반적으로 붙어 있는 `.script` 하나를 호스트나 코디네이터로 유지하고, 재사용 가능한 로직은 일반 Lua 모듈에 둡니다.

Unity에서 이 composition은 다음과 비슷할 수 있습니다.

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

Defold에서는 같은 책임이 붙어 있는 스크립트 하나와 재사용 가능한 모듈 사이에 나뉘는 경우가 많습니다.

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

붙어 있는 `.script`는 호스트 또는 코디네이터가 됩니다. Lua 모듈에는 Unity에서 작은 `MonoBehaviour` 스크립트가 하나의 책임을 담는 방식과 비슷하게 재사용 가능한 로직이 들어갑니다.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

중요한 차이는 Defold가 모듈식 아키텍처를 막는다는 것이 아니라, composition이 어디에서 일어나고 게임플레이 코드가 어떻게 통신하는가입니다.

| Unity | Defold |
|---|---|
| Inspector에서 여러 `MonoBehaviour` 스크립트를 붙입니다 | `.script` 하나를 붙이고 코드에서 Lua 모듈을 조합합니다 |
| `GetComponent<T>()` 또는 직렬화된 필드를 사용해 동작을 연결합니다 | 모듈 인스턴스를 `self`에 저장하고 오브젝트 간 주소/메세지를 사용합니다 |
| 각 컴포넌트가 자체 라이프사이클 메서드를 가질 수 있습니다 | 호스트 스크립트가 `init()`, `update()`, `on_message()`, `final()` 등을 라우팅합니다 |
| 다양한 아키텍처 스타일이 가능합니다 | 메세지 중심의 명시적 코드 composition이 일반적인 방식입니다 |

특히 Inspector에서 컴포넌트를 추가해 동작을 설정하는 데 익숙하다면 처음에는 낯설게 느껴질 수 있습니다. Defold에서는 Unity에서 시각적으로 설정하던 많은 것을 코드로 생성, 연결, 활성화, 비활성화 또는 업데이트할 수 있습니다. Defold의 메세징 시스템은 로직을 분리하는 데 도움이 됩니다. 발신자는 주소로 데이터를 게시하고, 수신자는 그 데이터로 무엇을 할지 결정합니다.

이 접근 방식은 권장되지만 강제되지는 않으므로, 게임 오브젝트 하나에 여러 스크립트를 붙이거나 객체 지향 프로그래밍 스타일에 더 가깝게 작성하는 것까지 원하는 방식으로 스크립트를 작성할 수 있습니다. 이를 돕는 라이브러리도 있습니다([defold-oop](https://github.com/xiyoo0812/defold-oop) 또는 [lua-class](https://github.com/d954mas/lua-class)).

탄환, 적, 파티클, 타일, 단순 상호작용 요소처럼 같은 타입의 오브젝트가 많을 때는 각 오브젝트에 별도 스크립트를 주는 것보다 시스템 또는 매니저 스크립트에서 제어하는 편이 더 나은 경우가 많습니다. 오브젝트가 자체적으로 의미 있는 상태와 동작을 가질 때는 오브젝트별 스크립트를 사용하세요. 재사용 가능한 로직이 필요하면 모듈을 사용하세요. 하나의 스크립트가 많은 오브젝트를 효율적으로 제어할 수 있으면 시스템 스크립트를 사용하세요.

Defold 스크립트 프로퍼티, 팩토리, 주소 지정, 메세징을 활용해 여러 유닛을 제어하는 방법을 보여 주는 예제는 [여기](https://defold.com/examples/factory/spawn_manager/)에서 볼 수 있습니다.

코드 작성에 좋은 매뉴얼:
- [Script manual](/manuals/script/)
- [Writing code](/manuals/writing-code/)
- [Debugging](/manuals/debugging/)


### 내장 코드 에디터

Defold Editor에는 코드 완성, 구문 강조, 빠른 문서 조회, linting, 내장 debugger를 갖춘 내장 코드 에디터가 포함되어 있습니다.

![Defold Code Editor](/images/editor/code-editor.png)

### VS Code와 다른 에디터

원한다면 외부 에디터를 계속 사용할 수 있습니다. 모든 Defold 컴포넌트와 관련 파일은 텍스트 기반이므로 어떤 텍스트 에디터로도 편집할 수 있지만, Protobuf 기반이므로 올바른 포멧과 요소 구조를 따라야 합니다.

VS Code에 익숙하고 게임 코드를 작성하는 데 사용하고 싶다면 Visual Studio Marketplace에서 [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) 또는 [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide)를 설치하는 것을 권장합니다.

Defold Editor preferences에서 텍스트 파일을 기본적으로 VS Code(또는 다른 외부 에디터)로 열도록 설정할 수도 있습니다. 자세한 내용은 [Editor Preferences](/manuals/editor-preferences/)를 참고하세요.

### Shaders - GLSL

Defold는 Unity와 비슷하게 쉐이더, 즉 `Vertex Programs`와 `Fragment Programs`에 GLSL(OpenGL Shading Language)을 사용합니다. Defold는 Unity의 Shader Graph 같은 도구를 제공하지 않지만(단점일 수 있음), 코드를 작성해 동등한 쉐이더를 만들 수 있습니다.

[Shaders manual](/manuals/shader)에서 쉐이더에 대해 더 읽어 보세요.

#### 메터리얼

Defold는 `.fp`와 `.vp` 쉐이더, 샘플러(텍스쳐), Vertex Attributes나 Constants 같은 다른 항목을 연결하는 `Material` 개념을 사용합니다.

[Materials manual](/manuals/material)에서 메터리얼에 대해 더 읽어 보세요.

---

## 메세징 시스템

Defold에서 오브젝트는 서로에 대한 직접 참조를 보유하지 않습니다. `GetComponent`도, 스크립트 사이의 오브젝트 간 메서드 호출도, Unity와 같은 전역 scene 액세스도 없습니다.

대신 스크립트는 메세지 전달을 통해 통신합니다. 메서드를 호출하거나 컴포넌트에 직접 액세스하는 대신 다른 스크립트에 메세지를 보냅니다. 그 오브젝트가 메세지로 무엇을 할지는 해당 오브젝트에 달려 있습니다.

처음에는 낯설 수 있지만, 이 방식은 느슨한 결합을 촉진하고 강한 상호 의존성을 줄입니다.


### 메세지 보내기

Unity에서 통신은 보통 다음과 같습니다.

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

따라서 오브젝트가 서로를 직접 참조하고 다른 스크립트의 메서드를 호출할 수 있습니다. 모든 것은 하나의 공유 scene 공간에 존재합니다.

Defold에서는 한 스크립트에서 다른 스크립트(또는 다른 컴포넌트)로 메세지를 보냅니다.

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

그리고 스크립트에서 그 메세지를 처리할 수 있습니다.

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

지금은 `#`와 `hash`를 무시하세요. 나중에 설명합니다. 나머지는 이해하기 쉬울 것입니다. 인스턴스화된 게임 오브젝트의 어떤 컴포넌트에도(같은 스크립트에도) 메세지를 보낼 수 있습니다.

#### 스크립트가 아닌 컴포넌트

때로는 `Sprite`나 `Collision` 컴포넌트 등에 메세지를 보내 활성화하거나 비활성화합니다. 때로는 충돌이 발생했을 때처럼 `Components`가 스크립트로 메세지를 보내며, 그러면 이를 처리할 수 있습니다. Defold는 엔진 이벤트와 게임플레이 통신을 위해 내부적으로 같은 메세징 시스템을 사용합니다.

메세징 시스템은 Unity의 SendMessage나 이벤트 시스템과 어느 정도 비슷하지만, 주소 지정과 규칙은 다릅니다.

[메세지 전달 매뉴얼](/manuals/message-passing/)에서 더 자세한 내용을 읽을 수 있습니다.

### 주소 지정

Defold의 오브젝트와 컴포넌트는 URL이라고 하는 주소로 식별됩니다.

인스턴스화된 모든 오브젝트와 컴포넌트에는 고유한 주소가 있으며, 이를 찾기 위해 씬 그래프를 순회할 필요가 없습니다. 덕분에 주소 지정이 명시적이고 직접적입니다.

Defold의 간단한 URL은 다음과 같을 수 있습니다.
```lua
"/player"
```

이는 *개념적으로* 다음과 비슷합니다.
```c#
GameObject.Find("player")
```

이제 주소에서 왜 `"/"` 또는 `"#"`가 사용되었는지 설명할 차례입니다.

Defold URL([URL](https://en.wikipedia.org/wiki/URL)과 유사)은 세 부분으로 구성됩니다.

```yaml
socket: /path #fragment
```

또는 Defold 명칭으로 더 자세히 설명하면 다음과 같습니다.

```yaml
collection: /gameobject #component
```
위 설명의 공백은 세 부분을 시각적으로 구분하기 위해서만 추가했습니다.

간단히 말하면:
1. `collection:`은 끝의 `:`와 함께 컬렉션 컨텍스트를 식별합니다.
2. `/path`는 앞의 `/`와 함께 게임 오브젝트를 식별합니다.
3. `#fragment`는 앞의 `#`와 함께 해당 오브젝트의 특정 컴포넌트(예: script, sprite, collision component)를 식별합니다.

#### 정적 주소

이 식별자들은 각각 생성될 때 결정되며, 부모-자식 관계를 변경해도 절대 바뀌지 않습니다. 파일의 Property `Id`에서 설정할 수 있고, 런타임에는 인스턴스화할 때 `factory.create` 또는 `collectionfactory.create` 호출에서 얻을 수 있습니다.

#### 상대 주소 지정

항상 전체 URL을 사용할 필요는 없습니다.

같은 컬렉션(같은 *월드*) 안에서 메세지를 보내면 socket 부분을 생략할 수 있습니다.

```yaml
/gameobject #component
```
같은 게임 오브젝트 안의 컴포넌트로 보내는 경우 게임 오브젝트 부분도 생략할 수 있습니다.

```yaml
#component
```

유용한 약칭 두 가지는 다음과 같습니다.
- 이 *Script* 컴포넌트로 보내는 `#`
- 이 *Game Object*의 모든 컴포넌트로 보내는 `.`

상대 주소 지정과 약칭을 사용하면 전체 경로를 지정하지 않고도 서로 다른 컨텍스트와 게임 오브젝트에서 재사용 가능한 URL을 작성할 수 있습니다.

### GUI와 렌더로 메세징

Defold는 GUI 월드와 Game Object 월드를 분리하므로, 게임 오브젝트 `.scripts`에서 `.gui_scripts`로도 메세지를 보낼 수 있습니다.

`@`로 시작하는 식별자를 사용해 특수 시스템 네임스페이스로 메세지를 보낼 수도 있습니다. 예를 들어 렌더 시스템은 `@render`:로 주소를 지정할 수 있으며, 이를 사용해 기본 렌더 스크립트에서 투영을 바꾸는 것 같은 특정 내장 렌더링 기능을 제어할 수 있습니다.

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

더 자세한 내용은 [주소 지정 매뉴얼](/manuals/addressing/)에서 확인할 수 있습니다.

---

## Prefabs와 인스턴스

Unity는 Scene의 어떤 것이든 정적으로 또는 동적으로 인스턴스화할 수 있으며, Defold도 같은 일을 할 수 있습니다. Unity에서는 Prefab을 가져와 `Instantiate(prefab)`을 호출합니다. Defold에는 컨텐츠를 인스턴스화하기 위한 컴포넌트가 3개 있습니다.

- `Factory` - 지정된 프로토타입인 `*.go` 파일(prefab)에서 **단일 게임 오브젝트**를 인스턴스화합니다.
- `Collection Factory` - 지정된 프로토타입인 `*.collection` 파일에서 부모-자식 관계가 있는 **게임 오브젝트 집합**을 인스턴스화합니다.
- `Collection Proxy` - `*.collection` 파일에서 새 *월드*를 **로드**하고 인스턴스화합니다.

### Factory

`Prototype` 프로퍼티가 적절한 게임 오브젝트 파일로 설정된 `Factory` 컴포넌트를 정의해 두면, 스폰은 코드에서 다음을 호출하는 것만큼 간단합니다.

```lua
factory.create("#my_factory")
```

이 호출은 컴포넌트의 주소를 사용하며, 이 경우 식별자 `"#my_factory"`를 사용하는 상대 경로입니다.

새로 생성된 인스턴스의 식별자를 반환하므로, 나중에 사용해야 한다면 변수에 저장해 둘 가치가 있습니다.

```lua
local new_instance_id = factory.create("#my_factory")
```

Defold에서는 오브젝트를 직접 풀링할 필요가 없다는 점을 기억하세요. 엔진 자체가 내부적으로 풀링을 수행합니다.

[Factory 매뉴얼](/manuals/factory/)에서 더 자세한 내용을 확인하세요.

### Collection Factory

`Factory`와 `Collection Factory` 컴포넌트의 차이는 Collection Factory가 한 번에 **여러** 게임 오브젝트를 스폰할 수 있고, `*.collection` 파일에 정의된 부모-자식 관계를 생성 시점에 정의할 수 있다는 점입니다.

Unity에는 이런 구분이 없으며, Defold의 Collection Factory와 맞는 전용 개념도 없습니다. 가장 가까운 비유는 오브젝트 계층구조를 포함하는 nested Prefab입니다.

스폰된 모든 인스턴스의 id가 들어 있는 **테이블**을 반환합니다.

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

[Collection Factory 매뉴얼](/manuals/collection-factory/)에서 더 자세한 내용을 확인하세요.

#### 인스턴스의 커스텀 프로퍼티

`factory.create()` 또는 `collectionfactory.create()`를 호출할 때 위치, 회전, 스케일, 스크립트 프로퍼티 같은 선택적 파라미터도 지정할 수 있으므로, 인스턴스가 정확히 어떻게 어디에 나타나고 어떻게 동작할지 제어할 수 있습니다. 예:

```lua
factory.create("#my_factory", my_position, my_rotation, my_scale, my_properties)
```

#### 동적 로딩

`Factory`와 `Collection Factory` 컴포넌트 모두에서 Prototype을 동적 리소스 로딩 대상으로 표시할 수 있습니다. 그러면 무거운 에셋은 필요할 때만 메모리로 가져오고 더 이상 사용하지 않을 때 언로드됩니다.

[리소스 관리 매뉴얼](/manuals/resource/)에서 더 자세한 내용을 확인하세요.

### Collection Proxy

`Collection Proxy`는 특정 `*.collection` 파일을 참조하지만, 팩토리처럼 오브젝트를 *현재 월드*에 주입하는 대신 **새 게임 월드를 로드하고 인스턴스화**합니다. 이는 Unity에서 전체 scene을 로드하는 것과 어느 정도 비슷하지만, 더 엄격하게 분리됩니다.

Unity에서는 additive scene을 다음처럼 로드할 수 있습니다.

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

Defold에서는 `Collection Proxy` 컴포넌트로 메세지를 보내는 것만으로 새 컬렉션을 로드합니다.

```lua
msg.post("#myproxy", "load")
```

1. 프록시에 `"load"` 메세지(또는 비동기 로딩용 `"async_load"`)를 보내면 엔진은 새 월드를 할당하고, 그 컬렉션의 모든 것을 그곳에 인스턴스화하며, 분리된 상태로 유지합니다.
2. 로드가 끝나면 프록시는 월드가 준비되었음을 나타내는 `"proxy_loaded"` 메세지를 다시 보냅니다.
3. 그런 다음 보통 `"init"`과 `"enable"` 메세지를 보내 새 월드의 오브젝트가 일반 라이프사이클을 시작하도록 합니다.

로드된 월드 사이에서 통신하려면 월드 이름(URL의 첫 번째 부분인 `collection:`)을 포함하는 URL로 명시적 메세징을 사용해야 합니다.

이 분리는 레벨 전환, 미니 게임, 대규모 모듈식 시스템을 구현할 때 큰 장점이 될 수 있습니다. 의도하지 않은 상호작용을 막고, 필요한 경우 업데이트 타이밍을 별도로 제어할 수도 있기 때문입니다(예: 일시정지나 슬로 모션).

Unity에서 여러 scene을 사용하면서 각각이 독립적으로 동작해야 했던 경험이 있다면, `Collection Proxy`를 그 개념을 Defold로 직접 가져오는 방법으로 생각할 수 있습니다.

[Collection Proxy 매뉴얼](/manuals/collection-proxy/)에서 더 자세한 내용을 확인하세요.

---

## 어플리케이션 라이프사이클

Unity의 라이프사이클 이벤트 집합인 `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy`, `OnApplicationQuit`에 익숙할 것입니다.

Defold에도 잘 정의된 어플리케이션 라이프사이클이 있지만, 개념과 용어는 다릅니다. Defold는 초기화, 각 프레임, 마무리 중 엔진이 호출하는 미리 정의된 Lua 콜백 집합을 통해 라이프사이클 단계를 노출합니다.

비교하면 다음과 같습니다.

| Defold | Unity | Comment |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold에는 단일 초기화 진입점이자 콜백인 init()이 있습니다. 각 컴포넌트가 생성될 때 호출됩니다. |
| `on_input` | Input Methods | Defold는 [스크립트에 입력 포커스가 설정되면](/manuals/input/#input-focus) 입력을 받습니다. 업데이트 루프에서 가장 먼저 처리됩니다. |
| `fixed_update()` | `FixedUpdate()` | 고정 타임스텝에서 호출됩니다. Defold에서 활성화하려면 `Use Fixed Timestep`을 설정해야 합니다. [자세히](https://defold.com/manuals/project-settings/#use-fixed-timestep). 1.12.0부터는 `update()` 전에 실행됩니다. |
| `update()` | `Update()` | delta time과 함께 프레임당 한 번 호출됩니다. |
| `late_update()` | `LateUpdate()` | `update()` 뒤, 프레임이 렌더링되기 직전에 호출됩니다. 1.12.0부터 사용할 수 있습니다. |
| `on_message` | Message Receiver | 메세지를 받기 위한 Defold의 핵심 콜백입니다. 큐에 메세지가 있을 때 처리됩니다. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold는 게임 오브젝트가 런타임에 삭제되거나(`go.delete()` 사용), 월드/컬렉션이 언로드될 때, 그리고 어플리케이션 종료 중 남아 있는 모든 오브젝트에 대해 각 컴포넌트의 `final()` 콜백을 호출합니다. |

::: sidenote
여러 컴포넌트가 한 번에 초기화/업데이트/제거될 때 Defold는 컴포넌트 간 실행 순서를 보장하지 않는다는 점을 기억하세요. 분리된 설계를 권장합니다.

### 초기화

Defold의 `init()`은 Unity의 `Awake()`, `Start()`, `OnEnable()` 요소를 하나의 진입점으로 결합한 것이라고 생각하면 됩니다. 이 시점에는 엔진이 이미 모든 것을 설정했으므로 컴포넌트 상태를 안전하게 준비할 수 있습니다.

### 메세지는 언제 처리되나요?

`init()`에서 이미 메세지를 게시할 수 있으므로, 메세지는 초기화 직후에 먼저 디스패치됩니다.

그런 다음 각 내부 처리 루프 뒤에, 큐에 무언가가 있을 때마다 메세지가 처리됩니다. 따라서 예를 들어 업데이트 루프 중에도 `on_message()`가 여러 번 호출될 수 있습니다.

### 업데이트 루프

매 프레임마다 Defold는 입력 처리, 메세지 디스패치, 스크립트와 GUI 업데이트 트리거, 물리와 변형 적용, 마지막 그래픽 렌더링이라는 일련의 작업을 실행합니다.

### 마무리

Defold에서 정리 작업은 항상 월드의 삭제 또는 언로드와 연결되며, 컴포넌트별 종료 훅은 `final()`뿐입니다.

Unity 모델과의 미묘한 차이는 컴포넌트가 비활성화되는 것과 전체 어플리케이션이 종료되는 것 사이에 구분이 없다는 점입니다.

### 렌더링

렌더 스크립트(`*.render_script`)는 렌더링 파이프라인의 일부이며, 자체 `init()`, `update()`, `on_message()` 콜백으로 라이프사이클에도 참여합니다. 하지만 이 콜백은 렌더 thread에서 동작하며 게임 오브젝트와 GUI 스크립트 로직과는 분리되어 있습니다.

자세한 내용은 [어플리케이션 라이프사이클 매뉴얼](/manuals/application-lifecycle/)을 읽어 보세요.

---

## GUI

Defold의 GUI는 User Interfaces, 즉 메뉴, 오버레이, 다이얼로그 및 기타 요소를 위한 별도의 단일 전용 프레임워크이며, Canvas를 사용하는 UI Toolkit 또는 uGUI와 비슷합니다.

GUI는 컴포넌트이며 게임 오브젝트 및 컬렉션과 분리되어 있습니다. 게임 오브젝트 대신 계층구조로 배열된 GUI 노드를 사용하며, GUI 스크립트가 이를 구동합니다.

### GUI 노드

Defold에서 `*.gui` 컴포넌트 파일을 열면 `"GUI nodes"`를 배치하는 canvas가 표시됩니다. 이것이 GUI의 빌딩 블록입니다. 추가할 수 있는 GUI 노드 타입은 다음과 같습니다.

- Box(텍스쳐가 있는 사각형 모양)
- Text(임의의 폰트 사용)
- Pie(텍스쳐가 있는 방사형 채우기 pie-slice 요소)
- ParticleFX
- Template(다른 전체 중첩 `.gui` 파일, GUI prefab과 유사)
- 그리고 Spine extension을 사용할 때는 Spine node.

### GUI 스크립트

GUI 컴포넌트에는 GUI 스크립트를 위한 특수 프로퍼티가 있습니다. 컴포넌트마다 `*.gui_script` 파일 하나를 할당하며, 이를 통해 컴포넌트의 동작을 수정할 수 있습니다. 따라서 일반 스크립트와 매우 비슷하지만, 게임 오브젝트 스크립트용인 `go.*` 네임스페이스를 사용하지 않는다는 점이 다릅니다. 대신 GUI 스크립트(`*.gui_script`) 안에서만 동작하는 특수한 `gui.*` 네임스페이스 API를 사용합니다. Canvas를 사용하는 Unity UI(uGUI)의 별도 Scene처럼 생각할 수 있습니다.

### GUI 렌더링

GUI 요소는 일반적으로 화면 공간에서 게임 카메라와 독립적으로 렌더링되지만, 커스텀 렌더링 파이프라인에서는 이 동작을 변경할 수 있습니다.

자세한 내용은 [GUI 매뉴얼](/manuals/gui/)을 읽어 보세요.

## Sorting Layers는 어디에 있나요?

이는 Unity에서 이전할 때 매우 흔히 겪는 혼동입니다.

GUI 컴포넌트에는 `Layers`가 있으며 이는 Unity의 "Sorting Layers"와 거의 같은 방식으로 동작합니다. 하지만 `Sprites`, `Tilemaps`, `Models` 같은 다른 컴포넌트에는 직접 대응되는 것이 없습니다.

대신 일반적으로 다음을 조합합니다.
- 기본 카메라를 사용할 때는 Z 축, Camera 컴포넌트를 사용할 때는 depth를 통한 세밀한 순서 지정.
- 렌더 스크립트에서 render predicates를 사용해 material tags별로 무엇을 그릴지 선택하는 대략적인 순서 지정.

하지만 Defold에서 tags는 렌더 레벨 메커니즘이므로, Unity Sorting Layers를 많은 tags로 흉내 내면 안 됩니다. 과도하게 사용하면 batching이 깨지고 draw overhead가 증가할 수 있습니다.

---

## 이제 어디로 가면 되나요?

- [Defold examples](/examples)
- [Tutorials](/tutorials)
- [Manuals](/manuals)
- [API References](/ref/go)
- [FAQ](/faq/faq)

질문이 있거나 막히면 [Defold Forum](//forum.defold.com)이나 [Discord](https://defold.com/discord/)에서 도움을 요청하기 좋습니다.
