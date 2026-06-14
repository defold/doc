---
title: Defold의 렌더링 파이프라인
brief: 이 매뉴얼은 Defold의 렌더링 파이프라인이 어떻게 동작하는지와 이를 프로그래밍하는 방법을 설명합니다.
---

# 렌더링 {#render}

엔진이 화면에 표시하는 모든 오브젝트, 즉 스프라이트, 모델, 타일, 파티클, GUI 노드는 렌더러가 그립니다. 렌더러의 핵심에는 렌더링 파이프라인을 제어하는 렌더 스크립트가 있습니다. 기본적으로 모든 2D 오브젝트는 지정된 블렌딩과 올바른 Z depth에서 올바른 비트맵으로 그려지므로, 정렬과 간단한 블렌딩 이상으로 렌더링을 신경 쓸 필요가 없을 수도 있습니다. 대부분의 2D 게임에서는 기본 파이프라인이 잘 동작하지만, 게임에 특별한 요구사항이 있을 수 있습니다. 이런 경우 Defold에서는 맞춤형 렌더링 파이프라인을 작성할 수 있습니다.

### 렌더링 파이프라인 - 무엇을, 언제, 어디에? {#render-pipeline---what-when-and-where}

렌더링 파이프라인은 무엇을 렌더링할지, 언제 렌더링할지, 그리고 어디에 렌더링할지를 제어합니다. 무엇을 렌더링할지는 [렌더 predicate](#render-predicates)가 제어합니다. predicate를 언제 렌더링할지는 [렌더 스크립트](#the-render-script)에서 제어하고, predicate를 어디에 렌더링할지는 [뷰 투영](#default-view-projection)이 제어합니다. 렌더링 파이프라인은 정의된 바운딩 박스나 절두체(frustum) 밖에 있는, 렌더 predicate가 그린 그래픽을 컬링할 수도 있습니다. 이 과정을 절두체 컬링(frustum culling)이라고 합니다.


## 기본 렌더링 {#the-default-render}

렌더 파일에는 현재 렌더 스크립트에 대한 참조와 렌더 스크립트에서 사용할 수 있어야 하는 커스텀 메터리얼이 들어 있습니다([`render.enable_material()`](/ref/render/#render.enable_material)과 함께 사용).

렌더링 파이프라인의 핵심은 _렌더 스크립트_입니다. 이는 `init()`, `update()`, `on_message()` 함수를 가진 Lua 스크립트이며, 주로 기반 그래픽 API와 상호작용하는 데 사용됩니다. 렌더 스크립트는 게임 라이프사이클에서 특별한 위치를 가집니다. 자세한 내용은 [어플리케이션 라이프사이클 문서](/manuals/application-lifecycle)에서 확인할 수 있습니다.

프로젝트의 "Builtins" 폴더에서 기본 렌더 리소스("default.render")와 기본 렌더 스크립트("default.render_script")를 찾을 수 있습니다.

![Builtin render](images/render/builtin.png)

커스텀 렌더러를 설정하려면:

1. "default.render"와 "default.render_script" 파일을 프로젝트 계층구조의 원하는 위치로 복사합니다. 물론 렌더 스크립트를 처음부터 만들 수도 있지만, Defold나 그래픽 프로그래밍을 처음 다룬다면 기본 스크립트의 복사본에서 시작하는 것이 좋습니다.

2. 복사한 "default.render" 파일을 편집하고 *Script* 프로퍼티를 복사한 렌더 스크립트를 참조하도록 변경합니다.

3. *game.project* 설정 파일의 *bootstrap* 아래에 있는 *Render* 프로퍼티를 복사한 "default.render" 파일을 참조하도록 변경합니다.


## 렌더 predicate {#render-predicates}

오브젝트의 그리기 순서를 제어하려면 렌더 _predicate_를 생성합니다. predicate는 메터리얼 _태그_ 선택을 기준으로 무엇을 그릴지 선언합니다.

화면에 그려지는 각 오브젝트에는 화면에 어떻게 그려질지를 제어하는 메터리얼이 연결되어 있습니다. 메터리얼에서는 해당 메터리얼과 연결할 하나 이상의 _태그_를 지정합니다.

그런 다음 렌더 스크립트에서 *render predicate*를 만들고 어떤 태그가 그 predicate에 속해야 하는지 지정할 수 있습니다. 엔진에 predicate를 그리라고 지시하면, predicate에 지정된 모든 태그를 포함하는 메터리얼을 가진 각 오브젝트가 그려집니다.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- "tree" 태그가 있는 모든 스프라이트와 매칭되는 predicate
local trees = render.predicate({"tree"})
-- Sprite 1, 2, 3을 그림
render.draw(trees)

-- "outlined" 태그가 있는 모든 스프라이트와 매칭되는 predicate
local outlined = render.predicate({"outlined"})
-- Sprite 1, 2, 4를 그림
render.draw(outlined)

-- "outlined"와 "tree" 태그를 모두 가진 모든 스프라이트와 매칭되는 predicate
local outlined_trees = render.predicate({"outlined", "tree"})
-- Sprite 1과 2를 그림
render.draw(outlined_trees)
```


메터리얼이 동작하는 방식에 대한 자세한 설명은 [메터리얼 문서](/manuals/material)에서 확인할 수 있습니다.


## 기본 뷰 투영 {#default-view-projection}

기본 렌더 스크립트는 2D 게임에 적합한 직교 투영(orthographic projection)을 사용하도록 설정되어 있습니다. 이 스크립트는 `Stretch`(기본값), `Fixed Fit`, `Fixed`라는 세 가지 직교 투영을 제공합니다. 기본 렌더 스크립트의 직교 투영 대신 카메라 컴포넌트가 제공하는 투영 매트릭스를 사용할 수도 있습니다.

### Stretch 투영 {#stretch-projection}

Stretch 투영은 창 크기가 변경되더라도 항상 *game.project*에 설정된 치수와 같은 게임 영역을 그립니다. 종횡비가 바뀌면 게임 컨텐츠가 세로 또는 가로로 늘어납니다.

![Stretch projection](images/render/stretch_projection.png)

*원래 창 크기의 Stretch 투영*

![Stretch projection when resized](images/render/stretch_projection_resized.png)

*창을 가로로 늘린 Stretch 투영*

Stretch 투영은 기본 투영입니다. 다른 투영으로 변경한 뒤 다시 돌아와야 한다면 렌더 스크립트에 메세지를 보내 전환합니다.

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Fixed Fit 투영 {#fixed-fit-projection}

Fixed Fit 투영은 Stretch 투영과 마찬가지로 항상 *game.project*에 설정된 치수와 같은 게임 영역을 보여줍니다. 하지만 창 크기가 변경되어 종횡비가 바뀌면 게임 컨텐츠는 원래 종횡비를 유지하고, 세로 또는 가로 방향으로 추가 게임 컨텐츠가 표시됩니다.

![Fixed fit projection](images/render/fixed_fit_projection.png)

*원래 창 크기의 Fixed Fit 투영*

![Fixed fit projection when resized](images/render/fixed_fit_projection_resized.png)

*창을 가로로 늘린 Fixed Fit 투영*

![Fixed fit projection when smaller](images/render/fixed_fit_projection_resized_smaller.png)

*창을 원래 크기의 50%로 줄인 Fixed Fit 투영*

Fixed Fit 투영은 렌더 스크립트에 메세지를 보내 활성화합니다.

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Fixed 투영 {#fixed-projection}

Fixed 투영은 원래 종횡비를 유지하고 고정된 줌 레벨로 게임 컨텐츠를 렌더링합니다. 즉 줌 레벨이 100%가 아닌 값으로 설정되어 있으면 *game.project*의 치수로 정의된 게임 영역보다 더 많거나 더 적은 영역을 보여줍니다.

![Fixed projection](images/render/fixed_projection_zoom_2_0.png)

*줌이 2로 설정된 Fixed 투영*

![Fixed projection](images/render/fixed_projection_zoom_0_5.png)

*줌이 0.5로 설정된 Fixed 투영*

![Fixed projection](images/render/fixed_projection_zoom_2_0_resized.png)

*줌이 2로 설정되고 창이 원래 크기의 50%로 줄어든 Fixed 투영*

Fixed 투영은 렌더 스크립트에 메세지를 보내 활성화합니다.

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### 카메라 투영 {#camera-projection}

기본 렌더 스크립트를 사용할 때 프로젝트에 활성화된 [Camera 컴포넌트](/manuals/camera)가 있으면 렌더 스크립트에 설정된 다른 모든 뷰/투영보다 우선합니다. 렌더 스크립트에서 카메라 컴포넌트를 다루는 방법에 대해 더 알아보려면 [Camera 문서](/manuals/camera)를 참고하세요.

직교 카메라는 창에 맞춰 적응하는 방식을 제어하는 `Orthographic Mode`를 지원합니다.
- `Fixed`는 카메라의 `Orthographic Zoom` 값을 사용합니다.
- `Auto Fit` (contain)은 전체 디자인 영역이 보이도록 유지합니다.
- `Auto Cover` (cover)는 창을 채우며 일부가 잘릴 수 있습니다.

에디터 또는 런타임에 Camera API를 통해 모드를 전환할 수 있습니다.

```lua
-- 직교 카메라에서 auto-fit 동작을 사용
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- 현재 모드 조회
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## 절두체 컬링 {#frustum-culling}

Defold의 render API는 개발자가 절두체 컬링(frustum culling)을 수행할 수 있게 해줍니다. 절두체 컬링이 활성화되면 정의된 바운딩 박스나 절두체 밖에 있는 그래픽은 무시됩니다. 한 번에 일부만 보이는 큰 게임 월드에서는 절두체 컬링을 통해 렌더링을 위해 GPU로 보내야 하는 데이터의 양을 크게 줄일 수 있으므로 성능이 향상되고 배터리도 절약됩니다(모바일 장치의 경우). 바운딩 박스를 만들 때는 카메라의 뷰와 투영을 사용하는 것이 일반적입니다. 기본 렌더 스크립트는 (카메라의) 뷰와 투영을 사용해 절두체를 계산합니다.

절두체 컬링은 엔진에서 컴포넌트 타입별로 구현됩니다. 현재 상태는 다음과 같습니다.

| 컴포넌트 | 지원 여부 |
|-------------|-----------|
| Sprite      | 예        |
| Model       | 예        |
| Mesh        | 예 (1)    |
| Label       | 예        |
| Spine       | 예        |
| Particle fx | 아니요    |
| Tilemap     | 예        |
| Rive        | 아니요    |

1 = Mesh 바운딩 박스는 개발자가 설정해야 합니다. [자세히 알아보기](/manuals/mesh/#frustum-culling).


## 좌표 시스템 {#coordinate-systems}

컴포넌트를 렌더링할 때는 보통 컴포넌트가 어떤 좌표 시스템에서 렌더링되는지 이야기합니다. 대부분의 게임에서는 일부 컴포넌트가 월드 공간에 그려지고 일부는 화면 공간에 그려집니다.

GUI 컴포넌트와 그 노드는 보통 화면 공간 좌표에 그려지며, 화면의 왼쪽 아래 모서리는 좌표 (0,0), 오른쪽 위 모서리는 (화면 너비, 화면 높이)가 됩니다. 화면 공간 좌표 시스템은 카메라에 의해 오프셋되거나 다른 방식으로 이동되지 않습니다. 따라서 월드가 어떻게 렌더링되든 GUI 노드는 항상 화면에 그려집니다.

게임 월드에 존재하는 게임 오브젝트에서 사용하는 스프라이트, 타일맵 및 기타 컴포넌트는 보통 월드 공간 좌표 시스템에 그려집니다. 렌더 스크립트를 수정하지 않고 뷰 투영을 바꾸는 카메라 컴포넌트도 사용하지 않는다면 이 좌표 시스템은 화면 공간 좌표 시스템과 같습니다. 하지만 카메라를 추가해 이동시키거나 뷰 투영을 변경하는 순간 두 좌표 시스템은 달라집니다. 카메라가 움직이면 화면의 왼쪽 아래 모서리가 (0, 0)에서 오프셋되어 월드의 다른 부분이 렌더링됩니다. 투영이 바뀌면 좌표는 이동되고(즉 0, 0에서 오프셋되고) 스케일 계수에 의해 수정됩니다.


## 렌더 스크립트 {#the-render-script}

아래는 내장 렌더 스크립트를 약간 수정한 커스텀 렌더 스크립트의 코드입니다.

init()
: `init()` 함수는 predicate, 뷰, 클리어 컬러를 설정하는 데 사용됩니다. 이 변수들은 실제 렌더링 중에 사용됩니다.

```lua
function init(self)
    -- 렌더 predicate를 정의합니다. 각 predicate는 개별적으로 그려지며
    -- 그리기 사이에 OpenGL 상태를 변경할 수 있습니다.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- update()에서 사용할 데이터 테이블을 생성하고 채웁니다.
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: `update()` 함수는 매 프레임마다 한 번 호출됩니다. 이 함수의 역할은 기반 OpenGL ES API(OpenGL Embedded Systems API)를 호출해 실제 그리기를 수행하는 것입니다. `update()` 함수에서 무슨 일이 일어나는지 제대로 이해하려면 OpenGL이 어떻게 동작하는지 알아야 합니다. OpenGL ES에 대한 훌륭한 자료는 많이 있으며, 공식 사이트가 좋은 출발점입니다. 공식 사이트는 https://www.khronos.org/opengles/ 에 있습니다.

  이 예제에는 3D 모델을 그리는 데 필요한 설정이 포함되어 있습니다. `init()` 함수는 `self.predicates.model` predicate를 정의했습니다. 다른 곳에서는 "model" 태그가 있는 메터리얼이 생성되어 있습니다. 이 메터리얼을 사용하는 모델 컴포넌트도 몇 개 있습니다.

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- 화면 버퍼 지우기
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- 모델 렌더링
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- 월드 렌더링(스프라이트, 타일맵, 파티클 등)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- 디버그
    render.draw_debug3d()

    -- GUI 렌더링
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

여기까지는 단순하고 직관적인 렌더 스크립트입니다. 이 스크립트는 매 프레임마다 같은 방식으로 그립니다. 하지만 렌더 스크립트에 상태를 도입하고 상태에 따라 다른 작업을 수행하고 싶을 때가 있습니다. 게임 코드의 다른 부분에서 렌더 스크립트와 통신하고 싶을 수도 있습니다.

on_message()
: 렌더 스크립트는 `on_message()` 함수를 정의하고 게임이나 앱의 다른 부분에서 메세지를 받을 수 있습니다. 외부 컴포넌트가 렌더 스크립트에 정보를 보내는 일반적인 사례는 _카메라_입니다. 카메라 포커스를 획득한 카메라 컴포넌트는 매 프레임마다 자신의 뷰와 투영을 렌더 스크립트에 자동으로 보냅니다. 이 메세지의 이름은 `"set_view_projection"`입니다.

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- 사용할 새 clear color를 누군가 보냈습니다.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- 카메라 포커스를 가진 카메라 컴포넌트가 @render 소켓으로
        -- set_view_projection 메세지를 보냅니다. 카메라 정보를 사용해
        -- 렌더링의 뷰(그리고 필요한 경우 투영)를 설정할 수 있습니다.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

하지만 어떤 스크립트나 GUI 스크립트도 특수한 `@render` 소켓을 통해 렌더 스크립트에 메세지를 보낼 수 있습니다.

```lua
-- clear color를 변경합니다.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## 렌더 리소스 {#render-resources}

특정 엔진 리소스를 렌더 스크립트로 전달하려면 프로젝트에 지정된 `.render` 파일의 `Render Resources` 테이블에 추가할 수 있습니다.

![Render resources](images/render/render_resources.png)

렌더 스크립트에서 이 리소스를 사용하는 예:

```lua
-- "my_material"은 이제 predicate와 연결된 모든 드로우 콜에 사용됩니다.
render.enable_material("my_material")
-- predicate로 그린 모든 것은 "my_render_target"에 들어갑니다.
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- render target 결과 텍스쳐를 predicate를 통해 렌더링되는 대상에 바인딩합니다.
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
현재 Defold는 참조된 렌더 리소스로 `Materials`와 `Render Targets`만 지원하지만, 시간이 지나면서 이 시스템에서 더 많은 리소스 타입을 지원할 예정입니다.
:::

## 텍스쳐 핸들 {#texture-handles}

Defold에서 텍스쳐는 내부적으로 핸들(handle)로 표현되며, 이는 엔진 어디에서든 텍스쳐 오브젝트를 고유하게 식별해야 하는 숫자와 사실상 같습니다. 즉 렌더 시스템과 게임 오브젝트 스크립트 사이에서 이러한 핸들을 전달하여 게임 오브젝트 쪽과 렌더링 쪽을 연결할 수 있습니다. 예를 들어 스크립트는 게임 오브젝트에 연결된 스크립트에서 동적 텍스쳐를 만들고 이를 렌더러로 보내 그리기 명령의 전역 텍스쳐로 사용할 수 있습니다.

`.script` 파일에서:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- 참고: my_texture_resource는 리소스 경로에 대한 hash이며, 핸들로 사용할 수 없습니다!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle에는 너비, 높이 등 텍스쳐에 대한 정보가 들어 있습니다.
-- 여기에는 필요한 핸들도 들어 있습니다.
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

`.render_script` 파일에서:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- 커스텀 텍스쳐를 그리기 상태에 바인딩합니다.
    render.enable_texture(0, self.my_texture)
    -- 그리기를 수행합니다.
end
```

::: sidenote
현재 리소스가 어떤 텍스쳐를 가리키는지 변경할 방법은 없습니다. 렌더 스크립트에서는 이와 같은 raw 핸들만 사용할 수 있습니다.
:::

## 지원되는 그래픽 API {#supported-graphics-apis}

Defold 렌더 스크립트 API는 렌더링 작업을 다음 그래픽 API로 변환합니다.

:[Graphics API](../shared/graphics-api.md)


## 시스템 메세지 {#system-messages}

`"set_view_projection"`
: 카메라 포커스를 획득한 카메라 컴포넌트가 이 메세지를 보냅니다.

`"window_resized"`
: 엔진은 창 크기가 변경될 때 이 메세지를 보냅니다. 타겟 창 크기가 변경될 때 렌더링을 변경하려면 이 메세지를 수신하면 됩니다. 데스크탑에서는 실제 게임 창의 크기가 변경되었다는 뜻이고, 모바일 장치에서는 방향(orientation)이 바뀔 때마다 이 메세지가 전송됩니다.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- 창 크기가 변경되었습니다. message.width와 message.height에는 새 치수가 들어 있습니다.
    ...
  end
end
```

`"draw_line"`
: 디버그 라인을 그립니다. `ray_casts`, 벡터 등을 시각화하는 데 사용합니다. 선은 `render.draw_debug3d()` 호출로 그려집니다.

```lua
-- 흰색 선을 그립니다.
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )
```

`"draw_text"`
: 디버그 텍스트를 그립니다. 디버그 정보를 출력하는 데 사용합니다. 텍스트는 내장 `always_on_top.font` 폰트로 그려집니다. 시스템 폰트에는 `debug_text` 태그가 있는 메터리얼이 있으며, 기본 렌더 스크립트에서 다른 텍스트와 함께 렌더링됩니다.

```lua
-- 텍스트 메세지를 그립니다.
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })
```

`@system` 소켓으로 `"toggle_profile"` 메세지를 보내 접근할 수 있는 비주얼 프로파일러(visual profiler)는 스크립트로 제어 가능한 렌더러의 일부가 아닙니다. 이 프로파일러는 렌더 스크립트와 별도로 그려집니다.


## 드로우 콜과 배치 {#draw-calls-and-batching}

드로우 콜은 텍스쳐와 메터리얼, 그리고 선택적인 추가 설정을 사용해 오브젝트를 화면에 그리도록 GPU를 설정하는 과정을 설명하는 용어입니다. 이 과정은 보통 리소스를 많이 사용하므로 드로우 콜 수를 가능한 한 적게 유지하는 것이 좋습니다. [내장 프로파일러](/manuals/profiling/)를 사용하면 드로우 콜 수와 렌더링에 걸리는 시간을 측정할 수 있습니다.

Defold는 아래에 정의된 규칙에 따라 렌더링 작업을 배치로 묶어 드로우 콜 수를 줄이려고 합니다. 이 규칙은 GUI 컴포넌트와 다른 모든 컴포넌트 타입 사이에서 다릅니다.


### 비 GUI 컴포넌트의 배치 규칙 {#batch-rules-for-non-gui-components}

렌더링은 낮은 값에서 높은 값으로 이어지는 z 순서를 기준으로 수행됩니다. 엔진은 그릴 항목 목록을 먼저 정렬한 뒤 낮은 z 값에서 높은 z 값으로 순회합니다. 목록의 각 오브젝트는 다음 조건을 만족하면 이전 오브젝트와 같은 드로우 콜로 그룹화됩니다.

* 같은 컬렉션 프록시(Collection proxy)에 속함
* 같은 컴포넌트 타입(sprite, particle fx, tilemap 등)임
* 같은 텍스쳐(atlas 또는 tile source)를 사용함
* 같은 메터리얼을 사용함
* 같은 쉐이더 상수(`tint` 등)를 가짐

즉 같은 컬렉션 프록시에 있는 두 스프라이트 컴포넌트가 인접한 z 값 또는 같은 z 값을 가져 정렬된 목록에서 서로 나란히 오고, 같은 텍스쳐, 메터리얼, 상수를 사용한다면 같은 드로우 콜로 그룹화됩니다.


### GUI 컴포넌트의 배치 규칙 {#batch-rules-for-gui-components}

GUI 컴포넌트의 노드 렌더링은 노드 목록의 위에서 아래 순서로 수행됩니다. 목록의 각 노드는 다음 조건을 만족하면 이전 노드와 같은 드로우 콜로 그룹화됩니다.

* 같은 타입(box, text, pie 등)임
* 같은 텍스쳐(atlas 또는 tile source)를 사용함
* 같은 블렌드 모드를 가짐
* 같은 폰트를 가짐(텍스트 노드에만 해당)
* 같은 스텐실 설정을 가짐

::: sidenote
노드 렌더링은 컴포넌트별로 수행됩니다. 따라서 서로 다른 GUI 컴포넌트의 노드는 배치되지 않습니다.
:::

노드를 계층구조로 정렬할 수 있으면 노드를 관리 가능한 단위로 쉽게 그룹화할 수 있습니다. 하지만 서로 다른 노드 타입을 섞으면 계층구조가 배치 렌더링을 효과적으로 끊을 수 있습니다. GUI 레이어를 사용하면 노드 계층구조를 유지하면서 GUI 노드를 더 효율적으로 배치할 수 있습니다. GUI 레이어와 이들이 드로우 콜에 미치는 영향에 대한 자세한 내용은 [GUI 매뉴얼](/manuals/gui#layers-and-draw-calls)을 참고하세요.
