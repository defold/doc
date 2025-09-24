---
title: "编辑器脚本：UI"
brief: 本手册解释了如何使用Lua在编辑器中创建UI元素
---

# 编辑器脚本和UI

本手册解释了如何使用用Lua编写的编辑器脚本在编辑器中创建交互式UI元素。要开始使用编辑器脚本，请参阅[编辑器脚本手册](/manuals/editor-scripts)。您可以找到完整的编辑器API参考[这里](/ref/stable/editor-lua/)。目前，只能创建交互式对话框，尽管我们希望将来将UI脚本支持扩展到编辑器的其余部分。

## Hello world

所有与UI相关的功能都存在于`editor.ui`模块中。这是一个带有自定义UI的编辑器脚本的最简单示例，可以帮助您入门：
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

此代码片段定义了一个**View → Do with confirmation**命令。当您执行它时，您将看到以下对话框：

![Hello world dialog](images/editor_scripts/perform_action_dialog.png)

最后，在按<kbd>Enter</kbd>（或点击`Perform`按钮）后，您将在编辑器控制台中看到以下行：
```
Perform action:	true
```

## 基本概念

### 组件

编辑器提供了各种UI**组件**，可以组合这些组件来创建所需的UI。按照惯例，所有组件都使用一个称为**props**的表进行配置。组件本身不是表，而是编辑器用于创建UI的**不可变用户数据**。

### Props

**Props**是定义组件输入的表。Props应被视为不可变的：原地修改props表不会导致组件重新渲染，但使用不同的表会。当组件实例接收到与前一个表浅不相等的props表时，UI会更新。

### 对齐

当组件在UI中被分配一些边界时，它将消耗整个空间，但这并不意味着组件的可见部分会拉伸。相反，可见部分将占据它所需的空间，然后它将在分配的边界内对齐。因此，大多数内置组件定义了`alignment`属性。

例如，考虑这个标签组件：
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
可见部分是`Hello`文本，它在分配的组件边界内对齐：

![Alignment](images/editor_scripts/alignment.png)

## 内置组件

编辑器定义了各种可以一起使用来构建UI的内置组件。组件大致可以分为3类：布局、数据展示和输入。

### 布局组件

布局组件用于将其他组件彼此相邻放置。主要的布局组件是**`horizontal`**、**`vertical`**和**`grid`**。这些组件还定义了**padding**和**spacing**等属性，其中padding是从分配边界边缘到内容的空白空间，而spacing是子组件之间的空白空间：

![Padding and Spacing](images/editor_scripts/padding_and_spacing.png)

编辑器定义了`small`、`medium`和`large`padding和spacing常量。当涉及到spacing时，`small`用于单个UI元素的不同子元素之间的间距，`medium`用于单个UI元素之间的间距，而`large`是元素组之间的间距。默认spacing是`medium`。`large`的padding值表示从窗口边缘到内容的padding，`medium`是从重要UI元素边缘的padding，而`small`是上下文菜单和工具提示等小UI元素边缘的padding（尚未实现）。

**`horizontal`**容器将其子组件一个接一个地水平放置，始终使每个子组件的高度填充可用空间。默认情况下，每个子组件的宽度保持最小，但可以通过在子组件上将`grow`属性设置为`true`来使其占用尽可能多的空间。

**`vertical`**容器与水平容器类似，但是轴切换了。

最后，**`grid`**是一个容器组件，将其子组件布置在2D网格中，就像表格一样。网格中的`grow`设置适用于行或列，因此它不是在子组件上设置，而是在列配置表上设置。此外，网格中的子组件可以配置为使用`row_span`和`column_span`属性跨越多行或多列。网格对于创建多输入表单很有用：
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- 在对话框边缘添加padding
    columns = {{}, {grow = true}}, -- 使第2列增长
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
上面的代码将产生以下对话框表单：

![New Level Dialog](images/editor_scripts/new_level_dialog.png)

### 数据展示组件

