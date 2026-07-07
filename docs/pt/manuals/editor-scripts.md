---
title: Scripts do editor
brief: Este manual explica como estender o editor usando Lua
---

# Scripts do editor

Você pode criar itens de menu personalizados e hooks de ciclo de vida do editor usando arquivos Lua com uma extensão especial: `.editor_script`. Usando este sistema, você pode ajustar o editor para melhorar seu fluxo de desenvolvimento.

## Runtime dos scripts do editor

Editor scripts rodam dentro de um editor, em uma VM Lua emulada pela VM Java. Todos os scripts compartilham o mesmo ambiente único, o que significa que podem interagir entre si. Você pode usar `require` para módulos Lua, assim como com arquivos `.script`, mas a versão de Lua que roda dentro do editor é diferente, então certifique-se de que seu código compartilhado seja compatível. O editor usa Lua versão 5.2.x, mais especificamente o runtime [luaj](https://github.com/luaj/luaj), que atualmente é a única solução viável para rodar Lua na JVM. Além disso, há algumas restrições:
- não há pacote `debug`;
- não há `os.execute`, embora forneçamos um `editor.execute()` semelhante;
- não há `os.tmpname` nem `io.tmpfile` — atualmente, editor scripts só podem acessar arquivos dentro do diretório do projeto;
- atualmente não há `os.rename`, embora queiramos adicioná-lo;
- não há `os.exit` nem `os.setlocale`.
- não é permitido usar algumas funções de longa duração em contextos em que o editor precisa de uma resposta imediata do script; veja [Modos de execução](#execution-modes) para mais detalhes.

Todas as extensões do editor definidas em editor scripts são carregadas quando você abre um projeto. Quando você busca bibliotecas, as extensões são recarregadas, pois pode haver novos editor scripts nas bibliotecas das quais você depende. Durante esse recarregamento, alterações nos seus próprios editor scripts não são carregadas, pois você pode estar no meio de editá-los. Para recarregá-los também, execute o comando **Project → Reload Editor Scripts**.

## Anatomia de `.editor_script`

Todo editor script deve retornar um módulo, assim:
```lua
local M = {}

function M.get_commands()
  -- TODO - definir comandos do editor
end

function M.get_language_servers()
  -- TODO - definir language servers
end

function M.get_prefs_schema()
  -- TODO - definir preferências
end

return M
```
O editor então coleta todos os editor scripts definidos no projeto e nas bibliotecas, carrega-os em uma única VM Lua e os chama quando necessário (mais sobre isso nas seções [comandos](#commands) e [hooks de ciclo de vida](#lifecycle-hooks)).

## API do editor

Você pode interagir com o editor usando o pacote `editor`, que define esta API:
- `editor.platform` — uma string, `"x86_64-win32"` para Windows, `"x86_64-macos"` para macOS ou `"x86_64-linux"` para Linux.
- `editor.version` — uma string, nome da versão do Defold, por exemplo `"1.4.8"`
- `editor.engine_sha1` — uma string, SHA1 da engine Defold
- `editor.editor_sha1` — uma string, SHA1 do editor Defold
- `editor.get(node_id, property)` — obtém o valor de algum node dentro do editor. Nodes no editor são várias entidades, como arquivos de script ou coleção, objetos de jogo dentro de coleções, arquivos json carregados como recursos etc. `node_id` é um userdata passado ao editor script pelo editor. Como alternativa, você pode passar o caminho do recurso em vez do id do node, por exemplo `"/main/game.script"`. `property` é uma string. Atualmente, estas propriedades são suportadas:
  - `"path"` — caminho do arquivo a partir da pasta do projeto para *recursos* — entidades que existem como arquivos ou diretórios. Exemplo de valor retornado: `"/main/game.script"`
  - `"children"` — lista de caminhos de recursos filhos para recursos de diretório
  - `"text"` — conteúdo textual de um recurso editável como texto (como arquivos de script ou json). Exemplo de valor retornado: `"function init(self)\nend"`. Observe que isso não é o mesmo que ler o arquivo com `io.open()`, porque você pode editar um arquivo sem salvá-lo, e essas edições ficam disponíveis apenas ao acessar a propriedade `"text"`.
  - para atlases: `images` (lista de nodes do editor para imagens no atlas) e `animations` (lista de nodes de animação)
  - para animações de atlas: `images` (igual a `images` no atlas)
  - para tilemaps: `layers` (lista de nodes do editor para camadas no tilemap)
  - para camadas de tilemap: `tiles` (uma grade 2D ilimitada de tiles), veja `tilemap.tiles.*` para mais informações
  - para particlefx: `emitters` (lista de nodes de emissor do editor) e `modifiers` (lista de nodes de modificador)
  - para emissores particlefx: `modifiers` (lista de nodes de modificador)
  - para objetos de colisão: `shapes` (lista de nodes de forma de colisão do editor)
  - para arquivos GUI: `layers` (lista de nodes de camada do editor)
  - algumas propriedades mostradas na visualização Properties quando você tem algo selecionado na visualização Outline. Estes tipos de propriedades de outline são suportados:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Observe que algumas dessas propriedades podem ser somente leitura, e algumas podem estar indisponíveis em contextos diferentes, então você deve usar `editor.can_get` antes de lê-las e `editor.can_set` antes de fazer o editor defini-las. Passe o mouse sobre o nome da propriedade na visualização Properties para ver uma tooltip com informações sobre como essa propriedade é nomeada em editor scripts. Você pode definir propriedades de recurso como `nil` fornecendo o valor `""`.
- `editor.can_get(node_id, property)` — verifica se você pode obter esta propriedade para que `editor.get()` não lance um erro.
- `editor.can_set(node_id, property)` — verifica se uma etapa de transação `editor.tx.set()` com esta propriedade não lançará um erro.
- `editor.create_directory(resource_path)` — cria um diretório se ele não existir, e todos os diretórios pais inexistentes.
- `editor.create_resources(resources)` — cria 1 ou mais recursos, a partir de templates ou com conteúdo personalizado.
- `editor.delete_directory(resource_path)` — exclui um diretório se ele existir, e todos os diretórios e arquivos filhos existentes.
- `editor.execute(cmd, [...args], [options])` — executa um comando de shell, opcionalmente capturando sua saída.
- `editor.save()` — persiste todas as alterações não salvas no disco.
- `editor.transact(txs)` — modifica o estado em memória do editor usando 1 ou mais etapas de transação criadas com funções `editor.tx.*`.
- `editor.ui.*` — várias funções relacionadas a UI, veja o [manual de UI](/manuals/editor-scripts-ui).
- `editor.prefs.*` — funções para interagir com preferências do editor, veja [preferências](#preferences).

Você encontra a referência completa da API do editor [aqui](https://defold.com/ref/alpha/editor/).

## Comandos {#commands}

Se o módulo de editor script definir a função `get_commands`, ela será chamada no recarregamento da extensão, e os comandos retornados ficarão disponíveis para uso dentro do editor na barra de menu ou nos menus de contexto dos painéis Assets e Outline. Exemplo:
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
O editor espera que `get_commands()` retorne um array de tabelas, cada uma descrevendo um comando separado. A descrição do comando consiste em:

- `label` (obrigatório) — texto em um item de menu que será exibido ao usuário
- `locations` (obrigatório) — um array com `"Edit"`, `"View"`, `"Project"`, `"Debug"`, `"Assets"`, `"Bundle"`, `"Scene"` ou `"Outline"`, descrevendo onde este comando deve estar disponível. `"Edit"`, `"View"`, `"Project"` e `"Debug"` significam barra de menu no topo, `"Assets"` significa menu de contexto no painel Assets, `"Outline"` significa menu de contexto no painel Outline, e `"Bundle"` significa submenu **Project → Bundle**.
- `query` — uma forma de o comando pedir ao editor informações relevantes e definir com quais dados ele opera. Para cada chave na tabela `query`, haverá uma chave correspondente na tabela `opts` que os callbacks `active` e `run` recebem como argumento. Chaves suportadas:
  - `selection` significa que este comando é válido quando há algo selecionado, e opera nessa seleção.
    - `type` é o tipo de nodes selecionados em que o comando tem interesse; atualmente estes tipos são permitidos:
      - `"resource"` — em Assets e Outline, resource é um item selecionado que tem um arquivo correspondente. Na barra de menu (Edit ou View), resource é um arquivo aberto no momento;
      - `"outline"` — algo que pode ser mostrado no Outline. No Outline é um item selecionado; na barra de menu é um arquivo aberto no momento;
      - `"scene"` — algo que pode ser renderizado na Scene.
    - `cardinality` define quantos itens selecionados deve haver. Se for `"one"`, a seleção passada ao callback do comando será um único node id. Se for `"many"`, a seleção passada ao callback do comando será um array de um ou mais node ids.
  - `active_view` significa que este comando é válido quando a visualização ativa do editor corresponde ao tipo solicitado. A visualização ativa é passada ao callback do comando como `opts.active_view`.
    - `type` é o tipo da visualização ativa em que o comando tem interesse: `"code"`, `"scene"`, `"html"` ou `"form"`.
    - A visualização ativa suporta as propriedades `"type"`, `"resource"` e `"dirty"`. Use `editor.get(view, "resource")` para obter o recurso mostrado na visualização, e `editor.get(view, "dirty")` para verificar se há alterações não salvas.
  - `argument` — argumento do comando. Atualmente, apenas comandos no local `"Bundle"` recebem um argumento, que é `true` quando o comando de bundle é selecionado explicitamente e `false` em rebundle.
- `id` - string identificadora do comando, usada por exemplo para persistir o último comando de bundle usado em `prefs`
- `active` - um callback executado para verificar se o comando está ativo, esperado retornar boolean. Se `locations` incluir `"Assets"`, `"Scene"` ou `"Outline"`, `active` será chamado ao mostrar o menu de contexto. Se locations incluir `"Edit"` ou `"View"`, active será chamado em toda interação do usuário, como digitar no teclado ou clicar com o mouse, então garanta que `active` seja relativamente rápido.
- `run` - um callback executado quando o usuário seleciona o item de menu.

### Use comandos para alterar o estado em memória do editor

Dentro do handler `run`, você pode consultar e alterar o estado em memória do editor. A consulta é feita usando a função `editor.get()`, com a qual você pode perguntar ao editor sobre o estado atual de arquivos e seleção (se estiver usando `query = {selection = ...}`). Você pode obter a propriedade `"text"` de arquivos de script e também algumas propriedades mostradas na visualização Properties — passe o mouse sobre o nome da propriedade para ver uma tooltip com informações sobre como essa propriedade é nomeada em editor scripts. A alteração do estado do editor é feita usando `editor.transact()`, onde você agrupa 1 ou mais modificações em uma única etapa desfazível. Por exemplo, se quiser poder resetar a transformação de um objeto de jogo, você poderia escrever um comando assim:
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Use comandos com a visualização ativa do editor

Comandos em locais de menu como `"View"` podem consultar a visualização ativa do editor. Isso é útil quando um comando deve operar no arquivo ou na cena que o usuário está vendo no momento:

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Editando atlases

Além de ler e escrever propriedades de um atlas, você pode ler e modificar imagens e animações do atlas. Atlas define propriedades de lista de nodes `images` e `animations`, e animações definem a propriedade de lista de nodes `images`: você pode usar as etapas de transação `editor.tx.add`, `editor.tx.remove` e `editor.tx.clear` com essas propriedades.

Por exemplo, para adicionar uma imagem a um atlas, execute o código a seguir no handler `run` do comando:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Para encontrar um conjunto de todas as imagens em um atlas, execute o código a seguir:
```lua
local all_images = {} ---@type table<string, true>
-- primeiro, coleta todas as imagens "bare"
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- depois, coleta todas as imagens usadas em animações
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
Para substituir todas as animações em um atlas:
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Editando tilesources

Além das propriedades de outline, tilesources definem as seguintes propriedades:
- `animations` - uma lista de nodes de animação do tilesource
- `collision_groups` - uma lista de nodes de grupos de colisão do tilesource
- `tile_collision_groups` - uma tabela de atribuições de grupos de colisão para tiles no tilesource

Por exemplo, veja como você pode configurar um tilesource:
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Editando tilemaps

Tilemaps definem a propriedade `layers`, uma lista de nodes de camadas de tilemap. Cada camada também define uma propriedade `tiles`, que mantém uma grade 2D ilimitada de tiles nessa camada. Isso é diferente da engine: tiles não têm limites e podem ser adicionados em qualquer lugar, inclusive em coordenadas negativas. Para editar tiles, a API de editor script define um módulo `tilemap.tiles` com as seguintes funções:
- `tilemap.tiles.new()` para criar uma estrutura de dados nova que mantém uma grade 2D ilimitada de tiles (no editor, ao contrário da engine, o tilemap é ilimitado, e coordenadas podem ser negativas)
- `tilemap.tiles.get_tile(tiles, x, y)` para obter o índice de um tile em uma coordenada específica
- `tilemap.tiles.get_info(tiles, x, y)` para obter informações completas do tile em uma coordenada específica (o formato dos dados é o mesmo da função `tilemap.get_tile_info` da engine)
- `tilemap.tiles.iterator(tiles)` para criar um iterador sobre todos os tiles no tilemap
- `tilemap.tiles.clear(tiles)` para remover todos os tiles do tilemap
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` para definir um tile em uma coordenada específica
- `tilemap.tiles.remove(tiles, x, y)` para remover um tile em uma coordenada específica

Por exemplo, veja como imprimir o conteúdo de todo o tilemap:
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Aqui está um exemplo que mostra como adicionar uma camada com tiles a um tilemap:
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Editando particlefx

Você pode editar particlefx usando as propriedades `modifiers` e `emitters`. Por exemplo, adicionar um emissor circular com modificador de aceleração é feito assim:
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
Muitas propriedades de particlefx são curvas ou curve spreads (isto é, curva + algum valor randomizador). Curvas são representadas como uma tabela com uma lista não vazia de `points`, em que cada ponto é uma tabela com as seguintes propriedades:
- `x` - a coordenada x do ponto, deve começar em 0 e terminar em 1
- `y` - o valor do ponto
- `tx` (0 a 1) e `ty` (-1 a 1) - tangentes do ponto. Por exemplo, para um ângulo de 80 graus, `tx` deve ser `math.cos(math.rad(80))` e `ty` deve ser `math.sin(math.rad(80))`.
Curve spreads também têm uma propriedade numérica `spread`.

Por exemplo, definir uma curva alpha de tempo de vida de partícula para um emissor já existente pode se parecer com isto:
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- começa em 0, sobe rapidamente
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- alcança 1 em 20% do tempo de vida
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- desce lentamente para 0
    }})
})
```
É claro que também é possível usar a chave `particle_key_alpha` em uma tabela ao criar um emissor. Além disso, você pode usar um único número para representar uma curva "estática".

#### Editando objetos de colisão

Além das propriedades padrão de outline, objetos de colisão definem a propriedade de lista de nodes `shapes`. Adicionar novas formas de colisão é feito assim:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- ou "shape-type-sphere", "shape-type-capsule"
    })
})
```
A propriedade `type` da forma é obrigatória durante a criação e não pode ser alterada depois que a forma é adicionada. Há 3 tipos de forma:
- `shape-type-box` - forma de caixa com propriedade `dimensions`
- `shape-type-sphere` - forma de esfera com propriedade `diameter`
- `shape-type-capsule` - forma de cápsula com propriedades `diameter` e `height`

#### Editando arquivos GUI

Além das propriedades de outline, nodes GUI definem as seguintes propriedades:
- `layers` — lista de nodes de camada do editor (reordenável)
- `materials` — lista de nodes de material do editor

É possível editar camadas GUI usando a propriedade `layers` do editor, por exemplo:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Além disso, é possível reordenar camadas:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
De forma semelhante, fontes, materiais, texturas e particlefxs são editados usando as propriedades `fonts`, `materials`, `textures` e `particlefxs`:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.material"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Essas propriedades não oferecem suporte a reordenação.

Por fim, você pode editar nodes GUI usando a propriedade de lista `nodes`, por exemplo:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Os tipos de node integrados são:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Se você está usando a extensão Spine, também pode usar o tipo de node `gui-node-type-spine`.

Se o arquivo GUI define layouts, você pode obter e definir os valores dos layouts usando a sintaxe `layout:property`, por exemplo:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Propriedades de layout que foram definidas podem ser resetadas para seus valores padrão usando `editor.tx.reset`:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Árvores de nodes de template podem ser lidas, mas não editadas — você só pode definir propriedades de node da árvore de nodes do template:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (sobrescreve um valor no template)
```

#### Editando objetos de jogo

É possível editar componentes de um arquivo de objeto de jogo usando editor scripts. Os componentes vêm em 2 variedades: referenciados e embutidos. Componentes referenciados usam o tipo `component-reference` e agem como referências a outros recursos, permitindo apenas overrides de propriedades go definidas em scripts. Componentes embutidos usam tipos como `sprite`, `label` etc., e permitem editar todas as propriedades definidas pelo tipo de componente, bem como adicionar subcomponentes, como formas de objetos de colisão. Por exemplo, você pode usar o código a seguir para configurar um objeto de jogo:
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script"
        id = "controller",
        __hp = 100 -- define uma propriedade go definida no script
    })
})
```

#### Editando coleções
É possível editar coleções usando editor scripts. Você pode adicionar objetos de jogo (embutidos ou referenciados) e coleções (referenciadas). Por exemplo:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- objeto de jogo embutido
        type = "go",
        id = "root",
        children = {
            {
                -- objeto de jogo referenciado
                type = "go-reference",
                path = "/char-view.go"
                id = "view"
            },
            {
                -- coleção referenciada
                type = "collection-reference",
                path = "/body-attachments.collection"
                id = "attachments"
            }
        },
        -- gos embutidos também podem ter componentes
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- define uma propriedade go definida no script
            }
        }
    })
})
```

Assim como no editor, coleções referenciadas só podem ser adicionadas à raiz da coleção editada, e objetos de jogo só podem ser adicionados a objetos de jogo embutidos ou referenciados, mas não a coleções referenciadas nem a objetos de jogo dentro dessas coleções referenciadas.

### Usar comandos de shell

Dentro do handler `run`, você pode escrever em arquivos (usando o módulo `io`) e executar comandos de shell (usando o comando `editor.execute()`). Ao executar comandos de shell, é possível capturar a saída de um comando de shell como string e então usá-la no código. Por exemplo, se você quiser criar um comando para formatar JSON que chama o [`jq`](https://jqlang.github.io/jq/) instalado globalmente, pode escrever o seguinte comando:
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- não recarrega recursos, já que jq não toca no disco
      out = "capture" -- retorna saída textual em vez de nada
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Como este comando invoca um programa de shell de forma somente leitura (e notifica o editor sobre isso usando `reload_resources = false`), você obtém o benefício de tornar essa ação desfazível.

::: sidenote
Se você quiser distribuir seu editor script como uma biblioteca, talvez queira incluir o programa binário para as plataformas do editor dentro da dependência. Veja [Editor scripts em bibliotecas](#editor-scripts-in-libraries) para mais detalhes sobre como fazer isso.
:::

## Hooks de ciclo de vida {#lifecycle-hooks}

Há um arquivo de editor script tratado de forma especial: `hooks.editor_script`, localizado na raiz do seu projeto, no mesmo diretório que *game.project*. Este e somente este editor script receberá eventos de ciclo de vida do editor. Exemplo desse arquivo:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Decidimos limitar hooks de ciclo de vida a um único arquivo de editor script porque a ordem em que hooks de build acontecem é mais importante do que a facilidade de adicionar outra etapa de build. Comandos são independentes entre si, então não importa muito em que ordem eles são mostrados no menu; no fim, o usuário executa um comando específico que selecionou. Se fosse possível especificar hooks de build em diferentes editor scripts, isso criaria um problema: em que ordem os hooks executam? Você provavelmente quer criar checksums de conteúdo depois de compactá-lo... E ter um único arquivo que estabelece a ordem das etapas de build chamando explicitamente cada função de etapa é uma forma de resolver esse problema.

Hooks de ciclo de vida existentes que `/hooks.editor_script` pode especificar:
- `on_build_started(opts)` — executado quando o jogo é compilado para rodar localmente ou em algum alvo remoto usando as opções Project Build ou Debug Start. Suas alterações aparecerão no jogo compilado. Lançar um erro a partir deste hook abortará o build. `opts` é uma tabela que contém as seguintes chaves:
  - `platform` — uma string no formato `%arch%-%os%` descrevendo para qual plataforma está sendo compilado, atualmente sempre o mesmo valor de `editor.platform`.
- `on_build_finished(opts)` — executado quando o build termina, seja com sucesso ou falha. `opts` é uma tabela com as seguintes chaves:
  - `platform` — igual a `on_build_started`
  - `success` — se o build teve sucesso, `true` ou `false`
- `on_bundle_started(opts)` — executado quando você cria um pacote ou Build HTML5 version de um jogo. Assim como em `on_build_started`, alterações acionadas por este hook aparecerão no pacote, e erros abortarão o pacote. `opts` terá estas chaves:
  - `output_directory` — um caminho de arquivo apontando para um diretório com a saída do pacote, por exemplo `"/path/to/project/build/default/__htmlLaunchDir"`
  - `platform` — plataforma para a qual o jogo é empacotado. Veja uma lista de possíveis valores de plataforma no [manual do Bob](/manuals/bob).
  - `variant` — variante do pacote, `"debug"`, `"release"` ou `"headless"`
- `on_bundle_finished(opts)` — executado quando o pacote termina, com sucesso ou não. `opts` é uma tabela com os mesmos dados de `opts` em `on_bundle_started`, mais a chave `success`, indicando se o build teve sucesso.
- `on_target_launched(opts)` — executado quando o usuário inicia um jogo e ele começa com sucesso. `opts` contém uma chave `url` apontando para um serviço da engine iniciado, por exemplo, `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — executado quando o jogo iniciado é fechado, tem os mesmos opts de `on_target_launched`

