---
title: Defold 씬 에디터
brief: Scene Editor는 컬렉션, 게임 오브젝트, GUI, 파티클 효과 및 기타 시각적 에셋을 편집하는 곳입니다. 이 매뉴얼은 선택, 도구, 2D와 3D에서 씬 뷰를 탐색하는 방법(Free Camera Mode와 카메라 설정 포함)을 설명합니다.
---

# Defold 씬 에디터

**Scene Editor**는 컬렉션(collection), 게임 오브젝트(game object) 및 기타 시각적 에셋과 같은 씬을 만들고 편집하는 데 사용하는 시각적 에디터입니다.

기본적으로 많은 시각적 씬은 **2D 직교 투영** 뷰로 열립니다. 3D 작업에서는 3D에 맞는 레이아웃으로 전환하고, 3D 그리드 평면을 활성화하며, **원근 투영(perspective)** 카메라를 사용할 수 있습니다.

## Scene Editor 열기

다음과 같은 시각적 리소스를 *Assets* pane 창에서 더블 클릭하여 Scene Editor를 엽니다.

- **씬 구조** — 컬렉션(`.collection`), 게임 오브젝트(`.go`)
- **2D 에셋** — 아틀라스(`.atlas`), 타일 맵(`.tilemap`), 스프라이트(`.sprite`), 타일 소스(`.tilesource`)
- **3D 에셋** — 모델(`.model`, `.glb`, `.gltf`)
- **UI** — GUI 씬(`.gui`)
- **효과** — 파티클 효과(`.particlefx`)
- 기타 리소스

## 씬 뷰 탐색(카메라 컨트롤)

Scene Editor 카메라는 마우스와 키보드로 제어할 수 있습니다. 사용할 수 있는 컨트롤은 표준 카메라 탐색을 사용하는지, **Free Camera Mode**를 사용하는지에 따라 달라집니다.

### 표준 탐색(모든 시각적 에디터)

시각적 에디터에서는 다음 컨트롤을 사용할 수 있습니다.

- **팬 이동**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **확대/축소**
  - <kbd>Mouse Wheel</kbd>, 또는
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **선택 항목을 중심으로 회전/오빗(3D)**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

**Frame Selection**(<kbd>F</kbd>)을 사용해 현재 선택 항목에 카메라 초점을 맞출 수도 있습니다.

## 2D와 3D 씬 방향 {#2d-and-3d-scene-orientation}

씬 뷰는 2D와 3D 워크플로우 모두에서 사용할 수 있습니다.

- **2D**에서는 일반적으로 2D 지향 그리드가 있는 직교 투영 뷰에서 작업합니다.
- **3D**에서는 일반적으로 다음과 같이 작업합니다.
  - 뷰를 3D 방향으로 다시 정렬합니다.
  - **원근 투영(perspective)** 카메라를 사용합니다.
  - 적절한 그리드 평면을 선택합니다. “지면”에는 보통 **Y**를 사용합니다.

이 기능은 툴바와 **View** 메뉴에서 사용할 수 있습니다.

![Scene Editor 3D](images/editor/3d_scene.png)

## 툴바 개요

씬 뷰 오른쪽 위에는 자주 사용하는 도구와 뷰 옵션이 있는 툴바가 있습니다(왼쪽부터 오른쪽 순서).

- **Move tool**(<kbd>W</kbd>)
- **Rotate tool**(<kbd>E</kbd>)
- **Scale tool**(<kbd>R</kbd>)
- **Grid Settings**(`▦`)
- **Align/Realign Camera 2D/3D**(`2D`) — 2D와 3D 방향을 전환합니다(단축키 <kbd>.</kbd>).
- **Camera Perspective/Orthographic**
- **Visibility Filters**(`👁`)

![Toolbar](images/editor/toolbar.png)

## 오브젝트 선택 및 조작 {#manipulating-objects}

### 오브젝트 선택

메인 창에서 오브젝트를 <kbd>Left Mouse Click</kbd>하여 선택합니다. 에디터 뷰에서 오브젝트를 둘러싼 사각형(또는 직육면체)이 청록색으로 강조되어 어떤 항목이 선택되었는지 나타냅니다. 선택된 오브젝트는 위 그림처럼 `Outline` 뷰에서도 강조됩니다.

또한 다음 방법으로 오브젝트를 선택할 수 있습니다.

- <kbd>Left Mouse Click</kbd> 후 <kbd>Drag</kbd>하여 선택 영역 안의 모든 오브젝트를 선택합니다.
- `Outline`에서 오브젝트를 <kbd>Left Mouse Click</kbd>하고, <kbd>⇧ Shift</kbd>를 누른 상태로 선택 범위를 확장하거나 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>를 누른 상태로 클릭한 항목을 선택/선택 해제할 수 있습니다.

#### Move tool

![Move tool](images/editor/icon_move.png){.left}

