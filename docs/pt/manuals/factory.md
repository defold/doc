---
title: Manual do componente de fábrica
brief: Este manual explica como usar componentes de fábrica para criar objetos de jogo dinamicamente em tempo de execução.
---

# Componentes de fábrica

Componentes de fábrica são usados para criar dinamicamente objetos de jogo a partir de um pool de objetos em um jogo em execução.

Quando você adiciona um componente de fábrica a um objeto de jogo, especifica na propriedade *Prototype* qual arquivo de objeto de jogo a fábrica deve usar como protótipo (também conhecido como "prefab" ou "blueprint" em outras engines) para todos os novos objetos de jogo que ela cria.

![Componente de fábrica](images/factory/factory_collection.png)

![Componente de fábrica](images/factory/factory_component.png)

Para disparar a criação de um objeto de jogo, chame `factory.create()`:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Objeto de jogo criado](images/factory/factory_spawned.png)

`factory.create()` recebe 5 parâmetros:

`url`
: O id do componente de fábrica que deve criar um novo objeto de jogo.

`[position]`
: (opcional) A posição no mundo do novo objeto de jogo. Deve ser um `vector3`. Se você não especificar uma posição, o objeto de jogo será criado na posição do objeto de jogo que chama `factory.create()`.

`[rotation]`
: (opcional) A rotação no mundo do novo objeto de jogo. Deve ser um `quat`.

`[properties]`
: (opcional) Uma tabela Lua com quaisquer valores de propriedades de script para iniciar o objeto de jogo. Consulte o [manual de propriedades de script](/manuals/script-properties) para informações sobre propriedades de script.

`[scale]`
: (opcional) A escala do objeto de jogo criado. A escala pode ser expressa como um `number` (maior que 0), que especifica escala uniforme em todos os eixos. Você também pode fornecer um `vector3`, em que cada componente especifica a escala no eixo correspondente.

Por exemplo:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Cria sem rotação, mas com escala dobrada.
-- Define a pontuação da estrela como 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Define a propriedade "score" do objeto de jogo da estrela.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. A propriedade de script "score" é definida com um valor padrão.
2. Referencie a propriedade de script "score" como um valor armazenado em "self".

![Objeto de jogo criado com propriedade e escala](images/factory/factory_spawned2.png)

::: sidenote
No momento, o Defold não dá suporte a escala não uniforme de formas de colisão. Se você fornecer um valor de escala não uniforme, por exemplo `vmath.vector3(1.0, 2.0, 1.0)`, o sprite será escalado corretamente, mas as formas de colisão não serão.
:::


## Endereçamento de objetos criados por fábrica

O mecanismo de endereçamento do Defold torna possível acessar todos os objetos e componentes em um jogo em execução. O [manual de endereçamento](/manuals/addressing/) explica em detalhes como o sistema funciona. É possível usar o mesmo mecanismo de endereçamento para objetos de jogo criados dinamicamente e seus componentes. Muitas vezes basta usar o id do objeto criado, por exemplo ao enviar uma mensagem:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
Enviar mensagens para o próprio objeto de jogo, em vez de para um componente específico, na prática enviará a mensagem para todos os componentes. Isso geralmente não é um problema, mas é bom ter em mente caso o objeto tenha muitos componentes.
:::

Mas e se você precisar acessar um componente específico em um objeto de jogo criado dinamicamente, por exemplo para desabilitar um objeto de colisão ou alterar a imagem de um sprite? A solução é construir uma URL a partir do id do objeto de jogo e do id do componente.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Rastreamento de objetos criados e objetos pai

Ao chamar `factory.create()`, você recebe de volta o id do novo objeto de jogo, o que permite armazenar o id para referência futura. Um uso comum é criar objetos e adicionar seus ids a uma tabela para poder apagá-los todos depois, por exemplo ao reiniciar o layout de um nível:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Cria uma moeda e a armazena na tabela "coins".
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

E então, mais tarde:

```lua
-- spawner.script
-- Apaga todas as moedas criadas.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- ou, alternativamente
go.delete(self.spawned_coins)
```

Também é comum querer que o objeto criado saiba qual objeto de jogo o criou. Um caso seria algum tipo de objeto autônomo que só pode existir um por vez. O objeto criado então precisa informar ao criador quando for apagado ou inativado, para que outro possa ser criado:

