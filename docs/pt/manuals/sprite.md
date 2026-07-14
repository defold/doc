---
title: Exibindo imagens 2D
brief: Este manual descreve como exibir imagens 2D e animações usando o componente sprite.
---

# Sprites

Um componente Sprite é uma imagem simples ou animação flipbook exibida na tela.

![sprite](images/graphics/sprite.png)

O componente Sprite pode usar um [Atlas](/manuals/atlas) ou um [Tile Source](/manuals/tilesource) para seus gráficos.

## Propriedades de Sprite

Além das propriedades *Id*, *Position* e *Rotation*, existem as seguintes propriedades específicas do componente:

*Image*
: Se o shader tiver um único sampler, esse campo se chama `Image`. Caso contrário, cada slot recebe o nome do sampler de textura no material.
Cada slot especifica o recurso de atlas ou tilesource a ser usado pelo sprite nesse sampler de textura.

*Default Animation*
: A animação a ser usada pelo sprite. As informações de animação são obtidas do primeiro atlas ou tilesource.

*Material*
: O material a ser usado para renderizar o sprite.

*Blend Mode*
: O modo de mesclagem a ser usado ao renderizar o sprite.

*Size Mode*
: Se definido como `Automatic`, o editor definirá um tamanho para o sprite. Se definido como `Manual`, você pode definir o tamanho por conta própria.

*Slice 9*
: Defina para preservar o tamanho em pixels da textura do sprite ao redor das bordas quando o sprite for redimensionado.

:[Slice-9](../shared/slice-9-texturing.md)

### Modos de mesclagem
:[blend-modes](../shared/blend-modes.md)

## Manipulação em tempo de execução

Você pode manipular sprites em tempo de execução por meio de várias funções e propriedades diferentes (consulte a [documentação da API para uso](/ref/sprite/)). Funções:

* `sprite.play_flipbook()` - Reproduz uma animação em um componente sprite.
* `sprite.set_hflip()` e `sprite.set_vflip()` - Define inversão horizontal e vertical na animação de um sprite.

Um sprite também tem várias propriedades diferentes que podem ser manipuladas usando `go.get()` e `go.set()`:

`cursor`
: O cursor normalizado da animação (`number`).

`image`
: A imagem do sprite (`hash`). Você pode alterá-la usando uma propriedade de recurso de atlas ou tile source e `go.set()`. Consulte a [referência da API para um exemplo](/ref/sprite/#image).

`material`
: O material do sprite (`hash`). Você pode alterá-lo usando uma propriedade de recurso de material e `go.set()`. Consulte a [referência da API para um exemplo](/ref/sprite/#material).

`playback_rate`
: A taxa de reprodução da animação (`number`).

`scale`
: A escala não uniforme do sprite (`vector3`).

`size`
: O tamanho do sprite (`vector3`). Só pode ser alterado se o `modo de tamanho` do sprite estiver definido como `manual`.

## Constantes de material

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: A cor de tingimento do sprite (`vector4`). O `vector4` é usado para representar o tingimento com `x`, `y`, `z` e `w` correspondendo ao tingimento vermelho, verde, azul e alfa.

## Atributos de material

Um sprite pode sobrescrever atributos de vértice do material atualmente atribuído, e eles serão passados para o vertex shader a partir do componente (consulte o [manual de Material para mais detalhes](/manuals/material/#attributes)).

Os atributos especificados no material aparecerão como propriedades regulares no inspetor e podem ser definidos em componentes sprite individuais. Se qualquer atributo for sobrescrito, ele aparecerá como uma propriedade sobrescrita e será armazenado no arquivo sprite em disco:

![sprite-attributes](../images/graphics/sprite-attributes.png)

## Configuração do projeto

O arquivo *game.project* tem algumas [configurações do projeto](/manuals/project-settings#sprite) relacionadas a sprites.

## Sprites com múltiplas texturas {#multi-textured-sprites}

Quando um sprite usa várias texturas, há alguns pontos a observar.

### Animações

Os dados de animação (fps, nomes dos frames) atualmente são obtidos da primeira textura. Vamos chamar isso de "animação condutora".

Os ids de imagem da animação condutora são usados para procurar as imagens em outra textura.
Por isso é importante garantir que os ids dos frames correspondam entre as texturas.

Por exemplo, se o seu `diffuse.atlas` tiver uma animação `run` assim:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Então os ids dos frames seriam `run/hero_run_color_1`, o que provavelmente não será encontrado, por exemplo, em um `normal.atlas`:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Então usamos os `Rename patterns` no [atlas](/manuals/material/) para renomeá-los.
Defina `_color=` e `_normal=` nos atlas correspondentes, e você terá nomes de frame como estes em ambos os atlas:

```
run/hero_run_1
run/hero_run_2
...
```

### UVs

As UVs são obtidas da primeira textura. Como há apenas um conjunto de vértices, não podemos garantir
uma boa correspondência se as texturas secundárias tiverem mais coordenadas UV ou uma forma diferente.

Isso é importante, então certifique-se de que as imagens tenham formas suficientemente parecidas, ou você pode observar vazamento de textura.

As dimensões das imagens em cada textura podem ser diferentes.
