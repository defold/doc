---
title: Glossário do Defold
brief: Este manual lista tudo que você encontra ao trabalhar no Defold, com uma breve descrição.
---

# Glossário do Defold

Este glossário fornece uma breve descrição de tudo que você encontra no Defold. Na maioria dos casos, você encontrará um link para uma documentação mais aprofundada.

## Conjunto de animação

![Conjunto de animação](images/icons/animationset.png){.left} Um recurso de conjunto de animação contém uma lista de arquivos .dae ou outros arquivos .animationset de onde ler animações. Adicionar um arquivo .animationset a outro é útil se você compartilhar conjuntos parciais de animações entre vários modelos. Consulte o [manual de animação de modelo](/manuals/model-animation/) para detalhes.

## Atlas

![Atlas](images/icons/atlas.png){.left} Um atlas é um conjunto de imagens separadas que são compiladas em uma folha maior por motivos de desempenho e memória. Ele pode conter imagens estáticas ou séries de imagens animadas em flip-book. Atlas são usados por vários componentes para compartilhar recursos gráficos. Consulte a [documentação de Atlas](/manuals/atlas) para mais informações.

## Builtins

![Builtins](images/icons/builtins.png){.left} A pasta de projeto builtins é uma pasta somente leitura que contém recursos padrão úteis. Nela você encontra o renderizador padrão, script de renderização, materiais e mais. Se precisar de modificações personalizadas em qualquer um desses recursos, basta copiá-los para o seu projeto e editar como desejar.

## Câmera

![Câmera](images/icons/camera.png){.left} O componente de câmera ajuda a decidir qual parte do mundo do jogo deve ficar visível e como ela deve ser projetada. Um caso de uso comum é anexar uma câmera ao objeto de jogo do jogador, ou ter um objeto de jogo separado com uma câmera que segue o jogador com algum algoritmo de suavização. Consulte a [documentação de câmera](/manuals/camera) para mais informações.

## Objeto de colisão

![Objeto de colisão](images/icons/collision-object.png){.left} Objetos de colisão são componentes que estendem objetos de jogo com propriedades físicas (como forma espacial, peso, atrito e restituição). Essas propriedades controlam como o objeto de colisão deve colidir com outros objetos de colisão. Os tipos mais comuns de objetos de colisão são objetos cinemáticos, objetos dinâmicos e gatilhos. Um objeto cinemático fornece informações detalhadas de colisão às quais você precisa responder manualmente; um objeto dinâmico é simulado automaticamente pela engine de física para obedecer às leis newtonianas da física. Gatilhos são formas simples que detectam se outras formas entraram ou saíram do gatilho. Consulte a [documentação de física](/manuals/physics) para detalhes de como isso funciona.

## Componente

Componentes são usados para dar expressão e/ou funcionalidade específica a objetos de jogo, como gráficos, animação, comportamento programado e som. Eles não têm vida própria e precisam estar contidos dentro de objetos de jogo. Há muitos tipos de componentes disponíveis no Defold. Consulte [o manual de blocos de construção](/manuals/building-blocks) para uma descrição dos componentes.

## Coleção

![Coleção](images/icons/collection.png){.left} Coleções são o mecanismo do Defold para criar templates, ou o que em outras engines é chamado de "prefabs", em que hierarquias de objetos de jogo podem ser reutilizadas. Coleções são estruturas em árvore que contêm objetos de jogo e outras coleções. Uma coleção sempre é armazenada em arquivo e trazida para o jogo de forma estática, ao ser posicionada manualmente no editor, ou de forma dinâmica, ao ser criada. Consulte [o manual de blocos de construção](/manuals/building-blocks) para uma descrição das coleções.

## Fábrica de coleção

![Fábrica de coleção](images/icons/collection-factory.png){.left} Um componente de fábrica de coleção é usado para criar hierarquias de objetos de jogo dinamicamente em um jogo em execução. Consulte o [manual de fábrica de coleção](/manuals/collection-factory) para detalhes.

## Proxy de coleção

![Coleção](images/icons/collection.png){.left} Um proxy de coleção é usado para carregar e habilitar coleções em tempo real enquanto um aplicativo ou jogo está em execução. O caso de uso mais comum para proxies de coleção é carregar níveis conforme eles devem ser jogados. Consulte a [documentação de proxy de coleção](/manuals/collection-proxy) para detalhes.

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} Um cubemap é um tipo especial de textura que consiste em 6 texturas diferentes mapeadas nos lados de um cubo. Isso é útil para renderizar skyboxes e diferentes tipos de mapas de reflexão e iluminação.

