---
title: Скрипти GUI у Defold
brief: Цей посібник пояснює використання скриптів GUI.
---

# Скрипти GUI {#gui-scripts}

Для керування логікою GUI та анімації вузлів використовуйте скрипти Lua. Скрипти GUI працюють так само, як звичайні скрипти ігрових об’єктів (game objects), але зберігаються у файлах іншого типу й мають доступ до іншого набору функцій — функцій модуля `gui`.

## Додавання скрипта до GUI {#adding-a-script-to-a-gui}

Щоб додати скрипт до GUI, спочатку створіть файл скрипта GUI: <kbd>клацніть правою кнопкою миші</kbd> потрібне місце в оглядачі *Assets* і виберіть <kbd>New ▸ Gui Script</kbd> у контекстному меню.

Редактор автоматично відкриє новий файл скрипта. Він створений на основі шаблону й містить порожні функції життєвого циклу, як і скрипти ігрових об’єктів:

```lua
function init(self)
   -- Add initialization code here
   -- Remove this function if not needed
end

function final(self)
   -- Add finalization code here
   -- Remove this function if not needed
end

function update(self, dt)
   -- Add update code here
   -- Remove this function if not needed
end

function on_message(self, message_id, message, sender)
   -- Add message-handling code here
   -- Remove this function if not needed
end

function on_input(self, action_id, action)
   -- Add input-handling code here
   -- Remove this function if not needed
end

function on_reload(self)
   -- Add input-handling code here
   -- Remove this function if not needed
end
```

Щоб підключити скрипт до компонента GUI (GUI component), відкрийте файл прототипу компонента GUI (в інших рушіях такі прототипи також називають префабами (prefabs) або шаблонами (blueprints)) і виберіть кореневий елемент у *Outline*, щоб відкрити *Properties* GUI. У властивості *Script* вкажіть файл скрипта.

![Скрипт](images/gui-script/set_script.png)

Якщо компонент GUI додано до ігрового об’єкта десь у вашій грі, скрипт тепер виконуватиметься.

## Простір імен «gui» {#the-gui-namespace}

Скрипти GUI мають доступ до простору імен `gui` та [всіх функцій `gui`](/ref/gui). Простір імен `go` недоступний, тому потрібно винести логіку ігрових об’єктів в окремі компоненти-скрипти та налагодити обмін даними між GUI і скриптами ігрових об’єктів. Будь-яка спроба використати функції `go` спричинить помилку:

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

## Передавання повідомлень {#message-passing}

Будь-який компонент GUI з підключеним скриптом може взаємодіяти з іншими об’єктами в середовищі виконання гри через передавання повідомлень. Він поводитиметься як будь-який інший компонент-скрипт.

Адресуйте компонент GUI так само, як будь-який інший компонент-скрипт:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![Передавання повідомлень](images/gui-script/message_passing.png)

## Адресація вузлів {#addressing-nodes}

Вузлами GUI можна керувати зі скрипта GUI, підключеного до компонента. Кожен вузол повинен мати унікальний *Id*, який задається в редакторі:

![Передавання повідомлень](images/gui-script/node_id.png)

За допомогою *Id* скрипт може отримати посилання на вузол і керувати ним через [функції простору імен `gui`](/ref/gui):

```lua
-- extend the health bar by 10 units
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Динамічно створені вузли {#dynamically-created-nodes}

Є два способи створити новий вузол за допомогою скрипта під час виконання. Перший — створити вузол з нуля, викликавши функції `gui.new_[type]_node()`. Вони повертають посилання на новий вузол, за допомогою якого ви можете ним керувати:

```lua
-- Create a new box node
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- Create a new text node
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![Динамічний вузол](images/gui-script/dynamic_nodes.png)

Інший спосіб створити нові вузли — клонувати наявний вузол за допомогою функції `gui.clone()` або дерево вузлів за допомогою функції `gui.clone_tree()`:

```lua
-- clone the healthbar
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- clone button node-tree
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- get the new tree root
local new_root = new_button_nodes["my_button"]

-- move the root (and children) 300 to the right
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## Ідентифікатори динамічних вузлів {#dynamic-node-ids}

Динамічно створеним вузлам не призначаються ідентифікатори. Так задумано. Посилання, які повертають `gui.new_[type]_node()`, `gui.clone()` і `gui.clone_tree()`, — це все, що потрібно для доступу до вузлів, тому слід зберігати ці посилання.

```lua
-- Add a text node
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contains the reference to the node.
-- The node has no id, and that is fine. There's no reason why we want
-- to do gui.get_node() when we already have the reference.
```
