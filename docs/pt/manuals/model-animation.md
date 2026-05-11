---
title: Manual de animação de modelo 3D no Defold
brief: Este manual descreve como usar animações de modelos 3D no Defold.
---

# Animação 3D com skinning

A animação esquelética de modelos 3D usa os ossos do modelo para aplicar deformação aos vértices do modelo.

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
Atualmente, o Defold oferece suporte apenas a animações baked. As animações precisam ter matrizes para cada osso animado em cada keyframe, e não posição, rotação e escala como chaves separadas.

As animações também são interpoladas linearmente. Se você usar interpolação de curvas mais avançada, as animações precisam ser prebaked pelo exportador.
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