## Depuração

Em algum momento seu jogo se comportará de forma inesperada e você precisará descobrir o que está errado. Aprender a depurar é uma arte e, felizmente, o Defold vem com um depurador integrado para ajudar. Consulte o [manual de depuração](/manuals/debugging) para mais informações.

## Perfis de exibição

![Perfis de exibição](images/icons/display-profiles.png){.left} O arquivo de recurso de perfis de exibição é usado para especificar layouts de GUI dependendo da orientação, proporção de tela ou modelo do dispositivo. Ele ajuda a adaptar sua UI para qualquer tipo de dispositivo. Leia mais no [manual de layouts](/manuals/gui-layouts).

## Fábrica

![Fábrica](images/icons/factory.png){.left} Em algumas situações, você não consegue posicionar manualmente todos os objetos de jogo necessários em uma coleção; precisa criar os objetos de jogo dinamicamente, em tempo real. Por exemplo, um jogador pode disparar projéteis e cada disparo deve ser criado dinamicamente e lançado sempre que o jogador pressionar o gatilho. Para criar objetos de jogo dinamicamente (a partir de um pool de objetos pré-alocado), você usa um componente de fábrica. Consulte o [manual de fábrica](/manuals/factory) para detalhes.

## Fonte

![Arquivo de fonte](images/icons/font.png){.left} Um recurso Font é criado a partir de um arquivo de fonte TrueType ou OpenType. A Font especifica em que tamanho a fonte será renderizada e que tipo de decoração (contorno e sombra) a fonte renderizada deve ter. Fontes são usadas por componentes GUI e Label. Consulte o [manual de fonte](/manuals/font/) para detalhes.

## Fragment shader

![Fragment shader](images/icons/fragment-shader.png){.left} Este é um programa executado no processador gráfico para cada pixel (fragmento) em um polígono quando ele é desenhado na tela. O objetivo do fragment shader é decidir a cor de cada fragmento resultante. Isso é feito por cálculo, buscas de textura (uma ou várias) ou uma combinação de buscas e cálculos. Consulte o [manual de shader](/manuals/shader) para mais informações.

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} Um arquivo de recurso de gamepads define como a entrada de um dispositivo gamepad específico é mapeada para gatilhos de entrada de gamepad em uma determinada plataforma. Consulte o [manual de entrada](/manuals/input) para detalhes.

## Objeto de jogo

![Objeto de jogo](images/icons/game-object.png){.left} Objetos de jogo são objetos simples com um tempo de vida separado durante a execução do jogo. Objetos de jogo são contêineres e normalmente vêm equipados com componentes visuais ou audíveis, como um som ou um sprite. Eles também podem receber comportamento por meio de componentes de script. Você cria objetos de jogo e os posiciona em coleções no editor, ou os cria dinamicamente em tempo de execução com fábricas. Consulte [o manual de blocos de construção](/manuals/building-blocks) para uma descrição dos objetos de jogo.

## GUI

![Componente GUI](images/icons/gui.png){.left} Um componente GUI contém elementos usados para construir interfaces de usuário: texto e blocos coloridos e/ou texturizados. Os elementos podem ser organizados em estruturas hierárquicas, receber scripts e ser animados. Componentes GUI normalmente são usados para criar heads-up displays, sistemas de menu e notificações na tela. Componentes GUI são controlados com scripts de GUI que definem o comportamento da GUI e controlam a interação do usuário com ela. Leia mais na [documentação de GUI](/manuals/gui).

## Script de GUI

![Script de GUI](images/icons/script.png){.left} Scripts de GUI são usados para controlar o comportamento de componentes GUI. Eles controlam animações de GUI e como o usuário interage com a GUI. Consulte o [manual de Lua no Defold](/manuals/lua) para detalhes sobre como scripts Lua são usados no Defold.

## Hot reload

O editor Defold permite atualizar conteúdo em um jogo que já está em execução, no desktop e no dispositivo. Esse recurso é extremamente poderoso e pode melhorar bastante o fluxo de desenvolvimento. Consulte o [manual de hot reload](/manuals/hot-reload) para mais informações.

