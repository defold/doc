---
title: Gerenciamento de recursos no Defold
brief: Este manual explica como o Defold gerencia recursos automaticamente e como você pode gerenciar manualmente o carregamento de recursos para respeitar restrições de uso de memória e tamanho do bundle.
---

# Gerenciamento de recursos

Se você criar um jogo muito pequeno, as limitações da plataforma-alvo (uso de memória, tamanho do bundle, poder de processamento e consumo de bateria) talvez nunca sejam um problema. Porém, ao criar jogos maiores, especialmente em dispositivos portáteis, o consumo de memória provavelmente será uma das maiores restrições. Uma equipe experiente define cuidadosamente orçamentos de recursos em relação às limitações da plataforma. O Defold fornece vários recursos para ajudar a gerenciar memória e tamanho de bundle. Este manual oferece uma visão geral desses recursos.

## A árvore estática de recursos

Ao compilar um jogo no Defold, você declara estaticamente a árvore de recursos. Cada parte do jogo é vinculada à árvore, começando pela coleção principal (geralmente chamada de "main.collection"). A árvore de recursos segue qualquer referência e inclui todos os recursos associados a essas referências:

- Dados de objetos de jogo e componentes (atlas, sons etc).
- Protótipos de componentes de fábrica (objetos de jogo e coleções).
- Referências de componentes de proxy de coleção (coleções).
- [Recursos personalizados](/manuals/project-settings/#custom-resources) declarados em *game.project*.

![Resource tree](images/resource/resource_tree.png)

::: sidenote
O Defold também tem o conceito de [recursos de bundle](/manuals/project-settings/#bundle-resources). Recursos de bundle são incluídos com o bundle da aplicação, mas não fazem parte da árvore de recursos. Esses recursos podem ser qualquer coisa, desde arquivos de suporte específicos de plataforma até arquivos externos [carregados do sistema de arquivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application) e usados pelo seu jogo (por exemplo, bancos de som do FMOD).
:::

Quando o jogo é *empacotado*, somente o que está na árvore de recursos é incluído. Qualquer item que não seja referenciado na árvore fica de fora. Não é necessário selecionar manualmente o que incluir ou excluir do bundle.

Quando o jogo é *executado*, a engine começa na raiz bootstrap da árvore e carrega recursos para a memória:

- Qualquer coleção referenciada e seu conteúdo.
- Objetos de jogo e dados de componentes.
- Protótipos de componentes de fábrica (objetos de jogo e coleções).

No entanto, a engine não carrega automaticamente os seguintes tipos de recursos referenciados em tempo de execução:

- Coleções de mundo de jogo referenciadas por proxies de coleção. Mundos de jogo são relativamente grandes, então você precisa acionar manualmente o carregamento e descarregamento deles no código. Consulte o [manual de proxy de coleção](/manuals/collection-proxy) para detalhes.
- Arquivos adicionados pela configuração *Custom Resources* em *game.project*. Esses arquivos são carregados manualmente com a função [`sys.load_resource()`](/ref/sys/#sys.load_resource).

A forma padrão como o Defold empacota e carrega recursos pode ser alterada para oferecer controle refinado sobre como e quando os recursos entram na memória.

![Resource loading](images/resource/loading.png)

## Carregando dinamicamente recursos de fábrica

Recursos referenciados por componentes de fábrica normalmente são carregados na memória quando o componente é carregado. Então os recursos ficam prontos para serem instanciados no jogo assim que a fábrica existe em tempo de execução. Para alterar o comportamento padrão e adiar o carregamento dos recursos da fábrica, basta marcar uma fábrica com a caixa *Load Dynamically*.

![Load dynamically](images/resource/load_dynamically.png)

Com essa caixa marcada, a engine ainda incluirá os recursos referenciados no bundle do jogo, mas não carregará automaticamente os recursos da fábrica. Em vez disso, você tem duas opções:

1. Chamar [`factory.create()`](/ref/factory/#factory.create) ou [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) quando quiser instanciar objetos. Isso carregará os recursos de forma síncrona e então criará novas instâncias.
2. Chamar [`factory.load()`](/ref/factory/#factory.load) ou [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) para carregar os recursos de forma assíncrona. Quando os recursos estiverem prontos para instanciação, um callback será recebido.

Leia o [manual de fábrica](/manuals/factory) e o [manual de fábrica de coleção](/manuals/collection-factory) para detalhes sobre como isso funciona.

## Descarregando recursos carregados dinamicamente

O Defold mantém contadores de referência para todos os recursos. Se o contador de um recurso chegar a zero, significa que nada mais se refere a ele. O recurso então é descarregado automaticamente da memória. Por exemplo, se você excluir todos os objetos criados por uma fábrica e também excluir o objeto que contém o componente de fábrica, os recursos anteriormente referenciados pela fábrica serão descarregados da memória.

Para fábricas marcadas como *Load Dynamically*, você pode chamar a função [`factory.unload()`](/ref/factory/#factory.unload) ou [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload). Essa chamada remove a referência do componente de fábrica ao recurso. Se nada mais se referir ao recurso (por exemplo, se todos os objetos instanciados tiverem sido excluídos), o recurso será descarregado da memória.

## Excluindo recursos do bundle

Com proxies de coleção, é possível deixar fora do processo de empacotamento todos os recursos aos quais o componente se refere. Isso é útil se você precisa manter o tamanho do bundle no mínimo. Por exemplo, ao executar jogos na web como HTML5, o navegador baixará o bundle inteiro antes de executar o jogo.

![Exclude](images/resource/exclude.png)

Ao marcar um proxy de coleção como *Exclude*, o recurso referenciado ficará fora do bundle do jogo. Em vez disso, você pode armazenar coleções excluídas em um serviço de armazenamento em nuvem escolhido. O [manual de Live update](/manuals/live-update/) explica como esse recurso funciona.
