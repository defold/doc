---
title: 컬러 그레이딩 쉐이더 튜토리얼
brief: 이 튜토리얼에서는 Defold에서 전체 화면 포스트 이펙트를 만듭니다.
---

# 컬러 그레이딩 튜토리얼

이 튜토리얼에서는 컬러 그레이딩 전체 화면 포스트 이펙트를 만들어 보겠습니다. 여기서 사용하는 기본 렌더링 방식은 블러, 잔상, 글로우, 색상 조정 등 다양한 포스트 이펙트에 폭넓게 적용할 수 있습니다.

Defold 에디터 사용법을 알고 있으며, GL 쉐이더와 Defold 렌더링 파이프라인을 기본적으로 이해하고 있다고 가정합니다. 이 주제들을 더 읽어야 한다면 [Shader 매뉴얼](/manuals/shader/)과 [Render 매뉴얼](/manuals/render/)을 확인하세요.

## 렌더 타겟

기본 렌더 스크립트를 사용하면 각 시각 컴포넌트(스프라이트, 타일맵, 파티클 효과, GUI 등)는 그래픽 카드의 *frame buffer*에 직접 렌더링됩니다. 그러면 하드웨어가 그래픽을 화면에 표시합니다. 컴포넌트 픽셀을 실제로 그리는 일은 GL *쉐이더 프로그램*이 수행합니다. Defold에는 각 컴포넌트 타입의 픽셀 데이터를 변경 없이 화면에 그리는 기본 쉐이더 프로그램이 포함되어 있습니다. 일반적으로 이것이 원하는 동작입니다. 이미지는 원래 의도한 모습 그대로 화면에 표시되어야 합니다.

컴포넌트의 쉐이더 프로그램을 픽셀 데이터를 수정하거나 완전히 새로운 픽셀 색상을 프로그래밍 방식으로 만드는 쉐이더 프로그램으로 교체할 수 있습니다. [Shadertoy 튜토리얼](/tutorials/shadertoy)에서 그 방법을 배울 수 있습니다.

이제 게임 전체를 흑백으로 렌더링하고 싶다고 해 봅시다. 가능한 한 가지 해결책은 각 컴포넌트 타입의 개별 쉐이더 프로그램을 수정하여 각 쉐이더가 픽셀 색상의 채도를 낮추게 하는 것입니다. 현재 Defold에는 6개의 내장 메터리얼과 6쌍의 버텍스 및 프래그먼트 쉐이더 프로그램이 포함되어 있으므로 꽤 많은 작업이 필요합니다. 게다가 이후 변경이나 효과 추가도 각 쉐이더 프로그램마다 적용해야 합니다.

훨씬 더 유연한 방식은 렌더링을 두 개의 별도 단계로 나누는 것입니다.

![렌더 타겟](images/grading/render_target.png)

1. 모든 컴포넌트를 평소처럼 그리되, 일반 frame buffer 대신 오프스크린 버퍼에 그립니다. 이를 위해 *렌더 타겟*이라는 것에 그립니다.
2. frame buffer에 정사각형 폴리곤을 그리고, 렌더 타겟에 저장된 픽셀 데이터를 그 폴리곤의 텍스쳐 소스로 사용합니다. 또한 정사각형 폴리곤이 전체 화면을 덮도록 늘립니다.

이 방법을 사용하면 결과 시각 데이터를 화면에 도달하기 전에 읽고 수정할 수 있습니다. 위의 2단계에 쉐이더 프로그램을 추가하면 전체 화면 이펙트를 쉽게 만들 수 있습니다. Defold에서 이를 어떻게 설정하는지 살펴보겠습니다.

## 커스텀 렌더러 설정

내장 렌더 스크립트를 수정하고 새 렌더링 기능을 추가해야 합니다. 기본 렌더 스크립트가 좋은 시작점이므로 먼저 복사합니다.

