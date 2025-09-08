---
title: 编写代码
brief: 本手册简要介绍了如何在 Defold 中编写代码。
---

# 编写代码

虽然 Defold 允许您使用诸如瓦片地图和粒子效果编辑器等可视化工具创建大量游戏内容，但您仍然需要使用代码编辑器来创建游戏逻辑。游戏逻辑使用 [Lua 编程语言](https://www.lua.org/) 编写，而引擎本身的扩展则使用目标平台的原生语言编写。

## 编写 Lua 代码

Defold 使用 Lua 5.1 和 LuaJIT（取决于目标平台），在编写游戏逻辑时，您需要遵循这些特定 Lua 版本的语言规范。有关在 Defold 中使用 Lua 的更多详细信息，请参阅我们的 [Defold 中的 Lua 手册](/manuals/lua)。

## 使用可转换为 Lua 的其他语言

Defold 支持使用可生成 Lua 代码的转换器。安装转换器扩展后，您可以使用替代语言（例如 [Teal](https://github.com/defold/extension-teal)）来编写带有静态类型检查的 Lua。这是一个预览功能，存在一些限制：当前的转换器支持不会暴露在 Defold Lua 运行时中定义的模块和函数信息。这意味着使用像 `go.animate` 这样的 Defold API 将需要您自己编写外部定义。

## 编写原生代码

Defold 允许您使用原生代码扩展游戏引擎，以访问引擎本身未提供的平台特定功能。当 Lua 的性能不足时（例如资源密集型计算、图像处理等），您也可以使用原生代码。请参阅我们的 [原生扩展手册](/manuals/extensions/) 了解更多信息。

## 使用内置代码编辑器

Defold 有一个内置代码编辑器，允许您打开和编辑 Lua 文件（.lua）、Defold 脚本文件（.script、.gui_script 和 .render_script）以及编辑器本身不原生处理的任何其他扩展名文件。此外，该编辑器为 Lua 和脚本文件提供语法高亮。

![](/images/editor/code-editor.png)


### 代码补全

内置代码编辑器在编写代码时会显示函数的代码补全：

![](/images/editor/codecompletion.png)

按 <kbd>CTRL</kbd> + <kbd>Space</kbd> 将显示有关函数、参数和返回值的附加信息：

![](/images/editor/apireference.png)

### 代码检查配置

内置代码编辑器使用 [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) 和 [Lua 语言服务器](https://luals.github.io/wiki/diagnostics/) 进行代码检查。要配置 Luacheck，请在项目根目录创建一个 `.luacheckrc` 文件。您可以阅读 [Luacheck 配置页面](https://luacheck.readthedocs.io/en/stable/config.html) 了解可用选项列表。Defold 对 Luacheck 配置使用以下默认值：

```lua
unused_args = false      -- 不要对未使用的参数发出警告（常见于 .script 文件）
max_line_length = false  -- 不要对长行发出警告
ignore = {
    "611",               -- 行只包含空白字符
    "612",               -- 行尾包含空白字符
    "614"                -- 注释中包含尾随空白字符
},
```

## 使用外部代码编辑器

Defold 中的代码编辑器提供了编写代码所需的基本功能，但对于更高级的用例或拥有喜爱代码编辑器的专业用户，可以让 Defold 使用外部编辑器打开文件。在 [首选项窗口的代码选项卡下](/manuals/editor-preferences/#code)，可以定义在编辑代码时应使用的外部编辑器。

### Visual Studio Code - Defold Kit

Defold Kit 是一个 Visual Studio Code 插件，具有以下功能：

* 安装推荐的扩展
* Lua 高亮显示、自动补全和代码检查
* 将相关设置应用于工作区
* Defold API 的 Lua 注释
* 依赖项的 Lua 注释
* 构建和启动
* 使用断点进行调试
* 为所有平台打包
* 部署到已连接的移动设备

了解更多信息并从 [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) 安装 Defold Kit。


## 文档软件

社区创建的 API 参考包可用于 [Dash 和 Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417)。
