---
title: 카메라 컴포넌트 매뉴얼
brief: 이 매뉴얼은 Defold 카메라 컴포넌트의 기능을 설명합니다.
---

# 카메라

Defold의 카메라는 게임 월드의 뷰포트와 투영을 변경하는 컴포넌트입니다. 카메라 컴포넌트는 렌더 스크립트에 뷰 매트릭스와 투영 매트릭스를 제공하는 기본적인 원근 또는 직교 카메라를 정의합니다.

원근 카메라는 보통 3D 게임에 사용되며, 카메라의 뷰와 오브젝트의 크기 및 원근은 뷰 절두체와 카메라에서 게임 속 오브젝트까지의 거리 및 시야각을 기준으로 결정됩니다.

2D 게임에서는 씬을 직교 투영(orthographic projection)으로 렌더링하는 것이 바람직한 경우가 많습니다. 이는 카메라의 뷰가 더 이상 뷰 절두체가 아니라 상자에 의해 정해진다는 뜻입니다. 직교 투영은 거리에 따라 오브젝트의 크기를 바꾸지 않기 때문에 현실적이지 않습니다. 1000 유닛 떨어진 오브젝트도 카메라 바로 앞에 있는 오브젝트와 같은 크기로 렌더링됩니다.

![projections](images/camera/projections.png)


## 카메라 생성하기

카메라를 생성하려면 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component ▸ Camera</kbd>를 선택합니다. 또는 프로젝트 계층구조에 컴포넌트 파일을 만든 뒤, 해당 컴포넌트 파일을 게임 오브젝트에 추가할 수도 있습니다.

![create camera component](images/camera/create.png)

카메라 컴포넌트에는 카메라 *절두체*를 정의하는 다음 프로퍼티가 있습니다.

![camera settings](images/camera/settings.png)

Id
: 컴포넌트의 id입니다.

Aspect Ratio
: (**원근 카메라 전용**) - 절두체의 너비와 높이 사이의 비율입니다. 1.0은 정사각형 뷰를 가정한다는 뜻입니다. 1.33은 1024x768 같은 4:3 뷰에 적합합니다. 1.78은 16:9 뷰에 적합합니다. *Auto Aspect Ratio*가 설정되어 있으면 이 설정은 무시됩니다.

Fov
: (**원근 카메라 전용**) - _라디안_으로 표현한 카메라의 *수직* 시야각입니다. 시야각이 넓을수록 카메라가 더 많은 영역을 볼 수 있습니다.

Near Z
: near clipping plane의 Z 값입니다.

Far Z
: far clipping plane의 Z 값입니다.

Auto Aspect Ratio
: (**원근 카메라 전용**) - 카메라가 종횡비를 자동으로 계산하도록 하려면 이 값을 설정합니다.

Orthographic Projection
: 카메라를 직교 투영으로 전환하려면 이 값을 설정합니다(아래 참조).

Orthographic Zoom
: (**직교 카메라 전용**) - 직교 투영에 사용하는 줌입니다(> 1 = 확대, < 1 = 축소).

Orthographic Mode
: (**직교 카메라 전용**) - 직교 카메라가 창 크기와 디자인 해상도(`game.project` → `display.width/height`의 값)를 기준으로 줌을 결정하는 방식을 제어합니다.
  - `Fixed` (고정 줌 사용): 현재 `Orthographic Zoom` 값을 그대로 사용합니다.
  - `Auto Fit` (contain): 전체 디자인 영역이 창 안에 들어가도록 줌을 자동으로 조정합니다. 좌우 또는 상하에 추가 컨텐츠가 보일 수 있습니다.
  - `Auto Cover` (cover): 디자인 영역이 창 전체를 덮도록 줌을 자동으로 조정합니다. 좌우 또는 상하가 잘릴 수 있습니다.
  `Orthographic Projection`이 활성화된 경우에만 사용할 수 있습니다.


## 카메라 사용하기

모든 카메라는 프레임 동안 자동으로 활성화되고 업데이트되며, Lua `camera` 모듈은 모든 스크립트 컨텍스트에서 사용할 수 있습니다. Defold 1.8.1부터는 카메라 컴포넌트에 `acquire_camera_focus` 메세지를 보내 카메라를 명시적으로 활성화할 필요가 없어졌습니다. 기존 acquire 및 release 메세지는 아직 사용할 수 있지만, 활성화하거나 비활성화하려는 다른 컴포넌트와 마찬가지로 `enable` 및 `disable` 메세지를 사용하는 것을 권장합니다.

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