## Mapeamento de entrada

![Mapeamento de entrada](images/icons/input-binding.png){.left} Arquivos de mapeamento de entrada definem como o jogo deve interpretar entrada de hardware (mouse, teclado, tela sensível ao toque e gamepad). O arquivo vincula entrada de hardware a _ações_ de entrada de alto nível, como "jump" e "move_forward". Em componentes de script que escutam entrada, você pode programar as ações que o jogo ou aplicativo deve executar dada determinada entrada. Consulte a [documentação de entrada](/manuals/input) para detalhes.

## Rótulo

![Rótulo](images/icons/label.png){.left} O componente label permite anexar conteúdo de texto a qualquer objeto de jogo. Ele renderiza um trecho de texto com uma fonte específica na tela, no espaço do jogo. Consulte o [manual de label](/manuals/label) para mais informações.

## Biblioteca

![Objeto de jogo](images/icons/builtins.png){.left} O Defold permite compartilhar dados entre projetos por meio de um poderoso mecanismo de bibliotecas. Você pode usá-lo para configurar bibliotecas compartilhadas acessíveis por todos os seus projetos, seja apenas para você ou para toda a equipe. Leia mais sobre o mecanismo de bibliotecas na [documentação de Bibliotecas](/manuals/libraries).

## Linguagem Lua

A linguagem de programação Lua é usada no Defold para criar lógica de jogo. Lua é uma linguagem de script poderosa, eficiente e muito pequena. Ela oferece suporte a programação procedural, programação orientada a objetos, programação funcional, programação orientada a dados e descrição de dados. Você pode ler mais sobre a linguagem na página oficial do Lua em https://www.lua.org/ e no [manual de Lua no Defold](/manuals/lua).

## Módulo Lua

![Módulo Lua](images/icons/lua-module.png){.left} Módulos Lua permitem estruturar seu projeto e criar código de biblioteca reutilizável. Leia mais no [manual de módulos Lua](/manuals/modules/).

## Material

![Material](images/icons/material.png){.left} Materiais definem como diferentes objetos devem ser renderizados ao especificar shaders e suas propriedades. Consulte o [manual de material](/manuals/material) para mais informações.

## Mensagem

Componentes se comunicam entre si e com outros sistemas por passagem de mensagens. Componentes também respondem a um conjunto de mensagens predefinidas que os alteram ou disparam ações específicas. Você envia mensagens para ocultar gráficos ou mover levemente objetos de física. A engine também usa mensagens para notificar componentes sobre eventos, por exemplo quando formas de física colidem. O mecanismo de passagem de mensagens precisa de um destinatário para cada mensagem enviada. Portanto, tudo no jogo é endereçado de forma única. Para permitir comunicação entre objetos, o Defold estende Lua com passagem de mensagens. O Defold também fornece uma biblioteca de funções úteis.

Por exemplo, o código Lua necessário para ocultar um componente de sprite em um objeto de jogo é:

```lua
msg.post("#weapon", "disable")
```

Aqui, `"#weapon"` é o endereço do componente de sprite do objeto atual. `"disable"` é uma mensagem à qual componentes de sprite respondem. Consulte a [documentação de passagem de mensagens](/manuals/message-passing) para uma explicação detalhada de como a passagem de mensagens funciona.

## Modelo

![Modelo](images/icons/model.png){.left} O componente de modelo 3D pode importar assets de malha, esqueleto e animação glTF para o seu jogo. Consulte o [manual de modelo](/manuals/model/) para mais informações.

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Partículas são muito úteis para criar efeitos visuais interessantes, especialmente em jogos. Você pode usá-las para criar névoa, fumaça, fogo, chuva ou folhas caindo. O Defold contém um poderoso editor de efeitos de partículas que permite criar e ajustar efeitos enquanto os executa em tempo real no seu jogo. A [documentação de ParticleFX](/manuals/particlefx) fornece os detalhes de como isso funciona.

## Profiling

Bom desempenho é essencial em jogos, e é vital que você consiga fazer profiling de desempenho e memória para medir seu jogo e identificar gargalos de desempenho e problemas de memória que precisam ser corrigidos. Consulte o [manual de profiling](/manuals/profiling) para mais informações sobre as ferramentas de profiling disponíveis no Defold.

## Render

