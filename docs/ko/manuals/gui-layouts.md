---
title: Defold의 GUI 레이아웃
brief: Defold는 모바일 장치의 화면 방향 전환에 자동으로 맞춰지는 GUI를 지원합니다. 이 문서는 이 기능이 작동하는 방식을 설명합니다.
---

# 레이아웃

Defold는 모바일 장치의 화면 방향 전환에 자동으로 맞춰지는 GUI를 지원합니다. 이 기능을 사용하면 다양한 화면 크기의 방향(orientation)과 종횡비(aspect ratio)에 맞게 조정되는 GUI를 디자인할 수 있습니다. 특정 장치 모델에 맞는 레이아웃을 만드는 것도 가능합니다.

## 디스플레이 프로파일 만들기 {#creating-display-profiles}

기본적으로 *game.project* 설정은 내장 디스플레이 프로파일 설정 파일("builtins/render/default.display_profiles")을 사용하도록 지정되어 있습니다. 기본 프로파일은 "Landscape"(폭 1280픽셀, 높이 720픽셀)와 "Portrait"(폭 720픽셀, 높이 1280픽셀)입니다. 프로파일에 장치 모델이 설정되어 있지 않으므로 어떤 장치에도 매칭됩니다.

새 프로파일 설정 파일을 만들려면 "builtins" 폴더의 파일을 복사하거나 *Assets* view의 적절한 위치에서 <kbd>오른쪽 클릭</kbd>하고 <kbd>New... ▸ Display Profiles</kbd>를 선택합니다. 새 파일에 적절한 이름을 지정하고 <kbd>Ok</kbd>를 클릭합니다.

이제 에디터에서 새 파일이 열려 편집할 수 있습니다. *Profiles* 목록에서 <kbd>+</kbd>를 클릭해 새 프로파일을 추가합니다. 각 프로파일마다 사용할 한정자(*qualifiers*) 집합을 추가합니다:

Width
: 한정자의 픽셀 폭입니다.

Height
: 한정자의 픽셀 높이입니다.

