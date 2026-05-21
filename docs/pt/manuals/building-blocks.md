---
title: Os blocos de construção do Defold
brief: Este manual detalha como objetos de jogo, componentes e coleções funcionam.
---

#  Blocos de construção

No centro do design do Defold há alguns conceitos muito importantes para entender bem. Este manual explica em que consistem os blocos de construção do Defold. Depois de ler este manual, siga para o [manual de endereçamento](/manuals/addressing) e o [manual de passagem de mensagens](/manuals/message-passing). Também há um conjunto de [tutoriais](/tutorials/getting-started) disponíveis dentro do editor para você começar rapidamente.

![Building blocks](images/building_blocks/building_blocks.png)

Há três tipos básicos de blocos de construção usados para criar um jogo no Defold:

Coleção
: Uma coleção é um arquivo usado para estruturar seu jogo. Em coleções, você monta hierarquias de objetos de jogo e outras coleções. Elas normalmente são usadas para estruturar níveis do jogo, grupos de inimigos ou personagens formados por vários objetos de jogo.

Objeto de jogo
: Um objeto de jogo é um contêiner com id, posição, rotação e escala. Ele é usado para conter componentes. Objetos de jogo normalmente são usados para criar personagens do jogador, projéteis, o sistema de regras do jogo ou um carregador/descarregador de níveis.

Componente
: Componentes são entidades colocadas em objetos de jogo para dar a eles representação visual, sonora e/ou lógica no jogo. Eles normalmente são usados para criar sprites de personagens, arquivos de script, efeitos sonoros ou efeitos de partículas.

## Coleções

Coleções são estruturas em árvore que contêm objetos de jogo e outras coleções. Uma coleção sempre é armazenada em um arquivo.

Quando a engine Defold inicia, ela carrega uma única _bootstrap collection_, conforme especificado no arquivo de configurações *game.project*. A coleção bootstrap costuma se chamar "main.collection", mas você pode usar qualquer nome.

Uma coleção pode conter objetos de jogo e outras coleções (por referência ao arquivo da subcoleção), aninhados em qualquer profundidade. Aqui está um arquivo de exemplo chamado "main.collection". Ele contém um objeto de jogo (com o id "can") e uma subcoleção (com o id "bean"). A subcoleção, por sua vez, contém dois objetos de jogo: "bean" e "shield".

![Collection](images/building_blocks/collection.png)

Observe que a subcoleção com id "bean" fica armazenada em seu próprio arquivo, chamado "/main/bean.collection", e é apenas referenciada em "main.collection":

![Bean collection](images/building_blocks/bean_collection.png)

Você não pode endereçar as coleções em si, já que não há objetos em tempo de execução correspondentes às coleções "main" e "bean". No entanto, às vezes você precisa usar a identidade de uma coleção como parte do _path_ para um objeto de jogo (consulte o [manual de endereçamento](/manuals/addressing) para detalhes):

```lua
-- arquivo: can.script
-- obtém a posição do objeto de jogo "bean" na coleção "bean"
local pos = go.get_position("bean/bean")
```

Uma coleção sempre é adicionada a outra coleção como uma referência a um arquivo de coleção:

<kbd>Right-click</kbd> na coleção na visualização *Outline* e selecione <kbd>Add Collection File</kbd>.

## Objetos de jogo

Objetos de jogo são objetos simples, cada um com um tempo de vida separado durante a execução do jogo. Objetos de jogo têm posição, rotação e escala, e cada uma dessas propriedades pode ser manipulada e animada em tempo de execução.

```lua
-- anima a posição X do objeto de jogo "can"
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Objetos de jogo podem ser usados vazios (como marcadores de posição, por exemplo), mas geralmente recebem vários componentes, como sprites, sons, scripts, modelos, fábricas e outros. Objetos de jogo são criados no editor, colocados em arquivos de coleção ou criados dinamicamente em tempo de execução por meio de componentes de _factory_.

Objetos de jogo podem ser adicionados diretamente no local em uma coleção ou adicionados a uma coleção como referência a um arquivo de objeto de jogo:

<kbd>Right-click</kbd> na coleção na visualização *Outline* e selecione <kbd>Add Game Object</kbd> (adicionar no local) ou <kbd>Add Game Object File</kbd> (adicionar como referência de arquivo).


## Componentes

:[components](../shared/components.md)

Consulte a [visão geral de componentes](/manuals/components/) para uma lista completa de todos os tipos de componente disponíveis.

## Objetos adicionados no local ou por referência

Quando você cria um _arquivo_ de coleção, objeto de jogo ou componente, você cria o que chamamos de protótipo (também conhecido como "prefab" ou "blueprint" em outras engines). Isso apenas adiciona um arquivo à estrutura de arquivos do projeto; nada é adicionado ao jogo em execução. Para adicionar uma instância de uma coleção, objeto de jogo ou componente baseada em um arquivo de protótipo, você adiciona uma instância dele em um dos seus arquivos de coleção.

Você pode ver em qual arquivo uma instância de objeto se baseia na visualização Outline. O arquivo "main.collection" contém três instâncias baseadas em arquivos:

1. A subcoleção "bean".
2. O componente de script "bean" no objeto de jogo "bean" da subcoleção "bean".
3. O componente de script "can" no objeto de jogo "can".

![Instance](images/building_blocks/instance.png)

A vantagem de criar arquivos de protótipo fica clara quando você tem várias instâncias de um objeto de jogo ou coleção e quer alterar todas elas:

![GO instances](images/building_blocks/go_instance.png)

Ao alterar o arquivo de protótipo, qualquer instância que usa esse arquivo é atualizada imediatamente.

![GO changing prototype](images/building_blocks/go_change_blueprint.png)

Aqui, a imagem do sprite no arquivo de protótipo é alterada e, imediatamente, todas as instâncias que usam o arquivo são atualizadas:

![GO instances updated](images/building_blocks/go_instance2.png)

## Objetos de jogo filhos

Em um arquivo de coleção, você pode criar hierarquias de objetos de jogo para que um ou mais objetos sejam filhos de um único objeto de jogo pai. Basta <kbd>arrastar</kbd> um objeto de jogo e <kbd>soltar</kbd> sobre outro para que o objeto arrastado se torne filho do alvo:

![Childing game objects](images/building_blocks/childing.png)

Hierarquias pai-filho entre objetos são relações dinâmicas que afetam como os objetos reagem a transformações. Qualquer transformação (movimento, rotação ou escala) aplicada a um objeto também será aplicada aos filhos desse objeto, tanto no editor quanto em tempo de execução:

![Child transform](images/building_blocks/child_transform.png)

Por outro lado, as translações de um filho são feitas no espaço local do pai. No editor, você pode escolher editar um objeto de jogo filho no espaço local ou no espaço do mundo selecionando <kbd>Edit ▸ World Space</kbd> (o padrão) ou <kbd>Edit ▸ Local Space</kbd>.

Também é possível alterar o pai de um objeto em tempo de execução enviando uma mensagem `set_parent` para o objeto.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Um equívoco comum é achar que o lugar de um objeto de jogo na hierarquia da coleção muda quando ele passa a fazer parte de uma hierarquia pai-filho. Porém, essas são duas coisas bem diferentes. Hierarquias pai-filho alteram dinamicamente o grafo de cena, permitindo que objetos fiquem visualmente anexados uns aos outros. A única coisa que determina o endereço de um objeto de jogo é seu lugar na hierarquia de coleções. O endereço é estático durante todo o tempo de vida do objeto.
:::
