---
title: Defold의 GUI 씬
brief: 이 매뉴얼은 Defold GUI 에디터, 다양한 GUI 노드 타입, GUI 스크립팅을 설명합니다.
---

# GUI

Defold는 사용자 인터페이스를 구성하고 구현하는 데 맞춰진 커스텀 GUI 에디터와 강력한 스크립팅 기능을 제공합니다.

Defold의 그래픽 사용자 인터페이스는 직접 만들어 게임 오브젝트에 첨부한 뒤 컬렉션에 배치하는 컴포넌트입니다. 이 컴포넌트에는 다음과 같은 프로퍼티가 있습니다.

* 사용자 인터페이스를 해상도와 종횡비에 독립적으로 렌더링할 수 있게 해 주는 단순하지만 강력한 레이아웃 기능이 있습니다.
* *GUI 스크립트*를 통해 로직 동작을 붙일 수 있습니다.
* 기본적으로 카메라 뷰와 독립적으로 다른 컨텐츠 위에 렌더링되므로, 움직이는 카메라를 사용하더라도 GUI 요소는 화면에 고정된 상태로 유지됩니다. 렌더링 동작은 변경할 수 있습니다.

GUI 컴포넌트는 게임 뷰와 독립적으로 렌더링됩니다. 따라서 컬렉션 에디터의 특정 위치에 배치되지 않으며, 컬렉션 에디터 안에서 시각적 표현도 가지지 않습니다. 하지만 GUI 컴포넌트는 컬렉션 안에 위치가 있는 게임 오브젝트에 포함되어야 합니다. 그 위치를 변경해도 GUI에는 영향을 주지 않습니다.

## GUI 컴포넌트 만들기

GUI 컴포넌트는 GUI 씬 프로토타입 파일(다른 엔진에서 "prefabs" 또는 "blueprints"라고도 부르는 것)에서 생성됩니다. 새 GUI 컴포넌트를 만들려면 *Assets* 브라우저의 한 위치에서 <kbd>right click</kbd>하고 <kbd>New ▸ Gui</kbd>를 선택합니다. 새 GUI 파일의 이름을 입력하고 <kbd>Ok</kbd>를 누릅니다.

![New gui file](images/gui/new_gui_file.png)

이제 Defold가 파일을 GUI 씬 에디터에서 자동으로 엽니다.

![New gui](images/gui/new_gui.png)

*Outline*에는 GUI의 모든 컨텐츠, 즉 노드 목록과 모든 종속성(아래 참고)이 표시됩니다.

중앙 편집 영역에는 GUI가 표시됩니다. 편집 영역 오른쪽 위의 툴바에는 *Move*, *Rotate*, *Scale* 도구와 [레이아웃](/manuals/gui-layouts) 선택기가 있습니다.

![toolbar](images/gui/toolbar.png)

흰색 사각형은 현재 선택한 레이아웃의 경계를 보여 주며, 프로젝트 설정에 지정된 기본 디스플레이 너비와 높이를 기준으로 합니다.

## GUI 프로퍼티

*Outline*에서 루트 "Gui" 노드를 선택하면 GUI 컴포넌트의 *Properties*가 표시됩니다.

*Script*
: 이 GUI 컴포넌트에 바인딩된 GUI 스크립트입니다.

*Material*
: 이 GUI를 렌더링할 때 사용하는 메터리얼입니다. *Outline* 패널에서 Gui에 여러 메터리얼을 추가하고 개별 노드에 할당할 수도 있습니다.

*Adjust Reference*
: 각 노드의 *Adjust Mode*를 계산하는 방식을 제어합니다.

  - `Per Node`는 각 노드를 부모 노드의 조정된 크기 또는 크기가 변경된 화면에 맞춰 조정합니다.
  - `Disable`은 노드 조정 모드를 끕니다. 그러면 모든 노드가 설정된 크기를 유지합니다.

