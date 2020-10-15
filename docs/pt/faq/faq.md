---
title: FAQ da engine e editor Defold
brief: Perguntas frequentes sobre a game engine Defold, editor e plataforma.
---

# Perguntas frequentes

## Perguntas gerais

#### P: Defold é realmente gratuito?

R: Sim, a engine Defold e editor com todas as funcionalidades é completamente de graça. Nenhum custo escondido, taxa ou royalties. Apenas de graça.


#### P: Por qual motivo a Defold Foundation doaria a Defold?

R: Um dos objetivos da [Defold Foundation](/foundation) é ter certeza que software Defold esteja disponível para desenvolvedores ao redor do mundo e que o código fonte esteja disponível de graça.


#### P: Por quanto tempo vocês darão suporte a Defold?

R: Nós estamos muito compromissados à Defold. A [Defold Foundation](/foundation) foi planejada de forma que garante a existência como um proprietário responsável para Defold por muitos anos à frente. Não vai acabar.


##### P: Posso confiar na Defold para desenvolvimento profissional?

R: Absolutamente. A Defold é usada por um número crescente de desenvolvedores profissionais de jogos e estúdios de jogos. Verifique [demonstração de jogos](/showcase) para exemplos de jogos criados usando Defold.


#### P: Que tipo de rastreamento de usuário (user tracking) estão fazendo?

R: Nós registramos uso de dados anônimos dos nossos sites e do editor Defold para melhorar nossos serviços e produtos. Não existe nenhum rastreamento de usuário nos jogos que você cria (a menos que você adicione serviços de análise/analytics por conta própria). Leia mais sobre isto em nossa [Política de Privacidade](/privacy-policy).


#### P: Quem fez a Defold?

R: A Defold foi criada por Ragnar Svensson e Christian Murray. Eles começaram a trabalhar na engine, editor e servidores em 2009. O King e a Defold comeraçam uma parceria em 2013 e o King adquiriu a Defold em 2014. Leia a história completa [aqui](/about).


## Perguntas de plataforma

#### P: Em quais plataforma a Defold roda?

R: As seguintes plataformas são suportadas para o editor/ferramentas e o tempo de execução da engine (engine runtime):

  | Sistema                    | Suportado            |
  | -------------------------- | -------------------- |
  | macOS 10.7 Lion            | Editor e runtime     |
  | Windows Vista              | Editor e runtime     |
  | Ubuntu 18.04 (64 bit)(1)   | Editor               |
  | Linux (64 bit)(2)          | Runtime              |
  | iOS 8.0                    | Runtime              |
  | Android 4.1 (API level 16) | Runtime              |
  | HTML5                      | Runtime              |

  (1 O editor é construído e testado para Ubuntu 18.04 64-bit. Deve funcionar em outras distribuições também, mas não damos garantias.)

  (2 A execução da engine deve rodar na maioria das distribuições Linux 64-bit desde que os drivers gráficos estejam atualizados e suportando OpenGL ES 2.0.)


#### P: Quais são os requisitos de sistema para o editor

R: O editor usará até 75% da memória disponível do sistema. Em um computador com 4 GB de RAM isto deve ser o suficiente para projetos Defold menores. Para projetos de tamanho médio e grande é recomendado usar 6 GB ou mais de RAM.


#### P: Para quais plataformas-alvo eu posso desenvolver jogos com Defold?

R: Com um clique você pode publicar para Nintendo Switch, iOS, Android e HTML5 como também macOS, Windows e Linux. É realmente uma base de código com múltiplas plataformas suportadas.


#### P: Com quais APIs de renderização a Defold está dependendo?

R: Defold usa OpenGL ES 2.0 para renderização gráfica, o qual está disponível em todas as plataformas suportadas.


#### P: Posso criar jogos 3D na Defold?

R: Absolutamente! A engine é uma engine 3D madura. Entretanto o conjunto de ferramentas (toolset) é feito para 2D, por isso terá que fazer muito trabalho pesado por conta própria. Um suporte 3D melhor está planejado.


#### P: Com quais linguagens de programação eu posso trabalhar com a Defold?

R: Lógica de jogo no seu projeto Defold é principalmente escrito usando a linguagem Lua (especificamente Lua 5.1/LuaJIT, recorrer ao [manual Lua](/manuals/lua) para detalhes). Lua é uma linguagem leve e dinâmica que é rápida e muito poderosa. Você também pode usar código nativo (C/C++, Objective-C, Java e Javascript dependendo da plataforma) para estender a engine Defold com novas funcionalidades. Quando construindo materiais personalizados, a linguagem de shading (shader language) do OpenGL ES SL é usada para escrever vertex e fragment shaders.



#### P: Existe alguma forma de saber qual versão estou rodando?

