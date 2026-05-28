---
title: FAQ da engine e do editor Defold
brief: Perguntas frequentes sobre a game engine Defold, o editor e a plataforma.
---

# Perguntas frequentes

## Perguntas gerais

#### P: O Defold é realmente gratuito?

R: Sim, a engine e o editor Defold, com funcionalidade completa, são totalmente gratuitos. Sem custos escondidos, taxas ou royalties. Apenas gratuito.


#### P: Por que a Defold Foundation disponibiliza o Defold de graça?

R: Um dos objetivos da [Defold Foundation](/foundation) é garantir que o software Defold esteja disponível para desenvolvedores do mundo todo e que o código-fonte esteja disponível gratuitamente.


#### P: Por quanto tempo vocês darão suporte ao Defold?

R: Temos um compromisso profundo com o Defold. A [Defold Foundation](/foundation) foi constituída de uma forma que garante sua existência como proprietária responsável pelo Defold por muitos anos. Ela não vai desaparecer.


#### P: Posso confiar no Defold para desenvolvimento profissional?

R: Com certeza. O Defold é usado por um número crescente de desenvolvedores profissionais de jogos e estúdios de jogos. Confira a [demonstração de jogos](/showcase) para ver exemplos de jogos criados com o Defold.


#### P: Que tipo de rastreamento de usuário vocês fazem?

R: Registramos dados de uso anônimos dos nossos sites e do editor Defold para melhorar nossos serviços e produto. Não há rastreamento de usuário nos jogos que você cria, a menos que você mesmo adicione um serviço de analytics. Leia mais sobre isso em nossa [Política de Privacidade](/privacy-policy).


#### P: Quem criou o Defold?

R: O Defold foi criado por Ragnar Svensson e Christian Murray. Eles começaram a trabalhar na engine, no editor e nos servidores em 2009. A King e o Defold iniciaram uma parceria em 2013, e a King adquiriu o Defold em 2014. Leia a história completa [aqui](/about).


## Perguntas sobre desenvolvimento de jogos

#### P: Posso fazer jogos 3D no Defold?

R: Com certeza! A engine é uma engine 3D completa. No entanto, o conjunto de ferramentas foi criado para 2D, então você precisará fazer bastante trabalho por conta própria. Um suporte melhor a 3D está planejado.


## Perguntas sobre linguagens de programação

#### P: Com qual linguagem de programação eu trabalho no Defold?

