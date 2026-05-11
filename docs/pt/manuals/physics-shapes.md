---
title: Formas de colisão
brief: Um componente de colisão pode usar várias formas primitivas ou uma única forma complexa.
---

# Formas de colisão

Um componente de colisão pode usar várias formas primitivas ou uma única forma complexa.

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
Uma forma complexa pode ser criada a partir de um componente tilemap ou de uma forma de casco convexo.

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
O Defold inclui um recurso que permite criar uma forma de casco convexo a partir de três ou mais pontos.

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


# Escalando formas de colisão
O objeto de colisão e suas formas herdam a escala do objeto de jogo. Para desabilitar esse comportamento, desmarque a caixa de seleção [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) na seção Physics de *game.project*. Observe que apenas escala uniforme é suportada e que o menor valor de escala será usado se a escala não for uniforme.

# Redimensionando formas de colisão
As formas de um objeto de colisão podem ser redimensionadas em tempo de execução usando `physics.set_shape()`. Exemplo:

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
Você pode [habilitar a depuração de Física](/manuals/debugging/#debugging-problems-with-physics) para ver as formas de colisão em tempo de execução.
