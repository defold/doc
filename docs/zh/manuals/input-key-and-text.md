---
title: Defold 键盘按键和文本输入教程
brief: 本教程介绍了键盘按键和文本输入的功能.
---

::: sidenote
建议首先熟练掌握 Defold 中常规输入的消息处理方式, 例如输入消息获取以及脚本间输入消息广播顺序等. 关于输入系统详情请见 [输入系统教程](/manuals/input).
:::

# Key Triggers
键盘输入触发器用以把键盘按键输入映射为游戏需要的动作. 每个按键分别与动作一一对应, 比如箭头键和WASD键映射为角色移动. 如果需要文字输入, 要使用 text triggers (见下文).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

# Text Triggers
文本触发器用来读取输入的文字. 分为两种: text 和 marked text.

![](images/input/text_bindings.png)

## Text
`text` 捕获一般字符输入. 事件 `text` 项保存了输入的字符. 动作由按下按钮时触发, 不存在 `release` 和 `repeated` 事件.

  ```lua
  if action_id == hash("text") then
    -- 收集输入字符填充 "user" 节点...
    local node = gui.get_node("user")
    local name = gui.get_text(node)
    name = name .. action.text
    gui.set_text(node, name)
  end
  ```

## Marked text
`marked-text` 一般用于亚洲键盘可把多个按键事件合为一个输入事件. 比如说, iOS 里的 "Japanese-Kana" 键盘, 用户输入多个键时键盘上方就会显示出可供输入的文字或字符串.

![Input marked text](images/input/marked_text.png){srcset="images/input/marked_text@2x.png 2x"}

- 每个键被按下时触发事件, 动作 `text` 为目前已经输入了的字符串 (星号标记文本).
- 用户选择了要提交的文字时, 一个 `text` 类型动作被触发 (证明当前触发器配置正确). 而这个动作的 `text` 项保存了用户最终提交的文字.