R: A lógica de jogo no seu projeto Defold é escrita principalmente usando a linguagem Lua, especificamente Lua 5.1/LuaJIT; consulte o [manual de Lua](/manuals/lua) para detalhes. Lua é uma linguagem dinâmica leve, rápida e muito poderosa. O Defold suporta o uso de transpiladores que emitem código Lua. Com uma extensão de transpilador instalada, você pode usar linguagens alternativas, como [Teal](https://github.com/defold/extension-teal), para escrever Lua com verificação estática. Você também pode usar código nativo (C/C++, Objective-C, Java e JavaScript, dependendo da plataforma) para [estender a engine Defold com novas funcionalidades](/manuals/extensions/). Ao criar [materiais personalizados](/manuals/material/), a linguagem de shader OpenGL ES SL é usada para escrever vertex shaders e fragment shaders.


#### P: Posso usar C++ para escrever lógica de jogo?

R: O suporte a C++ existe no Defold principalmente para escrever extensões nativas que fazem interface com SDKs de terceiros ou APIs específicas de plataforma. A [dmSDK](https://defold.com/ref/stable/dmGameObject/) (a API C++ do Defold usada em extensões nativas) será expandida gradualmente com mais funcionalidades para que seja possível escrever toda a lógica de jogo em C++, se um desenvolvedor desejar. Lua ainda será a principal linguagem usada para lógica de jogo, mas, com a API C++ expandida, também será possível escrever lógica de jogo usando C++. O trabalho para expandir a API C++ envolve principalmente mover arquivos de cabeçalho privados existentes para a seção pública e limpar APIs para uso público.


#### P: Posso usar TypeScript com o Defold?

R: TypeScript não tem suporte oficial. A comunidade mantém um toolkit, [ts-defold](https://ts-defold.dev/), para escrever TypeScript e transpilar para Lua diretamente a partir do VSCode.


#### P: Posso usar Haxe com o Defold?

R: Haxe não tem suporte oficial. A comunidade mantém [hxdefold](https://github.com/hxdefold/hxdefold) para escrever Haxe e transpilar para Lua.


#### P: Posso usar C# com o Defold?

R: A Defold Foundation adicionou suporte a C# e o disponibilizou como uma dependência de biblioteca. C# é uma linguagem de programação amplamente adotada, e isso ajudará estúdios e desenvolvedores com grande investimento em C# a fazer a transição para o Defold.


#### P: Estou preocupado que adicionar suporte a C# tenha um impacto negativo no Defold. Devo me preocupar?

R: O Defold NÃO está deixando Lua como a principal linguagem de script. O suporte a C# foi adicionado como uma nova linguagem para extensões. Ele não afetará a engine, a menos que você escolha usar extensões C# no seu projeto.

O suporte a C# terá um custo (tamanho do executável, desempenho em runtime etc.), mas isso cabe a cada desenvolvedor ou estúdio decidir.

Quanto ao C# em si, é uma mudança relativamente pequena, já que o sistema de extensões já suporta várias linguagens (C/C++/Java/Objective-C/Zig). Os SDKs serão mantidos em sincronia por meio da geração dos bindings C#. Isso manterá os bindings atualizados com esforço mínimo.

A Defold Foundation já foi contra adicionar suporte a C# no Defold, mas mudou de opinião por vários motivos:

* Estúdios e desenvolvedores continuam solicitando suporte a C#.
* O escopo do suporte a C# foi reduzido apenas a extensões (ou seja, baixo esforço).
* A engine principal não será afetada.
* As APIs C# podem ser mantidas em sincronia com esforço mínimo se forem geradas.
* O suporte a C# será baseado em DotNet 9 com NativeAOT, gerando bibliotecas estáticas às quais o pipeline de build existente pode vincular, como qualquer outra extensão do Defold.


## Perguntas sobre plataformas

#### P: Em quais plataformas o Defold roda?

R: As seguintes plataformas têm suporte para o editor/ferramentas e para o runtime da engine:

  | Sistema            | Versão             | Arquiteturas       | Suporte            |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Editor e Engine    |
  | Windows            | Vista              | `x86-32`, `x86-64` | Editor e Engine    |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Editor             |
  | Linux (2)          | Qualquer           | `x86-64`, `arm-64` | Engine             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Engine             |
  | Android            | 5.0 (API level 21) | `arm-32`, `arm-64` | Engine             |
  | HTML5              |                    | `asm.js`, `wasm`   | Engine             |

  (1 O editor é compilado e testado para Ubuntu 64-bit. Ele também deve funcionar em outras distribuições, mas não damos garantias.)

  (2 O runtime da engine deve rodar na maioria das distribuições Linux 64-bit, desde que os drivers gráficos estejam atualizados; veja abaixo mais informações sobre APIs gráficas.)


#### P: Para quais plataformas-alvo posso desenvolver jogos com o Defold?

R: Com um clique, você pode publicar para PS4™, PS5™, Nintendo Switch, iOS (64-bit), Android (32-bit e 64-bit) e HTML5, além de macOS (x86-64 e arm64), Windows (32-bit e 64-bit) e Linux (x86-64 e arm64). É realmente uma única base de código com várias plataformas suportadas.


#### P: De qual API de renderização o Defold depende?

R: Como desenvolvedor, você só precisa se preocupar com uma única API de renderização usando um [pipeline de renderização totalmente programável](/manuals/render/). A API de script de renderização do Defold traduz operações de renderização para as seguintes APIs gráficas:

:[Graphics API](../shared/graphics-api.md)

#### P: Existe uma forma de saber qual versão estou executando?

R: Sim, selecione a opção "About" no menu Help. O popup mostra claramente a versão beta do Defold e, mais importante, o SHA1 específico da release. Para consultar a versão em runtime, use [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

A versão beta mais recente disponível para download em [http://d.defold.com/beta](http://d.defold.com/beta) pode ser verificada abrindo [http://d.defold.com/beta/info.json](http://d.defold.com/beta.json) (o mesmo arquivo também existe para versões estáveis: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)).


#### P: Existe uma forma de saber em qual plataforma o jogo está rodando em runtime?

R: Sim, consulte [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Perguntas sobre o editor
:[Editor FAQ](../shared/editor-faq.md)


## Perguntas sobre Linux
:[Linux FAQ](../shared/linux-faq.md)


## Perguntas sobre Android
:[Android FAQ](../shared/android-faq.md)


## Perguntas sobre HTML5
:[HTML5 FAQ](../shared/html5-faq.md)


## Perguntas sobre iOS
:[iOS FAQ](../shared/ios-faq.md)


## Perguntas sobre Windows
:[Windows FAQ](../shared/windows-faq.md)


## Perguntas sobre consoles
:[Consoles FAQ](../shared/consoles-faq.md)


## Publicando jogos

#### P: Estou tentando publicar meu jogo na AppStore. Como devo responder sobre o IDFA?

R: Ao enviar, a Apple apresenta três caixas de seleção para os três casos de uso válidos do IDFA:

  1. Serve ads within the app
  2. Install attribution from ads
  3. User action attribution from ads

  Se você marcar a opção 1, o revisor do app procurará anúncios aparecendo no app. Se seu jogo não mostra anúncios, ele pode ser rejeitado. O Defold em si não usa AD id.


#### P: Como monetizo meu jogo?

R: O Defold tem suporte a compras dentro do aplicativo e várias soluções de publicidade. Consulte a [categoria Monetização no Portal de Assets](https://defold.com/tags/stars/monetization/) para ver uma lista atualizada das opções de monetização disponíveis.


## Erros ao usar o Defold

#### P: Não consigo iniciar o jogo e não há erro de build. O que está errado?

R: O processo de build pode deixar de recompilar arquivos em casos raros em que já encontrou erros de build que você corrigiu. Force um rebuild completo selecionando *Project > Rebuild And Launch* no menu.



## Conteúdo de jogo

#### P: O Defold suporta prefabs?

R: Sim. Eles são chamados de [coleções](/manuals/building-blocks/#collections). Elas permitem criar hierarquias complexas de objetos de jogo e armazená-las como blocos de construção separados que você pode instanciar no editor ou em runtime, por meio da geração de coleções. Para nodes de GUI, há suporte a templates de GUI.


#### P: Não consigo adicionar um objeto de jogo como filho de outro objeto de jogo. Por quê?

R: É provável que você esteja tentando adicionar um filho no arquivo de objeto de jogo, e isso não é possível. Isso só é possível no arquivo de coleção. Para entender o motivo, lembre-se de que hierarquias pai-filho são estritamente uma hierarquia de transformação de _scene-graph_. Um objeto de jogo que não foi colocado (ou gerado) em uma cena (coleção) não faz parte de um scene-graph e, portanto, não pode fazer parte de uma hierarquia de scene-graph. Você pode obter o id do pai do objeto de jogo usando [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id).


#### P: Por que não consigo enviar mensagens em broadcast para todos os filhos de um objeto de jogo?

R: Relações pai-filho não expressam nada além das relações de transformação no scene-graph e não devem ser confundidas com agregados de orientação a objetos. Se você tentar focar nos dados do jogo e em como transformá-los da melhor maneira à medida que o jogo altera seu estado, provavelmente terá menos necessidade de enviar mensagens com dados de estado para muitos objetos o tempo todo. Nos casos em que você precisar de hierarquias de dados, elas são facilmente construídas e manipuladas em Lua.


#### P: Por que estou vendo artefatos visuais ao redor das bordas dos meus sprites?

R: Isso é um artefato visual chamado "edge bleeding", em que pixels das bordas de imagens vizinhas em um atlas vazam para a imagem atribuída ao seu sprite. A solução é preencher as bordas das imagens do atlas com linhas e colunas extras de pixels idênticos. Felizmente, isso pode ser feito automaticamente pelo editor de atlas do Defold. Abra seu atlas e defina o valor de *Extrude Borders* como 1.


#### P: Posso tingir meus sprites ou torná-los transparentes, ou preciso escrever meu próprio shader para isso?

R: O shader de sprite integrado, usado por padrão em todos os sprites, tem uma constante "tint" definida:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### P: Se eu definir a coordenada z de um sprite como 100, ele não é renderizado. Por quê?

R: A posição Z de um objeto de jogo controla a ordem de renderização. Valores baixos são desenhados antes de valores mais altos. No script de renderização padrão, objetos de jogo com profundidade entre -1 e 1 são desenhados; qualquer coisa abaixo ou acima disso não será desenhada. Você pode ler mais sobre o script de renderização na [documentação oficial de renderização](/manuals/render). Em nodes de GUI, o valor Z é ignorado e não afeta a ordem de renderização. Em vez disso, os nodes são renderizados na ordem em que estão listados e de acordo com hierarquias de filhos (e camadas). Leia mais sobre renderização de GUI e otimização de draw calls usando camadas na [documentação oficial de GUI](/manuals/gui).


#### P: Alterar o intervalo Z da projeção de visualização para -100 a 100 afetaria o desempenho?

R: Não. O único efeito é a precisão. O z-buffer é logarítmico e tem resolução muito fina para valores de z próximos de 0, e menos resolução longe de 0. Por exemplo, com um buffer de 24 bits, os valores 10.0 e 10.000005 podem ser diferenciados, enquanto 10000 e 10005 não podem.


#### P: Não há consistência na forma como os ângulos são representados. Por quê?

R: Na verdade, há consistência. Os ângulos são expressos em graus em todos os lugares do editor e das APIs de jogo. As bibliotecas matemáticas usam radianos. Atualmente, a convenção falha na propriedade de física `angular_velocity`, que hoje é expressa em radianos/s. Espera-se que isso mude.


#### P: Ao criar um node GUI do tipo box apenas com cor (sem textura), como ele será renderizado?

R: É apenas uma forma colorida por vértices. Tenha em mente que ela ainda terá custo de fill-rate.


#### P: Se eu alterar assets dinamicamente, a engine os descarregará automaticamente?

R: Todos os recursos têm contagem de referências internamente. Assim que a contagem de referências chega a zero, o recurso é liberado.


#### P: É possível tocar áudio sem usar um componente de áudio anexado a um objeto de jogo?

R: Tudo é baseado em componentes. É possível criar um objeto de jogo headless com múltiplos sons e tocar sons enviando mensagens ao objeto controlador de som.


#### P: É possível alterar, em tempo de execução, o arquivo de áudio associado a um componente de áudio?

R: Em geral, todos os recursos são declarados estaticamente, com o benefício de que você recebe gerenciamento de recursos gratuitamente. Você pode usar [propriedades de recurso](/manuals/script-properties/#resource-properties) para alterar qual recurso é atribuído a um componente.


#### P: Existe uma forma de acessar as propriedades da forma de colisão da física?

R: Sim, veja a API de física, especialmente [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) e [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table).


#### P: Existe uma forma rápida de renderizar os objetos de colisão na minha cena? (como o debug draw do Box2D)

R: Sim, defina a flag *physics.debug* em *game.project*. (Consulte a [documentação oficial de configurações do projeto](/manuals/project-settings/#debug))


#### P: Quais são os custos de desempenho de ter muitos contatos/colisões?

R: O Defold executa uma versão modificada do Box2D em segundo plano, e o custo de desempenho deve ser bastante parecido. Você sempre pode ver quanto tempo a engine gasta em física abrindo o [profiler](/manuals/debugging). Você também deve considerar que tipo de objetos de colisão está usando. Objetos estáticos são mais baratos em termos de desempenho, por exemplo. Consulte a [documentação oficial de física](/manuals/physics) do Defold para mais detalhes.


#### P: Qual é o impacto de desempenho de ter muitos componentes de efeito de partículas?

R: Depende se eles estão em reprodução ou não. Um ParticleFx que não está em reprodução tem custo de desempenho zero. O impacto de desempenho de um ParticleFx em reprodução deve ser avaliado usando o profiler, já que seu impacto depende de como ele está configurado. Como na maioria das outras coisas, a memória é alocada antecipadamente para o número de ParticleFx definido como max_count em *game.project*.


#### P: Como recebo entrada em um objeto de jogo dentro de uma coleção carregada via proxy de coleção?

R: Cada coleção carregada por proxy tem sua própria pilha de entrada. A entrada é roteada da pilha de entrada da coleção principal, via componente proxy, para os objetos na coleção. Isso significa que não basta o objeto de jogo na coleção carregada adquirir foco de entrada; o objeto de jogo que _contém_ o componente proxy também precisa adquirir foco de entrada. Consulte a [documentação de entrada](/manuals/input) para detalhes.


#### P: Posso usar propriedades de script do tipo string?

R: Não. O Defold suporta propriedades do tipo [hash](/ref/builtins#hash). Elas podem ser usadas para indicar tipos, identificadores de estado ou chaves de qualquer tipo. Hashes também podem ser usados para armazenar ids de objetos de jogo (caminhos), embora propriedades [url](/ref/msg#msg.url) muitas vezes sejam preferíveis, pois o editor preenche automaticamente um menu suspenso com URLs relevantes para você. Consulte a [documentação de propriedades de script](/manuals/script-properties) para detalhes.


#### P: Como acesso as células individuais de uma matriz (criada usando [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) ou similar)?

R: Você acessa as células usando `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` etc.


#### P: Estou recebendo `Not enough resources to clone the node` ao usar [gui.clone()](/ref/gui/#gui.clone:node) ou [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

R: Aumente o valor de `Max Nodes` do componente GUI. Você encontra esse valor no painel Properties ao selecionar a raiz do componente no Outline.


## O fórum

#### P: Posso publicar uma thread anunciando meu trabalho?

R: Claro! Temos uma categoria especial ["Work for hire"](https://forum.defold.com/c/work-for-hire) para isso. Sempre incentivaremos tudo que beneficia a comunidade, e oferecer seus serviços à comunidade, com remuneração ou não, é um bom exemplo disso.


#### P: Criei uma thread e adicionei meu trabalho. Posso adicionar mais?

R: Para reduzir o bumping de threads da categoria "Work for hire", você não pode postar mais de uma vez a cada 14 dias na sua própria thread, a menos que seja uma resposta direta a um comentário na thread; nesse caso, você pode responder. Se quiser adicionar mais trabalhos à sua thread dentro do período de 14 dias, edite seus posts existentes com o conteúdo adicionado.


#### P: Posso usar a categoria Work for Hire para publicar ofertas de trabalho?

R: Claro, fique à vontade! Ela pode ser usada tanto para ofertas quanto para pedidos, por exemplo, "Programador procura artista de pixel 2D; sou rico e vou pagar bem".
