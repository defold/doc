---
title: Importando e editando assets
brief: Este manual aborda como importar e editar assets.
---

# Importando e editando assets

Um projeto de jogo geralmente consiste em um grande número de assets externos produzidos em vários programas especializados para criar gráficos, modelos 3D, arquivos de som, animações e assim por diante. O Defold foi criado para um fluxo de trabalho em que você trabalha nas suas ferramentas externas e depois importa os assets para o Defold conforme eles são finalizados.


## Importando assets

O Defold precisa que todos os assets usados no seu projeto estejam localizados em algum lugar da hierarquia do projeto. Portanto, você precisa importar todos os assets antes de poder usá-los. Para importar assets, basta arrastar os arquivos do sistema de arquivos do seu computador e soltá-los em um local apropriado no *painel Conteúdo* do editor Defold.

![Importing files](images/graphics/import.png)

::: sidenote
O Defold oferece suporte a imagens nos formatos PNG e JPEG. Imagens PNG devem estar no formato RGBA de 32 bits. Outros formatos de imagem precisam ser convertidos antes de poderem ser usados.
:::


## Usando assets

Quando os assets são importados para o Defold, eles podem ser usados pelos vários tipos de componente compatíveis com o Defold:

* Imagens podem ser usadas para criar muitos tipos de componentes visuais frequentemente usados em jogos 2D. Leia mais sobre [como importar e usar gráficos 2D aqui](/manuals/importing-graphics).
* Sons podem ser usados pelo [componente de Som](/manuals/sound) para reproduzir sons.
* Fontes são usadas pelo [componente de Rótulo](/manuals/label) e por [nodes de texto](/manuals/gui-text) em uma GUI.
* Modelos glTF (*.gltf* e *.glb*) podem ser usados pelo [componente de Modelo](/manuals/model) para mostrar modelos 3D com animações. Importe como assets separados quaisquer imagens de textura usadas pelo modelo e atribua-as nas propriedades de textura do material do componente de Modelo. Leia mais sobre [como importar e usar modelos 3D aqui](/manuals/importing-models).


## Editando assets externos

O Defold não fornece ferramentas de edição para imagens, arquivos de som, modelos ou animações. Esses assets precisam ser criados fora do Defold em ferramentas especializadas e importados para o Defold. O Defold detecta automaticamente alterações em qualquer asset entre os arquivos do seu projeto e atualiza a visualização do editor conforme necessário.


## Editando assets do Defold

O editor salva todos os assets do Defold em arquivos baseados em texto que são amigáveis para merge. Eles também são fáceis de criar e modificar com scripts simples. Consulte [este tópico do fórum](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) para mais informações. Observe, porém, que não publicamos os detalhes do nosso formato de arquivo, pois eles mudam de tempos em tempos. Você também pode usar [Editor Scripts](/manuals/editor-scripts/) para se conectar a certos eventos de ciclo de vida no editor e executar scripts para gerar ou modificar assets.

Tenha cuidado extra ao trabalhar com arquivos de asset do Defold por meio de um editor de texto ou ferramenta externa. Se você introduzir erros, eles podem impedir que o arquivo seja aberto no editor Defold.

Algumas ferramentas externas, como [Tiled](/assets/tiled/) e [Tilesetter](https://www.tilesetter.org/beta), podem ser usadas para gerar assets do Defold automaticamente.
