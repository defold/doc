---
title: Manual de tile map do Defold
brief: Este manual detalha o suporte do Defold a tile maps.
---

# Tile map

Um *Tile Map* é um componente que permite montar, ou pintar, tiles de um *Tile Source* em uma grande área de grade. Tile maps são comumente usados para construir ambientes de fases de jogos. Você também pode usar os *Collision Shapes* do tile source nos seus mapas para detecção de colisão e simulação física ([exemplo](/examples/tilemap/collisions/)).

Antes de criar um tile map, você precisa criar um Tile Source. Consulte o [manual de Tile Source](/manuals/tilesource) para aprender como criar um Tile Source.

## Criando um tile map

Para criar um novo tile map:

- Use <kbd>Right click</kbd> em um local no navegador *Assets* e selecione <kbd>New... ▸ Tile Map</kbd>).
- Dê um nome ao arquivo.
- O novo tile map abre automaticamente no editor de tile map.

  ![new tilemap](images/tilemap/tilemap.png)

- Defina a propriedade *Tile Source* para um arquivo de tile source que você preparou.

Para pintar tiles no seu tile map:

1. Selecione ou crie uma *Layer* para pintar na visualização *Outline*.
2. Selecione um tile para usar como pincel (pressione <kbd>Space</kbd> para mostrar a paleta de tiles) ou selecione alguns tiles clicando e arrastando na paleta para criar um pincel retangular com vários tiles.

   ![Palette](images/tilemap/palette.png)

3. Pinte com o pincel selecionado. Para apagar um tile, escolha um tile vazio e use-o como pincel, ou selecione a borracha (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Painting tiles](images/tilemap/paint_tiles.png)

Você pode escolher tiles diretamente de uma camada e usar a seleção como pincel. Segure <kbd>Shift</kbd> e clique em um tile para capturá-lo como o pincel atual. Enquanto segura <kbd>Shift</kbd>, você também pode clicar e arrastar para selecionar um bloco de tiles e usá-lo como um pincel maior. Também é possível recortar tiles de forma semelhante segurando <kbd>Shift+Ctrl</kbd> ou apagá-los segurando <kbd>Shift+Alt</kbd>.

Para rotacionar o pincel no sentido horário, use <kbd>Z</kbd>. Use <kbd>X</kbd> para inversão horizontal e <kbd>Y</kbd> para inversão vertical do pincel.

![Picking tiles](images/tilemap/pick_tiles.png)

## Adicionando um tile map ao seu jogo

Para adicionar um tile map ao seu jogo:

1. Crie um objeto de jogo para conter o componente tile map. O objeto de jogo pode estar em um arquivo ou ser criado diretamente em uma coleção.
2. Clique com o botão direito na raiz do objeto de jogo e selecione <kbd>Add Component File</kbd>.
3. Selecione o arquivo de tile map.

![Use tile map](images/tilemap/use_tilemap.png)

## Manipulação em tempo de execução

Você pode manipular tilemaps em tempo de execução por meio de várias funções e propriedades diferentes (consulte a [documentação da API para uso](/ref/tilemap/)).

### Alterando tiles por script

Você pode ler e escrever o conteúdo de um tile map dinamicamente enquanto o jogo está em execução. Para isso, use as funções [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) e [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile):

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Substitui grass-tile (2) por um tile de buraco perigoso (número 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Propriedades de Tilemap

Além das propriedades *Id*, *Position*, *Rotation* e *Scale*, existem as seguintes propriedades específicas do componente:

*Tile Source*
: O recurso tilesource a ser usado pelo tilemap.

*Material*
: O material a ser usado para renderizar o tilemap.

*Blend Mode*
: O modo de mesclagem a ser usado ao renderizar o tilemap.

### Modos de mesclagem
:[blend-modes](../shared/blend-modes.md)

### Alterando propriedades

Um tilemap tem várias propriedades diferentes que podem ser manipuladas usando `go.get()` e `go.set()`:

`tile_source`
: O tile source do tile map (`hash`). Você pode alterá-lo usando uma propriedade de recurso de tile source e `go.set()`. Consulte a [referência da API para um exemplo](/ref/tilemap/#tile_source).

`material`
: O material do tile map (`hash`). Você pode alterá-lo usando uma propriedade de recurso de material e `go.set()`. Consulte a [referência da API para um exemplo](/ref/tilemap/#material).

### Constantes de material

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: A cor de tingimento do tile map (`vector4`). O `vector4` é usado para representar o tingimento com x, y, z e w correspondendo ao tingimento vermelho, verde, azul e alfa.

## Configuração do projeto

O arquivo *game.project* tem algumas [configurações do projeto](/manuals/project-settings#tilemap) relacionadas a tilemaps.

## Ferramentas externas

Há editores externos de mapa/fase que podem exportar diretamente para tilemaps do Defold:

### Tiled

[Tiled](https://www.mapeditor.org/) é um editor de mapas conhecido e amplamente usado para mapas ortogonais, isométricos e hexagonais. O Tiled tem suporte a muitos recursos e pode [exportar diretamente para o Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/). Saiba mais sobre como exportar dados de tilemap e metadados adicionais [nesta publicação de blog do usuário Defold "goeshard"](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) pode ser usado para criar automaticamente tilesets completos a partir de tiles base simples, e tem um editor de mapas que pode exportar diretamente para o Defold.




