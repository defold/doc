---
title: Manual de atlas
brief: Este manual explica como os recursos de atlas funcionam no Defold.
---

# Atlas

Embora imagens individuais sejam usadas com frequência como origem para sprites, por motivos de desempenho as imagens precisam ser combinadas em conjuntos maiores de imagens, chamados atlases. Combinar conjuntos de imagens menores em atlases é especialmente importante em dispositivos móveis, onde memória e poder de processamento são mais escassos do que em computadores desktop ou consoles de jogos dedicados.

No Defold, um recurso de atlas é uma lista de arquivos de imagem separados, que são automaticamente combinados em uma imagem maior.

## Criando um atlas

Selecione <kbd>New... ▸ Atlas</kbd> no menu de contexto do navegador *Assets*. Dê um nome ao novo arquivo de atlas. O editor abrirá o arquivo no editor de atlas. As propriedades do atlas são exibidas no painel *Properties*, onde você pode editá-las (veja detalhes abaixo).

Você precisa preencher um atlas com imagens ou animações antes de poder usá-lo como origem gráfica para componentes de objetos, como sprites e componentes ParticleFX.

Certifique-se de ter adicionado suas imagens ao projeto (arraste e solte os arquivos de imagem no local correto no navegador *Assets*).

Adicionando imagens individuais

: Arraste e solte imagens do painel *Assets* para a visualização do editor.
  
  Como alternativa, use <kbd>Right click</kbd> na entrada raiz Atlas no painel *Outline*.

  Selecione <kbd>Add Images</kbd> no menu de contexto popup para adicionar imagens individuais.

  Uma caixa de diálogo é aberta, na qual você pode encontrar e selecionar as imagens que deseja adicionar ao atlas. Observe que você pode filtrar os arquivos de imagem e selecionar vários arquivos de uma vez.

  ![Criando um atlas, adicionando imagens](images/atlas/add.png)

  As imagens adicionadas são listadas em *Outline*, e o atlas completo pode ser visto no centro da visualização do editor. Talvez seja necessário pressionar <kbd>F</kbd> (<kbd>View ▸ Frame Selection</kbd> no menu) para enquadrar a seleção.

  ![Imagens adicionadas](images/atlas/single_images.png)

Adicionando animações flipbook
: Use <kbd>Right click</kbd> na entrada raiz Atlas no painel *Outline*.

  Selecione <kbd>Add Animation Group</kbd> no menu de contexto popup para criar um grupo de animação flipbook.

  Um novo grupo de animação vazio, com um nome padrão ("New Animation"), é adicionado ao atlas.

  Arraste e solte imagens do painel *Assets* para a visualização do editor para adicioná-las ao grupo selecionado no momento.
  
  Como alternativa, use <kbd>Right click</kbd> no novo grupo e selecione <kbd>Add Images</kbd> no menu de contexto.

  Uma caixa de diálogo é aberta, na qual você pode encontrar e selecionar as imagens que deseja adicionar ao grupo de animação.

  ![Criando um atlas, adicionando imagens](images/atlas/add_animation.png)

  Pressione <kbd>Space</kbd> com o grupo de animação selecionado para pré-visualizá-lo, e <kbd>Ctrl/Cmd+T</kbd> para fechar a pré-visualização. Ajuste as *Properties* da animação conforme necessário (veja abaixo).

  ![Grupo de animação](images/atlas/animation_group.png)

Você pode reordenar as imagens em Outline selecionando-as e pressionando <kbd>Alt + Up/down</kbd>. Também é fácil criar duplicatas copiando e colando imagens no outline (pelo menu <kbd>Edit</kbd>, pelo menu de contexto do botão direito ou por atalhos de teclado).

## Propriedades do atlas

Cada recurso de atlas tem um conjunto de propriedades. Elas são exibidas no painel *Properties* quando você seleciona o item raiz na visualização *Outline*.

Size
: Mostra o tamanho total calculado do recurso de textura resultante. A largura e a altura são definidas para a potência de dois mais próxima. Observe que, se você ativar a compressão de textura, alguns formatos exigem texturas quadradas. Texturas não quadradas serão então redimensionadas e preenchidas com espaço vazio para tornar a textura quadrada. Veja o [manual de perfis de textura](/manuals/texture-profiles/) para detalhes.

Margin
: O número de pixels que deve ser adicionado entre cada imagem.

Inner Padding
: O número de pixels vazios que deve ser adicionado ao redor de cada imagem.

Extrude Borders
: O número de pixels de borda que deve ser repetidamente estendido ao redor de cada imagem. Quando o fragment shader amostra pixels na borda de uma imagem, pixels de uma imagem vizinha (na mesma textura de atlas) podem vazar. Extrudar a borda resolve esse problema.

