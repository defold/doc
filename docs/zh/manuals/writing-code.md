---
title: 编写代码
brief: 本教程简述了Defold中编写代码的事项.
---

# 编写代码

Defold 可以让你使用编辑器的可视工具来创建许多游戏必要的东西, 比如瓷砖地图和粒子特效, 但是对于游戏逻辑还是得写代码. 游戏逻辑使用 [Lua 语言](https://www.lua.org/) , 引擎扩展使用目标平台的原生开发语言.

## 编写Lua脚本

Defold 使用 Lua 5.1 和 LuaJIT (与目标平台相关) 并且需要遵循 Lua 该版本的书写规范来编写代码. 关于 Defold 中 Lua 使用详情请见 [Defold中Lua使用教程](/manuals/lua).

## 使用其他语言再转换为 Lua

从 1.8.1 版本开始, Defold 支持使用生成 Lua 代码的翻译器. 安装了翻译器扩展, 你就能使用其他语言 — 比如 [Teal](https://github.com/defold/extension-teal) — 写出带静态检查的 Lua. 这还是个预览功能, 它有如下限制: 目前翻译器支持不暴露模块和定义在 Defold Lua 运行环境中的函数. 这意味着使用 Defold APIs 类似 `go.animate` 需要你自己手动去写外部定义.

## 编写原生代码

Defold 允许使用原生代码来扩展游戏引擎以使用引擎所不具备的特定功能. 或者 Lua 性能不良时 (密集计算, 图像处理等) 考虑使用原生扩展. 详情请见 [原生扩展教程](/manuals/extensions/).

## 使用内置代码编辑器

Defold 中内建编辑器可以打开和编辑 Lua 文件 (.lua), Defold 脚本文件 (.script, .gui_script 与 .render_script) 或者其他各类文件. 但只对Lua和脚本文件提供代码高亮.

![](/images/editor/code-editor.png)


### 代码补全

内置代码编辑器写代码时会出现代码补全功能:

![](/images/editor/codecompletion.png)

按 <kbd>CTRL</kbd> + <kbd>Space</kbd> 会出现函数, 参数和返回值的相关信息:

![](/images/editor/apireference.png)

### 检查配置

内置代码编辑器使用 Luacheck 和 Lua language server 进行代码检查. 为了配置检查, 需要在项目根目录创建 .luacheckrc 文件. 可用的配置列表可以参考 Luacheck 配置页面. Defold 默认使用如下代码进行 Luacheck 配置:

```lua
unused_args = false      -- 未使用的参数不提示 (一般用于 .script 文件)
max_line_length = false  -- 超长行不提示
ignore = {
    "611",               -- 行内只包含空白
    "612",               -- 行尾包含空白
    "614"                -- 注释结尾包含空白
},
```

## 使用第三方代码编辑器

尽管 Defold 提供了编写脚本的基本功能, 但是对于需求更多功能的专业开发者来说还是希望让 Defold 使用自己喜欢的第三方编辑器. 在 [Code 页下的 Preferences 窗口 ](/manuals/editor-preferences/#code) 中可以指定使用第三方编辑器.

### Visual Studio Code - Defold Kit

Defold Kit 是一个 Visual Studio Code 插件, 其包含如下功能:

* 安装推荐扩展
* Lua 高光, 自动补全和 linting
* 将相关设置应用于工作区
* Defold API 的 Lua 提示
* 依赖库的 Lua 提示
* 编译和运行
* 断点和调试
* 跨平台编译
* 在连接的设备上运行应用

安装 Defold Kit 详情参考 [Visual Studio 商店页面](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## 文档工具

社区创建的 API 参考包可用于 [Dash 和 Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
