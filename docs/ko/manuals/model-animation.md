---
title: Defold의 3D 모델 애니메이션 매뉴얼
brief: 이 매뉴얼은 Defold에서 3D 모델 애니메이션을 사용하는 방법을 설명합니다.
---

# 3D 모델 애니메이션

모델 컴포넌트는 glTF 파일에서 임포트한 스켈레탈 애니메이션과 morph target 애니메이션을 재생할 수 있습니다. 스켈레탈 애니메이션은 모델의 본(bone)을 사용해 모델의 버텍스에 변형을 적용합니다. blend shape 애니메이션이라고도 하는 morph target 애니메이션은 대체 버텍스 포지션에 대한 weight를 애니메이션하여 모델의 형태를 변경합니다.

애니메이션을 위해 3D 데이터를 Model로 임포트하는 방법에 대한 자세한 내용은 [모델 문서](/manuals/model)를 참고하세요.

  ![Blender 애니메이션](images/animation/blender_animation.png)
  ![Wiggle 루프](images/animation/suzanne.gif)


## 애니메이션 재생하기

모델은 [`model.play_anim()`](/ref/model#model.play_anim) 함수로 애니메이션됩니다:

```lua
function init(self)
    -- #model에서 "wiggle" 애니메이션을 앞뒤로 시작합니다
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold는 현재 베이크된 스켈레탈 애니메이션만 지원합니다. 스켈레탈 애니메이션에는 포지션, 회전, 스케일이 별도 키로 있는 것이 아니라, 애니메이션되는 각 본의 각 키프레임마다 매트릭스가 있어야 합니다.

애니메이션도 선형 보간됩니다. 더 고급 곡선 보간을 사용한다면 애니메이션을 익스포터에서 미리 베이크해야 합니다.
:::

### Morph targets

Morph target은 같은 메쉬의 대체 형태입니다. 각 target은 position, normal, tangent 델타를 저장하며, 각 target에는 해당 형태가 얼마나 적용되는지 제어하는 blend weight가 있습니다. weight가 `0`이면 target이 아무 효과도 주지 않으며, weight가 `1`이면 target 형태 전체가 적용됩니다. 쉐이더와 에셋이 이를 고려해 작성되어 있다면 이 범위를 벗어나는 값도 과장된 효과에 유용할 수 있습니다.

Defold는 glTF 모델 데이터에서 morph target과 초기 morph weight를 임포트합니다. morph weight를 애니메이션하는 glTF 애니메이션은 모델 애니메이션 세트로 임포트되며, 스켈레탈 애니메이션처럼 [`model.play_anim()`](/ref/model#model.play_anim)으로 재생할 수 있습니다:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Morph target 데이터는 단독으로 사용할 수도 있고 스켈레탈 애니메이션과 함께 사용할 수도 있지만, 모델 컴포넌트는 한 번에 하나의 모델 애니메이션만 재생할 수 있습니다. 즉 `model.play_anim()`을 사용해 하나의 스켈레탈 애니메이션과 별도의 morph target 애니메이션 하나를 동시에 재생할 수는 없습니다. 모델에 애니메이션 데이터는 있지만 스켈레톤이 없다면 morph target 애니메이션 데이터만 사용됩니다.

그래도 스크립트에서 `model.set_blend_weights()`로 morph target weight를 설정하는 방식처럼, 다른 소스에서 오는 morph target 변경과 스켈레탈 애니메이션 재생을 결합할 수 있습니다.

스크립트에서 morph target weight를 읽고 오버라이드할 수도 있습니다. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights)는 모델에서 morph target이 있는 첫 번째 메쉬의 현재 weight를 반환합니다. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights)는 모델 안의 모든 morphed 메쉬에 스크립트 오버라이드를 적용합니다:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

weight 테이블은 메쉬의 morph target과 같은 순서로 1부터 시작하는 Lua 인덱스를 사용합니다. 추가 값은 무시되고, 테이블에 들어 있는 값보다 morph target이 더 많은 메쉬에서는 누락된 값이 0으로 처리됩니다. 스크립트 오버라이드는 해제될 때까지 매 프레임 애니메이션 뒤에 적용됩니다:

```lua
model.set_blend_weights("#model")     -- 오버라이드를 해제합니다
model.set_blend_weights("#model", nil) -- 이 방법도 오버라이드를 해제합니다
```

### 쉐이더 지원

morph target을 렌더링하려면 모델 메터리얼의 버텍스 쉐이더가 생성된 `morph_targets` 텍스쳐를 샘플링하고, 가중치가 적용된 델타를 버텍스 데이터에 적용해야 합니다. morph target 텍스쳐는 2D array texture이며, 각 morph target은 position delta, normal delta, tangent delta라는 세 개의 array layer를 사용합니다.

엔진은 현재 morph weight를 `morph_targets_weights`라는 이름의 버텍스 쉐이더 uniform에 제공합니다. 각 `vec4`는 weight 네 개를 저장하므로, `morph_targets_weights[2]`에는 morph target 여덟 개를 위한 공간이 있습니다.

다음 예제는 인스턴싱되지 않은 모델 메터리얼에서 관련된 버텍스 쉐이더 부분을 보여줍니다:

```glsl
#version 140

in highp vec4 position;
in mediump vec2 texcoord0;
in mediump vec3 normal;
in mediump vec4 tangent;

out mediump vec2 var_texcoord0;
out mediump vec3 var_normal;
out mediump vec4 var_tangent;

uniform vs_uniforms
{
    mediump mat4 mtx_worldview;
    mediump mat4 mtx_proj;
    mediump mat4 mtx_normal;
    // 각 vec4는 blend weight 네 개를 저장합니다. morph target이 최대 4개라면
    // morph_targets_weights[1]을, 최대 8개라면 [2]를, 최대 12개라면 [3]을 사용하는 식입니다.
    mediump vec4 morph_targets_weights[2];
};

uniform sampler2DArray morph_targets;

vec2 get_morph_uv(int vertex_index, int width, int height)
{
    int x = vertex_index % width;
    int y = vertex_index / width;
    return vec2(
        (float(x) + 0.5) / float(width),
        (float(y) + 0.5) / float(height)
    );
}

void apply_morph_target(vec2 uv, float weight, int target,
    inout vec3 position_delta, inout vec3 normal_delta, inout vec3 tangent_delta)
{
    if (weight == 0.0) {
        return;
    }

    int position_layer = target * 3 + 0;
    int normal_layer = target * 3 + 1;
    int tangent_layer = target * 3 + 2;

    position_delta += weight * texture(morph_targets, vec3(uv, position_layer)).xyz;
    normal_delta += weight * texture(morph_targets, vec3(uv, normal_layer)).xyz;
    tangent_delta += weight * texture(morph_targets, vec3(uv, tangent_layer)).xyz;
}

void get_morph_target_data(int vertex_index,
    out vec3 position_delta, out vec3 normal_delta, out vec3 tangent_delta)
{
    position_delta = vec3(0.0);
    normal_delta = vec3(0.0);
    tangent_delta = vec3(0.0);

#ifndef EDITOR
    ivec3 texture_size = textureSize(morph_targets, 0);
    vec2 uv = get_morph_uv(vertex_index, texture_size.x, texture_size.y);

    apply_morph_target(uv, morph_targets_weights[0].x, 0, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].y, 1, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].z, 2, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].w, 3, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].x, 4, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].y, 5, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].z, 6, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].w, 7, position_delta, normal_delta, tangent_delta);