```lua
-- spawner.script
-- Cria um drone e define seu parent como a URL deste componente de script
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

E a lógica do objeto criado:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- Estou morto.
    msg.post(self.parent, "drone_dead")
end
```

## Carregamento dinâmico de recursos de fábrica {#dynamic-loading-of-factory-resources}

Ao marcar a caixa *Load Dynamically* nas propriedades da fábrica, a engine adia o carregamento dos recursos associados à fábrica.

![Carregar dinamicamente](images/factory/load_dynamically.png)

Com a caixa desmarcada, a engine carrega os recursos do protótipo quando o componente de fábrica é carregado, para que fiquem imediatamente prontos para criação.

Com a caixa marcada, você tem duas opções de uso:

Carregamento síncrono
: Chame [`factory.create()`](/ref/factory/#factory.create) quando quiser criar objetos. Isso carregará os recursos de forma síncrona, o que pode causar uma pausa, e então criará novas instâncias.

  ```lua
  function init(self)
      -- Nenhum recurso da fábrica é carregado quando a coleção pai
      -- da fábrica é carregada. Chamar create sem ter chamado
      -- load criará os recursos de forma síncrona.
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- Apaga objetos de jogo. Reduz referências dos recursos.
      -- Neste caso, os recursos são apagados porque o componente
      -- de fábrica não mantém nenhuma referência.
      go.delete(self.go_id)

      -- Chamar unload não fará nada, pois a fábrica não mantém referências
      factory.unload("#factory")
  end
  ```

Carregamento assíncrono
: Chame [`factory.load()`](/ref/factory/#factory.load) para carregar explicitamente os recursos de forma assíncrona. Quando os recursos estiverem prontos para criação, um callback será recebido.

  ```lua
  function load_complete(self, url, result)
      -- O carregamento terminou, os recursos estão prontos para criação
      self.go_id = factory.create(url)
  end

  function init(self)
      -- Nenhum recurso da fábrica é carregado quando a coleção pai
      -- da fábrica é carregada. Chamar load carregará os recursos.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Apaga o objeto de jogo. Reduz referências dos recursos.
      -- Neste caso, os recursos não são apagados porque o componente
      -- de fábrica ainda mantém uma referência.
      go.delete(self.go_id)

      -- Chamar unload reduzirá as referências dos recursos mantidos
      -- pelo componente de fábrica, resultando na destruição dos recursos.
      factory.unload("#factory")
  end
  ```

## Protótipo dinâmico

É possível alterar qual *Prototype* uma fábrica pode criar marcando a caixa *Dynamic Prototype* nas propriedades da fábrica.

![Protótipo dinâmico](images/factory/dynamic_prototype.png)

Quando a opção *Dynamic Prototype* está marcada, o componente de fábrica pode alterar o protótipo usando a função `factory.set_prototype()`. Exemplo:

```lua
factory.unload("#factory") -- descarrega os recursos anteriores
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Quando a opção *Dynamic Prototype* está definida, a contagem de componentes da coleção não pode ser otimizada, e a coleção proprietária usará as contagens de componentes padrão do arquivo *game.project*.
:::


## Limites de instâncias

A configuração de projeto *max_instances* em *Collection related settings* limita o número total de instâncias de objetos de jogo que podem existir em um mundo (a main.collection carregada na inicialização ou qualquer mundo carregado por um proxy de coleção). Todos os objetos de jogo que existem no mundo contam para esse limite, e não importa se eles foram colocados manualmente no editor ou criados em tempo de execução por um script.

![Máximo de instâncias](images/factory/factory_max_instances.png)

Se você definir *max_instances* como 1024 e tiver 24 objetos de jogo colocados manualmente na sua coleção principal, poderá criar mais 1000 objetos de jogo. Assim que apagar um objeto de jogo, você fica livre para criar outra instância.

## Pooling de objetos de jogo

Pode parecer uma boa ideia salvar objetos de jogo criados em um pool e reutilizá-los. No entanto, a engine já faz pooling de objetos internamente, então o overhead adicional só deixará tudo mais lento. É mais rápido e mais limpo apagar objetos de jogo e criar novos.
