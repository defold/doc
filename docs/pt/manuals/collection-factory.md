---
title: Manual de fábrica de coleção
brief: Este manual explica como usar componentes de fábrica de coleção para criar hierarquias de objetos de jogo.
---

# Fábricas de coleção

O componente de fábrica de coleção é usado para criar, em um jogo em execução, grupos e hierarquias de objetos de jogo armazenados em arquivos de coleção.

Coleções oferecem um mecanismo poderoso para criar modelos reutilizáveis, ou "prefabs", no Defold. Para uma visão geral de coleções, consulte a [documentação de blocos de construção](/manuals/building-blocks#collections). Coleções podem ser posicionadas no editor ou inseridas dinamicamente no seu jogo.

Com um componente de fábrica de coleção, você pode criar o conteúdo de um arquivo de coleção dentro de um mundo de jogo. Isso é análogo a executar a criação por fábrica de todos os objetos de jogo dentro da coleção e então construir a hierarquia pai-filho entre os objetos. Um caso de uso típico é criar inimigos compostos por vários objetos de jogo (inimigo + arma, por exemplo).

## Criando uma coleção {#spawning-a-collection}

Suponha que queremos um objeto de jogo de personagem e um objeto de jogo de escudo separado como filho do personagem. Construímos a hierarquia de objetos de jogo em um arquivo de coleção e a salvamos como "bean.collection".

::: sidenote
O componente *collection proxy* é usado para criar um novo mundo de jogo, incluindo um mundo de física separado, com base em uma coleção. O novo mundo é acessado por meio de um novo socket. Todos os assets contidos na coleção são carregados pelo proxy quando você envia uma mensagem ao proxy para iniciar o carregamento. Isso os torna muito úteis, por exemplo, para trocar fases em um jogo. Novos mundos de jogo têm uma sobrecarga considerável, portanto não os use para carregamento dinâmico de coisas pequenas. Para mais informações, veja a [documentação de proxy de coleção](/manuals/collection-proxy).
:::

![Coleção a criar](images/collection_factory/collection.png)

Em seguida, adicionamos uma *Collection factory* a um gameobject que cuidará da criação e definimos "bean.collection" como o *Prototype* do componente:

![Fábrica de coleção](images/collection_factory/factory.png)

Criar um bean e um escudo agora é apenas uma questão de chamar a função `collectionfactory.create()`:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

A função recebe 5 parâmetros:

`url`
: O id do componente de fábrica de coleção que deve criar o novo conjunto de objetos de jogo.

`[position]`
: (opcional) A posição no mundo dos objetos de jogo criados. Deve ser um `vector3`. Se você não especificar uma posição, os objetos serão criados na posição do componente de fábrica de coleção.

`[rotation]`
: (opcional) A rotação no mundo dos novos objetos de jogo. Deve ser um `quat`.

`[properties]`
: (opcional) Uma tabela Lua com pares `id`-`table` usados para inicializar os objetos de jogo criados. Veja abaixo como construir essa tabela.

`[scale]`
: (opcional) A escala dos objetos de jogo criados. A escala pode ser expressa como um `number` (maior que 0), que especifica escala uniforme em todos os eixos. Você também pode fornecer um `vector3` em que cada componente especifica a escala no eixo correspondente.

`collectionfactory.create()` retorna as identidades dos objetos de jogo criados como uma tabela. As chaves da tabela mapeiam o hash do id local da coleção de cada objeto para o id de runtime de cada objeto:

::: sidenote
A relação pai-filho entre "bean" e "shield" *não* é refletida na tabela retornada. Essa relação existe apenas no scene-graph de runtime, isto é, em como os objetos são transformados juntos. Reparentar um objeto nunca altera seu id.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. Um prefixo `/collection[N]/`, em que `[N]` é um contador, é adicionado ao id para identificar cada instância de forma única:

## Propriedades

Ao criar uma coleção, você pode passar parâmetros de propriedades para cada objeto de jogo construindo uma tabela em que as chaves são ids de objetos e os valores são tabelas com as propriedades de script a definir.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Supondo que o objeto de jogo "bean" em "bean.collection" defina a propriedade "shield". [O manual de propriedades de script](/manuals/script-properties) contém informações sobre propriedades de script.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Carregamento dinâmico de recursos de fábrica {#dynamic-loading-of-factory-resources}

Ao marcar a caixa *Load Dynamically* nas propriedades da fábrica de coleção, a engine adia o carregamento dos recursos associados à fábrica.

![Carregar dinamicamente](images/collection_factory/load_dynamically.png)

Com a caixa desmarcada, a engine carrega os recursos do protótipo quando o componente de fábrica de coleção é carregado, deixando-os imediatamente prontos para criação.

Com a caixa marcada, você tem duas opções de uso:

Carregamento síncrono
: Chame [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) quando quiser criar objetos. Isso carregará os recursos de forma síncrona, o que pode causar uma travada, e então criará novas instâncias.

  ```lua
  function init(self)
      -- Nenhum recurso da fábrica é carregado quando a coleção pai
      -- da fábrica de coleção é carregada. Chamar create sem
      -- ter chamado load criará os recursos de forma síncrona.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Exclui objetos de jogo. Fará decref dos recursos.
      -- Neste caso os recursos são excluídos, pois o componente
      -- de fábrica de coleção não mantém referência.
      go.delete(self.go_ids)

      -- Chamar unload não fará nada, pois a fábrica
      -- não mantém referências
      collectionfactory.unload("#factory")
  end
  ```

Carregamento assíncrono
: Chame [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) para carregar explicitamente os recursos de forma assíncrona. Quando os recursos estiverem prontos para criação, um callback será recebido.

  ```lua
  function load_complete(self, url, result)
      -- O carregamento terminou, os recursos estão prontos para criação
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- Nenhum recurso da fábrica é carregado quando a coleção pai
      -- da fábrica de coleção é carregada. Chamar load carregará os recursos.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Exclui objeto de jogo. Fará decref dos recursos.
      -- Neste caso os recursos não são excluídos, pois o componente
      -- de fábrica de coleção ainda mantém uma referência.
      go.delete(self.go_ids)

      -- Chamar unload fará decref dos recursos mantidos pelo componente de fábrica,
      -- resultando na destruição dos recursos.
      collectionfactory.unload("#factory")
  end
  ```


## Protótipo dinâmico

É possível alterar qual *Prototype* uma fábrica de coleção pode criar marcando a caixa *Dynamic Prototype* nas propriedades da fábrica de coleção.

![Protótipo dinâmico](images/collection_factory/dynamic_prototype.png)

Quando a opção *Dynamic Prototype* está marcada, o componente de fábrica de coleção pode trocar de protótipo usando a função `collectionfactory.set_prototype()`. Exemplo:

```lua
collectionfactory.unload("#factory") -- descarrega os recursos anteriores
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Quando a opção *Dynamic Prototype* está definida, a contagem de componentes da coleção não pode ser otimizada, e a coleção proprietária usará as contagens padrão de componentes do arquivo *game.project*.
:::