#endif
}

void main()
{
    vec3 position_delta;
    vec3 normal_delta;
    vec3 tangent_delta;
    get_morph_target_data(gl_VertexIndex, position_delta, normal_delta, tangent_delta);

    vec3 morphed_position = position.xyz + position_delta;
    vec3 morphed_normal = normalize(normal + normal_delta);
    vec3 morphed_tangent = normalize(tangent.xyz + tangent_delta);

    var_texcoord0 = texcoord0;
    var_normal = normalize((mtx_normal * vec4(morphed_normal, 0.0)).xyz);
    var_tangent = vec4(normalize((mtx_normal * vec4(morphed_tangent, 0.0)).xyz), tangent.w);

    gl_Position = mtx_proj * mtx_worldview * vec4(morphed_position, 1.0);
}
```

`#ifndef EDITOR` 래퍼가 필요한 이유는 모델 애니메이션 미리보기가 아직 에디터에서 제공되지 않아, 생성된 morph target 텍스쳐 데이터를 런타임에만 사용할 수 있기 때문입니다. 메쉬에 morph target이 더 많다면 `morph_targets_weights` 배열 크기를 늘리고 `apply_morph_target()` 호출을 더 추가하세요.

::: important
위 쉐이더 예제는 `textureSize()`를 사용하므로 OpenGL ES 2.0에서는 동작하지 않습니다.
:::

### 본 계층구조

Model 스켈레톤의 본은 내부적으로 게임 오브젝트로 표현됩니다.

런타임에 본 게임 오브젝트의 인스턴스 id를 가져올 수 있습니다. [`model.get_go()`](/ref/model#model.get_go) 함수는 지정한 본에 대한 게임 오브젝트의 id를 반환합니다.

```lua
-- wiggler 모델의 가운데 본 게임 오브젝트를 가져옵니다
local bone_go = model.get_go("#wiggler", "Bone_002")

-- 이제 이 게임 오브젝트로 유용한 작업을 수행합니다...
```

### 커서 애니메이션

모델 애니메이션을 진행하기 위해 `model.play_anim()`을 사용하는 것 외에도, *Model* 컴포넌트는 `go.animate()`로 조작할 수 있는 "cursor" 프로퍼티를 노출합니다([프로퍼티 애니메이션](/manuals/property-animation)에 대한 자세한 내용):

```lua
-- #model에 애니메이션을 설정하지만 시작하지는 않습니다
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- 커서를 애니메이션의 시작 지점으로 설정합니다
go.set("#model", "cursor", 0)
-- 커서를 0과 1 사이에서 in-out quad easing으로 pingpong 트윈합니다.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## 완료 콜백

모델 애니메이션 `model.play_anim()`은 마지막 인자로 선택적 Lua 콜백 함수를 지원합니다. 이 함수는 애니메이션이 끝까지 재생되면 호출됩니다. 루프 애니메이션에서는 호출되지 않으며, `go.cancel_animations()`로 애니메이션을 수동 취소한 경우에도 호출되지 않습니다. 콜백은 애니메이션 완료 시 이벤트를 트리거하거나 여러 애니메이션을 이어서 재생하는 데 사용할 수 있습니다.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- 애니메이션 완료
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## 재생 모드

애니메이션은 한 번만 재생하거나 루프로 재생할 수 있습니다. 애니메이션이 재생되는 방식은 재생 모드에 의해 결정됩니다:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
