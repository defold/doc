---
title: Exemplo de mapa RPG
brief: Neste projeto de exemplo, você aprende um método para criar mapas de RPG muito grandes.
---
# Mapa RPG - projeto de exemplo

Neste projeto de exemplo, que você pode [abrir pelo editor](/manuals/project-setup/) ou [baixar do GitHub](https://github.com/defold/sample-rpgmap), mostramos um método para criar mapas de RPG muito grandes no Defold. O design se baseia nas seguintes premissas:

1. O mundo é apresentado uma tela por vez. Isso permite que o jogo mantenha naturalmente inimigos e personagens NPC dentro dos limites de uma única tela. O designer de níveis tem controle total sobre como o mundo é apresentado na tela do jogador.
2. O personagem do jogador deve conseguir viajar uma distância arbitrariamente grande sem que o jogo apresente problemas de precisão de ponto flutuante. Esses problemas geralmente fazem objetos tremularem de forma estranha quando se afastam muito da origem.
3. O movimento do jogador é restringido por obstáculos no mapa, para que o designer de níveis possa conduzir o jogador entre telas usando árvores, pedras, água e outros obstáculos.
4. Deve ser possível combinar tilemaps, sprites e outros conteúdos visuais.

Primeiro, execute o exemplo e caminhe pelo mundo de 3x3 telas para entender a organização do exemplo. Você controla o personagem com as setas do teclado.

## A coleção principal

Abra "/main/main.collection" para ver a coleção bootstrap deste exemplo.

![](images/rpgmap/main_collection.png)

A coleção principal contém o objeto de jogo do personagem do jogador, controlado em 8 direções com as setas, e um segundo objeto de jogo chamado "game", que controla o fluxo do jogo. O objeto "game" consiste em um script e uma fábrica de coleção para cada tela do jogo. As fábricas são nomeadas de acordo com o esquema de nomes da grade de telas.

O script "/main/game.script" rastreia em qual tela o jogador está atualmente. O script também reage a uma mensagem personalizada chamada "load_screen". Essa mensagem carrega uma nova tela e a troca com a tela atual na direção em que o herói se move. Inicialmente, uma tela é carregada no centro da tela e não há outra tela para trocar de lugar com ela.

## Trocando de tela

O herói é controlado pelo script "/main/hero.script". O script verifica se o objeto de jogo do herói passa por uma linha superior, inferior, esquerda ou direita próxima à borda da tela:

![](images/rpgmap/change_screen.png)

1. Se o herói se mover perto o bastante de uma borda da tela, uma mensagem é enviada ao script do objeto "game" para carregar a próxima tela.
2. A próxima coleção de tela é criada chamando `factory.create()` no componente collectionfactory correto. O conteúdo da coleção é posicionado fora da tela.
3. A próxima tela desliza para o centro da visualização e a tela atual desliza para fora na direção oposta. O personagem do jogador também desliza a mesma distância e com a mesma velocidade.
4. A tela atual antiga, que agora está fora da tela, é removida, e a próxima tela é promovida a nova tela atual.
5. O herói anima para dentro da nova tela e o jogador recupera o controle.

Tudo isso acontece em menos de um segundo, então a transição é suave e não atrapalha o fluxo.

## Telas

Cada tela no mundo do jogo é construída dentro de uma coleção separada contendo o tilemap, o objeto de colisão e outros objetos de jogo exclusivos daquela tela. Para facilitar o gerenciamento e o carregamento das telas, as coleções de tela são nomeadas de acordo com um esquema simples:

![](images/rpgmap/screens.png)

Cada coleção de tela é nomeada de acordo com sua posição na grade do mundo. O primeiro número é a posição X na grade, e o segundo é a posição Y na grade.

Na visualização *Assets*, navegue até a coleção "/main/screens/0-0.collection" e abra-a. Ela descreve a tela no canto inferior esquerdo do mapa:

![](images/rpgmap/screen_collection.png)

Observe que há um objeto de jogo chamado "root" que é pai de todo o conteúdo da tela. Essa é outra convenção usada no exemplo e tem um propósito muito importante: quando uma tela é trazida para a visualização, apenas o objeto de jogo "root" precisa ser movido. Todos os objetos filhos são movidos automaticamente junto com o pai raiz. Se houver objetos de jogo especiais em uma tela, eles também podem ser animados livremente, já que seu movimento é relativo ao pai raiz. Quando a tela entra ou sai deslizando, esses filhos se movem junto com a tela. Código especial só é necessário se um objeto precisar se mover entre telas.

As abelhas na tela 0-1 são demonstrações simples dessa ideia:

![](images/rpgmap/bees.png)

## Editando telas no contexto do mundo

Cada tela tem seu próprio tilemap, que pode ser editado no editor de tilemap integrado. Porém, a principal desvantagem de editar cada tela isoladamente é que não é possível ver com facilidade como ela se conecta às telas adjacentes, algo importante para criar continuidade no mundo do jogo.

Por esse motivo, uma coleção especial foi criada. Abra "/main/map/test_layout.collection" para ver essa coleção de layout de teste do mundo:

![](images/rpgmap/test_layout.png)

O único propósito dessa coleção é servir como ferramenta de edição durante o desenvolvimento. Editar uma tela específica lado a lado com a coleção de layout de teste dá contexto para a tela em que você está trabalhando e torna o processo de edição muito melhor:

![](images/rpgmap/side_by_side.png)

Qualquer edição no tilemap da tela (aqui, no painel da direita) é refletida imediatamente na coleção de teste (no painel da esquerda). Observe também que a coleção de layout de teste não é adicionada à hierarquia estática, portanto ela é excluída automaticamente de todos os builds.

## Resumo

Como você viu, este exemplo é construído de acordo com restrições específicas sobre o mundo do jogo e sobre como o herói atravessa esse mundo. Se o seu jogo tiver requisitos diferentes, você provavelmente precisará encontrar outra solução. Por exemplo, se o seu jogo exigir que a câmera se mova de forma contínua pelo mapa do mundo, você precisará de uma maneira diferente de dividir seu conteúdo, de um mecanismo de carregamento diferente e também de ferramentas diferentes para criar o mundo do jogo.

Isso conclui o passo a passo do exemplo de mapa RPG. Como sempre, você pode usar o conteúdo do exemplo da forma que achar melhor. Para aprender mais sobre o Defold, confira nossas [páginas de documentação](https://defold.com/learn) com mais exemplos, tutoriais, manuais e documentação de API.

Se tiver problemas ou perguntas, [acesse nosso fórum](https://forum.defold.com/).

Boas criações com Defold!