R: Sim, selecione a opção "Sobre" no menu de Ajuda. O popup mostra claramente a versão beta da Defold e, mais importante, a release específica SHA1. Para verificar versões de runtime, utilize [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

A última versão beta disponível para download de http://d.defold.com/beta pode ser verificado abrindo http://d.defold.com/beta/info.json (o mesmo arquivo existe também para versões estáveis: http://d.defold.com/stable/info.json)


#### P: Existe alguma forma de saber em qual plataforma o jogo está sendo execução em tempo de execução?

R: Sim, verifique [`sys.get_sys.info()`](/ref/sys#sys.get_sys_info).


#### P: As versões beta da Defold atualizam automaticamente?

R: Sim. O editor beta Defold verifica por uma atualização na inicialização, assim como a versão estável da Defold faz.


## Publicando jogos

#### P: Estou tentando publicar meu jogo na AppStore. Como eu devo responder ao Identificador de Publicidade (IDFA)?

R: Quando estiver enviando, a Apple possui três checkboxes para os três casos de uso válidos para o IDFA:

  1. Servir propaganda dentro do app (Serve ads within the app)
  2. Instalar atribuição a partir de propaganda (Install attribution from ads)
  3. Atribuição de ação de usuário a partir de propaganda (User action attribution from ads)

  Se você marcar a opção 1, o revisor de app procurará por propagandas que aparecerão no app. Se seu jogo não mostra propagandas, o jogo pode ser rejeitado. Defold em si não utiliza id de propaganda (AD id).


#### P: Como eu monetizo o meu jogo?

R: Defold possui suporte para comprar dentro do app e várias soluções de publicidade. Verificar a [categoria de Monetização no Portal de Ativos](https://defold.com/tags/stars/monetization/) para uma lista atualizada das opções disponíveis de monetização.


## Erros usando Defold

#### P: Por que o editor não inicia ou abre meu projeto?

R: Verifique se existem espaços no path da aplicação Defold. Por exemplo, se você colocar a pasta *Defold-macosx* contendo a versão macOS do editor em sua pasta *Applications*, então deve estar tudo bem. Se você renomear a pasta *Defold macosx* o editor pode não inicializar mais. No Windows, colocar Defold dentro de *C:\\Program Files\\* pode ocasionar este problema. Isto é por conta de um bug conhecido na base do framework Eclipse.


#### P: Eu não consigo iniciar o jogo e não há erro de build. O que está acontecendo?

R: O processo de build pode falhar ao realizar rebuild dos arquivos em casos raros onde já tinha encontrado erro de build que você arrumou. Forçe um rebuild completo selecionando *Project > Rebuild And Launch* a partir do menu.


#### P: Por que estou tomando uma exceção java quando tentou iniciar a Defold?

R: `javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target`

Esta exceção ocorre quando o editor tenta fazer uma conexão https mas a cadeia de certificados fornecida pelo servidor não pode ser verificada.

Ver [este link](https://github.com/defold/editor2-issues/blob/master/faq/pkixpathbuilding.md) para detalhes neste erro.


## Linux
:[Linux FAQ](../shared/linux-faq.md)


## Android
:[Android FAQ](../shared/android-faq.md)


## HTML5
:[HTML5 FAQ](../shared/html5-faq.md)


## Windows
:[Windows FAQ](../shared/windows-faq.md)

## Nintendo Switch
:[Nintendo Switch FAQ](../shared/nintendo-switch-faq.md)


## Conteúdo de jogo

#### P: A Defold suporta prefabs?

R: Sim. São chamados de [coleções](/manuals/building-blocks/#collections)(collections). Elas permitem que você crie hieraquias de game object complexas e armazene-as como building blocks separados que você pode instanciar no editor ou em tempo de execução (por meio de collection spawning). Para nós GUI existe o suporte para templates GUI.


#### P: Eu não consigo adicionar um game object como filho de outro game object, por quê?

R: Existe chance de você estar tentando adicionar um filho em um arquivo de game object e isso não é possível. Para entender o porquê, tem que se lembrar que hierarquias pai-filho são estritamente uma hierarquia de transformação _scene-graph_. Um game object que não foi colocado (ou gerado) dentro de uma cena (coleção) não é parte de uma scene-graph e então não pode ser parte de uma hierarquia scene-graph.


#### P: Por que não consigo transmitir mensagens para todos os filhos de um game object?

R: Relações pai-filho espressam nada mais do que relações de transformação scene-graph e não devem ser confundidos por agregados de orientação objeto. Se você tenta focar no dados do seu jogo e em como melhor transformá-los enquanto seu jogo altera seu estado, você provavelmente encontrará menos necessidade de enviar mensagens com o estado dos dados para tantos objetos ao mesmo tempo. No caso de precisar de hieraquias de dados, estes são facilmente construídos e lidados em Lua.


#### P: Por que estou sofrendo com artefatos visuais ao redor das bordas dos meus sprites?

R: Isso é um artefato visual chamado "edge bleeding" onde você encontra os pixels de borda 