1. */builtins/render/default.render_script*를 복사합니다. *Asset* 뷰에서 *default.render_script*를 오른쪽 클릭하고 <kbd>Copy</kbd>를 선택한 다음, *main*을 오른쪽 클릭하고 <kbd>Paste</kbd>를 선택합니다. 복사본을 오른쪽 클릭하고 <kbd>Rename...</kbd>을 선택한 뒤 "grade.render_script" 같은 적절한 이름을 붙입니다.
2. *Asset* 뷰에서 *main*을 오른쪽 클릭하고 <kbd>New ▸ Render</kbd>를 선택하여 */main/grade.render*라는 새 render 파일을 만듭니다.
3. *grade.render*를 열고 *Script* 프로퍼티를 "/main/grade.render_script"로 설정합니다.

   ![grade.render](images/grading/grade_render.png)

4. *game.project*를 열고 *Render*를 "/main/grade.render"로 설정합니다.

   ![game.project](images/grading/game_project.png)

이제 수정할 수 있는 새 렌더 파이프라인으로 게임을 실행하도록 설정되었습니다. 렌더 스크립트 복사본이 엔진에서 사용되는지 테스트하려면 게임을 실행한 뒤, 시각적으로 결과가 나타나는 변경을 렌더 스크립트에 적용하고 스크립트를 다시 로드합니다. 예를 들어 타일과 스프라이트 그리기를 비활성화한 다음 <kbd>⌘ + R</kbd>을 눌러 "깨진" 렌더 스크립트를 실행 중인 게임에 핫 리로드할 수 있습니다.

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. 모든 스프라이트와 타일을 포함하는 "tile" predicate의 그리기를 주석 처리합니다. 이 코드 줄은 렌더 스크립트 파일의 33번째 줄 근처에서 찾을 수 있습니다.

이 간단한 테스트로 스프라이트와 타일이 사라진다면 게임이 해당 렌더 스크립트를 실행하고 있다는 뜻입니다. 모든 것이 예상대로 동작하면 렌더 스크립트 변경을 되돌릴 수 있습니다.

## 오프스크린 타겟에 그리기

