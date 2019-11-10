---
title: Defold GUI 文本节点
brief: 本教程介绍了如何在 GUI 场景中添加文本.
---

# GUI 文本节点

Defold 支持专门用于GUI场景中显示文本的GUI节点. 各种字体资源都可以被文本节点用以渲染文字.

## 添加文本节点

需要在文本节点使用的字体首先要应用到 GUI 组件之中. 或者使用右键点击 *Fonts* 文件夹, 使用 <kbd>GUI</kbd> 顶级菜单或者快捷键.

![Fonts](images/gui-text/fonts.png){srcset="images/gui-text/fonts@2x.png 2x"}

文本节点有一种特有属性:

*Font*
: 每个文本节点都要有 *字体* 属性设置.

*Text*
: 此属性设置节点显示的文字.

*Line Break*
: 文本对齐与锚点相关，此属性可以让文本溢出几行. 节点宽度决定文本在哪里换行.

## 对齐

你可以通过设置锚点来改变文本的对齐方式.

*Center*
: 如果锚点设置成 `Center`, `North` 或者 `South`, 则文本居中对齐.

*Left*
: 如果锚点设置成任何 `West` 模式, 则文本左对齐.

*Right*
: 如果锚点设置成任何 `East` 模式, 则文本右对齐.

![文本对齐](images/gui-text/align.png){srcset="images/gui-text/align@2x.png 2x"}

## 运行时修改文本

文本节点同样可以控制 size, pivot, color 之类的属性. 此外还有一些文本节点特有属性:

* 要改变文本字体, 使用 [`gui.set_font()`](/ref/gui/#gui.set_font) 方法.
* 要改变文本换行行为, 使用 [`gui.set_line_break()`](/ref/gui/#gui.set_line_break) 方法.
* 要改变文本文字, 使用 [`gui.set_text()`](/ref/gui/#gui.set_text) 方法.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```

