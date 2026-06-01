---
title: Modelos 3D no Defold
brief: Este manual descreve como trazer modelos 3D, esqueletos e animações para seu jogo.
---

# Componente Model

O Defold é, no seu núcleo, uma engine 3D. Mesmo quando você trabalha apenas com material 2D, toda renderização é feita em 3D, mas projetada ortograficamente na tela. O Defold permite usar conteúdo 3D completo incluindo assets 3D, ou _Models_, nas suas coleções. Você pode criar jogos estritamente 3D com apenas assets 3D, ou misturar conteúdo 3D e 2D como quiser.

## Criando um componente model

Componentes Model são criados como qualquer outro componente de objeto de jogo. Você pode fazer isso de duas formas:

- Crie um *arquivo Model* com <kbd>clique com o botão direito</kbd> em um local no navegador *Conteúdo* e selecione <kbd>Novo... ▸ Modelo</kbd>.
- Crie o componente incorporado diretamente em um objeto de jogo com <kbd>clique com o botão direito</kbd> em um objeto de jogo na visualização *Estrutura* e selecione <kbd>Adicionar Componente ▸ Modelo</kbd>.

![Model in game object](images/model/model.png)

Com o modelo criado, você precisa especificar algumas propriedades:

### Propriedades de model

Além das propriedades *Id*, *Position* e *Rotation*, existem as seguintes propriedades específicas do componente:

*Mesh*
: Esta propriedade deve referenciar o arquivo glTF *.gltf* que contém a malha a usar. Se o arquivo contiver morph targets, eles serão importados junto com a malha. Se o arquivo contiver várias malhas, apenas a primeira será lida.

*Create GO Bones*
: Marque isto para criar um objeto de jogo para cada osso do modelo. Você pode usar os objetos de jogo para anexar outros objetos de jogo, como armas, a ossos das mãos e assim por diante. 

*Skeleton*
: Esta propriedade deve referenciar o arquivo glTF *.gltf* que contém o esqueleto a usar para animação. Observe que o Defold exige um único osso raiz na sua hierarquia.

*Animations*
: Defina isto para o *Animation Set File* que contém as animações que você deseja usar no modelo.

*Default Animation*
: Esta é a animação (do conjunto de animações) que será reproduzida automaticamente no modelo.

Além das propriedades acima, também haverá um campo para atribuir um material a cada malha do modelo:

*Material*
: Defina esta propriedade para um material que você criou e que seja adequado para um objeto 3D texturizado. Há vários materiais integrados que você pode usar como ponto de partida:

  * Use *model.material* para modelos estáticos sem instancing
  * Use *model_instances.material* para modelos estáticos com instancing
  * Use *model_skinned.material* para modelos com skinning (animados) sem instancing
  * Use *model_skinned_instances.material* para modelos com skinning (animados) com instancing

Dependendo do material, haverá uma ou mais propriedades de textura:

*Texture*
: Esta propriedade deve apontar para o arquivo de imagem de textura que você deseja aplicar ao objeto.


## Manipulação no editor

Com o componente model no lugar, você pode editar e manipular livremente o componente e/ou o objeto de jogo que o encapsula com as ferramentas normais do *Scene Editor* para mover, rotacionar e escalar o modelo como desejar.

![Wiggler ingame](images/model/ingame.png)

## Manipulação em tempo de execução

Você pode manipular modelos em tempo de execução por meio de várias funções e propriedades diferentes (consulte a [documentação da API para uso](/ref/model/)).

### Animação em tempo de execução

O Defold oferece suporte poderoso para controlar animação em tempo de execução. Mais no [manual de animação de modelos](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

O cursor de reprodução da animação pode ser animado manualmente ou pelo sistema de animação de propriedades:

```lua
-- define a animação de corrida
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- anima o cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Modelos também podem usar animações glTF de morph target. Pesos de morph target são animados com `model.play_anim()` como outras animações de modelo, e podem ser lidos ou sobrescritos em tempo de execução usando [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) e [`model.set_blend_weights()`](/ref/model#model.set_blend_weights). Veja a [seção de morph targets](/manuals/model-animation#morph-targets) no manual de animação de modelos para detalhes.

### Alterando propriedades

Um modelo também tem várias propriedades diferentes que podem ser manipuladas usando `go.get()` e `go.set()`:

`animation`
: A animação atual do modelo (`hash`) (SOMENTE LEITURA). Você altera a animação usando `model.play_anim()` (veja acima).

`cursor`
: O cursor normalizado da animação (`number`).

`material`
: O material do modelo (`hash`). Você pode alterá-lo usando uma propriedade de recurso de material e `go.set()`. Consulte a [referência da API para um exemplo](/ref/model/#material).

`playback_rate`
: A taxa de reprodução da animação (`number`).

`textureN`
: As texturas do modelo, onde N é 0-7 (`hash`). Você pode alterá-las usando uma propriedade de recurso de textura e `go.set()`. Consulte a [referência da API para um exemplo](/ref/model/#textureN).


## Material

Softwares 3D normalmente permitem definir propriedades nos vértices do seu objeto, como coloração e texturização. Essas informações vão para o arquivo glTF *.gltf* que você exporta do seu software 3D. Dependendo dos requisitos do seu jogo, você terá que selecionar e/ou criar materiais apropriados e _performáticos_ para seus objetos. Um material combina _programas de shader_ com um conjunto de parâmetros para renderização do objeto.

Há vários materiais integrados que você pode usar como ponto de partida:

  * Use *model.material* para modelos estáticos sem instancing
  * Use *model_instances.material* para modelos estáticos com instancing
  * Use *model_skinned.material* para modelos com skinning (animados) sem instancing
  * Use *model_skinned_instances.material* para modelos com skinning (animados) com instancing

Se você precisar criar materiais personalizados para seus modelos, consulte a [documentação de Material](/manuals/material) para informações. O [manual de Shader](/manuals/shader) contém informações sobre como os programas de shader funcionam.


### Constantes de material

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: O tint de cor do modelo (`vector4`). O vector4 é usado para representar o tint com x, y, z e w correspondendo ao tint vermelho, verde, azul e alfa.


## Renderização

O script de renderização padrão é feito sob medida para jogos 2D e não funciona com modelos 3D. Mas, copiando o script de renderização padrão e adicionando algumas linhas de código ao script de renderização, você pode habilitar a renderização dos seus modelos. Por exemplo:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- ortográfica
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Veja a [documentação de Render](/manuals/render) para detalhes sobre como scripts de renderização funcionam.
