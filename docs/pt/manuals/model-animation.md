---
title: Manual de animação de modelo 3D no Defold
brief: Este manual descreve como usar animações de modelos 3D no Defold.
---

# Animação de modelo 3D

Componentes Model podem reproduzir animações esqueléticas e animações de morph target importadas de arquivos glTF. A animação esquelética usa os ossos do modelo para aplicar deformação aos vértices do modelo. A animação de morph target, também conhecida como animação de blend shape, muda a forma do modelo animando pesos para posições alternativas dos vértices.

Para detalhes sobre como importar dados 3D para um Model para animação, consulte a [documentação de Model](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png)
  ![Wiggle loop](images/animation/suzanne.gif)


## Reproduzindo animações

Modelos são animados com a função [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Inicia a animação "wiggle" para frente e para trás em #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Atualmente, o Defold oferece suporte apenas a animações esqueléticas baked. As animações esqueléticas precisam ter matrizes para cada osso animado em cada keyframe, e não posição, rotação e escala como chaves separadas.

As animações também são interpoladas linearmente. Se você usar interpolação de curvas mais avançada, as animações precisam ser prebaked pelo exportador.
:::

### Morph targets {#morph-targets}

Morph targets são formas alternativas para a mesma malha. Cada target armazena deltas de posição, normal e tangente, e cada target tem um peso de mistura que controla quanto daquela forma é aplicado. Um peso de `0` significa que o target não tem efeito, enquanto um peso de `1` aplica a forma completa do target. Valores fora desse intervalo também podem ser úteis para efeitos exagerados se o shader e o asset tiverem sido criados para isso.

O Defold importa morph targets e pesos iniciais de morph a partir dos dados de modelo glTF. Animações glTF que animam pesos de morph são importadas para o conjunto de animações do modelo e podem ser reproduzidas com [`model.play_anim()`](/ref/model#model.play_anim), assim como animações esqueléticas:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Dados de morph target podem ser usados sozinhos ou junto com animação esquelética, mas um componente de modelo só pode reproduzir uma animação de modelo por vez. Isso significa que você não pode reproduzir uma animação esquelética e uma animação separada de morph target ao mesmo tempo usando `model.play_anim()`. Se um modelo tiver dados de animação, mas não tiver esqueleto, somente os dados de animação de morph target serão usados.

Você ainda pode combinar a reprodução de animação esquelética com mudanças de morph target vindas de outras fontes, por exemplo definindo pesos de morph target por script com `model.set_blend_weights()`.

Você também pode ler e sobrescrever pesos de morph target por script. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) retorna os pesos atuais para a primeira malha no modelo que tem morph targets. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) aplica uma sobrescrita de script a todas as malhas com morph no modelo:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

A tabela de pesos usa índices Lua começando em um, na mesma ordem dos morph targets na malha. Valores extras são ignorados, e valores ausentes são tratados como zero para malhas com mais morph targets do que a tabela contém. A sobrescrita de script é aplicada depois da animação em todos os frames até ser limpa:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Suporte de shader

Para renderizar morph targets, o vertex shader do material do modelo precisa amostrar a textura `morph_targets` gerada e aplicar os deltas ponderados aos dados do vértice. A textura de morph target é uma textura de array 2D em que cada morph target usa três camadas do array: delta de posição, delta de normal e delta de tangente.

A engine fornece os pesos atuais de morph para um uniform do vertex shader chamado `morph_targets_weights`. Cada `vec4` armazena quatro pesos, então `morph_targets_weights[2]` tem espaço para oito morph targets.

O exemplo a seguir mostra as partes relevantes do vertex shader para um material de modelo sem instancing:

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

O wrapper `#ifndef EDITOR` é necessário porque a pré-visualização de animação de modelo ainda não está disponível no editor, então os dados da textura de morph target gerada só estão disponíveis em tempo de execução. Aumente o tamanho do array `morph_targets_weights` e adicione mais chamadas a `apply_morph_target()` se a malha tiver mais morph targets.

::: important
O exemplo de shader acima usa `textureSize()` e não funciona no OpenGL ES 2.0.
:::

### A hierarquia de ossos

Os ossos no esqueleto do Model são representados internamente como objetos de jogo.

Você pode recuperar o id de instância do objeto de jogo do osso em tempo de execução. A função [`model.get_go()`](/ref/model#model.get_go) retorna o id do objeto de jogo para o osso especificado.

```lua
-- Obtém o go do osso intermediário do nosso modelo wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Agora faça algo útil com o objeto de jogo...
```

### Animação por cursor

Além de usar `model.play_anim()` para avançar uma animação de modelo, componentes *Model* expõem uma propriedade "cursor" que pode ser manipulada com `go.animate()` (mais sobre [animações de propriedade](/manuals/property-animation)):

```lua
-- Define a animação em #model, mas não a inicia
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Define o cursor para o início da animação
go.set("#model", "cursor", 0)
-- Interpola o cursor entre 0 e 1 em pingpong com easing in-out quad.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callbacks de conclusão

A animação de modelo `model.play_anim()`) oferece suporte a uma função de callback Lua opcional como último argumento. Essa função será chamada quando a animação tiver sido reproduzida até o fim. A função nunca é chamada para animações em loop, nem quando uma animação é cancelada manualmente por `go.cancel_animations()`. O callback pode ser usado para disparar eventos ao concluir a animação ou para encadear várias animações.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Terminou de animar
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Modos de reprodução

Animações podem ser reproduzidas uma vez ou em loop. Como a animação é reproduzida é determinado pelo modo de reprodução:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
