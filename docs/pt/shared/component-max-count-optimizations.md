## Otimizações de contagem máxima de componentes {#component-max-count-optimizations}
O arquivo de configurações *game.project* contém muitos valores que especificam o número máximo de determinado recurso que pode existir ao mesmo tempo, geralmente contado por coleção carregada (também chamada de mundo). A engine Defold usará esses valores máximos para pré-alocar memória para essa quantidade, evitando alocações dinâmicas e fragmentação de memória enquanto o jogo está em execução.

As estruturas de dados do Defold usadas para representar componentes e outros recursos são otimizadas para usar o mínimo de memória possível, mas ainda é preciso tomar cuidado ao definir os valores para evitar alocar mais memória do que realmente é necessário.

Para otimizar ainda mais o uso de memória, o processo de build do Defold analisará o conteúdo do jogo e substituirá as contagens máximas se for possível saber com certeza a quantidade exata:

* Se uma coleção não contiver nenhum componente de fábrica, a quantidade exata de cada componente e objeto de jogo será alocada, e os valores de contagem máxima serão ignorados.
* Se uma coleção contiver um componente de fábrica, os objetos gerados serão analisados e a contagem máxima será usada para componentes que podem ser gerados pelas fábricas e para objetos de jogo.
* Se uma coleção contiver uma fábrica ou uma fábrica de coleção com a opção "Dynamic Prototype" ativada, essa coleção usará os contadores máximos.