![Render](images/icons/render.png){.left} Arquivos Render contêm configurações usadas ao renderizar o jogo na tela. Arquivos Render definem qual script de renderização usar para renderizar e quais materiais usar. Consulte o [manual de renderização](/manuals/render/) para mais detalhes.

## Script de renderização

![Script de renderização](images/icons/script.png){.left} Um script de renderização é um script Lua que controla como o jogo ou aplicativo deve ser renderizado na tela. Há um script de renderização padrão que cobre a maioria dos casos comuns, mas você pode escrever o seu próprio se precisar de modelos de iluminação personalizados e outros efeitos. Consulte o [manual de renderização](/manuals/render/) para mais detalhes sobre como o pipeline de renderização funciona, e o [manual de Lua no Defold](/manuals/lua) para detalhes sobre como scripts Lua são usados no Defold.

## Script

![Script](images/icons/script.png){.left} Um script é um componente que contém um programa que define comportamentos de objetos de jogo. Com scripts, você pode especificar as regras do seu jogo e como os objetos devem responder a várias interações (com o jogador e também com outros objetos). Todos os scripts são escritos na linguagem de programação Lua. Para trabalhar com o Defold, você ou alguém da sua equipe precisa aprender a programar em Lua. Consulte o [manual de Lua no Defold](/manuals/lua) para uma visão geral de Lua e detalhes sobre como scripts Lua são usados no Defold.

## Som

![Som](images/icons/sound.png){.left} O componente de som é responsável por reproduzir um som específico. Atualmente, o Defold oferece suporte a arquivos de som nos formatos WAV e Ogg Vorbis. Consulte o [manual de som](/manuals/sound) para mais informações.

## Sprite

![Sprite](images/icons/sprite.png){.left} Um sprite é um componente que estende objetos de jogo com gráficos. Ele exibe uma imagem de uma Tile source ou de um Atlas. Sprites têm suporte integrado a animação flip-book e animação por bones. Sprites normalmente são usados para personagens e itens.

## Perfis de textura

![Perfis de textura](images/icons/texture-profiles.png){.left} O arquivo de recurso de perfis de textura é usado no processo de empacotamento para processar e comprimir automaticamente dados de imagem (em Atlas, Tile sources, Cubemaps e texturas avulsas usadas por modelos, GUI etc.). Leia mais no [manual de perfis de textura](/manuals/texture-profiles).

## Tile map

![Tile map](images/icons/tilemap.png){.left} Componentes Tile map exibem imagens de uma tile source em uma ou mais grades sobrepostas. Eles são usados mais frequentemente para construir ambientes de jogo: chão, paredes, construções e obstáculos. Um tile map pode exibir várias camadas alinhadas umas sobre as outras com um modo de mesclagem especificado. Isso é útil, por exemplo, para colocar folhagem sobre tiles de fundo de grama. Também é possível alterar dinamicamente a imagem exibida em um tile. Isso permite, por exemplo, destruir uma ponte e torná-la intransponível simplesmente substituindo os tiles por outros que representem a ponte destruída e contenham a forma física correspondente. Consulte a [documentação de Tile map](/manuals/tilemap) para mais informações.

## Tile source

![Tile source](images/icons/tilesource.png){.left} Uma tile source descreve uma textura composta por várias imagens menores, todas com o mesmo tamanho. Você pode definir animações flip-book a partir de uma sequência de imagens em uma tile source. Tile sources também podem calcular automaticamente formas de colisão a partir dos dados da imagem. Isso é muito útil para criar níveis em tiles com os quais objetos possam colidir e interagir. Tile sources são usadas por componentes Tile map (e Sprite e ParticleFX) para compartilhar recursos gráficos. Observe que Atlases muitas vezes são uma opção melhor que tile sources. Consulte a [documentação de Tile map](/manuals/tilemap) para mais informações.

## Vertex shader

![Vertex shader](images/icons/vertex-shader.png){.left} O vertex shader calcula a geometria de tela das formas poligonais primitivas de um componente. Para qualquer tipo de componente visual, seja um sprite, tilemap ou modelo, a forma é representada por um conjunto de posições de vértices de polígono. O programa vertex shader processa cada vértice (no espaço do mundo) e calcula a coordenada resultante que cada vértice de uma primitiva deve ter. Consulte o [manual de shader](/manuals/shader) para mais informações.