이제 frame buffer 대신 오프스크린 렌더 타겟에 그리도록 렌더 스크립트를 수정하겠습니다. 먼저 렌더 타겟을 만들어야 합니다.

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 0)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 0)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[render.BUFFER_COLOR_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. 렌더 타겟의 color buffer 파라미터를 설정합니다. 게임의 타겟 해상도를 사용합니다.
2. color buffer 파라미터로 렌더 타겟을 생성합니다.

이제 원래 렌더링 코드를 다음과 같이 `render.set_render_target()`으로 감싸기만 하면 됩니다.

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color, [render.BUFFER_DEPTH_BIT] = 1, [render.BUFFER_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. 렌더 타겟을 활성화합니다. 이제부터 `render.draw()` 호출은 모두 우리의 오프스크린 렌더 타겟 버퍼에 그립니다.
2. `update()`의 원래 그리기 코드는 렌더 타겟 해상도로 설정되는 뷰포트를 제외하면 그대로 둡니다.
3. 이 시점에서는 게임의 모든 그래픽이 렌더 타겟에 그려졌습니다. 따라서 기본 렌더 타겟으로 설정하여 렌더 타겟을 비활성화할 차례입니다.

필요한 작업은 이것이 전부입니다. 이제 게임을 실행하면 모든 것이 렌더 타겟에 그려집니다. 하지만 현재 frame-buffer에는 아무것도 그리지 않으므로 검은 화면만 보입니다.

## 화면을 채울 무언가

렌더 타겟의 color buffer에 있는 픽셀을 화면에 그리려면 픽셀 데이터로 텍스쳐링할 수 있는 대상을 설정해야 합니다. 이를 위해 평평한 정사각형 3D 모델을 사용하겠습니다.

1. *`main.collection`*을 열고 "`grade`"라는 새 게임 오브젝트를 만듭니다.
2. "`grade`" 게임 오브젝트에 Model 컴포넌트를 추가합니다.
3. 모델 컴포넌트의 *Mesh* 프로퍼티를 `builtins/assets/meshes`에 있는 *`quad.gltf`* 파일로 설정합니다.

게임 오브젝트는 원점에 스케일 변경 없이 둡니다. 나중에 quad를 렌더링할 때 전체 화면을 채우도록 투영할 것입니다. 하지만 먼저 quad에 사용할 메터리얼과 쉐이더 프로그램이 필요합니다.

1. *Asset* 뷰에서 *main*을 오른쪽 클릭하고 <kbd>New ▸ Material</kbd>을 선택하여 새 메터리얼을 만들고 *`grade.material`*이라고 이름 붙입니다.
2. *Asset* 뷰에서 *main*을 오른쪽 클릭하고 <kbd>New ▸ Vertex program</kbd>과 <kbd>New ▸ Fragment program</kbd>을 선택하여 *`grade.vp`*라는 버텍스 쉐이더 프로그램과 *`grade.fp`*라는 프래그먼트 쉐이더 프로그램을 만듭니다.
3. *grade.material*을 열고 *Vertex program* 및 *Fragment program* 프로퍼티를 새 쉐이더 프로그램 파일로 설정합니다.
4. `CONSTANT_TYPE_VIEWPROJ` 타입의 "`view_proj`"라는 *Vertex constant*를 추가합니다. 이것은 quad 버텍스에 대한 버텍스 프로그램에서 사용하는 뷰 및 프로젝션 메트릭스입니다.
5. "`original`"이라는 *Sampler*를 추가합니다. 오프스크린 렌더 타겟 color buffer에서 픽셀을 샘플링하는 데 사용됩니다.
6. "`grade`"라는 *Tag*를 추가합니다. 렌더 스크립트에서 이 태그와 일치하는 새 *render predicate*를 만들어 quad를 그릴 것입니다.

   ![grade.material](images/grading/grade_material.png)

7. *`main.collection`*을 열고 "`grade`" 게임 오브젝트의 모델 컴포넌트를 선택한 뒤 *Material* 프로퍼티를 "`/main/grade.material`"로 설정합니다.

   ![model properties](images/grading/model_properties.png)

8. 버텍스 쉐이더 프로그램은 기본 템플릿에서 생성된 상태 그대로 둘 수 있습니다.

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // 포지션은 월드 공간에 있습니다
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. 프래그먼트 쉐이더 프로그램에서는 `gl_FragColor`를 샘플링한 색상 값으로 직접 설정하는 대신 간단한 색상 조작을 수행해 보겠습니다. 이는 지금까지 모든 것이 예상대로 동작하는지 확인하기 위한 것입니다.

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // original 텍스쳐에서 샘플링한 색상의 채도를 낮춥니다
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

이제 quad 모델, 메터리얼, 쉐이더가 준비되었습니다. 남은 일은 이것을 화면 frame buffer에 그리는 것입니다.

## 오프스크린 버퍼로 텍스쳐링하기

quad 모델을 그릴 수 있도록 렌더 스크립트에 렌더 predicate를 추가해야 합니다. *`grade.render_script`*를 열고 `init()` 함수를 편집합니다.

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. *`grade.material`*에 설정한 "grade" 태그와 일치하는 새 predicate를 추가합니다.

`update()`에서 렌더 타겟의 color buffer가 채워진 뒤, quad 모델이 전체 화면을 채우도록 만드는 뷰와 projection을 설정합니다. 그런 다음 렌더 타겟의 color buffer를 quad의 텍스쳐로 사용합니다.

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, render.BUFFER_COLOR_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. frame buffer를 지웁니다. 이전 `render.clear()` 호출은 화면 frame buffer가 아니라 렌더 타겟에 영향을 준다는 점에 유의하세요.
2. 뷰포트를 창 크기에 맞게 설정합니다.
3. 뷰를 identity matrix로 설정합니다. 이는 카메라가 원점에 있고 Z축을 따라 정면을 바라본다는 의미입니다. 또한 projection을 identity matrix로 설정하여 quad가 전체 화면에 평평하게 투영되도록 합니다.
4. 텍스쳐 슬롯 0을 렌더 타겟의 color buffer로 설정합니다. *`grade.material`*의 슬롯 0에 "original" 샘플러가 있으므로 프래그먼트 쉐이더는 렌더 타겟에서 샘플링합니다.
5. "grade" 태그가 있는 모든 메터리얼과 일치하도록 만든 predicate를 그립니다. quad 모델은 해당 태그를 설정하는 *`grade.material`*을 사용하므로 quad가 그려집니다.
6. 그리기가 끝났으므로 텍스쳐 슬롯 0을 비활성화합니다.

이제 게임을 실행하고 결과를 확인해 보겠습니다.

![채도가 낮아진 게임](images/grading/desaturated_game.png)

## 컬러 그레이딩

색상은 세 개의 컴포넌트 값으로 표현되며, 각 컴포넌트는 색상에 포함되는 빨강, 초록, 파랑(red, green, blue)의 양을 결정합니다. 검정에서 시작해 빨강, 초록, 파랑, 노랑, 분홍을 거쳐 흰색까지 이어지는 전체 색상 스펙트럼은 큐브 모양에 들어맞을 수 있습니다.

![색상 큐브](images/grading/color_cube.png)

화면에 표시할 수 있는 모든 색상은 이 색상 큐브 안에서 찾을 수 있습니다. 컬러 그레이딩의 기본 아이디어는 이렇게 생긴 색상 큐브를 사용하되, 색상을 변경한 큐브를 3D *룩업 테이블(lookup table)*로 사용하는 것입니다.

각 픽셀에 대해:

1. 색상 큐브에서 픽셀 색상의 위치를 찾습니다(빨강, 초록, 파랑 값 기준).
2. 그 위치에 그레이딩된 큐브가 저장한 색상을 *읽습니다*.
3. 원래 색상 대신 읽은 색상으로 픽셀을 그립니다.

프래그먼트 쉐이더에서 이를 수행할 수 있습니다.

1. 오프스크린 버퍼의 각 픽셀 색상 값을 샘플링합니다.
2. 샘플링한 픽셀의 색상 위치를 컬러 그레이딩된 색상 큐브에서 찾습니다.
3. 출력 프래그먼트 색상을 조회한 값으로 설정합니다.

![렌더 타겟 그레이딩](images/grading/render_target_grading.png)

## 룩업 테이블 표현하기

OpenGL ES 2.0은 3D 텍스쳐를 지원하지 않으므로 3D 색상 큐브를 표현할 다른 방법을 찾아야 합니다. 일반적인 방법은 큐브를 Z축(파랑)을 따라 자르고 각 slice를 2차원 그리드에 나란히 배치하는 것입니다. 16개의 slice는 각각 16⨉16 픽셀 그리드를 포함합니다. 이를 텍스쳐에 저장하면 프래그먼트 쉐이더에서 샘플러로 읽을 수 있습니다.

![룩업 텍스쳐](images/grading/lut.png)

결과 텍스쳐에는 16개의 셀(파란색 강도마다 하나씩)이 들어 있으며, 각 셀 안에는 X축을 따라 16개의 빨간색과 Y축을 따라 16개의 초록색이 있습니다. 이 텍스쳐는 전체 1,600만 색상 RGB 색공간을 단 4096개 색상으로 표현합니다. 즉 색상 깊이가 겨우 4비트입니다. 대부분의 기준에서는 형편없지만, GL 그래픽 하드웨어의 기능 덕분에 매우 높은 색상 정확도를 되찾을 수 있습니다. 어떻게 가능한지 살펴보겠습니다.

## 색상 조회하기

색상을 조회한다는 것은 파란색 컴포넌트를 확인하고, 어느 셀에서 빨강과 초록 값을 가져올지 알아내는 일입니다. 올바른 빨강-초록 색상 집합이 있는 셀을 찾는 공식은 간단합니다.

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

여기서 `B`는 0과 1 사이의 파란색 컴포넌트 값이고 `N`은 전체 셀 수입니다. 이 경우 셀 번호는 `0`--`15` 범위가 되며, 셀 `0`은 파란색 컴포넌트가 `0`인 모든 색상을 포함하고 셀 `15`는 파란색 컴포넌트가 `1`인 모든 색상을 포함합니다.

예를 들어 RGB 값 `(0.63, 0.83, 0.4)`는 파란색 값이 `0.4`인 모든 색상을 포함하는 셀에서 찾을 수 있으며, 이 셀은 번호 6입니다. 이를 알면 초록과 빨강 값을 바탕으로 최종 텍스쳐 좌표를 조회하는 일은 단순합니다.

![룩업 테이블](images/grading/lut_lookup.png)

빨강과 초록 값 `(0, 0)`은 왼쪽 아래 픽셀의 *중심*에 있고, `(1.0, 1.0)` 값은 오른쪽 위 픽셀의 *중심*에 있는 것으로 처리해야 한다는 점에 유의하세요.

::: sidenote
왼쪽 아래 픽셀의 중심에서 시작해 오른쪽 위 픽셀의 중심까지 읽는 이유는 현재 셀 바깥의 픽셀이 샘플링 값에 영향을 주지 않게 하기 위해서입니다. 필터링에 대해서는 아래를 참조하세요.
:::

텍스쳐의 이 특정 좌표에서 샘플링하면 결국 4개 픽셀의 바로 중간에 놓입니다. 그렇다면 GL은 그 지점의 색상 값을 무엇이라고 알려줄까요?

![룩업 테이블 필터링](images/grading/lut_filtering.png)

답은 메터리얼에서 샘플러의 *필터링(filtering)*을 어떻게 지정했는지에 따라 달라집니다.

- 샘플러 필터링이 `NEAREST`이면 GL은 가장 가까운 픽셀 값의 색상 값을 반환합니다(위치 값은 내림 처리). 위의 경우 GL은 위치 `(0.60, 0.80)`의 색상 값을 반환합니다. 4비트 룩업 텍스쳐에서는 전체 색상 값을 총 4096개 색상으로만 양자화한다는 뜻입니다.

- 샘플러 필터링이 `LINEAR`이면 GL은 *보간된* 색상 값을 반환합니다. GL은 샘플 위치 주변 픽셀까지의 거리를 바탕으로 색상을 혼합합니다. 위의 경우 GL은 샘플 지점 주변 4개 픽셀 각각을 25%씩 반영한 색상을 반환합니다.

따라서 linear 필터링을 사용하면 색상 양자화를 제거하고 꽤 작은 룩업 테이블에서도 매우 좋은 색상 정밀도를 얻을 수 있습니다.

## 조회 구현하기

프래그먼트 쉐이더에 텍스쳐 조회를 구현해 보겠습니다.

1. *`grade.material`*을 엽니다.
2. "`lut`"라는 두 번째 샘플러를 추가합니다(룩업 테이블용).
3. *`Filter min`* 프로퍼티를 `FILTER_MODE_MIN_LINEAR`로 설정하고 *`Filter mag`* 프로퍼티를 `FILTER_MODE_MAG_LINEAR`로 설정합니다.

    ![룩업 테이블 샘플러](images/grading/material_lut_sampler.png)

4. 다음 룩업 테이블 텍스쳐(*`lut16.png`*)를 다운로드하여 프로젝트에 추가합니다.

    ![16색 룩업 테이블](images/grading/lut16.png)

5. *`main.collection`*을 열고 *`lut`* 텍스쳐 프로퍼티를 다운로드한 룩업 텍스쳐로 설정합니다.

    ![quad 모델 룩업 테이블](images/grading/quad_lut.png)

6. 마지막으로 컬러 조회 지원을 추가할 수 있도록 *`grade.fp`*를 엽니다.

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. 샘플러 `lut`를 선언합니다.
    2. 최대 색상(0부터 시작하므로 15), 채널당 색상 수, 룩업 텍스쳐 너비와 높이에 대한 상수입니다.
    3. original 텍스쳐(오프스크린 렌더 타겟 color buffer)에서 픽셀 색상(`px`)을 샘플링합니다.
    4. `px`의 파란색 채널 값을 바탕으로 어느 셀에서 색상을 읽을지 계산합니다.
    5. 픽셀 중심에서 읽을 수 있도록 반 픽셀 오프셋을 계산합니다.
    6. `px`의 빨강 및 초록 값을 바탕으로 텍스쳐의 X 및 Y 오프셋을 계산합니다.
    7. 룩업 텍스쳐의 최종 샘플 위치를 계산합니다.
    8. 룩업 텍스쳐에서 결과 색상을 샘플링합니다.
    9. quad의 텍스쳐 색상을 결과 색상으로 설정합니다.

현재 룩업 테이블 텍스쳐는 조회한 것과 같은 색상 값만 반환합니다. 즉 게임은 원래 색상으로 렌더링되어야 합니다.

![원래 모습의 월드](images/grading/world_original.png)

지금까지는 모든 것을 올바르게 처리한 것처럼 보이지만, 표면 아래에 문제가 숨어 있습니다. 그라디언트 테스트 텍스쳐가 있는 스프라이트를 추가하면 어떤 일이 일어나는지 보세요.

![파란색 밴딩](images/grading/blue_banding.png)

파란색 그라디언트에 매우 보기 좋지 않은 밴딩(banding)이 나타납니다. 왜 그럴까요?

## 파란색 채널 보간하기

파란색 채널에 밴딩이 생기는 문제는 GL이 텍스쳐에서 색상을 읽을 때 파란색 채널 보간을 수행할 수 없다는 데 있습니다. 파란색 값을 기준으로 읽을 특정 셀을 미리 선택하고, 거기서 끝입니다. 예를 들어 파란색 채널에 `0.400`--`0.466` 범위의 어느 값이 들어 있더라도 그 값은 중요하지 않습니다. 항상 파란색 채널이 `0.400`으로 설정된 셀 번호 6에서 최종 색상을 샘플링하기 때문입니다.

파란색 채널 해상도를 높이려면 보간을 직접 구현할 수 있습니다. 파란색 값이 인접한 두 셀의 값 사이에 있으면 두 셀 모두에서 샘플링한 다음 색상을 혼합할 수 있습니다. 예를 들어 파란색 값이 `0.420`이면 셀 번호 6 *및* 셀 번호 7에서 샘플링한 다음 색상을 혼합해야 합니다.

따라서 두 셀에서 읽어야 합니다.

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

그리고:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

그런 다음 각 셀에서 색상 값을 샘플링하고, 다음 공식에 따라 색상을 선형으로 보간합니다.

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

여기서 `color`~low~는 낮은 쪽(가장 왼쪽) 셀에서 샘플링한 색상이고 `color`~high~는 높은 쪽(가장 오른쪽) 셀에서 샘플링한 색상입니다. GLSL 함수 `mix()`가 이 선형 보간을 대신 수행해 줍니다.

위의 `C~frac~` 값은 파란색 채널 값을 `0`--`15` 색상 범위로 스케일한 값의 소수 부분입니다.

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

마찬가지로 값의 소수 부분을 알려주는 GLSL 함수가 있습니다. 그 함수는 `frac()`입니다. 프래그먼트 쉐이더(*`grade.fp`*)의 최종 구현은 꽤 간단합니다.

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. 읽을 인접한 두 셀을 계산합니다.
2. 각 셀에 대해 별도의 룩업 위치 두 개를 계산합니다.
3. 셀 위치에서 두 색상을 샘플링합니다.
3. 스케일된 파란색 값인 `cell`의 소수 부분에 따라 색상을 선형으로 혼합합니다.

테스트 텍스쳐를 사용해 게임을 다시 실행하면 이제 훨씬 더 나은 결과가 나옵니다. 파란색 채널의 밴딩이 사라졌습니다.

![밴딩이 없는 파란색](images/grading/blue_no_banding.png)

## 룩업 텍스쳐 그레이딩하기

좋습니다. 원래 게임 월드와 똑같아 보이는 것을 그리기 위해 꽤 많은 작업을 했습니다. 하지만 이 설정을 사용하면 정말 멋진 일을 할 수 있습니다. 이제부터입니다!

1. 영향이 적용되지 않은 원래 형태의 게임 스크린샷을 찍습니다.
2. 선호하는 이미지 편집 프로그램에서 스크린샷을 엽니다.
3. 원하는 수의 색상 조정(brightness, contrast, color curves, white balance, exposure 등)을 적용합니다.

![Affinity의 월드](images/grading/world_graded_affinity.png)

4. 룩업 테이블 텍스쳐 파일(*`lut16.png`*)에 같은 색상 조정을 적용합니다.
5. 색상 조정된 룩업 테이블 텍스쳐 파일을 저장합니다.
6. Defold 프로젝트에서 사용하는 텍스쳐 *`lut16.png`*를 색상 조정된 파일로 교체합니다.
7. 게임을 실행합니다!

![그레이딩된 월드](images/grading/world_graded.png)

즐겨 보세요!
