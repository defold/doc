---
title: Manual de tile source do Defold
brief: Este manual descreve como usar e criar um tile source.
---

# Tile source

Um *Tile Source* pode ser usado por um [componente Tilemap](/manuals/tilemap) para pintar tiles em uma área de grade, ou pode ser usado como fonte gráfica para um [Sprite](/manuals/sprite) ou [componente Particle Effect](/manuals/particlefx). Você também pode usar os *Collision Shapes* do tile source em um Tilemap para [detecção de colisão e simulação física](/manuals/physics) ([exemplo](/examples/tilemap/collisions/)).

## Criando um tile source

Você precisa de uma imagem contendo todos os tiles. Cada tile deve ter exatamente as mesmas dimensões e estar posicionado em uma grade. O Defold suporta _spacing_ entre os tiles e uma _margin_ ao redor de cada tile.

![tile image](images/tilemap/small_map.png)

Depois de criar a imagem de origem, você pode criar um Tile Source:

- Importe a imagem para o seu projeto arrastando-a para um local do projeto no navegador *Assets*.
- Crie um novo arquivo de tile source (<kbd>right click</kbd> em um local no navegador *Assets* e selecione <kbd>New... ▸ Tile Source</kbd>).
- Dê um nome ao novo arquivo.
- O arquivo agora abre no editor de tile source.
- Clique no botão de navegação ao lado da propriedade *Image* e selecione sua imagem. Agora você deve ver a imagem exibida no editor.
- Ajuste as *Properties* para corresponder à imagem de origem. Quando tudo estiver correto, os tiles se alinharão perfeitamente.

![Creating a Tile Source](images/tilemap/tilesource.png)

Size
: O tamanho da imagem de origem.

Tile Width
: A largura de cada tile.

Tile Height
: A altura de cada tile.

Tile Margin
: O número de pixels ao redor de cada tile (laranja na imagem acima).

Tile Spacing
: O número de pixels entre cada tile (azul na imagem acima).

Inner Padding
: Especifica quantos pixels vazios devem ser adicionados automaticamente ao redor do tile na textura resultante usada quando o jogo é executado.

Extrude Border
: Especifica quantas vezes os pixels de borda devem ser replicados automaticamente ao redor do tile na textura resultante usada quando o jogo é executado.

Collision
: Especifica a imagem a ser usada para gerar automaticamente formas de colisão para os tiles.

## Animações flip-book de tile source

Para definir uma animação em um tile source, os tiles dos frames da animação devem estar lado a lado em uma sequência da esquerda para a direita. A sequência pode continuar de uma linha para a próxima. Todos os tile sources recém-criados têm uma animação padrão chamada "`anim`". Você pode adicionar novas animações clicando com o <kbd>right click</kbd> na raiz do tile source no *Outline* e selecionando <kbd>Add ▸ Animation</kbd>.

Selecionar uma animação exibe suas *Properties*.

![Tile Source animation](images/tilemap/animation.png)

Id
: A identidade da animação. Deve ser única para o tile source.

Start Tile
: O primeiro tile da animação. A numeração começa em 1 no canto superior esquerdo e segue para a direita, linha por linha, até o canto inferior direito.

End Tile
: O último tile da animação.

Playback
: Especifica como a animação deve ser reproduzida:

  - `None` não reproduz; a primeira imagem é exibida.
  - `Once Forward` reproduz a animação uma vez, da primeira à última imagem.
  - `Once Backward` reproduz a animação uma vez, da última à primeira imagem.
  - `Once Ping Pong` reproduz a animação uma vez, da primeira à última imagem e depois volta para a primeira.
  - `Loop Forward` reproduz a animação repetidamente, da primeira à última imagem.
  - `Loop Backward` reproduz a animação repetidamente, da última à primeira imagem.
  - `Loop Ping Pong` reproduz a animação repetidamente, da primeira à última imagem e depois volta para a primeira.

Fps
: A velocidade de reprodução da animação, expressa em frames por segundo (FPS).

Flip horizontal
: Inverte a animação horizontalmente.

Flip vertical
: Inverte a animação verticalmente.

## Formas de colisão de tile source

O Defold usa uma imagem especificada na propriedade *Collision* para gerar uma forma _convexa_ para cada tile. A forma contornará a parte do tile que tem informação de cor, ou seja, que não é 100% transparente.

Muitas vezes faz sentido usar para colisão a mesma imagem que contém os gráficos reais, mas você pode especificar uma imagem separada se quiser formas de colisão diferentes do visual. Quando você especifica uma imagem de colisão, a pré-visualização é atualizada com um contorno em cada tile indicando as formas de colisão geradas.

O *Outline* do tile source lista os grupos de colisão que você adicionou ao tile source. Novos arquivos de tile source recebem um grupo de colisão "default". Você pode adicionar novos grupos clicando com o <kbd>right click</kbd> na raiz do tile source no *Outline* e selecionando <kbd>Add ▸ Collision Group</kbd>.

Para selecionar as formas de tile que devem pertencer a um determinado grupo, selecione o grupo no *Outline* e clique em cada tile que deseja atribuir ao grupo. O contorno do tile e da forma é colorido com a cor do grupo. A cor é atribuída automaticamente ao grupo no editor.

![Collision Shapes](images/tilemap/collision.png)

Para remover um tile do seu grupo de colisão, selecione o elemento raiz do tile source no *Outline* e clique no tile.
