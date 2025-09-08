---
title: 键和文本输入在Defold中
brief: 本手册解释了键和文本输入的工作原理。
---

::: sidenote
建议您先熟悉Defold中输入的一般工作方式，如何接收输入以及输入在脚本文件中的接收顺序。有关输入系统的更多信息，请参阅[输入系统概述手册](/manuals/input)。
:::

# 键触发器
键触发器允许您将单个键的键盘输入绑定到游戏操作。每个键分别映射到相应的操作。键触发器用于将特定按钮绑定到特定功能，例如使用箭头键或WASD键进行角色移动。如果您需要读取任意键盘输入，请使用文本触发器（见下文）。

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- 开始向左移动
        elseif action.released then
            -- 停止向左移动
        end
    end
end
```

# 文本触发器
文本触发器用于读取任意文本输入。有两种类型的文本触发器：文本和标记文本。

![](images/input/text_bindings.png)

## 文本
`text`捕获普通文本输入。它将操作表的`text`字段设置为包含键入字符的字符串。该操作仅在按下按钮时触发，不会发送`release`或`repeated`操作。

  ```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- 将键入的字符连接到"user"节点...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end 
  ```

## 标记文本
`marked-text`主要用于亚洲键盘，其中多次按键可以映射到单个输入。例如，使用iOS的"Japanese-Kana"键盘，用户可以键入组合，键盘顶部将显示可输入的符号或符号序列。

![Input marked text](images/input/marked_text.png)

- 每次按键生成单独的操作，并将操作字段`text`设置为当前输入的符号序列（"标记文本"）。
- 当用户选择符号或符号组合时，会发送单独的`text`类型触发器操作（前提是在输入绑定列表中设置了一个）。单独的操作将操作字段`text`设置为最终的符号序列。