현재 사용할 수 있는 모든 카메라를 나열하려면 `camera.get_cameras()`를 사용할 수 있습니다.

```lua
-- 참고: render 호출은 렌더 스크립트에서만 사용할 수 있습니다.
--       camera.get_cameras() 함수는 어디서든 사용할 수 있지만,
--       render.set_camera는 렌더 스크립트에서만 사용할 수 있습니다.

for k,v in pairs(camera.get_cameras()) do
    -- camera 테이블은 모든 카메라의 URL을 포함합니다.
    render.set_camera(v)
    -- 여기서 렌더링을 수행합니다. 여기서 렌더링되는 것 중 뷰 및
    -- 투영 매트릭스가 지정된 메터리얼을 사용하는 것은 카메라의
    -- 매트릭스를 사용합니다.
end
-- 카메라를 비활성화하려면 render.set_camera에 nil을 전달하거나
-- 인수를 아예 전달하지 않습니다.
-- 이 호출 이후 모든 render 호출은 렌더 컨텍스트에 지정된
-- 뷰 및 투영 매트릭스(render.set_view 및 render.set_projection)를 사용합니다.
render.set_camera()
```

스크립트용 `camera` 모듈에는 카메라를 조작하는 데 사용할 수 있는 여러 함수가 있습니다. 사용할 수 있는 함수 중 일부만 아래에 소개합니다. 사용 가능한 모든 함수는 [API 문서](/ref/camera/)의 매뉴얼을 참조하세요.

```lua
camera.get_aspect_ratio(camera) -- 종횡비 얻기
camera.get_far_z(camera) -- far z 얻기
camera.get_fov(camera) -- 시야각 얻기
camera.get_orthographic_mode(camera) -- 직교 모드 얻기(camera.ORTHO_MODE_* 중 하나)
camera.set_aspect_ratio(camera, ratio) -- 종횡비 설정
camera.set_far_z(camera, far_z) -- far z 설정
camera.set_near_z(camera, near_z) -- near z 설정
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- 직교 모드 설정
... 기타 등등
```

카메라는 URL로 식별됩니다. 이 URL은 컴포넌트의 전체 씬 경로이며, 컬렉션, 해당 컴포넌트가 속한 게임 오브젝트, 컴포넌트 id를 포함합니다. 이 예제에서는 같은 컬렉션 안에서 카메라 컴포넌트를 식별할 때 URL `/go#camera`를 사용하고, 다른 컬렉션이나 렌더 스크립트에서 카메라에 액세스할 때는 `main:/go#camera`를 사용합니다.

![create camera component](images/camera/create.png)

```lua
-- 같은 컬렉션의 스크립트에서 카메라에 액세스:
camera.get_fov("/go#camera")

-- 다른 컬렉션의 스크립트에서 카메라에 액세스:
camera.get_fov("main:/go#camera")

-- 렌더 스크립트에서 카메라에 액세스:
render.set_camera("main:/go#camera")
```

각 프레임마다 현재 카메라 포커스를 가진 카메라 컴포넌트는 `@render` 소켓으로 `set_view_projection` 메세지를 보냅니다.

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. 카메라 컴포넌트가 보낸 메세지에는 뷰 매트릭스와 투영 매트릭스가 포함됩니다.

카메라 컴포넌트는 카메라의 *Orthographic Projection* 프로퍼티에 따라 원근 또는 직교 투영 매트릭스를 렌더 스크립트에 제공합니다. 투영 매트릭스는 정의된 near 및 far clipping plane, 시야각, 카메라의 종횡비 설정도 고려합니다.

카메라가 제공하는 뷰 매트릭스는 카메라의 위치와 방향을 정의합니다. *Orthographic Projection*을 사용하는 카메라는 연결된 게임 오브젝트의 위치를 기준으로 뷰를 중앙에 배치하고, *원근 투영*을 사용하는 카메라는 연결된 게임 오브젝트의 위치에 뷰의 왼쪽 아래 모서리를 배치합니다.


### 렌더 스크립트

