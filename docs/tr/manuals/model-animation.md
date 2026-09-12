---
title: Defold'da 3B model animasyonu kılavuzu
brief: Bu kılavuz, Defold'da 3B model animasyonlarının nasıl kullanılacağını açıklar.
---

# 3B model animasyonu

Model bileşenleri (model components), glTF dosyalarından içe aktarılan iskelet animasyonlarını (skeletal animations) ve biçim hedefi animasyonlarını (morph target animations) oynatabilir. İskelet animasyonu, modelin köşelerini deforme etmek için modelin kemiklerini kullanır. Şekil harmanlama animasyonu (blend shape animation) olarak da bilinen biçim hedefi animasyonu, alternatif köşe konumlarının ağırlıklarına animasyon uygulayarak modelin şeklini değiştirir.

Animasyon için 3B verilerin bir modele nasıl içe aktarılacağı hakkında ayrıntılı bilgi için [Model belgelerine](/manuals/model) bakın.

  ![Blender animasyonu](images/animation/blender_animation.png)
  ![Sallanma döngüsü](images/animation/suzanne.gif)


## Animasyonları oynatma

Modellere [`model.play_anim()`](/ref/model#model.play_anim) işleviyle animasyon uygulanır:

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold şu anda yalnızca önceden hesaplanıp kaydedilmiş (baked) iskelet animasyonlarını destekler. İskelet animasyonlarında konum, dönme ve ölçek için ayrı anahtarlar yerine, her anahtar karede animasyon uygulanan her kemik için bir matris bulunması gerekir.

Animasyonlarda ayrıca doğrusal ara değerleme (interpolation) uygulanır. Daha gelişmiş eğri ara değerlemesi kullanıyorsanız animasyonların dışa aktarma aracı tarafından önceden hesaplanıp kaydedilmesi gerekir.
:::

### Biçim hedefleri {#morph-targets}

Biçim hedefleri (morph targets), aynı örgünün (mesh) alternatif şekilleridir. Her hedef konum, normal ve teğet farklarını saklar ve her hedefin, o şeklin ne ölçüde uygulanacağını denetleyen bir harmanlama ağırlığı vardır. Ağırlığın `0` olması hedefin hiçbir etkisinin olmadığı anlamına gelirken, `1` olması hedef şeklin tamamını uygular. Gölgelendirici ve varlık buna uygun hazırlanmışsa bu aralığın dışındaki değerler de abartılı efektler için yararlı olabilir.

Defold, biçim hedeflerini ve başlangıçtaki biçim hedefi ağırlıklarını glTF model verilerinden içe aktarır. Biçim hedefi ağırlıklarına animasyon uygulayan glTF animasyonları, modelin animasyon kümesine içe aktarılır ve tıpkı iskelet animasyonları gibi [`model.play_anim()`](/ref/model#model.play_anim) ile oynatılabilir:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Biçim hedefi verileri tek başına veya iskelet animasyonuyla birlikte kullanılabilir, ancak bir model bileşeni aynı anda yalnızca bir model animasyonu oynatabilir. Bu, `model.play_anim()` kullanarak bir iskelet animasyonunu ve ayrı bir biçim hedefi animasyonunu aynı anda oynatamayacağınız anlamına gelir. Modelin animasyon verileri varsa ancak iskeleti yoksa yalnızca biçim hedefi animasyon verileri kullanılır.

Yine de iskelet animasyonu oynatmayı başka kaynaklardan gelen biçim hedefi değişiklikleriyle birleştirebilirsiniz; örneğin `model.set_blend_weights()` ile betikten biçim hedefi ağırlıklarını ayarlayabilirsiniz.

Biçim hedefi ağırlıklarını betikten okuyabilir ve geçersiz kılabilirsiniz. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights), modelde biçim hedefleri bulunan ilk örgünün o anki ağırlıklarını döndürür. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights), modelde biçimi değiştirilen her örgüye betikten geçersiz kılma uygular:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

Ağırlık tablosu, örgüdeki biçim hedefleriyle aynı sırada, birden başlayan Lua indekslerini kullanır. Fazladan değerler yok sayılır; tablonun içerdiğinden daha fazla biçim hedefi olan örgülerde eksik değerler sıfır kabul edilir. Betikle geçersiz kılma işlemi, kaldırılana kadar her karede animasyondan sonra uygulanır:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Gölgelendirici desteği

Biçim hedeflerini işleyerek (rendering) görüntü oluşturmak için model materyalinin köşe gölgelendiricisinin (vertex shader), oluşturulan `morph_targets` dokusundan örnekleme yapması ve ağırlıklandırılmış farkları köşe verilerine uygulaması gerekir. Biçim hedefi dokusu, her biçim hedefinin üç dizi katmanı kullandığı bir 2B dizi dokusudur: konum farkı, normal farkı ve teğet farkı.

Motor, o anki biçim hedefi ağırlıklarını köşe gölgelendiricisine `morph_targets_weights` adlı bir uniform aracılığıyla sağlar. Her `vec4` dört ağırlık saklar, dolayısıyla `morph_targets_weights[2]` sekiz biçim hedefi için yer içerir.

Aşağıdaki örnek, örnekli çizim kullanılmayan (non-instanced) bir model materyali için köşe gölgelendiricisinin ilgili bölümlerini gösterir:

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

Düzenleyicide model animasyonu önizlemesi henüz bulunmadığından, oluşturulan biçim hedefi dokusu verileri yalnızca çalışma sırasında kullanılabilir; bu nedenle `#ifndef EDITOR` sarmalayıcısı gereklidir. Örgüde daha fazla biçim hedefi varsa `morph_targets_weights` dizisinin boyutunu artırın ve daha fazla `apply_morph_target()` çağrısı ekleyin.

::: important
Yukarıdaki gölgelendirici örneği `textureSize()` kullanır ve OpenGL ES 2.0 üzerinde çalışmaz.
:::

### Kemik hiyerarşisi

Model iskeletindeki kemikler, motor içinde oyun nesneleri (game objects) olarak temsil edilir.

Kemiğe ait oyun nesnesi örneğinin kimliğini çalışma sırasında alabilirsiniz. [`model.get_go()`](/ref/model#model.get_go) işlevi, belirtilen kemiğin oyun nesnesinin kimliğini döndürür.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### İmleç animasyonu

Bir model animasyonunu ilerletmek için `model.play_anim()` kullanmanın yanı sıra, *Model* bileşenlerinin sunduğu `cursor` özelliğini `go.animate()` ile değiştirebilirsiniz ([özellik animasyonları](/manuals/property-animation) hakkında daha fazla bilgi):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Tamamlanma geri çağırımları

Model animasyonu işlevi `model.play_anim()`, son bağımsız değişken olarak isteğe bağlı bir Lua geri çağırım işlevini (callback function) destekler. Bu işlev, animasyon sonuna kadar oynatıldığında çağrılır. İşlev, döngüde oynatılan animasyonlarda veya bir animasyon `go.cancel_animations()` ile elle iptal edildiğinde hiçbir zaman çağrılmaz. Geri çağırım, animasyon tamamlandığında olayları tetiklemek veya birden fazla animasyonu zincirleme bağlamak için kullanılabilir.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Oynatma modları

Animasyonlar bir kez veya döngüde oynatılabilir. Animasyonun nasıl oynatılacağını oynatma modu belirler:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
