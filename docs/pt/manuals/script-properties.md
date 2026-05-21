---
title: Propriedades de componentes de script
brief: Este manual explica como adicionar propriedades personalizadas a componentes de script e acessá-las pelo editor e por scripts em tempo de execução.
---

# Propriedades de script

Propriedades de script oferecem uma forma simples e poderosa de definir e expor propriedades personalizadas para uma instância específica de objeto de jogo. Propriedades de script podem ser editadas em instâncias específicas diretamente no editor, e suas configurações podem ser usadas no código para alterar o comportamento de um objeto de jogo. Há muitos casos em que propriedades de script são muito úteis:

* Quando você quer sobrescrever valores para instâncias específicas no editor e, assim, aumentar a reutilização do script.
* Quando você quer instanciar um objeto de jogo com valores iniciais.
* Quando você quer animar os valores de uma propriedade.
* Quando você quer acessar dados de estado em um script a partir de outro. (Observe que, se você acessa propriedades com frequência entre objetos, talvez seja melhor mover os dados para um armazenamento compartilhado.)

Casos de uso comuns incluem definir a vida ou a velocidade de uma IA inimiga específica, a cor de tingimento de um objeto coletável, o atlas de um sprite ou qual mensagem um objeto de botão deve enviar quando pressionado - e/ou para onde enviá-la.

## Definindo uma propriedade de script

Propriedades de script são adicionadas a um componente de script ao defini-las com a função especial `go.property()`. A função precisa ser usada no nível superior - fora de quaisquer funções de ciclo de vida, como `init()` e `update()`. O valor padrão fornecido para a propriedade determina o tipo da propriedade: `number`, `boolean`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` e `resource` (veja abaixo).

::: important
Observe que a reversão do valor de hash funciona apenas na build Debug para facilitar a depuração. Na build Release, o valor de string revertido não existe, portanto usar `tostring()` em um valor `hash` para extrair a string dele não faz sentido.
:::


```lua
-- can.script
-- Define propriedades de script para vida e um alvo de ataque
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- armazena a posição inicial do alvo.
  -- self.target é uma url que referencia outro objeto.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- diminui a propriedade de vida
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

Qualquer instância de componente de script criada a partir desse script pode então definir os valores das propriedades.

![Component with properties](images/script-properties/component.png)

Selecione o componente de script na visualização *Outline* no editor e as propriedades aparecerão na visualização *Properties*, permitindo editá-las:

![Properties](images/script-properties/properties.png)

Qualquer propriedade sobrescrita com um novo valor específico da instância é marcada em azul. Clique no botão de redefinição ao lado do nome da propriedade para retornar o valor ao padrão (como definido no script).


::: important
Propriedades de script são analisadas ao compilar o projeto. Expressões de valor não são avaliadas. Isso significa que algo como `go.property("hp", 3+6)` não funcionará, enquanto `go.property("hp", 9)` funcionará.
:::

## Acessando propriedades de script

Qualquer propriedade de script definida fica disponível como um membro armazenado em `self`, a referência da instância do script:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Lê e escreve a propriedade
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Propriedades de script definidas pelo usuário também podem ser acessadas pelas funções get, set e animate, da mesma forma que qualquer outra propriedade:

```lua
-- another.script

-- aumenta "my_property" em "myobject#script" em 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- anima "my_property" em "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Objetos criados por fábrica

Se você usar uma fábrica para criar o objeto de jogo, é possível definir propriedades de script no momento da criação:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Acessando propriedades de script criadas por fábrica
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Ao instanciar uma hierarquia de objetos de jogo por meio de `collectionfactory.create()`, você precisa associar ids de objeto a tabelas de propriedades. Eles são reunidos em uma tabela e passados para a função `create()`:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Os valores de propriedade fornecidos por `factory.create()` e `collectionfactory.create()` sobrescrevem qualquer valor definido no arquivo de protótipo, assim como os valores padrão no script.

Se vários componentes de script anexados a um objeto de jogo definirem a mesma propriedade, cada componente será inicializado com o valor fornecido a `factory.create()` ou `collectionfactory.create()`.


## Propriedades de recurso

Propriedades de recurso são definidas da mesma forma que as propriedades de script dos tipos de dados básicos:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Quando uma propriedade de recurso é definida, ela aparece na visualização *Properties* como qualquer outra propriedade de script, mas como um campo de navegador de arquivo/recurso:

![Resource Properties](images/script-properties/resource-properties.png)

Você acessa e usa as propriedades de recurso usando `go.get()` ou pela referência da instância de script `self`, e usando `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