编辑器定义了4个数据展示组件：
- **`label`** — 文本标签，旨在与表单输入一起使用。
- **`icon`** — 图标；目前，它只能用于呈现一小组预定义图标，但我们打算将来允许更多图标。
- **`heading`** — 文本元素，旨在呈现例如表单或对话框中的标题行文本。`editor.ui.HEADING_STYLE`枚举定义了各种标题样式，包括HTML的`H1`-`H6`标题，以及编辑器特定的`DIALOG`和`FORM`。
- **`paragraph`** — 文本元素，旨在呈现一段文本。与`label`的主要区别是段落支持自动换行：如果分配的边界在水平方向上太小，文本将换行，如果无法适应视图，可能会用`"..."`缩短。

### 输入组件

输入组件是为用户与UI交互而设计的。所有输入组件都支持`enabled`属性来控制交互是否启用，并定义各种回调属性，在交互时通知编辑器脚本。

如果您创建静态UI，只需定义简单修改局部变量的回调就足够了。对于动态UI和更高级的交互，请参阅[响应式](#reactivity)。

例如，可以像这样创建一个简单的静态新建文件对话框：
```lua
-- 初始文件名，将被对话框替换
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- 输入回调：
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
这是内置输入组件的列表：
- **`string_field`**、**`integer_field`**和**`number_field`**是单行文本字段的变体，允许编辑字符串、整数和数字。
- **`select_box`**用于通过下拉控件从预定义的选项数组中选择一个选项。
- **`check_box`**是一个带有`on_value_changed`回调的布尔输入字段
- **`button`**带有在按钮按下时调用的`on_press`回调。
- **`external_file_field`**是一个用于选择计算机上文件路径的组件。它由一个文本字段和一个打开文件选择对话框的按钮组成。
- **`resource_field`**是一个用于选择项目中资源的组件。

除按钮外的所有组件都允许设置一个`issue`属性，显示与组件相关的问题（`editor.ui.ISSUE_SEVERITY.ERROR`或`editor.ui.ISSUE_SEVERITY.WARNING`），例如：
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
当指定issue时，它会改变输入组件的外观，并添加带有问题消息的工具提示。

这是所有输入及其问题变体的演示：

![Inputs](images/editor_scripts/inputs_demo.png)

### 对话框相关组件

要显示对话框，您需要使用`editor.ui.show_dialog`函数。它需要一个**`dialog`**组件，该组件定义了Defold对话框的主要结构：`title`、`header`、`content`和`buttons`。对话框组件有点特殊：您不能将其用作另一个组件的子组件，因为它代表一个窗口，而不是UI元素。`header`和`content`是常规组件。

对话框按钮也很特殊：它们是使用**`dialog_button`**组件创建的。与常规按钮不同，对话框按钮没有`on_pressed`回调。相反，它们定义了一个`result`属性，该属性将在对话框关闭时由`editor.ui.show_dialog`函数返回。对话框按钮还定义了`cancel`和`default`布尔属性：带有`cancel`属性的按钮在用户按<kbd>Escape</kbd>或使用OS关闭按钮关闭对话框时触发，而`default`按钮在用户按<kbd>Enter</kbd>时触发。对话框按钮可以同时将`cancel`和`default`属性设置为`true`。

### 实用组件

此外，编辑器还定义了一些实用组件：
- **`separator`**是一条细线，用于分隔内容块
- **`scroll`**是一个包装组件，当包装的组件不适合分配的空间时显示滚动条

## 响应式

由于组件是**不可变用户数据**，因此在创建后无法更改它们。那么如何使UI随时间变化呢？答案是：**响应式组件**。

::: sidenote
编辑器脚本UI的灵感来自[React](https://react.dev/)库，因此了解响应式UI和React hooks将有所帮助。
:::

在最简单的术语中，响应式组件是一个带有Lua函数的组件，该函数接收数据（props）并返回视图（另一个组件）。响应式组件函数可以使用**hooks**：`editor.ui`模块中的特殊函数，为您的组件添加响应式功能。按照惯例，所有hooks的名称都以`use_`开头。

要创建响应式组件，请使用`editor.ui.component()`函数。

让我们看这个示例——一个新建文件对话框，只有当输入的文件名不为空时才允许创建文件：

```lua
-- 1. dialog是一个响应式组件
local dialog = editor.ui.component(function(props)
    -- 2. 组件定义了一个本地状态（文件名），默认为空字符串
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. 输入+Enter更新本地状态
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. 当名称存在时启用创建
                enabled = name ~= "",
                default = true,
                -- 5. 结果是名称
                result = name
            })
        }
    })