Max Page Size
: O tamanho máximo de uma página em um atlas de múltiplas páginas. Isso pode ser usado para dividir um atlas em várias páginas do mesmo atlas, restringindo o tamanho do atlas e ainda usando apenas uma única draw call. Este recurso deve ser usado em combinação com materiais com atlas de múltiplas páginas habilitado encontrados em `/builtins/materials/*_paged_atlas.material`.

![Atlas de múltiplas páginas](images/atlas/multipage_atlas.png)

Rename Patterns
: Uma lista separada por vírgulas (´,´) de padrões de busca e substituição, onde cada padrão tem a forma `search=replace`.
O nome original de cada imagem (o nome base do arquivo) será transformado usando esses padrões. (Por exemplo, um padrão `hat=cat,_normal=` renomeará uma imagem chamada `hat_normal` para `cat`). Isso é útil ao combinar animações entre atlases.

Aqui estão exemplos das diferentes configurações de propriedades com quatro imagens quadradas de tamanho 64x64 adicionadas a um atlas. Observe como o atlas salta para 256x256 assim que as imagens não cabem em 128x128, resultando em muito espaço de textura desperdiçado.

![Propriedades do atlas](images/atlas/atlas_properties.png)

## Propriedades da imagem

Cada imagem em um atlas tem um conjunto de propriedades:

Id
: O id da imagem (somente leitura).

Size
: A largura e a altura da imagem (somente leitura).

Pivot
: O ponto de pivô da imagem (em unidades). O canto superior esquerdo é (0,0), e o canto inferior direito é (1,1). O padrão é (0.5, 0.5). O pivô pode ficar fora do intervalo 0-1. O ponto de pivô é onde a imagem será centralizada quando usada, por exemplo, em um sprite. Você pode modificar o ponto de pivô arrastando a alça do pivô na visualização do editor. A alça ficará visível somente quando uma única imagem estiver selecionada. O snapping pode ser ativado mantendo <kbd>Shift</kbd> pressionado enquanto arrasta.

Sprite Trim Mode
: Como o sprite é renderizado. O padrão é renderizar o sprite como um retângulo (Sprite Trim Mode definido como Off). Se o sprite contiver muitos pixels transparentes, pode ser mais eficiente renderizá-lo como uma forma não retangular usando entre 4 e 8 vértices. Observe que o recorte de sprite não funciona junto com sprites slice-9.

Image
: Caminho para a própria imagem.

![Propriedades da imagem](images/atlas/image_properties.png)

## Propriedades da animação

Além da lista de imagens que fazem parte de um grupo de animação, há um conjunto de propriedades disponível:

Id
: O nome da animação.

Fps
: A velocidade de reprodução da animação, expressa em frames por segundo (FPS).

Flip horizontal
: Inverte a animação horizontalmente.

Flip vertical
: Inverte a animação verticalmente.

Playback
: Especifica como a animação deve ser reproduzida:

  - `None` não reproduz nada; a primeira imagem é exibida.
  - `Once Forward` reproduz a animação uma vez, da primeira até a última imagem.
  - `Once Backward` reproduz a animação uma vez, da última até a primeira imagem.
  - `Once Ping Pong` reproduz a animação uma vez, da primeira até a última imagem, e depois volta para a primeira imagem.
  - `Loop Forward` reproduz a animação repetidamente, da primeira até a última imagem.
  - `Loop Backward` reproduz a animação repetidamente, da última até a primeira imagem.
  - `Loop Ping Pong` reproduz a animação repetidamente, da primeira até a última imagem, e depois volta para a primeira imagem.

## Criação de textura e atlas em runtime

É possível criar uma textura e um atlas em runtime.

### Criando um recurso de textura em runtime

Use [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) para criar um novo recurso de textura:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Depois que a textura for criada, você pode usar [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) para definir os pixels da textura:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
Também é possível usar `resource.set_texture()` para atualizar uma sub-região da textura usando uma largura e altura de buffer menores que o tamanho total da textura e alterando os parâmetros x e y de `resource.set_texture()`.
:::

A textura pode ser usada diretamente em um [componente de modelo](/manuals/model/) usando `go.set()`:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Criando um atlas em runtime

Se a textura deve ser usada em um [componente de sprite](/manuals/sprite/), ela precisa primeiro ser usada por um atlas. Use [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) para criar um atlas:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- atribui o atlas ao componente 'sprite' no mesmo go
  go.set("#sprite", "image", my_atlas_id)

  -- reproduz a "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

As entradas de `frames` são índices baseados em 1 da tabela `geometries`. Uma lista pode reutilizar, reordenar ou ignorar geometrias, o que não pode ser representado pelos campos de intervalo obsoletos `frame_start` e `frame_end`. `resource.get_atlas()` retorna `frames`; use a mesma representação ao passar dados do atlas para `resource.set_atlas()` ou `resource.create_atlas()`. Os campos de intervalo ainda são aceitos pelo setter e pelo creator para manter a compatibilidade, mas códigos novos devem usar `frames`.
