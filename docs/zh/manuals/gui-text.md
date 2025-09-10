---
title: Defold GUI文本节点
brief: 本手册描述了如何在GUI场景中添加文本。
---

# GUI文本节点

Defold支持一种特定类型的GUI节点，允许在GUI场景中渲染文本。项目中添加的任何字体资源都可以用于文本节点渲染。

## 添加文本节点

您希望在GUI文本节点中使用的字体必须添加到GUI组件中。可以右键单击*Fonts*文件夹，使用<kbd>GUI</kbd>顶部菜单或按相应的键盘快捷键。

![Fonts](images/gui-text/fonts.png)

文本节点具有一组特殊属性：

*Font*
: 您创建的任何文本节点都必须设置*Font*属性。

*Text*
: 此属性包含显示的文本。

*Line Break*
: 文本对齐遵循 pivot 设置，设置此属性允许文本流到多行。节点的宽度决定文本将在何处换行。

## 对齐

通过设置节点 pivot，您可以更改文本的对齐模式。

*Center*
: 如果 pivot 设置为`Center`、`North`或`South`，则文本居中对齐。

*Left*
: 如果 pivot 设置为任何`West`模式，则文本左对齐。

*Right*
: 如果 pivot 设置为任何`East`模式，则文本右对齐。

![文本对齐](images/gui-text/align.png)

## 运行时修改文本节点

文本节点响应任何通用的节点操作函数，用于设置大小、pivot、颜色等。存在一些仅用于文本节点的函数：

* 要更改文本节点的字体，请使用[`gui.set_font()`](/ref/gui/#gui.set_font)函数。
* 要更改文本节点的换行行为，请使用[`gui.set_line_break()`](/ref/gui/#gui.set_line_break)函数。
* 要更改文本节点的内容，请使用[`gui.set_text()`](/ref/gui/#gui.set_text)函数。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```

