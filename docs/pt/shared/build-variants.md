## Variantes de build

Ao empacotar um jogo, você precisa escolher que tipo de engine deseja usar. Você tem três opções básicas:

  * Debug
  * Release
  * Headless

Essas versões diferentes também são chamadas de `Build variants`

::: sidenote
Ao escolher <kbd>Project ▸ Build</kbd>, você sempre obterá a versão de debug.
:::


### Debug

Este tipo de executável é normalmente usado durante o desenvolvimento de um jogo, pois inclui vários recursos úteis de depuração:

* Profiler - Usado para coletar contadores de desempenho e uso. Aprenda a usar o profiler no [manual de profiling](/manuals/profiling/).
* Logging - A engine registrará informações do sistema, avisos e erros quando o logging estiver habilitado. A engine também emitirá logs da função Lua `print()` e de logs de extensões nativas usando `dmLogInfo()`, `dmLogError()` e assim por diante. Aprenda a ler esses logs no [manual de logs do jogo e do sistema](https://defold.com/manuals/debugging-game-and-system-logs/).
* Hot reload - Hot reload é um recurso poderoso que permite ao desenvolvedor recarregar recursos enquanto o jogo está em execução. Aprenda a usá-lo no [manual de Hot Reload](https://defold.com/manuals/hot-reload/).
* Engine services - É possível conectar-se e interagir com uma versão de debug de um jogo por meio de várias portas TCP abertas e serviços. Os serviços incluem o recurso de hot reload, acesso remoto a logs e o profiler mencionado acima, além de outros serviços para interagir remotamente com a engine. Saiba mais sobre os serviços da engine [na documentação do desenvolvedor](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

Esta variante tem os recursos de depuração desabilitados. Esta opção deve ser escolhida quando o jogo estiver pronto para ser lançado na loja de aplicativos ou compartilhado com jogadores de outras formas. Não é recomendado lançar um jogo com os recursos de depuração habilitados por vários motivos:

* Os recursos de depuração ocupam um pouco de espaço no binário, e [é uma boa prática tentar manter o tamanho do binário de um jogo lançado o menor possível](https://defold.com/manuals/optimization/#optimize-application-size).
* Os recursos de depuração também consomem um pouco de tempo de CPU. Isso pode impactar o desempenho do jogo se um usuário tiver hardware de baixo desempenho. Em celulares, o aumento de uso da CPU também contribuirá para aquecimento e consumo de bateria.
* Os recursos de depuração podem expor informações sobre o jogo que não foram feitas para os olhos dos jogadores, seja por motivos de segurança, trapaça ou fraude.


### Headless

Este executável roda sem gráficos nem som. Isso significa que você pode rodar testes unitários/de smoke do jogo em um servidor de CI, ou até usá-lo como servidor de jogo na nuvem.
