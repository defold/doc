---
title: Scripts de GUI no Defold
brief: Este manual explica scripting de GUI.
---

# Scripts de GUI

Para controlar a lógica da sua GUI e animar nodes, você usa scripts Lua. Scripts de GUI funcionam da mesma forma que scripts comuns de objetos de jogo, mas são salvos como um tipo de arquivo diferente e têm acesso a um conjunto diferente de funções: as funções do módulo `gui`.

## Adicionando um script a uma GUI

Para adicionar um script a uma GUI, primeiro crie um arquivo de script de GUI clicando com o botão direito em um local no navegador *Assets* e selecionando <kbd>New ▸ Gui Script</kbd> no menu de contexto popup.

O editor abre automaticamente o novo arquivo de script. Ele é baseado em um template e vem equipado com funções de ciclo de vida vazias, assim como scripts de objetos de jogo:

```lua
function init(self)
   -- Adicione código de inicialização aqui
   -- Remova esta função se não for necessária
end

function final(self)
   -- Adicione código de finalização aqui
   -- Remova esta função se não for necessária
end

function update(self, dt)
   -- Adicione código de atualização aqui
   -- Remova esta função se não for necessária
end

function on_message(self, message_id, message, sender)
   -- Adicione código de tratamento de mensagens aqui
   -- Remova esta função se não for necessária
end

function on_input(self, action_id, action)
   -- Adicione código de tratamento de entrada aqui
   -- Remova esta função se não for necessária
end

function on_reload(self)
   -- Adicione código de tratamento de entrada aqui
   -- Remova esta função se não for necessária
end
```

Para anexar o script a um componente GUI, abra o arquivo de protótipo do componente GUI (também conhecido como "prefab" ou "blueprint" em outras engines) e selecione a raiz no *Outline* para mostrar as *Properties* da GUI. Defina a propriedade *Script* para o arquivo de script.

![Script](images/gui-script/set_script.png)

Se o componente GUI tiver sido adicionado a um objeto de jogo em algum lugar do seu jogo, o script agora será executado.

## O namespace "gui"

Scripts de GUI têm acesso ao namespace `gui` e a [todas as funções gui](/ref/gui). O namespace `go` não está disponível, então você precisará separar a lógica de objeto de jogo em componentes de script e comunicar-se entre a GUI e os scripts de objeto de jogo. Qualquer tentativa de usar funções `go` causará um erro:

```lua
function init(self)
   local id = go.get_id()
end
```

```txt
ERROR:SCRIPT: /main/my_gui.gui_script:2: You can only access go.* functions and values from a script instance (.script file)
stack traceback:
   [C]: in function 'get_id'
   /main/my_gui.gui_script:2: in function </main/my_gui.gui_script:1>
```

## Passagem de mensagens

Qualquer componente GUI com um script anexado consegue se comunicar com outros objetos no ambiente de runtime do seu jogo por passagem de mensagens, comportando-se como qualquer outro componente de script.

Você endereça o componente GUI como faria com qualquer outro componente de script:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![passagem de mensagens](images/gui-script/message_passing.png)

## Endereçando nodes

Nodes GUI podem ser manipulados por um script de GUI anexado ao componente. Cada node deve ter um *Id* único definido no editor:

![passagem de mensagens](images/gui-script/node_id.png)

O *Id* permite que um script obtenha uma referência ao node e o manipule com as [funções do namespace gui](/ref/gui):

```lua
-- estende a barra de vida em 10 unidades
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Nodes criados dinamicamente

Para criar um novo node com script em runtime, você tem duas opções. A primeira é criar nodes do zero chamando as funções `gui.new_[type]_node()`. Elas retornam uma referência ao novo node que você pode usar para manipulá-lo:

```lua
-- Cria um novo node box
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- Cria um novo node text
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![node dinâmico](images/gui-script/dynamic_nodes.png)

A forma alternativa de criar novos nodes é clonar um node existente com a função `gui.clone()` ou uma árvore de nodes com a função `gui.clone_tree()`:

```lua
-- clona a barra de vida
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- clona a árvore de nodes do botão
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- obtém a nova raiz da árvore
local new_root = new_button_nodes["my_button"]

-- move a raiz (e filhos) 300 para a direita
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## Ids dinâmicos de nodes

Nodes criados dinamicamente não têm um id atribuído a eles. Isso é intencional. As referências retornadas por `gui.new_[type]_node()`, `gui.clone()` e `gui.clone_tree()` são a única coisa necessária para acessar os nodes, e você deve controlar essa referência.

```lua
-- Adiciona um node text
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contém a referência ao node.
-- O node não tem id, e isso não é problema. Não há motivo para chamar
-- gui.get_node() quando já temos a referência.
```