*Current Nodes*
: 이 GUI에서 현재 사용 중인 노드 수입니다.

*Max Nodes*
: 이 GUI의 최대 노드 수입니다.

*Max Dynamic Textures*
: [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip)를 사용해 만들 수 있는 최대 텍스쳐 수입니다.


## 런타임 조작

스크립트 컴포넌트에서 `go.get()`과 `go.set()`을 사용해 런타임에 GUI 프로퍼티를 조작할 수 있습니다.

Fonts
: GUI에서 사용하는 폰트를 가져오거나 설정합니다.

![get_set_font](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- id가 'default'인 폰트에 현재 할당된 폰트 파일을 가져옵니다
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- 리소스 프로퍼티 'mybigfont'에 할당된 폰트 파일을 id가 'default'인 폰트로 설정합니다
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- id가 'default'인 폰트에 새로 할당된 폰트 파일을 가져옵니다
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materials
: GUI에서 사용하는 메터리얼을 가져오거나 설정합니다.

![get_set_material](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- id가 'effect'인 메터리얼에 현재 할당된 메터리얼 파일을 가져옵니다
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- 리소스 프로퍼티 'myeffect'에 할당된 메터리얼 파일을 id가 'effect'인 메터리얼로 설정합니다
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- id가 'effect'인 메터리얼에 새로 할당된 메터리얼 파일을 가져옵니다
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Textures
: GUI에서 사용하는 텍스쳐(아틀라스)를 가져오거나 설정합니다.

![get_set_texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- id가 'theme'인 텍스쳐에 현재 할당된 텍스쳐 파일을 가져옵니다
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- 리소스 프로퍼티 'mytheme'에 할당된 텍스쳐 파일을 id가 'theme'인 텍스쳐로 설정합니다
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- id가 'theme'인 텍스쳐에 새로 할당된 텍스쳐 파일을 가져옵니다
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## 종속성

Defold 게임의 리소스 트리는 정적이므로, GUI 노드에 필요한 모든 종속성은 컴포넌트에 추가해야 합니다. *Outline*은 모든 종속성을 타입별로 "folders" 아래에 그룹화합니다.

![dependencies](images/gui/dependencies.png)

새 종속성을 추가하려면 *Asset* pane에서 에디터 뷰로 끌어다 놓습니다.

또는 *Outline*에서 "Gui" 루트를 <kbd>right click</kbd>한 다음 팝업 컨텍스트 메뉴에서 <kbd>Add ▸ [type]</kbd>을 선택합니다.

추가하려는 타입의 폴더 아이콘을 <kbd>right click</kbd>하고 <kbd>Add ▸ [type]</kbd>을 선택할 수도 있습니다.

## 노드 타입 {#node-types}

GUI 컴포넌트는 노드 집합으로 구성됩니다. 노드는 단순한 요소입니다. 에디터에서 또는 런타임에 스크립팅을 통해 노드를 변형(이동, 스케일, 회전)하고 부모-자식 계층구조로 정렬할 수 있습니다. 사용할 수 있는 노드 타입은 다음과 같습니다.

Box node
: ![box node](images/icons/gui-box-node.png){.left}
  단일 색상, 텍스쳐 또는 플립북 애니메이션을 가진 사각형 노드입니다. 자세한 내용은 [Box node 문서](/manuals/gui-box)를 참고하세요.

<div style="clear: both;"></div>

Text node
: ![text node](images/icons/gui-text-node.png){.left}
  텍스트를 표시합니다. 자세한 내용은 [Text node 문서](/manuals/gui-text)를 참고하세요.

<div style="clear: both;"></div>

Pie node
: ![pie node](images/icons/gui-pie-node.png){.left}
  일부만 채우거나 반전할 수 있는 원형 또는 타원형 노드입니다. 자세한 내용은 [Pie node 문서](/manuals/gui-pie)를 참고하세요.

<div style="clear: both;"></div>

Template node
: ![template node](images/icons/gui.png){.left}
  템플릿은 다른 GUI 씬 파일을 기반으로 인스턴스를 만드는 데 사용됩니다. 자세한 내용은 [Template node 문서](/manuals/gui-template)를 참고하세요.

<div style="clear: both;"></div>

ParticleFX node
: ![particlefx node](images/icons/particlefx.png){.left}
  파티클 효과를 재생합니다. 자세한 내용은 [ParticleFX node 문서](/manuals/gui-particlefx)를 참고하세요.

<div style="clear: both;"></div>

노드를 추가하려면 *Nodes* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add ▸</kbd>를 선택한 다음 <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> 또는 <kbd>ParticleFx</kbd>를 선택합니다.

![Add nodes](images/gui/add_node.png)

<kbd>A</kbd>를 누른 뒤 GUI에 추가하려는 타입을 선택할 수도 있습니다.

## 노드 프로퍼티 {#node-properties}

각 노드에는 외형을 제어하는 폭넓은 프로퍼티 집합이 있습니다.

Id
: 노드의 식별자입니다. 이 이름은 GUI 씬 안에서 유니크해야 합니다.

Position, Rotation and Scale
: 노드의 위치, 방향, 스케일을 제어합니다. *Move*, *Rotate*, *Scale* 도구를 사용해 이 값을 변경할 수 있습니다. 값은 스크립트에서 애니메이션할 수 있습니다([자세히 알아보기](/manuals/property-animation)).

Size (box, text and pie nodes)
: 노드의 크기는 기본적으로 자동이지만 *Size Mode*를 `Manual`로 설정하면 값을 변경할 수 있습니다. 크기는 노드의 경계를 정의하며 입력 선택을 할 때 사용됩니다. 이 값은 스크립트에서 애니메이션할 수 있습니다([자세히 알아보기](/manuals/property-animation)).

Size Mode (box and pie nodes)
: `Automatic`으로 설정하면 에디터가 노드의 크기를 설정합니다. `Manual`로 설정하면 직접 크기를 설정할 수 있습니다.

Enabled
: 체크를 해제하면 노드가 렌더링되지 않고, 애니메이션되지 않으며, `gui.pick_node()`로 선택할 수 없습니다. 이 프로퍼티를 프로그래밍 방식으로 변경하고 확인하려면 `gui.set_enabled()`와 `gui.is_enabled()`를 사용합니다.

Visible
: 체크를 해제하면 노드는 렌더링되지 않지만, 여전히 애니메이션할 수 있고 `gui.pick_node()`로 선택할 수 있습니다. 이 프로퍼티를 프로그래밍 방식으로 변경하고 확인하려면 `gui.set_visible()`과 `gui.get_visible()`을 사용합니다.

Text (text nodes)
: 노드에 표시할 텍스트입니다.

Line Break (text nodes)
: 텍스트가 노드 너비에 맞춰 줄바꿈되도록 설정합니다.

Font (text nodes)
: 텍스트를 렌더링할 때 사용할 폰트입니다.

Texture (box and pie nodes)
: 노드에 그릴 텍스쳐입니다. 아틀라스 또는 타일 소스 안의 이미지나 애니메이션에 대한 참조입니다.

Material (box, pie nodes, text and particlefx nodes)
: 노드를 그릴 때 사용할 메터리얼입니다. *Outline*의 Materials 섹션에 추가된 메터리얼을 사용할 수도 있고, 비워 두어 GUI 컴포넌트에 할당된 기본 메터리얼을 사용할 수도 있습니다.

Slice 9 (box nodes)
: 노드 크기가 변경될 때 가장자리 주변 노드 텍스쳐의 픽셀 크기를 보존하도록 설정합니다. 자세한 내용은 [Box node 문서](/manuals/gui-box)를 참고하세요.

Inner Radius (pie nodes)
: X축을 따라 표현되는 노드의 내부 반지름입니다. 자세한 내용은 [Pie node 문서](/manuals/gui-pie)를 참고하세요.

Outer Bounds (pie nodes)
: 외부 경계의 동작을 제어합니다. 자세한 내용은 [Pie node 문서](/manuals/gui-pie)를 참고하세요.

Perimeter Vertices (pie nodes)
: 모양을 만드는 데 사용할 세그먼트 수입니다. 자세한 내용은 [Pie node 문서](/manuals/gui-pie)를 참고하세요.

Pie Fill Angle (pie nodes)
: 파이를 얼마나 채울지 정합니다. 자세한 내용은 [Pie node 문서](/manuals/gui-pie)를 참고하세요.

Template (template nodes)
: 노드의 템플릿으로 사용할 GUI 씬 파일입니다. 자세한 내용은 [Template node 문서](/manuals/gui-template)를 참고하세요.

ParticleFX (particlefx nodes)
: 이 노드에서 사용할 파티클 효과입니다. 자세한 내용은 [ParticleFX node 문서](/manuals/gui-particlefx)를 참고하세요.

Color
: 노드의 색상입니다. 노드에 텍스쳐가 있으면 이 색상이 텍스쳐에 색조를 입힙니다. 색상은 스크립트에서 애니메이션할 수 있습니다([자세히 알아보기](/manuals/property-animation)).

Alpha
: 노드의 투명도입니다. 알파 값은 스크립트에서 애니메이션할 수 있습니다([자세히 알아보기](/manuals/property-animation)).

Inherit Alpha
: 이 체크박스를 설정하면 노드가 부모 노드의 알파 값을 상속합니다. 그러면 노드의 알파 값에 부모의 알파 값이 곱해집니다.

Leading (text nodes)
: 줄 간격에 대한 스케일 값입니다. `0` 값은 줄 간격이 없음을 의미합니다. `1`(기본값)은 일반 줄 간격입니다.

Tracking (text nodes)
: 글자 간격에 대한 스케일 값입니다. 기본값은 0입니다.

Layer
: 노드에 레이어를 할당하면 일반적인 그리기 순서를 오버라이드하고 대신 레이어 순서를 따릅니다. 자세한 내용은 아래를 참고하세요.

Blend mode
: 노드 그래픽이 배경 그래픽과 블렌딩되는 방식을 제어합니다.
  - `Alpha`는 노드의 픽셀 값을 배경과 알파 블렌딩합니다. 그래픽 소프트웨어의 "Normal" 블렌드 모드에 해당합니다.
  - `Add`는 노드의 픽셀 값을 배경에 더합니다. 일부 그래픽 소프트웨어의 "Linear dodge"에 해당합니다.
  - `Multiply`는 노드의 픽셀 값을 배경과 곱합니다.
  - `Screen`은 노드의 픽셀 값을 배경과 반대로 곱합니다. 그래픽 소프트웨어의 "Screen" 블렌드 모드에 해당합니다.

Pivot
: 노드의 피벗 포인트를 설정합니다. 이는 노드의 "중심점"으로 볼 수 있습니다. 모든 회전, 스케일 또는 크기 변경은 이 점을 중심으로 발생합니다.

  가능한 값은 `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West`, `South East`입니다.

  ![pivot point](images/gui/pivot.png)

  노드의 피벗을 변경하면 새 피벗이 노드의 위치에 오도록 노드가 이동합니다. 텍스트 노드는 `Center`이면 텍스트가 가운데 정렬되고, `West`이면 왼쪽 정렬되며, `East`이면 오른쪽 정렬됩니다.

X Anchor, Y Anchor
: 앵커는 씬 경계 또는 부모 노드의 경계가 실제 화면 크기에 맞게 늘어날 때 노드의 세로 및 가로 위치가 어떻게 변경되는지 제어합니다.

  ![Anchor unadjusted](images/gui/anchoring_unadjusted.png)

  사용할 수 있는 앵커 모드는 다음과 같습니다.

  - `None`(*X Anchor*와 *Y Anchor* 모두)은 부모 노드 또는 씬의 중심에서부터 노드 위치를 *조정된* 크기에 상대적으로 유지합니다.
  - `Left` 또는 `Right`(*X Anchor*)는 노드가 부모 노드 또는 씬의 왼쪽 및 오른쪽 가장자리에서 같은 비율의 위치를 유지하도록 노드의 가로 위치를 스케일합니다.
  - `Top` 또는 `Bottom`(*Y Anchor*)은 노드가 부모 노드 또는 씬의 위쪽 및 아래쪽 가장자리에서 같은 비율의 위치를 유지하도록 노드의 세로 위치를 스케일합니다.

  ![Anchoring](images/gui/anchoring.png)

Adjust Mode
: 노드의 조정 모드를 설정합니다. Adjust Mode 설정은 씬 경계 또는 부모 노드의 경계가 실제 화면 크기에 맞게 조정될 때 노드에 어떤 일이 일어나는지 제어합니다.

  논리 해상도가 일반적인 가로 화면 해상도인 씬에서 생성된 노드는 다음과 같습니다.

  ![Unadjusted](images/gui/unadjusted.png)

  씬을 세로 화면에 맞추면 씬이 늘어납니다. 각 노드의 바운딩 박스도 같은 방식으로 늘어납니다. 하지만 Adjust Mode를 설정하면 노드 컨텐츠의 종횡비를 그대로 유지할 수 있습니다. 사용할 수 있는 모드는 다음과 같습니다.

  - `Fit`은 늘어난 바운딩 박스의 너비 또는 높이 중 더 작은 쪽과 같아지도록 노드 컨텐츠를 스케일합니다. 즉 컨텐츠가 늘어난 노드 바운딩 박스 안에 맞습니다.
  - `Zoom`은 늘어난 바운딩 박스의 너비 또는 높이 중 더 큰 쪽과 같아지도록 노드 컨텐츠를 스케일합니다. 즉 컨텐츠가 늘어난 노드 바운딩 박스를 완전히 덮습니다.
  - `Stretch`는 늘어난 노드 바운딩 박스를 채우도록 노드 컨텐츠를 늘립니다.

  ![Adjust modes](images/gui/adjusted.png)

  GUI 씬 프로퍼티 *Adjust Reference*가 `Disabled`로 설정되어 있으면 이 설정은 무시됩니다.

Clipping Mode (box and pie nodes)
: 노드의 클리핑 모드를 설정합니다.

  - `None`은 노드를 평소처럼 렌더링합니다.
  - `Stencil`은 노드 경계가 노드의 자식 노드를 클리핑하는 데 사용되는 스텐실 마스크를 정의하게 합니다.

  자세한 내용은 [GUI 클리핑 매뉴얼](/manuals/gui-clipping)을 참고하세요.

Clipping Visible (box and pie nodes)
: 스텐실 영역 안에 노드의 컨텐츠를 렌더링하도록 설정합니다. 자세한 내용은 [GUI 클리핑 매뉴얼](/manuals/gui-clipping)을 참고하세요.

Clipping Inverted (box and pie nodes)
: 스텐실 마스크를 반전합니다. 자세한 내용은 [GUI 클리핑 매뉴얼](/manuals/gui-clipping)을 참고하세요.


## Pivot, Anchors 및 Adjust Mode

Pivot, Anchors, Adjust Mode 프로퍼티를 함께 사용하면 매우 유연하게 GUI를 디자인할 수 있지만, 구체적인 예제를 보지 않으면 동작 방식을 이해하기가 다소 어려울 수 있습니다. 640x1136 화면용으로 만든 다음 GUI 목업을 예로 들어 보겠습니다.

![](images/gui/adjustmode_example_original.png)

UI는 X와 Y Anchors가 None으로 설정된 상태로 만들어졌고, 각 노드의 Adjust Mode는 기본값인 Fit으로 남겨져 있습니다. 위쪽 패널의 Pivot 포인트는 North, 아래쪽 패널의 Pivot은 South, 위쪽 패널 안의 막대들의 Pivot 포인트는 West로 설정되어 있습니다. 나머지 노드의 Pivot 포인트는 Center로 설정되어 있습니다. 창의 너비를 넓히면 다음과 같은 일이 일어납니다.

![](images/gui/adjustmode_example_resized.png)

그렇다면 위쪽과 아래쪽 막대가 항상 화면 너비만큼 넓어지게 하려면 어떻게 해야 할까요? 위쪽과 아래쪽의 회색 배경 패널에 대한 Adjust Mode를 Stretch로 바꿀 수 있습니다.

![](images/gui/adjustmode_example_resized_stretch.png)

이쪽이 더 낫습니다. 이제 회색 배경 패널은 항상 창 너비만큼 늘어나지만, 위쪽 패널의 막대들과 아래쪽의 두 박스는 올바르게 배치되지 않았습니다. 위쪽 막대들을 왼쪽에 배치된 상태로 유지하려면 X Anchor를 None에서 Left로 바꿔야 합니다.

![](images/gui/adjustmode_example_top_anchor_left.png)

이것이 위쪽 패널에 대해 정확히 원하는 결과입니다. 위쪽 패널의 막대들은 이미 Pivot 포인트가 West로 설정되어 있었으므로, 막대의 왼쪽/서쪽 가장자리(Pivot)가 부모 패널의 왼쪽 가장자리(X Anchor)에 앵커되어 자연스럽게 위치를 잡습니다.

이제 왼쪽 박스의 X Anchor를 Left로, 오른쪽 박스의 X Anchor를 Right로 설정하면 다음 결과가 나옵니다.

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

이는 기대한 결과와 조금 다릅니다. 두 박스는 위쪽 패널의 두 막대처럼 왼쪽 및 오른쪽 가장자리에 가까운 상태로 유지되어야 합니다. 그 이유는 Pivot 포인트가 잘못되어 있기 때문입니다.

![](images/gui/adjustmode_example_bottom_pivot_center.png)

두 박스 모두 Pivot 포인트가 Center로 설정되어 있습니다. 이는 화면이 넓어질 때 박스의 중심점(피벗 포인트)이 가장자리에서 같은 상대 거리를 유지한다는 뜻입니다. 왼쪽 박스의 경우 원래 640x1136 창에서는 왼쪽 가장자리에서 17% 떨어져 있었습니다.

![](images/gui/adjustmode_example_original_ratio.png)

화면 크기가 변경되면 왼쪽 박스의 중심점은 왼쪽 가장자리에서 같은 거리인 17%를 유지합니다.

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

왼쪽 박스의 Pivot 포인트를 Center에서 West로, 오른쪽 박스는 East로 바꾸고 박스 위치를 다시 잡으면 화면 크기가 변경되어도 원하는 결과를 얻을 수 있습니다.

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## 그리기 순서

모든 노드는 "Nodes" 폴더 아래에 나열된 순서대로 렌더링됩니다. 목록 맨 위의 노드가 먼저 그려지므로 다른 모든 노드 뒤에 나타납니다. 목록의 마지막 노드는 마지막에 그려지므로 다른 모든 노드 앞에 나타납니다. 노드의 Z 값을 변경해도 그리기 순서는 제어되지 않습니다. 하지만 Z 값을 렌더 스크립트의 렌더 범위 밖으로 설정하면 노드는 더 이상 화면에 렌더링되지 않습니다. 레이어를 사용해 노드의 인덱스 순서를 오버라이드할 수 있습니다(아래 참고).

![Draw order](images/gui/draw_order.png)

노드를 선택하고 <kbd>Alt + Up/Down</kbd>을 눌러 노드를 위나 아래로 이동하고 인덱스 순서를 변경합니다.

그리기 순서는 스크립트에서 변경할 수 있습니다.

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## 부모-자식 계층구조

어떤 노드를 자식으로 만들려면 자식의 부모가 될 노드 위로 해당 노드를 끌어다 놓습니다. 부모가 있는 노드는 부모에 적용된, 그리고 부모 피벗에 상대적인 변형(transform: 위치, 회전, 스케일)을 상속합니다.

![Parent child](images/gui/parent_child.png)

부모는 자식보다 먼저 그려집니다. 부모와 자식 노드의 그리기 순서를 변경하고 노드 렌더링을 최적화하려면 레이어를 사용합니다(아래 참고).


## 레이어와 드로우 콜 {#layers-and-draw-calls}

레이어는 노드가 그려지는 방식을 세밀하게 제어하며, 엔진이 GUI 씬을 그리기 위해 만들어야 하는 드로우 콜 수를 줄이는 데 사용할 수 있습니다. 엔진이 GUI 씬의 노드를 그리려고 할 때, 다음 조건에 따라 노드를 드로우 콜 배치로 그룹화합니다.

- 노드가 같은 타입을 사용해야 합니다.
- 노드가 같은 아틀라스 또는 타일 소스를 사용해야 합니다.
- 노드가 같은 블렌드 모드로 렌더링되어야 합니다.
- 같은 폰트를 사용해야 합니다.

노드가 이 항목 중 하나라도 이전 노드와 다르면 배치가 끊기고 또 다른 드로우 콜이 만들어집니다. 클리핑 노드는 항상 배치를 끊으며, 각 스텐실 범위도 배치를 끊습니다.

노드를 계층구조로 정렬할 수 있으면 노드를 관리 가능한 단위로 쉽게 그룹화할 수 있습니다. 하지만 서로 다른 노드 타입을 섞으면 계층구조가 배치 렌더링을 효과적으로 끊을 수 있습니다.

![Breaking batch hierarchy](images/gui/break_batch.png)

렌더링 파이프라인이 노드 목록을 순회할 때 타입이 서로 다르기 때문에 각 개별 노드마다 별도의 배치를 설정해야 합니다. 결국 이 세 버튼에는 여섯 개의 드로우 콜이 필요합니다.

노드에 레이어를 할당하면 다른 순서로 정렬할 수 있으므로, 렌더 파이프라인이 더 적은 드로우 콜로 노드를 함께 그룹화할 수 있습니다. 먼저 씬에 필요한 레이어를 추가합니다. *Outline*에서 "Layers" 폴더 아이콘을 <kbd>Right click</kbd>하고 <kbd>Add ▸ Layer</kbd>를 선택합니다. 새 레이어를 선택하고 *Properties* 뷰에서 *Name* 프로퍼티를 할당합니다.

![Layers](images/gui/layers.png)

그런 다음 각 노드의 *Layer* 프로퍼티를 해당 레이어로 설정합니다. 레이어 그리기 순서는 일반적인 인덱스 기반 노드 순서보다 우선하므로, 버튼 그래픽 box 노드를 "graphics"로 설정하고 버튼 텍스트 노드를 "text"로 설정하면 다음 그리기 순서가 됩니다.

* 먼저 "graphics" 레이어의 모든 노드가 위에서부터 그려집니다.

  1. "button-1"
  2. "button-2"
  3. "button-3"

* 그런 다음 "text" 레이어의 모든 노드가 위에서부터 그려집니다.

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

이제 노드는 여섯 개 대신 두 개의 드로우 콜로 배치될 수 있습니다. 상당한 성능 향상입니다!

레이어가 설정되지 않은 자식 노드는 부모 노드의 레이어 설정을 암시적으로 상속합니다. 노드에 레이어를 설정하지 않으면 암시적으로 "null" 레이어에 추가되며, 이 레이어는 다른 모든 레이어보다 먼저 그려집니다.