오브젝트를 이동하려면 *Move Tool*을 사용합니다. 씬 에디터 오른쪽 위의 툴바에서 찾거나 <kbd>W</kbd> 키를 눌러 사용할 수 있습니다.

![오브젝트 이동](images/editor/move.png){.inline}![3D 오브젝트 이동](images/editor/move_3d.png){.inline}

기즈모가 변경되고, 드래그하여 이동할 수 있는 사각형과 화살표 조작 핸들이 표시됩니다. 선택된 조작 핸들은 주황색으로 바뀝니다.

- 청록색 중앙 사각형 핸들 하나는 오브젝트를 화면 공간에서만 이동합니다.
- 빨간색, 녹색, 파란색 화살표 3개는 각각 지정된 X, Y 또는 Z 축을 따라서만 오브젝트를 이동합니다.
- 투명한 채움과 외곽선으로 표시된 빨간색, 녹색, 파란색 사각형 핸들 3개는 지정된 평면에서만 오브젝트를 이동합니다. 예를 들어 X-Y(파란색) 평면과, 3D에서 카메라를 회전하면 보이는 X-Z(녹색), Y-Z(빨간색) 평면이 있습니다.

#### Rotate tool

![Rotate tool](images/editor/icon_rotate.png){.left}

오브젝트를 회전하려면 툴바에서 *Rotate Tool*을 선택하거나 <kbd>E</kbd> 키를 눌러 사용합니다.

![오브젝트 회전](images/editor/rotate.png){.inline}![3D 오브젝트 회전](images/editor/rotate_3d.png){.inline}

이 도구는 드래그하여 회전할 수 있는 네 개의 원형 조작 핸들로 구성됩니다. 선택된 조작 핸들은 주황색으로 바뀝니다.

- 청록색 조작 핸들 하나(가장 바깥쪽의 가장 큰 원)는 화면 공간에서 오브젝트를 회전합니다.
- 더 작은 빨간색, 녹색, 파란색 원형 조작 핸들 3개는 각각 X, Y, Z 축을 기준으로 별도로 회전할 수 있게 합니다. 2D 직교 투영 뷰에서는 이 중 두 개가 X축과 Y축에 수직이므로, 원이 오브젝트를 가로지르는 두 선처럼만 보입니다.

#### Scale tool

![Scale tool](images/editor/icon_scale.png){.left}

오브젝트의 스케일을 조정하려면 툴바에서 *Scale Tool*을 선택하거나 <kbd>R</kbd> 키를 눌러 사용합니다.

![오브젝트 스케일 조정](images/editor/scale.png){.inline}![3D 오브젝트 스케일 조정](images/editor/scale_3d.png){.inline}

이 도구는 드래그하여 스케일을 조정할 수 있는 사각형/정육면체 조작 핸들 세트로 구성됩니다. 선택된 조작 핸들은 주황색으로 바뀝니다.

- 중앙의 청록색 정육면체 하나는 모든 축에서 오브젝트의 스케일을 균일하게 조정합니다(Z 포함).
- 빨간색, 파란색, 녹색 정육면체 조작 핸들 3개는 각각 X, Y, Z 축을 따라 오브젝트의 스케일을 별도로 조정합니다.
- 투명한 채움과 외곽선으로 표시된 빨간색, 녹색, 파란색 사각형 조작 핸들 3개는 X-Y, X-Z 또는 Y-Z 평면에서 오브젝트의 스케일을 별도로 조정합니다.

### Visibility filters

툴바에서 **Visibility Eye Icon**(`👁`)을 클릭하면 여러 컴포넌트 타입뿐 아니라 바운딩 박스와 가이드 라인(`Component Guides`, 단축키는 Win/Linux에서 <kbd>Ctrl</kbd> + <kbd>H</kbd>, Mac에서 <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>)의 표시 여부를 전환할 수 있습니다.

![Visibility filters](images/editor/visibilityfilters.png)

## 그리드 설정 {#grid-settings}

그리드는 워크플로우에 맞게 사용자 지정할 수 있습니다. 특히 3D에서 유용합니다. **Grid Settings** 버튼(`▦`)을 클릭하여 그리드 설정 팝업을 엽니다.

![Grid Settings](images/editor/grid_popup.png)

설정에는 다음이 포함됩니다.

- **Grid size (X/Y/Z)**
  각 축을 따라 그리드 선 사이의 간격을 설정합니다. 작은 오브젝트를 정밀하게 배치하려면 작은 값을 사용하고, 더 넓게 살펴보려면 큰 값을 사용합니다.
- **Active plane (X/Y/Z)**
  그리드가 그려질 평면을 선택합니다. 2D 워크플로우에서는 일반적으로 **Z**(기본 X-Y 평면)입니다. 3D 워크플로우에서는 **Y**를 지면/바닥 평면으로 표현하는 경우가 많습니다.
