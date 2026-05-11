---
title: Importando e usando gráficos 2D
brief: Este manual aborda como importar e usar gráficos 2D.
---

# Importando gráficos 2D

O Defold oferece suporte a muitos tipos de componentes visuais frequentemente usados em jogos 2D. Você pode usar o Defold para criar sprites estáticos e animados, componentes de UI, efeitos de partículas, tile maps e fontes bitmap. Antes de criar qualquer um desses componentes visuais, você precisa importar arquivos de imagem com os gráficos que deseja usar. Para importar arquivos de imagem, basta arrastar os arquivos do sistema de arquivos do seu computador e soltá-los em um local apropriado no *painel Conteúdo* do editor Defold.

![Importing files](images/graphics/import.png)

::: sidenote
O Defold oferece suporte a imagens nos formatos PNG e JPEG. Outros formatos de imagem precisam ser convertidos antes de poderem ser usados.
:::


## Criando assets do Defold

Quando as imagens são importadas para o Defold, elas podem ser usadas para criar assets específicos do Defold:

![atlas](images/icons/atlas.png){.icon} Atlas
: Um atlas contém uma lista de arquivos de imagem separados, que são combinados automaticamente em uma imagem de textura maior. Atlases podem conter imagens estáticas e *Animation Groups*, conjuntos de imagens que juntas formam uma animação flip-book.

  ![atlas](images/graphics/atlas.png)

Saiba mais sobre o recurso atlas no [manual de Atlas](/manuals/atlas).

![tile source](images/icons/tilesource.png){.icon} Tile Source
: Um tile source referencia um arquivo de imagem que já foi preparado para consistir em subimagens menores organizadas em uma grade uniforme. Outro termo comumente usado para esse tipo de imagem composta é _sprite sheet_. Tile sources podem conter animações flip-book, definidas pelo primeiro e pelo último tile da animação. Também é possível usar uma imagem para anexar automaticamente formas de colisão aos tiles.

  ![tile source](images/graphics/tilesource.png)

Saiba mais sobre o recurso tile source no [manual de Tile source](/manuals/tilesource).

![bitmap font](images/icons/font.png){.icon} Bitmap Font
: Uma fonte bitmap tem seus glifos em uma folha de fonte PNG. Esses tipos de fonte não oferecem melhoria de desempenho em relação a fontes geradas a partir de arquivos TrueType ou OpenType, mas podem incluir gráficos arbitrários, coloração e sombras diretamente na imagem.

Saiba mais sobre fontes bitmap no [manual de Fontes](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png)


## Usando assets do Defold

Depois de converter as imagens em arquivos Atlas e Tile Source, você pode usá-las para criar vários tipos diferentes de componentes visuais:

![sprite](images/icons/sprite.png){.icon}
: Um sprite é uma imagem estática ou animação flip-book exibida na tela.

  ![sprite](images/graphics/sprite.png)

Saiba mais sobre sprites no [manual de Sprite](/manuals/sprite).

![tile map](images/icons/tilemap.png){.icon} Tile map
: Um componente de tile map monta um mapa a partir de tiles (imagem e formas de colisão) vindos de um tile source. Tile maps não podem usar atlas como origem.

  ![tilemap](images/graphics/tilemap.png)

Saiba mais sobre tile maps no [manual de Tilemap](/manuals/tilemap).

![particle effect](images/icons/particlefx.png){.icon} Particle fx
: Partículas geradas por um emissor de partículas consistem em uma imagem estática ou uma animação flip-book de um atlas ou tile source.

  ![particles](images/graphics/particles.png)

Saiba mais sobre efeitos de partículas no [manual de Particle fx](/manuals/particlefx).

![gui](images/icons/gui.png){.icon} GUI
: Nodes GUI do tipo box e pie podem usar imagens estáticas e animações flip-book de atlases e tile sources.

  ![gui](images/graphics/gui.png)

Saiba mais sobre GUIs no [manual de GUI](/manuals/gui).
