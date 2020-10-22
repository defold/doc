---
title: Os Blocos Construtores do Defold
brief: Esse manual mostra detalhes relacionados ao funcionameno de objetos componentes e coleções.
---

#  Building blocks

No núcleo de design do Defold existem alguns conceitos que demandão um certo tempo para se acostumar. Esse manual explica como os building blocks do Defold funcionam. Após ler esse manual, vá para o [addressing manual](/manuals/addressing) e o [message passing manual](/manuals/message-passing). Existem também alguns [tutorials](/tutorials/getting-started) no editor, tutoriais esses que o farão decolar na utilização do Defold.

![Building blocks](images/building_blocks/building_blocks.png){srcset="images/building_blocks/building_blocks@2x.png 2x"}

Existem três tipos basicos de building blocks que você utilizará para construir um jogo no Defold:

Collection
: A collection,ou coleção em português, é um arquivo utilizado para estruturar seu jogo. Nas collections você constroi hierarquias de game objects e outras collections. Geralmente eles são utilizados para estruturar níveis do jogo, gropus de inimigos ou characters built de diversos game objects.

Game object
: Um game object é um container com um id,posição,rotação e escala. É utilizado para conter components. Eles sçao geralmente utilizados para criar personagens, balas, o sistema de regras do jogo ou o level loader/unloader(o que faz o jogo carregar o mapa).

Component
: Components são entidades que são colocadas nos game objects para lhes dar um visual, audio e ou representção lógica no jogo. Eles são utilizados comumente para criar character sprites, script files e para adicionar efeitos sonoros ou partículas.

## Collections

Collections são estruturas em modelo de "arvores" que seguram game objects e outras collections. Uma collections é sempre guardada em um arquivo.

Quando a engine do Defold se inicias, ela carrega uma única _bootstrap collection_ como especificado no arquivo "game.project". A bootstrap collection frequentemente é nomeada "main.collection" mas você pode usar qualquer nome.

Uma collection pode conter game objects e outras collections (por referência ao arquivo sub-collection's), que se encontrar alojado profundamente.Aqui vai um arqivo de exemplo chamado "main.collection". Ele contem um game object (com o id "can") e uma sub-collection (com o id "bean"). A sub-collection, citada, têm dois game objects: "bean" e "shield".

![Collection](images/building_blocks/collection.png){srcset="images/building_blocks/collection@2x.png 2x"}

Perceba que a sub-collection com o id "bean" está guardada em seu próprio arquivo, chamado "/main/bean.collection" qque só é referenciado em "main.collection":

![Bean collection](images/building_blocks/bean_collection.png){srcset="images/building_blocks/bean_collection@2x.png 2x"}

Você não pode endereçar collections para elas mesmas uma vez que não tem runtime objects correspondendo ao "main" e ao "bean" collections. De qualquer forma, de vez em quando você precisa usar o id de uma collection como parte do _path_ para um game object (olhe o [addressing manual](/manuals/addressing) para detalhes):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

:Uma collection é sempre adicionada a outra collection como uma referência para um arquivo de collection:

<kbd>Right-click</kbd> a collection na Outline view e selecione <kbd>Add Collection File</kbd>.

## Game objects

Game objects são objetos simples que têm separadamente um lifespan durante a execução do jogo. Game objects têm uma posição,rotação e escala , sendo cada um desses atributos manipulaveis e animados no runtime.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Game objects podem ser utilizados vazios (como position markers, para instancias) mas geralmente são utiliados com varios componentes como sprites,sounds,scripts,models,factories e outros. Game objects ou são criados no editor, posicionado nos collection files, ou spawnados dinamicamente no run-time por meio dos _factory_ components.

Game objects ou são adicionados no local exato na collection, ou adicionados a uma collection como uma referência a um game object file:

<kbd>Right-click</kbd> a collection no *Outline* view e selecionar <kbd>Add Game Object</kbd> (add in-place) or <kbd>Add Game Object File</kbd> (add as file reference).


## Components

:[components](../shared/components.md)

Refere-se ao [component overview](/manuals/components/) para uma lista completa de todos tipos de  component.

## Objects added in-place or by reference

Quando você cria uma collection,game object ou component file,você cria uma blueprint,ou um protótipo. Isso só adiciona um arquivo ao project file structure, nada é adicionado ao seu jogo rodando. Para adicionar uma instancia de uma collection,game object ou component baseado em blueprint file,você adiciona uma instancia disso e um de seus collection files.

Você pode ver em qual arquivo um object instance se baseia a partir da outline view. O arquivo "main.collection" contem 3 instancias que são baseadas em arquivos:

1. O "bean" sub-collection.
2. O "bean" script component no "bean" game object no "bean" sub-collection.
3. A "can" script component no "can" game object.

![Instance](images/building_blocks/instance.png){srcset="images/building_blocks/instance@2x.png 2x"}

O benefício de criar blueprint files se mostra quando você tem multiplas instancias de game objects ou collections e quer trocar todas elas:

![GO instances](images/building_blocks/go_instance.png){srcset="images/building_blocks/go_instance@2x.png 2x"}

Ao trocar o blueprint file,todas as instancias que o utilizam são atualizadas imediatamente.

![GO instances updated](images/building_blocks/go_instance2.png){srcset="images/building_blocks/go_instance2@2x.png 2x"}

## Childing game objects

Em um collection file, você pode criar hierarquias de game objects para que um ou mais game objects sejam children(filhas) para um único parent game object. Basta <kbd>dragging</kbd> um game object e <kbd>dropping</kbd> em outro dragged game object que é childed embaixo do target:

![Childing game objects](images/building_blocks/childing.png){srcset="images/building_blocks/childing@2x.png 2x"}

AS Hierarquias de Object parent-child são relações dinamicas que afetam como os objects reagem a transformações.Qualquer transformação(movimento,rotação ou escala) aplicadas ao object irão ser aplicadas também aos object's children, ambos no editor e no runtime :

![Child transform](images/building_blocks/child_transform.png){srcset="images/building_blocks/child_transform@2x.png 2x"}

Inversamente, um child's translations é realizado no espaço local do parent. No editor, você pode escolher editar um child game object no espaço local ou espaço do mundo selecionando <kbd>Edit ▸ World Space</kbd> (o padrão) ou <kbd>Edit ▸ Local Space</kbd>.

Também é possível alterar um object's parent no run-time ao enviar uma mensagem `set_parent` para o object.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Uma comum confusão ocorre quando falamos do lugar de um game object na hierarquia da collection muda quando ele vira parte uma uma hierarquia parent-child.Essas são duas coisas muito diferentes.Hierarquias Parent-child alteram dinamicamente a cena gráfica, o que possibilita os objetos se grudarem visualmente. A única coisa que dita um endereço de game object é o seu local na hierarquia de collections. O endereço é estático durante toda a vida de um objeto.
:::