기본 렌더 스크립트를 사용할 때 Defold는 렌더링에 사용할 마지막으로 활성화된 카메라를 자동으로 설정합니다. 이 변경 전에는 프로젝트 어딘가의 스크립트가 렌더러에 `use_camera_projection` 메세지를 명시적으로 보내 카메라 컴포넌트의 뷰와 투영을 사용해야 한다고 알려야 했습니다. 이제는 필요하지 않지만, 이전 버전과의 호환성을 위해 여전히 그렇게 할 수 있습니다.

또는 렌더 스크립트에서 렌더링에 사용할 특정 카메라를 설정할 수 있습니다. 예를 들어 멀티플레이어 게임처럼 어떤 카메라를 렌더링에 사용할지 더 구체적으로 제어해야 하는 경우에 유용할 수 있습니다.

```lua
-- render.set_camera는 render.set_camera()가 호출될 때까지
-- 발생하는 모든 렌더링에 대해 뷰 및 투영 매트릭스를
-- 자동으로 사용합니다.
render.set_camera("main:/my_go#camera")
```

카메라가 활성 상태인지 확인하려면 [Camera API](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera)의 `get_enabled` 함수를 사용할 수 있습니다.

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- 카메라가 활성화되어 있으므로 렌더링에 사용합니다!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
`set_camera` 함수를 절두체 컬링(frustum culling)과 함께 사용하려면 이 옵션을 함수에 전달해야 합니다.
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### 카메라 패닝

카메라 컴포넌트가 연결된 게임 오브젝트를 움직이면 게임 월드에서 카메라를 패닝하거나 이동할 수 있습니다. 카메라 컴포넌트는 카메라의 현재 x축 및 y축 위치를 기준으로 업데이트된 뷰 매트릭스를 자동으로 보냅니다.

### 카메라 줌

원근 카메라를 사용할 때는 카메라가 연결된 게임 오브젝트를 z축을 따라 움직여 확대 및 축소할 수 있습니다. 카메라 컴포넌트는 카메라의 현재 z 위치를 기준으로 업데이트된 뷰 매트릭스를 자동으로 보냅니다.

직교 카메라를 사용할 때는 카메라의 *Orthographic Zoom* 프로퍼티를 변경하여 확대 및 축소할 수 있습니다.

```lua
go.set("#camera", "orthographic_zoom", 2)
```

직교 카메라를 사용할 때는 `Orthographic Mode` 설정 또는 스크립트를 통해 줌을 결정하는 방식을 전환할 수도 있습니다.