- **Grid color**
  그리드 선의 색을 설정합니다. 서로 다른 씬 배경과 대비를 맞출 때 유용합니다.
- **Grid opacity**
  그리드 선의 투명도를 제어합니다. 낮은 값은 그리드를 덜 눈에 띄게 하면서도 기준으로 사용할 수 있게 합니다.
- **Reset to Defaults** 버튼
  모든 그리드 설정을 기본값으로 되돌립니다.

## 카메라 타입: Perspective와 Orthographic

Scene Editor는 다음 두 가지를 모두 지원합니다.

- **Orthographic** 카메라(2D 워크플로우에서 일반적)
- **Perspective** 카메라(3D 워크플로우에서 일반적)

전환하려면 툴바의 카메라 토글을 사용합니다. 3D 씬에서는 일반적으로 Perspective 카메라 탐색이 더 자연스럽게 느껴집니다.

## Free Camera Mode

빠른 3D 탐색을 위해 Scene Editor는 1인칭/FPS 스타일 카메라인 **Free Camera Mode**를 제공합니다.

### Free Camera Mode 활성화

- <kbd>Right Mouse Button</kbd>을 길게 누릅니다. 버튼을 누르고 있는 동안 Free Camera Mode가 활성화됩니다.
- <kbd>Shift</kbd> + <kbd>`</kbd>(backtick)은 Free Camera Mode를 켜는 토글이며, 키를 놓은 뒤에도 활성 상태를 유지합니다.

::: sidenote
일부 키보드 레이아웃(예: 스웨덴어)에서는 backtick 키가 데드 키(dead key)라 단축키가 예상대로 동작하지 않을 수 있습니다. 이 단축키는 `File ▸ Preferences ▸ Keys`에서 다시 바인딩할 수 있으며, `Scene -> Free Camera -> Activate`의 단축키를 입력하면 됩니다.
:::

Free Camera Mode가 활성화되면 씬 뷰의 가장자리가 선으로 강조됩니다.

### Free Camera Mode 종료

- 길게 눌러 활성화한 경우 <kbd>Right Mouse Button</kbd>을 놓습니다. 또는
- Free Camera Mode를 토글로 활성화한 경우 <kbd>Left Mouse Button</kbd>, <kbd>Right Mouse Button</kbd>(누른 뒤 놓기) 또는 <kbd>Esc</kbd>를 누릅니다.

### 둘러보기(mouse look)

Free Camera Mode가 활성화되어 있는 동안 다음 입력은 에디터 도구 대신 카메라 이동을 제어합니다.

- 마우스를 움직여 **yaw**(좌/우)와 **pitch**(위/아래)를 제어합니다.
- 카메라가 뒤집히지 않도록 pitch는 제한됩니다.

선택적으로 Y축을 반전할 수도 있습니다. 아래의 **카메라 설정 팝업**을 참고하세요.

### 이동

Free Camera Mode가 활성화되어 있는 동안:

- <kbd>W</kbd> — 앞으로
- <kbd>S</kbd> — 뒤로
- <kbd>A</kbd> — 왼쪽
- <kbd>D</kbd> — 오른쪽
- <kbd>E</kbd> — 위
- <kbd>Q</kbd> — 아래

::: sidenote
모든 이동 키는 `File ▸ Preferences ▸ Keys`에서 다시 바인딩할 수 있습니다. 그런 다음 `Scene -> Free Camera`를 검색하세요.
:::

속도 변경 키:

- <kbd>Shift</kbd>를 길게 누릅니다. 더 빠르게 이동합니다.
- <kbd>Alt</kbd>/<kbd>⌥ Option</kbd>을 길게 누릅니다. 더 느리게, 더 정밀하게 이동합니다.

### Walking Mode(선택 사항)

Free Camera Mode는 **Walking Mode**를 지원합니다.

활성화하면:
- 위/아래 이동이 제한되어 지면 평면 위에서 이동하는 1인칭 보행처럼 동작합니다.
- 레벨을 탐색할 때 일관된 “지면 기반” 이동을 원하면 유용합니다.

## 카메라 설정 팝업

툴바의 Perspective 카메라 버튼에는 카메라 관련 환경설정을 위한 설정 팝업이 있습니다.

![Perspective Camera Settings](images/editor/camera_popup.png)

팝업에는 다음이 포함됩니다.

- **Move Speed**
  Free Camera Mode의 이동 속도를 조정합니다.

- **Look Sensitivity**
  마우스 이동에 반응하여 카메라가 회전하는 속도를 조정합니다.

- **Invert Y**
  마우스로 둘러볼 때의 수직 방향을 반전합니다.

- **Walking Mode**
  지면 위를 이동하는 것처럼 탐색하도록 움직임을 제한합니다.

- **Reset to Defaults**
  기본 카메라 설정을 복원합니다.