Observe que hooks de ciclo de vida atualmente são um recurso apenas do editor, e não são executados pelo Bob ao empacotar pela linha de comando.

## Language servers

O editor oferece suporte a um subconjunto do [Language Server Protocol](https://microsoft.github.io/language-server-protocol/). Embora pretendamos expandir o suporte do editor a recursos LSP no futuro, atualmente ele só pode mostrar diagnósticos (isto é, lints) nos arquivos editados e fornecer completions.

Para definir o language server, você precisa editar a função `get_language_servers` do seu editor script assim:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
O editor iniciará o language server usando o `command` especificado, usando a entrada e saída padrão do processo do servidor para comunicação.

A tabela de definição do language server pode especificar:
- `languages` (obrigatório) — uma lista de linguagens nas quais o servidor tem interesse, conforme definido [aqui](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (extensões de arquivo também funcionam);
- `command` (obrigatório) - um array de comando e seus argumentos
- `watched_files` - um array de tabelas com chaves `pattern` (um glob) que acionarão a notificação [watched files changed](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) do servidor.

## Servidor HTTP

Toda instância em execução do editor tem um servidor HTTP rodando. O servidor pode ser estendido usando editor scripts. Para estender o servidor HTTP do editor, você precisa adicionar a função de editor script `get_http_server_routes` — ela deve retornar as rotas adicionais:
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Depois de recarregar os editor scripts, você verá a seguinte saída no console: `My route: http://0.0.0.0:12345/my-extension`. Se abrir esse link no navegador, verá sua mensagem `"Hello world!"`.

O argumento de entrada `request` é uma tabela Lua simples com informações sobre a requisição. Ela contém chaves como `path` (segmento do caminho da URL que começa com `/`), `method` da requisição (por exemplo, `"GET"`), `headers` (uma tabela com nomes de headers em minúsculas), e opcionalmente `query` (a query string) e `body` (se a rota define como interpretar o corpo). Por exemplo, se você quiser criar uma rota que aceita corpo JSON, defina-a com um parâmetro conversor `"json"`:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Você pode testar este endpoint na linha de comando usando `curl` e `jq`:
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
O caminho da rota oferece suporte a padrões que podem ser extraídos do caminho da requisição e fornecidos à função handler como parte da requisição, por exemplo:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Agora, se você abrir, por exemplo, `http://0.0.0.0:12345/my-extension/setting/project.title`, verá o título do seu jogo obtido do arquivo `/game.project`.

Além de um padrão de caminho de segmento único, você também pode corresponder ao restante do caminho da URL usando a sintaxe `{*name}`. Por exemplo, aqui está um endpoint simples de servidor de arquivos que serve arquivos a partir da raiz do projeto:
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Agora, abrir, por exemplo, `http://0.0.0.0:12345/my-extension/files/main/main.collection` no navegador exibirá o conteúdo do arquivo `main/main.collection`.

## Editor scripts em bibliotecas {#editor-scripts-in-libraries}

Você pode publicar bibliotecas para outras pessoas usarem que contenham comandos, e eles serão carregados automaticamente pelo editor. Hooks, por outro lado, não podem ser carregados automaticamente, pois precisam ser definidos em um arquivo na pasta raiz de um projeto, mas bibliotecas expõem apenas subpastas. Isso é intencional para dar mais controle sobre o processo de build: você ainda pode criar hooks de ciclo de vida como funções simples em arquivos `.lua`, para que usuários da sua biblioteca possam requerê-los e usá-los em seu `/hooks.editor_script`.

Observe também que, embora dependências sejam mostradas na visualização Assets, elas não existem como arquivos (são entradas em um arquivo zip). É possível fazer o editor extrair alguns arquivos das dependências para a pasta `build/plugins/`. Para isso, você precisa criar um arquivo `ext.manifest` na pasta da sua biblioteca e então criar a pasta `plugins/bin/${platform}` na mesma pasta onde o arquivo `ext.manifest` está localizado. Arquivos nessa pasta serão extraídos automaticamente para a pasta `/build/plugins/${extension-path}/plugins/bin/${platform}`, para que seus editor scripts possam referenciá-los.

## Preferências {#preferences}

Editor scripts podem definir e usar preferências — dados persistentes, não versionados, armazenados no computador do usuário. Essas preferências têm três características principais:
- tipadas: toda preferência tem uma definição de schema que inclui o tipo de dado e outros metadados, como valor padrão
- escopadas: preferências têm escopo por projeto ou por usuário
- aninhadas: toda chave de preferência é uma string separada por pontos, em que o primeiro segmento do caminho identifica um editor script, e o restante

Todas as preferências devem ser registradas definindo seu schema:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Depois que esse editor script é recarregado, o editor registra esse schema. Então o editor script pode obter e definir as preferências, por exemplo:
```lua
-- Obtém uma preferência específica
editor.prefs.get("my_json_formatter.indent.type")
-- Retorna: "spaces"

-- Obtém um grupo inteiro de preferências
editor.prefs.get("my_json_formatter")
-- Retorna:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Define múltiplas preferências aninhadas de uma vez
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Modos de execução {#execution-modes}

O runtime de editor script usa 2 modos de execução que são em grande parte transparentes para editor scripts: **immediate** e **long-running**.

O modo **immediate** é usado quando o editor precisa receber uma resposta do script o mais rápido possível. Por exemplo, callbacks `active` de comandos de menu são executados em modo immediate, porque essas verificações são realizadas na thread de UI do editor em resposta à interação do usuário com o editor e devem atualizar a UI dentro do mesmo frame.

O modo **long-running** é usado quando o editor não precisa de uma resposta instantânea do script. Por exemplo, callbacks `run` de comandos de menu são executados em modo **long-running**, permitindo que o script leve mais tempo para concluir seu trabalho.

Algumas funções que os editor scripts podem usar podem levar bastante tempo para rodar. Por exemplo, `editor.execute("git", "status", {reload_resources=false, out="capture"})` pode levar até um segundo em projetos suficientemente grandes. Para manter a responsividade e o desempenho do editor, funções que podem consumir tempo não são permitidas em contextos em que o editor precisa de uma resposta imediata. Tentar usar uma função desse tipo em um contexto immediate resultará em um erro: `Cannot use long-running editor function in immediate context`. Para resolver esse erro, evite usar essas funções em contextos immediate.

As seguintes funções são consideradas long-running e não podem ser usadas em modo immediate:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` e `file:write()`: essas funções modificam os arquivos no disco, fazendo o editor sincronizar sua árvore de recursos em memória com o estado do disco, o que pode levar segundos em projetos grandes.
- `editor.execute()`: a execução de comandos de shell pode levar uma quantidade imprevisível de tempo.
- `editor.transact()`: transações grandes em nodes amplamente referenciados podem levar centenas de milissegundos, o que é lento demais para a responsividade da UI.

Os seguintes contextos de execução de código usam modo immediate:
- Callbacks `active` de comandos de menu: o editor precisa de uma resposta do script dentro do mesmo frame de UI.
- Top-level de editor scripts: não esperamos que o ato de recarregar editor scripts tenha efeitos colaterais.

## Actions

::: sidenote
Antes, o editor interagia com a VM Lua de forma bloqueante, então havia um requisito rígido de que editor scripts não bloqueassem, já que algumas interações precisam ser feitas pela thread de UI do editor. Por esse motivo, não havia, por exemplo, `editor.execute()` e `editor.transact()`. Executar scripts e alterar o estado do editor era acionado retornando um array de "actions" a partir de hooks e handlers `run` de comandos.

Agora o editor interage com a VM Lua de forma não bloqueante, então essas actions não são mais necessárias: usar funções como `editor.execute()` é mais conveniente, conciso e poderoso. As actions agora estão **OBSOLETAS**, embora não tenhamos planos de removê-las.
:::

Editor scripts podem retornar um array de actions a partir da função `run` de um comando ou das funções hook de `/hooks.editor_script`. Essas actions então serão executadas pelo editor.

Action é uma tabela que descreve o que o editor deve fazer. Toda action tem uma chave `action`. Actions vêm em 2 variedades: desfazíveis e não desfazíveis.

### Actions desfazíveis

::: sidenote
Prefira usar `editor.transact()`.
:::

Uma action desfazível pode ser desfeita depois de executada. Se um comando retornar várias actions desfazíveis, elas são executadas juntas e desfeitas juntas. Você deve usar actions desfazíveis se puder. A desvantagem é que elas são mais limitadas.

Actions desfazíveis existentes:
- `"set"` — define uma propriedade de um node no editor para algum valor. Exemplo:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  A action `"set"` exige estas chaves:
  - `node_id` — userdata de id de node. Como alternativa, você pode usar aqui o caminho de recurso em vez do id de node recebido do editor, por exemplo `"/main/game.script"`;
  - `property` — uma propriedade de um node a definir, por exemplo `"text"`;
  - `value` — novo valor para uma propriedade. Para a propriedade `"text"`, deve ser uma string.

### Actions não desfazíveis

::: sidenote
Prefira usar `editor.execute()`.
:::

Uma action não desfazível limpa o histórico de undo; portanto, se quiser desfazer essa action, você terá que usar outros meios, como controle de versão.

Actions não desfazíveis existentes:
- `"shell"` — executa um script de shell. Exemplo:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- remove "/" inicial
    }
  }
  ```
  A action `"shell"` exige a chave `command`, que é um array de comando e seus argumentos.

### Misturando actions e efeitos colaterais

Você pode misturar actions desfazíveis e não desfazíveis. Actions são executadas sequencialmente; portanto, dependendo da ordem das actions, você acabará perdendo a capacidade de desfazer partes desse comando.

Em vez de retornar actions de funções que as esperam, você pode simplesmente ler e escrever arquivos diretamente usando `io.open()`. Isso acionará um recarregamento de recursos que limpará o histórico de undo.
