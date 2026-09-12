---
title: Formas de colisão
brief: Objetos de colisão podem conter formas primitivas, cascos convexos ou malhas de triângulos, ou usar recursos de tilemap e formas convexas.
---

# Formas de colisão

Um objeto de colisão pode conter várias formas incorporadas. Na física 3D, elas podem incluir cascos convexos e malhas de triângulos de arquivos glTF ou GLB. Você também pode usar um tilemap ou um recurso de forma convexa pela propriedade *Collision Shape* do objeto de colisão.

### Formas primitivas
As formas primitivas são *box*, *sphere* e *capsule*. Você adiciona uma forma primitiva clicando com o botão direito no objeto de colisão e selecionando <kbd>Add Shape</kbd>:

![Add a primitive shape](images/physics/add_shape.png)

## Forma box
Uma box tem posição, rotação e dimensões (largura, altura e profundidade):

![Box shape](images/physics/box.png)

## Forma sphere
Uma sphere tem posição, rotação e diâmetro:

![Sphere shape](images/physics/sphere.png)

## Forma capsule
Uma capsule tem posição, rotação, diâmetro e altura:

![Sphere shape](images/physics/capsule.png)

::: important
Formas capsule são suportadas apenas ao usar física 3D (configurada na seção Physics do arquivo *game.project*).
:::

### Formas complexas
Formas complexas podem usar a geometria de tilemaps ou dados de cascos convexos. Desde o Defold 1.13.2, objetos de colisão 3D também podem criar cascos convexos e formas de malhas de triângulos a partir de malhas em cenas glTF ou GLB.

## Formas Hull e Mesh em 3D {#hull-and-mesh-shapes-in-3d}

Use uma forma *Hull* para uma aproximação convexa de uma malha, ou uma forma *Mesh* quando as colisões precisarem seguir seus triângulos, incluindo áreas côncavas como aberturas na geometria de um nível.

1. Defina **Physics → Type** como `3D` no *game.project*.
2. Clique com o botão direito no objeto de colisão no *Outline* e selecione <kbd>Add Shape ▸ Hull</kbd> ou <kbd>Add Shape ▸ Mesh</kbd>.
3. Selecione a nova forma e defina sua propriedade *Scene* para um arquivo *.gltf* ou *.glb*.
4. Selecione uma malha nomeada no campo *Mesh*. Se ela não aparecer na lista, dê um nome à malha na sua ferramenta de modelagem e exporte a cena novamente.
5. Posicione e gire a forma para alinhá-la à geometria visível do objeto de jogo. Repita esses passos para adicionar mais formas, se necessário.

A malha selecionada fornece sua geometria local; as transformações dos nós glTF não são aplicadas. As formas de colisão Mesh são compatíveis com o backend Bullet 3D, incluindo objetos de colisão estáticos e não estáticos. Elas não são compatíveis com os backends de física 2D.

A geometria da malha de triângulos é somente leitura pelas APIs de formas em tempo de execução. Edite a malha original e faça um novo build para alterar seus triângulos. Consulte [escala de formas de colisão](#scaling-collision-shapes) para saber sobre a escala do objeto de jogo.

## Forma de colisão de tilemap
O Defold inclui um recurso que permite gerar facilmente formas de física para o tile source usado por um tile map. O [manual de Tilesource](/manuals/tilesource/#tile-source-collision-shapes) explica como adicionar grupos de colisão a um tile source e atribuir tiles a grupos de colisão ([exemplo](/examples/tilemap/collisions/)).

Para adicionar colisão a um tile map:

1. Adicione o tilemap a um objeto de jogo clicando com o botão direito no objeto de jogo e selecionando <kbd>Add Component File</kbd>. Selecione o arquivo de tile map.
2. Adicione um componente de objeto de colisão ao objeto de jogo clicando com o botão direito no objeto de jogo e selecionando <kbd>Add Component ▸ Collision Object</kbd>.
3. Em vez de adicionar formas ao componente, defina a propriedade *Collision Shape* para o arquivo *tilemap*.
4. Configure as *Properties* do componente de objeto de colisão normalmente.

![Tilesource collision](images/physics/collision_tilemap.png)

::: important
Observe que a propriedade *Group* **não** é usada aqui, pois os grupos de colisão são definidos no tile source do tile map.
:::

## Forma de casco convexo
Na física 3D, você pode criar um casco convexo diretamente de uma malha usando o [fluxo de trabalho do editor descrito acima](#hull-and-mesh-shapes-in-3d). O recurso antigo `.convexshape` também é compatível e pode ser criado a partir de pontos usando um editor externo:

1. Crie um arquivo de forma de casco convexo (extensão de arquivo `.convexshape`) usando um editor externo.
2. Edite o arquivo manualmente usando um editor de texto ou ferramenta externa (veja abaixo)
3. Em vez de adicionar formas ao componente de objeto de colisão, defina a propriedade *Collision Shape* para o arquivo de *convex shape*.

### Formato do arquivo
O formato de arquivo de casco convexo usa o mesmo formato de dados de todos os outros arquivos Defold, ou seja, o formato de texto protobuf. Uma forma de casco convexo define os pontos do casco. Em física 2D, os pontos devem ser fornecidos em sentido anti-horário. Uma nuvem abstrata de pontos é usada no modo de física 3D. Exemplo 2D:

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

O exemplo acima define os quatro cantos de um retângulo:

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## Ferramentas externas

Há várias ferramentas externas diferentes que podem ser usadas para criar formas de colisão:

* O [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) da CodeAndWeb pode ser usado para criar objetos de jogo com sprites e formas de colisão correspondentes.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) pode ser usado para criar formas de casco convexo.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) pode ser usado para criar formas de casco convexo.


<a id="scaling-collision-shapes"></a>

# Escalando formas de colisão
O objeto de colisão e suas formas herdam a escala do objeto de jogo. Para desabilitar esse comportamento, desmarque a caixa de seleção [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) na seção Physics de *game.project*. Observe que apenas escala uniforme é suportada e que o menor valor de escala será usado se a escala não for uniforme.

# Redimensionando formas de colisão
Formas primitivas podem ser redimensionadas em tempo de execução usando `physics.set_shape()`. Essa função não substitui vértices de cascos convexos nem a geometria de malhas de triângulos. Exemplo:

```lua
-- define dados da forma capsule
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- define dados da forma sphere
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- define dados da forma box
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
Uma forma do tipo correto com o id especificado já deve existir no objeto de colisão.
:::

# Rotacionando formas de colisão

## Rotacionando formas de colisão em física 3D
Formas de colisão em física 3D podem ser rotacionadas ao redor de todos os eixos.


## Rotacionando formas de colisão em física 2D
Formas de colisão em física 2D só podem ser rotacionadas ao redor do eixo z. Rotação ao redor do eixo x ou y produzirá resultados incorretos e deve ser evitada, mesmo ao rotacionar 180 graus para essencialmente inverter a forma ao longo do eixo x ou y. Para inverter uma forma de física, é recomendado usar [`physics.set_hflip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) e [`physics.set_vflip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip).


# Depuração
Você pode [habilitar a depuração de Física](/manuals/debugging-game-logic/#debugging-problems-with-physics) para ver as formas de colisão em tempo de execução.