end)

-- 6. show_dialog将返回非空文件名或在取消时返回nil
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

当您执行运行此代码的菜单命令时，编辑器将显示一个在开始时禁用`"Create File"`对话框的对话框，但是当您输入名称并按<kbd>Enter</kbd>时，它将变为启用状态：

![New File Dialog](images/editor_scripts/reactive_new_file_dialog.png)

那么，它是如何工作的呢？在第一次渲染时，`use_state` hook创建一个与组件关联的本地状态，并返回它以及状态的setter。当调用setter函数时，它会安排组件重新渲染。在随后的重新渲染中，组件函数再次被调用，`use_state`返回更新的状态。然后，组件函数返回的新视图组件与旧组件进行差异比较，并在检测到更改的地方更新UI。

这种响应式方法大大简化了构建交互式UI并使其保持同步：而不是在用户输入时显式更新所有受影响的UI组件，视图被定义为输入（props和本地状态）的纯函数，编辑器自己处理所有更新。

### 响应式规则

编辑器期望响应式函数组件表现良好才能正常工作：

1. 组件函数必须是纯函数。不保证何时或多久调用一次组件函数。所有副作用都应该在渲染之外，例如在回调中
2. Props和本地状态必须是不可变的。不要改变props。如果您的本地状态是一个表，不要原地修改它，而是在状态需要更改时创建一个新表并将其传递给setter。
3. 组件函数必须在每次调用时以相同的顺序调用相同的hooks。不要在循环中、条件块中、提前返回后等调用hooks。最佳实践是在组件函数的开头调用hooks，在任何其他代码之前。
4. 只从组件函数调用hooks。Hooks在响应式组件的上下文中工作，因此只允许在组件函数中（或由组件函数直接调用的另一个函数中）调用它们。

### Hooks

::: sidenote
如果您熟悉[React](https://react.dev/)，您会注意到编辑器中的hooks在hook依赖项方面具有稍微不同的语义。
:::

编辑器定义了2个hooks：**`use_memo`**和**`use_state`**。

### **`use_state`**

本地状态可以通过两种方式创建：使用默认值或使用初始化器函数：
```lua
-- 默认值
local enabled, set_enabled = editor.ui.use_state(true)
-- 初始化器函数+参数
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
类似地，可以使用新值或更新器函数调用setter：
```lua
-- 更新器函数
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

最后，状态可以被**重置**。当`editor.ui.use_state()`的任何参数更改时，状态会重置，使用`==`进行检查。因此，您不能使用字面量表或字面量初始化器函数作为`use_state` hook的参数：这会导致每次重新渲染时状态重置。举例说明：
```lua
-- ❌ 错误：字面量表初始化器在每次重新渲染时导致状态重置
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ 正确：在组件函数外部使用初始化器函数创建表状态
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...稍后，在组件函数中：
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ 错误：字面量初始化器函数在每次重新渲染时导致状态重置
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ 正确：使用引用的初始化器函数创建状态
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

您可以使用`use_memo` hook来提高性能。通常在渲染函数中执行一些计算，例如检查用户输入是否有效。`use_memo` hook可用于检查计算函数的参数是否更改比调用计算函数更便宜的情况。hook将在第一次渲染时调用计算函数，如果`use_memo`的所有参数都未更改，则在随后的重新渲染中重用计算值：
```lua
-- 组件函数外的验证函数
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...稍后，在组件函数中
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
在这个例子中，密码验证将在每次密码更改时运行（例如在密码字段中输入时），但在用户名更改时不会运行。

`use_memo`的另一个用例是创建然后在输入组件上使用的回调，或者当本地创建的函数用作另一个组件的prop值时——这可以防止不必要的重新渲染。