Device Models
: 쉼표로 구분된 장치 모델 목록입니다. 장치 모델은 장치 모델 이름의 시작 부분과 매칭됩니다. 예를 들어 `iPhone10`은 "iPhone10,\*" 모델과 매칭됩니다. 쉼표가 들어 있는 모델 이름은 따옴표로 감싸야 합니다. 즉 `"iPhone10,3", "iPhone10,6"`은 iPhone X 모델과 매칭됩니다([iPhone wiki](https://www.theiphonewiki.com/wiki/Models) 참고). `sys.get_sys_info()`를 호출했을 때 장치 모델을 보고하는 플랫폼은 Android와 iOS뿐입니다. 다른 플랫폼은 빈 문자열을 반환하므로 장치 모델 한정자가 있는 디스플레이 프로파일을 선택하지 않습니다.

![New display profiles](images/gui-layouts/new_profiles.png)

엔진이 새 프로파일을 사용하도록 지정해야 합니다. *game.project*를 열고 *display* 아래의 *Display Profiles* 설정에서 디스플레이 프로파일 파일을 선택합니다:

![Settings](images/gui-layouts/settings.png)

장치 회전 시 엔진이 세로(portrait)와 가로(landscape) 레이아웃 사이를 자동으로 전환하게 하려면 *Dynamic Orientation* 상자를 체크합니다. 엔진은 매칭되는 레이아웃을 동적으로 선택하고, 장치 방향이 바뀌면 선택도 변경합니다.

### Auto Layout Selection (Display Profiles)

Display Profiles 리소스에는 "Auto Layout Selection" 옵션이 있습니다(기본값 ON). ON이면 엔진은 씬이 생성될 때와 윈도우/디스플레이 크기가 변경될 때 모두 가장 잘 매칭되는 GUI 레이아웃을 자동으로 선택합니다. OFF이면 엔진은 레이아웃을 자동으로 변경하지 않습니다. 레이아웃을 수동으로 전환하려면 GUI 스크립트에서 `gui.set_layout()`을 사용하세요. 이 설정은 Display Profiles 파일에 저장되며 모든 GUI 씬에 영향을 줍니다.

## GUI 레이아웃

현재 디스플레이 프로파일 집합을 사용해 GUI 노드 구성의 레이아웃 변형을 만들 수 있습니다. GUI 씬에 새 레이아웃을 추가하려면 *Outline* view에서 *Layouts* 아이콘을 오른쪽 클릭하고 <kbd>Add ▸ Layout ▸ ...</kbd>를 선택합니다:

![Add layout to scene](images/gui-layouts/add_layout.png)

GUI 씬을 편집할 때 모든 노드는 특정 레이아웃에서 편집됩니다. 현재 선택된 레이아웃은 툴바의 GUI 씬 레이아웃 드롭다운에 표시됩니다. 레이아웃을 선택하지 않으면 노드는 *Default* 레이아웃에서 편집됩니다.

![Layouts toolbar](images/gui-layouts/toolbar.png)

![portrait edit](images/gui-layouts/portrait.png)

레이아웃이 선택된 상태에서 노드 프로퍼티를 변경할 때마다 *Default* 레이아웃 기준의 프로퍼티를 _오버라이드_합니다. 오버라이드된 프로퍼티는 파란색으로 표시됩니다. 오버라이드된 프로퍼티가 있는 노드도 파란색으로 표시됩니다. 오버라이드된 프로퍼티 옆의 리셋 버튼을 클릭하면 원래 값으로 되돌릴 수 있습니다.

![landscape edit](images/gui-layouts/landscape.png)

레이아웃은 노드를 삭제하거나 새 노드를 만들 수 없고, 프로퍼티만 오버라이드할 수 있습니다. 레이아웃에서 노드를 제거해야 한다면 노드를 화면 밖으로 옮기거나 스크립트 로직으로 삭제할 수 있습니다. 현재 선택된 레이아웃에도 주의해야 합니다. 프로젝트에 레이아웃을 추가하면 새 레이아웃은 현재 선택된 레이아웃을 기준으로 설정됩니다. 또한 노드 복사 붙여넣기는 복사할 때와 붙여넣을 때 *모두* 현재 선택된 레이아웃을 고려합니다.

## 동적 프로파일 선택

Auto Layout Selection이 활성화되면 엔진은 가장 잘 매칭되는 레이아웃을 자동으로 선택합니다. 동적 레이아웃 매칭은 다음 규칙에 따라 각 디스플레이 프로파일 한정자의 점수를 매깁니다:

1. 장치 모델이 설정되어 있지 않거나 장치 모델이 매칭되면, 해당 한정자의 점수(S)를 계산합니다.

2. 점수(S)는 디스플레이 면적(A), 한정자의 면적(A_Q), 디스플레이 종횡비(R), 한정자의 종횡비(R_Q)를 사용해 계산됩니다:

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. 한정자의 방향(landscape 또는 portrait)이 디스플레이와 일치하면, 가장 낮은 점수의 한정자를 가진 프로파일이 선택됩니다.

4. 같은 방향의 한정자를 가진 프로파일을 찾을 수 없으면, 다른 방향에서 가장 좋은 점수의 한정자를 가진 프로파일이 선택됩니다.

5. 프로파일을 선택할 수 없으면 *Default* 대체 프로파일이 사용됩니다.

런타임에 더 잘 매칭되는 레이아웃이 없으면 *Default* 레이아웃이 대체 레이아웃으로 사용됩니다. 따라서 "Landscape" 레이아웃을 추가하면 "Portrait" 레이아웃도 추가하기 전까지 *모든* 방향에서 가장 잘 매칭되는 레이아웃이 됩니다.

## 레이아웃 변경 메세지

레이아웃이 변경되면 `layout_changed` 메세지가 GUI 컴포넌트의 스크립트로 보내집니다. 이는 엔진이 레이아웃을 자동으로 변경할 때(Auto Layout Selection ON) 또는 스크립트가 `gui.set_layout()`을 호출하고 레이아웃이 실제로 변경될 때 발생합니다. 메세지에는 레이아웃의 해쉬된 id가 들어 있으므로, 스크립트는 어떤 레이아웃이 선택되었는지에 따라 로직을 수행할 수 있습니다:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- 레이아웃을 landscape로 전환
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- 레이아웃을 portrait로 전환
  end
end
```

또한 현재 렌더 스크립트는 윈도우(게임 뷰)가 변경될 때마다 메세지를 받으며, 여기에는 방향 전환도 포함됩니다.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- 윈도우 크기가 변경되었습니다. message.width와 message.height에는
    -- 윈도우의 새 크기가 들어 있습니다.
  end
end
```

방향이 전환되면 GUI 레이아웃 매니저는 레이아웃과 노드 프로퍼티에 따라 GUI 노드의 스케일과 위치를 자동으로 조정합니다. 그러나 게임 내 컨텐츠는 별도의 패스(기본값)에서 현재 윈도우로 stretch-fit 투영되어 렌더링됩니다. 이 동작을 변경하려면 수정한 렌더 스크립트를 직접 제공하거나 카메라 [라이브러리](/assets/)를 사용하세요.

## 수동 레이아웃 선택 (Lua)

사용 중인 Display Profiles에서 Auto Layout Selection이 OFF이면 엔진은 레이아웃을 자동으로 전환하지 않습니다. GUI 스크립트에서 다음 함수를 사용해 수동으로 레이아웃을 관리합니다:

### gui.set_layout(layout)

- 문자열 또는 해쉬(layout id)를 받습니다.
- 불린값을 반환합니다: 레이아웃이 씬에 있고 적용되었으면 `true`, 그렇지 않으면 `false`입니다.
- 레이아웃이 Display Profiles에 있으면 씬 해상도를 프로파일의 폭/높이로 업데이트합니다.
- 레이아웃이 실제로 변경되면 `layout_changed`를 발생시킵니다.

예:

```lua
function init(self)
    -- "Portrait" 레이아웃을 수동으로 적용
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- 각 레이아웃 id 해쉬를 `vmath.vector3(width, height, 0)`에 매핑한 테이블을 반환합니다.
- 기본 레이아웃의 경우 현재 씬 해상도를 반환합니다.

예:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

참고: GUI 레이아웃이 씬에 있지만 Display Profiles에는 없으면, `gui.set_layout()`은 여전히 레이아웃별 노드 오버라이드를 적용하지만 씬 해상도는 변경하지 않습니다.