```lua
-- 현재 모드 얻기(camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER 중 하나)
local mode = camera.get_orthographic_mode("#camera")

-- 전체 디자인 영역이 항상 보이도록 auto-fit(contain)으로 전환
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- 디자인 영역이 창을 덮도록 auto-cover로 전환
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- orthographic_zoom으로 줌을 직접 제어하도록 fixed mode로 다시 전환
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### 적응형 줌

적응형 줌의 개념은 디스플레이 해상도가 *game.project*에 설정된 초기 해상도에서 변경될 때 카메라 줌 값을 조정하는 것입니다.

적응형 줌에는 두 가지 일반적인 접근 방식이 있습니다.

1. 최대 줌 - *game.project*의 초기 해상도가 덮는 컨텐츠가 화면 경계를 채우고 그 너머로 확장되도록 줌 값을 계산합니다. 이때 좌우 또는 상하 일부 컨텐츠가 숨겨질 수 있습니다.
2. 최소 줌 - *game.project*의 초기 해상도가 덮는 컨텐츠가 화면 경계 안에 완전히 포함되도록 줌 값을 계산합니다. 이때 좌우 또는 상하에 추가 컨텐츠가 보일 수 있습니다.

예제:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: 초기 디자인 크기가 화면 경계를 채우고 그 너머로 확장되도록 보장
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: 초기 디자인 크기가 줄어들어 화면 경계 안에 포함되도록 보장
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale

            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

적응형 줌의 전체 예제는 [이 샘플 프로젝트](https://github.com/defold/sample-adaptive-zoom)에서 볼 수 있습니다.

참고: 직교 카메라를 사용할 때 이제는 커스텀 코드 없이도 `Orthographic Mode`를 `Auto Fit`(contain) 또는 `Auto Cover`(cover)로 설정하여 contain/cover 동작을 구현할 수 있습니다. 이 모드에서는 창 크기와 디자인 해상도를 기준으로 유효 줌이 자동으로 계산됩니다.


### 게임 오브젝트 따라가기

카메라 컴포넌트가 연결된 게임 오브젝트를 따라갈 게임 오브젝트의 자식으로 설정하면 카메라가 게임 오브젝트를 따라가게 할 수 있습니다.

![follow game object](images/camera/follow.png)

다른 방법으로는 따라갈 게임 오브젝트가 움직일 때마다 카메라 컴포넌트가 연결된 게임 오브젝트의 위치를 매 프레임 업데이트하는 방식이 있습니다.

### 마우스를 월드 좌표로 변환하기

카메라가 패닝되거나 줌되었거나 기본 직교 Stretch 투영에서 투영이 변경되면, `on_input()` 라이프사이클 함수에서 제공되는 마우스 좌표는 더 이상 게임 오브젝트의 월드 좌표와 일치하지 않습니다. 뷰 또는 투영의 변화를 직접 고려해야 합니다. 마우스/화면 좌표를 월드 좌표로 변환하는 코드는 다음과 같습니다.

```Lua
--- 특정 카메라의 뷰와 투영을 고려하여
-- 화면 좌표를 월드 좌표로 변환합니다.
-- @param camera 변환에 사용할 카메라의 URL
-- @param screen_x 변환할 화면 x 좌표
-- @param screen_y 변환할 화면 y 좌표
-- @param z 변환을 통과시킬 선택적 z 좌표, 기본값은 0
-- @return world_x 화면 좌표의 결과 월드 x 좌표
-- @return world_y 화면 좌표의 결과 월드 y 좌표
-- @return world_z 화면 좌표의 결과 월드 z 좌표
function M.screen_to_world(camera, screen_x, screen_y, z)
    local projection = go.get(camera, "projection")
    local view = go.get(camera, "view")
    local w, h = window.get_size()

    -- https://defold.com/manuals/camera/#converting-mouse-to-world-coordinates
    local inv = vmath.inv(projection * view)
    local x = (2 * screen_x / w) - 1
    local y = (2 * screen_y / h) - 1
    local x1 = x * inv.m00 + y * inv.m01 + z * inv.m02 + inv.m03
    local y1 = x * inv.m10 + y * inv.m11 + z * inv.m12 + inv.m13
    return x1, y1, z or 0
end
```

`on_input()`의 `action.screen_x` 및 `action.screen_y` 값을 이 함수의 인수로 사용해야 한다는 점을 기억하세요. 화면 좌표에서 월드 좌표로 변환하는 동작을 보려면 [예제 페이지](https://defold.com/examples/render/screen_to_world/)를 방문하세요. 화면 좌표를 월드 좌표로 변환하는 방법을 보여주는 [샘플 프로젝트](https://github.com/defold/sample-screen-to-world-coordinates/)도 있습니다.

::: sidenote
이 매뉴얼에서 언급한 [서드파티 카메라 솔루션](/manuals/camera/#third-party-camera-solutions)은 화면 좌표로 변환하거나 화면 좌표에서 변환하는 함수를 제공합니다.
:::

## 런타임 조작

여러 다양한 메세지와 프로퍼티를 통해 런타임에 카메라를 조작할 수 있습니다(사용법은 [API 문서](/ref/camera/) 참조).

카메라에는 `go.get()` 및 `go.set()`으로 조작할 수 있는 여러 프로퍼티가 있습니다.

`fov`
: 카메라 시야각입니다(`number`).

`near_z`
: 카메라 near Z 값입니다(`number`).

`far_z`
: 카메라 far Z 값입니다(`number`).

`orthographic_zoom`
: 직교 카메라 줌입니다(`number`).

`aspect_ratio`
: 절두체의 너비와 높이 사이의 비율입니다. 원근 카메라의 투영을 계산할 때 사용됩니다(`number`).

`view`
: 카메라의 계산된 뷰 매트릭스입니다. 읽기 전용입니다(`matrix4`).

`projection`
: 카메라의 계산된 투영 매트릭스입니다. 읽기 전용입니다(`matrix4`).


## 서드파티 카메라 솔루션

화면 흔들림, 게임 오브젝트 따라가기, 화면-월드 좌표 변환 등 일반적인 기능을 구현한 커뮤니티 제작 카메라 솔루션이 있습니다. Defold asset portal에서 다운로드할 수 있습니다.

- [Orthographic camera](https://defold.com/assets/orthographic/) (2D 전용), Björn Ritzl 제작.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D 및 3D), Klayton Kowalski 제작.
