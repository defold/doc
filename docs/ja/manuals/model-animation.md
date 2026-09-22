---
title: Defold の 3D モデルアニメーションマニュアル
brief: このマニュアルでは、Defold で 3D モデルアニメーションを使用する方法を説明します。
---

# 3D モデルアニメーション {#3d-model-animation}

モデルコンポーネント（model component）は、glTF ファイルからインポートしたスケルタルアニメーション（skeletal animation）とモーフターゲットアニメーション（morph target animation）を再生できます。スケルタルアニメーションは、モデルのボーン（bone）を使ってモデル内の頂点を変形させます。ブレンドシェイプアニメーション（blend shape animation）とも呼ばれるモーフターゲットアニメーションは、別の頂点位置に対するウェイトをアニメーションさせて、モデルの形状を変化させます。

アニメーション用の 3D データをモデルにインポートする方法の詳細は、[モデルのドキュメント](/manuals/model)を参照してください。

  ![Blender のアニメーション](images/animation/blender_animation.png)
  ![揺れる動きのループ](images/animation/suzanne.gif)


## アニメーションの再生 {#playing-animations}

モデルは [`model.play_anim()`](/ref/model#model.play_anim) 関数でアニメーションさせます。

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold は現在、ベイク済みのスケルタルアニメーションのみをサポートしています。スケルタルアニメーションでは、アニメーションする各ボーンについて、キーフレームごとに行列が必要です。位置、回転、スケールをそれぞれ別のキーとして持つ形式には対応していません。

また、アニメーションは線形補間されます。より高度なカーブ補間を使用する場合は、エクスポーターでアニメーションを事前にベイクする必要があります。
:::

### モーフターゲット {#morph-targets}

モーフターゲット（morph target）は、同じメッシュ（mesh）に対する別の形状です。各ターゲットは位置、法線、接線の差分を格納し、それぞれの形状をどの程度適用するかを制御するブレンドウェイトを持ちます。ウェイトが `0` の場合、ターゲットは影響を与えず、`1` の場合、ターゲットの形状が完全に適用されます。シェーダー（shader）とアセット（asset）が対応するように作成されていれば、この範囲外の値も誇張した効果を表現するのに役立つことがあります。

Defold は、glTF のモデルデータからモーフターゲットと初期モーフウェイトをインポートします。モーフウェイトをアニメーションさせる glTF アニメーションは、モデルのアニメーションセット（animation set）にインポートされ、スケルタルアニメーションと同様に [`model.play_anim()`](/ref/model#model.play_anim) で再生できます。

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

モーフターゲットデータは単独でもスケルタルアニメーションと組み合わせても使用できますが、モデルコンポーネントが同時に再生できるモデルアニメーションは1つだけです。つまり、`model.play_anim()` を使って、1つのスケルタルアニメーションと、それとは別の1つのモーフターゲットアニメーションを同時に再生することはできません。モデルにアニメーションデータがあってもスケルトン（skeleton）がない場合は、モーフターゲットのアニメーションデータのみが使用されます。

ただし、スケルタルアニメーションの再生と、ほかの方法によるモーフターゲットの変更を組み合わせることはできます。たとえば、スクリプトから `model.set_blend_weights()` でモーフターゲットのウェイトを設定できます。

スクリプトからモーフターゲットのウェイトを読み取ったり、上書きしたりすることもできます。[`model.get_blend_weights()`](/ref/model#model.get_blend_weights) は、モデル内でモーフターゲットを持つ最初のメッシュの現在のウェイトを返します。[`model.set_blend_weights()`](/ref/model#model.set_blend_weights) は、モデル内でモーフィングするすべてのメッシュにスクリプトによる上書きを適用します。

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

ウェイトのテーブルは、メッシュ内のモーフターゲットと同じ順序で、1から始まる Lua のインデックスを使用します。余分な値は無視され、テーブルに含まれる値より多くのモーフターゲットを持つメッシュでは、不足している値はゼロとして扱われます。スクリプトによる上書きは、解除されるまで毎フレーム、アニメーションの後に適用されます。

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### シェーダーの対応 {#shader-support}

モーフターゲットを描画するには、モデルのマテリアル（material）の頂点シェーダーで、生成された `morph_targets` テクスチャ（texture）をサンプリングし、ウェイトを乗算した差分を頂点データに適用する必要があります。モーフターゲットのテクスチャは 2D 配列テクスチャで、各モーフターゲットは位置の差分、法線の差分、接線の差分という3つの配列レイヤーを使用します。

エンジンは、現在のモーフウェイトを `morph_targets_weights` という名前の頂点シェーダーのユニフォーム（uniform）に渡します。各 `vec4` には4つのウェイトが格納されるため、`morph_targets_weights[2]` には8つのモーフターゲット分を格納できます。

次の例は、インスタンシングを使用しないモデルマテリアルの頂点シェーダーから、関連する部分を示しています。

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
    // Each vec4 stores four blend weights. Use morph_targets_weights[1]
    // for up to 4 morph targets, [2] for up to 8, [3] for up to 12, etc.
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

エディターではモデルアニメーションのプレビューがまだ利用できず、生成されたモーフターゲットのテクスチャデータは実行時にのみ利用できるため、`#ifndef EDITOR` で囲む必要があります。メッシュにさらに多くのモーフターゲットがある場合は、`morph_targets_weights` の配列サイズを増やし、`apply_morph_target()` の呼び出しを追加してください。

::: important
上のシェーダーの例は `textureSize()` を使用しているため、OpenGL ES 2.0 では動作しません。
:::

### ボーンの階層 {#the-bone-hierarchy}

モデルのスケルトン内のボーンは、内部的にはゲームオブジェクト（game object）として表現されます。

実行時に、ボーンのゲームオブジェクトのインスタンス識別子を取得できます。[`model.get_go()`](/ref/model#model.get_go) 関数は、指定したボーンのゲームオブジェクトの識別子を返します。

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### カーソルのアニメーション {#cursor-animation}

`model.play_anim()` を使ってモデルアニメーションを進める方法に加えて、*モデル* コンポーネントは `cursor` プロパティ（property）を公開しており、`go.animate()` で操作できます（詳細は[プロパティアニメーション](/manuals/property-animation)を参照してください）。

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## 完了コールバック {#completion-callbacks}

モデルアニメーションの `model.play_anim()` は、最後の引数として省略可能な Lua のコールバック関数を受け取ります。この関数は、アニメーションが最後まで再生されると呼び出されます。ループするアニメーションでは呼び出されず、`go.cancel_animations()` でアニメーションを手動でキャンセルした場合も呼び出されません。コールバックは、アニメーションの完了時にイベントを発生させたり、複数のアニメーションをつなげたりするために使用できます。

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## 再生モード {#playback-modes}

アニメーションは1回だけ再生することも、ループ再生することもできます。アニメーションの再生方法は、再生モードによって決まります。

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
